"""Proje klasörü ve kaynaklar.txt üretimi.

Klasör yapısı:
    projeler/<proje_adi>/
        proje.json        kullanılan öğelerin kaydı (lisans kararı dahil)
        son_arama.json    son aramanın sonuçları (indir komutu için)
        medya/            indirilen dosyalar
        klipler/          üretilen Ken Burns / parallax klipleri
        kaynaklar.txt     YouTube açıklamasına yapıştırılacak atıf listesi
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from .licenses import ATTRIBUTION_REQUIRED, attribution_text, evaluate_license
from .models import MediaItem


@dataclass
class Project:
    root: Path

    @classmethod
    def open(cls, base: Path, name: str) -> "Project":
        root = base / name
        (root / "medya").mkdir(parents=True, exist_ok=True)
        (root / "klipler").mkdir(parents=True, exist_ok=True)
        return cls(root)

    @property
    def manifest_path(self) -> Path:
        return self.root / "proje.json"

    @property
    def media_dir(self) -> Path:
        return self.root / "medya"

    @property
    def clips_dir(self) -> Path:
        return self.root / "klipler"

    def load(self) -> Dict[str, dict]:
        if not self.manifest_path.exists():
            return {}
        return json.loads(self.manifest_path.read_text(encoding="utf-8"))

    def add(self, item: MediaItem, local_file: Path) -> None:
        data = self.load()
        record = item.to_dict()
        try:
            record["local_file"] = str(local_file.resolve().relative_to(self.root.resolve()))
        except ValueError:
            record["local_file"] = str(local_file)
        decision = evaluate_license(item)
        record["license_decision"] = {"allowed": decision.allowed, "category": decision.category,
                                      "reason": decision.reason}
        data[item.key] = record
        self.manifest_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def items(self) -> List[MediaItem]:
        out = []
        for record in self.load().values():
            fields = {k: v for k, v in record.items() if k in MediaItem.__dataclass_fields__}
            out.append(MediaItem.from_dict(fields))
        return out

    def save_last_search(self, items: List[MediaItem]) -> None:
        (self.root / "son_arama.json").write_text(
            json.dumps([i.to_dict() for i in items], ensure_ascii=False, indent=2), encoding="utf-8")

    def load_last_search(self) -> List[MediaItem]:
        path = self.root / "son_arama.json"
        if not path.exists():
            return []
        return [MediaItem.from_dict(d) for d in json.loads(path.read_text(encoding="utf-8"))]

    def write_credits(self) -> Path:
        path = self.root / "kaynaklar.txt"
        path.write_text(build_credits_text(self.items()), encoding="utf-8")
        return path


def build_credits_text(items: List[MediaItem]) -> str:
    """İki bölüm: atıf zorunlu olanlar (CC BY / BY-SA) ve diğerleri."""
    required, other = [], []
    for item in sorted(items, key=lambda i: (i.source, i.title.lower())):
        decision = evaluate_license(item)
        if not decision.allowed:
            continue
        line = f"- {attribution_text(item)}"
        (required if decision.category in ATTRIBUTION_REQUIRED else other).append(line)
    parts = ["VISUAL CREDITS", ""]
    if required:
        parts += ["Licensed under Creative Commons (attribution required):", *required, ""]
    if other:
        parts += ["Public domain, Pexels and Pixabay:", *other, ""]
    if any(evaluate_license(i).share_alike for i in items):
        parts += ["Note: some images are CC BY-SA; adaptations of those images are shared under the same licence.", ""]
    if not required and not other:
        parts += ["(no media recorded in this project)", ""]
    return "\n".join(parts)
