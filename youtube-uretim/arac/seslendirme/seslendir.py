"""Senaryodan Kokoro TTS ile seslendirme (duraklama ve hız işaretleriyle).

Kokoro'nun resmi Python paketi SSML okumaz: <break>, <emphasis> gibi etiketler sesli okunur.
Bu yüzden senaryoda kendi basit işaretlerimizi kullanıyoruz ve duraklamaları
segmentlerin arasına sessizlik ekleyerek üretiyoruz.

İşaretler ("> " anlatım satırlarında):
    [pause]          700 ms ek sessizlik
    [pause 1200]     belirtilen ms kadar sessizlik
    [slow] ... [/slow]   bu kısım daha yavaş (varsayılan hız × 0.92)
Otomatik kurallar:
    soru işaretiyle biten cümleden sonra   +1000 ms
    paragraf sonu ("> " boş satır)         600 ms
    sahne sonu ("### [SAHNE" değişimi)     900 ms
Telaffuz: telaffuz.json içindeki "yazılış": "okunuş" çiftleri kelime sınırında değiştirilir.

Kullanım:
    python seslendir.py ../../hidden_systems/04-v2.md --plan          # sadece planı yazdır (Kokoro gerekmez)
    python seslendir.py ../../hidden_systems/04-v2.md -o cikti/hs04.wav --ses bm_george --dil b
    python seslendir.py ../../centworks/03-v2.md  -o cikti/cw03.wav --ses am_michael --dil a

Kurulum (Windows/Mac/Linux): pip install kokoro soundfile numpy
"""
from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass
from typing import List

ORNEK_HIZI = 24000          # Kokoro çıkışı 24 kHz
VARSAYILAN_PAUSE = 700
SORU_PAUSE = 1000
PARAGRAF_PAUSE = 600
SAHNE_PAUSE = 900
YAVAS_CARPAN = 0.92

PAUSE_RE = re.compile(r"\[pause(?:\s+(\d+))?\]")
SLOW_RE = re.compile(r"\[slow\](.*?)\[/slow\]", re.S)


@dataclass
class Segment:
    metin: str
    hiz: float = 1.0
    sonra_ms: int = 0


def senaryo_bloklari(md: str) -> List[List[str]]:
    """'## Senaryo' bölümündeki sahneleri, her biri paragraf listesi olacak şekilde döndürür."""
    m = re.search(r"^## Senaryo\s*$(.*?)(?=^## )", md, re.S | re.M)
    if not m:
        raise ValueError("'## Senaryo' bölümü bulunamadı")
    sahneler, paragraflar, simdiki = [], [], []
    for satir in m.group(1).splitlines():
        if satir.startswith("### "):
            if simdiki:
                paragraflar.append(" ".join(simdiki)); simdiki = []
            if paragraflar:
                sahneler.append(paragraflar); paragraflar = []
        elif satir.startswith(">"):
            t = satir[1:].strip()
            if t:
                simdiki.append(t)
            elif simdiki:
                paragraflar.append(" ".join(simdiki)); simdiki = []
        elif simdiki:
            paragraflar.append(" ".join(simdiki)); simdiki = []
    if simdiki:
        paragraflar.append(" ".join(simdiki))
    if paragraflar:
        sahneler.append(paragraflar)
    return sahneler


def telaffuz_uygula(metin: str, sozluk: dict) -> str:
    for yazilis, okunus in sorted(sozluk.items(), key=lambda kv: -len(kv[0])):
        metin = re.sub(r"(?<![\w-])" + re.escape(yazilis) + r"(?![\w-])", okunus, metin)
    return metin


def _cumlelere_bol(metin: str) -> List[str]:
    return [c.strip() for c in re.split(r"(?<=[.?!…])\s+", metin) if c.strip()]


