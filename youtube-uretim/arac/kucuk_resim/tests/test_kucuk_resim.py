"""python -m unittest discover -s tests -t .   (arac/kucuk_resim klasöründe)"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import uret  # noqa: E402
from temalar import TEMALAR, contrast  # noqa: E402

VIDEOS = json.loads((HERE / "videolar.json").read_text(encoding="utf-8"))


class SpecTests(unittest.TestCase):
    def test_twelve_videos_two_variants(self):
        self.assertEqual(len(VIDEOS), 12)
        for v in VIDEOS:
            self.assertEqual(set(v["varyantlar"]), {"A", "B"}, v["id"])

    def test_max_four_words_and_known_objects(self):
        for v in VIDEOS:
            for key, var in v["varyantlar"].items():
                with self.subTest(video=v["id"], varyant=key):
                    self.assertLessEqual(len(uret.kelimeler(var["yazi"])), 4)
                    self.assertIn(var["nesne"], uret.NESNELER)

    def test_theme_contrast(self):
        for name, t in TEMALAR.items():
            with self.subTest(tema=name):
                self.assertGreaterEqual(min(contrast(t.yazi, t.bg_ust), contrast(t.yazi, t.bg_alt)), 4.5)

    def test_scam_engineer_is_light_and_has_no_red(self):
        t = TEMALAR["scam_engineer"]
        self.assertFalse(t.koyu)
        for c in (t.vurgu, t.vurgu2):
            self.assertFalse(c[0] > 200 and c[1] < 80 and c[2] < 80, f"kırmızı vurgu: {c}")

    def test_dark_channels(self):
        self.assertTrue(TEMALAR["hidden_systems"].koyu)
        self.assertTrue(TEMALAR["centworks"].koyu)

    def test_rule_violation_raises(self):
        with self.assertRaises(uret.KuralHatasi):
            uret.kurallari_kontrol("ONE TWO THREE FOUR FIVE", TEMALAR["centworks"])


class RenderTests(unittest.TestCase):
    def test_render_size_and_min_font(self):
        img, size = uret.kucuk_resim(VIDEOS[0], "A")
        self.assertEqual(img.size, (1280, 720))
        # Telefonda (360 px genişlik) yazı yüksekliği en az ~25 px kalsın
        self.assertGreaterEqual(size * 360 / 1280, 25)

    def test_all_variants_readable_on_phone(self):
        for v in VIDEOS:
            for key in ("A", "B"):
                lines, size = uret.yazi_yerlesimi(v["varyantlar"][key]["yazi"])
                with self.subTest(video=v["id"], varyant=key):
                    self.assertGreaterEqual(size, 95, f"punto {size} çok küçük")
                    self.assertLessEqual(len(lines), 3)

    def test_main_writes_files(self):
        out = Path(tempfile.mkdtemp())
        self.assertEqual(uret.main(["--sadece", "SE-03", "--cikti", str(out)]), 0)
        for name in ("SE-03_A.png", "SE-03_B.png", "onizleme/SE-03_AB_telefon.png",
                     "onizleme/telefon_izgara.png", "onizleme/kucuk_izgara.png"):
            self.assertTrue((out / name).exists(), name)


if __name__ == "__main__":
    unittest.main()
