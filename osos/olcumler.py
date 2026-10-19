"""Sayaçtan gelen OBIS değerlerini anlamlı gruplara ve alarmlara çevirir.

Sayaç ne gönderiyorsa saklanır; burada bilinen kodlar adlandırılır,
bilinmeyenler "Diğer" altında ham haliyle gösterilir. Hiçbir değer gizlenmez.
"""

from osos import iec62056 as iec

# (kod, ad) - gösterim sırası
GRUPLAR = [
    ("Tüketim (çekiş)", [
        ("1.8.0", "Toplam aktif"), ("1.8.1", "T1 gündüz"), ("1.8.2", "T2 puant"),
        ("1.8.3", "T3 gece"), ("1.8.4", "T4"),
    ]),
    ("Üretim (veriş)", [
        ("2.8.0", "Toplam aktif veriş"), ("2.8.1", "T1"), ("2.8.2", "T2"), ("2.8.3", "T3"),
    ]),
    ("Reaktif", [
        ("5.8.0", "Endüktif (Q1)"), ("6.8.0", "Kapasitif (Q2)"),
        ("7.8.0", "Endüktif (Q3)"), ("8.8.0", "Kapasitif (Q4)"),
        ("3.8.0", "Reaktif çekiş"), ("4.8.0", "Reaktif veriş"),
    ]),
    ("Talep", [
        ("1.6.0", "Maksimum talep"), ("1.6.1", "Maks. talep T1"),
        ("1.6.2", "Maks. talep T2"), ("1.6.3", "Maks. talep T3"),
        ("1.4.0", "Anlık demand"),
    ]),
    ("Anlık güç", [
        ("1.7.0", "Aktif güç (toplam)"), ("21.7.0", "Aktif güç L1"),
        ("41.7.0", "Aktif güç L2"), ("61.7.0", "Aktif güç L3"),
        ("3.7.0", "Reaktif güç"), ("13.7.0", "Güç faktörü (toplam)"),
        ("14.7.0", "Frekans"),
    ]),
    ("Olaylar", [
        ("C.7.0", "Enerji kesintisi sayısı"), ("C.7.1", "L1 kesinti sayısı"),
        ("C.7.2", "L2 kesinti sayısı"), ("C.7.3", "L3 kesinti sayısı"),
        ("C.2.0", "Programlama sayısı"), ("C.51.0", "Kapak açılma sayısı"),
        ("F.F", "Hata kodu"), ("F.F.0", "Hata kodu"),
    ]),
    ("Sayaç", [
        ("0.0.0", "Seri no"), ("C.1.0", "Seri no"), ("96.1.0", "Seri no"),
        ("0.2.0", "Yazılım sürümü"), ("0.9.1", "Saat"), ("0.9.2", "Tarih"),
        ("96.6.1", "Pil durumu"),
    ]),
]

# Faz tablosu: (ölçü, L1, L2, L3)
FAZLAR = [
    ("Gerilim", "32.7.0", "52.7.0", "72.7.0"),
    ("Akım", "31.7.0", "51.7.0", "71.7.0"),
    ("Güç faktörü", "33.7.0", "53.7.0", "73.7.0"),
    ("Aktif güç", "21.7.0", "41.7.0", "61.7.0"),
]

GERILIM_YOK = 50.0      # bunun altı: faz yok
GERILIM_ALT = 207.0     # 230 V -%10
GERILIM_UST = 253.0     # 230 V +%10


def sayi(deger):
    try:
        return float(str(deger).replace(",", "."))
    except (TypeError, ValueError):
        return None


def degerleri_topla(satirlar):
    """[(obis, deger, birim), ...] -> {kisa_kod: [(deger, birim), ...]}"""
    sonuc = {}
    for obis, deger, birim in satirlar:
        sonuc.setdefault(iec.obis_kisa(obis), []).append((deger, birim or ""))
    return sonuc


def gruplu(degerler):
    """Panel için [(grup, [(ad, kod, deger, birim, ek), ...]), ...] ve kalanlar."""
    kullanilan = set()
    cikti = []
    faz_kodlari = {k for _, *ks in FAZLAR for k in ks}
    for grup, kodlar in GRUPLAR:
        satirlar = []
        for kod, ad in kodlar:
            if kod in degerler and kod not in kullanilan and kod not in faz_kodlari:
                ilk, *ekler = degerler[kod]
                ek = " ".join(d for d, _ in ekler)  # ör. maksimum talep zamanı
                satirlar.append((ad, kod, ilk[0], ilk[1], ek))
                kullanilan.add(kod)
        if satirlar:
            cikti.append((grup, satirlar))
    diger = [(kod, d, b) for kod, liste in degerler.items()
             if kod not in kullanilan and kod not in faz_kodlari for d, b in liste]
    return cikti, diger


def faz_tablosu(degerler):
    """[(ölçü, [(deger, birim) | None] * 3), ...] - sadece sayacın gönderdiği satırlar."""
    tablo = []
    for olcu, *kodlar in FAZLAR:
        hucreler = [degerler[k][0] if k in degerler else None for k in kodlar]
        if any(hucreler):
            tablo.append((olcu, hucreler))
    return tablo


def faz_durumu(degerler):
    """Her faz için 'ok' / 'yok' / 'dusuk' / 'yuksek' / None (bilgi yok)."""
    durum = []
    for kod in ("32.7.0", "52.7.0", "72.7.0"):
        v = sayi(degerler[kod][0][0]) if kod in degerler else None
        if v is None:
            durum.append(None)
        elif v < GERILIM_YOK:
            durum.append("yok")
        elif v < GERILIM_ALT:
            durum.append("dusuk")
        elif v > GERILIM_UST:
            durum.append("yuksek")
        else:
            durum.append("ok")
    return durum


def alarmlar(degerler):
    """Son okumadan çıkan sorunlar: [(seviye, mesaj), ...]  seviye: 'kritik' / 'uyari'"""
    sonuc = []
    fazlar = faz_durumu(degerler)
    for i, d in enumerate(fazlar, 1):
        kod = ("32.7.0", "52.7.0", "72.7.0")[i - 1]
        v = degerler.get(kod, [("", "")])[0][0]
        if d == "yok":
            sonuc.append(("kritik", f"L{i} fazı yok ({v} V)"))
        elif d == "dusuk":
            sonuc.append(("uyari", f"L{i} gerilimi düşük ({v} V)"))
        elif d == "yuksek":
            sonuc.append(("uyari", f"L{i} gerilimi yüksek ({v} V)"))
    for kod in ("F.F", "F.F.0"):
        if kod in degerler:
            v = degerler[kod][0][0].strip()
            if v and v.strip("0") != "":
                sonuc.append(("uyari", f"Sayaç hata kodu: {v}"))
            break
    pf = sayi(degerler["13.7.0"][0][0]) if "13.7.0" in degerler else None
    if pf is not None and 0 < abs(pf) < 0.85:
        sonuc.append(("uyari", f"Düşük güç faktörü ({pf})"))
    akimlar = [sayi(degerler[k][0][0]) for k in ("31.7.0", "51.7.0", "71.7.0") if k in degerler]
    akimlar = [a for a in akimlar if a is not None]
    if len(akimlar) == 3 and max(akimlar) > 5 and min(akimlar) < 0.2 * max(akimlar):
        sonuc.append(("uyari", "Fazlar arası akım dengesiz"))
    return sonuc
