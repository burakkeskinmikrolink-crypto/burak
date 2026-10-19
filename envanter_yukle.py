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
    python envanter_yukle.py meterStatusList_20.10.2026.xls   # Sayaç Durum Kontrol -> Excel

Dosyanın modem mi sayaç listesi mi olduğu başlıklardan anlaşılır.
Aynı dosyayı tekrar yüklemek kayıtları günceller, çoğaltmaz.
"""

import argparse
import csv
import io
import sys
from html.parser import HTMLParser

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

DURUM_BASLIK = {
    "MODEM SERI NO": "imei",
    "SAYAC SERI NO": "seri_no",
    "SAYAC ADI": "ad",
    "BOLGE": "bolge",
    "SUBE KODU": "sube_kodu",
    "SAYAC DURUMU": "eski_durum",
    "SON OKUMA TARIHI": "eski_son_okuma",
    "WORKGROUPNAME": "calisma_grubu",
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


class _HtmlTablo(HTMLParser):
    """EnerClever'ın .xls dışa aktarımı aslında bir HTML tablosu."""

    def __init__(self):
        super().__init__()
        self.satirlar, self._satir, self._hucre = [], None, None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._satir = []
        elif tag in ("td", "th"):
            self._hucre = ""

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._hucre is not None and self._satir is not None:
            self._satir.append(self._hucre.strip())
            self._hucre = None
        elif tag == "tr" and self._satir is not None:
            self.satirlar.append(self._satir)
            self._satir = None

    def handle_data(self, data):
        if self._hucre is not None:
            self._hucre += data


def satirlar(metin: str):
    if "<table" in metin[:2000].lower():
        p = _HtmlTablo()
        p.feed(metin)
        tablo = p.satirlar
    else:
        ilk = metin.splitlines()[0] if metin.strip() else ""
        ayirici = max(("\t", ";", ","), key=ilk.count)
        tablo = csv.reader(io.StringIO(metin), delimiter=ayirici)
    basliklar = None
    for satir in tablo:
        if not any(h.strip() for h in satir):
            continue
        if basliklar is None:
            basliklar = [sade(h) for h in satir]
            continue
        # EnerClever sayıları Excel için 'tırnak' içine alıyor
        yield dict(zip(basliklar, (h.strip().strip("'") for h in satir)))


def tur_bul(basliklar) -> str:
    b = set(basliklar)
    if "MODEM SERI NO" in b and "SAYAC SERI NO" in b:
        return "durum"
    if "MODEM" in b or "MODEM ADI" in b or "GSM NO" in b:
        return "modem"
    if "SAYAC" in b or "SAYAC ADI" in b:
        return "sayac"
    raise SystemExit(f"Başlıklardan liste türü anlaşılamadı: {sorted(b)}")


def _yaz(db, tablo, anahtar, alanlar):
    kolonlar = ", ".join(alanlar)
    yer = ", ".join("?" for _ in alanlar)
    guncelle = ", ".join(f"{c}=excluded.{c}" for c in alanlar if c != anahtar)
    db.execute(
        f"INSERT INTO {tablo} ({kolonlar}) VALUES ({yer}) "
        f"ON CONFLICT({anahtar}) DO {'UPDATE SET ' + guncelle if guncelle else 'NOTHING'}",
        tuple(alanlar.values()),
    )


def _secilen(kayit, esleme):
    alanlar = {}
    for baslik, deger in kayit.items():
        alan = esleme.get(baslik)
        if alan and deger and alan not in alanlar:
            alanlar[alan] = deger
    return alanlar


def yukle(db, metin: str):
    kayitlar = list(satirlar(metin))
    if not kayitlar:
        raise SystemExit("Dosyada kayıt bulunamadı.")
    tur = tur_bul(kayitlar[0].keys())

    sayi = atlanan = 0
    for k in kayitlar:
        if tur == "durum":
            # Sayaç Durum Kontrol listesi: modem + sayaç + eski sistemdeki durum
            s = _secilen(k, DURUM_BASLIK)
            imei, seri = s.pop("imei", ""), s.get("seri_no", "")
            if not seri:
                atlanan += 1
                continue
            s["saha"] = veritabani.saha_adi(s.get("ad", ""))
            if imei:
                s["modem_imei"] = imei
            _yaz(db, "sayaclar", "seri_no", s)
            if imei:
                # Modem adı yoksa sayaç adından türet; modem listesindeki ad varsa ona dokunma
                db.execute(
                    "INSERT INTO modemler (imei, ad, saha) VALUES (?, ?, ?) "
                    "ON CONFLICT(imei) DO UPDATE SET saha=excluded.saha",
                    (imei, "M-" + s["saha"] if s["saha"] else imei, s["saha"]),
                )
            sayi += 1
            continue

        esleme = MODEM_BASLIK if tur == "modem" else SAYAC_BASLIK
        anahtar = "imei" if tur == "modem" else "seri_no"
        alanlar = _secilen(k, esleme)
        if not alanlar.get(anahtar):
            atlanan += 1
            continue
        alanlar["saha"] = veritabani.saha_adi(alanlar.get("ad", ""))
        _yaz(db, "modemler" if tur == "modem" else "sayaclar", anahtar, alanlar)
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
        "SELECT COUNT(*) FROM modemler m WHERE EXISTS (SELECT 1 FROM sayaclar s "
        "WHERE s.modem_imei = m.imei OR (s.saha = m.saha AND m.saha != ''))"
    ).fetchone()[0]
    print(f"Toplam: {m} modem, {s} sayaç, {e} modemin sayacı eşleşti")


if __name__ == "__main__":
    sys.exit(main())
