import asyncio
import os
import sqlite3
import tempfile
import unittest

from osos import iec62056 as iec
import osos_server

VERI = (
    "0.0.0(400106101)\r\n"
    "0.9.1(15:03:35)\r\n"
    "1.8.0(012345.678*kWh)\r\n"
    "1.8.1(006000.000*kWh)\r\n"
    "1.8.2(003000.000*kWh)\r\n"
    "1.8.3(003345.678*kWh)\r\n"
    "1.6.0(001.234*kW)(25-12-23 14:00)\r\n"
    "!\r\n"
)


def blok(metin: str) -> bytes:
    govde = metin.encode() + bytes([iec.ETX])
    return bytes([iec.STX]) + govde + bytes([iec.bcc(govde)])


class ProtokolTest(unittest.TestCase):
    def test_bcc_ve_ayirma(self):
        b = blok(VERI)
        icerik, ok = iec.veri_blogu_ayir(b"cop" + b)
        self.assertTrue(ok)
        self.assertEqual(icerik.decode(), VERI)

    def test_bozuk_bcc(self):
        b = bytearray(blok(VERI))
        b[-1] ^= 0x01
        self.assertFalse(iec.veri_blogu_ayir(bytes(b))[1])

    def test_eksik_blok(self):
        self.assertIsNone(iec.veri_blogu_ayir(blok(VERI)[:-1]))

    def test_obis(self):
        d = iec.obis_ayristir(VERI)
        self.assertIn(("1.8.0", "012345.678", "kWh"), d)
        self.assertIn(("1.6.0", "001.234", "kW"), d)
        self.assertIn(("1.6.0", "25-12-23 14:00", ""), d)
        self.assertEqual(iec.obis_kisa("1-0:1.8.0*255"), "1.8.0")

    def test_kimlik(self):
        k = iec.Kimlik("/LUN5LUNA-X5\r\n")
        self.assertEqual((k.uretici, k.baud), ("LUN", 9600))

    def test_parity(self):
        veri = b"/?!\r\n"
        self.assertEqual(iec.parity_temizle(iec.parity_ekle(veri)), veri)
        self.assertEqual(iec.parity_ekle(b"/")[0], ord("/") | 0x80)  # '/' 5 adet 1 bit


class SunucuTest(unittest.TestCase):
    def test_modem_uzerinden_okuma(self):
        tmp = tempfile.mkdtemp()
        db = os.path.join(tmp, "t.db")
        args = osos_server.arguman_ayristir([
            "--host", "127.0.0.1", "--port", "0", "--oku", "--bekle", "0.3",
            "--db", db, "--log-klasoru", os.path.join(tmp, "logs"),
        ])

        async def sahte_modem(port):
            r, w = await asyncio.open_connection("127.0.0.1", port)
            w.write(b"IMEI:358741052021927;ICCID:899002930158646081\r\n")
            await w.drain()
            self.assertEqual(await r.readuntil(b"\n"), b"/?!\r\n")
            w.write(b"/KHL5X5\r\n")
            await w.drain()
            onay = await r.readuntil(b"\n")
            self.assertEqual(onay, bytes([iec.ACK]) + b"000\r\n")  # 300 baud'da kal
            b = blok(VERI)
            w.write(b[:20])  # parça parça gelsin
            await w.drain()
            await asyncio.sleep(0.1)
            w.write(b[20:])
            await w.drain()
            await asyncio.sleep(0.3)
            w.close()

        async def calistir():
            srv = await osos_server.Sunucu(args).baslat()
            port = srv.sockets[0].getsockname()[1]
            async with srv:
                await asyncio.wait_for(sahte_modem(port), 10)
                await asyncio.sleep(0.3)

        asyncio.run(calistir())

        con = sqlite3.connect(db)
        imei, iccid = con.execute("SELECT imei, iccid FROM baglantilar").fetchone()
        self.assertEqual((imei, iccid), ("358741052021927", "899002930158646081"))
        kimlik, bcc_ok, okuma_imei = con.execute(
            "SELECT sayac_kimlik, bcc_dogru, imei FROM okumalar").fetchone()
        self.assertEqual((kimlik, bcc_ok, okuma_imei), ("/KHL5X5", 1, "358741052021927"))
        self.assertEqual(
            con.execute("SELECT deger FROM degerler WHERE obis='1.8.0'").fetchone()[0], "012345.678")


if __name__ == "__main__":
    unittest.main()
