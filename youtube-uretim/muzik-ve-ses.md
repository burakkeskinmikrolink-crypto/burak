# Müzik ve ses rehberi (YouTube Ses Kitaplığı, seviyeler, Kokoro TTS)

**Kısa özet:**
1. **Müzik:** Yalnızca YouTube Ses Kitaplığı'ndan, "atıf gerekmez" filtresiyle. Kanal başına sabit bir ses karakteri. Sözlü müzik yok.
2. **Seviye:** Final miks ≈ −14 LUFS. Müzik konuşmanın **yaklaşık 20 dB altında**; Scam Engineer'da daha da düşük ya da önemli bilgide hiç yok.
3. **TTS:** Kokoro **SSML okumaz**. Duraklama ve hız için kendi işaretlerimiz var: `[pause]`, `[pause 1200]`, `[slow]…[/slow]`. Araç: `arac/seslendirme/seslendir.py`.

> ⚠️ **Oyun kitabındaki düzeltme:** `oyun-kitabi/gorsel-ve-ses.md` §C'de SSML örneği (`<break>`, `<emphasis>`, `<prosody>`) var. Bu etiketler Polly/Azure/Google gibi motorlar için geçerli. **Kokoro'nun resmi Python paketi SSML ayrıştırmaz; etiketler sesli okunabilir.** Kokoro kullanılıyorsa bu dosyadaki işaretler geçerlidir. (Kaynaklar §3.)
> Aynı dosyadaki politika notu hâlâ geçerli: Centworks ve Scam Engineer için gerçek insan sesi daha düşük risk (`oyun-kitabi/yapay-zeka-ve-politika.md`, `eksik-analizi.md` §4).

Güven düzeyleri: **Yüksek** = resmi sayfa veya bağımsız araştırma. **Orta** = birden fazla ikincil kaynak tutarlı. **Düşük** = tek kaynak veya satıcı.

---

## 1) YouTube Ses Kitaplığı: ne, nasıl, neden

