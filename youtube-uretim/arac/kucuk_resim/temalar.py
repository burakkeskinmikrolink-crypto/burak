"""Kanal temaları: renkler ve arka plan.

Kurallar (kanal kimliği):
    hidden_systems : koyu (lacivert-siyah), kırmızı vurgu
    centworks      : koyu (antrasit), altın ve yeşil vurgu
    scam_engineer  : açık ve renkli (gökyüzü mavisi → sıcak sarı), korku kırmızısı YOK
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

RGB = Tuple[int, int, int]


@dataclass(frozen=True)
class Tema:
    ad: str
    bg_ust: RGB          # gradyan üst
    bg_alt: RGB          # gradyan alt
    yazi: RGB            # ana yazı rengi
    kontur: RGB          # yazı konturu
    vurgu: RGB           # ana vurgu
    vurgu2: RGB          # ikinci vurgu
    notr: RGB            # nesne gövdeleri için nötr ton
    koyu: bool


TEMALAR = {
    "hidden_systems": Tema(
        ad="hidden_systems", bg_ust=(6, 9, 18), bg_alt=(22, 30, 48),
        yazi=(255, 255, 255), kontur=(0, 0, 0),
        vurgu=(255, 45, 45), vurgu2=(255, 170, 60), notr=(70, 82, 104), koyu=True),
    "centworks": Tema(
        ad="centworks", bg_ust=(14, 14, 16), bg_alt=(32, 34, 40),
        yazi=(255, 255, 255), kontur=(0, 0, 0),
        vurgu=(255, 196, 0), vurgu2=(34, 197, 94), notr=(78, 82, 92), koyu=True),
    "scam_engineer": Tema(
        ad="scam_engineer", bg_ust=(186, 226, 255), bg_alt=(255, 236, 170),
        yazi=(10, 31, 68), kontur=(255, 255, 255),
        vurgu=(0, 110, 255), vurgu2=(255, 140, 0), notr=(60, 80, 110), koyu=False),
}


def luminance(c: RGB) -> float:
    def ch(v: int) -> float:
        v = v / 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(x) for x in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: RGB, b: RGB) -> float:
    """WCAG kontrast oranı (1–21)."""
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)
