import shutil
import tempfile
import unittest
from pathlib import Path

from gorsel_kutuphane.config import load_settings, parse_env_file
from gorsel_kutuphane.indirme import LicenseRejected, download, safe_filename
from gorsel_kutuphane.kaynaklar import wikimedia
from gorsel_kutuphane.models import MediaItem
from gorsel_kutuphane.proje import Project, build_credits_text

from .sahte import WIKIMEDIA_RESPONSE, FakeResponse, FakeSession


def pexels_item():
    return MediaItem(source="pexels", source_id="5551234", media_type="image", title="Card payment terminal",
                     author="Ana Photographer", page_url="https://www.pexels.com/photo/5551234/",
                     download_url="https://images.pexels.com/photos/5551234/a.jpeg",
                     license_name="Pexels License")


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_download_writes_file_and_manifest(self):
        project = Project.open(self.tmp, "hs-04")
        item = pexels_item()
        session = FakeSession({item.download_url: FakeResponse(content=b"\xff\xd8fakejpeg")})
        path = download(item, project.media_dir, session)
        self.assertEqual(path.read_bytes(), b"\xff\xd8fakejpeg")
        project.add(item, path)
        record = project.load()[item.key]
        self.assertEqual(record["local_file"], str(Path("medya") / path.name))
        self.assertTrue(record["license_decision"]["allowed"])
        self.assertEqual(project.items()[0].key, item.key)

    def test_download_refuses_rejected_license(self):
        nc = [i for i in wikimedia.parse_response(WIKIMEDIA_RESPONSE) if i.source_id == "102"][0]
        with self.assertRaises(LicenseRejected):
            download(nc, self.tmp, FakeSession({}))

    def test_credits_file_sections(self):
        items = wikimedia.parse_response(WIKIMEDIA_RESPONSE) + [pexels_item()]
        text = build_credits_text(items)
        self.assertTrue(text.startswith("VISUAL CREDITS"))
        self.assertIn("attribution required", text)
        self.assertIn('"Diesel generator" by Jane Example', text)
        self.assertIn("Photo by Ana Photographer on Pexels", text)
        self.assertIn("(public domain)", text)
        self.assertNotIn("John Doe", text)          # NC lisanslı öğe listeye girmez
        self.assertIn("CC BY-SA", text.split("Note:")[1])

    def test_write_credits_empty_project(self):
        project = Project.open(self.tmp, "bos")
        self.assertIn("no media recorded", project.write_credits().read_text(encoding="utf-8"))

    def test_last_search_roundtrip(self):
        project = Project.open(self.tmp, "p")
        items = wikimedia.parse_response(WIKIMEDIA_RESPONSE)
        project.save_last_search(items)
        self.assertEqual([i.key for i in project.load_last_search()], [i.key for i in items])

    def test_safe_filename_windows_friendly(self):
        item = pexels_item()
        item.title = 'Bad:/\\*?"<>| name'
        name = safe_filename(item)
        self.assertRegex(name, r"^[A-Za-z0-9_\-.]+$")
        self.assertTrue(name.endswith(".jpeg"))


class ConfigTests(unittest.TestCase):
    def test_env_parsing_and_precedence(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            env = tmp / ".env"
            env.write_text('# yorum\nPEXELS_API_KEY="abc"\nexport PIXABAY_API_KEY=def\nBOS=\n', encoding="utf-8")
            self.assertEqual(parse_env_file(env)["PEXELS_API_KEY"], "abc")
            s = load_settings(env)
            self.assertEqual((s.pexels_api_key, s.pixabay_api_key), ("abc", "def"))
            self.assertIn("gorsel-kutuphane", s.wikimedia_user_agent)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