def paragraf_segmentleri(paragraf: str, sozluk: dict) -> List[Segment]:
    """Bir paragrafı [slow] ve [pause] işaretlerine göre segmentlere böler."""
    parcalar, son = [], 0
    for m in SLOW_RE.finditer(paragraf):
        parcalar.append((paragraf[son:m.start()], 1.0))
        parcalar.append((m.group(1), YAVAS_CARPAN))
        son = m.end()
    parcalar.append((paragraf[son:], 1.0))

    segler: List[Segment] = []
    for metin, hiz in parcalar:
        konum = 0
        for m in PAUSE_RE.finditer(metin):
            onceki = metin[konum:m.start()]
            ms = int(m.group(1)) if m.group(1) else VARSAYILAN_PAUSE
            segler += _cumle_seg(onceki, hiz, sozluk)
            if segler:
                segler[-1].sonra_ms += ms
            konum = m.end()
        segler += _cumle_seg(metin[konum:], hiz, sozluk)
    return segler


def _cumle_seg(metin: str, hiz: float, sozluk: dict) -> List[Segment]:
    out = []
    for c in _cumlelere_bol(metin):
        c = telaffuz_uygula(c, sozluk)
        out.append(Segment(c, hiz, SORU_PAUSE if c.endswith("?") else 0))
    return out


def plan(md: str, sozluk: dict | None = None) -> List[Segment]:
    sozluk = sozluk or {}
    segler: List[Segment] = []
    for sahne in senaryo_bloklari(md):
        for i, p in enumerate(sahne):
            ps = paragraf_segmentleri(p, sozluk)
            if ps:
                ps[-1].sonra_ms = max(ps[-1].sonra_ms, PARAGRAF_PAUSE)
            segler += ps
        if segler:
            segler[-1].sonra_ms = max(segler[-1].sonra_ms, SAHNE_PAUSE)
    return segler


def seslendir(segler: List[Segment], cikti: str, ses: str, dil: str, hiz: float) -> float:
    import numpy as np          # noqa: WPS433 (yalnızca gerçek seslendirmede gerekir)
    import soundfile as sf
    from kokoro import KPipeline

    boru = KPipeline(lang_code=dil)
    parcalar = []
    for s in segler:
        for _, _, ses_dizisi in boru(s.metin, voice=ses, speed=hiz * s.hiz):
            parcalar.append(np.asarray(ses_dizisi, dtype="float32"))
        parcalar.append(np.zeros(int(ORNEK_HIZI * s.sonra_ms / 1000), dtype="float32"))
    tum = np.concatenate(parcalar) if parcalar else np.zeros(1, dtype="float32")
    os.makedirs(os.path.dirname(os.path.abspath(cikti)), exist_ok=True)
    sf.write(cikti, tum, ORNEK_HIZI)
    return len(tum) / ORNEK_HIZI


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("senaryo")
    ap.add_argument("-o", "--cikti", default="cikti/seslendirme.wav")
    ap.add_argument("--ses", default="bm_george", help="Kokoro sesi (ör. bm_george, am_michael)")
    ap.add_argument("--dil", default="b", help="a = Amerikan İngilizcesi, b = İngiliz İngilizcesi")
    ap.add_argument("--hiz", type=float, default=1.0)
    ap.add_argument("--telaffuz", default=os.path.join(os.path.dirname(__file__), "telaffuz.json"))
    ap.add_argument("--plan", action="store_true", help="sadece segment planını yazdır")
    a = ap.parse_args()
    sozluk = json.load(open(a.telaffuz, encoding="utf-8")) if os.path.exists(a.telaffuz) else {}
    segler = plan(open(a.senaryo, encoding="utf-8").read(), sozluk)
    if a.plan:
        toplam = 0
        for s in segler:
            print(f"[x{s.hiz:.2f}] {s.metin}  ⟶ +{s.sonra_ms} ms")
            toplam += s.sonra_ms
        print(f"\n{len(segler)} segment, eklenen sessizlik toplamı {toplam / 1000:.1f} sn")
        return
    sure = seslendir(segler, a.cikti, a.ses, a.dil, a.hiz)
    print(f"{a.cikti}: {sure / 60:.1f} dk")


if __name__ == "__main__":
    main()
