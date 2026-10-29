"""Komut satırı arayüzü.

Örnekler (README'de ayrıntılı):
    python -m gorsel_kutuphane ara "data centre generator" --proje hs-04 --kaynak wikimedia,pexels
    python -m gorsel_kutuphane indir --proje hs-04 --secim 1,3
    python -m gorsel_kutuphane klip --proje hs-04 --dosya medya/xxx.jpg --efekt kenburns --hareket zoom_in
    python -m gorsel_kutuphane kaynaklar --proje hs-04
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from .config import load_settings
from .efektler import KEN_BURNS_MOVES, make_clips
from .indirme import LicenseRejected, download
from .kaynaklar import SEARCHERS
from .licenses import evaluate_license
from .models import MediaItem
from .proje import Project


def _session():
    import requests  # yalnızca ağ komutlarında gerekir
    return requests.Session()


def cmd_ara(args, settings) -> int:
    project = Project.open(Path(args.projeler), args.proje)
    session = _session()
    results: List[MediaItem] = []
    for name in [s.strip() for s in args.kaynak.split(",") if s.strip()]:
        if name not in SEARCHERS:
            print(f"[uyarı] bilinmeyen kaynak: {name}", file=sys.stderr)
            continue
        try:
            results += SEARCHERS[name](args.sorgu, settings, session, limit=args.adet, media_type=args.tur)
        except Exception as exc:  # bir kaynağın hatası diğerlerini durdurmasın
            print(f"[uyarı] {name}: {exc}", file=sys.stderr)
    project.save_last_search(results)
    print(f"{'#':>3}  {'KAYNAK':9} {'LİSANS':8} {'UYGUN':5}  BAŞLIK")
    for idx, item in enumerate(results, 1):
        d = evaluate_license(item)
        print(f"{idx:>3}  {item.source:9} {d.category[:8]:8} {'EVET' if d.allowed else 'HAYIR':5}  "
              f"{item.title[:60]}  ({item.width}x{item.height})")
    print(f"\n{len(results)} sonuç '{project.root / 'son_arama.json'}' dosyasına kaydedildi.")
    return 0


def cmd_indir(args, settings) -> int:
    project = Project.open(Path(args.projeler), args.proje)
    last = project.load_last_search()
    if not last:
        print("Önce 'ara' komutunu çalıştırın.", file=sys.stderr)
        return 1
    session = _session()
    picks = [int(x) for x in args.secim.split(",") if x.strip()]
    errors = 0
    for n in picks:
        if not 1 <= n <= len(last):
            print(f"[hata] geçersiz seçim: {n}", file=sys.stderr)
            errors += 1
            continue
        item = last[n - 1]
        try:
            path = download(item, project.media_dir, session, settings.wikimedia_user_agent)
            project.add(item, path)
            print(f"[tamam] {item.key} -> {path}")
        except LicenseRejected as exc:
            print(f"[red] {exc}", file=sys.stderr)
            errors += 1
    project.write_credits()
    return 1 if errors else 0


def cmd_klip(args, settings) -> int:
    project = Project.open(Path(args.projeler), args.proje)
    image = Path(args.dosya)
    if not image.is_absolute():
        image = project.root / image
    formats = ("yatay", "dikey") if args.format == "ikisi" else (args.format,)
    fg = Path(args.on_plan) if args.on_plan else None
    outputs = make_clips(image, project.clips_dir, args.efekt, formats, args.sure, args.hareket, fg)
    for out in outputs:
        print(f"[klip] {out}")
    return 0


def cmd_kaynaklar(args, settings) -> int:
    project = Project.open(Path(args.projeler), args.proje)
    path = project.write_credits()
    print(path.read_text(encoding="utf-8"))
    print(f"-> {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="gorsel_kutuphane", description="Telifsiz görsel arama ve klip aracı")
    p.add_argument("--projeler", default="projeler", help="Proje klasörlerinin kökü (varsayılan: ./projeler)")
    p.add_argument("--env", default=".env", help=".env dosyası yolu")
    sub = p.add_subparsers(dest="komut", required=True)

    a = sub.add_parser("ara", help="Anahtar kelimeyle arama")
    a.add_argument("sorgu")
    a.add_argument("--proje", required=True)
    a.add_argument("--kaynak", default="wikimedia,nasa,pexels,pixabay")
    a.add_argument("--tur", choices=["image", "video"], default="image")
    a.add_argument("--adet", type=int, default=10)
    a.set_defaults(func=cmd_ara)

    i = sub.add_parser("indir", help="Son aramadan seçilenleri indir (lisans kontrolüyle)")
    i.add_argument("--proje", required=True)
    i.add_argument("--secim", required=True, help="Örn. 1,3,5")
    i.set_defaults(func=cmd_indir)

    k = sub.add_parser("klip", help="Ken Burns / parallax klip üret")
    k.add_argument("--proje", required=True)
    k.add_argument("--dosya", required=True, help="Görsel yolu (proje klasörüne göre veya mutlak)")
    k.add_argument("--efekt", choices=["kenburns", "parallax"], default="kenburns")
    k.add_argument("--hareket", choices=list(KEN_BURNS_MOVES), default="zoom_in")
    k.add_argument("--format", choices=["yatay", "dikey", "ikisi"], default="ikisi")
    k.add_argument("--sure", type=float, default=6.0)
    k.add_argument("--on-plan", dest="on_plan", help="Parallax için saydam ön plan PNG'si (isteğe bağlı)")
    k.set_defaults(func=cmd_klip)

    c = sub.add_parser("kaynaklar", help="kaynaklar.txt üret")
    c.add_argument("--proje", required=True)
    c.set_defaults(func=cmd_kaynaklar)
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    settings = load_settings(Path(args.env))
    return args.func(args, settings)


if __name__ == "__main__":
    sys.exit(main())
