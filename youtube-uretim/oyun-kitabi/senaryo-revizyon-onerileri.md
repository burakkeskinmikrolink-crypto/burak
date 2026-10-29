# 10. Senaryo revizyon önerileri

Bu dosya mevcut senaryoları [ozet-ve-kurallar.md](ozet-ve-kurallar.md) içindeki 15 kurala göre gözden geçiriyor. **Senaryo dosyalarında değişiklik yapılmadı.** Öneriler uygulanacaksa ilgili dosyada elle değiştirilmeli.

Öneri etiketleri: **[Kural n]** = ilgili kural. Öncelik: 🔴 yayından önce şart, 🟠 güçlü öneri, 🟢 iyileştirme.

---

## Tüm senaryolar için ortak bulgular

| Öncelik | Bulgu | Öneri |
|---|---|---|
| 🔴 [Kural 1] | 12 senaryonun hepsinde kimlik cümlesi var ("I work in a mobile network operations centre…", "I'm a telecom engineer…", "I spend my evenings reading Federal Reserve research…"). | Her kimlik cümlesinin **gerçek olduğunu** doğrula. Centworks ve Scam Engineer için gerçek insan sesiyle kayıt yap. TTS zorunluysa kimlik cümlesini çıkar. |
| 🔴 [Kural 2] | İlk merak sorusu tüm senaryolarda ~0:47–0:55 arasında. | Her senaryonun 3. sahnesini ~25–30 kelime kısalt ve ilk soruyu **0:35–0:40** aralığına taşı. Aşağıda senaryo bazında hangi cümlelerin çıkarılacağı yazıyor. |
| 🟠 [Kural 10] | Hepsi aynı iskeleti kullanıyor: şok → "By the end of this video…" → kimlik → reconstruction → soru her ~70 sn → "So, our questions…" kapanışı. | Kapanış kalıbını ("So, let's answer our questions / So, our questions…") en az yarısında değiştir. 5. ve 6. hafta senaryolarında farklı bir yapı kullan (aşağıda öneri var). |
| 🟠 [Kural 4] | Vaat cümleleri 18–25 kelime ve hepsi "By the end of this video, you'll know…" diye başlıyor. | ≤15 kelime ve farklı kalıplar kullan: "Stay to the end and you'll know…", "In eight minutes, you'll be able to spot…", "Here's the one switch that should have saved it." |
| 🟠 [Kural 3] | Bazı videolarda küçük resimdeki nesne ile ilk kare farklı (ayrıntılar aşağıda). | İlk karede küçük resimdeki nesneyi göster. |
| 🟢 [Kural 5] | Sahne tablolarında süre var ama görsel değişim sıklığı yok. | Her sahnenin görsel notuna "kesme sıklığı: 2–4 sn (ilk 30 sn), 4–6 sn (sonrası)" ekle. |

---

## Hidden Systems

### HS-04: Google Cloud Londra (`hidden_systems/04.md`)
- 🟠 **[Kural 3] İlk kare ile küçük resim uyuşmuyor.** Küçük resimde "GENERATOR NEVER STARTED" ve jeneratör var, ama ilk kare kart terminali "DECLINED". İki seçenek:
  - (a) Açılış 0–2 sn jeneratör ve "OFF", 2–5 sn kart terminali olsun.
  - (b) Küçük resmi "DECLINED" terminali + küçük bir jeneratör silueti olarak değiştir ve ikisini Test & Compare'de yarıştır.
- 🔴 **[Kural 2]** SAHNE 3'te "Commuters are tapping phones at barriers." ve "Taps again. Declined." cümlelerini çıkar. "And here's the thing — that should be a non-event." ifadesini kısalt. Böylece ilk soru ("how does a building designed around the certainty of power cuts…") ~0:38'e gelir.
- 🟠 **[Kural 4]** SAHNE 2'deki kimliği hikâyeye göm. Önerilen yeni metin: *"In my network control room, this is the failure we rehearse most."* (12 kelime)
- 🟢 Re-engagement ~3:15'te ("Why didn't the generators start?") ve ~5:40'ta (bölgesel bağımlılık) var, iyi.
- 🔴 Google'ın nihai raporu yayımlandıysa SAHNE 6'yı güncelle (mevcut not hâlâ geçerli).

