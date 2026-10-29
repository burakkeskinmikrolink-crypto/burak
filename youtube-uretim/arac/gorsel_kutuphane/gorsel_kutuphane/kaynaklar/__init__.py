"""Kaynak adaptörleri. Her modül iki fonksiyon sağlar:

    parse_*(json_dict) -> list[MediaItem]   (ağsız, test edilebilir)
    search(query, settings, session, ...) -> list[MediaItem]   (HTTP isteği yapar)
"""

from typing import Callable, Dict

from . import nasa, pexels, pixabay, wikimedia

SEARCHERS: Dict[str, Callable] = {
    "wikimedia": wikimedia.search,
    "nasa": nasa.search,
    "pexels": pexels.search,
    "pixabay": pixabay.search,
}

__all__ = ["SEARCHERS", "wikimedia", "nasa", "pexels", "pixabay"]
