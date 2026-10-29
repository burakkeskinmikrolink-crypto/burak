# Yayınlanmış 4 uzun video için A/B test planı (küçük resim ve başlık)

**Amaç:** Yayınlanmış videoların küçük resmini ve başlığını YouTube Studio'daki **Test & Compare** ile yeniden test etmek.
- Mevcut küçük resim ve başlık **A** (kontrol) olarak kalır.
- Aşağıdaki iki alternatif **B** ve **C** olarak eklenir.

**Kurallar:**
- Küçük resim metni **en fazla 4 kelime**.
- Gerçek kişi fotoğrafı, haber ajansı görseli ve gerçek şirket logosu yok (CrowdStrike, Microsoft, banka logoları dahil).
- Scam Engineer başlıklarında arama kelimesi **"scam"** geçer.
- Korku dili ve abartılı vaat yok. Küçük resimdeki nesne videonun ilk 10 saniyesinde görünmeli. Görünmüyorsa o alternatif seçilmemeli ya da açılışa kısa bir ekleme yapılmalı.

**Test & Compare nasıl okunur** (ayrıntı: `oyun-kitabi/baslik-ve-kucuk-resim.md`):
- Kazanan, tıklama oranına göre değil **izlenme süresi payına** göre seçilir.
- Önce **küçük resmi** test et (A/B/C). Kazanan belli olduktan sonra **başlığı** ayrı bir testte dene. İkisini aynı anda değiştirme.
- Yayınlanmış videolarda gösterim az olabilir. Test 2 haftada "Inconclusive" çıkarsa, alternatifi o videonun en çok trafik aldığı haftaya denk getirip yeniden dene.
- Sonucu `haftalik-analiz-sablonu.md` içine yaz.

---

## 1) Hidden Systems: Spain blackout (Nisan 2025)

### Küçük resim alternatifleri
| | Metin (≤4) | Görsel tarifi | Renk |
|---|---|---|---|
| **B** | A COUNTRY WENT DARK | NASA Black Marble gece uydu görüntüsü: İber Yarımadası, sol yarısı ışıklı, sağ yarısı tamamen karanlık. Sınırda ince bir "kesik" çizgisi | Lacivert gece + sıcak turuncu şehir ışıkları. Yazı beyaz, "DARK" kelimesi soluk gri |
| **C** | 60 MILLION, NO POWER | Kararmış bir trafik ışığı ve durmuş bir metro tabelası (Pexels/Wikimedia), ortada büyük bir frekans ibresi (50 Hz) kırmızı bölgeye düşmüş | Koyu gri arka plan, kırmızı ibre, sarı rakam |

> "60 million" İspanya ve Portekiz'in toplam nüfusu için yuvarlak bir rakam. Videoda bu rakam geçmiyorsa C'nin metnini **"SPAIN: ZERO VOLTS"** olarak değiştir. Videoda olmayan bir sayı küçük resme konmamalı.

### Başlık alternatifleri
- **B:** The Day Spain Went Dark: How a Whole Country Lost Power in Seconds
- **C:** Spain Blackout Explained: What Really Caused the April 2025 Grid Collapse *(arama odaklı)*

---

## 2) Hidden Systems: CrowdStrike outage (Temmuz 2024)

### Küçük resim alternatifleri
| | Metin (≤4) | Görsel tarifi | Renk |
|---|---|---|---|
| **B** | ONE UPDATE. 8.5M CRASHES. | Havalimanı kalkış panosu, tüm satırlar "CANCELLED" (kurgusal pano grafiği, gerçek havayolu adı yok). Önde mavi bir hata ekranı silueti, logo yok | Mavi hata ekranı tonu + kırmızı "CANCELLED" |
| **C** | THE FILE THAT FROZE | Tek bir dosya simgesi devrilen domino taşlarının başında. Domino taşlarının üstünde havalimanı, hastane ve banka ikonları | Siyah zemin, beyaz domino taşları, dosya simgesi elektrik mavisi |

> **Not:** "8.5M" rakamı Microsoft'un etkilenen Windows cihaz tahmini. Videoda geçmiyorsa B'nin metnini "ONE UPDATE. WORLD DOWN." yap. CrowdStrike ve Microsoft logoları kullanılmaz.

### Başlık alternatifleri
- **B:** One Faulty Update Crashed 8.5 Million Computers. Here's How.
- **C:** CrowdStrike Outage Explained: How One Update Grounded Flights Worldwide *(arama odaklı)*

---

## 3) Centworks: Kredi kartı şirketleri neden geç ödemeni ister?

### Küçük resim alternatifleri
| | Metin (≤4) | Görsel tarifi | Renk |
|---|---|---|---|
| **B** | LATE = THEIR PROFIT | Kredi kartı (kurgusal, logosuz) bir takvimin üstünde, takvimde ödeme günü kırmızı çarpıyla geçilmiş, kartın arkasından yeşil bir para grafiği yükseliyor | Siyah + Centworks sarısı. Grafik yeşil, çarpı kırmızı |
| **C** | YOU'RE THE PRODUCT | Bir kart terminali ekranında "+$32 LATE FEE" ve "+24% APR" satırları; arka planda bulanık bir banka binası (Wikimedia, logosuz) | Sarı zemin, siyah rakamlar |

> "$32" gibi belirli bir ücret videoda geçmiyorsa C görselinde rakam yerine "LATE FEE" ve "APR" kelimelerini kullan.

### Başlık alternatifleri
- **B:** Why Credit Card Companies Secretly Love It When You Pay Late
- **C:** How Credit Card Companies Make Money: Late Fees, Interest and APR Explained *(arama odaklı)*

---

## 4) Scam Engineer: Bankanın gerçek numarasından arama (caller ID spoofing)

### Küçük resim alternatifleri
| | Metin (≤4) | Görsel tarifi | Renk |
|---|---|---|---|
| **B** | NOT YOUR BANK | Telefon ekranında gelen arama: kurgusal banka adı ve gerçek görünen bir numara, numaranın üstünde ince bir "maske" efekti (numara bir kâğıt gibi soyuluyor) | Sakin lacivert + beyaz. Korku kırmızısı yok, sadece ince gri çarpı |
| **C** | REAL NUMBER. FAKE CALLER. | Bölünmüş görsel: solda banka kartının arka yüzü (kurgusal, numara görünür), sağda aynı numarayı gösteren gelen arama ekranı. Ortada eşittir işaretinin üstü çizili | Açık mavi + beyaz, metin koyu lacivert |

### Başlık alternatifleri (ikisinde de "scam" geçiyor)
- **B:** The "Bank Fraud Department" Scam: Why Your Bank's Real Number Can Lie
- **C:** Caller ID Spoofing Scam Explained: How Scammers Call From Your Bank's Real Number *(arama odaklı)*

---

## Uygulama sırası (öneri)
| Hafta | Video | Test |
|---|---|---|
| 2–8 Kas | Scam Engineer: spoofing | Küçük resim A/B/C. 5–10 Kasım Shorts serisi bu videoya trafik getireceği için ilk test bu |
| 9–15 Kas | Centworks: geç ödeme | Küçük resim A/B/C. CW-04 (ödüller) yayınlandığı hafta ilgili trafik artar |
| 16–22 Kas | Hidden Systems: CrowdStrike | Küçük resim A/B/C |
| 23–29 Kas | Hidden Systems: Spain blackout | Küçük resim A/B/C |
| 30 Kas–13 Ara | 4 videonun kazanan küçük resimleriyle | Başlık A/B/C testleri |
