# Doğrulama turu (S6) — 30 Ekim 2026

**Ne yapıldı:** Bütün `-v2` senaryolarında, evergreen videolarda ve bunların v1 doğrulama tablolarında **"doğrulanamadı", "değişebilir", "kontrol et", "Orta"** olarak işaretli 30 madde WebSearch ile yeniden kontrol edildi. Yanlış çıkanlar düzeltildi, doğrulananların durumu güncellendi, hâlâ açık olanlar işaretlendi.

**Sonuç özeti:**
| Durum | Sayı |
|---|---|
| ✏️ **Metin düzeltildi** (yanlış veya fazla güçlü ifade) | 7 |
| ➕ **Yeni gelişme eklendi** | 1 |
| ✅ **Doğrulandı** (metin değişmedi, tablo güncellendi) | 15 |
| ⏳ **Hâlâ açık** (yayın haftasında tekrar bak) | 7 |

> WebFetch bu ortamda engelli olduğu için kontroller arama özetleri ve birden fazla kaynağın karşılaştırılmasıyla yapıldı. Tek kaynaklı bilgiler "Orta" bırakıldı.

---

## 1) Düzeltilen metinler ✏️

| # | Dosya | Önce | Bulgu | Sonra |
|---|---|---|---|---|
| 1 | `hidden_systems/05-v2.md` (SAHNE 8) | "A criminal trial is expected next year" | Yargıç Analisa Torres, Patrick ve Edward James için **13 Temmuz 2026**'ya duruşma tarihi koydu; eski CFO Mart 2026'da suçunu kabul etti ve tanıklık etmesi bekleniyor ([TT News](https://www.ttnews.com/articles/first-brands-cfo-pleads-guilty), [AML Intelligence](https://www.amlintelligence.com/2026/02/news-first-brands-founder-patrick-james-pleads-not-guilty-to-multi-billion-dollar-fraud/)). Duruşmanın gerçekleşip gerçekleşmediğine dair Ekim 2026 haberi bulunamadı | "A federal judge has set a criminal trial for the founder and his brother, and until there's a verdict, these remain allegations." |
| 2 | `hidden_systems/05-v2.md` (açıklama) | "the defendants have pleaded not guilty" | CFO da sanıktı ve suçunu kabul etti; "sanıklar" ifadesi yanlış genelleme | "Patrick James and Edward James have pleaded not guilty and are presumed innocent." |
| 3 | `hidden_systems/07-v2.md` (SAHNE 6) | "according to the House of Commons Library, Ofcom fined Virgin Media… over serious failures…" | Ofcom 1 Aralık 2025'te 23,8 milyon £ ceza verdi; sebep **telecare müşterilerinin dijital geçişte bağlantısının kesilmesi** ([ISPreview](https://www.ispreview.co.uk/index.php/2025/12/virgin-media-uk-fined-23-8m-over-poorly-handled-digital-phone-migrations.html), Which?) | "Ofcom fined Virgin Media 23.8 million pounds after it disconnected telecare customers during its move to digital landlines, putting thousands at risk." Kaynak eklendi |
| 4 | `hidden_systems/08-v2.md` (SAHNE 5) + `shorts_08-v2.md` (Short 2) | "Nearly eighty percent of the units that failed…" | FERC/NERC'in %80 oranı **donma kaynaklı** arızalar için ([Utility Dive](https://utilitydive.com/news/winter-storm-elliott-ferc-nerc-report-power-plant-outages/694451), [Public Power](https://www.publicpower.org/periodical/article/report-outlines-reliability-recommendations-tied-winter-storm-elliott)) | "Of the units that failed because of freezing, nearly eighty percent…" (Short'ta: "of the units that froze") |
| 5 | `centworks/07-v2.md` (SAHNE 6) + `shorts_07-v2.md` (Short 1) | "New Jersey passed a cash-acceptance law in 2021. Massachusetts, Colorado, Rhode Island and Connecticut have state rules." | NJ yasası **2019**; Massachusetts 1978; Rhode Island 2019; Colorado 2021. Connecticut tek kaynaklı ([Money.com](https://money.com/states-that-require-businesses-to-accept-cash/), [Bloomberg Law – RI](https://news.bloomberglaw.com/banking-law/rhode-island-retailers-must-take-cash-under-new-law)) | "Massachusetts has required stores to accept cash since the 1970s. New Jersey and Rhode Island passed laws in 2019, and Colorado in 2021." CT çıkarıldı |
| 6 | `centworks/07-v2.md` (SAHNE 9) + `shorts_07-v2.md` (Short 3) + `gelir/pdf-icerikleri.md` | "emergency checklists… tell you to keep some cash" | Ready.gov nakdi **"ek malzemeler"** listesinde öneriyor, temel listede değil ([Ready.gov](https://www.ready.gov/kit)) | "suggest keeping some cash at home" |
| 7 | `scam_engineer/evergreen-02.md` (SAHNE 4, Short VO, Short ekran yazısı) | "your number cannot be suspended" / "NUMBERS CAN'T BE SUSPENDED" | SSA'nın ifadesi: SSN'nin askıya alındığını söylemek için **asla aramaz**. "Askıya alınamaz" birebir bulunamadı (SSA OIG uyarıları, ABD Savcılığı duyuruları) | "it will never call to tell you your number has been suspended" · ekran: "SSA WON'T CALL ABOUT THIS" |

## 2) Eklenen yeni gelişme ➕

| # | Dosya | Bulgu | Değişiklik |
|---|---|---|---|
| 8 | `centworks/04-v2.md` (SAHNE 5) + v1 tablo | **26 Ekim 2026:** 8. Daire İstinaf Mahkemesi, Fed'in 21 sentlik banka kartı tavanının (Regulation II) yasanın izin vermediği maliyetleri içerdiğine dair Kuzey Dakota kararını onadı. Tavan, mahkemenin resmi kararı (mandate) çıkana kadar yürürlükte. 6. Daire'de görülen benzer dava farklı sonuçlanabilir ([Payments Dive](https://www.paymentsdive.com/news/fed-loses-debit-card-cap-appeal/872785/), [American Banker](https://www.americanbanker.com/news/appeals-court-confirms-fed-set-interchange-fee-too-high)) | 2 cümle eklendi: "In October 2026, a federal appeals court agreed with a lower court that the Fed counted costs the law didn't allow. For now, the cap stays in place while the Fed works out what comes next." Kaynak eklendi. **Not:** SAHNE 5 ~14 sn uzadı; kurgudan sonra bölüm zamanlarını kontrol et |

## 3) Doğrulanan maddeler ✅ (metin aynı, tablolar güncellendi)

| # | Dosya | İddia | Kaynak |
|---|---|---|---|
| 9 | `centworks/05-v2.md` | Freddie Mac 30 yıllık ortalama %7,40 (Ekim 2026) | FRED MORTGAGE30US (8 ve 15 Ekim: %7,40). v1 tablosundaki "29 Ekim %7,24" bulunamadı, çıkarıldı |
| 10 | `centworks/05-v2.md`, `06-v2.md` | Ortalama kart faizi ~%21 | Fed G.19 / FRED TERMCBCCALLNS (Şubat 2026 %21,00, Mayıs 2026 %20,94) |
| 11 | `centworks/06-v2.md` | Büyük bir BNPL sağlayıcısı %0–36 APR | NerdWallet 2026 Affirm incelemesi, Bankrate |
| 12 | `centworks/04-v2.md` | Visa/Mastercard uzlaşmasına Haziran 2026'da ön onay | PYMNTS, Payments Journal (9 Haziran 2026, Yargıç Brian Cogan). Nihai onay henüz yok |
| 13 | `centworks/07-v2.md` | Federal yasa özel işletmeyi nakit almaya zorlamıyor | [Federal Reserve FAQ](https://federalreserve.gov/faqs/currency_12772.htm) |
| 14 | `centworks/07-v2.md` | FDIC: bankasız olmanın en sık nedeni yeterli bakiye olmaması | FDIC 2023 yönetici özeti (%42,3 "nedenlerden biri") |
| 15 | `centworks/07-v2.md` | 55+ ayda ~10, 18–24 ~2 nakit ödeme | Fed 2026 Diary özetleri (tekrar kontrol) |
| 16 | `hidden_systems/07-v2.md` | ~1,5 milyon hat hâlâ bakırda (Temmuz 2026), 31 Ocak 2027, uzatma yok | ISPreview (Temmuz 2026), thinkbroadband |
| 17 | `scam_engineer/04-v2.md` | Planlar genelde izinsiz soğuk arama yapamaz | [42 CFR 422.2264](https://www.law.cornell.edu/cfr/text/42/422.2264). Not: (c) fıkrasındaki zaman/şekil kuralları CMS-4201-F ile değişti; "generally" ifadesi doğru |
| 18 | `scam_engineer/05-v2.md` | Microsoft hata mesajlarında telefon numarası olmaz | [Microsoft Support](https://support.microsoft.com/help/4013405) |
| 19 | `scam_engineer/07-v2.md` | Kart boşaltma: koruyucu etiket sökme, PIN kazıma, barkod etiketi | [FTC – Check out gift cards before you buy them (Ara 2024)](https://www.consumer.ftc.gov/consumer-alerts/2024/12/check-out-gift-cards-you-buy-them). Kaynak açıklamaya eklendi |
| 20 | `scam_engineer/07-v2.md`, `evergreen-01.md` | USPS, kayıt olmadıkça linkli SMS göndermez | USPIS (TIME, yerel haberlerdeki USPIS açıklamaları) |
| 21 | `scam_engineer/evergreen-02.md` | Kredi dondurma ücretsiz, geçici kaldırılabilir | [FTC (2018)](https://consumer.ftc.gov/consumer-alerts/2018/09/free-credit-freezes-are-here) |
| 22 | `scam_engineer/evergreen-04.md` | Postayla gönderilen nakit: USPIS'ten paketi durdurmasını iste | FTC "What to do if you were scammed" (USPIS 877-876-2455) |
| 23 | `hidden_systems/08-v2.md` | 90.500 MW, %13, %96, TVA/Duke rakamları | FERC/NERC (S3'te doğrulanmıştı, tekrar teyit) |

## 4) Hâlâ açık ⏳ (yayın haftasında tekrar bak)

| # | Dosya | Madde | Neden açık | Ne zaman |
|---|---|---|---|---|
| 24 | `hidden_systems/04-v2.md` | Google'ın **nihai** olay raporu | 30 Ekim itibarıyla yayımlanmadı; Google "iç soruşturma bitince" dedi. Metin "preliminary" diyor, doğru | 11 Kasım öncesi |
| 25 | `hidden_systems/05-v2.md` | James kardeşlerin duruşması yapıldı mı, karar var mı? | Temmuz 2026 sonrası haber bulunamadı | 18 Kasım öncesi (SDNY 26-cr-29) |
| 26 | `hidden_systems/06-v2.md` | AWS'nin resmî post-event summary'si | Bulunamadı; Health Dashboard ve Coinbase açıklaması kullanılıyor | 25 Kasım öncesi |
| 27 | `centworks/03-v2.md` | Common Cents Act imzalandı mı? | Kongre'den geçti, imza beklendiği bildiriliyor; imza kaynağı yok | 7 Kasım öncesi. İmzalandıysa SAHNE 4'e "and it's now law" |
| 28 | `centworks/04-v2.md` | Uzlaşmanın nihai onayı; 8. Daire kararının "mandate"ı; Fed'in yeni kuralı | Süreç devam ediyor | 14 Kasım öncesi |
| 29 | `centworks/07-v2.md` | Payment Choice Act durumu; Connecticut yasası | Tasarı bekliyor; CT tek kaynaklı (metinden çıkarıldı) | 5 Aralık öncesi |
| 30 | `centworks/08-v2.md` | Bankrate'in 2025 hediye kartı anketi var mı? | 2024 rakamları kullanılıyor | 12 Aralık öncesi |

---

## 5) Etkilenen diğer dosyalar
- **Çeviriler:** `ceviriler/CW-04.md`, `HS-07.md`, `SE-07.md` kaynak listeleri değişti → `python ceviriler/_uret.py` ile yeniden üretildi.
- **Shorts kontrolü:** Değişen Short'lar (`shorts_07-v2.md`, `shorts_08-v2.md`, `evergreen-02.md` Shorts) `shortchk`'tan geçti.
- **Kelime sayıları** (değişen senaryolar, 1.100–1.350 aralığında): CW-04 1.161 · CW-07 1.150 · HS-05 1.122 · HS-07 1.106 · HS-08 1.118 · EV-02 1.109.
- **Küçük resimler:** Etkilenmedi.

## 6) Bir sonraki doğrulama turu için kural
- Her yayından **3 gün önce** o videonun ⚠️ satırı ve doğrulama tablosundaki "Orta" maddeleri tekrar aranır.
- Mahkeme, mevzuat ve faiz/oran içeren videolar (CW-03, CW-04, CW-05, HS-05) **öncelikli**.
- Sonuç bu dosyaya yeni bir bölüm olarak eklenir: "Tur 2 — <tarih>".
