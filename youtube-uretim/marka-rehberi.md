# Marka rehberi (3 kanal)

**Neden var:** Renkler `arac/kucuk_resim/temalar.py`'de, kimlik cümleleri senaryolarda, seri adları `kanal-sayfalari.md`'de, ses kuralları `muzik-ve-ses.md`'de dağınıktı. Bu dosya hepsini tek yerde topluyor. Yeni bir video, Short, kanal sanatı veya çeviri hazırlarken buradan bak.

**Kural:** Bir şeyi değiştirirsen önce bu dosyayı, sonra kaynağını değiştir (ör. renk değişirse `temalar.py`).

---

## 1) Kimlik tablosu

| | Hidden Systems | Centworks | Scam Engineer |
|---|---|---|---|
| Kullanıcı adı | @collapse.stories | @centworks | @thescamengineer |
| Bir cümlede | How invisible systems work, and how they fail | How money really works, explained by an engineer | How scams really work, so they never work on you |
| Kitle | İngiltere + ABD | ABD | ABD, 40+ |
| Ton | İngiliz belgesel anlatıcısı. Sakin, ölçülü, gerilim yapıdan gelir, sıfattan değil | Meraklı, net, rakamlı. "Zengin ol" vaadi yok | Sakin, saygılı, öğretici. Korku ve panik dili yok |
| Yazım | **İngiliz İngilizcesi** (centre, colour, realise) | **Amerikan İngilizcesi** | **Amerikan İngilizcesi** |
| Kimlik cümlesi (birebir) | This channel is made by someone who works inside a mobile network operations center. | This channel is made by an engineer, not a banker. | This channel is made by a telecom engineer. |
| Kimlik cümlesinin yeri | 0:12–0:20 arası, tek başına bir sahne | 0:12–0:20 | 0:12–0:20 |
| Zorunlu uyarı | Ceza davalarında "allegations… presumed innocent" | "This is educational, not financial advice." (kapanışta) + açıklamada | Gerektiğinde "not legal or financial advice", "recovery isn't guaranteed" |
| Kapanış cümlesi | "Next on Hidden Systems: …" (sonraki bölümün tek cümlelik merakı) | "This is educational, not financial advice. Next week on Centworks: …" | "That's how this scam works — so it never works on you." |
| Yasak | Siyasi taraf tutma, felakette grafik ayrıntı, ölüm sayısıyla başlık | Kripto/trading tavsiyesi, "bu hisseyi al", kesin getiri | Korku kelimeleri (terrifying, nightmare, you're in danger), mağduru suçlama, gerçek mağdur görüntüsü |

> Kimlik cümlesi birinci tekil şahısla genişletilmez. "I spend my nights…" gibi uydurma geçmiş cümleleri yasak (v2 kuralı).

### Scam Engineer'da kaçınılacak ve yerine kullanılacak kelimeler
| Kullanma | Kullan |
|---|---|
| terrifying, horrifying, nightmare | common, costly, well organized |
| you could lose everything | here's what's at risk, and how to protect it |
| act now!, urgent | take these steps today, in this order |
| victims were stupid / fell for it | careful people get targeted too |
| hackers are everywhere | this is how this one works |

---

## 2) Renkler

Kaynak: `arac/kucuk_resim/temalar.py`. Küçük resim, kanal banner'ı, bitiş ekranı ve video içi grafiklerde aynı renkler.

| Kanal | Arka plan (üst → alt) | Ana vurgu | İkinci vurgu | Yazı |
|---|---|---|---|---|
| Hidden Systems | `#060912` → `#161E30` (gece laciverti) | `#FF2D2D` (alarm kırmızısı) | `#FFAA3C` (sodyum lamba turuncusu) | `#FFFFFF`, siyah kontur |
| Centworks | `#0E0E10` → `#202228` (antrasit) | `#FFC400` (altın) | `#22C55E` (para yeşili) | `#FFFFFF`, siyah kontur |
| Scam Engineer | `#BAE2FF` → `#FFECAA` (gökyüzü → güneş) | `#006EFF` (güven mavisi) | `#FF8C00` (dikkat turuncusu) | `#0A1F44` (lacivert), beyaz kontur |

- **Scam Engineer'da kırmızı yok.** Uyarı rengi turuncu. Kırmızı korku ve panik çağrıştırır.
- Kontrast: Yazı/arka plan en az **4,5:1** (WCAG). Üretici bunu kodla kontrol ediyor.
- Grafiklerde "iyi/kötü": Hidden Systems kırmızı = arıza, turuncu = uyarı. Centworks yeşil = kazanç, altın = vurgu. Scam Engineer mavi = güvenli adım, turuncu = dikkat edilecek işaret.

## 3) Yazı tipleri

| Kullanım | Yazı tipi | Lisans |
|---|---|---|
| Küçük resim başlığı | Inter Display Black | SIL OFL 1.1 (`arac/kucuk_resim/fonts/OFL.txt`) |
| Video içi başlık, alt yazı kartı, rakam | Inter Display Black / Inter Bold | OFL 1.1 |
| Kaynak satırı (ekranın altı) | Inter Bold, küçük, %70 opaklık | OFL 1.1 |

Tek yazı ailesi: üç kanal aynı aileyi farklı renklerle kullanır, böylece üretim tek şablonla yapılır.

## 4) Küçük resim kuralları (özet)
- En fazla **4 kelime**, tek ana nesne, yazı sol blokta, nesne sağda, süre rozeti alanı (sağ alt) boş.
- Nesne videonun **ilk karesinde** görünür.
- Gerçek kişi, gerçek logo, gerçek banknot/kimlik tasarımı yok. Nesneler vektör çizim.
- Üretici ve testler: `arac/kucuk_resim/`. A/B yöntemi: `kucuk-resim-ab.md`.

## 5) Ses kimliği
- Anlatıcı: Kokoro TTS. **Kanal başına tek ses**, hiç değişmez. Ses seçimi ve ayarlar: `muzik-ve-ses.md`.
- Müzik karakteri: Hidden Systems koyu ambient/drone; Centworks hafif, ritmik, "bilgi" müziği; Scam Engineer sıcak, sakin piyano/akustik. Ayrıntı: `muzik-ve-ses.md`.
- Ses logosu: Kullanılmıyor. İlk saniyede ses efekti yerine hikâye başlar (hook kuralı).

## 6) Seri ve adlandırma
| Kanal | Seriler (oynatma listesi adıyla aynı) |
|---|---|
| Hidden Systems | Outage Files · How the Grid Fails · Phone Networks Explained · Company Collapses |
| Centworks | Money Mechanics · Credit Cards Decoded · What If… · A vs B |
| Scam Engineer | Scam Anatomy · Phone Scams · Protect Your Parents · Seasonal Scam Alerts · Is It a Scam? · Real or Fake? (Shorts) |

- Seri numarası başlıkta değil, açıklamada ve video içi küçük etikette: "Outage Files #2", "What If #2".
- Dosya adı: `<kanal>/<sıra>-v2.md`, Shorts `shorts_<sıra>-v2.md` (Scam Engineer'da Shorts senaryo içinde). Kalıcı videolar `evergreen-<sıra>.md`. Bağımsız Shorts `shorts-bagimsiz-hafta-<n>.md`.
- Video kimliği (ID): `HS-04`, `CW-07`, `SE-05`, `EV-02`. Küçük resim ve çeviri dosyaları bu kimlikle adlanır.

## 7) Bitiş ekranı şablonu (son 15–20 sn)

```
┌──────────────────────────────────────────────┐
│                                              │
│   [ SONRAKİ VİDEO ]        [ ABONE OL ]      │
│   (seri içinden,           (kanal logosu)    │
│    büyük kutu, sol)                          │
│                                              │
│   Alt şerit: kanalın arka plan rengi,        │
│   seri adı ("Outage Files") küçük yazıyla    │
└──────────────────────────────────────────────┘
```
- Öğe sayısı: 2 (video + abone ol). Fazla öğe tıklamayı böler.
- Video öğesi: Senaryodaki "Bitiş ekranı" satırındaki video. Henüz yayınlanmadıysa "En son yüklenen".
- Son 20 saniyede anlatım bitiş cümlesini söyler, ekrandaki görüntü sade kalır (kanalın arka plan rengi + bulanık son sahne).

## 8) Kanal sanatı (banner ve profil resmi) metin şartnamesi
Görsel üretilmedi. Tasarımcıya veya Canva benzeri bir araca verilecek metin:

| Kanal | Banner ana yazı | Banner alt yazı | Profil resmi |
|---|---|---|---|
| Hidden Systems | HIDDEN SYSTEMS | How the things you rely on work — and how they fail. New episodes every Wednesday. | Koyu lacivert zemin, tek kırmızı nokta (bir arıza lambası). Yazı yok |
| Centworks | CENTWORKS | How money really works. Explained by an engineer. New episodes every Saturday. | Antrasit zemin, altın renkli "¢" işareti |
| Scam Engineer | THE SCAM ENGINEER | A telecom engineer explains how scams really work, so they never work on you. New every Wednesday. | Açık mavi zemin, lacivert bir anahtar/kilit simgesi (logo değil, basit şekil). Kırmızı yok |

- Banner ölçüsü: 2560 × 1440 px. Tüm cihazlarda görünen güvenli alan: ortadaki **1546 × 423 px**. Yazı bu alanın içinde kalır.
- Yayın günleri: Hidden Systems ve Scam Engineer **Çarşamba**, Centworks **Cumartesi** (README takvimi). Gün değişirse banner'ı da güncelle.

## 9) Filigran (watermark)
- Studio → Özelleştirme → Marka → Video filigranı: Profil resminin sade hâli, 150 × 150 px, "videonun sonunda" değil **"tüm video boyunca"**. Abone ol butonu gibi çalışır.
