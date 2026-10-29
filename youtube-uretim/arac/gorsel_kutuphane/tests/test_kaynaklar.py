import unittest

from gorsel_kutuphane.config import Settings
from gorsel_kutuphane.kaynaklar import nasa, pexels, pixabay, wikimedia
from gorsel_kutuphane.licenses import evaluate_license

from .sahte import (NASA_ASSET_RESPONSE, NASA_SEARCH_RESPONSE, PEXELS_PHOTOS_RESPONSE, PEXELS_VIDEOS_RESPONSE,
                    PIXABAY_IMAGES_RESPONSE, PIXABAY_VIDEOS_RESPONSE, WIKIMEDIA_RESPONSE, FakeResponse,
                    FakeSession)

SETTINGS = Settings(pexels_api_key="PEXELS-TEST", pixabay_api_key="PIXABAY-TEST",
                    wikimedia_user_agent="test-agent (test@example.com)")


class WikimediaTests(unittest.TestCase):
    def test_parse_orders_by_index_and_cleans_html(self):
        items = wikimedia.parse_response(WIKIMEDIA_RESPONSE)
        self.assertEqual([i.source_id for i in items], ["102", "101", "103"])
        gen = items[1]
        self.assertEqual(gen.author, "Jane Example")
        self.assertEqual(gen.license_name, "CC BY-SA 4.0")
        self.assertEqual((gen.width, gen.height), (4000, 3000))

    def test_license_decisions(self):
        decisions = {i.source_id: evaluate_license(i).allowed for i in wikimedia.parse_response(WIKIMEDIA_RESPONSE)}
        self.assertEqual(decisions, {"101": True, "102": False, "103": True})

    def test_search_sends_user_agent_and_params(self):
        session = FakeSession({wikimedia.API_URL: FakeResponse(WIKIMEDIA_RESPONSE)})
        wikimedia.search("generator", SETTINGS, session, limit=5)
        call = session.calls[0]
        self.assertEqual(call["headers"]["User-Agent"], "test-agent (test@example.com)")
        self.assertIn("generator filetype:bitmap", call["params"]["gsrsearch"])
        self.assertEqual(call["params"]["gsrlimit"], 5)

    def test_video_filetype(self):
        self.assertIn("filetype:video", wikimedia.build_params("x", 3, "video")["gsrsearch"])

    def test_empty_response(self):
        self.assertEqual(wikimedia.parse_response({}), [])


class NasaTests(unittest.TestCase):
    def test_parse_and_resolve_original(self):
        session = FakeSession({
            nasa.SEARCH_URL: FakeResponse(NASA_SEARCH_RESPONSE),
            "https://images-api.nasa.gov/asset/": FakeResponse(NASA_ASSET_RESPONSE),
        })
        items = nasa.search("earth at night", SETTINGS, session)
        self.assertEqual(len(items), 2)
        self.assertTrue(items[0].download_url.endswith("~orig.jpg"))
        self.assertEqual(items[0].page_url, "https://images.nasa.gov/details/iss071e000001")
        self.assertTrue(evaluate_license(items[0]).allowed)
        self.assertFalse(evaluate_license(items[1]).allowed)  # © notu

    def test_pick_original_video(self):
        data = {"collection": {"items": [{"href": "a~small.mp4"}, {"href": "a~orig.mp4"}]}}
        self.assertEqual(nasa.pick_original(data, "video"), "a~orig.mp4")
        self.assertIsNone(nasa.pick_original({"collection": {"items": []}}, "video"))


class PexelsTests(unittest.TestCase):
    def test_photos(self):
        items = pexels.parse_photos(PEXELS_PHOTOS_RESPONSE)
        self.assertEqual(items[0].author, "Ana Photographer")
        self.assertTrue(items[0].download_url.endswith("a.jpeg"))

    def test_videos_pick_smallest_at_least_1920(self):
        items = pexels.parse_videos(PEXELS_VIDEOS_RESPONSE)
        self.assertEqual(items[0].download_url, "https://videos.pexels.com/777-hd.mp4")

    def test_search_uses_auth_header(self):
        session = FakeSession({pexels.PHOTO_URL: FakeResponse(PEXELS_PHOTOS_RESPONSE)})
        pexels.search("card terminal", SETTINGS, session, limit=200, orientation="portrait")
        call = session.calls[0]
        self.assertEqual(call["headers"]["Authorization"], "PEXELS-TEST")
        self.assertEqual(call["params"]["per_page"], 80)
        self.assertEqual(call["params"]["orientation"], "portrait")

    def test_missing_key(self):
        with self.assertRaises(pexels.MissingApiKey):
            pexels.search("x", Settings(), FakeSession({}))


class PixabayTests(unittest.TestCase):
    def test_images(self):
        item = pixabay.parse_images(PIXABAY_IMAGES_RESPONSE)[0]
        self.assertEqual(item.author, "coinlover")
        self.assertEqual(item.license_name, "Pixabay Content License")

    def test_videos_fallback_when_large_missing(self):
        item = pixabay.parse_videos(PIXABAY_VIDEOS_RESPONSE)[0]
        self.assertEqual(item.download_url, "https://cdn.pixabay.com/99_medium.mp4")

    def test_per_page_bounds_and_key(self):
        params = pixabay.build_params("penny", 1, "K", "image")
        self.assertEqual(params["per_page"], 3)
        self.assertEqual(params["key"], "K")
        self.assertEqual(params["image_type"], "photo")
        self.assertNotIn("image_type", pixabay.build_params("x", 500, "K", "video"))

    def test_search_video_endpoint(self):
        session = FakeSession({pixabay.VIDEO_URL: FakeResponse(PIXABAY_VIDEOS_RESPONSE),
                               pixabay.IMAGE_URL: FakeResponse(PIXABAY_IMAGES_RESPONSE)})
        items = pixabay.search("thermometer", SETTINGS, session, media_type="video")
        self.assertEqual(items[0].media_type, "video")
        self.assertTrue(session.calls[0]["url"].startswith(pixabay.VIDEO_URL))

    def test_missing_key(self):
        with self.assertRaises(pixabay.MissingApiKey):
            pixabay.search("x", Settings(), FakeSession({}))


if __name__ == "__main__":
    unittest.main()
