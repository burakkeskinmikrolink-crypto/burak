# Hidden Systems: Shorts v2, Bölüm 06 (AWS soğutma)

- **Ana video:** `06-v2.md`, yayın 25 Kasım 2026
- **Önerilen takvim:** 26, 28 ve 30 Kasım
- **Kurallar:** [shorts_04-v2.md](shorts_04-v2.md) dosyasındaki v2 kuralları.

---

## Short 1: Fizik dersi (~34 sn)

| Zaman | Görsel | Ekran yazısı |
|---|---|---|
| 0–2 sn | **Hareketli:** Sunucu rafı ısı kamerası efektiyle maviden kırmızıya dönüyor | EVERY SERVER IS A HEATER. |
| 2–12 sn | Animasyon: elektrik → ısı | POWER IN = HEAT OUT |
| 12–22 sn | Termometre yükseliyor | COOLING FAILS → SERVERS SWITCH OFF |
| 22–34 sn | Donan kripto grafik ekranı (kendi grafik) | VIRGINIA · MAY 2026 |

**VO:**
> Every server is a heater.
> Almost all the electricity a server uses turns into heat. So a data centre is really a giant heater that happens to do maths.
> When cooling fails, servers have one safe move: switch themselves off. That's what happened in an Amazon data hall in Virginia in May 2026, and Coinbase's core trading was disrupted for hours.
> Heat, not hackers. Because, whatever the cloud feels like…

**Döngü:** "…whatever the cloud feels like…" → "Every server is a heater."
**Açıklama notu:** Related video bağlantısı: *A Room Got Too Hot. A Crypto Exchange Went Dark.* (HS-06 v2)
**Hashtag:** #aws #datacenter #coinbase #outage #hiddensystems

---

## Short 2: Soru-cevap (~33 sn)

| Zaman | Görsel | Ekran yazısı |
|---|---|---|
| 0–2 sn | **Hareketli:** Büyük bir "ON" anahtarına parmak uzanıyor, anahtar titreyip kırmızıya dönüyor | WHY NOT TURN IT BACK ON? |
| 2–12 sn | Elektrik kesintisi ikonu → yeşil | POWER CUT: SWITCH BACK ON |
| 12–24 sn | Sıcak oda ikonu, termometre yavaşça düşüyor | COOLING FAILURE: WAIT |
| 24–33 sn | Sunucular aşama aşama yeşile dönüyor | RESTART IN STAGES |

**VO:**
> Why not turn it back on?
> After a power cut, you often can. After a cooling failure, you can't. The room is still hot, and servers brought back too early trip again, or get damaged.
> Engineers restore cooling, wait for the temperature to fall, then restart hardware in stages. That's why an Amazon cooling failure in Virginia took well into the next day to settle. And the first thing everyone asked was:

**Döngü:** "…everyone asked was:" → "Why not turn it back on?"
**Açıklama notu:** Related video bağlantısı: *A Room Got Too Hot. A Crypto Exchange Went Dark.* (HS-06 v2)
**Hashtag:** #aws #cloud #engineering #datacentre #hiddensystems

---

## Short 3: Görsel karşılaştırma (~36 sn)

| Zaman | Görsel | Ekran yazısı |
|---|---|---|
| 0–2 sn | **Hareketli:** "2" ve "3" rakamları ekrana dönerek geliyor | WHY THREE BEATS TWO. |
| 2–12 sn | İki kutu, biri kararıyor, "MAJORITY?" | LOSE ONE → NO MAJORITY |
| 12–22 sn | Üç kutu, biri kararıyor, iki kutu "✓" | LOSE ONE → 2 OF 3 DECIDE |
| 22–36 sn | "2 zones → 3 zones" metin grafiği | COINBASE'S FIX |

**VO:**
> Why three beats two.
> Many systems keep data consistent by voting: a change only counts when a majority agrees. With two locations, lose one, and there's no majority. With three, lose one, and the other two still decide.
> After the Amazon cooling failure in May 2026, Coinbase said it would move a key messaging system from two zones to three. A backup waits to be switched on. A quorum keeps working. And that's exactly…

**Döngü:** "…that's exactly…" → "…why three beats two."
**Açıklama notu:** Related video bağlantısı: *A Room Got Too Hot. A Crypto Exchange Went Dark.* (HS-06 v2)
**Hashtag:** #distributedsystems #aws #coinbase #engineering #hiddensystems
