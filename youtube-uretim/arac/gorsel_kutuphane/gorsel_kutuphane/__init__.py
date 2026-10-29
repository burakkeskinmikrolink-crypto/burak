"""gorsel_kutuphane: telifsiz görsel/video arama, lisans kontrolü, Ken Burns/parallax klip
üretimi ve YouTube açıklaması için atıf listesi (kaynaklar.txt).

Kullanım için README.md dosyasına bakın.
"""

from .models import MediaItem
from .licenses import LicenseDecision, evaluate_license, attribution_text

__all__ = ["MediaItem", "LicenseDecision", "evaluate_license", "attribution_text"]
__version__ = "0.1.0"
