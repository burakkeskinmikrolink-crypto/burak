import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from transkript import anlatim  # noqa: E402

ORNEK = """# Başlık
## Senaryo

### [SAHNE 1 | görsel | 0:00–0:12]
> First line of narration.
> Still the same paragraph.
>
> Second paragraph <break time="600ms"/> with a pause [pause].

### [SAHNE 2 | görsel | 0:12–0:17]
> This channel is made by a telecom engineer.

## Başlık seçenekleri
1. Not narration
> not narration either
"""


class TestTranskript(unittest.TestCase):
    def test_paragraflar(self):
        p = anlatim(ORNEK)
        self.assertEqual(p, ["First line of narration. Still the same paragraph.",
                             "Second paragraph with a pause.",
                             "This channel is made by a telecom engineer."])

    def test_senaryo_disi_alinmaz(self):
        self.assertNotIn("not narration either", " ".join(anlatim(ORNEK)))

    def test_bolum_yoksa_hata(self):
        with self.assertRaises(ValueError):
            anlatim("# boş\n## Başlık seçenekleri\n")

    def test_gercek_dosyalar(self):
        kok = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        for yol in ["hidden_systems/04-v2.md", "centworks/03-v2.md", "scam_engineer/03-v2.md",
                    "scam_engineer/evergreen-01.md"]:
            p = anlatim(open(os.path.join(kok, yol), encoding="utf-8").read())
            kelime = len(" ".join(p).split())
            self.assertTrue(1000 <= kelime <= 1450, (yol, kelime))
            self.assertNotIn("<", " ".join(p))


if __name__ == "__main__":
    unittest.main()
