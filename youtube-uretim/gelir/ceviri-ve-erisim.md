# Çeviri ve erişim: çok dilli başlık/açıklama, çoklu ses kanalı, otomatik dublaj

**Kısa sonuç:**
- **Hemen yap:** Her videonun başlığını ve açıklamasını İspanyolca, Portekizce (Brezilya) ve Almanca ekle. Bedava, risksiz ve tüm kanallara açık. Hazır metinler `ceviriler/` klasöründe.
- **Kontrollü dene:** Otomatik dublaj (AI ses). Uygun videolarda varsayılan olarak açık gelebilir. Scam Engineer'da İspanyolca dublaj ABD'deki İspanyolca konuşan izleyiciye de ulaşır. Yayından önce dinle; Centworks'te ilk ay kapalı tut (gerekçe aşağıda).
- **Şimdilik yapma:** Elle çoklu ses kanalı (kendi dublajını yüklemek). Her video için ayrı TTS kaydı ve kontrol gerekir. 4.000 saat hedefi bitmeden zaman yatırımı olarak pahalı.

Güven düzeyleri: **Yüksek** = resmi YouTube sayfası veya büyük teknoloji basını. **Orta** = birden fazla ikincil kaynak tutarlı. **Düşük** = tek kaynak, satıcı blogu ya da çelişkili.

---

## 1) Üç ayrı özellik: karıştırma

| Özellik | Ne yapar | Kimlere açık | Bizim için |
|---|---|---|---|
| **Başlık ve açıklama çevirisi** | İzleyicinin dili İspanyolcaysa, videoyu senin yazdığın İspanyolca başlık ve açıklamayla görür. Video ve ses aynı kalır | Tüm kanallar. YPP şartı yok | **Hemen.** `ceviriler/<ID>.md` dosyalarını yapıştır |
| **Çoklu ses kanalı (multi-language audio)** | Videoya kendi hazırladığın başka dildeki ses dosyasını eklersin. İzleyici oynatıcıdan dili seçer | Eylül 2025'ten itibaren tüm içerik üreticilerine kademeli açıldı | Sonra. Kokoro ile ES/PT/DE seslendirme mümkün ama her video için iş yükü var |
| **Otomatik dublaj (auto-dubbing)** | YouTube, videonun konuşmasını yapay zekâyla çevirip seslendirir. "auto-dubbed" etiketiyle gösterilir | Uygun kanallarda varsayılan olarak açık. Video bazında uygunluk kontrolü var | Kontrollü dene. Aşağıdaki politika notunu oku |

