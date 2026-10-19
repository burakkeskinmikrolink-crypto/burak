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



class EnvanterPanelTest(unittest.TestCase):
    def test_envanter_ve_panel(self):
        import envanter_yukle
        import osos_panel
        from osos import veritabani

        db = veritabani.baglan(":memory:")
        modemler = ("MÜŞTERİ\tMODEM\tSERİ NO\tGSM NO\tIP\tPORT\tAÇIKLAMA\n"
                    "VODAFONE\tM-B34_M1523_BOGAZICI_KAPSAL\t358741052021927\t5465295149\t\t\t\n"
                    "VODAFONE\tM-GL34_01078_KUCUKBEBEK2_SE\t358741051624226\t5497132927\t\t\t\n")
        sayaclar = ("SAYAÇ;SERİ NO;OKUMA ZAMANI\n"
                    "S-B34_M1523_BOGAZICI_KAPSAL;400106101;23.12.2025 15:03:35\n")
        self.assertEqual(envanter_yukle.yukle(db, modemler)[:2], ("modem", 2))
        self.assertEqual(envanter_yukle.yukle(db, sayaclar)[:2], ("sayac", 1))
        envanter_yukle.yukle(db, modemler)  # tekrar yükleme çoğaltmaz
        self.assertEqual(db.execute("SELECT COUNT(*) FROM modemler").fetchone()[0], 2)

        db.execute("INSERT INTO baglantilar (baslangic, imei) VALUES (datetime('now','localtime'), ?)",
                   ("358741052021927",))
        cur = db.execute("INSERT INTO okumalar (zaman, imei, bcc_dogru) VALUES (datetime('now','localtime'), ?, 1)",
                         ("358741052021927",))
        db.execute("INSERT INTO degerler VALUES (?, '1.8.0', '012345.678', 'kWh')", (cur.lastrowid,))
        liste = {x["imei"]: x for x in osos_panel.saha_listesi(db, 26)}
        k = liste["358741052021927"]
        self.assertEqual((k["durum"], k["endeks"], k["sayac"]), ("ok", "012345.678", "400106101"))
        self.assertEqual(liste["358741051624226"]["durum"], "hic")
        self.assertIn("BOGAZICI", osos_panel.ana_sayfa(db, 26))
        self.assertIn("012345.678", osos_panel.modem_sayfasi(db, "358741052021927"))
        self.assertIn("Okunuyor", osos_panel.okumalar_csv(db, 26).decode("utf-8"))


class DurumListesiTest(unittest.TestCase):
    def test_enerclever_xls(self):
        import envanter_yukle
        import osos_panel
        from osos import veritabani

        xls = ("<div><table><tr><th>WorkGroupName</th><th>B&#246;lge</th><th>&#350;ube Kodu</th>"
               "<th>Saya&#231; Durumu</th><th>Modem Seri No</th><th>Saya&#231; Seri No</th>"
               "<th>Son Okuma Tarihi</th><th>Saya&#231; Ad&#305;</th></tr>"
               "<tr><td>Genel</td><td>&#304;stanbul-Avrupa</td><td>1T-N1523</td>"
               "<td>Veri G&#246;nderimi Yok</td><td>&#39;358741052021927&#39;</td><td>&#39;400106101&#39;</td>"
               "<td></td><td>S-B34_M1523_BOGAZICI_KAPSAL</td></tr>"
               "<tr><td>Genel</td><td>&#304;stanbul-Avrupa</td><td>1T-X1</td>"
               "<td>Veri G&#246;nderiliyor</td><td>&#39;358741052021927&#39;</td><td>&#39;17000001&#39;</td>"
               "<td>20.10.2026 00:31:23</td><td>S-B34_IKINCI</td></tr></table></div>")
        db = veritabani.baglan(":memory:")
        self.assertEqual(envanter_yukle.yukle(db, xls)[:2], ("durum", 2))
        s = db.execute("SELECT * FROM sayaclar WHERE seri_no='400106101'").fetchone()
        self.assertEqual((s["modem_imei"], s["eski_durum"], s["bolge"], s["sube_kodu"]),
                         ("358741052021927", "Veri Gönderimi Yok", "İstanbul-Avrupa", "1T-N1523"))
        # İki sayaçlı modem panelde tek satır olmalı
        liste = osos_panel.saha_listesi(db, 26)
        self.assertEqual(len(liste), 1)


class EnerjiVeOlcumTest(unittest.TestCase):
    def test_enerji_raporu_ve_fazlar(self):
        import envanter_yukle
        import osos_panel
        from osos import olcumler, veritabani

        rapor = ("Yıl\n\nDeğer;;Okuma Tipi\n;;Toplam Tüketim\n;;2026/10\n"
                 "Sayaç No;Sayaç Adı;Modem No;Modem;SIMKART GSM No;Alt Bölge;Sehir;Saha Adi;Saha Id;kWh\n"
                 "400106101;S-B34_M1523_BOGAZICI_KAPSAL;358741052021927;M-B34_M1523_BOGAZICI_KAPSAL;"
                 "5465295149;İstanbul Avrupa;İstanbul;B34_M1523_BOGAZICI_KAPSAL;1T-N1523;120,5\n"
                 "17000002;S-X;1;M-X;;;;;;5\n")
        db = veritabani.baglan(":memory:")
        self.assertEqual(envanter_yukle.yukle(db, rapor)[:2], ("enerji", 2))
        self.assertIsNone(db.execute("SELECT 1 FROM modemler WHERE imei='1'").fetchone())
        self.assertEqual(db.execute("SELECT gsm FROM modemler").fetchone()[0], "5465295149")

        def okuma(zaman, endeks, l1):
            cur = db.execute("INSERT INTO okumalar (zaman, imei, bcc_dogru) VALUES (?, '358741052021927', 1)",
                             (zaman,))
            db.executemany("INSERT INTO degerler VALUES (?,?,?,?)", [
                (cur.lastrowid, "1.8.0", endeks, "kWh"), (cur.lastrowid, "32.7.0", l1, "V"),
                (cur.lastrowid, "52.7.0", "230.0", "V"), (cur.lastrowid, "72.7.0", "231.0", "V")])
        okuma("2026-09-30 23:00:00", "001000.000", "229.0")
        okuma("2026-10-15 12:00:00", "001050.000", "229.0")
        okuma("2026-10-31 23:00:00", "001100.250", "000.0")
        satir = [x for x in osos_panel.enerji_raporu(db, "2026-10") if x["Sayaç No"] == "400106101"][0]
        self.assertEqual((satir["kWh"], satir["EnerClever kWh"], satir["SIMKART GSM No"]),
                         (100.25, 120.5, "5465295149"))
        self.assertIn("Sayaç No;Sayaç Adı", osos_panel.rapor_csv(db, "2026-10").decode("utf-8"))

        son = osos_panel.son_degerler(db, 3)
        self.assertEqual(olcumler.faz_durumu(son), ["yok", "ok", "ok"])
        self.assertTrue(any("L1 fazı yok" in m for _, m in olcumler.alarmlar(son)))
        sayfa = osos_panel.modem_sayfasi(db, "358741052021927")
        self.assertIn("L1 fazı yok", sayfa)
        self.assertIn("<svg", sayfa)


if __name__ == "__main__":
    unittest.main()
