# Yayınlanmış 4 uzun video ve 4 Short için iyileştirme (yapıştırmaya hazır)

**Kapsam:** Spain blackout, CrowdStrike (Hidden Systems) · Kredi kartı geç ödeme (Centworks) · Bankanın gerçek numarası / caller ID spoofing (Scam Engineer). Her biri için:
1. **Arama odaklı açıklama:** İlk iki satır anahtar kelimeli, sonra bölümler ve kaynaklar.
2. **Etiketler.**
3. **Sabit yorum.**
4. **Oynatma listesi.**

**Önemli uyarılar:**
- Bu videoların **gerçek metni ve süreleri depoda yok**. Açıklamalar konuyla ilgili doğrulanmış kaynaklara göre yazıldı.
- Yapıştırmadan önce iki kontrol yap:
  1. **Videoda geçmeyen bir iddia açıklamada olmasın.** Geçmiyorsa o cümleyi sil.
  2. **Bölüm zaman kodlarını kendi videona göre doldur.** `[m:ss]` yazan yerler. İlk bölüm her zaman `0:00`. YouTube'un bölümleri göstermesi için en az 3 bölüm ve her biri en az 10 saniye olmalı.
- Başlık değişikliği burada yok. Başlık ve küçük resim testleri `kucuk-resim-ab.md`'de; önce küçük resmi, sonra başlığı test et.
- Kimlik cümleleri v2 kuralına göre (birinci tekil şahıs yok).
- Değişiklikten sonra çevirileri güncelle: `ceviriler/P-*.md` (kaynak listeleri bu dosyadan eklendi).

**Neden ilk iki satır:** Arama sonuçlarında ve "daha fazla" düğmesinden önce yalnızca açıklamanın başı görünür. İzleyicinin aradığı kelimeler (ör. "Spain blackout explained", "CrowdStrike outage cause") orada geçmeli. Kanıt düzeyi: YouTube'un kendi önerisi açıklamada anahtar kelimeleri doğal kullanmak (`oyun-kitabi/baslik-ve-kucuk-resim.md`).

---

## 1) Hidden Systems: Spain blackout (28 Nisan 2025)

### Açıklama
```
Spain blackout explained: on 28 April 2025, Spain and Portugal lost power within seconds. What actually caused the Iberian blackout, according to the European grid operators' final expert report? Here's the hidden system that keeps a power grid stable — voltage, frequency and the backups that should have caught it.

This channel is made by someone who works inside a mobile network operations center.

CHAPTERS
0:00 [Açılış: ülke birkaç saniyede karanlıkta]
[m:ss] [12:32 – voltajın kontrolsüz yükselişi]
[m:ss] [Kademeli kopmalar ve İberya'nın Avrupa şebekesinden ayrılması]
[m:ss] [Şebeke nasıl dengede kalır: frekans ve voltaj]
[m:ss] [Neden yedekler yakalayamadı]
[m:ss] [Ülke yeniden nasıl başlatıldı]
[m:ss] [Bundan sonra ne değişiyor]

SOURCES
- Euronews – "Perfect storm" of multiple factors behind 2025 Iberia power blackout, experts say (20 Mar 2026): https://www.euronews.com/2026/03/20/perfect-storm-of-multiple-factors-behind-2025-iberia-power-blackout-experts-say
- pv magazine Europe – Expert report identifies causes of Iberian blackout: https://www.pveurope.eu/grid-connection/expert-report-identifies-causes-iberian-blackout
- Enlit – Final ENTSO-E report sheds light on multiple factors that caused Iberian blackout: https://www.enlit.world/library/final-entso-e-reports-sheds-light-on-multiple-factors-that-caused-iberian-blackout
- UKERC – Reflections from the Iberian blackout, one year on: https://ukerc.ac.uk/news/reflections-from-the-iberian-blackout-one-year-on/
- NESO – What is inertia?: https://www.neso.energy/energy-101/electricity-explained/how-do-we-balance-grid/what-inertia
- NESO – Restoration services (black start): https://www.neso.energy/industry-information/balancing-services/system-security-services/restoration-services

Series: Outage Files · How the Grid Fails
Watch the series: [How the Grid Fails oynatma listesi içi link]

VISUAL CREDITS
- Wikimedia Commons files as credited on screen; NASA/NOAA public-domain imagery; Pexels; Pixabay
Scenes marked "Reconstruction" are dramatised and do not depict real individuals.
```
> **Ne değişti:** İlk satır "Spain blackout explained" ile başlıyor; ikinci cümle "what caused the Iberian blackout" aramasını karşılıyor. Mart 2026'daki **nihai ENTSO-E uzman raporu** eklendi (aşırı gerilim kaynaklı zincirleme kopmalar; tek bir sebep değil; panel yenilenebilir enerjiyi tek başına sebep saymadı). **Videoda nihai rapordan bahsedilmiyorsa** ikinci cümleyi "What caused the Iberian blackout?" diye kısalt ve rapordan bahsetme. Seri linki eklendi.

