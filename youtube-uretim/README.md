# youtube-uretim: Üretim dosyaları

Senaryo metinleri İngilizce, notlar ve açıklamalar Türkçe. Sadece metin üretildi, görsel üretilmedi.

- **1. tur:** konu planı, 1.–2. hafta senaryoları, Scam Engineer Shorts serisi
- **2. tur:** 3.–4. hafta senaryoları, Hidden Systems ve Centworks için ayrı Shorts dosyaları
- **3. tur:** büyüme ve para kazanma oyun kitabı (`oyun-kitabi/`)
- **4. tur (güncel):** tüm senaryoların **v2** sürümleri (`-v2.md`), Scam Engineer yayın sırasının değişmesi, Küba videosunun yedeğe alınması, Hidden Systems için yeni 2 Aralık konusu

> **Yayına giren sürüm her zaman `-v2.md`.** v1 dosyaları ve doğrulama tabloları referans olarak duruyor.

---

## 📅 Yayın takvimi (v2)

| Tarih | Gün | Kanal | Uzun video | Shorts dosyası | Önerilen Shorts günleri |
|---|---|---|---|---|---|
| 5–10 Kas | Per–Sal | Scam Engineer | — (yayınlanmış V1 spoofing ve V2 SIM swap videolarına trafik) | `scam_engineer/shorts_5-10_kasim-v2.md` | 5, 6, 7, 8, 9, 10 Kas |
| **7 Kas** | Cmt | Centworks | `centworks/03-v2.md`: Kuruşun sonu ve nakit yuvarlama | `centworks/shorts_03-v2.md` | 8, 10, 12 Kas |
| **11 Kas** | Çar | Hidden Systems | `hidden_systems/04-v2.md`: Google Cloud Londra, çalışmayan jeneratör | `hidden_systems/shorts_04-v2.md` | 12, 14, 16 Kas |
| **11 Kas** | Çar | Scam Engineer | `scam_engineer/03-v2.md`: "Unpaid toll" SMS'i | Senaryo dosyasının içinde | 12, 14, 16 Kas |
| **14 Kas** | Cmt | Centworks | `centworks/04-v2.md`: Kredi kartı ödüllerini kim ödüyor? | `centworks/shorts_04-v2.md` | 15, 17, 19 Kas |
| **18 Kas** | Çar | Hidden Systems | `hidden_systems/05-v2.md`: First Brands (zaman çizelgesi yapısı) | `hidden_systems/shorts_05-v2.md` | 19, 21, 23 Kas |
| **18 Kas** | Çar | Scam Engineer | `scam_engineer/04-v2.md`: **Medicare** açık kayıt aramaları (bitiş 7 Ara) | Senaryo dosyasının içinde | 19, 21, 23 Kas |
| **21 Kas** | Cmt | Centworks | `centworks/05-v2.md`: What if the Fed keeps raising rates? (üç dallı yapı) | `centworks/shorts_05-v2.md` | 22, 24, 26 Kas |
| **25 Kas** | Çar | Hidden Systems | `hidden_systems/06-v2.md`: AWS us-east-1 soğutma arızası | `hidden_systems/shorts_06-v2.md` | 26, 28, 30 Kas |
| **25 Kas** | Çar | Scam Engineer | `scam_engineer/05-v2.md`: **Phantom Hacker** (Şükran Günü arifesi) | Senaryo dosyasının içinde | 26, 28, 30 Kas |
| **28 Kas** | Cmt | Centworks | `centworks/06-v2.md`: BNPL vs kredi kartı (Black Friday hafta sonu) | `centworks/shorts_06-v2.md` | 29 Kas, 30 Kas (Cyber Monday, Short 3), 2 Ara |
| **2 Ara** | Çar | Hidden Systems | `hidden_systems/07-v2.md`: **YENİ** İngiltere bakır hat kapanışı (31 Ocak 2027) | `hidden_systems/shorts_07-v2.md` | 3, 5, 7 Ara |
| **2 Ara** | Çar | Scam Engineer | `scam_engineer/06-v2.md`: **Sahte online mağazalar** (Cyber Monday ve tatil alışverişi) | Senaryo dosyasının içinde | 3, 5, 7 Ara |

**Yedek:** `hidden_systems/yedek-kuba.md` (+ `yedek-kuba-shorts.md`). Küba videosu politik hassasiyet nedeniyle takvimden çıkarıldı.
**Sonraki haftalar (planlanan, senaryosu yok):** [`konular.md`](konular.md)

---

## v2'de ne değişti (tüm senaryolar)
Kaynak: `oyun-kitabi/ozet-ve-kurallar.md` ve `oyun-kitabi/senaryo-revizyon-onerileri.md`, ayrıca kullanıcının ek talimatları.

1. **Kimlik:** Hiçbir senaryoda anlatıcı birinci tekil şahısla gerçek bir kişi olarak tanıtılmıyor. Kanal tanıtılıyor:
   - Hidden Systems: *"This channel is made by someone who works inside a mobile network operations center."*
   - Centworks: *"This channel is made by an engineer, not a banker."*
   - Scam Engineer: *"This channel is made by a telecom engineer."*

   Uydurma geçmiş cümleleri ve "In my world", "As an engineer, I…" gibi kişisel iddialar kaldırıldı.
