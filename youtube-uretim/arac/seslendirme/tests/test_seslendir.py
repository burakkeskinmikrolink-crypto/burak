import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import seslendir as s  # noqa: E402

ORNEK = """## Senaryo

### [SAHNE 1 | görsel | 0:00–0:12]
> First sentence. Is this a question?
>
> A pause here [pause 1200] and then more.

### [SAHNE 2 | görsel | 0:12–0:20]
> [slow]Read this slowly.[/slow] Normal speed in europe-west2.

## Başlık seçenekleri
"""


class TestPlan(unittest.TestCase):
    def setUp(self):
        self.segs = s.plan(ORNEK, {"europe-west2": "europe west two"})

    def test_soru_sonrasi_pause(self):
        q = [x for x in self.segs if x.metin.endswith("?")][0]
        self.assertGreaterEqual(q.sonra_ms, s.SORU_PAUSE)

    def test_acik_pause(self):
        seg = [x for x in self.segs if x.metin == "A pause here"][0]
        self.assertEqual(seg.sonra_ms, 1200)

    def test_yavas(self):
        seg = [x for x in self.segs if x.metin.startswith("Read this")][0]
        self.assertAlmostEqual(seg.hiz, s.YAVAS_CARPAN)

    def test_telaffuz(self):
        self.assertTrue(any("europe west two" in x.metin for x in self.segs))
        self.assertFalse(any("[" in x.metin for x in self.segs))

    def test_sahne_sonu(self):
        seg = [x for x in self.segs if x.metin.startswith("and then more")][0]
        self.assertGreaterEqual(seg.sonra_ms, s.SAHNE_PAUSE)

    def test_gercek_senaryo(self):
        kok = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        segs = s.plan(open(os.path.join(kok, "hidden_systems/08-v2.md"), encoding="utf-8").read())
        self.assertGreater(len(segs), 50)
        self.assertFalse(any("<" in x.metin for x in segs))


if __name__ == "__main__":
    unittest.main()
