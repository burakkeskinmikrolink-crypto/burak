#!/usr/bin/env python3
"""OSOS merkez sunucusu: modemlerin bağlandığı TCP (isteğe bağlı UDP) dinleyici.

Sahadaki ECL-BGS5 modemler açılınca bir sunucuya (bugün 10.124.132.180:80)
kendileri bağlanıyor. Modemin adresini bu sunucuya çevirdiğimizde:

  1. Modemin bağlanırken gönderdiği her byte'ı kaydeder (hex + metin).
     Modemin kendini nasıl tanıttığı (IMEI, ICCID, paket yapısı) buradan çıkar.
  2. --oku verilirse modem şeffaf köprü varsayılır: sayaca bağlantı
     üzerinden IEC 62056-21 isteği gönderilir, hız 300 baud'da tutulur
     (modemin seri portu okuma ortasında hız değiştiremez), gelen endeksler
     SQLite veritabanına yazılır.

Kullanım:
    python osos_server.py --port 80                 # sadece dinle ve kaydet
    python osos_server.py --port 80 --oku           # bağlanan modemden sayacı oku
    python osos_server.py --port 80 --oku --periyot 60   # bağlantı açık kaldıkça saatte bir oku
    python osos_server.py --port 80 --udp           # UDP gelirse onu da kaydet

Sorgu:
    python osos_server.py --rapor                   # son okumaları listele
"""

import argparse
import asyncio
import datetime as dt
import os
import re
import sqlite3
import sys

from osos import iec62056 as iec

IMEI_RE = re.compile(rb"(?<!\d)(35\d{13}|86\d{13})(?!\d)")
ICCID_RE = re.compile(rb"(?<!\d)(89\d{16,18})(?!\d)")


def simdi() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# --------------------------------------------------------------------------
# Kayıt
# --------------------------------------------------------------------------

class Kayit:
    def __init__(self, db_yolu: str, log_klasoru: str):
        self.log_klasoru = log_klasoru
        os.makedirs(log_klasoru, exist_ok=True)
        self.db = sqlite3.connect(db_yolu)
        self.db.executescript(
            """
            CREATE TABLE IF NOT EXISTS baglantilar (
                id INTEGER PRIMARY KEY, baslangic TEXT, bitis TEXT,
                ip TEXT, port INTEGER, protokol TEXT,
                imei TEXT, iccid TEXT, ilk_veri_hex TEXT, toplam_byte INTEGER
            );
            CREATE TABLE IF NOT EXISTS okumalar (
                id INTEGER PRIMARY KEY, zaman TEXT, baglanti_id INTEGER,
                imei TEXT, sayac_kimlik TEXT, bcc_dogru INTEGER, ham TEXT
            );
            CREATE TABLE IF NOT EXISTS degerler (
                okuma_id INTEGER, obis TEXT, deger TEXT, birim TEXT
            );
            """
        )
        self.db.commit()

    def log(self, metin: str):
        satir = f"{simdi()}  {metin}"
        print(satir, flush=True)
        dosya = os.path.join(self.log_klasoru, dt.date.today().isoformat() + ".log")
        with open(dosya, "a", encoding="utf-8") as f:
            f.write(satir + "\n")

    def baglanti_ac(self, ip, port, protokol) -> int:
        cur = self.db.execute(
            "INSERT INTO baglantilar (baslangic, ip, port, protokol, toplam_byte) VALUES (?,?,?,?,0)",
            (simdi(), ip, port, protokol),
        )
        self.db.commit()
        return cur.lastrowid

    def baglanti_guncelle(self, bid, **alanlar):
        if not alanlar:
            return
        kume = ", ".join(f"{k}=?" for k in alanlar)
        self.db.execute(f"UPDATE baglantilar SET {kume} WHERE id=?", (*alanlar.values(), bid))
        self.db.commit()

    def okuma_yaz(self, bid, imei, kimlik, bcc_ok, blok: bytes) -> int:
        metin = blok.decode("ascii", "replace")
        cur = self.db.execute(
            "INSERT INTO okumalar (zaman, baglanti_id, imei, sayac_kimlik, bcc_dogru, ham) VALUES (?,?,?,?,?,?)",
            (simdi(), bid, imei, kimlik, int(bcc_ok), metin),
        )
        oid = cur.lastrowid
        self.db.executemany(
            "INSERT INTO degerler (okuma_id, obis, deger, birim) VALUES (?,?,?,?)",
            [(oid, a, d, b) for a, d, b in iec.obis_ayristir(metin)],
        )
        self.db.commit()
        return oid


def gorunur(veri: bytes) -> str:
    """Byte'ları okunur hale getirir: yazdırılabilirler olduğu gibi, diğerleri <xx>."""
    return "".join(chr(b) if 32 <= b < 127 else f"<{b:02x}>" for b in veri)


# --------------------------------------------------------------------------
# Modem bağlantısı
# --------------------------------------------------------------------------

