"""Senaryo dosyasından YouTube'a yüklenecek düz transkript üretir.

YouTube Studio → Altyazılar → İngilizce → Ekle → "Dosya yükle" → "Zamanlama olmadan"
seçeneği bu metni videonun sesiyle otomatik eşler (auto-sync). Senaryo metni,
otomatik altyazıdan daha doğrudur: özel adlar, rakamlar ve kısaltmalar doğru yazılır.

Kullanım:
    python transkript.py ../../hidden_systems/04-v2.md            # ekrana yazar
    python transkript.py ../../hidden_systems/04-v2.md -o cikti/   # cikti/04-v2_transkript.txt
"""
import argparse
import os
import re

ETIKET = re.compile(r"<[^>]+>")          # SSML / ses işaretleri: <break time="600ms"/> vb.
KOSELI = re.compile(r"\[[^\]]*\]")       # [pause], [SAHNE ...] gibi yönerge notları
BOSLUK = re.compile(r"[ \t]{2,}")


def anlatim(md: str) -> list[str]:
    """'## Senaryo' ile sonraki '## ' başlığı arasındaki '> ' satırlarını paragraf listesi olarak döndürür."""
    m = re.search(r"^## Senaryo\s*$(.*?)(?=^## )", md, re.S | re.M)
    if not m:
        raise ValueError("'## Senaryo' bölümü bulunamadı")
    paragraflar, simdiki = [], []
    for satir in m.group(1).splitlines():
        if satir.startswith(">"):
            metin = satir[1:].strip()
            if metin:
                simdiki.append(metin)
            elif simdiki:
                paragraflar.append(" ".join(simdiki))
                simdiki = []
        elif simdiki:
            paragraflar.append(" ".join(simdiki))
            simdiki = []
    if simdiki:
        paragraflar.append(" ".join(simdiki))
    temiz = []
    for p in paragraflar:
        p = KOSELI.sub("", ETIKET.sub("", p))
        p = BOSLUK.sub(" ", p).strip()
        p = re.sub(r" +([.,;:!?])", r"\1", p)
        if p:
            temiz.append(p)
    return temiz


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("senaryo")
    ap.add_argument("-o", "--cikti", help="çıktı klasörü (yoksa ekrana yazar)")
    a = ap.parse_args()
    metin = "\n\n".join(anlatim(open(a.senaryo, encoding="utf-8").read())) + "\n"
    if a.cikti:
        os.makedirs(a.cikti, exist_ok=True)
        ad = os.path.splitext(os.path.basename(a.senaryo))[0] + "_transkript.txt"
        yol = os.path.join(a.cikti, ad)
        open(yol, "w", encoding="utf-8").write(metin)
        print(f"{yol} ({len(metin.split())} kelime)")
    else:
        print(metin, end="")


if __name__ == "__main__":
    main()
