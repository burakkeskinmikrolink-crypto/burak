# Hızlı kazanımlar: başka kanallarda işe yaramış 10 taktik

**Kapsam:** `oyun-kitabi/` içinde yazılanlar burada **tekrar edilmedi**. Oradakiler: Test & Compare, başlık formülleri, bitiş ekranı, seri/oynatma listesi, topluluk gönderisi, yoruma kalp/sabitleme, Short → Related video, yayın saati, forum/dış trafik, hook, tempo, Ken Burns, TTS, YPP/RPM, üyelik, affiliate, sponsorluk. `gelir/4000-saat-plani.md`'deki derleme ve Premiere de tekrar edilmedi.

**Güven düzeyi:** **Yüksek** = YouTube resmi sayfası veya bağımsız veri. **Orta** = birden fazla ikincil kaynak tutarlı ya da mekanizma resmi ama etkisi ölçülmemiş. **Düşük** = tek anekdot, satıcı blogu.

**Dürüst not:** "Kanıtlandı" sütunundaki örneklerin çoğu büyük kanallardan. Küçük kanalda etki daha küçük olur. Her taktiği uygula, 4 hafta sonra `haftalik-analiz-sablonu.md` ile ölç, işe yaramayanı bırak.

## Özet tablo (öncelik sırasıyla)

| # | Taktik | Kanal | Süre | Beklenen etki | Güven |
|---|---|---|---|---|---|
| 1 | Senaryodan doğru altyazı yükle | Hepsi | 5 dk/video | Küçük ama kalıcı (+%7 izlenme ölçülmüş bir çalışmada) | Orta |
| 2 | Oynatma listesi içi link (`&list=`) | Hepsi | 10 dk, bir kez | Oturum başına +1 video izlenme şansı | Düşük–Orta |
| 3 | Yorumlara Short ile yanıt | Scam Engineer, Centworks | 20 dk/Short | Bedava Short konusu + yorumcuya bildirim | Orta |
| 4 | Haber tetiklemeli yeniden paketleme | Hidden Systems, Scam | 15 dk/olay | Eski videoya ikinci hayat | Düşük–Orta |
| 5 | 48 saatte hızlı açıklama videosu | Hidden Systems, Scam | 1 gün/olay | En büyük tek seferlik sıçrama potansiyeli | Orta |
| 6 | Oynatma listesini "podcast" yap | Hidden Systems, Centworks | 10 dk, bir kez | YouTube Music'te arka planda dinlenme | Orta |
| 7 | Videonun makale sürümü (web sitesi) | Hepsi, önce Scam | 30 dk/video | Google aramadan yavaş ama birikimli trafik | Düşük–Orta |
| 8 | Tek sayfalık PDF + e-posta listesi | Scam, Centworks | 1 gün kurulum | Platformdan bağımsız kitle, ileride sponsor değeri | Düşük |
| 9 | Shorts'u Facebook Reels'e de yükle | Scam, Centworks | 5 dk/Short | 40+ kitleye ek erişim | Orta |
| 10 | Hype için hazırlık | Hepsi (YPP sonrası) | 2 dk/video | YPP + 500 abone sonrası keşif | Yüksek (kural), Düşük (etki) |

---

## 1) Senaryodan doğru altyazı yükle

- **Ne yapılır:** Otomatik altyazıya bırakma. Senaryonun anlatım metnini YouTube Studio'ya "zamanlama olmadan" yükle. YouTube metni sesle kendisi eşler.
- **Nerede kanıtlandı:** Discovery Digital Networks'ün 2013 kontrollü testi: altyazılı 125 video, altyazısız 209 videoya göre **%7,32 daha fazla** izlenme aldı. Fark ilk 14 günde **%13,48** idi. Paylaşım ve diğer etkileşimde anlamlı fark çıkmadı. [3Play Media vaka çalışması](https://www.3playmedia.com/case-studies/discovery-digital-networks/), [3Play özet](https://www.3playmedia.com/blog/studies-find-captions-improve-engagement). **Güven: Orta.** Eski bir çalışma ve kaynak altyazı hizmeti satan şirket. Bazı bloglardaki "%40" rakamı doğrulanamadı, kullanma.
- **Bizde nasıl:** Hazır araç: `arac/altyazi/transkript.py`. Senaryodan "> " satırlarını alır, ses işaretlerini (`<break>`, `[pause]`) temizler.
  ```
  python arac/altyazi/transkript.py hidden_systems/04-v2.md -o arac/altyazi/cikti
  ```
  Studio → **Altyazılar** → İngilizce → **Ekle** → **Dosya yükle** → **Zamanlama olmadan** → `.txt` dosyasını seç.
