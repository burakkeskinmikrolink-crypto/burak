"""Testler için sahte HTTP oturumu ve örnek API yanıtları (ağ kullanılmaz)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional


class FakeResponse:
    def __init__(self, payload: Any = None, status: int = 200, content: bytes = b""):
        self._payload = payload
        self.status_code = status
        self.ok = 200 <= status < 300
        self._content = content

    def json(self):
        return self._payload

    def raise_for_status(self):
        if not self.ok:
            raise RuntimeError(f"HTTP {self.status_code}")

    def iter_content(self, chunk_size: int = 1024):
        for i in range(0, len(self._content), chunk_size):
            yield self._content[i:i + chunk_size]

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class FakeSession:
    """URL önekine göre hazır yanıt döndürür ve yapılan çağrıları kaydeder."""

    def __init__(self, routes: Dict[str, FakeResponse]):
        self.routes = routes
        self.calls: List[Dict[str, Any]] = []

    def get(self, url: str, params: Optional[dict] = None, headers: Optional[dict] = None, **kwargs):
        self.calls.append({"url": url, "params": params or {}, "headers": headers or {}, **kwargs})
        for prefix in sorted(self.routes, key=len, reverse=True):
            if url.startswith(prefix):
                return self.routes[prefix]
        return FakeResponse({}, status=404)


WIKIMEDIA_RESPONSE = {
    "query": {"pages": {
        "101": {"pageid": 101, "index": 2, "title": "File:Diesel generator.jpg", "imageinfo": [{
            "url": "https://upload.wikimedia.org/a/ab/Diesel_generator.jpg",
            "descriptionurl": "https://commons.wikimedia.org/wiki/File:Diesel_generator.jpg",
            "width": 4000, "height": 3000, "mime": "image/jpeg",
            "extmetadata": {
                "ObjectName": {"value": "Diesel generator"},
                "Artist": {"value": "<a href=\"//commons.wikimedia.org/wiki/User:Example\">Jane Example</a>"},
                "LicenseShortName": {"value": "CC BY-SA 4.0"},
                "LicenseUrl": {"value": "https://creativecommons.org/licenses/by-sa/4.0"},
            }}]},
        "102": {"pageid": 102, "index": 1, "title": "File:Server room.jpg", "imageinfo": [{
            "url": "https://upload.wikimedia.org/b/bc/Server_room.jpg",
            "descriptionurl": "https://commons.wikimedia.org/wiki/File:Server_room.jpg",
            "width": 1920, "height": 1080, "mime": "image/jpeg",
            "extmetadata": {
                "Artist": {"value": "John Doe"},
                "LicenseShortName": {"value": "CC BY-NC 2.0"},
                "LicenseUrl": {"value": "https://creativecommons.org/licenses/by-nc/2.0"},
            }}]},
        "103": {"pageid": 103, "index": 3, "title": "File:Old telephone.png", "imageinfo": [{
            "url": "https://upload.wikimedia.org/c/cd/Old_telephone.png",
            "descriptionurl": "https://commons.wikimedia.org/wiki/File:Old_telephone.png",
            "width": 2000, "height": 1500, "mime": "image/png",
            "extmetadata": {
                "Artist": {"value": "Unknown"},
                "LicenseShortName": {"value": "Public domain"},
            }}]},
    }}
}

NASA_SEARCH_RESPONSE = {"collection": {"items": [
    {"data": [{"nasa_id": "iss071e000001", "title": "Earth at night", "media_type": "image",
               "center": "JSC", "description": "City lights seen from the ISS."}],
     "links": [{"href": "https://images-assets.nasa.gov/image/iss071e000001/iss071e000001~thumb.jpg"}]},
    {"data": [{"nasa_id": "partner001", "title": "Partner photo", "media_type": "image",
               "description": "Image © Partner Agency. Used with permission."}],
     "links": [{"href": "https://images-assets.nasa.gov/image/partner001/partner001~thumb.jpg"}]},
]}}

NASA_ASSET_RESPONSE = {"collection": {"items": [
    {"href": "https://images-assets.nasa.gov/image/iss071e000001/iss071e000001~thumb.jpg"},
    {"href": "https://images-assets.nasa.gov/image/iss071e000001/iss071e000001~large.jpg"},
    {"href": "https://images-assets.nasa.gov/image/iss071e000001/iss071e000001~orig.jpg"},
    {"href": "https://images-assets.nasa.gov/image/iss071e000001/metadata.json"},
]}}

PEXELS_PHOTOS_RESPONSE = {"photos": [{
    "id": 5551234, "width": 6000, "height": 4000, "url": "https://www.pexels.com/photo/card-terminal-5551234/",
    "photographer": "Ana Photographer", "photographer_url": "https://www.pexels.com/@ana",
    "alt": "Card payment terminal", "src": {"original": "https://images.pexels.com/photos/5551234/a.jpeg",
                                            "large2x": "https://images.pexels.com/photos/5551234/b.jpeg"}}]}

PEXELS_VIDEOS_RESPONSE = {"videos": [{
    "id": 777, "url": "https://www.pexels.com/video/server-room-777/", "duration": 12,
    "user": {"name": "Video Maker", "url": "https://www.pexels.com/@vm"},
    "video_files": [
        {"link": "https://videos.pexels.com/777-sd.mp4", "width": 960, "height": 540, "file_type": "video/mp4"},
        {"link": "https://videos.pexels.com/777-hd.mp4", "width": 1920, "height": 1080, "file_type": "video/mp4"},
        {"link": "https://videos.pexels.com/777-4k.mp4", "width": 3840, "height": 2160, "file_type": "video/mp4"},
    ]}]}

PIXABAY_IMAGES_RESPONSE = {"hits": [{
    "id": 42, "pageURL": "https://pixabay.com/photos/penny-coin-42/", "tags": "penny, coin, cent",
    "largeImageURL": "https://pixabay.com/get/42_1280.jpg", "imageWidth": 5000, "imageHeight": 3300,
    "user": "coinlover"}]}

PIXABAY_VIDEOS_RESPONSE = {"hits": [{
    "id": 99, "pageURL": "https://pixabay.com/videos/thermometer-99/", "tags": "thermometer, heat",
    "duration": 15, "user": "heatcam",
    "videos": {"large": {"url": "", "width": 0, "height": 0},
               "medium": {"url": "https://cdn.pixabay.com/99_medium.mp4", "width": 1920, "height": 1080}}}]}