class Oturum:
    def __init__(self, sunucu, reader, writer):
        self.s = sunucu
        self.reader = reader
        self.writer = writer
        self.tampon = b""
        self.yeni_veri = asyncio.Event()
        self.son_veri = asyncio.get_running_loop().time()
        self.toplam = 0
        self.ilk_veri = b""
        self.imei = None
        self.iccid = None
        ip, port = writer.get_extra_info("peername")[:2]
        self.etiket = f"{ip}:{port}"
        self.bid = sunucu.kayit.baglanti_ac(ip, port, "tcp")

    def log(self, metin):
        kim = self.imei or self.etiket
        self.s.kayit.log(f"[{kim}] {metin}")

    async def dinle(self):
        while True:
            parca = await self.reader.read(4096)
            if not parca:
                return
            self.toplam += len(parca)
            self.son_veri = asyncio.get_running_loop().time()
            self.log(f"<< {len(parca)} byte  hex={parca.hex()}  metin={gorunur(parca)!r}")
            if len(self.ilk_veri) < 512:
                self.ilk_veri += parca[: 512 - len(self.ilk_veri)]
                self.kimlik_bul()
            self.tampon += parca
            self.yeni_veri.set()

    def kimlik_bul(self):
        guncelle = {"ilk_veri_hex": self.ilk_veri.hex()}
        if not self.imei:
            m = IMEI_RE.search(self.ilk_veri)
            if m:
                self.imei = m.group(1).decode()
                guncelle["imei"] = self.imei
                self.log(f"IMEI bulundu: {self.imei}")
        if not self.iccid:
            m = ICCID_RE.search(self.ilk_veri)
            if m:
                self.iccid = m.group(1).decode()
                guncelle["iccid"] = self.iccid
                self.log(f"ICCID bulundu: {self.iccid}")
        self.s.kayit.baglanti_guncelle(self.bid, **guncelle)

    async def gonder(self, veri: bytes):
        if self.s.args.parity_ekle:
            veri = iec.parity_ekle(veri)
        self.log(f">> {len(veri)} byte  metin={gorunur(veri)!r}")
        self.writer.write(veri)
        await self.writer.drain()

    async def bekle(self, kosul, sure: float) -> bool:
        """Tampon kosul(tampon) True dönene kadar bekler."""
        loop = asyncio.get_running_loop()
        bitis = loop.time() + sure
        while not kosul(iec.parity_temizle(self.tampon)):
            kalan = bitis - loop.time()
            if kalan <= 0:
                return False
            self.yeni_veri.clear()
            try:
                await asyncio.wait_for(self.yeni_veri.wait(), kalan)
            except asyncio.TimeoutError:
                return False
        return True

    async def sessizlik_bekle(self, saniye: float):
        loop = asyncio.get_running_loop()
        while loop.time() - self.son_veri < saniye:
            await asyncio.sleep(0.2)

    async def sayac_oku(self) -> bool:
        a = self.s.args
        self.tampon = b""
        await self.gonder(iec.istek(a.adres))

        def kimlik_geldi(t):
            i = t.find(b"/")
            return i >= 0 and b"\n" in t[i:]

        if not await self.bekle(kimlik_geldi, a.kimlik_sure):
            self.log("Sayaç kimlik göndermedi (modem şeffaf köprü değil ya da RS485 tarafı sorunlu)")
            return False
        t = iec.parity_temizle(self.tampon)
        i = t.find(b"/")
        satir = t[i : t.find(b"\n", i)].decode("ascii", "replace")
        kimlik = iec.Kimlik(satir)
        self.log(f"Sayaç kimliği: {kimlik.ham}  (üretici {kimlik.uretici}, önerdiği {kimlik.baud} baud)")

        self.tampon = b""
        # Modemin seri portu hız değiştiremeyeceği için varsayılan: 300 baud'da kal
        hiz = kimlik.hiz_harfi if a.hiz_degistir else "0"
        await asyncio.sleep(0.3)
        await self.gonder(iec.ack(hiz))

        ok = await self.bekle(lambda t: iec.veri_blogu_ayir(t) is not None, a.veri_sure)
        t = iec.parity_temizle(self.tampon)
        if not ok:
            self.log(f"Veri bloğu tamamlanmadı ({len(t)} byte geldi)")
            return False
        blok, bcc_ok = iec.veri_blogu_ayir(t)
        oid = self.s.kayit.okuma_yaz(self.bid, self.imei, kimlik.ham, bcc_ok, blok)
        degerler = iec.obis_ayristir(blok.decode("ascii", "replace"))
        ozet = ", ".join(
            f"{iec.obis_kisa(o)}={d}{b}" for o, d, b in degerler
            if iec.obis_kisa(o) in ("1.8.0", "1.8.1", "1.8.2", "1.8.3")
        )
        self.log(f"OKUMA #{oid}: {len(blok)} byte, BCC {'doğru' if bcc_ok else 'HATALI'}, {ozet}")
        return True

    async def calis(self):
        self.log("Bağlantı açıldı")
        dinleyici = asyncio.create_task(self.dinle())
        try:
            if self.s.args.oku:
                await self.sessizlik_bekle(self.s.args.bekle)
                while not dinleyici.done():
                    try:
                        await self.sayac_oku()
                    except (ConnectionError, OSError) as e:
                        self.log(f"Okuma sırasında bağlantı hatası: {e}")
                        break
                    if not self.s.args.periyot:
                        break
                    await asyncio.wait({dinleyici}, timeout=self.s.args.periyot * 60)
            await dinleyici
        except (ConnectionError, OSError) as e:
            self.log(f"Bağlantı hatası: {e}")
        finally:
            dinleyici.cancel()
            self.s.kayit.baglanti_guncelle(self.bid, bitis=simdi(), toplam_byte=self.toplam)
            self.log(f"Bağlantı kapandı ({self.toplam} byte alındı)")
            self.writer.close()