- **Neden bizde daha değerli:** TTS anlatımda özel adlar ("europe-west2", "Greensill", "7726") otomatik altyazıda sık bozulur. Sessiz izleyenler (telefon, toplu taşıma) doğru metni görür. Çeviri altyazılarının (`ceviriler/`) temeli de bu metin olur.
- **Beklenen etki:** Küçük ama her videoda kalıcı. Ayrıca erişilebilirlik.
- **Süre:** Video başına 5 dakika. Senaryo kurguda değiştiyse önce `.md` dosyasını düzelt.

## 2) Açıklamada ve sabit yorumda oynatma listesi içi link

- **Ne yapılır:** Bir sonraki videoya düz link (`youtu.be/ID`) yerine **oynatma listesi içinden** link ver: `https://www.youtube.com/watch?v=ID&list=PLAYLIST_ID`. Bu linkten açılan video, bittiğinde YouTube'un önerisine değil, **listedeki sıradaki videoya** geçer.
- **Nerede kanıtlandı:** Mekanizma: URL'de `list=` varsa oynatıcı onu liste olarak açar ([Online Tech Tips – YouTube URL tricks](https://www.online-tech-tips.com/9-youtube-url-tricks-you-need-to-try-now/)). Belgesel ve eğitim kanallarında "seri linki" yaygın bir uygulama. **Etkisini ölçen bağımsız bir çalışma bulunamadı. Güven: Düşük–Orta.**
- **Bizde nasıl:**
  - Hidden Systems: açıklamanın en altına `Watch the whole Outage Files series: <liste içi link>`.
  - Scam Engineer evergreen videolar: "Is It a Scam?" listesine liste içi link. Sırası: evergreen-01 → 03 → 04 → 02 (metin → link → para → kimlik).
  - Centworks: "What If…" ve "Money Mechanics" listeleri (adlar: `kanal-sayfalari.md`).
  - Sabit yorumdaki "next video" linki de liste içi olsun (`topluluk-ve-yorum.md`).
- **Beklenen etki:** İzleyici başına izlenen video sayısı. Studio'da "Oynatma listesinden gelen izlenme" kaynağını izle.
- **Süre:** Listeler kurulduktan sonra 10 dakika. Her yeni videoda 1 dakika.

## 3) Yorumlara Short ile yanıt

- **Ne yapılır:** Bir yorumdaki soruya metinle değil, **Short ile** cevap ver. Studio veya mobil uygulamada yorumun altında *Yanıtla → Short oluştur*. Yorum, Short'un içinde çıkartma (sticker) olarak görünür. Yorumu yazana bildirim gider ve Short yorumun altında görünür.
- **Nerede kanıtlandı:** Eylül 2022'de YouTube'a geldi. TikTok'un 2020'den beri olan "video ile yanıt" özelliğinin karşılığı. TikTok'ta soru-cevap kanallarının temel formatı. [YouTube Help](https://support.google.com/youtube/answer/12816427), [TechCrunch](https://techcrunch.com/2022/09/16/youtube-encourages-creators-to-make-shorts-directly-from-replies), [Social Media Examiner rehberi](https://www.socialmediaexaminer.com/how-to-reply-to-youtube-comments-with-shorts/). **Güven: Orta** (özellik resmi, büyüme etkisi ölçülmemiş). Arayüz değişmiş olabilir, ilk kullanımda kontrol et.
- **Bizde nasıl:**
  - **Scam Engineer:** "Is this a scam?" yorumları için en uygun format. Yorumdaki mesajı **kişisel bilgi olmadan** yeniden yaz. Numara, isim ve link asla gösterilmez. Kalıp: yorum çıkartması → "Here's the 4-sign check on it" → cevap → "Forward it to 7726."
  - **Centworks:** "Ya faiz düşerse?", "BNPL kredi notumu etkiler mi?" gibi sorular.
  - Bu Shortlar **S2 bağımsız Short takviminde** boş günleri doldurur. Kurallar aynı: ilk karede hareket, ≤6 kelime ekran metni, döngü kapanışı.
  - Gerçek yorum yoksa bu taktik bekler. Uydurma yorum kullanma.
