# Hidden Systems: Bağımsız Shorts, Hafta 2 (16–22 Kasım 2026)

**Kurallar:** [`shorts-bagimsiz-hafta-1.md`](shorts-bagimsiz-hafta-1.md) ile aynı.

| Gün | Short | Format | Related video |
|---|---|---|---|
| Sal 17 Kas | 5. Haritadan silinen şirket | Zaman çizelgesi | CrowdStrike (yayınlanmış) |
| Çar 18 Kas | 6. 45 dakikada 460 milyon | Rakam çatışması | HS-05 First Brands (18 Kas, videodan sonra) |
| Cum 20 Kas | 7. Tek satır kod | Tek gizem | CrowdStrike |
| Pzt 22 Kas | 8. Uydu saati | Gizli süper güç | Deprem/telefon şebekesi (yayınlanmış) |

---

## Short 5 — 17 Kas | Zaman çizelgesi: Haritadan silinen şirket (~36 sn)

| Zaman | Görsel | Ekran yazısı |
|---|---|---|
| 0–2 sn | **Hareketli:** Bir internet haritasında bir düğüm sönüyor, bağlantı çizgileri tek tek kopuyor | FACEBOOK VANISHED FROM THE MAP. |
| 2–12 sn | Veri merkezleri arası hatlar (kendi animasyon) | ONE MAINTENANCE COMMAND |
| 12–24 sn | "DNS: not found" ekran grafiği | THE INTERNET COULDN'T FIND IT |
| 24–36 sn | Saat: 6 saat | ABOUT SIX HOURS |

**VO:**
> Facebook vanished from the map.
> October 2021. During routine maintenance, a command meant to check the network's capacity accidentally cut every connection in Facebook's backbone between its data centres. Then its address servers did what they were built to do when cut off: they stopped announcing themselves to the rest of the internet. For about six hours, Facebook, Instagram and WhatsApp simply couldn't be found. Nothing was hacked. The road signs just disappeared. And that's the day Facebook…

**Döngü:** "…the day Facebook…" → "Facebook vanished from the map."
**Kaynak:** Meta Engineering – More details about the October 4 outage (engineering.fb.com, 5 Oct 2021); Computer Weekly – Facebook unplugged for six hours due to configuration error
**Açıklama notu:** Related video bağlantısı: *<yayınlanmış CrowdStrike videosunun başlığı>*
**Hashtag:** #facebookdown #bgp #internet #outage #hiddensystems

---

## Short 6 — 18 Kas | Rakam çatışması: 45 dakikada 460 milyon (~36 sn)

| Zaman | Görsel | Ekran yazısı |
|---|---|---|
| 0–2 sn | **Hareketli:** Sayaç dolar sembolüyle hızla yükseliyor, yanında 45:00'tan geri sayan saat | $460 MILLION LOST IN 45 MINUTES. |
| 2–12 sn | Borsa ekranı (Pexels, marka yok) | 1 AUGUST 2012 |
| 12–24 sn | 8 sunucu ikonu; biri kırmızı yanıyor | OLD CODE WOKE UP |
| 24–36 sn | "4,000,000 orders" vs "212 orders" | 4 MILLION ORDERS FOR 212 |

**VO:**
> $460 million lost in 45 minutes.
> August 2012. Knight Capital, one of the biggest traders of US shares, switched on new software. On one of its eight servers, old code that should have been retired woke up instead. In the first 45 minutes of trading, its system sent more than four million orders while trying to fill just 212 customer orders. The SEC later said the firm lost more than 460 million dollars. Automated warnings had gone out before the market opened. That's the price of one forgotten switch:

**Döngü:** "…one forgotten switch:" → "$460 million lost in 45 minutes."
**Kaynak:** U.S. SEC – Knight Capital settlement, 16 Oct 2013 (sec.gov/news/digest/2013/dig101613.htm); Knight Capital Form 10-Q, Q2 2012
**Açıklama notu:** Related video bağlantısı: *The $10 Billion Company That Was Built on Invoices* (HS-05)
**Hashtag:** #knightcapital #stockmarket #software #companycollapse #hiddensystems

---

## Short 7 — 20 Kas | Tek gizem: Tek satır kod (~34 sn)

| Zaman | Görsel | Ekran yazısı |
|---|---|---|
| 0–2 sn | **Hareketli:** Tek bir kod satırı yazılıyor, sonra dünya haritasında tüm noktalar aynı anda kırmızıya dönüyor | ONE LINE OF CODE. 27 MINUTES. |
| 2–14 sn | CPU göstergeleri %100'e fırlıyor | EVERY CPU AT 100% |
| 14–24 sn | Tarayıcıda "502 Bad Gateway" | WEBSITES RETURNED ERRORS |
| 24–34 sn | Harita üzerinde aşamalı yayılım: önce bir nokta, sonra bölge, sonra dünya | NOW: SLOW, IN STAGES |

**VO:**
> One line of code. 27 minutes.
> July 2019. Cloudflare, which sits in front of millions of websites, pushed a new firewall rule to every server in the world at once. Inside it was a pattern-matching expression that, on certain traffic, made processors try more and more combinations. CPUs everywhere hit one hundred percent, and websites returned errors. Cloudflare says the outage lasted 27 minutes. Its fix wasn't just the bad line. It was never sending a change everywhere at once. Because it all started with…

**Döngü:** "…started with…" → "One line of code. 27 minutes."
**Kaynak:** Cloudflare Blog – Details of the Cloudflare outage on July 2, 2019
**Açıklama notu:** Related video bağlantısı: *<yayınlanmış CrowdStrike videosunun başlığı>*
**Hashtag:** #cloudflare #outage #regex #softwareengineering #hiddensystems

---

## Short 8 — 22 Kas | Gizli süper güç: Uydu saati (~33 sn)

| Zaman | Görsel | Ekran yazısı |
|---|---|---|
| 0–2 sn | **Hareketli:** Bir baz istasyonu direği; gökyüzünden ince bir zaman sinyali çizgisi iniyor (NASA/GPS.gov kamu malı uydu görseli) | YOUR PHONE NETWORK LISTENS TO SATELLITES. |
| 2–12 sn | Atom saati simgesi | NOT FOR LOCATION. FOR TIME. |
| 12–24 sn | İki direk; sinyaller çakışıyor, sonra hizalanıyor | MASTS MUST STAY IN SYNC |
| 24–33 sn | Ekipman odasında yedek saat kutusu (Pexels) | BACKUP CLOCKS ON SITE |

**VO:**
> Your phone network listens to satellites.
> Not for location. For time. Mobile masts have to stay precisely in sync, so millions of phones can share the same airwaves without talking over each other. Many masts take that timing from GPS satellites, which carry atomic clocks. The US government's GPS site says wireless networks use GPS time to keep their base stations synchronised. That's why network engineers worry about jamming, and keep backup clocks. Full bars on your screen? That's because your phone network listens…

**Döngü:** "…your phone network listens…" → "Your phone network listens to satellites."
**Kaynak:** GPS.gov – Timing applications (archive.gps.gov/applications/timing); ATIS report on GPS timing dependency (GPS.gov, 2016)
**Açıklama notu:** Related video bağlantısı: *<yayınlanmış deprem/telefon şebekesi videosunun başlığı>*
**Hashtag:** #gps #mobilenetwork #telecom #engineering #hiddensystems
