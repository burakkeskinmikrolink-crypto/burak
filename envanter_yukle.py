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
    python envanter_yukle.py EnerjiRaporu_55.xls              # Enerji Raporu (aylık kWh, GSM no)

Dosyanın modem mi sayaç listesi mi olduğu başlıklardan anlaşılır.
Aynı dosyayı tekrar yüklemek kayıtları günceller, çoğaltmaz.
"""

import argparse
import csv
import io
import re
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

ENERJI_BASLIK = {
    "SAYAC NO": "seri_no",
    "SAYAC ADI": "ad",
    "MODEM NO": "imei",
    "MODEM": "modem_ad",
    "SIMKART GSM NO": "gsm",
    "ALT BOLGE": "alt_bolge",
    "SEHIR": "sehir",
    "SAHA ADI": "saha_adi",
    "SAHA ID": "sube_kodu",
    "KWH": "kwh",
}

BILINEN = {*MODEM_BASLIK, *SAYAC_BASLIK, *DURUM_BASLIK, *ENERJI_BASLIK}

_TR = str.maketrans("ÇĞİIÖŞÜçğıiöşü", "CGIIOSUCGIIOSU")


def sade(baslik: str) -> str:
    return " ".join(baslik.translate(_TR).upper().split())


def dosya_oku(yol: str) -> bytes:
    return open(yol, "rb").read()


def _coz(ham: bytes) -> str:
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


def _hucre_metni(v) -> str:
    if isinstance(v, float):
        return str(int(v)) if v.is_integer() else repr(v)
    return str(v)


def tablo_oku(kaynak):
    """Dosya içeriğini satır listesine çevirir (Excel .xls, HTML'li .xls, CSV/TXT)."""
    if isinstance(kaynak, bytes) and kaynak[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1":
        try:
            import xlrd
        except ImportError:
            raise SystemExit("Bu gerçek bir Excel dosyası. Okumak için:  pip install xlrd")
        sayfa = xlrd.open_workbook(file_contents=kaynak).sheet_by_index(0)
        return [[_hucre_metni(v) for v in sayfa.row_values(i)] for i in range(sayfa.nrows)]
    metin = kaynak if isinstance(kaynak, str) else _coz(kaynak)
    if "<table" in metin[:2000].lower():
        p = _HtmlTablo()
        p.feed(metin)
        return p.satirlar
    ornek = "\n".join(metin.splitlines()[:20])
    ayirici = max(("\t", ";", ","), key=ornek.count)
    return list(csv.reader(io.StringIO(metin), delimiter=ayirici))


def satirlar(tablo):
    """Başlık satırını bulur ve sonraki satırları sözlük olarak döner.

    Başlık, bilinen başlıklardan en az üçünü içeren ilk satırdır; EnerClever
    raporlarının üstündeki 'Yıl', 'Değer' gibi satırlar atlanır.
    """
    basliklar = None
    for satir in tablo:
        if not any(str(h).strip() for h in satir):
            continue
        if basliklar is None:
            aday = [sade(h) for h in satir]
            if sum(1 for h in aday if h in BILINEN) >= 3:
                basliklar = aday
            continue
        # EnerClever sayıları Excel için 'tırnak' içine alıyor
        yield dict(zip(basliklar, (str(h).strip().strip("'") for h in satir)))


def donem_bul(tablo):
    """Rapor üstündeki '2026/09' gibi dönemi 'YYYY-AA' olarak döner."""
    for satir in tablo[:15]:
        for h in satir:
            m = re.fullmatch(r"\s*(\d{4})[/.-](\d{1,2})\s*", str(h))
            if m:
                return f"{m.group(1)}-{int(m.group(2)):02d}"
    return None


def tur_bul(basliklar) -> str:
    b = set(basliklar)
    if "MODEM SERI NO" in b and "SAYAC SERI NO" in b:
        return "durum"
    if "SAYAC NO" in b and "KWH" in b:
        return "enerji"
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


def yukle(db, kaynak):
    tablo = tablo_oku(kaynak)
    kayitlar = list(satirlar(tablo))
    if not kayitlar:
        raise SystemExit("Dosyada kayıt bulunamadı.")
    tur = tur_bul(kayitlar[0].keys())
    donem = donem_bul(tablo) if tur == "enerji" else None
    if tur == "enerji" and not donem:
        raise SystemExit("Enerji raporunda dönem (ör. 2026/09) bulunamadı.")

    sayi = atlanan = 0
    for k in kayitlar:
        if tur == "enerji":
            # EnerClever Enerji Raporu: sayaç, modem, GSM, saha ve aylık kWh
            e = _secilen(k, ENERJI_BASLIK)
            seri = e.get("seri_no", "")
            if not seri:
                atlanan += 1
                continue
            saha = veritabani.saha_adi(e.get("ad", "")) or e.get("saha_adi", "").upper()
            sayac = {"seri_no": seri, "saha": saha}
            for alan in ("ad", "alt_bolge", "sehir", "sube_kodu"):
                if e.get(alan):
                    sayac[alan] = e[alan]
            if len(e.get("imei", "")) < 6:  # kaynakta "1" gibi hatalı modem numaraları var
                e.pop("imei", None)
            if e.get("imei"):
                sayac["modem_imei"] = e["imei"]
                modem = {"imei": e["imei"], "saha": saha}
                for alan, kolon in (("modem_ad", "ad"), ("gsm", "gsm")):
                    if e.get(alan):
                        modem[kolon] = e[alan]
                _yaz(db, "modemler", "imei", modem)
            _yaz(db, "sayaclar", "seri_no", sayac)
            try:
                kwh = float(e.get("kwh", "").replace(",", "."))
            except ValueError:
                kwh = None
            if kwh is not None:
                db.execute(
                    "INSERT INTO aylik_tuketim (seri_no, ay, kwh, kaynak) VALUES (?, ?, ?, 'enerclever') "
                    "ON CONFLICT(seri_no, ay, kaynak) DO UPDATE SET kwh=excluded.kwh",
                    (seri, donem, kwh),
                )
            sayi += 1
            continue
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
        if tur == "enerji":
            for ay, adet, top in db.execute(
                "SELECT ay, COUNT(*), SUM(kwh) FROM aylik_tuketim WHERE kaynak='enerclever' GROUP BY ay ORDER BY ay"
            ):
                print(f"   EnerClever tüketimi {ay}: {adet} sayaç, {top:,.0f} kWh")
    m = db.execute("SELECT COUNT(*) FROM modemler").fetchone()[0]
    s = db.execute("SELECT COUNT(*) FROM sayaclar").fetchone()[0]
    e = db.execute(
        "SELECT COUNT(*) FROM modemler m WHERE EXISTS (SELECT 1 FROM sayaclar s "
        "WHERE s.modem_imei = m.imei OR (s.saha = m.saha AND m.saha != ''))"
    ).fetchone()[0]
    print(f"Toplam: {m} modem, {s} sayaç, {e} modemin sayacı eşleşti")


if __name__ == "__main__":
    sys.exit(main())