### HS-05: First Brands (`hidden_systems/05.md`)
- 🟠 **[Kural 3]** Küçük resim "SOLD THE SAME INVOICE?" ve fatura kopyaları, ama ilk kare ATM fişi "12,000,000". İlk karede üçe ayrılan faturayı göster, rakamı ekran yazısı olarak ver.
- 🔴 **[Kural 2]** SAHNE 3'te "Not a delay. Not a bank holiday." cümlesini ve "Thirteen days later…" cümlesini birleştir. İlk soru ~0:40'a çekilir.
- 🟢 **[Kural 10]** Bu video "zaman çizelgesi" yapısına çok uygun (15 Eyl → 28 Eyl → Ocak → Mart → Ağustos). İskeleti değiştirmek için iyi bir aday: ekranda sürekli bir tarih şeridi kullan.
- 🟢 Kapanış cümlesi "The invoices behind them are now evidence." güçlü, koru.

### HS-06: AWS soğutma (`hidden_systems/06.md`)
- ✅ **[Kural 3]** Küçük resim (termometre) ile ilk kare (yükselen termometre) uyumlu.
- 🔴 **[Kural 2]** SAHNE 3'ün açılışındaki "on Thursday, the seventh of May 2026" tarihini ekran yazısına taşı ve sesten çıkar. "A few hundred miles away…" cümlesini kısalt. Soru ~0:40'a gelir.
- 🟠 **[Kural 7]** `shorts_06.md` Short 1'in sonundaki "Heat, not hackers. Full story on Hidden Systems." döngüyü kırıyor. Yerine *"…the only safe move is to switch off. Because every server is a heater."* yaz. Bu, ilk karedeki "EVERY SERVER IS A HEATER" yazısına bağlanır.
- 🟢 Quorum animasyonu (SAHNE 6) kanalın "mekanizma göster" dersinin iyi bir örneği ([rakip-analizi.md](rakip-analizi.md), Practical Engineering).

### HS-07: Küba (`hidden_systems/07.md`)
- 🟠 **[Kural 4]** İlk cümledeki "by one count" çekincesi hook'u zayıflatıyor. İlk cümleyi *"Cuba's whole power grid has collapsed seven times this year."* yap. 0:00–0:05'te ekranın altına küçük yazıyla "Count: UPI, Sep 2026" koy ve çekinceyi SAHNE 9'da sesli olarak ver. Doğruluk korunur, hook güçlenir.
- 🔴 **[Kural 2]** SAHNE 3'te "For many Cubans, this isn't shocking any more. It's familiar." cümlesini çıkar. İlk soru ~0:40'a gelir.
- 🟢 **[Kural 14]** Hastane ve su sahneleri grafik değil, uygun. Gerçek kişilerin yüzleri görünmesin (not mevcut).
- 🟢 SAHNE 8'deki İngiltere bağlantısı, İngiltere kitlesi için güçlü bir re-engagement. Bunu ~5:00'e çekmek düşünülebilir.

---

## Centworks

### CW-03: Kuruş (`centworks/03.md`)
- 🔴 **[Kural 1]** Kimlik cümlesi ("I spend my evenings reading Federal Reserve research…") bir persona gibi. Gerçek arka planına göre yeniden yaz ve gerçek sesle kaydet.
- 🟠 **[Kural 3]** Küçük resimde "$4.93 → $4.95?" fişi var, ilk kare dönen kuruş. İlk karede fişi göster: 4.93 üstü çizilip 4.95 oluyor. Kuruş ikinci kare olsun.
- 🔴 **[Kural 2]** SAHNE 3'te "This wasn't a one-off." paragrafını iki cümleye indir. Soru ("why did stores run out?") ~0:40'a gelir.
- 🔴 Common Cents Act'in imza durumu (mevcut not).
- 🟢 `shorts_03.md` Short 1 (quiz) formatı iyi. İlk karedeki "$7.48 · CASH · NO PENNIES" yazısı ile VO'nun ilk cümlesi uyumlu.

### CW-04: Kredi kartı ödülleri (`centworks/04.md`)
- 🟠 **[Kural 4]** İlk cümledeki "may be helping fund" ifadesi belirsiz. Kaynaklı ve somut bir şok cümlesi daha güçlü: *"Federal Reserve economists estimated cash-paying households hand about $149 a year to card users."* Kaynak Boston Fed 2010. Yılını ekranda göster.
- 🔴 **[Kural 2]** SAHNE 3'teki iki alışverişçi anlatımını 2 cümle kısalt. İlk soru ~0:38'e gelir.
- 🔴 Visa/Mastercard nihai onay durumu (mevcut not).
- 🟢 **[Kural 15]** Bu video ileride kredi kartı affiliate'i için cazip olabilir. **Yapma**, çünkü videonun tezi ödüllerin başkalarınca finanse edildiği. Bu güven çelişkisi yaratır.

