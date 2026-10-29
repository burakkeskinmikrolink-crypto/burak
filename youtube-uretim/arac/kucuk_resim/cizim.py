"""Ana nesne çizimleri (tek nesne kuralı): basit, kalın, telefonda tanınır ikonlar.

Her fonksiyon: f(d, cx, cy, s, t, **ayar)
    d  : ImageDraw (RGBA)
    cx, cy : nesnenin merkezi (px)
    s  : nesnenin sığacağı kare kutunun kenarı (px)
    t  : Tema
Fotoğraf yerine vektör tarzı çizim kullanılır: telif riski yok, küçük boyutta net.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Callable, Dict

from PIL import ImageDraw, ImageFont

FONT_DIR = Path(__file__).resolve().parent / "fonts"
_cache: Dict[tuple, ImageFont.FreeTypeFont] = {}


def font(size: int, black: bool = True) -> ImageFont.FreeTypeFont:
    key = (int(size), black)
    if key not in _cache:
        name = "InterDisplay-Black.otf" if black else "Inter-Bold.otf"
        _cache[key] = ImageFont.truetype(str(FONT_DIR / name), int(size))
    return _cache[key]


def _text_c(d: ImageDraw.ImageDraw, cx, cy, text, size, fill, black=True, stroke=0, stroke_fill=None):
    f = font(size, black)
    d.text((cx, cy), text, font=f, fill=fill, anchor="mm", stroke_width=stroke, stroke_fill=stroke_fill)


def _rr(d, box, r, fill, outline=None, width=0):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


WHITE, BLACK, DARK = (255, 255, 255), (0, 0, 0), (20, 24, 32)
PAPER = (250, 250, 245)


# --- Hidden Systems ---------------------------------------------------------

def jenerator(d, cx, cy, s, t, etiket="OFF"):
    w, h = s * 0.9, s * 0.55
    x0, y0 = cx - w / 2, cy - h / 2
    _rr(d, (x0, y0 + h - s * 0.06, x0 + w, y0 + h + s * 0.04), s * 0.02, (40, 40, 44))            # kızak
    _rr(d, (x0, y0, x0 + w, y0 + h), s * 0.04, (242, 194, 48), outline=BLACK, width=int(s * 0.012))  # gövde
    for i in range(7):                                                                              # ızgara
        gx = x0 + w * 0.08 + i * w * 0.06
        d.rectangle((gx, y0 + h * 0.2, gx + w * 0.025, y0 + h * 0.8), fill=(60, 50, 20))
    _rr(d, (x0 + w * 0.55, y0 + h * 0.18, x0 + w * 0.92, y0 + h * 0.62), s * 0.02, (30, 30, 34))  # panel
    d.ellipse((x0 + w * 0.6, y0 + h * 0.3, x0 + w * 0.68, y0 + h * 0.42), fill=(90, 90, 90))       # sönük lamba
    d.rectangle((x0 + w * 0.12, y0 - s * 0.16, x0 + w * 0.19, y0), fill=(50, 50, 54))              # egzoz
    tw, th = s * 0.42, s * 0.16                                                                     # OFF etiketi
    tx, ty = cx + s * 0.08, y0 - s * 0.2
    _rr(d, (tx, ty, tx + tw, ty + th), s * 0.03, t.vurgu, outline=WHITE, width=int(s * 0.01))
    _text_c(d, tx + tw / 2, ty + th / 2, etiket, s * 0.11, WHITE)


def terminal(d, cx, cy, s, t, ekran="DECLINED"):
    w, h = s * 0.55, s * 0.85
    x0, y0 = cx - w / 2, cy - h / 2
    _rr(d, (x0, y0, x0 + w, y0 + h), s * 0.06, (34, 38, 46), outline=(90, 96, 110), width=int(s * 0.012))
    _rr(d, (x0 + w * 0.1, y0 + h * 0.08, x0 + w * 0.9, y0 + h * 0.4), s * 0.02, (12, 14, 18))
    _text_c(d, cx, y0 + h * 0.24, ekran, s * 0.075, t.vurgu)
    for r in range(4):
        for c in range(3):
            bx = x0 + w * (0.14 + c * 0.26)
            by = y0 + h * (0.48 + r * 0.12)
            _rr(d, (bx, by, bx + w * 0.2, by + h * 0.08), s * 0.015, (70, 76, 90))


def fatura_kopya(d, cx, cy, s, t, adet=3):
    w, h = s * 0.48, s * 0.66
    for i in range(adet - 1, -1, -1):
        ox, oy = (i - 1) * s * 0.16, (i - 1) * s * 0.06
        x0, y0 = cx - w / 2 + ox, cy - h / 2 + oy
        shade = 255 - i * 22
        _rr(d, (x0, y0, x0 + w, y0 + h), s * 0.015, (shade, shade, shade - 5), outline=BLACK, width=int(s * 0.008))
        _text_c(d, x0 + w / 2, y0 + h * 0.12, "INVOICE", s * 0.06, (30, 30, 30))
        for k in range(5):
            ly = y0 + h * (0.28 + k * 0.1)
            d.rectangle((x0 + w * 0.12, ly, x0 + w * (0.88 - (k % 2) * 0.25), ly + h * 0.025), fill=(150, 150, 150))
        _text_c(d, x0 + w / 2, y0 + h * 0.86, "$100,000", s * 0.055, (30, 30, 30))
    _text_c(d, cx + s * 0.34, cy - s * 0.36, "×3", s * 0.16, t.vurgu, stroke=int(s * 0.012), stroke_fill=BLACK)


def iki_cubuk(d, cx, cy, s, t, sol="$9B", sag="$12M"):
    base = cy + s * 0.38
    bw = s * 0.3
    d.rectangle((cx - s * 0.38, cy - s * 0.42, cx - s * 0.38 + bw, base), fill=t.vurgu)
    d.rectangle((cx + s * 0.08, base - s * 0.04, cx + s * 0.08 + bw, base), fill=(170, 176, 188))
    d.line((cx - s * 0.46, base, cx + s * 0.46, base), fill=WHITE, width=int(s * 0.012))
    _text_c(d, cx - s * 0.38 + bw / 2, cy - s * 0.2, sol, s * 0.13, WHITE, stroke=int(s * 0.008), stroke_fill=BLACK)
    _text_c(d, cx + s * 0.08 + bw / 2, base - s * 0.14, sag, s * 0.13, WHITE, stroke=int(s * 0.008), stroke_fill=BLACK)


def termometre(d, cx, cy, s, t):
    tw = s * 0.16
    x0, y0, y1 = cx - tw / 2, cy - s * 0.45, cy + s * 0.25
    _rr(d, (x0, y0, x0 + tw, y1), tw / 2, (235, 238, 245), outline=BLACK, width=int(s * 0.01))
    d.ellipse((cx - s * 0.15, cy + s * 0.15, cx + s * 0.15, cy + s * 0.45), fill=t.vurgu, outline=BLACK,
              width=int(s * 0.01))
    _rr(d, (cx - tw * 0.25, y0 + s * 0.06, cx + tw * 0.25, y1 + s * 0.05), tw * 0.25, t.vurgu)
    for i in range(6):
        ty = y0 + s * 0.08 + i * s * 0.1
        d.line((x0 + tw, ty, x0 + tw + s * 0.06, ty), fill=WHITE, width=int(s * 0.01))
    for i in range(3):  # ısı dalgaları
        wx = cx + s * 0.22 + i * s * 0.08
        pts = [(wx + math.sin(k / 3) * s * 0.025, cy - s * 0.3 + k * s * 0.03) for k in range(14)]
        d.line(pts, fill=t.vurgu2, width=int(s * 0.015))


def zonlar(d, cx, cy, s, t, kapali=(0,)):
    bw = s * 0.27
    for i in range(3):
        x0 = cx - s * 0.45 + i * s * 0.32
        y0 = cy - bw / 2
        dead = i in kapali
        _rr(d, (x0, y0, x0 + bw, y0 + bw), s * 0.03, (40, 40, 46) if dead else (60, 200, 120),
            outline=t.vurgu if dead else WHITE, width=int(s * 0.012))
        if dead:  # çizilmiş X (font glifine güvenme)
            m, lw = bw * 0.28, int(s * 0.025)
            d.line((x0 + m, y0 + m, x0 + bw - m, y0 + bw - m), fill=t.vurgu, width=lw)
            d.line((x0 + bw - m, y0 + m, x0 + m, y0 + bw - m), fill=t.vurgu, width=lw)
        else:
            _text_c(d, x0 + bw / 2, y0 + bw / 2, "✓", s * 0.14, WHITE)
        _text_c(d, x0 + bw / 2, y0 + bw + s * 0.07, f"ZONE {chr(65 + i)}", s * 0.055, WHITE, black=False)


def ev_telefonu(d, cx, cy, s, t):
    bw, bh = s * 0.7, s * 0.34
    x0, y0 = cx - bw / 2, cy - s * 0.02
    d.polygon([(x0 + bw * 0.1, y0), (x0 + bw * 0.9, y0), (x0 + bw, y0 + bh), (x0, y0 + bh)],
              fill=(150, 30, 30), outline=BLACK, width=int(s * 0.012))
    d.ellipse((cx - s * 0.12, y0 + bh * 0.15, cx + s * 0.12, y0 + bh * 0.15 + s * 0.24), fill=(235, 235, 230),
              outline=BLACK, width=int(s * 0.008))
    for k in range(10):  # kadran delikleri
        a = math.radians(-60 + k * 30)
        px, py = cx + math.cos(a) * s * 0.085, y0 + bh * 0.15 + s * 0.12 + math.sin(a) * s * 0.085
        d.ellipse((px - s * 0.014, py - s * 0.014, px + s * 0.014, py + s * 0.014), fill=(60, 60, 60))
    hy = y0 - s * 0.16  # ahize
    _rr(d, (x0 + bw * 0.05, hy, x0 + bw * 0.95, hy + s * 0.11), s * 0.05, (150, 30, 30), outline=BLACK,
        width=int(s * 0.012))
    pts = [(x0 + bw, y0 + bh * 0.6)]  # kopuk kablo
    for k in range(1, 7):
        pts.append((x0 + bw + k * s * 0.035, y0 + bh * 0.6 + (s * 0.03 if k % 2 else -s * 0.03)))
    d.line(pts, fill=(30, 30, 30), width=int(s * 0.014))
    ex = pts[-1][0] + s * 0.06
    d.line([(ex, y0 + bh * 0.6), (ex + s * 0.1, y0 + bh * 0.62)], fill=(30, 30, 30), width=int(s * 0.014))
    sx, sy = ex - s * 0.02, y0 + bh * 0.28  # kıvılcım (kopukluk)
    d.polygon([(sx, sy - s * 0.09), (sx - s * 0.04, sy + s * 0.01), (sx, sy + s * 0.01),
               (sx - s * 0.02, sy + s * 0.09), (sx + s * 0.05, sy - s * 0.02), (sx + s * 0.01, sy - s * 0.02)],
              fill=t.vurgu2)


# --- Centworks --------------------------------------------------------------

def fis(d, cx, cy, s, t, eski="$4.93", yeni="$4.95"):
    w, h = s * 0.55, s * 0.9
    x0, y0 = cx - w / 2, cy - h / 2
    zig = [(x0, y0 + h)]
    for k in range(12):
        zig.append((x0 + (k + 0.5) * w / 12, y0 + h - s * 0.03))
        zig.append((x0 + (k + 1) * w / 12, y0 + h))
    d.polygon([(x0, y0), (x0 + w, y0)] + list(reversed(zig)), fill=PAPER)
    _text_c(d, cx, y0 + h * 0.08, "RECEIPT", s * 0.05, (40, 40, 40))
    for k in range(5):
        ly = y0 + h * (0.18 + k * 0.08)
        d.rectangle((x0 + w * 0.1, ly, x0 + w * 0.6, ly + h * 0.02), fill=(170, 170, 170))
        d.rectangle((x0 + w * 0.72, ly, x0 + w * 0.9, ly + h * 0.02), fill=(170, 170, 170))
    _text_c(d, x0 + w * 0.28, y0 + h * 0.66, "TOTAL", s * 0.055, (30, 30, 30))
    _text_c(d, x0 + w * 0.7, y0 + h * 0.66, eski, s * 0.07, (30, 30, 30))
    d.line((x0 + w * 0.5, y0 + h * 0.67, x0 + w * 0.92, y0 + h * 0.65), fill=(220, 40, 40), width=int(s * 0.018))
    _text_c(d, x0 + w * 0.62, y0 + h * 0.82, yeni, s * 0.13, t.vurgu2, stroke=int(s * 0.008), stroke_fill=BLACK)


def madeni_para(d, cx, cy, s, t, yazi="1¢", alt="3.69¢"):
    r = s * 0.36
    d.ellipse((cx - r, cy - r - s * 0.05, cx + r, cy + r - s * 0.05), fill=(184, 115, 51), outline=(110, 60, 20),
              width=int(s * 0.025))
    d.ellipse((cx - r * 0.82, cy - r * 0.82 - s * 0.05, cx + r * 0.82, cy + r * 0.82 - s * 0.05),
              outline=(150, 85, 35), width=int(s * 0.01))
    _text_c(d, cx, cy - s * 0.05, yazi, s * 0.26, (90, 45, 15))
    _rr(d, (cx - s * 0.3, cy + s * 0.34, cx + s * 0.3, cy + s * 0.48), s * 0.03, t.vurgu)
    _text_c(d, cx, cy + s * 0.41, f"COST: {alt}", s * 0.07, BLACK)


def kart_ucak(d, cx, cy, s, t):
    w, h = s * 0.7, s * 0.44
    x0, y0 = cx - w / 2 - s * 0.05, cy - h / 2 + s * 0.12
    _rr(d, (x0, y0, x0 + w, y0 + h), s * 0.04, t.vurgu, outline=(120, 90, 0), width=int(s * 0.01))
    _rr(d, (x0 + w * 0.1, y0 + h * 0.3, x0 + w * 0.28, y0 + h * 0.55), s * 0.015, (200, 170, 90))
    for k in range(4):
        d.rectangle((x0 + w * (0.1 + k * 0.2), y0 + h * 0.72, x0 + w * (0.25 + k * 0.2), y0 + h * 0.8),
                    fill=(120, 90, 0))
    px, py = cx + s * 0.25, cy - s * 0.3  # uçak
    plane = [(px - s * 0.18, py), (px + s * 0.2, py - s * 0.02), (px + s * 0.24, py), (px + s * 0.2, py + s * 0.02)]
    d.polygon(plane, fill=WHITE)
    d.polygon([(px, py), (px - s * 0.08, py - s * 0.14), (px - s * 0.03, py - s * 0.14), (px + s * 0.07, py)],
              fill=WHITE)
    d.polygon([(px, py), (px - s * 0.08, py + s * 0.14), (px - s * 0.03, py + s * 0.14), (px + s * 0.07, py)],
              fill=WHITE)
    for k in range(6):  # kesik çizgi karttan uçağa
        a = x0 + w * 0.9 + k * s * 0.03
        d.line((a, y0 - k * s * 0.035, a + s * 0.015, y0 - k * s * 0.035 - s * 0.017), fill=t.vurgu2,
               width=int(s * 0.012))


def nakit(d, cx, cy, s, t, etiket="$149", sonek="/YR"):
    for i in range(3):
        ox, oy = i * s * 0.05, -i * s * 0.05
        x0, y0 = cx - s * 0.4 + ox, cy - s * 0.18 + oy
        _rr(d, (x0, y0, x0 + s * 0.72, y0 + s * 0.36), s * 0.02, (60, 150, 80), outline=(20, 70, 30),
            width=int(s * 0.01))
        d.ellipse((x0 + s * 0.28, y0 + s * 0.08, x0 + s * 0.44, y0 + s * 0.28), outline=(20, 70, 30),
                  width=int(s * 0.01))
        _text_c(d, x0 + s * 0.36, y0 + s * 0.18, "$", s * 0.1, (20, 70, 30))
    yazi = f"{etiket}{sonek}"
    _rr(d, (cx - s * 0.2, cy + s * 0.25, cx + s * 0.3, cy + s * 0.42), s * 0.03, t.vurgu)
    _text_c(d, cx + s * 0.05, cy + s * 0.335, yazi, s * (0.08 if len(yazi) <= 9 else 0.06), BLACK)


def ev(d, cx, cy, s, t, etiket="+$284/MO"):
    w = s * 0.6
    x0, y0 = cx - w / 2, cy - s * 0.05
    d.polygon([(x0 - s * 0.05, y0), (cx, y0 - s * 0.3), (x0 + w + s * 0.05, y0)], fill=(200, 205, 215),
              outline=BLACK, width=int(s * 0.012))
    d.rectangle((x0, y0, x0 + w, y0 + s * 0.4), fill=(235, 238, 245), outline=BLACK, width=int(s * 0.012))
    d.rectangle((cx - s * 0.06, y0 + s * 0.2, cx + s * 0.06, y0 + s * 0.4), fill=(90, 60, 40))
    for wx in (x0 + w * 0.12, x0 + w * 0.68):
        d.rectangle((wx, y0 + s * 0.08, wx + w * 0.2, y0 + s * 0.2), fill=(120, 170, 220), outline=BLACK,
                    width=int(s * 0.008))
    tx, ty = cx - s * 0.05, y0 - s * 0.42
    _rr(d, (tx, ty, tx + s * 0.5, ty + s * 0.15), s * 0.03, t.vurgu, outline=BLACK, width=int(s * 0.008))
    _text_c(d, tx + s * 0.25, ty + s * 0.075, etiket, s * 0.075, BLACK)


def merdiven(d, cx, cy, s, t):
    step = s * 0.2
    for i in range(4):
        x0 = cx - s * 0.45 + i * step
        y0 = cy + s * 0.35 - (i + 1) * step * 0.8
        d.rectangle((x0, y0, x0 + step, cy + s * 0.35), fill=t.notr, outline=BLACK, width=int(s * 0.008))
        _text_c(d, x0 + step / 2, y0 + step * 0.35, "%", s * 0.08, t.vurgu)
    d.line((cx - s * 0.45, cy + s * 0.1, cx + s * 0.38, cy - s * 0.4), fill=t.vurgu2, width=int(s * 0.03))
    d.polygon([(cx + s * 0.42, cy - s * 0.45), (cx + s * 0.28, cy - s * 0.4), (cx + s * 0.38, cy - s * 0.3)],
              fill=t.vurgu2)


def iki_buton(d, cx, cy, s, t, sol="0%", sag="21%"):
    for i, (txt, col) in enumerate(((sol, t.vurgu2), (sag, t.vurgu))):
        x0 = cx - s * 0.45 + i * s * 0.48
        _rr(d, (x0, cy - s * 0.2, x0 + s * 0.42, cy + s * 0.2), s * 0.05, col, outline=WHITE, width=int(s * 0.012))
        _text_c(d, x0 + s * 0.21, cy, txt, s * 0.16, BLACK)
    _text_c(d, cx + s * 0.005, cy - s * 0.32, "VS", s * 0.1, WHITE)


def fiyat_etiketi(d, cx, cy, s, t, yazi="47%"):
    pts = [(cx - s * 0.4, cy - s * 0.2), (cx + s * 0.25, cy - s * 0.2), (cx + s * 0.45, cy),
           (cx + s * 0.25, cy + s * 0.2), (cx - s * 0.4, cy + s * 0.2)]
    d.polygon(pts, fill=t.vurgu, outline=BLACK, width=int(s * 0.012))
    d.ellipse((cx + s * 0.22, cy - s * 0.04, cx + s * 0.3, cy + s * 0.04), fill=(30, 30, 30))
    _text_c(d, cx - s * 0.08, cy, yazi, s * (0.17 if len(yazi) <= 4 else 0.105), BLACK)
    for k in range(4):  # dörde bölünmüş
        x = cx - s * 0.4 + k * s * 0.16
        d.line((x, cy + s * 0.25, x + s * 0.12, cy + s * 0.25), fill=WHITE, width=int(s * 0.02))


# --- Scam Engineer ----------------------------------------------------------

def _telefon_govde(d, cx, cy, s, t):
    w, h = s * 0.48, s * 0.92
    x0, y0 = cx - w / 2, cy - h / 2
    _rr(d, (x0, y0, x0 + w, y0 + h), s * 0.06, (25, 30, 40))
    _rr(d, (x0 + w * 0.06, y0 + h * 0.05, x0 + w * 0.94, y0 + h * 0.95), s * 0.045, (245, 248, 255))
    return x0, y0, w, h


def telefon_sms(d, cx, cy, s, t, satir1="Unpaid toll", satir2="$12.51", rozet="CARD"):
    x0, y0, w, h = _telefon_govde(d, cx, cy, s, t)
    bx0, by0 = x0 + w * 0.1, y0 + h * 0.25
    _rr(d, (bx0, by0, x0 + w * 0.9, by0 + h * 0.3), s * 0.03, (225, 228, 235))
    _text_c(d, cx, by0 + h * 0.08, satir1, s * 0.05, (30, 30, 30), black=False)
    _text_c(d, cx, by0 + h * 0.19, satir2, s * 0.1, t.vurgu2)
    _rr(d, (bx0, by0 + h * 0.36, x0 + w * 0.9, by0 + h * 0.44), s * 0.02, (200, 205, 215))
    _text_c(d, cx, by0 + h * 0.4, "tap link…", s * 0.04, (120, 120, 120), black=False)
    if rozet:  # köşe rozeti (boş verilirse çizilmez)
        _rr(d, (cx + s * 0.12, cy - s * 0.42, cx + s * 0.42, cy - s * 0.26), s * 0.04, t.vurgu)
        _text_c(d, cx + s * 0.27, cy - s * 0.34, rozet, s * 0.06, WHITE)


def telefon_arama(d, cx, cy, s, t, ad="MEDICARE"):
    x0, y0, w, h = _telefon_govde(d, cx, cy, s, t)
    _text_c(d, cx, y0 + h * 0.2, "incoming call", s * 0.04, (110, 110, 120), black=False)
    _text_c(d, cx, y0 + h * 0.3, ad, s * 0.07, (20, 30, 50))
    d.ellipse((cx - s * 0.09, y0 + h * 0.42, cx + s * 0.09, y0 + h * 0.42 + s * 0.18), fill=(200, 210, 225))
    for i, col in enumerate(((150, 160, 175), (60, 190, 110))):
        bx = x0 + w * (0.22 + i * 0.56)
        d.ellipse((bx - s * 0.06, y0 + h * 0.78, bx + s * 0.06, y0 + h * 0.78 + s * 0.12), fill=col)
    d.line((cx - s * 0.2, y0 + h * 0.26, cx + s * 0.2, y0 + h * 0.34), fill=(120, 120, 130), width=int(s * 0.012))


def laptop_uc_telefon(d, cx, cy, s, t):
    lw, lh = s * 0.7, s * 0.42
    x0, y0 = cx - lw / 2, cy - s * 0.42
    _rr(d, (x0, y0, x0 + lw, y0 + lh), s * 0.02, (30, 34, 44))
    d.rectangle((x0 + lw * 0.04, y0 + lh * 0.06, x0 + lw * 0.96, y0 + lh * 0.94), fill=(230, 236, 245))
    _rr(d, (x0 + lw * 0.18, y0 + lh * 0.2, x0 + lw * 0.82, y0 + lh * 0.8), s * 0.015, t.vurgu2,
        outline=(30, 30, 30), width=int(s * 0.006))
    _text_c(d, cx, y0 + lh * 0.5, "ALERT ⚠", s * 0.06, BLACK)
    d.polygon([(x0 - s * 0.04, y0 + lh), (x0 + lw + s * 0.04, y0 + lh), (x0 + lw + s * 0.08, y0 + lh + s * 0.04),
               (x0 - s * 0.08, y0 + lh + s * 0.04)], fill=(60, 66, 80))
    for i, lab in enumerate(("TECH", "BANK", "GOV")):
        px = cx - s * 0.32 + i * s * 0.32
        py = cy + s * 0.25
        _rr(d, (px - s * 0.08, py - s * 0.13, px + s * 0.08, py + s * 0.13), s * 0.02, (25, 30, 40))
        _rr(d, (px - s * 0.065, py - s * 0.11, px + s * 0.065, py + s * 0.11), s * 0.015, t.vurgu)
        _text_c(d, px, py, lab, s * 0.04, WHITE)


def asma_kilit(d, cx, cy, s, t, etiket="≠ SAFE"):
    bw, bh = s * 0.46, s * 0.4
    x0, y0 = cx - bw / 2, cy - s * 0.02
    d.arc((cx - bw * 0.36, y0 - bh * 0.75, cx + bw * 0.36, y0 + bh * 0.4), 180, 360, fill=(110, 120, 135),
          width=int(s * 0.06))
    _rr(d, (x0, y0, x0 + bw, y0 + bh), s * 0.05, (255, 196, 40), outline=(40, 40, 40), width=int(s * 0.012))
    d.ellipse((cx - s * 0.04, y0 + bh * 0.3, cx + s * 0.04, y0 + bh * 0.3 + s * 0.08), fill=(40, 40, 40))
    d.rectangle((cx - s * 0.015, y0 + bh * 0.45, cx + s * 0.015, y0 + bh * 0.75), fill=(40, 40, 40))
    _rr(d, (cx + s * 0.08, cy - s * 0.44, cx + s * 0.48, cy - s * 0.28), s * 0.04, t.vurgu, outline=WHITE,
        width=int(s * 0.01))
    _text_c(d, cx + s * 0.28, cy - s * 0.36, etiket, s * 0.075, WHITE)


def tarayici_magaza(d, cx, cy, s, t, etiket="11 DAYS OLD"):
    w, h = s * 0.9, s * 0.62
    x0, y0 = cx - w / 2, cy - h / 2
    _rr(d, (x0, y0, x0 + w, y0 + h), s * 0.03, WHITE, outline=(40, 50, 70), width=int(s * 0.01))
    d.rectangle((x0, y0, x0 + w, y0 + h * 0.14), fill=(225, 230, 240))
    _rr(d, (x0 + w * 0.06, y0 + h * 0.03, x0 + w * 0.94, y0 + h * 0.11), s * 0.02, WHITE)
    lx, ly = x0 + w * 0.11, y0 + h * 0.075  # küçük kilit simgesi
    d.rectangle((lx - s * 0.012, ly - s * 0.002, lx + s * 0.012, ly + s * 0.018), fill=(40, 40, 40))
    d.arc((lx - s * 0.009, ly - s * 0.016, lx + s * 0.009, ly + s * 0.004), 180, 360, fill=(40, 40, 40),
          width=max(1, int(s * 0.004)))
    _text_c(d, cx, y0 + h * 0.07, "deals-store.shop", s * 0.035, (80, 80, 80), black=False)
    _rr(d, (x0 + w * 0.08, y0 + h * 0.22, x0 + w * 0.48, y0 + h * 0.88), s * 0.02, (200, 220, 240))
    _text_c(d, x0 + w * 0.73, y0 + h * 0.35, "70% OFF", s * 0.07, t.vurgu2)
    for k in range(5):  # yıldızlar
        sx, sy, r = x0 + w * (0.61 + k * 0.06), y0 + h * 0.5, s * 0.018
        pts = [(sx + r * math.cos(math.radians(-90 + i * 36)) * (1 if i % 2 == 0 else 0.45),
                sy + r * math.sin(math.radians(-90 + i * 36)) * (1 if i % 2 == 0 else 0.45)) for i in range(10)]
        d.polygon(pts, fill=(240, 180, 0))
    _rr(d, (cx - s * 0.05, y0 + h * 0.86, cx + s * 0.47, y0 + h + s * 0.08), s * 0.03, t.vurgu, outline=WHITE,
        width=int(s * 0.01))
    _text_c(d, cx + s * 0.21, y0 + h * 0.98, etiket, s * 0.06, WHITE)


def kontrol_listesi(d, cx, cy, s, t, baslik="SSN", adim=4):
    """Pano üzerinde numaralı onay kutuları (ilk ikisi işaretli)."""
    w, h = s * 0.62, s * 0.86
    x0, y0 = cx - w / 2, cy - h / 2
    _rr(d, (x0, y0, x0 + w, y0 + h), s * 0.04, (120, 84, 50))                       # pano
    _rr(d, (x0 + w * 0.06, y0 + h * 0.06, x0 + w * 0.94, y0 + h * 0.96), s * 0.02, PAPER)
    _rr(d, (cx - w * 0.2, y0 - s * 0.03, cx + w * 0.2, y0 + h * 0.07), s * 0.02, (150, 155, 165))  # klips
    _rr(d, (x0 + w * 0.14, y0 + h * 0.12, x0 + w * 0.86, y0 + h * 0.24), s * 0.02, t.vurgu)
    _text_c(d, cx, y0 + h * 0.18, baslik, s * 0.07, WHITE)
    for i in range(adim):
        by = y0 + h * (0.32 + i * 0.16)
        bx = x0 + w * 0.16
        d.rectangle((bx, by, bx + s * 0.08, by + s * 0.08), outline=(40, 40, 40), width=int(s * 0.01))
        if i < 2:
            d.line((bx + s * 0.012, by + s * 0.04, bx + s * 0.035, by + s * 0.068, bx + s * 0.075, by + s * 0.01),
                   fill=(30, 160, 80), width=int(s * 0.018))
        _text_c(d, bx + s * 0.16, by + s * 0.04, str(i + 1), s * 0.06, (40, 40, 40))
        d.line((bx + s * 0.22, by + s * 0.04, x0 + w * 0.84, by + s * 0.04), fill=(170, 175, 185),
               width=int(s * 0.02))
    _rr(d, (cx + s * 0.1, cy - s * 0.47, cx + s * 0.46, cy - s * 0.32), s * 0.04, t.vurgu2, outline=WHITE,
        width=int(s * 0.01))
    _text_c(d, cx + s * 0.28, cy - s * 0.395, "FREE", s * 0.075, WHITE)


def odeme_yollari(d, cx, cy, s, t):
    """Beş ödeme yolu: kart (yeşil onay), banka, havale, hediye kartı, kripto (gri). Üstte saat."""
    etiketler = ("CARD", "BANK", "WIRE", "GIFT", "CRYPTO")
    for i, lab in enumerate(etiketler):
        col, row = i % 3, i // 3
        px = cx - s * 0.32 + col * s * 0.32 + (s * 0.16 if row else 0)
        py = cy - s * 0.02 + row * s * 0.3
        fill = (30, 160, 80) if i == 0 else ((60, 110, 200) if i in (1, 2) else (150, 155, 165))
        _rr(d, (px - s * 0.13, py - s * 0.11, px + s * 0.13, py + s * 0.11), s * 0.03, fill, outline=WHITE,
            width=int(s * 0.008))
        _text_c(d, px, py, lab, s * (0.055 if len(lab) <= 4 else 0.045), WHITE)
        if i == 0:
            d.ellipse((px + s * 0.07, py - s * 0.17, px + s * 0.17, py - s * 0.07), fill=WHITE)
            d.line((px + s * 0.09, py - s * 0.12, px + s * 0.11, py - s * 0.095, px + s * 0.15, py - s * 0.145),
                   fill=(30, 160, 80), width=int(s * 0.015))
    ox, oy, r = cx, cy - s * 0.36, s * 0.1                                             # saat
    d.ellipse((ox - r, oy - r, ox + r, oy + r), fill=WHITE, outline=(40, 40, 40), width=int(s * 0.012))
    d.line((ox, oy, ox, oy - r * 0.7), fill=(40, 40, 40), width=int(s * 0.012))
    d.line((ox, oy, ox + r * 0.55, oy), fill=t.vurgu2, width=int(s * 0.012))


NESNELER: Dict[str, Callable] = {
    "jenerator": jenerator, "terminal": terminal, "fatura_kopya": fatura_kopya, "iki_cubuk": iki_cubuk,
    "termometre": termometre, "zonlar": zonlar, "ev_telefonu": ev_telefonu,
    "fis": fis, "madeni_para": madeni_para, "kart_ucak": kart_ucak, "nakit": nakit, "ev": ev,
    "merdiven": merdiven, "iki_buton": iki_buton, "fiyat_etiketi": fiyat_etiketi,
    "telefon_sms": telefon_sms, "telefon_arama": telefon_arama, "laptop_uc_telefon": laptop_uc_telefon,
    "asma_kilit": asma_kilit, "tarayici_magaza": tarayici_magaza,
    "kontrol_listesi": kontrol_listesi, "odeme_yollari": odeme_yollari,
}
