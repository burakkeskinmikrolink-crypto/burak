"""Küçük resim üreticisi (Pillow).

Kullanım:
    python uret.py                     # videolar.json içindeki tüm videolar, A ve B varyantları
    python uret.py --sadece HS-04      # tek video
    python uret.py --cikti baska_klasor

Çıktı:
    cikti/<ID>_<A|B>.png                     1280x720, A/B testine hazır
    cikti/onizleme/<ID>_AB_telefon.png       iki varyant yan yana, telefon akışı boyutunda
    cikti/onizleme/telefon_izgara.png        hepsi tek görselde, mobil ana sayfa boyutunda (360 px genişlik)
    cikti/onizleme/kucuk_izgara.png          hepsi tek görselde, "Sıradaki"/arama listesi boyutunda (168 px)

Kurallar (kodla zorlanır): en fazla 4 kelime, kalın büyük yazı (Inter Display Black, OFL),
tek ana nesne, yüksek kontrast (WCAG ≥ 4.5), yazı süre rozetinin (sağ alt) dışında.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from PIL import Image, ImageDraw, ImageFilter

from cizim import NESNELER, font
from temalar import TEMALAR, Tema, contrast

HERE = Path(__file__).resolve().parent
W, H = 1280, 720
SS = 2                      # süper örnekleme (kenar yumuşatma)
TEXT_BOX = (52, 70, 640, 650)  # x0, y0, x1, y1 (1x) — sol blok, süre rozetinden uzak
OBJ_CENTER, OBJ_SIZE = (985, 370), 540
MAX_WORDS = 4


class KuralHatasi(ValueError):
    pass


def kelimeler(yazi: str) -> List[str]:
    return [w for w in yazi.split() if w not in ("→", "-", "–", "—")]


def _gradyan(t: Tema, w: int, h: int) -> Image.Image:
    img = Image.new("RGB", (w, h), t.bg_ust)
    d = ImageDraw.Draw(img)
    for y in range(h):
        k = y / (h - 1)
        c = tuple(int(t.bg_ust[i] + (t.bg_alt[i] - t.bg_ust[i]) * k) for i in range(3))
        d.line((0, y, w, y), fill=c)
    return img


def arka_plan(t: Tema) -> Image.Image:
    w, h = W * SS, H * SS
    img = _gradyan(t, w, h).convert("RGBA")
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    cx, cy, r = OBJ_CENTER[0] * SS, OBJ_CENTER[1] * SS, int(OBJ_SIZE * 0.62 * SS)
    if t.koyu:
        g.ellipse((cx - r, cy - r, cx + r, cy + r), fill=t.vurgu + (70,))   # nesnenin arkasında vurgu ışığı
    else:
        g.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 150))
        g.ellipse((-200 * SS, 520 * SS, 260 * SS, 980 * SS), fill=t.vurgu2 + (60,))
        g.ellipse((560 * SS, -260 * SS, 900 * SS, 80 * SS), fill=t.vurgu + (45,))
    glow = glow.filter(ImageFilter.GaussianBlur(70 * SS))
    img = Image.alpha_composite(img, glow)
    if t.koyu:  # vinyet
        v = Image.new("L", (w, h), 0)
        ImageDraw.Draw(v).ellipse((-w * 0.15, -h * 0.3, w * 1.15, h * 1.3), fill=255)
        v = v.filter(ImageFilter.GaussianBlur(120 * SS))
        dark = Image.new("RGBA", (w, h), (0, 0, 0, 170))
        img = Image.composite(img, Image.alpha_composite(img, dark), v)
    return img


def _satirlara_bol(ws: Sequence[str]) -> List[List[List[str]]]:
    """Kelime listesinin 1–3 satıra tüm bölünüşleri."""
    n = len(ws)
    out = []
    for k in range(0, min(n - 1, 2) + 1):
        for cuts in itertools.combinations(range(1, n), k):
            parts, prev = [], 0
            for c in (*cuts, n):
                parts.append(list(ws[prev:c]))
                prev = c
            out.append(parts)
    return out


def yazi_yerlesimi(yazi: str) -> Tuple[List[List[str]], int]:
    """Kutuya sığan en büyük punto ve satır bölünüşünü bulur (1x px cinsinden punto)."""
    ws = yazi.upper().split()
    bw, bh = TEXT_BOX[2] - TEXT_BOX[0], TEXT_BOX[3] - TEXT_BOX[1]
    best = (None, 0)
    for lines in _satirlara_bol(ws):
        lo, hi = 40, 210
        while lo < hi:
            mid = (lo + hi + 1) // 2
            f = font(mid)
            widths = [f.getlength(" ".join(l)) for l in lines]
            height = len(lines) * mid * 1.02
            if max(widths) <= bw and height <= bh:
                lo = mid
            else:
                hi = mid - 1
        if lo > best[1]:
            best = (lines, lo)
    return best


def yazi_ciz(img: Image.Image, t: Tema, yazi: str, vurgu: Sequence[int]) -> int:
    lines, size = yazi_yerlesimi(yazi)
    f = font(size * SS)
    d = ImageDraw.Draw(img)
    line_h = size * 1.02 * SS
    total_h = line_h * len(lines)
    y = (TEXT_BOX[1] + TEXT_BOX[3]) / 2 * SS - total_h / 2
    stroke = max(4, int(size * 0.07)) * SS
    idx = 0
    for line in lines:
        x = TEXT_BOX[0] * SS
        for w_ in line:
            col = t.vurgu if idx in vurgu else t.yazi
            if t.koyu is False and idx in vurgu:
                col = t.vurgu
            # gölge
            d.text((x + 6 * SS, y + 8 * SS), w_, font=f, fill=(0, 0, 0, 110) if t.koyu else (10, 31, 68, 60))
            d.text((x, y), w_, font=f, fill=col, stroke_width=stroke, stroke_fill=t.kontur)
            x += f.getlength(w_ + " ")
            idx += 1
        y += line_h
    return size


def nesne_ciz(img: Image.Image, t: Tema, nesne: str, ayar: Dict) -> None:
    if nesne not in NESNELER:
        raise KuralHatasi(f"Bilinmeyen nesne: {nesne}")
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    NESNELER[nesne](ImageDraw.Draw(layer), OBJ_CENTER[0] * SS, OBJ_CENTER[1] * SS, OBJ_SIZE * SS, t, **ayar)
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    shadow.putalpha(layer.getchannel("A").point(lambda a: int(a * 0.55)))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14 * SS))
    img.alpha_composite(shadow, (10 * SS, 18 * SS))
    img.alpha_composite(layer)


def kurallari_kontrol(yazi: str, t: Tema) -> None:
    n = len(kelimeler(yazi))
    if n == 0 or n > MAX_WORDS:
        raise KuralHatasi(f"'{yazi}': {n} kelime (en fazla {MAX_WORDS})")
    worst = min(contrast(t.yazi, t.bg_ust), contrast(t.yazi, t.bg_alt))
    if worst < 4.5:
        raise KuralHatasi(f"Kontrast düşük ({worst:.1f} < 4.5)")


def kucuk_resim(video: Dict, varyant: str) -> Tuple[Image.Image, int]:
    t = TEMALAR[video["kanal"]]
    v = video["varyantlar"][varyant]
    kurallari_kontrol(v["yazi"], t)
    img = arka_plan(t)
    nesne_ciz(img, t, v["nesne"], v.get("ayar", {}))
    size = yazi_ciz(img, t, v["yazi"], v.get("vurgu", []))
    return img.convert("RGB").resize((W, H), Image.LANCZOS), size


# --- Önizleme --------------------------------------------------------------

YT_BG, YT_TXT, YT_SUB = (15, 15, 15), (241, 241, 241), (170, 170, 170)
KANAL_AD = {"hidden_systems": "Hidden Systems", "centworks": "Centworks", "scam_engineer": "Scam Engineer"}


def _sure_rozeti(d: ImageDraw.ImageDraw, x1: int, y1: int, scale: float, text: str = "8:00"):
    f = font(max(9, int(12 * scale)), black=False)
    tw = f.getlength(text)
    pad = 4 * scale
    d.rounded_rectangle((x1 - tw - 2 * pad - 4 * scale, y1 - 18 * scale - 4 * scale, x1 - 4 * scale, y1 - 4 * scale),
                        radius=3 * scale, fill=(0, 0, 0, 220))
    d.text((x1 - tw - pad - 4 * scale, y1 - 13 * scale - 4 * scale), text, font=f, fill=(255, 255, 255))


def _kisalt(f, text: str, maxw: int) -> List[str]:
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if f.getlength(trial) <= maxw:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
        if len(lines) == 2:
            break
    if len(lines) < 2 and cur:
        lines.append(cur)
    if len(lines) == 2 and " ".join(lines) != text:
        lines[1] = lines[1].rstrip(".,") + "…"
    return lines[:2]


def kart(thumb: Image.Image, baslik: str, kanal: str, genislik: int) -> Image.Image:
    """Mobil akıştaki bir video kartını taklit eder: küçük resim + süre rozeti + başlık + kanal satırı."""
    th = int(genislik * 9 / 16)
    scale = genislik / 360
    card = Image.new("RGB", (genislik, th + int(64 * scale)), YT_BG)
    card.paste(thumb.resize((genislik, th), Image.LANCZOS), (0, 0))
    d = ImageDraw.Draw(card, "RGBA")
    _sure_rozeti(d, genislik, th, scale)
    f = font(max(9, int(14 * scale)), black=False)
    y = th + 6 * scale
    for line in _kisalt(f, baslik, genislik - 8):
        d.text((4, y), line, font=f, fill=YT_TXT)
        y += 17 * scale
    d.text((4, y + 2 * scale), f"{KANAL_AD[kanal]} · 1.2K views · 2 days ago", font=font(max(8, int(11 * scale)),
           black=False), fill=YT_SUB)
    return card


def izgara(kartlar: List[Image.Image], sutun: int, bosluk: int, baslik: str) -> Image.Image:
    cw, ch = kartlar[0].size
    rows = (len(kartlar) + sutun - 1) // sutun
    top = 56
    img = Image.new("RGB", (sutun * cw + (sutun + 1) * bosluk, top + rows * ch + (rows + 1) * bosluk), YT_BG)
    d = ImageDraw.Draw(img)
    d.text((bosluk, 16), baslik, font=font(22, black=False), fill=YT_TXT)
    for i, k in enumerate(kartlar):
        r, c = divmod(i, sutun)
        img.paste(k, (bosluk + c * (cw + bosluk), top + bosluk + r * (ch + bosluk)))
    return img


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Küçük resim üreticisi")
    ap.add_argument("--videolar", default=str(HERE / "videolar.json"))
    ap.add_argument("--cikti", default=str(HERE / "cikti"))
    ap.add_argument("--sadece", help="Tek video ID (örn. HS-04)")
    args = ap.parse_args(argv)

    videos = json.loads(Path(args.videolar).read_text(encoding="utf-8"))
    if args.sadece:
        videos = [v for v in videos if v["id"] == args.sadece]
    out = Path(args.cikti)
    (out / "onizleme").mkdir(parents=True, exist_ok=True)

    phone_cards, small_cards = [], []
    for v in videos:
        pair = []
        for key in ("A", "B"):
            img, size = kucuk_resim(v, key)
            path = out / f"{v['id']}_{key}.png"
            img.save(path, optimize=True)
            print(f"[png] {path.name}  yazı: '{v['varyantlar'][key]['yazi']}'  punto: {size}")
            label = f"[{v['id']} {key}] {v['baslik']}"
            pc = kart(img, label, v["kanal"], 360)
            phone_cards.append(pc)
            small_cards.append(kart(img, f"{v['id']} {key}", v["kanal"], 168))
            pair.append(pc)
        izgara(pair, 2, 16, f"{v['id']}: A / B (telefon akışı, 360 px)").save(
            out / "onizleme" / f"{v['id']}_AB_telefon.png", optimize=True)

    izgara(phone_cards, 4, 20, "Telefon ana sayfa akışı (360 px genişlik) · tüm varyantlar").save(
        out / "onizleme" / "telefon_izgara.png", optimize=True)
    izgara(small_cards, 8, 14, "Sıradaki / arama listesi boyutu (168 px) · tüm varyantlar").save(
        out / "onizleme" / "kucuk_izgara.png", optimize=True)
    print(f"[önizleme] {out / 'onizleme'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
