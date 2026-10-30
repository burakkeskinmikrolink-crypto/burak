# youtube-uretim: Üretim dosyaları (son hâl — 30 Ekim 2026)

> 📦 **Yükleme yaparken [`yukleme/`](yukleme/README.md) klasörünü kullan.** Her yayının başlığı, açıklaması, etiketleri, sabit yorumu, saati ve seslendirme metni orada hazır.

Üç İngilizce YouTube kanalı için senaryolar, Shorts, araçlar, gelir planı ve operasyon dosyaları. **Senaryo metinleri İngilizce, açıklamalar ve notlar Türkçe.**

| Kanal | Kitle | Yayın günü | Kimlik cümlesi |
|---|---|---|---|
| **Hidden Systems** (@collapse.stories) | İngiltere + ABD | Çarşamba | *This channel is made by someone who works inside a mobile network operations center.* |
| **Centworks** (@centworks) | ABD | Cumartesi | *This channel is made by an engineer, not a banker.* |
| **Scam Engineer** (@thescamengineer) | ABD, 40+ | Çarşamba | *This channel is made by a telecom engineer.* |

**Hazır olanlar:**
- **20 uzun senaryo:** 7 Kasım – 16 Aralık takvimi + 4 kalıcı (evergreen) video.
- **126 Short:** uzun video Shorts'ları + 60 bağımsız Short.
- **Her video için:** 2 küçük resim, 3 dilde çeviri, sabit yorum, bilgi kartı planı.
- **Her yayın için hazır yükleme paketi** (`yukleme/`, 126 paket) ve Kokoro'ya hazır seslendirme metni.
- **6 araç**, hepsi testli.
- **Gelir planı** ve **kanal operasyon dosyaları.**

> **Kural:** Yayına giren sürüm her zaman **`-v2.md`** dosyasıdır. v1 dosyaları (`04.md` vb.) yalnızca doğrulama tablosu için durur.

---

## 📦 Yükleme sırasında bu klasörü kullan: [`yukleme/`](yukleme/README.md)

