"""Pixabay API (anahtar gerekir: PIXABAY_API_KEY).

Belge: https://pixabay.com/api/docs/
Görsel: https://pixabay.com/api/
Video:  https://pixabay.com/api/videos/
Not: Pixabay, görsel URL'lerinin uzun süre sıcak bağlantı (hotlink) ile kullanılmamasını,
dosyaların indirilmesini ister; bu modül zaten indirir.
"""

from __future__ import annotations

from typing import Any, Dict, List

from ..models import MediaItem

IMAGE_URL = "https://pixabay.com/api/"
VIDEO_URL = "https://pixabay.com/api/videos/"


class MissingApiKey(RuntimeError):
    pass


def build_params(query: str, limit: int, api_key: str, media_type: str) -> Dict[str, Any]:
    params: Dict[str, Any] = {
        "key": api_key,
        "q": query[:100],
        "per_page": max(3, min(limit, 200)),  # Pixabay: 3–200
        "safesearch": "true",
    }
    if media_type != "video":
        params["image_type"] = "photo"
    return params


def parse_images(data: Dict[str, Any]) -> List[MediaItem]:
    items = []
    for h in data.get("hits") or []:
        items.append(MediaItem(
            source="pixabay", source_id=str(h.get("id")), media_type="image",
            title=h.get("tags") or f"Pixabay image {h.get('id')}",
            author=h.get("user") or "Unknown",
            page_url=h.get("pageURL", ""),
            download_url=h.get("largeImageURL") or h.get("webformatURL", ""),
            license_name="Pixabay Content License", license_url="https://pixabay.com/service/license-summary/",
            width=h.get("imageWidth"), height=h.get("imageHeight"),
        ))
    return items


def parse_videos(data: Dict[str, Any]) -> List[MediaItem]:
    items = []
    for h in data.get("hits") or []:
        videos = h.get("videos") or {}
        best = videos.get("large") or videos.get("medium") or videos.get("small") or {}
        if not best.get("url"):
            best = videos.get("medium") or videos.get("small") or {}
        items.append(MediaItem(
            source="pixabay", source_id=str(h.get("id")), media_type="video",
            title=h.get("tags") or f"Pixabay video {h.get('id')}",
            author=h.get("user") or "Unknown",
            page_url=h.get("pageURL", ""),
            download_url=best.get("url", ""),
            license_name="Pixabay Content License", license_url="https://pixabay.com/service/license-summary/",
            width=best.get("width"), height=best.get("height"),
            extra={"duration": h.get("duration")},
        ))
    return items


def search(query: str, settings, session, limit: int = 10, media_type: str = "image") -> List[MediaItem]:
    if not settings.pixabay_api_key:
        raise MissingApiKey("PIXABAY_API_KEY .env dosyasında tanımlı değil")
    url = VIDEO_URL if media_type == "video" else IMAGE_URL
    resp = session.get(url, params=build_params(query, limit, settings.pixabay_api_key, media_type), timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return parse_videos(data) if media_type == "video" else parse_images(data)
