"""Fotoğrafı hareketlendirme: Ken Burns ve parallax klipleri (ffmpeg ile).

Çıktı boyutları:
    yatay  -> 1920x1080 (uzun video)
    dikey  -> 1080x1920 (Shorts)

Komutlar `build_*_command` fonksiyonlarıyla liste olarak üretilir (test edilebilir),
`render()` ise ffmpeg'i çalıştırır. ffmpeg PATH'te olmalıdır (README: Windows kurulumu).
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence

FORMATS = {"yatay": (1920, 1080), "dikey": (1080, 1920)}
KEN_BURNS_MOVES = ("zoom_in", "zoom_out", "pan_left", "pan_right", "pan_up", "pan_down")


class FfmpegNotFound(RuntimeError):
    pass


@dataclass
class ClipSpec:
    width: int
    height: int
    duration: float = 6.0
    fps: int = 30

    @property
    def frames(self) -> int:
        return max(1, int(round(self.duration * self.fps)))


def spec_for(fmt: str, duration: float = 6.0, fps: int = 30) -> ClipSpec:
    if fmt not in FORMATS:
        raise ValueError(f"Bilinmeyen format: {fmt} (yatay | dikey)")
    w, h = FORMATS[fmt]
    return ClipSpec(w, h, duration, fps)


def _cover(width: int, height: int, factor: float = 1.0) -> str:
    """Görseli hedef en-boy oranını tamamen kaplayacak şekilde ölçekler ve kırpar."""
    w, h = int(width * factor) // 2 * 2, int(height * factor) // 2 * 2
    return (f"scale={w}:{h}:force_original_aspect_ratio=increase,"
            f"crop={w}:{h},setsar=1")


def ken_burns_filter(spec: ClipSpec, move: str = "zoom_in", zoom: float = 1.15) -> str:
    """zoompan tabanlı Ken Burns. Titremeyi azaltmak için kaynak önce 2x ölçeklenir."""
    if move not in KEN_BURNS_MOVES:
        raise ValueError(f"Bilinmeyen hareket: {move} ({', '.join(KEN_BURNS_MOVES)})")
    n = spec.frames
    step = (zoom - 1.0) / n
    cx, cy = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    if move == "zoom_in":
        z, x, y = f"min(1+{step:.6f}*on,{zoom})", cx, cy
    elif move == "zoom_out":
        z, x, y = f"max({zoom}-{step:.6f}*on,1)", cx, cy
    else:
        z = f"{zoom}"
        span_x, span_y = "(iw-iw/zoom)", "(ih-ih/zoom)"
        if move == "pan_left":
            x, y = f"{span_x}*(1-on/{n})", cy
        elif move == "pan_right":
            x, y = f"{span_x}*on/{n}", cy
        elif move == "pan_up":
            x, y = cx, f"{span_y}*(1-on/{n})"
        else:  # pan_down
            x, y = cx, f"{span_y}*on/{n}"
    return (f"{_cover(spec.width, spec.height, 2.0)},"
            f"zoompan=z='{z}':x='{x}':y='{y}':d={n}:s={spec.width}x{spec.height}:fps={spec.fps},"
            f"format=yuv420p")


def build_ken_burns_command(image: Path, output: Path, spec: ClipSpec, move: str = "zoom_in",
                            zoom: float = 1.15, ffmpeg: str = "ffmpeg") -> List[str]:
    return [
        ffmpeg, "-y", "-loop", "1", "-i", str(image),
        "-vf", ken_burns_filter(spec, move, zoom),
        "-t", f"{spec.duration:.3f}", "-r", str(spec.fps),
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-an", str(output),
    ]


def parallax_filter(spec: ClipSpec, has_foreground: bool, bg_travel: float = 0.06,
                    fg_travel: float = 0.16, fg_scale: float = 0.72) -> str:
    """İki katmanlı parallax.

    - Arka plan: hedefin (1+bg_travel) katı genişlikte kaplanır ve yavaşça kayar.
    - Ön plan: verilmişse (saydam PNG) aynı yönde daha hızlı kayar -> derinlik hissi.
    - Ön plan yoksa "sözde parallax": aynı görselin ortası, hafif gölgeyle ön plana
      alınır ve daha hızlı kayar; arka plan bulanıklaştırılır. Gerçek parallax için
      GIMP/Photoshop ile ayrılmış bir ön plan PNG'si verilmesi önerilir.
    """
    W, H, D = spec.width, spec.height, spec.duration
    bw = int(W * (1 + bg_travel)) // 2 * 2
    bh = int(H * (1 + bg_travel)) // 2 * 2
    bg = (f"[0:v]{_cover(W, H, 1 + bg_travel)},"
          + ("boxblur=8:1," if not has_foreground else "")
          + f"crop={W}:{H}:x='({bw}-{W})*t/{D}':y='({bh}-{H})/2'[bg]")
    fw = int(W * fg_scale) // 2 * 2
    fh = int(H * fg_scale) // 2 * 2
    travel = int(W * fg_travel)
    x_expr = f"(({W}-{fw})/2)+{travel // 2}-{travel}*t/{D}"
    y_expr = f"({H}-{fh})/2"
    if has_foreground:
        fg = f"[1:v]scale={fw}:-2,format=rgba[fg]"
    else:
        fg = f"[0:v]{_cover(fw, fh)},format=rgba[fg]"
    return (f"{bg};{fg};[bg][fg]overlay=x='{x_expr}':y='{y_expr}':shortest=1,"
            f"format=yuv420p[out]")


def build_parallax_command(image: Path, output: Path, spec: ClipSpec,
                           foreground: Optional[Path] = None, ffmpeg: str = "ffmpeg") -> List[str]:
    cmd = [ffmpeg, "-y", "-loop", "1", "-t", f"{spec.duration:.3f}", "-i", str(image)]
    if foreground is not None:
        cmd += ["-loop", "1", "-t", f"{spec.duration:.3f}", "-i", str(foreground)]
    cmd += [
        "-filter_complex", parallax_filter(spec, foreground is not None),
        "-map", "[out]", "-t", f"{spec.duration:.3f}", "-r", str(spec.fps),
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-an", str(output),
    ]
    return cmd


def find_ffmpeg(explicit: Optional[str] = None) -> str:
    path = explicit or shutil.which("ffmpeg")
    if not path:
        raise FfmpegNotFound("ffmpeg bulunamadı. README'deki Windows kurulum adımlarına bakın.")
    return path


def render(cmd: Sequence[str]) -> None:
    result = subprocess.run(list(cmd), capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg hata verdi:\n{result.stderr[-2000:]}")


def make_clips(image: Path, out_dir: Path, effect: str = "kenburns", formats: Sequence[str] = ("yatay", "dikey"),
               duration: float = 6.0, move: str = "zoom_in", foreground: Optional[Path] = None,
               fps: int = 30, ffmpeg: Optional[str] = None) -> List[Path]:
    """Bir görselden istenen formatlarda klip üretir ve dosya yollarını döndürür."""
    exe = find_ffmpeg(ffmpeg)
    out_dir.mkdir(parents=True, exist_ok=True)
    outputs = []
    for fmt in formats:
        spec = spec_for(fmt, duration, fps)
        suffix = move if effect == "kenburns" else "parallax"
        out = out_dir / f"{image.stem}_{suffix}_{spec.width}x{spec.height}.mp4"
        if effect == "kenburns":
            cmd = build_ken_burns_command(image, out, spec, move, ffmpeg=exe)
        elif effect == "parallax":
            cmd = build_parallax_command(image, out, spec, foreground, ffmpeg=exe)
        else:
            raise ValueError("efekt: kenburns | parallax")
        render(cmd)
        outputs.append(out)
    return outputs