2. **İlk merak sorusu** her senaryoda **0:29–0:39** arasında. İlk soruya kadar en fazla ~98 kelime var (150 kelime/dk ile hesaplandı).
3. **Küçük resimdeki ana nesne ilk sahnede görünüyor.** Gerekirse küçük resim konsepti değiştirildi (ör. CW-05: "+$284/MONTH").
4. **Vaat cümleleri** kısaltıldı ve "By the end of this video" kalıbı bırakıldı.
5. **Yapı çeşitliliği:**
   - HS-05: zaman çizelgesi
   - HS-06: sıcaklık göstergesi
   - CW-05: üç dallı senaryo
   - CW-06: puan tablosu
   - SE-05: "üç kapı"

   Kapanışlar farklılaştırıldı.
6. **Scam Engineer sırası:** Medicare videosu 7 Aralık'tan önce çıksın diye sıra 03 SMS (11 Kas) → 04 Medicare (18 Kas) → 05 Phantom Hacker (25 Kas) → 06 Sahte mağazalar (2 Ara) oldu.
   - v1 dosyaları da bu sıraya göre yeniden adlandırıldı. İçlerindeki eski başlık numaraları (#04, #05, #06) değiştirilmedi.
7. **CW-05 (Fed):** Savaş ve politika ayrıntıları çıkarıldı, enerji fiyatları tek cümleyle geçildi.
8. **CW-06 (BNPL):** Metin "Black Friday weekend" diline göre düzeltildi (yayın 28 Kasım Cumartesi).
9. **Shorts (tümü):**
   - İlk kare hareketli.
   - Ekran yazısı en fazla 6 kelime ve VO'nun ilk cümlesiyle aynı. Bu, kontrol betiğiyle 42 Short'ta doğrulandı.
   - Son cümle ilk cümleye bağlanıyor (döngü).
   - "Full story on the channel" yerine açıklamada "Related video bağlantısı: <video adı>" notu var.

---

## Dosya yapısı

### Hidden Systems (`hidden_systems/`)
| v2 (yayın) | v1 (referans + doğrulama tablosu) | Shorts v2 |
|---|---|---|
| `04-v2.md` | `04.md` | `shorts_04-v2.md` (v1: `shorts_04.md`) |
| `05-v2.md` | `05.md` | `shorts_05-v2.md` (v1: `shorts_05.md`) |
| `06-v2.md` | `06.md` | `shorts_06-v2.md` (v1: `shorts_06.md`) |
| `07-v2.md` (yeni konu, doğrulama tablosu dosyanın içinde) | — | `shorts_07-v2.md` |
| — | `yedek-kuba.md` (eski 07) | `yedek-kuba-shorts.md` (eski shorts_07) |

### Centworks (`centworks/`)
| v2 | v1 | Shorts v2 |
|---|---|---|
| `03-v2.md` | `03.md` | `shorts_03-v2.md` |
| `04-v2.md` | `04.md` | `shorts_04-v2.md` |
| `05-v2.md` | `05.md` | `shorts_05-v2.md` |
| `06-v2.md` | `06.md` | `shorts_06-v2.md` |

### Scam Engineer (`scam_engineer/`)
| v2 | v1 (yeni dosya adı ← eski) | Shorts |
|---|---|---|
| `03-v2.md` SMS | `03.md` | Senaryo içinde |
| `04-v2.md` Medicare | `04.md` (← eski 06.md) | Senaryo içinde |
| `05-v2.md` Phantom Hacker | `05.md` (← eski 04.md) | Senaryo içinde |
| `06-v2.md` Sahte mağazalar | `06.md` (← eski 05.md) | Senaryo içinde |
| — | — | `shorts_5-10_kasim-v2.md` (v1: `shorts_5-10_kasim.md`) |

### Planlama ve araştırma
| Dosya | İçerik |
|---|---|
| `konular.md` | 6 haftalık konu planı (yeni sıraya göre güncellendi) |
| `oyun-kitabi/` | Büyüme ve para kazanma oyun kitabı (10 dosya). **Başlangıç:** `oyun-kitabi/ozet-ve-kurallar.md` |

---

## ⚠️ Yayından önce yapılması gerekenler
1. **Linkleri bir kez aç.** Bu oturumda doğrudan sayfa açma (WebFetch) engelliydi. İddialar arama özetlerinden doğrulandı.
2. **Değişebilecek bilgiler:**
   - HS-04: Google'ın nihai raporu
   - HS-05: Ceza davasının tarihi
   - HS-06: AWS'nin resmî post-event summary'si
   - HS-07: Openreach'in güncel hat sayısı ve Emergency Voice Access durumu
   - CW-03: Common Cents Act'in imza durumu
   - CW-04: Visa/Mastercard uzlaşmasının nihai onayı
   - CW-05: Son Freddie Mac oranı ve TÜFE
   - CW-06: BNPL sağlayıcılarının ücret koşulları
   - SE-04: Michigan DIFS duyurusu ve 42 CFR 422.2264
3. **`shorts_5-10_kasim-v2.md`:** Related video notlarına yayınlanmış V1 ve V2 videolarının **gerçek başlıklarını** yaz.
4. **Ses:** Centworks ve Scam Engineer için gerçek insan sesi önerilir (bkz. `oyun-kitabi/yapay-zeka-ve-politika.md`).
5. **Dramatize karakterler temsilî** (Diane, Dorothy, Frank, Carol, Ana & Chris, Jordan, Linda, Tom). Ekranda "Reconstruction / Composite character / Illustrative example" yazısı kullanılmalı.
