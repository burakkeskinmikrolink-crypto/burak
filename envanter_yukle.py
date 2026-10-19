#!/usr/bin/env python3
"""EnerClever'dan kopyalanan modem / sayaç listesini veritabanına aktarır.

EnerClever'da:
  Modemler sayfası -> "Sayfada" kutusunu en büyük değere al -> tabloyu
  başlıklarıyla birlikte seçip kopyala -> Excel'e yapıştır -> CSV olarak kaydet
  (ya da doğrudan bir .txt dosyasına yapıştır; sekmeyle ayrılmış olur).

Kullanım:
    python envanter_yukle.py modemler.csv
    python envanter_yukle.py sayac_okumalari.csv
    python envanter_yukle.py sayaclar.csv --db osos.db

Dosyanın modem mi sayaç listesi mi olduğu başlıklardan anlaşılır.
Aynı dosyayı tekrar yüklemek kayıtları günceller, çoğaltmaz.
"""

import argparse
import csv
import io
import sys

from osos import veritabani

# Başlık -> alan eşlemesi (büyük harfe çevrilmiş, Türkçe karakterler sadeleştirilmiş)
MODEM_BASLIK = {
    "MUSTERI": "musteri",
    "MODEM": "ad",
    "MODEM ADI": "ad",
    "SERI NO": "imei",
    "SERI NUMARASI": "imei",
    "MODEM IMEI": "imei",
    "IMEI": "imei",
    "GSM NO": "gsm",
    "GSM": "gsm",
    "MSISDN": "gsm",
    "SIM KART SERI NO": "iccid",
    "ICCID": "iccid",
    "ACIKLAMA": "aciklama",
}
SAYAC_BASLIK = {
    "SAYAC": "ad",
    "SAYAC ADI": "ad",
    "SERI NO": "seri_no",
    "MARKA": "marka",
    "SAYAC MODELI": "model",
    "MODEL": "model",
    "ANA BOLGE": "bolge",
    "ALT BOLGE": "alt_bolge",
    "OKUMA ZAMANI": "eski_son_okuma",
    "SON OKUMA TARIHI": "eski_son_okuma",
}

_TR = str.maketrans("ÇĞİIÖŞÜçğıiöşü", "CGIIOSUCGIIOSU")


def sade(baslik: str) -> str:
    return " ".join(baslik.translate(_TR).upper().split())


def dosya_oku(yol: str) -> str:
    ham = open(yol, "rb").read()
    for kod in ("utf-8-sig", "cp1254"):
        try:
            return ham.decode(kod)
        except UnicodeDecodeError:
            continue
    return ham.decode("latin-1")


def satirlar(metin: str):
    ilk = metin.splitlines()[0] if metin.strip() else ""
    ayirici = max(("\t", ";", ","), key=ilk.count)
    okuyucu = csv.reader(io.StringIO(metin), delimiter=ayirici)
    basliklar = None
    for satir in okuyucu:
        if not any(h.strip() for h in satir):
            continue
        if basliklar is None:
            basliklar = [sade(h) for h in satir]
            continue
        yield dict(zip(basliklar, (h.strip() for h in satir)))


def tur_bul(basliklar) -> str:
    b = set(basliklar)
    if "MODEM" in b or "MODEM ADI" in b or "GSM NO" in b:
        return "modem"
    if "SAYAC" in b or "SAYAC ADI" in b:
        return "sayac"
    raise SystemExit(f"Başlıklardan liste türü anlaşılamadı: {sorted(b)}")


def yukle(db, metin: str):
    kayitlar = list(satirlar(metin))
    if not kayitlar:
        raise SystemExit("Dosyada kayıt bulunamadı.")
    tur = tur_bul(kayitlar[0].keys())
    esleme = MODEM_BASLIK if tur == "modem" else SAYAC_BASLIK
    anahtar = "imei" if tur == "modem" else "seri_no"
    tablo = "modemler" if tur == "modem" else "sayaclar"

    sayi = atlanan = 0
    for k in kayitlar:
        alanlar = {}
        for baslik, deger in k.items():
            alan = esleme.get(baslik)
            if alan and deger and alan not in alanlar:
                alanlar[alan] = deger
        if not alanlar.get(anahtar):
            atlanan += 1
            continue
        alanlar["saha"] = veritabani.saha_adi(alanlar.get("ad", ""))
        kolonlar = ", ".join(alanlar)
        yer = ", ".join("?" for _ in alanlar)
        guncelle = ", ".join(f"{c}=excluded.{c}" for c in alanlar if c != anahtar)
        db.execute(
            f"INSERT INTO {tablo} ({kolonlar}) VALUES ({yer}) "
            f"ON CONFLICT({anahtar}) DO UPDATE SET {guncelle}",
            tuple(alanlar.values()),
        )
        sayi += 1
    db.commit()
    return tur, sayi, atlanan


def main():
    ap = argparse.ArgumentParser(description="EnerClever listesini içeri aktar")
    ap.add_argument("dosyalar", nargs="+")
    ap.add_argument("--db", default="osos.db")
    args = ap.parse_args()
    db = veritabani.baglan(args.db)
    for yol in args.dosyalar:
        tur, sayi, atlanan = yukle(db, dosya_oku(yol))
        print(f"{yol}: {sayi} {tur} kaydı yüklendi" + (f", {atlanan} satır atlandı" if atlanan else ""))
    m = db.execute("SELECT COUNT(*) FROM modemler").fetchone()[0]
    s = db.execute("SELECT COUNT(*) FROM sayaclar").fetchone()[0]
    e = db.execute(
        "SELECT COUNT(*) FROM modemler m JOIN sayaclar s ON s.saha = m.saha"
    ).fetchone()[0]
    print(f"Toplam: {m} modem, {s} sayaç, {e} modem-sayaç eşleşmesi")


if __name__ == "__main__":
    sys.exit(main())