### Etiketler
```
spain blackout, spain blackout explained, iberian blackout, portugal blackout, 28 april 2025 blackout, spain power outage cause, entso-e report, grid overvoltage, power grid explained, how the grid fails, blackout documentary, hidden systems, outage files, europe power grid, black start
```

### Sabit yorum
```
The final expert report on this blackout came out in March 2026: no single cause, but a chain — voltage rising out of control, then plants disconnecting one after another. Where were you when the lights went out, and what was the first thing that stopped working for you: phone, card payments, or water? Sources for every claim are in the description. Next in the series: [liste içi link]
```

### Oynatma listesi
- **How the Grid Fails** (1. sıra) · **Outage Files**
- Bitiş ekranı: HS-08 Winter Storm Elliott (9 Aralık'tan sonra) veya HS-07 bakır hat.

---

## 2) Hidden Systems: CrowdStrike outage (19 Temmuz 2024)

### Açıklama
```
The CrowdStrike outage explained: on 19 July 2024, one faulty content update crashed an estimated 8.5 million Windows computers and grounded flights, hospitals and banks. What actually went wrong in "Channel File 291" — a 21st field that the code didn't expect — and why it hit everywhere at once.

This channel is made by someone who works inside a mobile network operations center.

CHAPTERS
0:00 [Açılış: dünya çapında mavi ekran]
[m:ss] [19 Temmuz sabahı: havalimanları, hastaneler, bankalar]
[m:ss] [Güvenlik yazılımı neden işletim sisteminin bu kadar derininde]
[m:ss] [Channel File 291: 21 alan, 20 değer]
[m:ss] [Test neden yakalamadı]
[m:ss] [Neden tek tek elle düzeltilmesi gerekti]
[m:ss] [Ders: her şeyi aynı anda gönderme]

SOURCES
- CrowdStrike – Channel File 291 incident: Root cause analysis is available (Aug 2024): https://www.crowdstrike.com/en-us/blog/channel-file-291-rca-available/
- CrowdStrike – Executive summary, RCA Channel File 291 (PDF): https://crowdstrike.com/wp-content/uploads/2024/08/Executive-Summary_Root-Cause-Analysis_Channel-File-291.pdf
- TechCrunch – Microsoft says 8.5M Windows devices were affected by CrowdStrike outage (20 Jul 2024): https://techcrunch.com/2024/07/20/microsoft-says-8-5m-windows-devices-were-affected-by-crowdstrike-outage/
- TechTarget – CrowdStrike details errors that led to mass IT outage: https://www.techtarget.com/cybersecurity/news/366602392/CrowdStrike-details-errors-that-led-to-mass-IT-outage
- Reason J., "Human error: models and management", BMJ 2000 (the Swiss cheese model): https://pmc.ncbi.nlm.nih.gov/articles/PMC1070929

Series: Outage Files
Watch the series: [Outage Files oynatma listesi içi link]

VISUAL CREDITS
- Wikimedia Commons files as credited on screen; Pexels; Pixabay. No company logos are used.
Scenes marked "Reconstruction" are dramatised and do not depict real individuals.
```
> **Ne değişti:** İlk satır "CrowdStrike outage explained" ve "8.5 million Windows" (en çok aranan rakam) ile başlıyor. Kök neden raporundaki teknik ayrıntı (21 alan / 20 değer) tek cümlede veriliyor. **Videoda bu ayrıntı yoksa** "a 21st field that the code didn't expect" kısmını sil. İsviçre peyniri kaynağı, aynı konudaki bağımsız Short'la (Bağımsız Hafta 1, Short 3) bağ kuruyor.

### Etiketler
```
crowdstrike outage, crowdstrike outage explained, crowdstrike blue screen, channel file 291, windows blue screen july 2024, global it outage, 8.5 million windows devices, crowdstrike root cause, software update outage, outage files, hidden systems, tech documentary, cybersecurity outage, microsoft outage 2024
```

### Sabit yorum
```
CrowdStrike's own root cause report says the update defined 21 input fields, but the code only passed 20 — and the test that should have caught it didn't. Did the outage hit your workplace, your flight or your bank? And should critical systems be allowed to auto-update at all? Next in the series: [liste içi link]
```

### Oynatma listesi
- **Outage Files** (1. sıra)
- Bitiş ekranı: HS-04 Google jeneratör (11 Kasım'dan sonra).

---

## 3) Centworks: Kredi kartı şirketleri neden geç ödemeni ister?

### Açıklama
```
Why do credit card companies want you to pay late? In 2022, Americans paid more than $105 billion in credit card interest and $14.5 billion in late fees, according to the CFPB. Here's how card companies actually make money — interest, fees and the grace period — and what changed after the $8 late fee cap was thrown out in 2025.

This channel is made by an engineer, not a banker. Educational content, not financial advice.

CHAPTERS
0:00 [Açılış]
[m:ss] [Kart şirketi paranı nereden kazanır]
[m:ss] [Faizsiz süre (grace period) nasıl işler]
[m:ss] [Asgari ödeme tuzağı]
[m:ss] [Geç ödeme ücretleri: 14,5 milyar $]
[m:ss] [8 $ tavanı ve mahkeme kararı]
[m:ss] [Kendini korumanın yolları]

SOURCES
- CFPB – Report finds credit card companies charged consumers record-high $130 billion in interest and fees in 2022 (Oct 2023): https://www.consumerfinance.gov/about-us/newsroom/cfpb-report-finds-credit-card-companies-charged-consumers-record-high-130-billion-in-interest-and-fees-in-2022
- ABA Banking Journal – Court vacates CFPB credit card late fee rule (Apr 2025): https://bankingjournal.aba.com/2025/04/court-vacates-cfpb-credit-card-late-fee-rule/
- Holland & Knight – CFPB credit card late fees rule vacated by Texas district court: https://www.hklaw.com/en/insights/publications/2025/04/cfpb-credit-card-late-fees-rule-vacated-by-texas-district-court
- CFPB – What is a grace period for a credit card?: https://www.consumerfinance.gov/ask-cfpb/what-is-a-grace-period-for-a-credit-card-en-47/
- CFPB – The minimum payment box on your credit card statement: https://www.consumerfinance.gov/ask-cfpb/a-box-on-my-credit-card-bill-says-that-i-will-pay-off-the-balance-in-three-years-if-i-pay-a-certain-amount-what-does-that-mean-en-36/
- myFICO – What's in my FICO Scores?: https://www.myfico.com/crediteducation/whatsinyourscore.aspx

Series: Credit Cards Decoded
Next: Who really pays for your credit card rewards? [CW-04 linki — 14 Kasım'dan sonra]
```
> **Ne değişti:** İlk satır videonun başlığıyla aynı soruyu tekrar ediyor (arama eşleşmesi). İkinci satır CFPB'nin resmi rakamları. 8 $ geç ödeme ücreti tavanı **15 Nisan 2025'te mahkeme kararıyla iptal edildi**. Video bu karardan önce yayınlandıysa ve 8 $ tavanından "yürürlükte" diye bahsediyorsa, **açıklamaya ve sabit yoruma düzeltme notu ekle** (aşağıda hazır). Grace period ve FICO kaynakları bağımsız Short'larla bağ kuruyor.

### Etiketler
```
why credit card companies want you to pay late, credit card late fees, credit card interest, how credit card companies make money, cfpb credit card report, late fee rule vacated, $8 late fee cap, grace period credit card, minimum payment trap, credit card debt, centworks, credit cards decoded, personal finance, how money works
```

### Sabit yorum
```
Update: the CFPB's $8 cap on credit card late fees was vacated by a federal court in April 2025, so most issuers can again charge their earlier late fee amounts. The rest of the video still applies. Honest poll in the replies: do you pay your card in full every month — yes, mostly, or not yet? No judgement. Next in the series: who's really paying for card rewards. [liste içi link]
```
> İlk cümle yalnızca video 8 $ tavanını "yürürlükte" gibi anlatıyorsa kullanılır. Anlatmıyorsa "Update:" cümlesini sil.

### Oynatma listesi
- **Credit Cards Decoded** (1. sıra) · **Money Mechanics**
- Bitiş ekranı: CW-04 (14 Kasım'dan sonra).

---

## 4) Scam Engineer: Bankanın gerçek numarasından gelen arama (caller ID spoofing)

### Açıklama
```
A scam call from your bank's real number? Caller ID spoofing explained: scammers can make your phone show your bank's actual phone number. Here's, calmly, how spoofing works on the phone network, why STIR/SHAKEN call authentication doesn't stop every fake call, and the one rule that works every time: hang up and call the number on your card.

This channel is made by a telecom engineer.

CHAPTERS
0:00 [Açılış: ekranda bankanın gerçek numarası]
[m:ss] [Hikâye (yeniden canlandırma)]
[m:ss] [Arayan numara telefon ağında nasıl taşınır]
[m:ss] [Spoofing: numarayı kim yazıyor?]
[m:ss] [STIR/SHAKEN neyi çözer, neyi çözemez]
[m:ss] [Dolandırıcının istediği şey: kod, transfer, uygulama]
[m:ss] [Tek kural: kapat ve kartındaki numarayı ara]

WHERE TO REPORT
- FTC: https://reportfraud.ftc.gov
- FCC complaints: https://consumercomplaints.fcc.gov
- FBI IC3: https://www.ic3.gov

SOURCES
- FCC – Caller ID spoofing: https://www.fcc.gov/spoofing
- FCC – Combating spoofed robocalls with caller ID authentication (STIR/SHAKEN): https://www.fcc.gov/call-authentication
- FCC Consumer Advisory Committee – Recommendation regarding caller ID authentication: https://www.fcc.gov/sites/default/files/fcc_consumer_advisory_committee_recommendation_regarding_caller_id_authentication.pdf
- FTC – Top text scams of 2024 (fake bank fraud alerts): https://www.ftc.gov/news-events/data-visualizations/data-spotlight/2025/04/top-text-scams-2024
- FTC – How to recognize and avoid phishing scams: https://consumer.ftc.gov/articles/how-recognize-and-avoid-phishing-scams
- ABA Banking Journal – Banks ask FCC for highest call attestation: https://bankingjournal.aba.com/?p=42397

Series: Phone Scams · Scam Anatomy
More calm explainers: [Phone Scams oynatma listesi içi link]

Visual credits: Wikimedia Commons (as credited on screen), U.S. government public-domain materials, Pexels, Pixabay. Characters in reconstructions are composites.
```
> **Ne değişti:** İlk satır en çok aranan iki kalıbı içeriyor: "scam call from bank's real number" ve "caller ID spoofing explained". **Başlıkta "scam" kelimesi yoksa** `kucuk-resim-ab.md`'deki "scam" içeren başlık alternatifini test et. STIR/SHAKEN satırı **videoda yoksa** sil. "WHERE TO REPORT" bölümü eklendi (40+ kitle için en çok tıklanan kısım olması beklenir).

### Etiketler
```
scam call from bank real number, caller id spoofing, caller id spoofing explained, bank impersonation scam, spoofed call, stir shaken, fake bank fraud call, how scammers spoof numbers, bank fraud department scam, phone scam, scam engineer, scam awareness, protect your parents, hang up and call back
```

### Sabit yorum
```
The one rule: if a call shows your bank's number, hang up and call the number on the back of your card yourself. A real bank will never mind. Have you ever had a call that showed your bank's real number? What did the caller ask for first? Please don't post your number or any codes here. More calm explainers: [Phone Scams liste içi link]
```

### Oynatma listesi
- **Phone Scams** (1. sıra) · **Scam Anatomy** · **Protect Your Parents**
- Bitiş ekranı: SE-03 otoyol SMS'i (11 Kasım'dan sonra) veya SIM swap.

---

## 5) Yayınlanmış 4 Short

Bu Short'ların gerçek metinleri depoda yok. Aşağıdaki başlık ve açıklamalar her videonun ana konusuna göre yazıldı. **Short'un ilk ekran yazısı farklıysa** başlığı ona göre değiştir (başlık = ekran yazısı + 1 arama kelimesi kuralı, `yukleme-kontrol-listesi.md` §D).

| Short | Başlık (öneri) | Açıklama (yapıştır) | Related video | Hashtag |
|---|---|---|---|---|
| Spain blackout Short | `A whole country lost power in seconds #spainblackout` | `On 28 April 2025, Spain and Portugal went dark in seconds. The final expert report points to a chain of overvoltage disconnections. Sources: ENTSO-E expert panel final report (Mar 2026).` | Spain blackout uzun videosu | #spainblackout #blackout #powergrid #europe #hiddensystems |
| CrowdStrike Short | `One update. 8.5 million crashed PCs. #crowdstrike` | `In July 2024, one faulty CrowdStrike content update crashed an estimated 8.5 million Windows devices. Sources: CrowdStrike root cause analysis; Microsoft estimate via TechCrunch.` | CrowdStrike uzun videosu | #crowdstrike #outage #windows #tech #hiddensystems |
| Geç ödeme Short | `$14.5 billion in late fees #creditcard` | `In 2022, Americans paid $14.5 billion in credit card late fees and over $105 billion in interest (CFPB). Educational, not financial advice.` | Geç ödeme uzun videosu | #creditcard #latefees #debt #personalfinance #centworks |
| Spoofing Short | `Your bank's real number. A scam? #scamcall` | `Caller ID can be faked. If a call shows your bank's number, hang up and call the number on your card. Sources: FCC – Caller ID spoofing.` | Spoofing uzun videosu | #callerid #spoofing #scamcall #scamawareness #scamengineer |

**Short'lar için sabit yorum (dördü için ortak kalıp):**
```
Full explanation (with sources) in the related video linked above. What's one question you still have about this? We answer the best ones in future Shorts.
```
> "We answer the best ones in future Shorts" = yorumlara Short ile yanıt taktiği (`gelir/hizli-kazanimlar.md` #3). Söz verdiysen gerçekten yap.

---

## 6) Ek: S4 kapsamı dışındaki 3 yayınlanmış video (kısa)

Kullanıcı S4'ü 4 videoyla tanımladı. Diğer üçü için yalnızca **ilk iki satır + etiket + liste** önerisi:

| Video | Açıklamanın ilk iki satırı | Etiketler | Liste |
|---|---|---|---|
| Deprem: telefon şebekesi saatler sonra çöktü | `Why does the mobile network go down hours after an earthquake? Not because of the shaking — because of the batteries. Here's how backup power keeps phone masts running, and why it runs out.` | why phone network fails after earthquake, mobile network backup power, cell tower battery, phone outage disaster, emergency calls, telecom explained, hidden systems | Phone Networks Explained |
| Bankalar parayı yoktan nasıl yaratır | `How do banks create money out of nothing? When a bank makes a loan, it creates a new deposit — that's how the Bank of England explains it. Here's what that means for your savings and for inflation.` | how banks create money, money creation explained, fractional reserve myth, bank of england money creation, how money works, centworks | Money Mechanics |
| SIM swap | `SIM swap scam explained: how someone moves your phone number to their SIM card and gets your security codes — and the free account lock that stops it. Under FCC rules, carriers must alert you to SIM change requests.` | sim swap scam, sim swap explained, phone number hijack, account lock carrier, fcc sim swap rule, two factor code scam, scam engineer | Phone Scams |

> İddialar videoda geçmiyorsa kısalt. Kaynak listesi gerekirse bir sonraki turda araştırılıp eklenir.
