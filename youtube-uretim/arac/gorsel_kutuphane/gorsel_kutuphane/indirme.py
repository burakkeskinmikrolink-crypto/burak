"""Dosya indirme (yalnızca lisansı kabul edilen öğeler)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from .licenses import evaluate_license
from .models import MediaItem

DEFAULT_EXT = {"image": ".jpg", "video": ".mp4"}


class LicenseRejected(RuntimeError):
    pass


def safe_filename(item: MediaItem) -> str:
    """Kaynak + kimlik + başlıktan Windows'ta da geçerli bir dosya adı üretir."""
    ext = Path(urlparse(item.download_url).path).suffix.lower()
    if not ext or len(ext) > 5:
        ext = DEFAULT_EXT.get(item.media_type, ".bin")
    slug = re.sub(r"[^A-Za-z0-9]+", "-", item.title).strip("-").lower()[:40] or "media"
    sid = re.sub(r"[^A-Za-z0-9]+", "", item.source_id)[:24]
    return f"{item.source}_{sid}_{slug}{ext}"


def download(item: MediaItem, target_dir: Path, session, user_agent: Optional[str] = None,
             chunk_size: int = 1 << 16) -> Path:
    decision = evaluate_license(item)
    if not decision.allowed:
        raise LicenseRejected(f"{item.key}: {decision.reason}")
    if not item.download_url:
        raise ValueError(f"{item.key}: indirme URL'si yok")
    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / safe_filename(item)
    headers = {"User-Agent": user_agent} if user_agent else {}
    with session.get(item.download_url, headers=headers, stream=True, timeout=120) as resp:
        resp.raise_for_status()
        tmp = path.with_suffix(path.suffix + ".part")
        with open(tmp, "wb") as fh:
            for chunk in resp.iter_content(chunk_size):
                if chunk:
                    fh.write(chunk)
        tmp.replace(path)
    return path
