"""ceviriler/<ID>.md dosyalarını üretir.

Kullanım (youtube-uretim/ klasöründen):
    python ceviriler/_uret.py

- Başlık, özet ve bölüm adları `_veri.py` içindeki çevirilerden gelir.
- Zaman kodları, kaynak linkleri ve yardım satırları orijinal senaryonun
  "## YouTube açıklaması" bloğundan otomatik okunur. Senaryodaki zaman kodu
  değişirse bu betiği yeniden çalıştırmak yeterli.
"""
import os
import re
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _veri import KIMLIK, ETIKET, VIDEOLAR, DIPNOT, EK, YARDIM_IFADE, YAYINLANMIS  # noqa: E402

DILLER = [("es", "Español (İspanyolca)", "Spanish"),
          ("pt", "Português – Brasil (Portekizce, Brezilya)", "Portuguese (Brazil)"),
          ("de", "Deutsch (Almanca)", "German")]

YARDIM_BASLIKLARI = ("REPORT", "WHERE TO REPORT", "FREE HELP", "GET HELP / REPORT",
                     "OFFICIAL, FREE RESOURCES", "QUICK HELP")
YARDIM_ETIKET = {"es": "AYUDA Y DENUNCIAS", "pt": "AJUDA E DENÚNCIAS", "de": "HILFE UND MELDUNG"}


def aciklama_blogu(md):
    m = re.search(r"## YouTube açıklaması\s*\n```\n(.*?)\n```", md, re.S)
    if not m:
        raise ValueError("açıklama bloğu bulunamadı")
    return m.group(1).splitlines()


def bolum(satirlar, basliklar):
    """Başlığı `basliklar` içinde olan bölümün '- ' satırlarını döndürür."""
    out, icinde = [], False
    for s in satirlar:
        if s.strip() in basliklar:
            icinde = True
            continue
        if icinde:
            if not s.strip():
                break
            out.append(s)
    return out


def yardim_cevir(satir, dil):
    for en, cev in YARDIM_IFADE.items():
        if satir.startswith("- " + en):
            return "- " + cev[dil] + satir[len("- " + en):]
    return satir


def zaman_kodlari(satirlar):
    return [m.group(1) for s in satirlar if (m := re.match(r"^(\d+:\d\d) ", s))]


def baslik_en(md):
    m = re.search(r"## Başlık seçenekleri\s*\n1\. (.+)", md)
    return m.group(1).strip() if m else "?"


def video_dosyasi(v):
    md = open(os.path.join(KOK, v["dosya"]), encoding="utf-8").read()
    satir = aciklama_blogu(md)
    zk = zaman_kodlari(satir)
    kaynak = bolum(satir, ("SOURCES",))
    yardim = bolum(satir, YARDIM_BASLIKLARI)
    for d, _, _ in DILLER:
        assert len(v[d]["bolumler"]) == len(zk), (v["id"], d, len(zk))
        assert len(v[d]["baslik"]) <= 100, (v["id"], d, "başlık 100 karakteri aşıyor")
    assert kaynak, v["id"]

    o = [f"# {v['id']} — çeviriler (ES, PT-BR, DE)", "",
         f"**Kaynak senaryo:** `{v['dosya']}`  ",
         f"**Orijinal başlık (1. seçenek):** {baslik_en(md)}", "",
         "**Studio'da nereye:** YouTube Studio → Altyazılar (Subtitles) → *Dil ekle* → dili seç → "
         "*Başlık ve açıklama* → *Ekle*. Aşağıdaki başlığı ve kod bloğunu olduğu gibi yapıştır.",
         "Kaynak linkleri ve kurum adları bilerek İngilizce bırakıldı (kaynaklar İngilizce).", "",
         "> Bu dosya `ceviriler/_uret.py` ile üretildi. Elle düzeltme yaparsan `_veri.py` içine de işle.", ""]
    for d, ad, _ in DILLER:
        t, e = v[d], ETIKET[d]
        govde = [t["ozet"], ""]
        if v["id"] in EK:
            govde += [EK[v["id"]][d], ""]
        govde += [KIMLIK[v["kanal"]][d], ""]
        if v.get("abd"):
            govde += [e["not_us"], ""]
        govde.append(e["bolum"])
        govde += [f"{z} {b}" for z, b in zip(zk, t["bolumler"])]
        govde.append("")
        if yardim:
            govde.append(YARDIM_ETIKET[d])
            govde += [yardim_cevir(s, d) for s in yardim]
            govde.append("")
        govde.append(e["kaynak"])
        govde += kaynak
        govde += ["", DIPNOT[v["kanal"]][d]]
        o += [f"## {ad}", "", "**Başlık:**", "```", t["baslik"], "```", "",
              "**Açıklama:**", "```", *govde, "```", ""]
    return "\n".join(o)


def yayinlanmis_dosyasi(v):
    o = [f"# {v['id']} — çeviriler (ES, PT-BR, DE) — yayınlanmış video", "",
         f"**Video:** {v['konu']}", "",
         "**Dikkat:** Bu videonun gerçek İngilizce başlığı ve açıklaması depoda yok.",
         "- Başlık, `kucuk-resim-ab.md`'deki arama odaklı alternatifin (yoksa konunun) çevirisidir. "
         "Studio'daki başlık farklıysa onun anlamına göre uyarla.",
         "- Özet genel tutuldu. Videoda geçmeyen bir iddia varsa sil.",
         "- Bölüm (chapter) ve kaynak listesi `yayinlanmis-video-iyilestirme.md` (S4) hazır olunca eklenecek. "
         "O zamana kadar sadece başlık ve özeti yapıştır.", ""]
    for d, ad, _ in DILLER:
        t = v[d]
        assert len(t["baslik"]) <= 100, (v["id"], d)
        govde = [t["ozet"], "", KIMLIK[v["kanal"]][d]]
        if v["kanal"] == "scam_engineer":
            govde += ["", ETIKET[d]["not_us"]]
        o += [f"## {ad}", "", "**Başlık:**", "```", t["baslik"], "```", "",
              "**Açıklama (geçici):**", "```", *govde, "```", ""]
    return "\n".join(o)


def main():
    hedef = os.path.dirname(os.path.abspath(__file__))
    for v in VIDEOLAR:
        open(os.path.join(hedef, f"{v['id']}.md"), "w", encoding="utf-8").write(video_dosyasi(v))
    for v in YAYINLANMIS:
        open(os.path.join(hedef, f"{v['id']}.md"), "w", encoding="utf-8").write(yayinlanmis_dosyasi(v))
    print(f"{len(VIDEOLAR)} planlanmış + {len(YAYINLANMIS)} yayınlanmış video dosyası yazıldı.")


if __name__ == "__main__":
    main()
