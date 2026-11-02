import contextlib
import io
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from gorsel_kutuphane import cli
from gorsel_kutuphane.kaynaklar import wikimedia

from .sahte import WIKIMEDIA_RESPONSE, FakeResponse, FakeSession


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.base = ["--projeler", str(self.tmp), "--env", str(self.tmp / ".env")]

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_cli(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            code = cli.main([*self.base, *args])
        return code, out.getvalue()

    def test_search_then_download_then_credits(self):
        items = wikimedia.parse_response(WIKIMEDIA_RESPONSE)
        routes = {wikimedia.API_URL: FakeResponse(WIKIMEDIA_RESPONSE)}
        for i in items:
            routes[i.download_url] = FakeResponse(content=b"img")
        session = FakeSession(routes)
        with mock.patch.object(cli, "_session", return_value=session):
            code, out = self.run_cli("ara", "generator", "--proje", "p1", "--kaynak", "wikimedia")
            self.assertEqual(code, 0)
            self.assertIn("HAYIR", out)  # NC lisanslı sonuç uygun değil olarak gösterilir
            # 1 = NC (reddedilmeli), 2 = CC BY-SA, 3 = public domain
            code, _ = self.run_cli("indir", "--proje", "p1", "--secim", "1,2,3")
        self.assertEqual(code, 1)  # reddedilen seçim olduğu için hata kodu
        media = sorted(p.name for p in (self.tmp / "p1" / "medya").iterdir())
        self.assertEqual(len(media), 2)
        credits = (self.tmp / "p1" / "kaynaklar.txt").read_text(encoding="utf-8")
        self.assertIn("Jane Example", credits)
        self.assertNotIn("John Doe", credits)

    def test_download_without_search(self):
        code, _ = self.run_cli("indir", "--proje", "bos", "--secim", "1")
        self.assertEqual(code, 1)

    @unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg yok")
    def test_klip_command(self):
        proj = self.tmp / "p2" / "medya"
        proj.mkdir(parents=True)
        img = proj / "card.png"
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "testsrc=size=800x600:rate=1", "-frames:v", "1",
                        str(img)], check=True, capture_output=True)
        code, out = self.run_cli("klip", "--proje", "p2", "--dosya", "medya/card.png", "--format", "yatay",
                                 "--sure", "0.4", "--hareket", "pan_left")
        self.assertEqual(code, 0)
        self.assertIn("pan_left_1920x1080.mp4", out)


if __name__ == "__main__":
    unittest.main()
