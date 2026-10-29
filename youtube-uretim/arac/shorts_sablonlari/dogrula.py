"""Short JSON dosyalarını doğrular.

1) JSON şeması (short.schema.json). jsonschema kuruluysa onunla, değilse temel kontrollerle.
2) Kanal kuralları (şemada ifade edilemeyenler):
   - İlk kare ekran yazısı en fazla 6 kelime ve VO'nun ilk cümlesiyle birebir aynı (noktalama ve büyük/küçük harf hariç)
   - İlk sahne 0. saniyede başlar, en geç 2. saniyede biter, rolü "hook"
   - Sahneler boşluksuz ve çakışmasız; son sahne sure_sn'de biter
   - VO toplamı 60–115 kelime (30–45 sn, dakikada ~140–150 kelime)
   - Kapanış köprüsü '…', ':' veya '—' ile biter (döngü)
   - VO'da "full story", "on the channel", "link in bio" gibi çağrılar yok
   - Birinci tekil şahısla kimlik iddiası yok ("I'm a telecom engineer", "as an engineer, I")
   - Format kuralları: quiz → 3 seçenek ve doğru cevap; gerçek mi sahte mi → 3 öğe ve cevaplar etiketlerden;
     kısa hikâye → temsilî karakter ve ilk karede "Composite character" notu

Kullanım:
    python dogrula.py ornekler/*.json
    python dogrula.py --sablon sablonlar/quiz.json   (şablonlar yalnızca biçim olarak kontrol edilir)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List

HERE = Path(__file__).resolve().parent
SCHEMA_PATH = HERE / "short.schema.json"

BANNED_CTA = [r"full story", r"on the channel", r"link in (the )?bio", r"full breakdown"]
FIRST_PERSON_ID = [r"\bI'?m an? (telecom|network|engineer)", r"\bas an engineer,? I\b", r"\bin my (world|control room|operations)"]


def words(text: str) -> List[str]:
    clean = text.lower().replace("…", " ").replace("’", "'")
    clean = re.sub(r"[^\w$%'.,]+", " ", clean)
    return [w.strip(".,'") for w in clean.split() if w.strip(".,'")]


def schema_errors(data: dict) -> List[str]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    try:
        import jsonschema
    except ImportError:
        missing = [k for k in schema["required"] if k not in data]
        return [f"şema: eksik alan '{k}'" for k in missing]
    validator = jsonschema.Draft202012Validator(schema)
    return [f"şema: {'/'.join(map(str, e.path)) or '(kök)'}: {e.message}" for e in validator.iter_errors(data)]


def rule_errors(d: dict) -> List[str]:
    errs: List[str] = []
    screen = d["ilk_kare"]["ekran_yazisi"]
    first = d["vo"]["ilk_cumle"]
    if len(words(screen)) > 6:
        errs.append(f"ilk kare yazısı 6 kelimeyi aşıyor ({len(words(screen))}): '{screen}'")
    if words(screen) != words(first):
        errs.append(f"ilk kare yazısı VO'nun ilk cümlesiyle aynı değil: '{screen}' ≠ '{first}'")

    scenes = sorted(d["sahneler"], key=lambda s: s["bas_sn"])
    if scenes[0]["bas_sn"] != 0 or scenes[0]["bit_sn"] > 2 or scenes[0]["rol"] != "hook":
        errs.append("ilk sahne 0–2 sn aralığında 'hook' rolünde olmalı")
    if words(scenes[0]["ekran_yazisi"]) != words(screen):
        errs.append("ilk sahnenin ekran yazısı ilk_kare.ekran_yazisi ile aynı olmalı")
    for prev, cur in zip(scenes, scenes[1:]):
        if abs(prev["bit_sn"] - cur["bas_sn"]) > 1e-6:
            errs.append(f"sahne boşluğu/çakışması: {prev['bit_sn']} → {cur['bas_sn']}")
    for s in scenes:
        if s["bit_sn"] <= s["bas_sn"]:
            errs.append(f"sahne süresi geçersiz: {s['bas_sn']}–{s['bit_sn']}")
    if abs(scenes[-1]["bit_sn"] - d["sure_sn"]) > 1e-6:
        errs.append(f"son sahne {scenes[-1]['bit_sn']} sn'de bitiyor, sure_sn {d['sure_sn']}")

    vo_all = " ".join([first, *d["vo"]["govde"], d["vo"]["kapanis_kopru"]])
    n = len(words(vo_all))
    if not 60 <= n <= 115:
        errs.append(f"VO {n} kelime; 30–45 sn için 60–115 olmalı")
    bridge = d["vo"]["kapanis_kopru"].rstrip()
    if not bridge.endswith(("…", ":", "—", "...")):
        errs.append("kapanış köprüsü '…', ':' veya '—' ile bitmeli (döngü)")
    if words(d["dongu"]["hedef"]) != words(first):
        errs.append("dongu.hedef VO'nun ilk cümlesi olmalı")
    if words(d["dongu"]["kopru"]) and words(d["dongu"]["kopru"])[-1] not in words(bridge):
        errs.append("dongu.kopru kapanış köprüsünün son kelimelerinden olmalı")

    for pat in BANNED_CTA:
        if re.search(pat, vo_all, re.I):
            errs.append(f"yasak çağrı ifadesi VO'da: /{pat}/")
    for pat in FIRST_PERSON_ID:
        if re.search(pat, vo_all, re.I):
            errs.append(f"birinci tekil şahıs kimlik iddiası VO'da: /{pat}/")

    fmt = d["format"]
    if fmt == "quiz":
        q = d["quiz"]
        if q["dogru"] not in q["secenekler"]:
            errs.append("quiz: doğru cevap seçeneklerde yok")
        if not any(s["rol"] == "geri_sayim" for s in scenes):
            errs.append("quiz: geri sayım sahnesi yok")
    elif fmt == "gercek_mi_sahte_mi":
        g = d["gercek_mi_sahte_mi"]
        labels = {l.upper() for l in g["etiketler"]}
        for o in g["ogeler"]:
            if o["cevap"].upper() not in labels:
                errs.append(f"gerçek mi sahte mi: cevap '{o['cevap']}' etiketlerde yok {sorted(labels)}")
    elif fmt == "kisa_hikaye":
        note = d["ilk_kare"].get("not", "")
        if "composite character" not in note.lower():
            errs.append("kısa hikâye: ilk karede 'Composite character' notu olmalı")
    return errs


def validate_file(path: Path, template_only: bool = False) -> List[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if template_only:
        required = {"format", "sure_aralik_sn", "zamanlama", "ilk_kare_kurallari", "dongu_kurallari"}
        return [f"şablon: eksik alan '{k}'" for k in sorted(required - data.keys())]
    errs = schema_errors(data)
    if errs:
        return errs
    return rule_errors(data)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dosyalar", nargs="+")
    ap.add_argument("--sablon", action="store_true", help="Şablon (format tanımı) dosyalarını kontrol et")
    args = ap.parse_args(argv)
    failed = 0
    for f in args.dosyalar:
        errs = validate_file(Path(f), args.sablon)
        if errs:
            failed += 1
            print(f"✗ {f}")
            for e in errs:
                print(f"    - {e}")
        else:
            print(f"✓ {f}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
