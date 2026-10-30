"""Yükleme paketleri: her yayın (uzun video veya Short) için youtube-uretim/yukleme/ altında bir klasör.

Kullanım (youtube-uretim/ klasöründen):
    python arac/yukleme_paketi/paketle.py                 # 13 Aralık 2026'ya kadar
    python arac/yukleme_paketi/paketle.py --son 2026-12-31

Her klasörde:
    baslik.txt, baslik_alternatifleri.txt, aciklama.txt, etiketler.txt, sabit_yorum.txt,
    yayin_zamani.txt, kucuk_resim.txt, seslendirme.txt, seslendirme_ayar.txt,
    ilgili_video.txt (yalnızca Short'larda)
Kaynak: -v2 senaryolar, Short dosyaları, topluluk-ve-yorum.md, arac/kucuk_resim/cikti/.
Klasör her çalıştırmada baştan üretilir; elle düzeltmeleri kaynak .md dosyalarına yap.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional

KOK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(KOK, "arac", "seslendirme"))
from seslendir import senaryo_bloklari, telaffuz_uygula  # noqa: E402

try:
    from zoneinfo import ZoneInfo
    TZ_IST, TZ_LON, TZ_NY = ZoneInfo("Europe/Istanbul"), ZoneInfo("Europe/London"), ZoneInfo("America/New_York")
except Exception:  # pragma: no cover
    TZ_IST = TZ_LON = TZ_NY = None

SENTETIK = "Narration uses a synthetic voice."
YIL = 2026
AY = {"Kas": 11, "Kasım": 11, "Ara": 12, "Aralık": 12}

KANAL = {
    "hidden_systems": {"slug": "hidden-systems", "ad": "Hidden Systems", "dil": "b", "hiz": 0.97, "ses": "<seçilecek bm_… sesi>",
                       "kimlik": "This channel is made by someone who works inside a mobile network operations center.",
                       "short_saat": ["21:30", "22:30"],
                       "etiket": ["hidden systems", "engineering explained", "infrastructure"],
                       "short_yorum": "Sources are in the related video linked above. Which hidden system should we explain next?"},
    "centworks": {"slug": "centworks", "ad": "Centworks", "dil": "a", "hiz": 1.0, "ses": "<seçilecek am_/af_ sesi>",
                  "kimlik": "This channel is made by an engineer, not a banker. Educational content, not financial advice.",
                  "short_saat": ["20:00", "23:00"],
                  "etiket": ["centworks", "how money works", "personal finance"],
                  "short_yorum": "Educational, not financial advice. The full breakdown with sources is in the related video above. What money question should we answer next?"},
    "scam_engineer": {"slug": "scam-engineer", "ad": "Scam Engineer", "dil": "a", "hiz": 0.93, "ses": "<seçilecek am_/af_ sesi>",
                      "kimlik": "This channel is made by a telecom engineer.",
                      "short_saat": ["20:00", "23:00"],
                      "etiket": ["scam engineer", "scam awareness", "fraud prevention"],
                      "short_yorum": "Calm reminder: please never post phone numbers, codes or links in the comments. The full breakdown with sources is in the related video above. Which message or call should we look at next?"},
}
UZUN_SAAT = "21:00"

# Uzun videolar ve Short günleri (README takvimi; Short numarası → tarih)
TAKVIM = [
    ("HS-04", "hidden_systems", "hidden_systems/04-v2.md", "2026-11-11", "hidden_systems/shorts_04-v2.md", {1: "2026-11-12", 2: "2026-11-14", 3: "2026-11-16"}),
    ("HS-05", "hidden_systems", "hidden_systems/05-v3-uzun.md", "2026-11-18", "hidden_systems/shorts_05-v2.md", {1: "2026-11-19", 2: "2026-11-21", 3: "2026-11-23"}),
    ("HS-06", "hidden_systems", "hidden_systems/06-v2.md", "2026-11-25", "hidden_systems/shorts_06-v2.md", {1: "2026-11-26", 2: "2026-11-28", 3: "2026-11-30"}),
    ("HS-07", "hidden_systems", "hidden_systems/07-v2.md", "2026-12-02", "hidden_systems/shorts_07-v2.md", {1: "2026-12-03", 2: "2026-12-05", 3: "2026-12-07"}),
    ("HS-08", "hidden_systems", "hidden_systems/08-v2.md", "2026-12-09", "hidden_systems/shorts_08-v2.md", {1: "2026-12-10", 2: "2026-12-12", 3: "2026-12-14"}),
    ("CW-03", "centworks", "centworks/03-v2.md", "2026-11-07", "centworks/shorts_03-v2.md", {1: "2026-11-08", 2: "2026-11-10", 3: "2026-11-12"}),
    ("CW-04", "centworks", "centworks/04-v2.md", "2026-11-14", "centworks/shorts_04-v2.md", {1: "2026-11-15", 2: "2026-11-17", 3: "2026-11-19"}),
    ("CW-05", "centworks", "centworks/05-v2.md", "2026-11-21", "centworks/shorts_05-v2.md", {1: "2026-11-22", 2: "2026-11-24", 3: "2026-11-26"}),
    ("CW-06", "centworks", "centworks/06-v2.md", "2026-11-28", "centworks/shorts_06-v2.md", {1: "2026-11-29", 3: "2026-11-30", 2: "2026-12-02"}),
    ("CW-07", "centworks", "centworks/07-v2.md", "2026-12-05", "centworks/shorts_07-v2.md", {1: "2026-12-06", 2: "2026-12-08", 3: "2026-12-10"}),
    ("CW-08", "centworks", "centworks/08-v2.md", "2026-12-12", "centworks/shorts_08-v2.md", {1: "2026-12-13", 2: "2026-12-15", 3: "2026-12-17"}),
    ("SE-03", "scam_engineer", "scam_engineer/03-v2.md", "2026-11-11", None, {1: "2026-11-12", 2: "2026-11-14", 3: "2026-11-16"}),
    ("SE-04", "scam_engineer", "scam_engineer/04-v2.md", "2026-11-18", None, {1: "2026-11-19", 2: "2026-11-21", 3: "2026-11-23"}),
    ("SE-05", "scam_engineer", "scam_engineer/05-v2.md", "2026-11-25", None, {1: "2026-11-26", 2: "2026-11-28", 3: "2026-11-30"}),
    ("SE-06", "scam_engineer", "scam_engineer/06-v2.md", "2026-12-02", None, {1: "2026-12-03", 2: "2026-12-05", 3: "2026-12-07"}),
    ("SE-07", "scam_engineer", "scam_engineer/07-v2.md", "2026-12-09", None, {1: "2026-12-10", 2: "2026-12-12", 3: "2026-12-14"}),
]
SERI_5_10 = ("scam_engineer", "scam_engineer/shorts_5-10_kasim-v2.md")
BAGIMSIZ = [(k, f"{k}/shorts-bagimsiz-hafta-{n}.md") for k in KANAL for n in range(1, 6)]

SLOW_RE = re.compile(r"(\b7726\b|1-8\d\d|1-833|\b105\b|ReportFraud|IdentityTheft|reportfraud|identitytheft"
                     r"|[Hh]ang up|call the number on|number on the back of your card)")


@dataclass
class Paket:
    tarih: str
    saat: str
    kanal: str
    tur: str                      # "uzun" | "short"
    baslik: str
    alternatifler: List[str]
    aciklama: str
    etiketler: List[str]
    sabit_yorum: str
    seslendirme: str
    kucuk_resim: List[str]
    kimlik: str = ""
    ilgili_video: Optional[str] = None
    uyarilar: List[str] = field(default_factory=list)


# ---------------------------------------------------------------- yardımcılar
def oku(yol: str) -> str:
    return open(os.path.join(KOK, yol), encoding="utf-8").read()


def slug(metin: str, n: int = 48) -> str:
    tr = str.maketrans("çğıöşüÇĞİÖŞÜ’'", "cgiosuCGIOSU  ")
    s = re.sub(r"[^a-z0-9]+", "-", metin.translate(tr).lower()).strip("-")
    return s[:n].rstrip("-") or "video"


def bolum_sonra(md: str, baslik: str) -> str:
    m = re.search(r"^" + re.escape(baslik) + r"\s*$(.*?)(?=^## |\Z)", md, re.S | re.M)
    return m.group(1) if m else ""


def telaffuz() -> Dict[str, str]:
    p = os.path.join(KOK, "arac", "seslendirme", "telaffuz.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def cumleler(p: str) -> List[str]:
    return [c.strip() for c in re.split(r"(?<=[.?!…])\s+", p) if c.strip()]


def ses_cumle(c: str, sozluk: dict) -> str:
    yavas = bool(SLOW_RE.search(c))
    c = telaffuz_uygula(c, sozluk)
    if yavas:
        c = f"[slow]{c}[/slow]"
    if c.rstrip("]").rstrip("/slow[").endswith("?") or c.endswith("?"):
        c += " [pause 1000]"
    return c


def uzun_seslendirme(md: str) -> str:
    """Sahne/görsel notları olmadan, işaretli anlatım metni."""
    sozluk, sahneler = telaffuz(), senaryo_bloklari(md)
    out = []
    for sahne in sahneler:
        paragraflar = [" ".join(ses_cumle(c, sozluk) for c in cumleler(p)) for p in sahne]
        if not paragraflar[-1].endswith("[pause 1000]"):      # soru ile bitiyorsa 1000 ms kalır
            paragraflar[-1] += " [pause 900]"
        out.extend(paragraflar)
    return "\n\n".join(out) + "\n"


def short_seslendirme(vo: List[str]) -> str:
    sozluk = telaffuz()
    satirlar = []
    for i, s in enumerate(vo):
        parca = []
        for c in cumleler(s):                       # [slow] yalnızca ilgili cümleye
            tc = telaffuz_uygula(c, sozluk)
            parca.append(f"[slow]{tc}[/slow]" if SLOW_RE.search(c) else tc)
        t = " ".join(parca)
        if i == 0:
            t += " [pause 400]"
        satirlar.append(t)
    return "\n".join(satirlar) + "\n"


def zaman_metni(tarih: str, saat: str, tur: str) -> str:
    h, m = map(int, saat.split(":"))
    y, a, g = map(int, tarih.split("-"))
    if TZ_IST:
        t = dt.datetime(y, a, g, h, m, tzinfo=TZ_IST)
        lon, ny = t.astimezone(TZ_LON).strftime("%H:%M"), t.astimezone(TZ_NY).strftime("%H:%M")
    else:
        lon, ny = f"{(h - 3) % 24:02d}:{m:02d}", f"{(h - 8) % 24:02d}:{m:02d}"
    gun = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"][dt.date(y, a, g).weekday()]
    not_ = ("Premiere olarak planla (gerekçe: gelir/4000-saat-plani.md §2.4)." if tur == "uzun"
            else "Short: Studio'da zamanla (Görünürlük → Planla).")
    return (f"{tarih} {gun} {saat} (İstanbul, UTC+3)\n"
            f"= {lon} Londra / {ny} New York\n{not_}\n")


def sabit_yorum_bul(vid: str) -> Optional[str]:
    for satir in oku("topluluk-ve-yorum.md").splitlines():
        if satir.startswith(f"| {vid} "):
            hucre = [h.strip() for h in satir.strip().strip("|").split("|")]
            return hucre[-1].replace("*", "")
    return None


# ---------------------------------------------------------------- uzun video
def uzun_paket(vid, kanal, dosya, tarih) -> Paket:
    md = oku(dosya)
    bas = [re.sub(r"^\d+\.\s*", "", l).strip() for l in bolum_sonra(md, "## Başlık seçenekleri").splitlines()
           if re.match(r"^\d+\.", l)]
    bas = [b.replace("**(Arama odaklı)** ", "").replace("**(Arama odaklı)**", "").strip() for b in bas]
    alt = []
    for i, b in enumerate(bas[1:], 2):
        alt.append(b + ("   ← arama odaklı" if i == 3 else ""))
    blok = re.search(r"## YouTube açıklaması\s*\n```\n(.*?)\n```", md, re.S).group(1).rstrip()
    aciklama = blok + "\n\n" + SENTETIK + "\n"
    etiket = [e.strip() for e in bolum_sonra(md, "## Etiketler").strip().splitlines()[0].split(",") if e.strip()]
    yorum = sabit_yorum_bul(vid) or "<DOLDUR: topluluk-ve-yorum.md'de bu video için sabit yorum yok>"
    kr = [f"arac/kucuk_resim/cikti/{vid}_A.png", f"arac/kucuk_resim/cikti/{vid}_B.png"]
    p = Paket(tarih, UZUN_SAAT, kanal, "uzun", bas[0], alt, aciklama, etiket, yorum, uzun_seslendirme(md), kr, vid)
    return p


# ---------------------------------------------------------------- Short'lar
BOLUM_RE = re.compile(r"^#{2,3} (Short \d+\b.*|\d+ Kasım:.*)$", re.M)


def short_bolumleri(md: str) -> List[tuple]:
    idx = [(m.start(), m.group(1)) for m in BOLUM_RE.finditer(md)]
    out = []
    for i, (bas, baslik) in enumerate(idx):
        son = idx[i + 1][0] if i + 1 < len(idx) else len(md)
        ilk_satir, _, govde = md[bas:son].partition("\n")
        govde = re.split(r"^## ", govde, flags=re.M)[0]   # bir sonraki ana bölümde dur
        out.append((baslik, govde))
    return out


def short_alanlari(govde: str) -> dict:
    ekran = None
    for l in govde.splitlines():
        if l.startswith("| 0–2 sn"):
            ekran = l.strip().rstrip("|").split("|")[-1].strip()
            break
    vo = [l[2:].strip() for l in govde.splitlines() if l.startswith("> ")]

    def alan(ad):
        m = re.search(r"\*\*" + ad + r":\*\*\s*(.+)", govde)
        return m.group(1).strip() if m else None
    rel = alan("Açıklama notu")
    if rel:
        rel = re.sub(r"^Related video bağlantısı:\s*", "", rel).split(". \"Educational")[0].replace("*", "").strip()
    return {"ekran": ekran, "vo": vo, "kaynak": alan("Kaynak"), "ilgili": rel,
            "hashtag": (alan("Hashtag") or "").split()}


VARSAYILAN_HASHTAG = {"scam_engineer": ["#scamawareness", "#scams", "#fraudprevention", "#scamengineer"]}


def short_paket(kanal, alan, tarih, kaynak_ek=None, ana_baslik=None) -> Paket:
    k = KANAL[kanal]
    vo, hashtag = alan["vo"], alan["hashtag"] or VARSAYILAN_HASHTAG.get(kanal, [])
    ilk = vo[0]
    etiket_kelime = hashtag[0] if hashtag else ""
    baslik = f"{ilk} {etiket_kelime}".strip()[:100]
    alt = [f"{ilk} {hashtag[1] if len(hashtag) > 1 else ''}".strip(),
           f"{ilk} | {k['ad']}"]
    if alan["kaynak"]:
        kaynak = f"Source: {alan['kaynak']}"
    elif kaynak_ek:
        kaynak = "Sources:\n" + kaynak_ek
    else:
        kaynak = "Sources are listed in the related video's description."
    govde = " ".join(vo[1:3])
    aciklama = (f"{ilk}\n{govde}\n\n{kaynak}\n\n{k['kimlik']}\n\n{' '.join(hashtag)}\n\n{SENTETIK}\n")
    etiket = [h.lstrip("#") for h in hashtag] + k["etiket"]
    ilgili = alan["ilgili"] or (ana_baslik or "<DOLDUR: ilgili uzun video>")
    p = Paket(tarih, "", kanal, "short", baslik, alt, aciklama, list(dict.fromkeys(etiket)), k["short_yorum"],
              short_seslendirme(vo), [], ilgili_video=ilgili)
    if not alan["kaynak"] and kanal == "centworks":
        p.aciklama = p.aciklama.replace(f"\n\n{SENTETIK}", f"\n\nEducational, not financial advice.\n\n{SENTETIK}")
    return p


def tarih_coz(metin: str) -> Optional[str]:
    m = re.search(r"\b(\d{1,2}) (Kas|Kasım|Ara|Aralık)\b", metin)
    return f"{YIL}-{AY[m.group(2)]:02d}-{int(m.group(1)):02d}" if m else None


# ---------------------------------------------------------------- toplama
def tum_paketler(son: str) -> List[Paket]:
    paketler: List[Paket] = []
    for vid, kanal, dosya, tarih, sdosya, sgun in TAKVIM:
        if tarih <= son:
            paketler.append(uzun_paket(vid, kanal, dosya, tarih))
        md = oku(sdosya) if sdosya else bolum_sonra(oku(dosya), "## Shorts (v2: üç farklı format)") or \
            oku(dosya).split("## Shorts", 1)[1]
        for baslik, govde in short_bolumleri(md):
            no = int(re.match(r"Short (\d+)", baslik).group(1))
            if no in sgun and sgun[no] <= son:
                p = short_paket(kanal, short_alanlari(govde), sgun[no])
                p.kimlik = f"{vid}-S{no}"
                paketler.append(p)
    # 5–10 Kasım serisi
    kanal, dosya = SERI_5_10
    md = oku(dosya)
    ek = "\n".join(l for l in bolum_sonra(md, "## Kaynaklar (açıklamaya eklenecek)").splitlines() if l.startswith("- "))
    for baslik, govde in short_bolumleri(md):
        t = tarih_coz(baslik)
        if t and t <= son:
            p = short_paket(kanal, short_alanlari(govde), t, kaynak_ek=ek)
            p.kimlik = f"SE-seri-{t[-2:]}"
            paketler.append(p)
    # bağımsız Shorts
    for kanal, dosya in BAGIMSIZ:
        md = oku(dosya)
        for baslik, govde in short_bolumleri(md):
            t = tarih_coz(baslik)
            if t and t <= son:
                p = short_paket(kanal, short_alanlari(govde), t)
                p.kimlik = f"{KANAL[kanal]['slug']}-bagimsiz-{re.match(r'Short (\d+)', baslik).group(1)}"
                paketler.append(p)
    # Short saatleri: aynı kanal aynı gün ikinci Short → sonraki saat
    sayac: Dict[tuple, int] = {}
    for p in sorted(paketler, key=lambda x: (x.tarih, x.tur != "short", x.kimlik)):
        if p.tur == "short":
            key = (p.tarih, p.kanal)
            i = sayac.get(key, 0)
            p.saat = KANAL[p.kanal]["short_saat"][min(i, 1)]
            sayac[key] = i + 1
    return sorted(paketler, key=lambda x: (x.tarih, x.saat, x.kanal))


AYAR_YOLU = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ayarlar.json")
YER_TUTUCU = [  # (yer tutucuda geçen ifade, ayarlar.json anahtarı)
    ("Spain blackout", "Spain blackout"), ("CrowdStrike", "CrowdStrike"), ("deprem", "deprem"),
    ("geç ödemeni", "geç ödeme"), ("yoktan", "para yaratma"), ("spoofing", "caller ID spoofing"),
    ("SIM swap", "SIM swap"),
]


def ayarlar() -> dict:
    return json.load(open(AYAR_YOLU, encoding="utf-8")) if os.path.exists(AYAR_YOLU) else {}


def yer_tutucu_doldur(metin: str, ayar: dict) -> str:
    basliklar = ayar.get("yayinlanmis_basliklar", {})

    def degistir(m):
        ic = m.group(0)
        for ifade, anahtar in YER_TUTUCU:
            if ifade in ic and basliklar.get(anahtar):
                return basliklar[anahtar]
        if "SE-07 linki" in ic and ayar.get("linkler", {}).get("SE-07"):
            return ayar["linkler"]["SE-07"]
        return ic
    return re.sub(r"<[^<>]{3,90}>", degistir, metin)


def yaz(paketler: List[Paket], hedef: str) -> List[tuple]:
    ayar = ayarlar()
    for p in paketler:
        p.aciklama = yer_tutucu_doldur(p.aciklama, ayar)
        p.sabit_yorum = yer_tutucu_doldur(p.sabit_yorum, ayar)
        if p.ilgili_video:
            p.ilgili_video = yer_tutucu_doldur(p.ilgili_video, ayar)
    if os.path.isdir(hedef):
        shutil.rmtree(hedef)
    os.makedirs(hedef)
    satirlar = []
    for p in paketler:
        k = KANAL[p.kanal]
        on_ek = "" if p.tur == "uzun" else "short-"
        klasor = f"{p.tarih}_{k['slug']}_{on_ek}{slug(p.baslik.split(' #')[0])}"
        yol = os.path.join(hedef, klasor)
        os.makedirs(yol)

        def w(ad, metin):
            open(os.path.join(yol, ad), "w", encoding="utf-8").write(metin if metin.endswith("\n") else metin + "\n")
        w("baslik.txt", p.baslik)
        w("baslik_alternatifleri.txt", "\n".join(p.alternatifler))
        w("aciklama.txt", p.aciklama)
        w("etiketler.txt", ", ".join(p.etiketler))
        w("sabit_yorum.txt", p.sabit_yorum)
        w("yayin_zamani.txt", zaman_metni(p.tarih, p.saat, p.tur))
        if p.tur == "uzun":
            w("kucuk_resim.txt", "A (yükle):  youtube-uretim/" + p.kucuk_resim[0] +
              "\nB (Test & Compare): youtube-uretim/" + p.kucuk_resim[1] + "\n")
        else:
            w("kucuk_resim.txt", "Short: ayrı küçük resim yok. Studio'da kapak karesi olarak ilk hareketli kareyi seç.\n")
            w("ilgili_video.txt", f"{p.ilgili_video}\n(Studio → Short'u düzenle → İlgili video)\n")
        w("seslendirme.txt", p.seslendirme)
        ses = ayar.get("sesler", {}).get(p.kanal) or k["ses"]
        w("seslendirme_ayar.txt",
          f"dil: {k['dil']}\nses: {ses}\nhız: {k['hiz']}\n\n"
          f"Komut (youtube-uretim/ klasöründen):\n"
          f"python arac/seslendirme/seslendir.py yukleme/{klasor}/seslendirme.txt "
          f"-o yukleme/{klasor}/ses.wav --dil {k['dil']} --ses {ses if not ses.startswith('<') else '<ses>'} --hiz {k['hiz']}\n")
        tum = p.baslik + p.aciklama + p.sabit_yorum + (p.ilgili_video or "")
        if re.search(r"<[^<>]{3,90}>", tum):
            p.uyarilar.append("`<…>` doldur: `arac/yukleme_paketi/ayarlar.json`")
        if len(p.baslik) > 100:
            p.uyarilar.append("başlık 100 karakteri aşıyor")
        if len(", ".join(p.etiketler)) > 500:
            p.uyarilar.append("etiketler 500 karakteri aşıyor")
        satirlar.append((p, klasor))
    return satirlar


def indeks(satirlar: List[tuple], hedef: str, son: str) -> None:
    gun = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Pzr"]
    out = [f"# Yükleme paketleri ({satirlar[0][0].tarih} – {son})", "",
           "**Yükleme sırasında bu klasörü kullan.** Her alt klasör tek bir yayındır; dosyaları Studio'daki alanlara kopyala.",
           "Bu klasör `python arac/yukleme_paketi/paketle.py` ile **otomatik üretilir**. Elle düzeltme yapma; düzeltmeyi kaynak "
           "`.md` dosyasına yapıp betiği yeniden çalıştır.", "",
           "| Dosya | Studio alanı |", "|---|---|",
           "| `baslik.txt` | Başlık |", "| `baslik_alternatifleri.txt` | Test & Compare için (uzun video) |",
           "| `aciklama.txt` | Açıklama (bölümler, kaynaklar, en sonda \"Narration uses a synthetic voice.\") |",
           "| `etiketler.txt` | Etiketler (virgülle) |", "| `sabit_yorum.txt` | Yayından sonra ilk yorum → Sabitle |",
           "| `ilgili_video.txt` | Short → İlgili video |", "| `yayin_zamani.txt` | Görünürlük → Planla / Premiere |",
           "| `kucuk_resim.txt` | Küçük resim dosya yolu |",
           "| `seslendirme.txt` + `seslendirme_ayar.txt` | Kokoro seslendirmesi (`arac/seslendirme/seslendir.py`) |", "",
           "**⚠️ işaretli satırlar:** Yayınlanmış videoların gerçek başlıkları (ve SE-07 linki) depoda yok. "
           "Bunları bir kez `arac/yukleme_paketi/ayarlar.json` dosyasına yaz ve betiği tekrar çalıştır; tüm paketler dolar. "
           "Seçtiğin Kokoro seslerini de aynı dosyaya yaz.", "",
           f"**Toplam:** {sum(1 for p, _ in satirlar if p.tur == 'uzun')} uzun video, "
           f"{sum(1 for p, _ in satirlar if p.tur == 'short')} Short.", "",
           "| Tarih | Saat (İst.) | Kanal | Tür | Başlık | Klasör | Not |", "|---|---|---|---|---|---|---|"]
    for p, k in satirlar:
        d = dt.date.fromisoformat(p.tarih)
        out.append(f"| {p.tarih} {gun[d.weekday()]} | {p.saat} | {KANAL[p.kanal]['ad']} | "
                   f"{'**Uzun**' if p.tur == 'uzun' else 'Short'} | {p.baslik.replace('|', '/')} | `{k}/` | "
                   f"{'⚠️ ' + '; '.join(p.uyarilar) if p.uyarilar else ''} |")
    open(os.path.join(hedef, "README.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--son", default="2026-12-13", help="bu tarihe kadar (dahil) olan yayınlar")
    ap.add_argument("--hedef", default=os.path.join(KOK, "yukleme"))
    a = ap.parse_args()
    paketler = tum_paketler(a.son)
    satirlar = yaz(paketler, a.hedef)
    indeks(satirlar, a.hedef, a.son)
    u = sum(1 for p, _ in satirlar if p.tur == "uzun")
    print(f"{len(satirlar)} paket yazıldı ({u} uzun, {len(satirlar) - u} Short) → {a.hedef}")


if __name__ == "__main__":
    main()
