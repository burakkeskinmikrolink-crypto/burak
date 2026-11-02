import unittest

from gorsel_kutuphane.licenses import (CC0, CC_BY, CC_BY_SA, PEXELS, PIXABAY, PUBLIC_DOMAIN, REJECTED,
                                       attribution_text, classify_license, evaluate_license, strip_html)
from gorsel_kutuphane.models import MediaItem


def item(source="wikimedia", license_name="CC BY 4.0", license_url="", **kw):
    base = dict(source=source, source_id="1", media_type="image", title="Diesel generator",
                author="Jane Example", page_url="https://commons.wikimedia.org/wiki/File:X.jpg",
                download_url="https://upload.wikimedia.org/x.jpg", license_name=license_name,
                license_url=license_url)
    base.update(kw)
    return MediaItem(**base)


class ClassifyTests(unittest.TestCase):
    def test_accepted_licenses(self):
        cases = {
            "CC BY 4.0": CC_BY, "CC BY 2.0": CC_BY, "cc-by-3.0": CC_BY,
            "CC BY-SA 4.0": CC_BY_SA, "CC BY-SA 3.0 DE": CC_BY_SA,
            "CC0": CC0, "Public domain": PUBLIC_DOMAIN, "PD-USGov-NASA": PUBLIC_DOMAIN,
            "Public Domain Mark 1.0": PUBLIC_DOMAIN,
        }
        for name, expected in cases.items():
            with self.subTest(name=name):
                d = classify_license("wikimedia", name)
                self.assertTrue(d.allowed, name)
                self.assertEqual(d.category, expected)

    def test_rejected_licenses(self):
        for name in ["CC BY-NC 2.0", "CC BY-NC-SA 4.0", "CC BY-ND 4.0", "GFDL", "All rights reserved",
                     "Attribution", "", "Copyrighted free use"]:
            with self.subTest(name=name):
                d = classify_license("wikimedia", name)
                self.assertFalse(d.allowed, name)
                self.assertEqual(d.category, REJECTED)

    def test_license_url_is_used(self):
        d = classify_license("wikimedia", "", "https://creativecommons.org/licenses/by-sa/4.0/")
        self.assertEqual(d.category, CC_BY_SA)
        d = classify_license("wikimedia", "", "https://creativecommons.org/publicdomain/zero/1.0/")
        self.assertEqual(d.category, CC0)

    def test_stock_sources(self):
        self.assertEqual(classify_license("pexels", "anything").category, PEXELS)
        self.assertEqual(classify_license("pixabay", "anything").category, PIXABAY)

    def test_attribution_flags(self):
        self.assertTrue(classify_license("wikimedia", "CC BY 4.0").attribution_required)
        sa = classify_license("wikimedia", "CC BY-SA 4.0")
        self.assertTrue(sa.attribution_required and sa.share_alike)
        self.assertFalse(classify_license("wikimedia", "CC0").attribution_required)

    def test_nasa_copyright_note_rejected(self):
        ok = item(source="nasa", license_name="NASA media", extra={"description": "City lights"})
        bad = item(source="nasa", license_name="NASA media", extra={"description": "Image © Partner"})
        self.assertTrue(evaluate_license(ok).allowed)
        self.assertFalse(evaluate_license(bad).allowed)


class AttributionTests(unittest.TestCase):
    def test_cc_by_sa_tasl(self):
        text = attribution_text(item(license_name="CC BY-SA 4.0",
                                     license_url="https://creativecommons.org/licenses/by-sa/4.0"))
        self.assertIn('"Diesel generator"', text)
        self.assertIn("by Jane Example", text)
        self.assertIn("https://commons.wikimedia.org/wiki/File:X.jpg", text)
        self.assertIn("licensed under CC BY-SA 4.0", text)
        self.assertIn("(modified: cropped, animated)", text)

    def test_unmodified_flag(self):
        self.assertNotIn("modified", attribution_text(item(), modified=False))

    def test_pexels_and_pixabay(self):
        self.assertTrue(attribution_text(item(source="pexels", page_url="https://pexels.com/p/1"))
                        .startswith("Photo by Jane Example on Pexels"))
        self.assertIn("from Pixabay", attribution_text(item(source="pixabay", media_type="video")))

    def test_nasa_no_endorsement(self):
        self.assertIn("does not imply NASA endorsement",
                      attribution_text(item(source="nasa", license_name="NASA media")))

    def test_rejected_raises(self):
        with self.assertRaises(ValueError):
            attribution_text(item(license_name="CC BY-NC 4.0"))

    def test_strip_html(self):
        self.assertEqual(strip_html('<a href="x">Jane&nbsp;Example</a>\n'), "Jane Example")
        self.assertEqual(strip_html(None), "")


if __name__ == "__main__":
    unittest.main()