**Her yayın için hazır bir paket var** (13 Aralık'a kadar: 16 uzun video + 110 Short = **126 paket**). Klasör adı: `yukleme/<YYYY-MM-DD>_<kanal>_<başlık>/`. İçinde:

| Dosya | Studio'da nereye |
|---|---|
| `baslik.txt` / `baslik_alternatifleri.txt` | Başlık / Test & Compare |
| `aciklama.txt` | Açıklama (bölümler, kaynaklar, en sonda *"Narration uses a synthetic voice."*) |
| `etiketler.txt` | Etiketler |
| `sabit_yorum.txt` | İlk yorum → Sabitle |
| `ilgili_video.txt` | Short → İlgili video |
| `yayin_zamani.txt` | Planla / Premiere (İstanbul saati; Londra ve New York karşılığı yanında) |
| `kucuk_resim.txt` | Küçük resim dosyasının yolu (A yükle, B test) |
| `seslendirme.txt` + `seslendirme_ayar.txt` | Kokoro'ya verilecek temiz anlatım metni ve hazır komut |

**Yayın saatleri (İstanbul):**
- Uzun videolar **21:00** (= 18:00 Londra / 13:00 New York).
- Hidden Systems Short'ları **21:30** (İngiltere akşamı).
- Centworks ve Scam Engineer Short'ları **20:00** (New York öğleni).
- Aynı gün ikinci bir Short varsa sonraki saate kayar.
- Saatlerin gerekçesi: `oyun-kitabi/buyume-taktikleri.md` §C.

**Kural:**
- Paketler `python arac/yukleme_paketi/paketle.py` ile **otomatik üretilir**.
- Bir şeyi düzelteceksen kaynak `.md` dosyasını düzelt ve betiği yeniden çalıştır. Paketi elle düzenleme; bir sonraki çalıştırmada silinir.
- Yayınlanmış videoların gerçek başlıklarını, SE-07 linkini ve seçtiğin Kokoro seslerini **bir kez** `arac/yukleme_paketi/ayarlar.json` dosyasına yaz. Betiği çalıştırınca ⚠️ işaretli 34 paket kendiliğinden dolar.

---

## 🔰 Salı günü (3 Kasım) üretime başlarken okunacak sıra

İlk yayınlar: **Perşembe 5 Kasım**'da Scam Engineer Shorts serisi, **Cumartesi 7 Kasım**'da Centworks ilk uzun video. Salı ve Çarşamba bunlar için hazırlık günleri.

### A) Önce oku (≈ 45 dk, bir kez)
| Sıra | Dosya | Neden | Süre |
|---|---|---|---|
| 1 | **Bu README** | Takvim, paket klasörü, harita | 10 dk |
| 2 | [`yukleme/README.md`](yukleme/README.md) | 126 yayının tarih/saat sıralı listesi; ⚠️ olanlar doldurulacak | 5 dk |
| 3 | [`gelir/ypp-esik-dogrulama.md`](gelir/ypp-esik-dogrulama.md) | **8.000 saat kuralı resmi** (1 Şubat 2027'den itibaren yeni başvurular). Hedefimiz bu | 5 dk |
| 4 | [`dogrulama-turu.md`](dogrulama-turu.md) §4 | 7 açık madde ve hangi videodan önce bakılacağı | 5 dk |
| 5 | [`eksik-analizi.md`](eksik-analizi.md) §3 | Senin yapman gereken işler | 5 dk |
| 6 | [`yukleme-kontrol-listesi.md`](yukleme-kontrol-listesi.md) §B ve §E | Studio ayarları (çocuklara özel değil, sentetik içerik kuralı) ve bilgi kartları. Metin alanları artık paketten geliyor | 10 dk |
| 7 | [`muzik-ve-ses.md`](muzik-ve-ses.md) §1–2 | Müzik seçimi ve seviyeler (seslendirme metni paketlerde hazır) | 5 dk |

### B) Salı yapılacaklar (≈ 2 saat)
1. **`arac/yukleme_paketi/ayarlar.json`'u doldur:**
   - Yayınlanmış 7 videonun gerçek başlıkları.
   - Seçtiğin 3 Kokoro sesi (önce aşağıdaki 2. adım).
   - Sonra `python arac/yukleme_paketi/paketle.py`.
   - ~15 dk.
2. **Ses seçimi:**
   - `muzik-ve-ses.md` §3.1'deki test paragrafını her kanal için 2–3 Kokoro sesiyle dinle, birer ses seç.
   - `arac/seslendirme/telaffuz.json`'a göz at.
   - ~30 dk.
3. **Moderasyon:** [`yorum-moderasyonu.md`](yorum-moderasyonu.md) §1–2 (en önemlisi Scam Engineer). ~20 dk.
4. **Kanal sayfaları:**
   - [`kanal-sayfalari.md`](kanal-sayfalari.md): Hakkında metni, oynatma listeleri (şimdi oluştur), fragman.
   - Çeviriler: [`ceviriler/kanal-hakkinda.md`](ceviriler/kanal-hakkinda.md).
   - ~40 dk.
5. **Yayınlanmış videolar:**
   - [`yayinlanmis-video-iyilestirme.md`](yayinlanmis-video-iyilestirme.md): açıklama, etiket, sabit yorum. Bölüm zamanlarını doldur.
   - [`kucuk-resim-ab.md`](kucuk-resim-ab.md): Test & Compare.
   - ~30 dk.

### C) İlk 10 günün üretim sırası (paket klasörleriyle)
| Bitiş | Ne üretilecek | Paketler (`yukleme/…`) |
|---|---|---|
| **Çar 4 Kas** | Scam Engineer 6 Short (5–10 Kas) | `2026-11-05_scam-engineer_short-*` … `2026-11-10_scam-engineer_short-*` |
| **Cum 6 Kas** | CW-03 uzun video + 3 Short | `2026-11-07_centworks_america-killed-the-penny-*`, `2026-11-08/10/12_centworks_short-*` |
| **Pzr 8 Kas** | Bağımsız Shorts Hafta 1 (üç kanal, 12 Short) | `2026-11-09` … `2026-11-15` arası `short-*` klasörleri |
| **Pzt 9 Kas** | HS-04 ve SE-03 uzun videolar + Shorts | `2026-11-11_hidden-systems_the-generator-*`, `2026-11-11_scam-engineer_the-unpaid-toll-*` ve 12/14/16 Kasım Short'ları |
| **Per 12 Kas** | CW-04 + Bağımsız Shorts Hafta 2 | `2026-11-14_centworks_who-really-pays-*` ve 16–22 Kasım Short'ları |

### D) Her yayın için iş akışı (paket klasörüyle)
1. **Kontrol:** Senaryonun ⚠️ satırı ve `dogrulama-turu.md` (yayından 3 gün önce). Değişiklik varsa `.md`'yi düzelt → `paketle.py`'yi tekrar çalıştır.
2. **Ses:** Paketteki `seslendirme_ayar.txt` içindeki komutu çalıştır → `ses.wav` paket klasörüne düşer. Önce `--plan` ile duraklamalara bak.
3. **Görsel:** `python -m gorsel_kutuphane ara/indir/klip` (senaryodaki sahne notlarına göre) → `kaynaklar.txt`.
4. **Miks:** `muzik-ve-ses.md` §1–2 (−14 LUFS, müzik konuşmanın ~20 dB altında).
5. **Altyazı:** `python arac/altyazi/transkript.py <senaryo> -o arac/altyazi/cikti` (uzun videolar).
6. **Yükleme:**
   - Paketteki dosyaları Studio alanlarına kopyala.
   - Studio ayarları ve bilgi kartları için `yukleme-kontrol-listesi.md`.
   - Zamanlama için `yayin_zamani.txt`.
7. **Yayın sonrası:**
   - `sabit_yorum.txt` → yorum yaz ve sabitle.
   - Çeviriler `ceviriler/<ID>.md`.
8. **Cumartesi:** `haftalik-analiz-sablonu.md`. **13 Aralık karar kuralı** buradan işler.

---

## 📅 Yayın takvimi

| Tarih | Gün | Kanal | Uzun video | Shorts | Shorts günleri |
|---|---|---|---|---|---|
| 5–10 Kas | Per–Sal | Scam Engineer | — (yayınlanmış spoofing ve SIM swap videolarına trafik) | `scam_engineer/shorts_5-10_kasim-v2.md` | 5, 6, 7, 8, 9, 10 Kas |
| **7 Kas** | Cmt | Centworks | `centworks/03-v2.md` Kuruşun sonu ve nakit yuvarlama | `centworks/shorts_03-v2.md` | 8, 10, 12 Kas |
| **11 Kas** | Çar | Hidden Systems | `hidden_systems/04-v2.md` Google Cloud Londra, çalışmayan jeneratör | `hidden_systems/shorts_04-v2.md` | 12, 14, 16 Kas |
| **11 Kas** | Çar | Scam Engineer | `scam_engineer/03-v2.md` "Unpaid toll" SMS'i | senaryo içinde | 12, 14, 16 Kas |
| **14 Kas** | Cmt | Centworks | `centworks/04-v2.md` Kredi kartı ödüllerini kim ödüyor? | `centworks/shorts_04-v2.md` | 15, 17, 19 Kas |
| **18 Kas** | Çar | Hidden Systems | `hidden_systems/05-v2.md` First Brands | `hidden_systems/shorts_05-v2.md` | 19, 21, 23 Kas |
| **18 Kas** | Çar | Scam Engineer | `scam_engineer/04-v2.md` Medicare aramaları (açık kayıt 7 Ara'da biter) | senaryo içinde | 19, 21, 23 Kas |
| **21 Kas** | Cmt | Centworks | `centworks/05-v2.md` What if the Fed keeps raising rates? | `centworks/shorts_05-v2.md` | 22, 24, 26 Kas |
| **25 Kas** | Çar | Hidden Systems | `hidden_systems/06-v2.md` AWS us-east-1 soğutma arızası | `hidden_systems/shorts_06-v2.md` | 26, 28, 30 Kas |
| **25 Kas** | Çar | Scam Engineer | `scam_engineer/05-v2.md` Phantom Hacker (Şükran Günü arifesi) | senaryo içinde | 26, 28, 30 Kas |
| **28 Kas** | Cmt | Centworks | `centworks/06-v2.md` BNPL vs kredi kartı (Black Friday) | `centworks/shorts_06-v2.md` | 29, 30 Kas, 2 Ara |
| **2 Ara** | Çar | Hidden Systems | `hidden_systems/07-v2.md` İngiltere bakır hat kapanışı | `hidden_systems/shorts_07-v2.md` | 3, 5, 7 Ara |
| **2 Ara** | Çar | Scam Engineer | `scam_engineer/06-v2.md` Sahte online mağazalar | senaryo içinde | 3, 5, 7 Ara |
| **5 Ara** | Cmt | Centworks | `centworks/07-v2.md` What if America stopped using cash? | `centworks/shorts_07-v2.md` | 6, 8, 10 Ara |
| **9 Ara** | Çar | Hidden Systems | `hidden_systems/08-v2.md` Winter Storm Elliott, Noel arifesinde planlı kesinti | `hidden_systems/shorts_08-v2.md` | 10, 12, 14 Ara |
| **9 Ara** | Çar | Scam Engineer | `scam_engineer/07-v2.md` Hediye kartı boşaltma + sahte kargo SMS'i | senaryo içinde | 10, 12, 14 Ara |
| **12 Ara** | Cmt | Centworks | `centworks/08-v2.md` Gift card vs cash | `centworks/shorts_08-v2.md` | 13, 15, 17 Ara |
| 13 Ara | Pzr | **Hepsi** | **Karar günü** (`haftalik-analiz-sablonu.md`) | — | — |
| 16 Ara | Çar | Hidden Systems | Karardan sonra; konu Azure West US (`konular.md`) | — | — |
| 16 Ara | Çar | Scam Engineer | Öneri: `scam_engineer/evergreen-04.md` (para gönderdim) | senaryo içinde | 17, 19, 21 Ara |

**Kalıcı (evergreen) videolar** `scam_engineer/evergreen-01..04.md`: takvimdeki boş Scam Engineer haftalarına. **Yedek:** `hidden_systems/yedek-kuba.md` (politik hassasiyet nedeniyle takvim dışı).

### 📱 Bağımsız Shorts (9 Kasım – 13 Aralık, 60 Short)
Kanal başına haftada 4. Uzun video Short'larının **çıkmadığı** günlere yerleştirildi. Related video her zaman o gün yayınlanmış bir videoya bağlanır.

| Hafta | Hidden Systems | Centworks | Scam Engineer |
|---|---|---|---|
| 1 (9–15 Kas) | 9, 10, 11, 13 | 9, 11, 13, 14 | 11, 13, 14 (akşam), 15 |
| 2 (16–22 Kas) | 17, 18, 20, 22 | 16, 18, 20, 21 | 17, 18, 20, 22 |
| 3 (23–29 Kas) | 24, 25, 27, 29 | 23, 25, 27, 28 | 24, 25, 27, 29 |
| 4 (30 Kas–6 Ara) | 1, 2, 4, 6 | 1, 3, 4, 5 | 1, 2, 4, 6 |
| 5 (7–13 Ara) | 8, 9, 11, 13 | 7, 9, 11, 12 | 8, 9, 11, 13 |

Dosyalar: `<kanal>/shorts-bagimsiz-hafta-<n>.md`.

---

## 🗺️ Dosya haritası

### Kök klasör
| Dosya | Ne işe yarar |
|---|---|
| `README.md` | Bu dosya: takvim, harita, Salı okuma sırası |
| `yukleme/` | **Yükleme paketleri** (otomatik üretilir): her yayın için bir klasör + tarih sıralı `yukleme/README.md` |
| `konular.md` | 6 haftalık konu planı (S3 ile kayan konular ➡️ ile işaretli) |
| `eksik-analizi.md` | Kanal × 8 başlık durum tablosu, kapatılan eksikler, senin yapman gerekenler, şeffaflık kararı |
| `dogrulama-turu.md` | 30 Ekim doğrulama turu: 7 düzeltme, 1 yeni gelişme, 15 doğrulama, 7 açık madde |
| `marka-rehberi.md` | Kimlik tablosu, renk kodları, yazı tipi, kapanışlar, yasak kelimeler, bitiş ekranı, banner ve filigran |
| `yukleme-kontrol-listesi.md` | Studio yükleme sırası (uzun video + Short), sentetik içerik kuralı, 20 video için bilgi kartı planı |
| `muzik-ve-ses.md` | Ses Kitaplığı, müzik profili, seviyeler (−14 LUFS), Kokoro: SSML yok, `[pause]`/`[slow]` işaretleri |
| `yorum-moderasyonu.md` | Moderasyon ayarları, engellenen kelimeler, sahte "kurtarma uzmanı" yanıtları, taklitçi hesaplar |
| `kanal-sayfalari.md` | Fragman senaryoları, Hakkında metinleri, oynatma listeleri, kanal anahtar kelimeleri |
| `topluluk-ve-yorum.md` | Her video için sabit yorum + Kasım–Aralık haftalık topluluk gönderileri |
| `yayinlanmis-video-iyilestirme.md` | Yayınlanmış 4 uzun video + 4 Short için yapıştırmaya hazır açıklama, etiket, sabit yorum, liste |
| `kucuk-resim-ab.md` | Yayınlanmış 4 video için küçük resim ve başlık A/B planı |
| `haftalik-analiz-sablonu.md` | Cumartesi metrik tablosu ve 13 Aralık karar kuralı |

### `hidden_systems/` (İngiliz yazımı)
| Dosya | İçerik |
|---|---|
| `04-v2.md` … `08-v2.md` | **Yayın senaryoları:** HS-04 Google jeneratör · HS-05 First Brands · HS-06 AWS ısınma · HS-07 bakır hat · HS-08 Winter Storm Elliott |
| `shorts_04-v2.md` … `shorts_08-v2.md` | Her videonun 3 Short'u |
| `shorts-bagimsiz-hafta-1..5.md` | 20 bağımsız Short (50 Hz, TV pickup, Facebook BGP, Knight Capital, Teksas 4:37, Heathrow…) |
| `04.md`, `05.md`, `06.md`, `shorts_0x.md` | v1 + doğrulama tabloları (referans) |
| `yedek-kuba.md`, `yedek-kuba-shorts.md` | Yedek video |

### `centworks/` (Amerikan yazımı)
| Dosya | İçerik |
|---|---|
| `03-v2.md` … `08-v2.md` | **Yayın senaryoları:** CW-03 kuruş · CW-04 ödüller · CW-05 Fed · CW-06 BNPL · CW-07 nakitsiz Amerika · CW-08 hediye kartı vs nakit |
| `shorts_03-v2.md` … `shorts_08-v2.md` | Her videonun 3 Short'u |
| `shorts-bagimsiz-hafta-1..5.md` | 20 bağımsız Short (72 kuralı, FICO %35, FDIC 250 bin $, 2 $ banknot…) |
| `03.md` … `06.md`, `shorts_0x.md` | v1 + doğrulama tabloları |

### `scam_engineer/` (Amerikan yazımı, sakin ton)
| Dosya | İçerik |
|---|---|
| `03-v2.md` … `07-v2.md` | **Yayın senaryoları** (Shorts içinde): SE-03 otoyol SMS'i · SE-04 Medicare · SE-05 Phantom Hacker · SE-06 sahte mağaza · SE-07 hediye kartı + kargo SMS'i |
| `evergreen-01.md` … `evergreen-04.md` | Kalıcı arama videoları: "Is this text a scam?" · SSN verdim · linke tıkladım · para gönderdim |
| `shorts_5-10_kasim-v2.md` | 5–10 Kasım Shorts serisi |
| `shorts-bagimsiz-hafta-1..5.md` | 20 bağımsız Short (quiz / kısa hikâye / gerçek mi sahte mi döngüsü) |
| `03.md` … `06.md`, `shorts_5-10_kasim.md` | v1 + doğrulama tabloları (dosya adları yeni sıraya göre: 04 = Medicare, 05 = Phantom, 06 = mağaza) |

### `gelir/`
| Dosya | İçerik |
|---|---|
| `reklam-disi-gelir.md` | Affiliate programları, Türkiye'den ödeme alma (CJ + Payoneer), FTC/ASA kuralları, şablonlar |
| `ypp-esik-dogrulama.md` | **YPP eşik doğrulaması (30 Ekim 2026):** 8.000 saat / 20 milyon Shorts kuralı 1 Şubat 2027'den itibaren yeni başvurular için resmi; bugün 4.000 geçerli; 500 abone kademesi değişmedi |
| `4000-saat-plani.md` | İzlenme saati hesabı, **1 Şubat 2027 eşik değişikliği uyarısı**, haftalık hedefler |
| `arama-icerigi-scam.md` | 15 kalıcı arama konusu (ilk 4'ü yazıldı) |
| `ceviri-ve-erisim.md` | Çok dilli başlık/açıklama, çoklu ses, otomatik dublaj: kimlere açık, politika notu |
| `hizli-kazanimlar.md` | 10 yeni taktik (altyazı, liste içi link, yoruma Short ile yanıt, 48 saat videosu, podcast, Facebook Reels, Hype…) |
| `q4-firsati.md` | Q4 reklam fiyatı ve Ocak düşüşü, tatil konuları |
| `pdf-icerikleri.md` | E-posta listesi için "Scam Check Card" ve "Before You Swipe" metinleri |

### `ceviriler/`
| Dosya | İçerik |
|---|---|
| `HS-0x.md`, `CW-0x.md`, `SE-0x.md`, `EV-0x.md` | 20 planlanmış video: ES, PT-BR, DE başlık + açıklama (Studio'ya yapıştır) |
| `P-*.md` | 7 yayınlanmış video (başlık, özet, kaynaklar) |
| `kanal-hakkinda.md` | 3 kanalın Hakkında metni, 3 dilde |
| `_veri.py`, `_uret.py` | Çeviri verisi ve üretici: `python ceviriler/_uret.py` |

### `oyun-kitabi/` (araştırma, Türkçe)
`ozet-ve-kurallar.md` (**başlangıç**: en etkili 15 kural) · `giris-ve-elde-tutma.md` · `shorts.md` · `baslik-ve-kucuk-resim.md` · `rakip-analizi.md` · `yapay-zeka-ve-politika.md` · `gorsel-ve-ses.md` (SSML kısmı Kokoro için geçersiz, bkz. `muzik-ve-ses.md`) · `buyume-taktikleri.md` · `para-kazanma.md` · `senaryo-revizyon-onerileri.md`

### `arac/` (Python araçları, hepsi testli)
| Klasör | Ne yapar | Çalıştır | Test |
|---|---|---|---|
| `gorsel_kutuphane/` | Wikimedia/NASA/Pexels/Pixabay arama, lisans filtresi, atıf metni, Ken Burns ve parallax klip (16:9 + 9:16), `kaynaklar.txt` | `python -m gorsel_kutuphane ara/indir/klip/kaynaklar` (Windows kurulumu klasör README'sinde, anahtarlar `.env`) | 45 |
| `shorts_sablonlari/` | 3 Short formatının JSON şeması, şablonlar, örnekler, doğrulayıcı | `python dogrula.py ornekler/*.json` | 11 |
| `kucuk_resim/` | 20 video × A/B küçük resim (1280×720) + telefon önizlemesi | `python uret.py` → `cikti/` (62 PNG) | 9 |
| `altyazi/` | Senaryodan altyazı transkripti ("zamanlama olmadan" yükleme) | `python transkript.py <senaryo> -o cikti` | 4 |
| `seslendirme/` | Senaryodan veya paketteki `seslendirme.txt`'den Kokoro seslendirme: `[pause]`, `[slow]`, otomatik sessizlikler, `telaffuz.json` | `python seslendir.py <senaryo.md veya seslendirme.txt> --plan` veya `-o x.wav --dil b --ses <ses>` | 7 |
| `yukleme_paketi/` | Tüm `-v2` senaryo ve Short dosyalarından `yukleme/` paketlerini üretir (başlık, açıklama + sentetik ses satırı, etiketler, sabit yorum, ilgili video, İstanbul yayın saati, küçük resim yolu, işaretli seslendirme metni). Gerçek başlıklar ve sesler için `ayarlar.json` | `python arac/yukleme_paketi/paketle.py` (`--son 2026-12-31` ile daha ileri) | 8 |

---

## 📏 Tüm senaryolarda geçerli kurallar (özet)
- **İlk cümle** en çarpıcı sonuç. Tarih ya da selamla açılış yok.
- **Vaat** ilk 15 sn içinde. **Kimlik cümlesi** 0:12–0:20 arasında, birinci tekil şahıs yok.
- **İlk merak sorusu** en geç 0:35–0:40'ta, sonra her 60–90 sn'de bir. **0:45'ten önce arka plan bilgisi yok.**
- **Uzunluk:** 7–9 dk, ~1.100–1.350 kelime.
- **Sahne biçimi:** `[SAHNE n | görsel | süre]`.
- **Küçük resmin ana nesnesi** ilk sahnede görünür.
- **Görseller** yalnızca Wikimedia, NASA/ABD kamu arşivleri, Pexels, Pixabay. Gerçek kişi, logo ve ajans fotoğrafı yok. Dramatize sahnede "Reconstruction / Composite character".
- **Shorts:**
  - İlk kare hareketli.
  - Ekran yazısı ≤6 kelime ve ilk VO cümlesiyle birebir aynı.
  - Döngü kapanışı.
  - Açıklamada "Related video bağlantısı".
  - Scam Engineer'da format döngüsü: quiz / kısa hikâye / gerçek mi sahte mi.
- **Her iddiaya kaynak.** Doğrulanamayan iddia yazılmaz; "Orta" olanlar senaryo tablosunda işaretli.

## ⚠️ Yayından önce
1. **Açık maddeler:** [`dogrulama-turu.md`](dogrulama-turu.md) §4. Bunlar: Google nihai raporu, First Brands duruşması, AWS raporu, Common Cents Act imzası, Visa/Mastercard nihai onayı ve Reg II kararı, Payment Choice Act, Bankrate 2025.
2. **Linkleri bir kez aç.** Bu çalışmada doğrudan sayfa açma engelliydi. İddialar arama özetleriyle ve birden fazla kaynakla doğrulandı.
3. **Ses kararı:** Centworks ve Scam Engineer için gerçek insan sesi daha düşük politika riski taşır (`oyun-kitabi/yapay-zeka-ve-politika.md`). TTS kullanılacaksa şeffaflık cümlesi için `eksik-analizi.md` §4.
4. **Yayınlanmış videoların gerçek başlık ve süreleri depoda yok.** Bunlara bağlanan dosyalarda (`yayinlanmis-video-iyilestirme.md`, `ceviriler/P-*.md`, `shorts_5-10_kasim-v2.md`) `< >` ile işaretli yerleri doldur.

---

## 🕓 Üretim geçmişi
| Tur | Ne yapıldı |
|---|---|
| 1 | Konu planı, 1.–2. hafta senaryoları, Scam Engineer Shorts serisi |
| 2 | 3.–4. hafta senaryoları, ayrı Shorts dosyaları |
| 3 | Büyüme ve para kazanma oyun kitabı (`oyun-kitabi/`) |
| 4 | Tüm senaryoların **v2**'si, Scam Engineer sıra değişikliği, Küba yedeğe, HS-07 |
| 5 | Araçlar (görsel kütüphane, Shorts şablonları), kanal sayfaları, topluluk planı, A/B planı, analiz şablonu |
| 6 (G1–G6) | Küçük resim üreticisi, reklam dışı gelir, 4.000 saat planı, Scam evergreen, çeviriler, hızlı kazanımlar, altyazı aracı |
| 7 (S1–S7) | Eksik analizi ve kapatılan eksikler (CW-07, marka rehberi, yükleme listesi, moderasyon), 60 bağımsız Short, Q4 analizi + 3 tatil senaryosu, yayınlanmış video iyileştirme, müzik/ses rehberi + seslendirme aracı, doğrulama turu, bu README |
| 8 | YPP eşik doğrulaması (8.000 saat resmi), yükleme paketi üreticisi ve 126 paket, Kokoro'ya hazır seslendirme metinleri |
