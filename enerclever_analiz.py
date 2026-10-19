#!/usr/bin/env python3
"""EnerClever Sayaç Durum Kontrol listesinden mevcut durum raporu.

Önce listeyi içeri al, sonra raporu çıkar:
    python envanter_yukle.py meterStatusList_20.10.2026.xls
    python enerclever_analiz.py                       # özet ekrana
    python enerclever_analiz.py --csv sorunlu.csv     # sahaya gidilecek liste

Modem tipi IMEI'nin ilk 8 hanesinden (TAC) ayrılır. 35874105 = ECL-BGS5.
"""

import argparse
import collections
import csv
import datetime as dt

from osos import veritabani

MODEM_TIPLERI = {
    "35874105": "ECL-BGS5 (Cinterion BGS5)",
}
OK = "Veri Gönderiliyor"
DURDU = "Veri Gönderimi Durdu"
YOK = "Veri Gönderimi Yok"


def tarih(s):
    try:
        return dt.datetime.strptime(s, "%d.%m.%Y %H:%M:%S")
    except (TypeError, ValueError):
        return None


def sure_dilimi(t, simdi):
    if not t:
        return "hiç okunmamış"
    gun = (simdi - t).days
    if gun < 1:
        return "son 24 saat"
    if gun < 7:
        return "1-7 gün"
    if gun < 30:
        return "1-4 hafta"
    if gun < 180:
        return "1-6 ay"
    if gun < 365:
        return "6-12 ay"
    return "1 yıldan fazla"


def yuzde(a, b):
    return f"%{100 * a / b:.0f}" if b else "-"


def tablo(baslik, satirlar, kolonlar):
    print(f"\n{baslik}")
    genislik = [max(len(str(k)), *(len(str(s[i])) for s in satirlar)) for i, k in enumerate(kolonlar)]
    print("  " + "  ".join(str(k).ljust(g) for k, g in zip(kolonlar, genislik)))
    for s in satirlar:
        print("  " + "  ".join(str(v).ljust(g) for v, g in zip(s, genislik)))


def main():
    ap = argparse.ArgumentParser(description="EnerClever mevcut durum raporu")
    ap.add_argument("--db", default="osos.db")
    ap.add_argument("--csv", help="Okunmayan sahaları bu CSV dosyasına yaz")
    ap.add_argument("--tarih", help="Rapor tarihi (GG.AA.YYYY SS:DD:ss), varsayılan şimdi")
    args = ap.parse_args()

    db = veritabani.baglan(args.db)
    kayitlar = db.execute(
        "SELECT * FROM sayaclar WHERE eski_durum IS NOT NULL ORDER BY bolge, ad"
    ).fetchall()
    if not kayitlar:
        raise SystemExit("Veritabanında durum listesi yok. Önce envanter_yukle.py ile .xls dosyasını yükle.")
    simdi = tarih(args.tarih) if args.tarih else dt.datetime.now()
    n = len(kayitlar)
    durum = collections.Counter(r["eski_durum"] for r in kayitlar)

    print(f"EnerClever mevcut durum ({n} sayaç, {simdi:%d.%m.%Y %H:%M})")
    tablo("Genel durum", [(k, v, yuzde(v, n)) for k, v in durum.most_common()], ("Durum", "Sayaç", "Oran"))

    dilim = collections.Counter(
        sure_dilimi(tarih(r["eski_son_okuma"]), simdi) for r in kayitlar if r["eski_durum"] != OK
    )
    sira = ["1-7 gün", "1-4 hafta", "1-6 ay", "6-12 ay", "1 yıldan fazla", "hiç okunmamış", "son 24 saat"]
    tablo("Okunmayanlar: en son ne zaman okunmuş?",
          [(k, dilim[k]) for k in sira if dilim[k]], ("Süre", "Sayaç"))

    def grup(fn, baslik, kolon):
        g = collections.defaultdict(collections.Counter)
        for r in kayitlar:
            g[fn(r)][r["eski_durum"]] += 1
        satirlar = []
        for k, c in sorted(g.items(), key=lambda x: -sum(x[1].values())):
            t = sum(c.values())
            satirlar.append((k, t, c[OK], c[DURDU], c[YOK], yuzde(c[OK], t)))
        tablo(baslik, satirlar, (kolon, "Toplam", "Okunuyor", "Durdu", "Hiç gelmedi", "Başarı"))

    def modem_tipi(r):
        tac = (r["modem_imei"] or "")[:8]
        return MODEM_TIPLERI.get(tac, f"TAC {tac}" if tac.isdigit() else "diğer")

    grup(modem_tipi, "Modem tipine göre", "Modem tipi")
    grup(lambda r: r["bolge"] or "-", "Bölgeye göre", "Bölge")
    grup(lambda r: f"{len(r['seri_no'])} hane, {r['seri_no'][:2]}xxx", "Sayaç seri numarasına göre", "Seri no")
    grup(lambda r: r["calisma_grubu"] or "-", "Çalışma grubuna göre", "Grup")

    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(["Saha", "Şube kodu", "Bölge", "Durum", "Son okuma", "Süre",
                        "Modem IMEI", "Modem tipi", "Sayaç seri no"])
            for r in kayitlar:
                if r["eski_durum"] == OK:
                    continue
                w.writerow([r["ad"], r["sube_kodu"], r["bolge"], r["eski_durum"], r["eski_son_okuma"],
                            sure_dilimi(tarih(r["eski_son_okuma"]), simdi), r["modem_imei"],
                            modem_tipi(r), r["seri_no"]])
        print(f"\nOkunmayan {n - durum[OK]} saha {args.csv} dosyasına yazıldı.")


if __name__ == "__main__":
    main()