### Kaynaklar ve güven
- **Başlık/açıklama çevirisi:** Studio'da *Altyazılar → Dil ekle → Başlık ve açıklama → Ekle* akışı. Resmi yardım: [Translate your own video titles & descriptions](https://support.google.com/youtube/answer/6289575?hl=en). **Güven: Yüksek.** Studio menü adları zamanla değişebilir.
- **Çoklu ses kanalı herkese açıldı (10 Eylül 2025, kademeli):** [TechCrunch](https://techcrunch.com/2025/09/10/youtubes-multi-language-audio-feature-for-dubbing-videos-rolls-out-to-all-creators/), [Android Authority](https://www.androidauthority.com/youtube-multi-language-audio-rollout-3596733/), [heise](https://heise.de/-10640944). Pilot kanallarda izlenme süresinin %25'ten fazlası ana dil dışındaki izlenmelerden gelmiş (YouTube'un açıklaması, basın aktarımı). **Güven: Yüksek** (yayılma), **Orta** (%25, pilot kanallar büyük kanallardı, bize genellenemez).
- **Otomatik dublaj 27 dile genişledi (Şubat 2026), "expressive speech" 8 dilde (EN, ES, PT, FR, DE, IT, HI, ID):** [Storyboard18](https://www.storyboard18.com/digital/youtube-expands-auto-dubbing-to-27-languages-adds-more-natural-and-expressive-voices-88923.htm), [Gulf News](https://gulfnews.com/technology/media/youtube-expands-ai-auto-dubbing-to-27-languages-with-expressive-speech-1.500433271), [PPC Land](https://ppc.land/youtube-auto-dubbing-tops-6m-daily-viewers-expands-to-27-languages), [Outlierkit](https://outlierkit.com/resources/youtube-auto-dubbing-all-creators-global-growth-2026/). **Güven: Orta.** Dil sayısı kaynaklara göre değişiyor (27 / 29 / 20). Dudak senkronu pilot aşamada; genel özellik değil.
- **Uygun olmayan videolar:** 120 dakikadan uzun, konuşması az olan, çok hızlı konuşulan, dili algılanamayan veya aktif Content ID talebi olan videolar. Kaynak: yukarıdaki PPC Land ve Storyboard18 haberleri. **Güven: Orta.** Videolarımız 7–9 dakika ve konuşma ağırlıklı, yani uygun olmalı. Müzikte Content ID talebi çıkarsa dublaj kapanır (müzik seçimi için bkz. `muzik-ve-ses.md`).
- **"auto-dubbed" etiketi, orijinal ses her zaman seçilebilir:** [YouTube resmi blog – Auto dubbing](https://blog.youtube/news-and-events/auto-dubbing-on-youtube/), [Uppbeat](https://uppbeat.io/blog/creator-news/youtube-auto-dubbing). **Güven: Yüksek.**
- **Dublajlı videolarda izlenme süresinin %40'tan fazlası dublaj dilini seçen izleyicilerden** (Neal Mohan, Şubat 2025 yıllık mektubu, PPC Land aktarımı). **Güven: Orta.**
- **Dublajlı izlenmenin ortalama süresi orijinalin yaklaşık %75'i:** [AIR Media-Tech](https://air.io/en/youtube-hacks/is-youtubes-ai-dubbing-safe-for-your-channel-auto-dub-vs-pro-with-real-retention-data). **Güven: Düşük.** Dublaj hizmeti satan şirketin verisi.
- **Dublajlı izlenmelerin reklam geliri:** Resmi ve net bir kaynak bulunamadı. Dublaj ayrı video değil, aynı videonun ses kanalı. Bu yüzden izlenme süresi aynı videoya yazılır (mantıksal çıkarım, **Güven: Orta**). YPP 4.000 saat sayımına katkısı için resmi teyit yok. **Doğrulanamadı.** Studio → Analytics'te "Ses dili" (audio track) kırılımına bak.
- **İzleyici tarafında otomatik başlık çevirisi:** YouTube, bazı izleyicilere başlıkları otomatik çeviriyor ya da bunu test ediyor; izleyici şikâyetleri var ([PPC Land](https://ppc.land/youtube-users-complain-about-forced-auto-translation/), [XDA](https://www.xda-developers.com/youtube-show-video-titles-native-language/)). **Güven: Düşük** (kapsam belirsiz). Bizim için anlamı: makine çevirisine bırakmak yerine kendi çevirimizi yüklemek, başlıktaki merak öğesini ve arama kelimesini korur.

---

## 2) Neden İspanyolca, Portekizce (Brezilya), Almanca?

- **Otomatik dublajın "expressive speech" desteklediği diller** arasında üçü de var. Yani ileride dublaj açarsak en doğal sesi bu dillerde alırız (kaynak yukarıda, **Orta**).
- **İspanyolca:** Scam Engineer için en değerli dil. ABD'de İspanyolca konuşan büyük bir nüfus var ve videodaki kurumlar (FTC, FBI IC3, 7726) onlar için de geçerli. FTC'nin İspanyolca tüketici sitesi var: [consumidor.ftc.gov](https://consumidor.ftc.gov). **Güven: Yüksek** (sitenin varlığı). Bu yüzden SE açıklamalarına "kaynaklar ABD'ye ait" notu eklendi ama silinmedi; ABD'deki İspanyolca izleyiciye doğrudan uyar.
- **Portekizce (Brezilya):** Büyük YouTube pazarı. Hidden Systems'ın altyapı konuları (kesinti, bulut, şebeke) ülkeye bağlı değil.
- **Almanca:** Yüksek reklam fiyatlı pazar. Hidden Systems'ın İngiltere odaklı konuları (bakır hat kapanışı, Google Cloud Londra) Almanca konuşan izleyici için de "aynısı bizde olur mu?" sorusunu doğurur.

> **Beklenti:** Bu adım tek başına büyüme getirmez. Yeni izleyici çoğunlukla arama ve "önerilen videolar" ile gelir; çeviri yalnızca o dilde arayanın videoyu bulmasını ve tıklamasını kolaylaştırır. Etkiyi 4 hafta sonra Studio → Analytics → *Coğrafya* ve *Altyazı/CC dili* kırılımlarında ölç.

---

## 3) Politika notu: otomatik dublaj ve yapay zekâ sesi

- Anlatım zaten TTS (Kokoro). Dublaj da AI sesi. İkisi birlikte "insansı içerik eksikliği" sinyali gibi okunabilir.
- YouTube'un "inauthentic content" politikası Temmuz 2026'da netleşti ve finans, sağlık ve hukuk konularında **yapay zekâ karakteri/persona** kullanan içerik ayrı bir kategori olarak sayıldı (ayrıntı ve kaynaklar: `oyun-kitabi/yapay-zeka-ve-politika.md`).
- **Centworks** finans konusu. Dublajda "Bu kanal bir mühendis tarafından yapılır" cümlesi ve "finansal tavsiye değildir" uyarısı yanlış veya eksik çevrilirse risk artar. **Öneri:** İlk ay otomatik dublajı **kapalı** tut. Yalnızca başlık ve açıklama çevirisi yap.
- **Scam Engineer:** Telefon numaraları (7726, 1-800-MEDICARE, 1-833-FRAUD-11) dublajda yanlış okunabilir. **Öneri:** İspanyolca dublajı aç, ama yayından önce numaraların geçtiği bölümleri dinle. Yanlışsa o dilin dublajını yayından kaldır. Studio'da otomatik dublajları yayından önce inceleme ve kaldırma seçeneği olduğu aktarılıyor (**Güven: Orta**, Studio'da kontrol et).
- **Hidden Systems:** En düşük risk. Dublajı aç, ilk 2 videoda dinleyerek kalite kontrolü yap.
- Her durumda: dublajı açtığın videonun açıklamasına (her dilde) şunu ekle: *"Audio in other languages is auto-dubbed by YouTube."* Çevirisi: ES *"El audio en otros idiomas está doblado automáticamente por YouTube."* / PT *"O áudio em outros idiomas é dublado automaticamente pelo YouTube."* / DE *"Der Ton in anderen Sprachen wird von YouTube automatisch synchronisiert."*

---

## 4) Uygulama: her yayında 5 dakika

1. Video İngilizce yayına girdikten hemen sonra Studio → **Altyazılar** → videoyu aç.
2. **Dil ekle** → *Spanish* → *Başlık ve açıklama* → **Ekle** → `ceviriler/<ID>.md` içindeki İspanyolca başlığı ve açıklama kod bloğunu yapıştır → **Yayınla**.
3. Aynısını *Portuguese (Brazil)* ve *German* için tekrarla.
4. Zaman kodları senaryodan otomatik alındı. Kurguda bölüm süreleri değişirse İngilizce senaryodaki CHAPTERS'ı düzelt ve şunu çalıştır:
   ```
   python ceviriler/_uret.py
   ```
5. Etiketler (tags) çevrilmez, gerek yok. Hashtag kullanıyorsan İngilizce kalsın.
6. Otomatik dublaj açıksa: Studio'da videonun dil listesinde dublajın durumunu kontrol et ve yukarıdaki politika notuna göre dinle.

### Kanal düzeyinde (tek seferlik)
- Studio → **Ayarlar → Kanal → Temel bilgiler → Dil ekle** ile kanal adı ve açıklaması da çevrilebiliyor (**Güven: Orta**, menü yeri değişebilir). Kanal adları marka olduğu için **çevrilmez**; yalnızca "Hakkında" metni çevrilir. Hakkında metinleri: `kanal-sayfalari.md`.

---

## 5) `ceviriler/` klasörü

| Dosya | İçerik |
|---|---|
| `_veri.py` | Tüm çeviriler: başlık, özet, bölüm adları, kimlik cümleleri, dipnotlar, yardım satırı ifadeleri |
| `_uret.py` | `_veri.py` + orijinal senaryodan (zaman kodları, kaynaklar, yardım satırları) `<ID>.md` dosyalarını üretir. Başlık 100 karakteri aşarsa veya bölüm sayısı tutmazsa hata verir |
| `HS-04` … `HS-07`, `CW-03` … `CW-06`, `SE-03` … `SE-06`, `EV-01` … `EV-04` | Planlanmış 16 video. Başlık + yapıştırmaya hazır açıklama (özet, kimlik cümlesi, bölümler, yardım/ihbar, kaynaklar, görsel notu) |
| `P-HS-ispanya`, `P-HS-crowdstrike`, `P-HS-deprem`, `P-CW-gec-odeme`, `P-CW-para-yaratma`, `P-SE-spoofing`, `P-SE-sim-swap` | Yayınlanmış 7 video. Şimdilik başlık + geçici açıklama. Gerçek İngilizce başlıklar depoda olmadığı için **yapıştırmadan önce mevcut başlıkla karşılaştır**. Bölümler ve kaynaklar S4 (`yayinlanmis-video-iyilestirme.md`) ile eklenir |

**Çeviri kuralları:**
- Kimlik cümleleri üç kanal cümlesinin birebir çevirisidir. Birinci tekil şahıs yok.
- Rakamlar ve tarihler hedef dilin biçimine göre yazıldı (ES/DE ondalık ayracı ve "mil millones", PT "US$ … bilhões").
- Kaynak başlıkları ve linkler İngilizce bırakıldı. Kaynağın kendisi İngilizce.
- Scam Engineer'da korku dili yok. "Con calma / Com calma / ruhig erklärt" kalıbı kanal tonunu taşır.
- Makine çevirisi kullanılmadı. Yine de yayından önce o dili bilen biri varsa başlıkları göstermek iyi olur.
