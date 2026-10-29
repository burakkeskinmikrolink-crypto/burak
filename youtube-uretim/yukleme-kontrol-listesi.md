# Yükleme kontrol listesi (her uzun video ve her Short için)

**Neden var:** Kurallar 20'den fazla dosyaya dağılmıştı. Bu dosya, yükleme ekranında **sırayla** yapılacakları tek yerde topluyor. Her madde ilgili dosyaya bağlanıyor. Yazdır ya da yükleme sırasında yan pencerede aç.

> Studio menü adları zaman zaman değişir. Bir menüyü bulamazsan YouTube Yardım'da adını ara.

---

## A) Uzun video: yüklemeden önce (Salı–Perşembe)

- [ ] Senaryo `-v2.md` dosyasından. Doğrulama tablosundaki **"Orta"** ve **"kontrol et"** satırları yayın haftasında yeniden kontrol edildi (`dogrulama-turu.md`).
- [ ] Ses: Kokoro TTS. Duraklama ve telaffuz kuralları: `muzik-ve-ses.md`.
- [ ] Müzik: YouTube Ses Kitaplığı, konuşmanın altında doğru seviyede (`muzik-ve-ses.md`). Atıf isteyen parça ise atıf satırı açıklamaya eklendi.
- [ ] Görseller yalnızca Wikimedia / NASA ve ABD kamu arşivleri / Pexels / Pixabay. `arac/gorsel_kutuphane/` ile indirildi, `kaynaklar.txt` hazır.
- [ ] Gerçek kişi fotoğrafı, haber ajansı görseli, kurum logosu yok.
- [ ] Dramatize sahnelerde ekranda "Reconstruction" veya "Illustrative example" yazıyor.
- [ ] Küçük resimdeki nesne **ilk karede** görünüyor.
- [ ] Küçük resim A ve B: `arac/kucuk_resim/cikti/<ID>_A.png`, `<ID>_B.png`.
- [ ] Transkript: `python arac/altyazi/transkript.py <senaryo> -o arac/altyazi/cikti` (`gelir/hizli-kazanimlar.md` #1).

## B) Uzun video: yükleme ekranı (Studio)

**Ayrıntılar**
- [ ] **Başlık:** Senaryodaki 1. seçenek. Arama odaklı 3. seçenek Test & Compare için yedekte (`kucuk-resim-ab.md`).
- [ ] **Açıklama:** Senaryodaki "YouTube açıklaması" kod bloğu, olduğu gibi. Bölüm zaman kodları kurgudaki gerçek sürelere göre düzeltildi.
- [ ] **Küçük resim:** A. Yayın sonrası **Test & Compare** ile A/B/C (`kucuk-resim-ab.md`).
- [ ] **Oynatma listesi:** `kanal-sayfalari.md`'deki listeye eklendi.
- [ ] **Kitle:** **"Hayır, çocuklara özel değil"** (Made for kids: No). Üç kanalın kitlesi de yetişkin. Yanlış seçim yorumları ve bitiş ekranını kapatır.
- [ ] **Ücretli tanıtım:** Sponsor veya affiliate varsa **işaretli**. Yoksa boş. Kurallar: `gelir/reklam-disi-gelir.md`.
- [ ] **Değiştirilmiş veya sentetik içerik (Altered content):** Aşağıdaki karar kuralına göre.
- [ ] **Etiketler:** Senaryodaki "Etiketler" satırı.
- [ ] **Dil:** Video dili ve başlık/açıklama dili İngilizce. Hidden Systems: İngilizce (Birleşik Krallık). Centworks ve Scam Engineer: İngilizce (ABD).
- [ ] **Altyazı:** İngilizce transkript "zamanlama olmadan" yüklendi.
- [ ] **Kategori:** Hidden Systems → *Science & Technology*. Centworks → *Education*. Scam Engineer → *Education*.
- [ ] **Yorumlar:** Açık, moderasyon "Temel" veya üstü (`yorum-moderasyonu.md`).
- [ ] **Lisans:** Standart YouTube lisansı.

**Video öğeleri**
- [ ] **Bitiş ekranı (son 15–20 sn):** Senaryodaki "Bitiş ekranı" satırı + abone ol öğesi. Şablon: `marka-rehberi.md` → Bitiş ekranı.
- [ ] **Bilgi kartları:** Aşağıdaki kart planı tablosu.

**Görünürlük**
- [ ] **Premiere** olarak planla. Gün ve saat: README takvimi. Premiere kuralları: `gelir/4000-saat-plani.md` §2.4.

### "Değiştirilmiş veya sentetik içerik" karar kuralı
YouTube beyanı **gerçekçi** ve izleyicinin **gerçek bir kişi, yer veya olay sanabileceği** içerik için istiyor. Gerçek dışı içerik ve küçük düzenlemeler muaf. Beyan erişimi veya para kazanmayı kısıtlamıyor. Beyan edilmezse YouTube etiketi kendisi ekleyebilir. [YouTube Help – Disclosing altered or synthetic content](https://support.google.com/youtube/answer/14328491), [YouTube Blog](https://blog.youtube/news-and-events/disclosing-ai-generated-content). **Güven: Yüksek.**

| Durum | Beyan |
|---|---|
| Stok görüntü + arşiv fotoğrafı + grafik + TTS anlatım (standart videomuz) | **Gerekmiyor.** Anlatım sesi gerçek bir kişiyi taklit etmiyor, olay görüntüsü uydurulmuyor. TTS'nin tek başına beyan gerektirip gerektirmediği yardım sayfasında açık örnekle yazmıyor. Bu yüzden: **Güven: Orta** |
| Yapay zekâ ile üretilmiş, gerçek bir olayı gösteriyormuş gibi duran görüntü (ör. "kesinti anında veri merkezi" AI videosu) | **Gerekli.** Zaten kullanmıyoruz (`oyun-kitabi/yapay-zeka-ve-politika.md`) |
| Gerçek bir kişinin sesini veya yüzünü taklit eden ses/görüntü | **Gerekli** ve kanal kurallarına göre **yasak** |
| Otomatik dublaj | YouTube "auto-dubbed" etiketini kendisi koyar (`gelir/ceviri-ve-erisim.md`) |

> Emin değilsen beyan et. Beyan cezalandırılmıyor; beyansız yanıltıcı içerik cezalandırılıyor.

## C) Uzun video: yayından sonra (ilk 48 saat)

- [ ] Sabit yorum: `topluluk-ve-yorum.md`'deki metin. İçindeki "next video" linki **oynatma listesi içi link** (`gelir/hizli-kazanimlar.md` #2).
- [ ] Çeviriler: `ceviriler/<ID>.md` → ES, PT-BR, DE başlık ve açıklama (`gelir/ceviri-ve-erisim.md` §4).
- [ ] Önceki videolarda bu videoya **bilgi kartı** eklenecek yer var mı? Kart planı tablosunda "Sonradan ekle" sütunu.
- [ ] Shorts takvimi: Bu videonun 3 Short'u + bağımsız Shorts (README takvimi).
- [ ] Topluluk gönderisi: `topluluk-ve-yorum.md` haftalık plan.
- [ ] Facebook Reels (yalnızca Scam Engineer ve Centworks Shorts): `gelir/hizli-kazanimlar.md` #9.
- [ ] İlk 2 saatte gelen yorumlara yanıt ve kalp. "Is this a scam?" sorularını Short yanıt listesine ekle (`gelir/hizli-kazanimlar.md` #3).
- [ ] Cumartesi: `haftalik-analiz-sablonu.md`.

---

## D) Short: yükleme

- [ ] İlk kare hareketli. Ekran yazısı ≤6 kelime ve ilk VO cümlesiyle **birebir aynı**. Döngü kapanışı var. Kontrol: `arac/shorts_sablonlari/dogrula.py`.
- [ ] Başlık: Ekran yazısı + 1 arama kelimesi (ör. "Stores must take cash? #cashless").
- [ ] Açıklama: 1–2 cümle + kaynak (kurum adı) + hashtag'ler (dosyadaki).
- [ ] **Related video:** Dosyadaki "Related video bağlantısı" satırındaki uzun video. Bağımsız Shorts'ta konuya en yakın uzun video.
- [ ] Kitle: Çocuklara özel değil.
- [ ] Müzik: YouTube Ses Kitaplığı veya Shorts müzik kitaplığı. Telif talebi olan şarkı yok (otomatik dublaj ve para kazanmayı bozar).
- [ ] Ücretli tanıtım ve sentetik içerik: uzun videodaki kuralın aynısı.

---

## E) Bilgi kartı planı

**Kural:** Kart, senaryoda başka bir videodan bahsedilen ya da konunun doğal olarak başka bir videoya bağlandığı anda çıkar. Video başına en fazla 2 kart. Kart yalnızca **yayınlanmış** videoya bağlanabilir; hedef henüz yayınlanmadıysa "Sonradan ekle" sütununa bak. Zaman kodları senaryodaki bölüm başlıklarından; kurguya göre birkaç saniye kaydır.

| Video (yayın) | Kart 1 | Kart 2 | Sonradan ekle |
|---|---|---|---|
| HS-04 Google jeneratör (11 Kas) | 4:15 "Why losing one zone…" → CrowdStrike (yayınlanmış) | 1:55 "The batteries run down" → Deprem/telefon şebekesi (yayınlanmış) | 25 Kas sonrası: 4:15'teki kartı HS-06'ya çevir |
| HS-05 First Brands (18 Kas) | — (kanalda ilgili bir video yok) | — | Kart yok. Bitiş ekranı yeterli |
| HS-06 AWS ısınma (25 Kas) | 3:05 "One zone or many?" → HS-04 | — | — |
| HS-07 Bakır hat (2 Ara) | 0:45 "Why the old landline worked…" → Deprem/telefon şebekesi | 1:55 "The one-hour rule…" → Spain blackout | — |
| CW-03 Kuruş (7 Kas) | 3:15 "Can a store refuse your cash?" → "How banks create money" (yayınlanmış) | — | 5 Ara sonrası: 3:15'e CW-07 kartı |
| CW-04 Ödüller (14 Kas) | 6:45 "The three kinds of shoppers" → "Why card companies want you to pay late" | — | — |
| CW-05 Fed (21 Kas) | 2:00 "Branch 1" (kart faizi) → "Why card companies want you to pay late" | — | 28 Kas sonrası: CW-06 |
| CW-06 BNPL (28 Kas) | 0:45 "Round 1" → CW-04 (ödülleri kim ödüyor) | 3:15 "Round 3" → CW-05 (faiz) | — |
| CW-07 Nakit (5 Ara) | 3:18 "…the penny episode" → CW-03 | 4:17 "…the rewards episode" → CW-04 | — |
| SE-03 Otoyol SMS'i (11 Kas) | 3:10 "Your card in a digital wallet" → SIM swap (yayınlanmış; tek kullanımlık kodlar) | 0:45 "reply Y" → Caller ID spoofing (yayınlanmış) | — |
| SE-04 Medicare (18 Kas) | 0:45 "Why the screen says MEDICARE" → Caller ID spoofing | — | — |
| SE-05 Phantom Hacker (25 Kas) | 2:00 "Door 2: the bank calls" → Caller ID spoofing | 3:10 "Door 3" → SE-04 Medicare | — |
| SE-06 Sahte mağaza (2 Ara) | 2:00 "How the store found her" → SE-03 (link tuzakları) | — | Evergreen-04 yayınlanınca: 6:45 "If you already paid" → EV-04 |
| EV-01 Is this text a scam? | 1:55 "The 4 signs" → SE-03 | 5:30 "Report, delete, filter" → EV-03 | — |
| EV-02 SSN verdim | 1:55 "IdentityTheft.gov" → SIM swap | 6:35 "The checklist" → EV-04 | — |
| EV-03 Linke tıkladım | 0:45 "What a link really does" → EV-01 | 2:55 "Door 2" → EV-02 | — |
| EV-04 Para gönderdim | 2:55 "Bank transfer, Zelle" → SE-05 Phantom Hacker | 6:10 "Recovery scams" → `yorum-moderasyonu.md`'deki uyarı ile uyumlu sabit yorum | — |

> Yayınlanmış videoların (Spain blackout, CrowdStrike, deprem, geç ödeme, para yaratma, spoofing, SIM swap) gerçek süreleri depoda yok. Bu videolara **yeni videolara giden** kart eklerken zaman kodunu Studio'daki bölümlerden seç (S4: `yayinlanmis-video-iyilestirme.md`).