### CW-05: Fed (`centworks/05.md`)
- 🟠 **[Kural 3]** Küçük resim "WHAT IF IT CONTINUES?" (merdiven), açılış ise "+$284/month". Küçük resmi "+$284/MONTH" + ev ikonu yap. "What if" ifadesi başlıkta kalsın (başlık ve küçük resim birbirini tamamlar).
- 🔴 **[Kural 2]** SAHNE 3'te "Three bedrooms, a yard, a school down the road." cümlesini çıkar. Soru ~0:40'a gelir.
- 🔴 Yayın haftasının Freddie Mac oranı ve Ekim TÜFE'si (mevcut not).
- 🟢 **[Kural 10]** "What if" formatı yapı çeşitliliği için iyi bir fırsat. Senaryoyu "Senaryo 1: Fed artırırsa / Senaryo 2: tutarsa / Senaryo 3: indirirse" diye üç dallı yapıya çevirmek iskeleti kırar.

### CW-06: BNPL vs kart (`centworks/06.md`)
- 🔴 **Takvim sorunu:** Video 28 Kasım (Cumartesi) yayında, ama metin *"It's Black Friday night"* ve *"this Black Friday"* diyor. 2026'da Black Friday 27 Kasım. İki seçenek:
  - (a) Yayını **24–25 Kasım**'a çek.
  - (b) Metni "Cyber Monday" (30 Kasım) ve "holiday shopping" olarak güncelle.
- 🟠 **[Kural 3]** Küçük resim "0% vs 21%?", açılış ise "%47 geç ödedi". Ya ilk karede iki butonu (0% / 21%) göster, ya da küçük resmi "47% PAID LATE" yap ve ikisini test et.
- 🔴 **[Kural 2]** SAHNE 3'te Jordan'ın aynı hafta aldığı ürün listesini tek cümleye indir. Soru ~0:40'a gelir.

---

## Scam Engineer

### SE-03: Otoyol SMS'i (`scam_engineer/03.md`)
- 🔴 **[Kural 1]** "I'm a telecom engineer…" cümlesi kanalın sloganıyla aynı. Gerçek olduğundan emin ol, gerçek sesle kaydet.
- ✅ **[Kural 3]** Küçük resim ("IT'S NOT THE $12") ile ilk kare ($12.51 mesajı) uyumlu.
- 🔴 **[Kural 2]** SAHNE 3'te Diane'in tanıtımını ("She's sixty-one, a retired teacher, and last week she drove…") tek cümleye indir. "Reply Y" sorusunu ~0:38'e çek.
- 🟠 iMessage'ın link davranışı Apple güncellemeleriyle değişmiş olabilir (mevcut doğrulama notu).
- 🟢 **[Kural 7]** Short 1 (quiz) sonundaki "Delete and report to 7726." iyi bir kapanış. Döngü için sonuna *"So… why do they want that Y?"* ekle.

### SE-04: Phantom Hacker (`scam_engineer/04.md`)
- 🟠 **[Kural 14]** SAHNE 3'teki *"A loud tone."* anlatımı ses efektine dönüşmesin. Kurguda yüksek alarm sesi kullanma, sadece görsel uyarı penceresi göster.
- 🔴 **[Kural 2]** SAHNE 3'te Frank'in tanıtımını kısalt ("He's sixty-eight, a retired machinist, and he's careful with money" yerine "Frank, sixty-eight, is careful with money."). İlk soru ~0:38'e gelir.
- 🟢 Bu video ebeveynlerle paylaşılabilir türde. Açıklamanın ilk satırına "Share this with a parent" koy (mevcut açıklamada var, ilk satıra taşı).

### SE-05: Sahte mağazalar (`scam_engineer/05.md`)
- 🟠 **[Kural 13/14]** İlk cümle *"…its web address was eleven days old"* kurgusal bir örnek ama gerçek bir olay gibi sunuluyor. 0:00'da ekrana küçük "Illustrative example" yazısı koy. Mevcut not "Temsilî" diyor, bunu ilk kareye taşı.
- 🔴 **[Kural 2]** SAHNE 3'te Carol'ın tanıtımını kısalt. İlk soru ~0:38'e gelir.
- 🟢 Takvim doğru: 25 Kasım, Black Friday'den önce.