| Bulgu | Kaynak | Güven |
|---|---|---|
| Studio → **Ses Kitaplığı**'ndan indirilen müzik ve efektler YouTube'a yüklenen videolarda telifsiz kullanılabilir ve Content ID ile talep (claim) almaz | [YouTube Help – Use music and sound effects from the Audio Library](https://support.google.com/youtube/answer/3376882?hl=en) | Yüksek |
| Filtre çubuğunda **lisans türü** filtresi var: "atıf gerekmez" (standart Ses Kitaplığı lisansı) seçilebilir | Aynı sayfa | Yüksek |
| Güvence yalnızca Ses Kitaplığı içindir. Başka sitedeki "telifsiz" etiketi veya açıklamaya "free song" yazmak Content ID taramasını durdurmaz | Aynı sayfa; ikincil rehberler | Yüksek / Orta |
| Yayından önce videoyu **liste dışı** yükleyip telif kontrolünün bitmesini beklemek, talepleri erken yakalar | İkincil rehberler | Orta |

**Neden önemli:**
- Content ID talebi olan videoda **otomatik dublaj kapanır** (`gelir/ceviri-ve-erisim.md`).
- YPP sonrası gelir talep sahibine gidebilir.
- Shorts'u Facebook Reels'e yüklerken (`gelir/hizli-kazanimlar.md` #9) YouTube'un ticari Shorts müzikleri **başka platformda kullanılamaz**. Bu yüzden Shorts'ta da Ses Kitaplığı parçası kullan.

**Kural:**
- Yalnızca "Attribution not required" parçaları.
- Atıf gereken bir parça zorunluysa açıklamaya, Ses Kitaplığı'nın verdiği atıf satırını aynen ekle.
- Her videonun müziğini `arac/gorsel_kutuphane/` projesindeki `kaynaklar.txt` dosyasına yaz: parça adı, sanatçı, lisans türü, indirme tarihi.

### Kanal başına müzik profili
Ses Kitaplığı filtreleri: **Tür (Genre)**, **Ruh hâli (Mood)**, **Enstrüman**, **Süre**, **Lisans türü**. (Filtre adları arayüzde değişebilir; **Güven: Orta**.)

| Kanal | Tür | Ruh hâli | Enstrüman | Kaçın | Hareket kuralı |
|---|---|---|---|---|---|
| **Hidden Systems** | Ambient, Cinematic | Dark, Dramatic, Calm (açıklama bölümlerinde) | Synth pad, piano, strings, düşük drone | Davul ağırlıklı "epic trailer" müziği, ani vuruşlar, şarkı sözü | Her sahne/perde değişiminde parça veya yoğunluk değişir. Soru cümlesinde müzik 1–2 sn tamamen kesilir |
| **Centworks** | Ambient, Electronic (hafif), Corporate değil | Bright, Calm, Inspirational | Piano, plucks, hafif perküsyon | Gerilim müziği, "para yağmuru" neşesi, yüksek tempolu EDM | Rakam ekranlarında müzik bir kademe düşer; raunt geçişlerinde kısa geçiş efekti |
| **Scam Engineer** | Ambient, Acoustic, Classical (yumuşak) | **Calm**, Inspirational. **Dark/Dramatic yok** | Piano, akustik gitar, yumuşak pad | Korku/gerilim "stinger"ları, siren, alarm sesi, kalp atışı efekti (korku dili yasağının ses karşılığı) | Hikâye kısmında hafif müzik; **kontrol listesi, telefon numarası ve "ne yapmalı" bölümlerinde müzik yok** |

**Ses efektleri (Ses Kitaplığı → Sound effects):** Bölüm geçişinde tek, yumuşak "whoosh" ya da "click". Hidden Systems'te kesinti anında kısa elektrik "hum"ının kesilmesi. Scam Engineer'da telefon titreşimi/SMS sesi hikâyeyi taşır ama **alarm sesi yok**.

---

## 2) Seviyeler: müzik konuşmanın ne kadar altında?

| Bulgu | Kaynak | Güven |
|---|---|---|
| YouTube yüksek sesli videoları oynatırken kısar; referansın **≈ −14 LUFS** olduğu yaygın biçimde bildiriliyor. YouTube sessiz videoyu yükseltmez. "Stats for nerds" → "content loudness" değeri uygulanan ayarı gösterir | [Production Advice – YouTube loudness](https://productionadvice.co.uk/youtube-loudness/), [MeterPlugs](https://meterplugs.com/blog/2019/09/18/youtube-changes-loudness-reference-to-14-lufs.html) | **Orta** (YouTube resmi bir rakam yayımlamıyor) |
| BBC'nin yapımcı rehberi: konuşmayla birlikte çalan arka plan müziğini **ek olarak 3–4 dB kıs**; şarkı sözü ve vurgulu davul kullanma | Salford Üniversitesi araştırması, BBC rehberini aktararak ([Salford repository](https://salford-repository.worktribe.com/OutputFile/1488623)) | Orta (BBC belgesine ikincil kaynaktan ulaşıldı) |
| Widex/Channel 4 araştırması (BBC ve RNID destekli): **65 yaş üstünün %62'si** arka plan müziğinin programdan aldıkları keyfi azalttığını söyledi | Aynı Salford kaynağı ve ilgili çalışmalar | Orta |
| İşitme kaybı olan dinleyiciler, konuşmayı anlamak için daha yüksek konuşma/arka plan oranına ihtiyaç duyar (rakip bir ses için ~10 dB'ye kadar ek fark) | [arXiv – Dialogue enhancement… people above 65](https://arxiv.org/pdf/2006.14282) ve atıf verdiği çalışmalar | Orta |

### Bizim kuralımız (deneyim kuralı + yukarıdaki bulgular)
| Öğe | Hidden Systems | Centworks | Scam Engineer (40+) |
|---|---|---|---|
| Final miks (integrated) | −14 LUFS | −14 LUFS | −14 LUFS |
| Konuşma tepe (true peak) | ≤ −1 dBTP | ≤ −1 dBTP | ≤ −1 dBTP |
| Müzik, konuşma **varken** | konuşmanın ~18–20 dB altı | ~20 dB altı | **~24 dB altı** veya hiç |
| Müzik, konuşma **yokken** (geçiş, bitiş ekranı) | ~6–8 dB altı | ~6–8 dB altı | ~8–10 dB altı |
| Ses efekti | konuşmanın ~10–12 dB altı | ~12 dB altı | ~12 dB altı, alarm yok |
| Sidechain/ducking | Açık (konuşma başlayınca müzik 0,3 sn'de iner) | Açık | Açık |

> Rakam referansı: "konuşmanın X dB altı" = müzik kanalının ortalama seviyesi (LUFS-S) ile anlatımın ortalama seviyesi arasındaki fark. Kulağa göre son kontrol: telefon hoparlöründe ve kulaklıkta bir kez dinle. **Telefon hoparlöründe müzik duyuluyorsa fazla yüksek.**

### Uygulama (ücretsiz araçlar)
- **DaVinci Resolve (Fairlight):** Anlatım kanalına compressor (oran 3:1, hafif). Müzik kanalına **Ducker** ya da sidechain compressor, anahtar = anlatım kanalı. Deliver sayfasında **Normalize audio levels → −14 LUFS**, true peak −1 dBTP. (Menü adları sürüme göre değişebilir; **Güven: Orta**.)
- **Audacity:** Effect → **Loudness Normalization** (perceived loudness, −14 LUFS). Müzik için Effect → **Auto Duck** (anlatım kanalını kontrol kanalı olarak kullanır).
- **Kontrol:** Yükledikten sonra Stats for nerds → "content loudness". 0 dB'ye yakınsa hedefe yakınsın; +6 dB gibi büyük bir pozitif değer miksin çok sessiz olduğunu gösterir.

---

## 3) Kokoro TTS: ses seçimi, noktalama ve işaretleme

| Bulgu | Kaynak | Güven |
|---|---|---|
| Kokoro'nun İngilizce telaffuzu **misaki** G2P kütüphanesinden gelir (İngilizcede espeak kullanılmaz) | [DeepInfra – Kokoro-82M](https://deepinfra.com/hexgrad/Kokoro-82M), [Kokoro-82M Core AI](https://huggingface.co/mlboydaisuke/Kokoro-82M-CoreAI) | Orta |
| Telaffuz özelleştirme: Markdown link söz dizimi `[Kokoro](/kˈOkəɹO/)` (IPA eğik çizgiler arasında). Kod içinden sözlüğe "gold" girişi de eklenebilir | [Kokoro TTS demo (HF Space)](https://pendrokar-kokoro-tts.hf.space/), [FluidInference docs](https://docs.fluidinference.com/tts/kokoro) | Orta |
| **SSML:** Resmi Python paketinde SSML ayrıştırıcı yok; `<break>` gibi etiketler düz metin gibi okunabilir. Bazı sarmalayıcılar (ör. FluidInference Swift) kendi SSML desteğini ekliyor | [deAPI – Kokoro TTS guide](https://deapi.ai/blog/kokoro-tts-guide-how-to-control-41-voices-with-nothing-but-punctuation), FluidInference docs | Orta (kaynaklar çelişkili; sarmalayıcıya bağlı) |
| Duraklama için ayrı bir etiket yok; noktalama (virgül, nokta, üç nokta) duraklamayı belirler | deAPI; [pykokoro docs](https://pykokoro.readthedocs.io/en/stable/advanced_features.html) | Orta |
| Hız parametresi var (uygulamalarda 0,5–2,0 aralığı yaygın) | DeepInfra, topluluk uygulamaları | Orta |
| Ses paketleri `voices/*.pt` dosyaları. Ses adlarının ön eki aksan ve cinsiyeti gösterir (`af_`/`am_` Amerikan kadın/erkek, `bf_`/`bm_` İngiliz kadın/erkek) | hexgrad/Kokoro-82M deposu (VOICES.md) | **Orta** (ön ek düzeni bu turda aramayla doğrulanamadı; depodaki VOICES.md'den kontrol et) |

### 3.1) Kanal başına ses
- **Hidden Systems:** İngiliz İngilizcesi pipeline'ı (`lang_code="b"`), erkek İngiliz sesi adayları (`bm_…`). 3 adayı aynı paragrafla dene, birini seç ve **bir daha değiştirme**.
- **Centworks ve Scam Engineer:** Amerikan İngilizcesi (`lang_code="a"`), sakin ve orta tonlu bir ses (`am_…` veya `af_…`).
- **Test paragrafı** (üç kanalda aynı; telaffuz, sayı ve soru tonunu sınar):
  > Nine billion dollars. Twelve million in the bank. On the twenty-third of December, 2022, the frequency fell to 59.4 hertz. Why? Because the gas froze. Forward it to 7726.
- **Hız:** Hidden Systems 0.95–1.0 · Centworks 1.0 · Scam Engineer **0.92–0.95** (40+ kitle). `seslendir.py --hiz`.

### 3.2) Kulak için yazım kuralları (senaryo metninde)
| Kural | Örnek (yanlış → doğru) | Neden |
|---|---|---|
| Önemli rakamları yazıyla yaz | "$9B" → "nine billion dollars" | TTS sembolleri tutarsız okuyabilir; ekranda rakam zaten görünüyor |
| Tarihleri konuşur gibi yaz | "23/12/2022" → "the twenty-third of December, 2022" (İngiliz) / "December twenty-third" (ABD) | Biçim kanalın aksanına uymalı |
| Kısaltma ya harf harf ya kelime olarak, karar `telaffuz.json`'da | "NESO" → "nee-so", "FDIC" → "F D I C" | Aynı kısaltma her videoda aynı okunsun |
| Parantez kullanma | "(and it failed)" → ", and it failed," | TTS parantezde tonu düşürmez |
| Cümle en fazla ~20 kelime | — | Nefes ve vurgu doğal kalır |
| Soru cümlesi soru işaretiyle bitsin | — | Araç sorudan sonra otomatik +1 sn sessizlik ekler |
| Tire (—) yerine virgül veya nokta tercih et | "It worked — barely." → "It worked. Barely." | Tirenin duraklaması motordan motora değişir |
| Üç nokta (…) yalnızca bilinçli dramatik duraklamada | "And then… nothing." | Fazlası yapay duyulur |

### 3.3) İşaretleme (senaryodaki "> " satırlarına yazılır)
| İşaret | Ne yapar | Ne zaman |
|---|---|---|
| `[pause]` | 700 ms sessizlik | Bir bilgiyi "oturtmak" için, paragraf içinde |
| `[pause 1200]` | Belirtilen ms kadar sessizlik | Büyük açıklamadan önce (en fazla 1.500 ms) |
| `[slow]…[/slow]` | O kısım ×0.92 hızda | Kural, telefon numarası, adım listesi |
| (otomatik) soru işareti | +1.000 ms | Merak sorularından sonra |
| (otomatik) paragraf sonu | 600 ms | — |
| (otomatik) sahne sonu | 900 ms | — |

**Örnek (HS-04'ten):**
```
> The batteries took the load. [pause] The generators stayed silent.
>
> So how does a building designed for power cuts lose to… a power cut?
```
**Örnek (Scam Engineer):**
```
> [slow]Hang up. Then call the number on the back of your card.[/slow] [pause]
> A real bank will never mind.
```

- İşaretler **altyazıya geçmez**: `arac/altyazi/transkript.py` köşeli parantezleri temizler.
- Mevcut senaryolarda işaret yok. **Varsayılan otomatik duraklamalar** çoğu video için yeterli. İşareti yalnızca dinlerken gerçekten gereken yere ekle. Paragraf başına en fazla bir `[pause]`.

### 3.4) Araç: `arac/seslendirme/`
```
pip install kokoro soundfile numpy
python arac/seslendirme/seslendir.py hidden_systems/08-v2.md --plan
python arac/seslendirme/seslendir.py hidden_systems/08-v2.md -o arac/seslendirme/cikti/hs08.wav --dil b --ses <seçtiğin bm_ sesi> --hiz 0.97
```
- `--plan` Kokoro olmadan çalışır: her cümleyi, hızını ve sonrasındaki sessizliği listeler. Toplam eklenen sessizliği gösterir (HS-08: ~30 sn).
- Telaffuz sözlüğü: `arac/seslendirme/telaffuz.json` (yazılış → okunuş). Yeni bir özel ad çıkınca buraya ekle. Okunuş IPA değil, düz İngilizce heceleme. Kokoro'nun `[kelime](/IPA/)` söz dizimi de çalışır ama yanlış IPA daha kötü sonuç verir.
- Testler: `cd arac/seslendirme && python -m unittest discover -s tests -t .` (6 test, Kokoro gerekmez).

### 3.5) Kurgu sonrası ses zinciri (anlatım kanalı)
1. Gürültü yok (TTS temiz). EQ: 80 Hz altını kes, 3–5 kHz'de hafif (+1–2 dB) netlik.
2. Hafif compressor (3:1, atak 10 ms, release 100 ms).
3. Çok hafif oda yankısı (TTS'in "kuru" sesini yumuşatır; wet ≤ %8).
4. Limiter −1 dBTP.
5. Final normalizasyon −14 LUFS (§2).

---

## 4) Video başına ses kontrol listesi
- [ ] Müzik: Ses Kitaplığı, "atıf gerekmez". Parça adları `kaynaklar.txt`'de.
- [ ] Sözlü müzik yok. Scam Engineer'da alarm/gerilim efekti yok.
- [ ] Soru cümlelerinde müzik 1–2 sn çekildi.
- [ ] Ducking açık. Telefon hoparlöründe müzik konuşmayı bastırmıyor.
- [ ] Final −14 LUFS, true peak ≤ −1 dBTP.
- [ ] Liste dışı yüklemede telif talebi çıkmadı (otomatik dublaj için şart).
- [ ] Telaffuz: özel adlar `telaffuz.json`'da, test paragrafı bir kez dinlendi.
