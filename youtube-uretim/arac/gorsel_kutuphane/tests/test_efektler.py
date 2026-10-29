import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from gorsel_kutuphane import efektler
from gorsel_kutuphane.efektler import (ClipSpec, build_ken_burns_command, build_parallax_command,
                                       ken_burns_filter, parallax_filter, spec_for)


class CommandTests(unittest.TestCase):
    def test_spec_sizes(self):
        self.assertEqual((spec_for("yatay").width, spec_for("yatay").height), (1920, 1080))
        self.assertEqual((spec_for("dikey").width, spec_for("dikey").height), (1080, 1920))
        self.assertEqual(spec_for("yatay", 6, 30).frames, 180)
        with self.assertRaises(ValueError):
            spec_for("kare")

    def test_ken_burns_filter_contains_zoompan_and_size(self):
        f = ken_burns_filter(spec_for("dikey", 6, 30), "zoom_in", 1.15)
        self.assertIn("zoompan=", f)
        self.assertIn("s=1080x1920", f)
        self.assertIn("d=180", f)
        self.assertIn("scale=2160:3840:force_original_aspect_ratio=increase", f)
        self.assertTrue(f.endswith("format=yuv420p"))

    def test_all_moves_build(self):
        for move in efektler.KEN_BURNS_MOVES:
            with self.subTest(move=move):
                self.assertIn("zoompan", ken_burns_filter(spec_for("yatay"), move))
        with self.assertRaises(ValueError):
            ken_burns_filter(spec_for("yatay"), "spin")

    def test_ken_burns_command(self):
        cmd = build_ken_burns_command(Path("in.jpg"), Path("out.mp4"), spec_for("yatay", 5, 25))
        self.assertEqual(cmd[:5], ["ffmpeg", "-y", "-loop", "1", "-i"])
        self.assertIn("-t", cmd)
        self.assertEqual(cmd[cmd.index("-t") + 1], "5.000")
        self.assertEqual(cmd[-1], "out.mp4")

    def test_parallax_with_and_without_foreground(self):
        spec = spec_for("yatay", 6)
        auto = parallax_filter(spec, has_foreground=False)
        self.assertIn("boxblur", auto)
        self.assertIn("[0:v]", auto.split(";")[1])
        manual = parallax_filter(spec, has_foreground=True)
        self.assertNotIn("boxblur", manual)
        self.assertIn("[1:v]", manual)
        cmd = build_parallax_command(Path("bg.jpg"), Path("o.mp4"), spec, Path("fg.png"))
        self.assertEqual(cmd.count("-i"), 2)
        self.assertIn("[out]", cmd)


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg/ffprobe yok")
class RenderTests(unittest.TestCase):
    """Sahte bir test görseliyle gerçekten kısa klip üretir (ağ gerekmez)."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.image = cls.tmp / "test_card.png"
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "testsrc=size=1200x800:rate=1",
                        "-frames:v", "1", str(cls.image)], check=True, capture_output=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def probe(self, path: Path):
        out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                              "stream=width,height", "-of", "json", str(path)],
                             check=True, capture_output=True, text=True).stdout
        s = json.loads(out)["streams"][0]
        return s["width"], s["height"]

    def test_ken_burns_both_formats(self):
        outs = efektler.make_clips(self.image, self.tmp / "klipler", "kenburns", ("yatay", "dikey"),
                                   duration=0.5, move="zoom_in", fps=10)
        self.assertEqual([self.probe(o) for o in outs], [(1920, 1080), (1080, 1920)])

    def test_parallax_auto(self):
        outs = efektler.make_clips(self.image, self.tmp / "klipler", "parallax", ("dikey",),
                                   duration=0.5, fps=10)
        self.assertEqual(self.probe(outs[0]), (1080, 1920))


if __name__ == "__main__":
    unittest.main()