- **Beklenen etki:** Konu bulma maliyeti sıfır. Yorumcu ve onun gibi düşünenler geri gelir. Yorum yazmayı teşvik eder.
- **Süre:** Short başına 20 dakika (TTS + kısa kurgu).

## 4) Haber tetiklemeli yeniden paketleme (eski videoya ikinci hayat)

- **Ne yapılır:** Eski bir videonun konusu yeniden gündeme gelince (yeni kesinti, aynı dolandırıcılığın yeni dalgası, yıl dönümü), o videonun başlığını ve küçük resmini **gündeme bağlayan** bir sürümle değiştir. Açıklamanın ilk satırına güncel bağlamı ekle. Video içeriği değişmez.
- **Nerede kanıtlandı:** YouTube stratejisti Paddy Galloway, Colin and Samir programında Tim Gabe'in eski bir videonun küçük resmini iyileştirdiğini, videonun günlük izlenmesinin yaklaşık **40 katına** çıktığını anlattı ([Colin and Samir – The New Rules of YouTube](https://www.colinandsamir.com/resources/the-new-rules-of-youtube-from-paddy-galloway)). Galloway'in genel ilkesi: paketleme (başlık + küçük resim) en büyük kaldıraç. **Güven: Düşük** (anekdot, rakamın birincil kaynağı görülemedi).
- **Fark (oyun kitabından):** `kucuk-resim-ab.md` rastgele zamanda A/B testi yapıyor. Burada değişiklik **bir olaya bağlı** ve olay sürerken yapılıyor.
- **Bizde nasıl (hazır tetikleyiciler):**
  | Tetikleyici | Video | Geçici başlık örneği |
  |---|---|---|
  | Avrupa'da büyük bir elektrik kesintisi | Spain blackout | "Spain Lost Power in Seconds. Could It Happen Again?" |
  | Büyük bir yazılım güncellemesi kesintisi | CrowdStrike | "One Update Broke 8.5 Million PCs. Here's Why It Keeps Happening" |
  | Bir bulut bölgesinin çökmesi | HS-04 / HS-06 | Olayın adı + "the same weak point" |
  | FTC/FBI yeni bir dolandırıcılık uyarısı | İlgili SE videosu | Uyarıdaki dolandırıcılık adı + "how it works" |
  | 28 Nisan 2027 (İspanya kesintisinin 2. yıl dönümü) | Spain blackout | "Spain's Blackout, Two Years On: Could It Happen Again?" (yalnızca videoda karşılığı varsa) |
