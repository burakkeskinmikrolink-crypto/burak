"""Lisans kontrolü ve atıf metni üretimi.

Kabul edilen lisanslar (başka hiçbir şey kabul edilmez):
    - Kamu malı (Public domain, PD-*, Public Domain Mark, ABD federal hükümet eserleri/NASA)
    - CC0
    - CC BY (tüm sürümler)
    - CC BY-SA (tüm sürümler)
    - Pexels License
    - Pixabay Content License

Reddedilenler: NC (ticari olmayan), ND (türev yok), GFDL, "All rights reserved",
tanınmayan/boş lisanslar. Şüpheli durumda RED verilir.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from typing import Optional

from .models import MediaItem

# Kategori sabitleri
PUBLIC_DOMAIN = "public_domain"
CC0 = "cc0"
CC_BY = "cc_by"
CC_BY_SA = "cc_by_sa"
PEXELS = "pexels"
PIXABAY = "pixabay"
REJECTED = "rejected"

ATTRIBUTION_REQUIRED = {CC_BY, CC_BY_SA}


@dataclass(frozen=True)
class LicenseDecision:
    allowed: bool
    category: str
    reason: str
    attribution_required: bool = False
    share_alike: bool = False


def strip_html(text: Optional[str]) -> str:
    """Wikimedia 'Artist' alanı gibi HTML içeren metinleri düz metne çevirir."""
    if not text:
        return ""
    no_tags = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", html.unescape(no_tags)).strip()


def _normalize(name: str) -> str:
    s = name.lower().strip()
    s = s.replace("_", " ").replace("–", "-")
    return re.sub(r"\s+", " ", s)


def classify_license(source: str, license_name: str, license_url: str = "") -> LicenseDecision:
    """Kaynak + lisans adı/URL'sinden karar üretir."""
    name = _normalize(license_name or "")
    url = (license_url or "").lower()
    combined = f"{name} {url}"

    if source == "pexels":
        return LicenseDecision(True, PEXELS, "Pexels License")
    if source == "pixabay":
        return LicenseDecision(True, PIXABAY, "Pixabay Content License")

    # Kısıtlayıcı ekler: önce reddet
    if re.search(r"\bnc\b|non-?commercial|by-nc", combined):
        return LicenseDecision(False, REJECTED, "Ticari olmayan (NC) lisans kabul edilmez")
    if re.search(r"\bnd\b|no-?deriv|by-nd|-nd\b", combined):
        return LicenseDecision(False, REJECTED, "Türev yasağı (ND) olan lisans kabul edilmez")
    if "gfdl" in combined or "gnu free documentation" in combined:
        return LicenseDecision(False, REJECTED, "GFDL kabul listesinde değil")
    if "all rights reserved" in combined or "copyrighted" in combined:
        return LicenseDecision(False, REJECTED, "Telifli içerik")

    if "cc0" in combined or "publicdomain/zero" in combined:
        return LicenseDecision(True, CC0, "CC0")
    if (name.startswith("pd") or "public domain" in combined or "publicdomain/mark" in combined
            or source == "nasa"):
        return LicenseDecision(True, PUBLIC_DOMAIN, "Kamu malı")
    if re.search(r"cc[ -]by[ -]sa|by-sa", combined):
        return LicenseDecision(True, CC_BY_SA, "CC BY-SA", attribution_required=True, share_alike=True)
    if re.search(r"cc[ -]by(\b|[ -]\d)|licenses/by/", combined):
        return LicenseDecision(True, CC_BY, "CC BY", attribution_required=True)

    return LicenseDecision(False, REJECTED, f"Tanınmayan veya kabul edilmeyen lisans: '{license_name}'")


def evaluate_license(item: MediaItem) -> LicenseDecision:
    decision = classify_license(item.source, item.license_name, item.license_url)
    # NASA: açıklamada telif işareti varsa (ör. ortak kurum fotoğrafı) reddet
    if item.source == "nasa" and decision.allowed:
        desc = str(item.extra.get("description", "")).lower()
        if "©" in desc or "copyright" in desc:
            return LicenseDecision(False, REJECTED, "NASA kaydında telif notu var; kullanma")
    return decision


def attribution_text(item: MediaItem, modified: bool = True) -> str:
    """YouTube açıklamasına yapıştırılacak tek satırlık atıf.

    CC BY / CC BY-SA için TASL (Title, Author, Source, License) biçimi zorunludur.
    Diğer lisanslarda atıf zorunlu değildir ama iyi uygulama olarak yine yazılır.
    """
    decision = evaluate_license(item)
    title = item.title or "Untitled"
    author = item.author or "Unknown author"
    change = " (modified: cropped, animated)" if modified else ""

    if decision.category in ATTRIBUTION_REQUIRED:
        lic = item.license_name or ("CC BY-SA" if decision.category == CC_BY_SA else "CC BY")
        lic_url = f" ({item.license_url})" if item.license_url else ""
        return f'"{title}" by {author}, {item.page_url}, licensed under {lic}{lic_url}{change}'
    if decision.category == PEXELS:
        return f"{'Video' if item.media_type == 'video' else 'Photo'} by {author} on Pexels: {item.page_url}"
    if decision.category == PIXABAY:
        return f"{'Video' if item.media_type == 'video' else 'Image'} by {author} from Pixabay: {item.page_url}"
    if item.source == "nasa":
        return (f'"{title}" — NASA, {item.page_url} (public domain; '
                f"use does not imply NASA endorsement)")
    if decision.category in (PUBLIC_DOMAIN, CC0):
        label = "CC0" if decision.category == CC0 else "public domain"
        return f'"{title}" by {author}, {item.page_url} ({label})'
    raise ValueError(f"Bu öğe kullanılamaz: {decision.reason}")
