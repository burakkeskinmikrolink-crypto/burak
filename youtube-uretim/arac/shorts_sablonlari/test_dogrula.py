"""python -m unittest test_dogrula   (bu klasörde çalıştırın)"""

import copy
import json
import unittest
from pathlib import Path

import dogrula

HERE = Path(__file__).resolve().parent
EXAMPLES = sorted((HERE / "ornekler").glob("*.json"))


def load(name):
    return json.loads((HERE / "ornekler" / name).read_text(encoding="utf-8"))


def errors(data):
    return dogrula.schema_errors(data) or dogrula.rule_errors(data)


class ExampleTests(unittest.TestCase):
    def test_all_examples_valid(self):
        self.assertGreaterEqual(len(EXAMPLES), 3)
        for path in EXAMPLES:
            with self.subTest(path=path.name):
                self.assertEqual(dogrula.validate_file(path), [])

    def test_templates_complete(self):
        for path in (HERE / "sablonlar").glob("*.json"):
            with self.subTest(path=path.name):
                self.assertEqual(dogrula.validate_file(path, template_only=True), [])

    def test_three_formats_covered(self):
        formats = {json.loads(p.read_text(encoding="utf-8"))["format"] for p in EXAMPLES}
        self.assertEqual(formats, {"quiz", "kisa_hikaye", "gercek_mi_sahte_mi"})


class RuleTests(unittest.TestCase):
    def setUp(self):
        self.quiz = load("quiz-cw03-yuvarlama.json")

    def test_seven_words_rejected(self):
        d = copy.deepcopy(self.quiz)
        d["ilk_kare"]["ekran_yazisi"] = d["sahneler"][0]["ekran_yazisi"] = "ONE TWO THREE FOUR FIVE SIX SEVEN"
        d["vo"]["ilk_cumle"] = "One two three four five six seven"
        self.assertTrue(any("6 kelime" in e for e in errors(d)))

    def test_screen_must_match_first_line(self):
        d = copy.deepcopy(self.quiz)
        d["vo"]["ilk_cumle"] = "Here's a quick money quiz."
        self.assertTrue(any("ilk cümlesiyle aynı değil" in e for e in errors(d)))

    def test_loop_bridge_required(self):
        d = copy.deepcopy(self.quiz)
        d["vo"]["kapanis_kopru"] = "Thanks for watching."
        self.assertTrue(any("döngü" in e for e in errors(d)))

    def test_cta_and_first_person_banned(self):
        d = copy.deepcopy(self.quiz)
        d["vo"]["govde"].append("I'm a telecom engineer. Full story on the channel.")
        errs = errors(d)
        self.assertTrue(any("yasak çağrı" in e for e in errs))
        self.assertTrue(any("birinci tekil" in e for e in errs))

    def test_scene_gap_detected(self):
        d = copy.deepcopy(self.quiz)
        d["sahneler"][2]["bas_sn"] = 10
        self.assertTrue(any("boşluğu" in e for e in errors(d)))

    def test_story_needs_composite_note(self):
        d = load("kisa-hikaye-se03-kod.json")
        del d["ilk_kare"]["not"]
        self.assertTrue(errors(d))

    def test_real_or_fake_labels(self):
        d = load("gercek-mi-sahte-mi-se06-magaza.json")
        d["gercek_mi_sahte_mi"]["ogeler"][0]["cevap"] = "MAYBE"
        self.assertTrue(any("etiketlerde yok" in e for e in errors(d)))

    def test_format_block_mismatch(self):
        d = copy.deepcopy(self.quiz)
        d["kisa_hikaye"] = {"karakter": {"ad": "X", "temsili": True}, "sonuc": "", "donum_noktasi": "", "ders": ""}
        self.assertTrue(dogrula.schema_errors(d))


if __name__ == "__main__":
    unittest.main()