### SE-06: Medicare (`scam_engineer/06.md`)
- 🟠 **[Kural 4]** Açık kayıt 7 Aralık'ta bitiyor. Başlığa ve küçük resme tarih ekle: *"…Before Dec 7"*. Aciliyet gerçek ve korku dili gerektirmiyor.
- 🔴 **[Kural 2]** SAHNE 3'teki "Her kitchen table is covered in plan brochures…" cümlesini kısalt. Soru ~0:40'a gelir.

---

## Shorts dosyaları

| Dosya | Sorun | Öneri |
|---|---|---|
| `hidden_systems/shorts_04.md` S1 | İlk kare yazısı ("ONE GENERATOR. ONE COUNTRY.") ile VO'nun ilk cümlesi farklı. [Kural 6] | Yazıyı VO ile eşitle: "A GENERATOR DIDN'T START." |
| `hidden_systems/shorts_04.md` S2 | Hikâyenin tamamını anlatıyor, uzun videoya merak bırakmıyor. [Kural 7] | *"And Google's final report still hasn't told us why."* cümlesi iyi bir merak kapanışı. Ondan sonra gelen "Full breakdown on Hidden Systems." cümlesini sil ve Related Video bağlantısına güven. |
| `hidden_systems/shorts_05.md` S1 | İlk cümle bağlam kuruyor ("Here's a hidden system most people never think about"). [Kural 6] | İlk cümle: *"This company owed nine billion dollars. Its shops never knew."* |
| `hidden_systems/shorts_06.md` S1 | "Full story on Hidden Systems" döngüyü kırıyor. [Kural 7] | Döngü cümlesi (HS-06 bölümünde). |
| `centworks/shorts_05.md` S2 | Rakam karşılaştırma formatı iyi. İlk kare statik. | İlk karede "$15" ile "$1,270" yan yana, ikincisi büyüyerek gelsin (hareket). |
| `centworks/shorts_06.md` S2 | İyi bir "veri bilmecesi". | Değişiklik gerekmiyor. Yayını Cyber Monday'e (30 Kasım) denk getir. |
| `scam_engineer/shorts_5-10_kasim.md` | Format döngüsü (quiz → hikâye → gerçek mi sahte mi) iyi. Ama bazı hikâyeler "Linda's phone was fine at lunch." gibi bağlamla açılıyor. [Kural 6] | Hikâye Short'larında ilk cümle sonuç olsun: *"Linda's phone said SOS. Her bank account was next."* (başlıkla aynı). |
| Tüm Scam Engineer Short'ları | Composite karakter uyarısı Short'un sonunda. | "Composite character" ibaresi ilk karede küçük yazıyla da görünsün. |

---

## 5. ve 6. haftalar için yapı önerileri (iskeleti kırmak için) [Kural 10]

| Kanal | Konu (konular.md) | Önerilen farklı yapı |
|---|---|---|
| Hidden Systems | İngiltere'nin bakır hat kapanışı (9 Ara) | **"Geri sayım" yapısı:** "31 January 2027: 63 days to go". Her bölüm bir gün veya bir saat. Ders kısmı arıza senaryosu üzerinden ilerlesin |
| Hidden Systems | Azure West US (16 Ara) | **"Dakika dakika" tek sahne:** Tüm video 5 saatlik kesintinin zaman çizelgesi, kimlik cümlesi sahnenin içinde |
| Centworks | What if America stopped using cash? (5 Ara) | **Üç dallı senaryo:** 1 yıl / 5 yıl / 20 yıl sonrası |
| Centworks | Gift card vs cash (12 Ara) | **"Yarışma" yapısı:** 5 tur (esneklik, kayıp riski, dolandırıcılık riski, hediye hissi, ekonomik kayıp). Skor tablosu ekranda kalsın |
| Scam Engineer | Ses klonu + kurye (9 Ara) | **Soru-cevap:** İzleyici yorumlarından ya da genel sorulardan 6 soru, her birine 60–80 saniyelik cevap |
| Scam Engineer | Hediye kartı boşaltma (16 Ara) | **"Mağazada 60 saniye" kontrol listesi:** Video, rafta kartı kontrol etme adımlarıyla ilerlesin |
