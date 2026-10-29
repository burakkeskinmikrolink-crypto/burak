"""Wikimedia Commons API (MediaWiki action API).

Belge: https://commons.wikimedia.org/w/api.php
Wikimedia, iletişim bilgisi içeren bir User-Agent ister (WIKIMEDIA_USER_AGENT).
"""

from __future__ import annotations

from typing import Any, Dict, List

from ..licenses import strip_html
from ..models import MediaItem

API_URL = "https://commons.wikimedia.org/w/api.php"


def build_params(query: str, limit: int, media_type: str) -> Dict[str, Any]:
    filetype = "filetype:video" if media_type == "video" else "filetype:bitmap"
    return {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f"{query} {filetype}",
        "gsrnamespace": 6,  # File:
        "gsrlimit": max(1, min(limit, 50)),
        "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata",
        "iiurlwidth": 1920,
    }


def _meta(ext: Dict[str, Any], key: str) -> str:
    value = ext.get(key, {})
    return strip_html(value.get("value") if isinstance(value, dict) else str(value))


def parse_response(data: Dict[str, Any], media_type: str = "image") -> List[MediaItem]:
    pages = (data.get("query") or {}).get("pages") or {}
    items: List[MediaItem] = []
    for page in sorted(pages.values(), key=lambda p: p.get("index", 0)):
        infos = page.get("imageinfo") or []
        if not infos:
            continue
        info = infos[0]
        ext = info.get("extmetadata") or {}
        title = _meta(ext, "ObjectName") or page.get("title", "").replace("File:", "")
        items.append(MediaItem(
            source="wikimedia",
            source_id=str(page.get("pageid", page.get("title", ""))),
            media_type=media_type,
            title=title,
            author=_meta(ext, "Artist") or _meta(ext, "Credit") or "Unknown author",
            page_url=info.get("descriptionurl", ""),
            download_url=info.get("url", ""),
            license_name=_meta(ext, "LicenseShortName") or _meta(ext, "UsageTerms"),
            license_url=_meta(ext, "LicenseUrl"),
            width=info.get("width"),
            height=info.get("height"),
            extra={"mime": info.get("mime", ""), "thumb_url": info.get("thumburl", "")},
        ))
    return items


def search(query: str, settings, session, limit: int = 10, media_type: str = "image") -> List[MediaItem]:
    headers = {"User-Agent": settings.wikimedia_user_agent}
    resp = session.get(API_URL, params=build_params(query, limit, media_type), headers=headers, timeout=30)
    resp.raise_for_status()
    return parse_response(resp.json(), media_type)
