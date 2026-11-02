"""NASA Image and Video Library API (anahtar gerekmez).

Belge: https://images.nasa.gov/docs/images.nasa.gov_api_docs.pdf
Arama:  https://images-api.nasa.gov/search?q=...&media_type=image
Dosya:  https://images-api.nasa.gov/asset/{nasa_id}  -> orijinal dosya listesi

Not: NASA logoları kamu malı değildir ve NASA'nın onayı ima edilemez.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..models import MediaItem

SEARCH_URL = "https://images-api.nasa.gov/search"
ASSET_URL = "https://images-api.nasa.gov/asset/{nasa_id}"
PAGE_URL = "https://images.nasa.gov/details/{nasa_id}"


def build_params(query: str, media_type: str) -> Dict[str, Any]:
    return {"q": query, "media_type": "video" if media_type == "video" else "image"}


def parse_search(data: Dict[str, Any], limit: int = 10) -> List[MediaItem]:
    items: List[MediaItem] = []
    for entry in ((data.get("collection") or {}).get("items") or [])[:limit]:
        meta = (entry.get("data") or [{}])[0]
        nasa_id = meta.get("nasa_id")
        if not nasa_id:
            continue
        links = entry.get("links") or []
        preview = links[0].get("href", "") if links else ""
        author = meta.get("photographer") or meta.get("secondary_creator") or meta.get("center") or "NASA"
        items.append(MediaItem(
            source="nasa",
            source_id=nasa_id,
            media_type=meta.get("media_type", "image"),
            title=meta.get("title", nasa_id),
            author=f"NASA ({author})" if author != "NASA" else "NASA",
            page_url=PAGE_URL.format(nasa_id=nasa_id),
            download_url=preview,  # asset çözümlenince orijinalle değiştirilir
            license_name="NASA media (public domain unless noted)",
            license_url="https://www.nasa.gov/nasa-brand-center/images-and-media/",
            extra={"description": meta.get("description", ""), "center": meta.get("center", "")},
        ))
    return items


def pick_original(asset_data: Dict[str, Any], media_type: str = "image") -> Optional[str]:
    """Asset listesinden en yüksek çözünürlüklü dosyayı seçer (~orig > ~large)."""
    hrefs = [i.get("href", "") for i in ((asset_data.get("collection") or {}).get("items") or [])]
    if media_type == "video":
        for suffix in ("~orig.mp4", "~large.mp4", "~medium.mp4", ".mp4"):
            for h in hrefs:
                if h.endswith(suffix):
                    return h
        return None
    for suffix in ("~orig.jpg", "~orig.png", "~orig.tif", "~large.jpg", "~large.png"):
        for h in hrefs:
            if h.lower().endswith(suffix):
                return h
    return hrefs[0] if hrefs else None


def search(query: str, settings, session, limit: int = 10, media_type: str = "image",
           resolve_assets: bool = True) -> List[MediaItem]:
    resp = session.get(SEARCH_URL, params=build_params(query, media_type), timeout=30)
    resp.raise_for_status()
    items = parse_search(resp.json(), limit)
    if resolve_assets:
        for item in items:
            a = session.get(ASSET_URL.format(nasa_id=item.source_id), timeout=30)
            if a.ok:
                original = pick_original(a.json(), item.media_type)
                if original:
                    item.download_url = original
    return items