- **Kural:** Başlık videonun gerçekten anlattığı şeyi vaat etmeli. Yeni olay hakkında videoda olmayan bir iddia başlığa konmaz. Olay geçince (≈2 hafta) en iyi performans gösteren başlığa dön.
- **Beklenen etki:** Değişmez; olaya göre. Kayıp riski çok düşük, eski başlık her zaman geri alınabilir.
- **Süre:** Olay başına 15 dakika (küçük resim için `arac/kucuk_resim/videolar.json`'a bir giriş ekle).

## 5) 48 saatte hızlı açıklama videosu

- **Ne yapılır:** Kanalın konusuna giren büyük bir olay olduğunda, tam belgesel yerine **4–6 dakikalık, kaynaklı, hızlı bir açıklama** videosu yayınla. Arama talebi olayın ilk günlerinde zirve yapar ve rakip video azdır.
- **Nerede kanıtlandı:** CrowdStrike kesintisinden (19 Temmuz 2024) sonraki günlerde "Some bad code just broke a billion Windows machines" başlıklı açıklama videosu bir istatistik sitesinde ~2,47 milyon izlenmeyle listeleniyor ([Social Counts](https://socialcounts.org/youtube-video-live-view-count/4yDm6xNeYas)). Bu video Fireship kanalına ait (kanal adı istatistik sayfasında görünmüyor, **yayından önce YouTube'da doğrula**). Fireship büyük bir kanal; küçük kanal için doğrudan kıyas değil. Mekanizma (olay anında arama talebi) her ölçekte geçerli. **Güven: Orta.**
- **Bizde nasıl:**
  - **Hidden Systems:** "Outage Files: Breaking" alt serisi. Tetikleyici: İngiltere veya ABD'de milyonlarca kişiyi etkileyen altyapı kesintisi. Şablon: 0:00 sonuç → 0:15 kimlik cümlesi → 0:35 soru → "ne biliyoruz / ne bilmiyoruz" → sistem açıklaması (eski videodan uyarlanır) → "resmi rapor gelince tam bölüm" vaadi.
  - **Scam Engineer:** FTC, FBI veya büyük bir operatörün yeni dolandırıcılık uyarısı. Şablon: uyarının kendisi → nasıl çalışıyor → tek kontrol.
  - **Kesin kural:** Sadece resmi açıklamalar ve güvenilir haber kaynakları. Kesinleşmemiş sebep "**şu an bilinen**" diye sunulur. Ölüm veya yaralanma olan olaylarda dramatize sahne yok. Tam belgesel geldiğinde hızlı video ile birbirine bağlanır.
  - Takvime etkisi: Haftalık uzun video yerine geçmez. O hafta bağımsız Short'lardan 2 tanesini düşür, yerine bunu yap.
- **Beklenen etki:** Tek videoda kanalın ortalamasının çok üstüne çıkma şansı en yüksek taktik. Olay yoksa hiçbir şey olmaz.
- **Süre:** Olay başına 1 gün (senaryo 2 saat, ses 30 dk, kurgu 4 saat).

## 6) Oynatma listesini "podcast" olarak ayarla

- **Ne yapılır:** Studio → **İçerik → Oynatma listeleri** → listenin menüsü → **Podcast olarak ayarla**. Liste YouTube Music'e de girer. Kullanıcılar podcast içeriğini Premium olmadan **arka planda** dinleyebilir ve indirebilir. youtube.com/podcasts'ta görünme ve podcast rozeti gelir.
- **Nerede kanıtlandı:** [YouTube Creators – Podcasts](https://www.youtube.com/creators/create/podcasts/), [Tubefilter (2023): YouTube Music'te podcast için ücretsiz arka plan dinleme](https://tubefilter.com/2023/04/28/youtube-music-audio-video-podcasts-free-background-listening/), [Podnews: İngiltere lansmanı](https://podnews.net/press-release/youtube-music-podcasts-uk). Podcast listesi izlenme süresine göre haftalık tabloda sıralanıyor ([Lindsey Gamble](https://www.lindseygamble.com/blog/youtube-launches-weekly-podcast-shows-chart-to-showcase-the-most-popular-podcasts)). **Güven: Orta** (özellik resmi, arka plan dinlemenin YPP saatine sayılıp sayılmadığı **doğrulanamadı**).
- **Bizde nasıl:**
  - **Hidden Systems "Outage Files":** Anlatım ağırlıklı, görsel olmadan da anlaşılıyor. İngiltere'de YouTube Music podcast desteği var; izleyicimizin %45'i İngiltere'de.
  - **Centworks "Money Mechanics":** Uygun. "What If…" ve "A vs B" grafik ağırlıklı, uygun değil.
  - **Scam Engineer:** Uygun değil. Ekrandaki mesaj örnekleri görsel olarak önemli.
  - **Dikkat:** Podcast listesine yalnızca tam bölümler girer. Short ve fragman koyma. Videolarda "as you can see on screen" gibi görsele dayanan cümleler azsa daha iyi dinlenir; yeni senaryolarda bunu gözet.
- **Beklenen etki:** Yeni bir keşif yüzeyi (YouTube Music, podcast sekmesi). Küçük ama sıfır maliyetli.
- **Süre:** 10 dakika, bir kez.

## 7) Videonun makale sürümü (ücretsiz web sitesi)

- **Ne yapılır:** Her videonun transkriptini (taktik 1'deki metin) başlıklar ve kaynak linkleriyle bir web sayfasına koy. Videoyu sayfanın en üstüne göm. Google'da "makale + video" olarak aranır.
- **Nerede kanıtlandı:** Practical Engineering (~4,7 M abone) sitesinde videoların blog sürümlerini yayınlıyor. Bazı yazılarda "this article is a transcript of the video embedded above" notu var ([practical.engineering blog örneği](https://practical.engineering/blog/2023/9/12/heavy-construction-of-a-sewage-pump-station-ep-2), [ooh.directory listesi](https://ooh.directory/blog/65zzj6)). **Güven: Düşük–Orta** (uygulama doğrulandı, trafiğe etkisi ölçülmedi).
- **Bizde nasıl:**
  - Ücretsiz barındırma: GitHub Pages (bu depo dışında **ayrı bir depo**). Kanal başına bir sayfa grubu.
  - **Önce Scam Engineer evergreen videoları:** "What to do if you clicked a link in a scam text" gibi sorular Google'da da aranıyor. Sayfanın en üstünde 4 adımlık özet kutusu, altında video, sonra metin.
  - Her sayfanın sonunda kanal linki ve "Watch the series" (taktik 2).
  - Kişisel bilgi, sahte yorum, reklam yok.
- **Beklenen etki:** Aylar içinde birikir. İlk ay neredeyse sıfır. Gömülü oynatmalar Studio'da "harici" trafik kaynağı olarak görünür; YPP saatine katkısını Analytics'te kontrol et (resmi teyit aranmadı).
- **Süre:** Kurulum yarım gün. Video başına 30 dakika.

## 8) Tek sayfalık PDF + e-posta listesi

- **Ne yapılır:** Videonun özünü tek sayfalık, yazdırılabilir bir kontrol listesine çevir. Açıklamadaki linkten e-posta karşılığında ücretsiz ver. Yeni video çıktığında listeye kısa bir e-posta gönder.
- **Nerede kanıtlandı:** İçerik üreticisi rehberleri, en kolay ve en çok dönüşüm getiren "lead magnet"in videoya özel tek sayfalık PDF kontrol listesi olduğunu söylüyor ([OptinMonster](https://optinmonster.com/how-to-build-an-email-list-for-your-youtube-channel), [Niche Pursuits](https://www.nichepursuits.com/how-to-build-an-email-list-from-youtube/), [Kit](https://convertkit.com/lead-magnet)). **Güven: Düşük.** Kaynakların çoğu e-posta aracı satan şirketler. Yüzsüz bir kanalın bu yolla büyüdüğüne dair bağımsız bir örnek bulunamadı.
- **Neden yine de listede:** Platformdan bağımsız tek kitle. Kanal politika sorunu yaşarsa (bkz. `oyun-kitabi/yapay-zeka-ve-politika.md`) izleyiciye ulaşmanın tek yolu. Sponsorlar e-posta listesine de değer veriyor.
- **Bizde nasıl:**
  - **Scam Engineer:** "The Scam Check Card": buzdolabına asılacak tek sayfa. 4 işaret (sürpriz, acele, yol, istek), "kapat ve kendin ara" kuralı, FTC/7726/IC3 bilgileri. 40+ kitle yazdırılabilir materyali paylaşır, aile içinde dolaşır.
  - **Centworks:** "Before You Swipe" kontrol listesi (BNPL vs kart sorusu, faiz değişince yapılacak 3 şey).
  - Araç: Kit veya beehiiv'in ücretsiz planı (limitleri kayıttan önce kontrol et).
  - **Kurallar:** Açık rıza, tek tıkla abonelikten çıkma, e-postada asla "kart numaranızı doğrulayın" benzeri bir istek yok (Scam kanalında güven her şey). Türkiye'den gönderim yapılsa da alıcılar ABD/İngiltere'de: CAN-SPAM ve UK PECR kurallarına uy.
- **Beklenen etki:** İlk aylarda liste küçük olur (onlarca kişi). Değer 6–12 ayda ortaya çıkar.
- **Süre:** Kurulum 1 gün. PDF başına 1 saat.

## 9) Shorts'u Facebook Reels'e de yükle

- **Ne yapılır:** Scam Engineer ve Centworks Shorts'larını **kendi orijinal dosyasından** (YouTube filigranı olmadan) Facebook Reels olarak da yükle. Açıklamada YouTube kanal adını yaz.
- **Nerede kanıtlandı:** Pew Research 2025: ABD'li yetişkinlerin %71'i Facebook kullanıyor. Facebook, her yaş grubunda çoğunluğun kullandığı iki platformdan biri. Günlük kullanım 50–64 yaşta **%54** ([Pew – Americans' Social Media Use 2025](https://www.pewresearch.org/internet/2025/11/20/americans-social-media-use-2025/), [Pew fact sheet](https://www.pewresearch.org/internet/fact-sheet/social-media/)). **Güven: Yüksek** (kitle verisi). **Orta** (Reels'ten YouTube'a abone geçişi ölçülmedi).
- **Bizde nasıl:**
  - **Scam Engineer:** En uygun kanal. 40+ kitle Facebook'ta. Dolandırıcılık uyarıları aile gruplarında paylaşılır.
  - **Centworks:** İkinci sırada.
  - **Hidden Systems:** Şimdilik hayır (İngiltere/belgesel kitlesi, Facebook önceliği düşük).
  - Bir Facebook sayfası aç (kişisel profil değil). Sayfa adı kanal adıyla aynı olsun.
  - Meta'nın orijinal içerik kurallarına uy: başka platformun filigranı olan video yükleme.
- **Beklenen etki:** Erişim artar. YouTube'a geçen izleyici oranı belirsiz. Ama marka tanınırlığı ve "bu kanal güvenilir" sinyali iki platformda birden oluşur.
- **Süre:** Short başına 5 dakika (aynı dosya, aynı metin).

## 10) Hype için hazırlık

- **Ne yapılır:** İzleyiciler, yayından sonraki **ilk 7 gün** içinde bir videoyu "Hype"layabilir. Her izleyicinin haftada 3 hype hakkı var ve ücretsiz. Puanlar haftalık bir sıralamaya girer; küçük kanalların hype'ı daha çok puan getirir. İlk 100 video Keşfet bölümünde görünür.
- **Kimlere açık:** YouTube Partner Program'daki, **500–500.000 abonesi** olan kanallar. Kanallar varsayılan olarak dahil. Ülke listesinde ABD, İngiltere ve Türkiye var. [YouTube Help – Hyping videos eligibility](https://support.google.com/youtube/answer/15509925), [Hype a video](https://support.google.com/youtube/answer/15333273), [Leaderboard](https://support.google.com/youtube/answer/15334500), [YouTube Blog – küresel genişleme](https://blog.youtube/news-and-events/hype-global-expansion/). **Güven: Yüksek** (kurallar). Etki için bağımsız veri yok.
- **Bizde nasıl:**
  - **Şu an uygun değiliz** (YPP yok). Bu yüzden 10. sırada. YPP'ye girildiği hafta (genişletilmiş YPP: 500 abone + 3.000 saat) aç.
  - Hazırlık: Sabit yoruma ve videonun son 20 saniyesine tek cümle: *"If this helped, a free Hype in the first week helps a small channel get found."* Yalnızca ilk 7 gün söylenir; sonra sabit yorumdan çıkarılır.
  - Hype istemek için ödül veya karşılık vaat etme.
- **Beklenen etki:** YPP sonrası en ucuz keşif kanalı. Sıralamaya girmek için gereken puanı bilmiyoruz.
- **Süre:** Video başına 2 dakika.

---

## Araştırıldı ama listeye alınmadı

| Taktik | Neden alınmadı | Kaynak |
|---|---|---|
| **Collab (ortak yazarlı video) özelliği** | Ağustos 2025'ten beri sınırlı bir test. Herkese açık değil. Açılırsa Hidden Systems ↔ küçük bir mühendislik kanalı denenebilir | [PPC Land](https://ppc.land/youtube-launches-collaboration-feature-for-creator-partnerships/), [eMarketer](https://www.emarketer.com/content/youtube-collab-feature-reshape-influencer-strategy) |
| **Canlı yayın soru-cevap** | Canlı yayın izlenme süresi YPP'ye sayılır ama yüzsüz ve TTS anlatımlı kanalda canlı ses yok. Metinle canlı yayın zayıf kalır | `gelir/4000-saat-plani.md` |
| **Başka kanalların Shorts'unu remix etme** | Kendi yorumumuz olsa da "yeniden kullanılan içerik" riskini artırır. Scam Engineer'da gerçek mağdur görüntüsü etik sorun | `oyun-kitabi/yapay-zeka-ve-politika.md` |

## Uygulama sırası (önerilen)

| Hafta | Yapılacak |
|---|---|
| 2–8 Kas | 1 (altyazı: ilk 4 video), 2 (liste içi linkler), 6 (podcast listeleri), 9 (Facebook sayfası + ilk 3 Reels) |
| 9–15 Kas | 3 (ilk gerçek yorumlara Short yanıt), 4 (tetikleyici listesi hazır; olay olunca uygula) |
| 16–29 Kas | 7 (Scam evergreen sayfaları), 8 (Scam Check Card PDF) |
| Olay olduğunda | 5 (48 saat videosu) ve 4 (eski videoyu yeniden paketle) birlikte |
| YPP sonrası | 10 (Hype) |
