"""Pexels API (anahtar gerekir: PEXELS_API_KEY).

Belge: https://www.pexels.com/api/documentation/
Fotoğraf: https://api.pexels.com/v1/search
Video:    https://api.pexels.com/videos/search
"""

from __future__ import annotations

from typing import Any, Dict, List

from ..models import MediaItem

PHOTO_URL = "https://api.pexels.com/v1/search"
VIDEO_URL = "https://api.pexels.com/videos/search"


class MissingApiKey(RuntimeError):
    pass


def build_params(query: str, limit: int, orientation: str = "") -> Dict[str, Any]:
    params: Dict[str, Any] = {"query": query, "per_page": max(1, min(limit, 80))}
    if orientation in ("landscape", "portrait", "square"):
        params["orientation"] = orientation
    return params


def parse_photos(data: Dict[str, Any]) -> List[MediaItem]:
    items = []
    for p in data.get("photos") or []:
        src = p.get("src") or {}
        items.append(MediaItem(
            source="pexels", source_id=str(p.get("id")), media_type="image",
            title=p.get("alt") or f"Pexels photo {p.get('id')}",
            author=p.get("photographer") or "Unknown",
            page_url=p.get("url", ""),
            download_url=src.get("original") or src.get("large2x") or src.get("large", ""),
            license_name="Pexels License", license_url="https://www.pexels.com/license/",
            width=p.get("width"), height=p.get("height"),
            extra={"photographer_url": p.get("photographer_url", "")},
        ))
    return items


def _best_video_file(files: List[Dict[str, Any]], target_width: int = 1920) -> Dict[str, Any]:
    mp4 = [f for f in files if f.get("file_type") == "video/mp4" and f.get("width")]
    if not mp4:
        return files[0] if files else {}
    at_least = [f for f in mp4 if f["width"] >= target_width]
    return min(at_least, key=lambda f: f["width"]) if at_least else max(mp4, key=lambda f: f["width"])


def parse_videos(data: Dict[str, Any]) -> List[MediaItem]:
    items = []
    for v in data.get("videos") or []:
        best = _best_video_file(v.get("video_files") or [])
        user = v.get("user") or {}
        items.append(MediaItem(
            source="pexels", source_id=str(v.get("id")), media_type="video",
            title=f"Pexels video {v.get('id')}",
            author=user.get("name") or "Unknown",
            page_url=v.get("url", ""),
            download_url=best.get("link", ""),
            license_name="Pexels License", license_url="https://www.pexels.com/license/",
            width=best.get("width"), height=best.get("height"),
            extra={"duration": v.get("duration")},
        ))
    return items


def search(query: str, settings, session, limit: int = 10, media_type: str = "image",
           orientation: str = "") -> List[MediaItem]:
    if not settings.pexels_api_key:
        raise MissingApiKey("PEXELS_API_KEY .env dosyasında tanımlı değil")
    url = VIDEO_URL if media_type == "video" else PHOTO_URL
    resp = session.get(url, params=build_params(query, limit, orientation),
                       headers={"Authorization": settings.pexels_api_key}, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return parse_videos(data) if media_type == "video" else parse_photos(data)
