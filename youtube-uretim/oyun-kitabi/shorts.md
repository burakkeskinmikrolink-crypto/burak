# 2. Shorts: izlemeye devam oranı, ilk kare, döngü, aktarım

**Durumumuz:** "Viewed" (izlemeye devam) %30, "swiped away" (kaydırıp geçme) %70.
**Anlamı:** Short'larımızın ilk 1–2 saniyesi akışta yeterince durdurucu değil. Bu metrik videonun geri kalanını değil, **yalnızca açılış anını** puanlıyor.

> Güven düzeyleri [giris-ve-elde-tutma.md](giris-ve-elde-tutma.md) dosyasındaki gibi tanımlı. Linkler bu oturumda açılamadı, yayın öncesi kontrol et.

---

## A. Metrik ve kıyaslar

| Bulgu | Kaynak | Güven |
|---|---|---|
| "Viewed vs swiped away", Short akışta gösterildiğinde izleyicinin izlemeyi mi yoksa kaydırmayı mı seçtiğini gösteren paydır. YouTube, sıralamada izlemeyi seçenlerin payını, ortalama izlenme süresini ve ortalama izlenme yüzdesini kullandığını belirtiyor. | [Metricool](https://metricool.com/youtube-shorts-algorithm/), [1of10](https://1of10.com/blog/youtube-shorts-analytics/) (YouTube açıklamasını aktararak) | Orta |
| YouTube bu metrik için resmî bir kıyas yayınlamıyor. Üçüncü taraf hedefler çelişkili: bir uzman %50 öneriyor, bir şirket %70–90 bandının en iyi sonuç verdiğini söylüyor. | [Retensis](https://retensis.com/blog/youtube-shorts-viewed-vs-swiped-away), [Grow Creator](https://growcreator.pro/blog/viewed-vs-swiped-away-youtube-shorts) | Düşük |
| Gösterim sayısı düşükken yüzde güvenilmez. | [1of10](https://1of10.com/blog/youtube-shorts-analytics/) | Orta |

**Hedefimiz:** Önce %30'dan **%45–50**'ye çıkmak. Bunun için her Short'ta ilk kareyi yeniden tasarlamak gerekiyor (aşağıda).

---

## B. İlk kare ve ilk 2 saniye

| Bulgu | Kaynak | Güven |
|---|---|---|
| İlk 1–3 saniye, izleyicinin kalıp kalmayacağını belirliyor. İlk kare, ses ve ekran yazısı birlikte bir "hook puanı" gibi çalışıyor. | [Versely](https://www.versely.studio/blog/viewed-vs-swiped-away-the-shorts-hook-gate) | Düşük-Orta |
| Tek bir vaka çalışmasında, ilk 100 ms içinde bir sonuç vaat eden ekran yazısı ile küçük bir jump-zoom, 3 saniyelik kalma oranını %54'ten %71'e çıkardı. | [ChatCut (Vidocu vakası)](https://chatcut.io/blog/how-to-make-youtube-shorts) | Düşük (tek vaka, satıcı) |

**Bizim Short'larımızdaki somut sorunlar** (shorts dosyalarını incelediğimde gördüklerim):
1. İlk kare çoğu zaman **statik bir görüntü** (siyah ekran ya da sabit fotoğraf). Hareket yok.
2. Ekran yazısı ile seslendirmenin ilk cümlesi **aynı şeyi söylemiyor**. Akışta izleyici çoğu zaman sesi kapalı geziniyor, ilk kare sessizde de anlaşılmalı.
3. İlk cümleler bazen bağlam kuruyor ("Here's a hidden system most people never think about"). İlk cümle doğrudan iddia ya da soru olmalı.

**İlk kare kuralları:**
- **0. kare:** Hareket halindeki bir görüntü (zoom-in, düşen kart, kararan harita) + en fazla 6 kelimelik büyük yazı + yazının birebir seslendirilmesi.
- **Yazı türü:** İddia ("THE PADLOCK ISN'T SAFETY"), soru ("$7.48 IN CASH?") ya da rakam çatışması ("$9B vs $12M").
- Logo, kanal tanıtımı, "wait for it" gibi ifadeler kullanma.
- İlk 2 saniye içinde **bir görsel değişim** olsun (jump-zoom ya da kesme).

---

## C. Döngü (loop) tekniği

| Bulgu | Kaynak | Güven |
|---|---|---|
| Döngüler ve tekrar izlemeler izlenme süresine sayıldığı için bir Short %100'ün üzerinde elde tutma gösterebilir. | [Teleprompter](https://www.teleprompter.com/blog/youtube-audience-retention), [Virvid](https://virvid.ai/blog/looping-structure-shorts-retention-2026) | Orta-Düşük |
| Son cümle, vedalaşma yerine ilk cümleye bağlanacak şekilde yazılmalı. | [Virvid](https://virvid.ai/blog/looping-structure-shorts-retention-2026) | Düşük |

**Uygulama:** Son cümle, ilk cümlenin öznesini soru ya da yarım cümle olarak geri getirsin.
Örnek (HS-04 Short 1): Sonu *"…test whether it starts."* olsun, Short da *"Because a generator that didn't start…"* diye açılsın. Döngü, izleyicinin fark etmeden ikinci tura girmesini sağlar.

**Not:** "Full story on the channel" gibi çağrılar döngüyü kırar. Bunun yerine Related Video bağlantısını kullan (aşağıda).

---

## D. Süre

| Bulgu | Kaynak | Güven |
|---|---|---|
| Shorts 15 Ekim 2024'ten beri 3 dakikaya kadar olabiliyor (kare veya dikey oranda). | [PetaPixel](https://petapixel.com/2024/10/04/youtube-shorts-expands-video-length-to-three-minutes/), [Tubefilter](https://www.tubefilter.com/?p=182474) (YouTube Blog'a atıfla) | Yüksek |
| Optimal süre konusunda kontrollü bir çalışma yok. Bloglar 30–45 sn öneriyor. 30 saniyenin altında ortalama izlenme ~%65, 30–60 sn aralığında ~%50 gibi rakamlar dolaşıyor. | [Prepublish](https://prepublish.ai/guides/youtube-shorts-retention), [Aibrify](https://aibrify.com/blog/youtube-shorts-retention-curve-playbook) | Düşük |

**Kararımız:** Bilgi yoğun Short'lar 30–40 sn, quiz formatı 20–30 sn olsun. Uzun Short'lar ancak "viewed" oranı %50'yi geçtikten sonra denenmeli.

---

## E. Short'tan uzun videoya izleyici aktarma

| Bulgu | Kaynak | Güven |
|---|---|---|
| Bir Short'a, kanaldaki uzun bir videoya, canlı yayına veya başka bir Short'a giden **tek bir "Related video" bağlantısı** eklenebilir. Bağlantı ekranın altında tek tıkla açılan bir buton olarak görünür (Ağustos 2023'te tüm üreticilere açıldı). | [Creator Insider (X)](https://x.com/YouTubeInsider/status/1696270150108856791), [vidIQ](https://vidiq.com/blog/post/youtube-related-links-connect-shorts-long-videos/) | Yüksek |
| YouTube Blog'un resmî rehberi, Shorts erişimini uzun video izlenmesine çevirmenin ilk adımı olarak Related Videos özelliğini gösteriyor. | [YouTube Blog – Related videos traffic guide](https://blog.youtube/creator-and-artist-stories/youtube-related-videos-traffic-guide/) | Yüksek |
| Tıklama oranı çok düşük olabilir. Bir tahmine göre bazı durumlarda %0,05 (10 milyon izlenmeli bir Short'tan ~3.000 uzun video izlenmesi). | [Subscribr](https://subscribr.ai/youtube-strategy/drive-traffic-shorts-to-long-videos) | Düşük |
| Ayda ~5 Short yayınlayan kanalların uzun videoları, genel ortalamadan %46 daha fazla izlenme alıyor (~800 bin videoluk analiz, nedensellik değil korelasyon). | [Metricool – YouTube Trends 2026](https://metricool.com/youtube-trends/) | Orta |
| Ölçüm: uzun videonun Reach → Traffic sources bölümündeki "YouTube Shorts" kaynağına bak. | [TubeMilestone](https://tubemilestone.com/blog/youtube-shorts-growth-strategy) | Orta |

**Uygulama:**
- Her Short'a **aynı konudaki** uzun videoyu Related Video olarak bağla. Shorts dosyalarında hangi ana videonun bağlanacağı dosya başlığında yazıyor.
- Short, uzun videonun **cevabını vermeyen** ama merakını açan bir parçası olsun. Şu anki Short'ların bir kısmı hikâyenin tamamını anlatıyor (örneğin HS-04 Short 2). Böyle bir Short izleyiciye uzun videoya gitmek için bir sebep bırakmaz.
- Ana videodan sonraki 7 gün içinde "YouTube Shorts" trafik kaynağını takip et.

---

## F. Yayın sıklığı

| Bulgu | Kaynak | Güven |
|---|---|---|
| Günlük ile haftalık yayını karşılaştıran kontrollü bir çalışma yok. Akademik bir arXiv çalışması yeni kanallarda Shorts yayın sıklığının zamanla azaldığını gözlemliyor ama hangisinin daha iyi olduğunu söylemiyor. | [arXiv 2403.00454](https://arxiv.org/pdf/2403.00454) | Yüksek (yöntem), ama soruya doğrudan cevap vermiyor |
| "Günlük yayın haftalığa göre 3–5 kat daha fazla dağıtım sağlar" iddiası verisiz. | [Virlo](https://virlo.ai/blog/how-often-to-post-youtube-shorts) | Düşük |
| Shorts RPM'i çok düşük (1.000 izlenme başına ~0,03–0,15 $). Shorts gelir için değil keşif için var. | [para-kazanma.md](para-kazanma.md) | Orta |

**Kararımız:** Her kanalda haftada **3–4 Short** yayınla. Bunlar o haftanın uzun videosuna bağlansın. Kaliteyi düşürecek günlük üretimden kaçın: Temmuz 2026'daki "inauthentic content" netleştirmesi, kalıplaşmış ve tekrarlayan içeriği hedefliyor ([yapay-zeka-ve-politika.md](yapay-zeka-ve-politika.md)).

---

## G. Yeni Short kontrol listesi
- [ ] İlk kare hareketli mi, yazı ≤6 kelime mi, yazı seslendirmeyle aynı mı?
- [ ] İlk cümle iddia, soru ya da rakam mı (bağlam kurmuyor mu)?
- [ ] Son cümle ilk cümleye bağlanıyor mu (döngü var mı)?
- [ ] Related Video olarak doğru uzun video seçili mi?
- [ ] Short, uzun videonun cevabını vermeden merak açıyor mu?
- [ ] Format bu hafta başka bir Short'ta kullanıldı mı (çeşitlilik)?
