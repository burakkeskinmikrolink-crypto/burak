"""Ayarlar: API anahtarları .env dosyasından (veya ortam değişkenlerinden) okunur.

Beklenen anahtarlar (bkz. .env.example):
    PEXELS_API_KEY        Pexels API anahtarı (Pexels araması için zorunlu)
    PIXABAY_API_KEY       Pixabay API anahtarı (Pixabay araması için zorunlu)
    NASA_API_KEY          İsteğe bağlı; NASA Image Library anahtar istemez
    WIKIMEDIA_USER_AGENT  Wikimedia politikası gereği iletişim bilgili User-Agent
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

DEFAULT_USER_AGENT = "gorsel-kutuphane/0.1 (YouTube production tool; contact: set WIKIMEDIA_USER_AGENT)"


def parse_env_file(path: Path) -> Dict[str, str]:
    """Basit .env ayrıştırıcı (python-dotenv kurulu değilse de çalışsın diye)."""
    values: Dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export "):]
        key, value = line.split("=", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        values[key.strip()] = value
    return values


@dataclass
class Settings:
    pexels_api_key: Optional[str] = None
    pixabay_api_key: Optional[str] = None
    nasa_api_key: Optional[str] = None
    wikimedia_user_agent: str = DEFAULT_USER_AGENT


def load_settings(env_path: Optional[Path] = None) -> Settings:
    """Önce .env, sonra ortam değişkenleri (ortam değişkeni önceliklidir)."""
    path = env_path or Path.cwd() / ".env"
    file_values = parse_env_file(path)

    def get(name: str) -> Optional[str]:
        return os.environ.get(name) or file_values.get(name) or None

    return Settings(
        pexels_api_key=get("PEXELS_API_KEY"),
        pixabay_api_key=get("PIXABAY_API_KEY"),
        nasa_api_key=get("NASA_API_KEY"),
        wikimedia_user_agent=get("WIKIMEDIA_USER_AGENT") or DEFAULT_USER_AGENT,
    )