class UdpAlici(asyncio.DatagramProtocol):
    def __init__(self, kayit):
        self.kayit = kayit

    def datagram_received(self, data, addr):
        bid = self.kayit.baglanti_ac(addr[0], addr[1], "udp")
        m = IMEI_RE.search(data)
        self.kayit.baglanti_guncelle(
            bid, bitis=simdi(), ilk_veri_hex=data.hex(), toplam_byte=len(data),
            **({"imei": m.group(1).decode()} if m else {}),
        )
        self.kayit.log(f"[udp {addr[0]}:{addr[1]}] << {len(data)} byte hex={data.hex()} metin={gorunur(data)!r}")


class Sunucu:
    def __init__(self, args):
        self.args = args
        self.kayit = Kayit(args.db, args.log_klasoru)

    async def baglanti(self, reader, writer):
        await Oturum(self, reader, writer).calis()

    async def baslat(self):
        srv = await asyncio.start_server(self.baglanti, self.args.host, self.args.port)
        adresler = ", ".join(str(s.getsockname()) for s in srv.sockets)
        self.kayit.log(f"TCP dinleniyor: {adresler}  (oku={'açık' if self.args.oku else 'kapalı'})")
        if self.args.udp:
            loop = asyncio.get_running_loop()
            await loop.create_datagram_endpoint(
                lambda: UdpAlici(self.kayit), local_addr=(self.args.host, self.args.port)
            )
            self.kayit.log(f"UDP dinleniyor: {self.args.host}:{self.args.port}")
        return srv


def rapor(db_yolu: str):
    db = sqlite3.connect(db_yolu)
    print("Son bağlantılar:")
    for r in db.execute(
        "SELECT baslangic, bitis, ip, protokol, imei, toplam_byte FROM baglantilar ORDER BY id DESC LIMIT 20"
    ):
        print("  ", *r)
    print("\nSon okumalar:")
    for oid, zaman, imei, kimlik, bcc_ok in db.execute(
        "SELECT id, zaman, imei, sayac_kimlik, bcc_dogru FROM okumalar ORDER BY id DESC LIMIT 20"
    ):
        endeks = db.execute(
            "SELECT deger, birim FROM degerler WHERE okuma_id=? AND (obis='1.8.0' OR obis LIKE '%:1.8.0%')",
            (oid,),
        ).fetchone()
        print(f"   #{oid} {zaman} imei={imei} sayaç={kimlik} bcc={'ok' if bcc_ok else 'HATA'} "
              f"1.8.0={endeks[0] + ' ' + endeks[1] if endeks else '-'}")


def arguman_ayristir(argv=None):
    ap = argparse.ArgumentParser(description="OSOS merkez sunucusu")
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=80)
    ap.add_argument("--udp", action="store_true", help="Aynı portta UDP de dinle")
    ap.add_argument("--oku", action="store_true", help="Bağlanan modem üzerinden sayacı oku")
    ap.add_argument("--adres", default="", help="Sayaç adresi (boş = hattaki tek sayaç)")
    ap.add_argument("--bekle", type=float, default=5, help="Okumadan önce modemin susmasını bekle (sn)")
    ap.add_argument("--kimlik-sure", type=float, default=30, help="Sayaç kimliği bekleme (sn)")
    ap.add_argument("--veri-sure", type=float, default=180, help="Veri bloğu bekleme (sn)")
    ap.add_argument("--periyot", type=float, default=0, help="Bağlantı açık kaldıkça kaç dakikada bir okunsun")
    ap.add_argument("--hiz-degistir", action="store_true", help="Sayacın önerdiği hıza geç (genelde kapalı kalmalı)")
    ap.add_argument("--parity-ekle", action="store_true",
                    help="Modem 8N1 ise 7E1 parity bitini yazılımdan ekle")
    ap.add_argument("--db", default="osos.db")
    ap.add_argument("--log-klasoru", default="logs")
    ap.add_argument("--rapor", action="store_true", help="Veritabanındaki son kayıtları göster ve çık")
    return ap.parse_args(argv)


async def ana(args):
    srv = await Sunucu(args).baslat()
    async with srv:
        await srv.serve_forever()


def main():
    args = arguman_ayristir()
    if args.rapor:
        rapor(args.db)
        return
    try:
        asyncio.run(ana(args))
    except PermissionError:
        sys.exit(f"{args.port} portunu açma izni yok. Linux'ta sudo ile ya da --port 8080 ile dene.")
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
