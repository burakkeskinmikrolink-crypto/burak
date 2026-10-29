# shorts_sablonlari: Shorts format şablonları, JSON şeması ve doğrulayıcı

Üç kanalın Short'ları için üç sabit format var. Her Short, `short.schema.json` şemasına uyan bir JSON dosyası olarak yazılır. `dogrula.py`, şemanın ifade edemediği kanal kurallarını da kontrol eder: ilk kare, döngü, süre, yasak ifadeler.

```
shorts_sablonlari/
├── short.schema.json          JSON Schema (draft 2020-12)
├── dogrula.py                 şema + kanal kuralları doğrulayıcısı
├── test_dogrula.py            birim testleri
├── sablonlar/                 format tanımları (zamanlama, kurallar, boş iskelet)
│   ├── quiz.json
│   ├── kisa-hikaye.json
│   └── gercek-mi-sahte-mi.json
└── ornekler/                  doldurulmuş örnekler (v2 Short'larından)
    ├── quiz-se04-medicare.json
    ├── quiz-cw03-yuvarlama.json
    ├── kisa-hikaye-se03-kod.json
    └── gercek-mi-sahte-mi-se06-magaza.json
```

---

## Üç format özeti

| | Quiz (A/B/C) | Kısa hikâye | Gerçek mi sahte mi |
|---|---|---|---|
| **Süre** | 30–35 sn | 34–40 sn | 30–34 sn |
| **0–2 sn (hook)** | Soru | Hikâyenin **sonucu** | "Real or fake? Three X." |
| **Gövde** | 2–12 sn şıklar → 3 sn geri sayım → cevap ve tek kural | 2–14 kurulum → 14–26 dönüm (gizli mekanizma) → ders | 3 öğe × ~9 sn: ifade → 1,5 sn bekleme → etiket → tek cümle gerekçe |
| **Son 2–3 sn** | Soruya geri dönen köprü | Sonuca geri dönen köprü | "Next round? Real or fake…" |
| **Özel kural** | Doğru şık harfini Short'lar arasında değiştir | İlk karede "Composite character", yüz yok | En az bir öğe "gerçek" ya da "OK" olsun |

## Tüm formatlar için kurallar (doğrulayıcı kontrol eder)
1. **İlk kare hareketli** (`ilk_kare.hareket` alanı zorunlu, statik kare yasak).
2. **Ekran yazısı en fazla 6 kelime** ve **seslendirmenin ilk cümlesiyle birebir aynı** (noktalama ve harf büyüklüğü hariç).
3. İlk sahne 0–2 sn arasında ve rolü `hook`. Sahneler boşluksuz ve son sahne `sure_sn`'de biter.
4. VO toplamı **60–115 kelime** (30–45 sn).
5. **Döngü:** Son cümle `…`, `:` veya `—` ile biter ve `dongu.hedef` VO'nun ilk cümlesidir.
6. **Yasak:** "full story", "on the channel", "link in bio" gibi çağrılar ve birinci tekil şahısla kimlik iddiası ("I'm a telecom engineer").
7. **Açıklama**, `Related video bağlantısı: <video adı>` notunu içerir. `related_video` alanı zorunludur.

## Kullanım
```bash
# Bir veya daha fazla Short'u doğrula
python dogrula.py ornekler/*.json

# Şablon dosyalarının eksiksiz olduğunu kontrol et
python dogrula.py --sablon sablonlar/*.json

# Testler
python -m unittest test_dogrula
```
Windows PowerShell'de de aynı komutlar çalışır (`python` yerine gerekirse `py`).

**Bağımlılık:** `jsonschema` paketi kuruluysa (`pip install jsonschema`) tam şema doğrulaması yapılır. Kurulu değilse yalnızca zorunlu alanlar ve kanal kuralları kontrol edilir.

## Yeni Short yazmak
1. `sablonlar/<format>.json` içindeki `bos_iskelet` nesnesini kopyalayıp yeni bir dosyaya yapıştır.
2. Alanları doldur. `zamanlama` ve `ilk_kare_kurallari` alanlarını rehber olarak kullan.
3. `python dogrula.py yeni-short.json` komutu hata vermeden geçene kadar düzelt.
