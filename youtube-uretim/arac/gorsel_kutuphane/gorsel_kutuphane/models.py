"""Ortak veri modeli: her kaynaktan gelen sonuç tek bir MediaItem'a dönüştürülür."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional


@dataclass
class MediaItem:
    source: str                 # "wikimedia" | "nasa" | "pexels" | "pixabay"
    source_id: str              # kaynaktaki benzersiz kimlik
    media_type: str             # "image" | "video"
    title: str
    author: str
    page_url: str               # insanın açacağı sayfa (atıfta kullanılır)
    download_url: str           # indirilecek dosya
    license_name: str           # kaynaktan gelen ham lisans adı
    license_url: str = ""
    width: Optional[int] = None
    height: Optional[int] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    @property
    def key(self) -> str:
        return f"{self.source}:{self.source_id}"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MediaItem":
        return cls(**data)
