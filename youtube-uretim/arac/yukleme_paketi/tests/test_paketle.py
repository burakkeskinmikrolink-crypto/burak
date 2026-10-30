import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import paketle as pk  # noqa: E402


class TestPaketle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = pk.tum_paketler("2026-12-13")

    def test_sayilar(self):
        uzun = [x for x in self.p if x.tur == "uzun"]
        short = [x for x in self.p if x.tur == "short"]
        self.assertEqual(len(uzun), 16)
        self.assertEqual(len(short), 110)

    def test_tarih_siniri(self):
        self.assertTrue(all("2026-11-05" <= x.tarih <= "2026-12-13" for x in self.p))

    def test_sentetik_ses_satiri_en_sonda(self):
        for x in self.p:
            self.assertTrue(x.aciklama.rstrip().endswith(pk.SENTETIK), x.baslik)

    def test_seslendirme_temiz(self):
        for x in self.p:
            for yasak in ("SAHNE", "Wikimedia", "| ", "**", "Ekranda", "Reconstruction"):
                self.assertNotIn(yasak, x.seslendirme, (x.baslik, yasak))

    def test_short_alanlari(self):
        for x in self.p:
            if x.tur == "short":
                self.assertTrue(x.ilgili_video)
                self.assertLessEqual(len(x.baslik), 100)
                self.assertIn("[pause 400]", x.seslendirme.splitlines()[0])

    def test_uzun_alanlar(self):
        for x in self.p:
            if x.tur == "uzun":
                self.assertEqual(x.saat, "21:00")
                self.assertEqual(len(x.alternatifler), 2)
                self.assertIn("CHAPTERS", x.aciklama)
                self.assertTrue(os.path.exists(os.path.join(pk.KOK, x.kucuk_resim[0])), x.kucuk_resim[0])

    def test_ayni_gun_iki_short_farkli_saat(self):
        gorulen = {}
        for x in self.p:
            if x.tur == "short":
                key = (x.tarih, x.kanal, x.saat)
                self.assertNotIn(key, gorulen, key)
                gorulen[key] = True

    def test_yazma(self):
        with tempfile.TemporaryDirectory() as d:
            satir = pk.yaz(self.p[:3], os.path.join(d, "y"))
            for _, klasor in satir:
                self.assertTrue(os.path.exists(os.path.join(d, "y", klasor, "seslendirme.txt")))


if __name__ == "__main__":
    unittest.main()
