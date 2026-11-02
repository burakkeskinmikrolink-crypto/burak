# Hidden Systems: Shorts, Bölüm 06 (AWS us-east-1 soğutma arızası)

- **Ana video:** `06.md`, yayın 25 Kasım 2026
- **Önerilen Short takvimi:** 26, 28 ve 30 Kasım
- **Ses:** İngiliz belgesel anlatıcısı

---

## Short 1: "Fizik dersi" (tek fikir)
- **Süre:** ~35 sn
- **Hook:** EVERY SERVER IS A HEATER

| Zaman | Görsel | Ekran yazısı |
|---|---|---|
| 0–4 sn | Sunucu rafı, ısı kamerası efekti (Pixabay + renk efekti) | EVERY SERVER IS A HEATER |
| 4–14 sn | Animasyon: elektrik → ısı | ELECTRICITY IN = HEAT OUT |
| 14–24 sn | Termometre yükseliyor | COOLING FAILS → SERVERS SWITCH OFF |
| 24–35 sn | Kripto grafik ekranı donuyor (kendi grafik) | MAY 2026 · COINBASE TRADING DISRUPTED |

**VO (tam metin):**
> Here's the physics the cloud doesn't advertise. Almost all the electricity a server uses turns into heat. A data centre is basically a giant heater that happens to do maths.
> So when cooling fails, servers have one safe option: switch themselves off.
> That's what happened in an Amazon data hall in Virginia in May 2026. Several cooling units failed, servers shut down, and Coinbase's core trading was disrupted for hours.
> Heat, not hackers. Full story on Hidden Systems.

**Açıklama:** Veri merkezlerinin görünmeyen düşmanı ısı. AWS us-east-1 "thermal event" (Mayıs 2026).
**Hashtag:** #aws #datacenter #coinbase #outage #hiddensystems
**Kaynak:** Network World, Quartz, Coinbase retrospektifi (haberler üzerinden)

---

## Short 2: "Neden hemen açamıyorlar?" (soru-cevap)
- **Süre:** ~35 sn
- **Hook:** WHY NOT JUST TURN IT BACK ON?

| Zaman | Görsel | Ekran yazısı |
|---|---|---|
| 0–4 sn | Büyük bir "ON" anahtarı | WHY NOT JUST TURN IT BACK ON? |
| 4–14 sn | Elektrik kesintisi ikonu → anahtar yeşil | POWER CUT: SWITCH BACK ON |
| 14–26 sn | Sıcak oda ikonu → termometre yavaşça düşüyor | COOLING FAILURE: WAIT FOR THE ROOM TO COOL |
| 26–35 sn | Sunucular aşama aşama yeşile dönüyor | THEN RESTART IN STAGES |

**VO (tam metin):**
> When a data centre loses power, you can often switch it back on. When it loses cooling, you can't.
> The room is still hot. Bring servers back too early and they trip again, or get damaged.
> So engineers restore cooling, wait for the temperature to fall below safe limits, then restart hardware in stages.
> That's why an Amazon cooling failure in Virginia in May 2026 took well into the next day to fully settle. You can't wake a room until you've cooled it.

**Açıklama:** Soğutma arızası elektrik kesintisinden neden daha yavaş toparlanır?
**Hashtag:** #aws #cloud #engineering #datacentre #hiddensystems
**Kaynak:** Network World, Tech-Insider (zaman çizelgesi), AWS Health Dashboard

---

## Short 3: "İki mi, üç mü?" (görsel karşılaştırma)
- **Süre:** ~40 sn
- **Hook:** WHY 3 IS SAFER THAN 2

| Zaman | Görsel | Ekran yazısı |
|---|---|---|
| 0–4 sn | İki kutu yan yana | 2 COPIES |
| 4–14 sn | Biri kararıyor, "MAJORITY?" soru işareti | LOSE ONE → NO MAJORITY |
| 14–24 sn | Üç kutu, biri kararıyor, iki kutu "✓" | LOSE ONE → 2 OF 3 STILL DECIDE |
| 24–40 sn | "Kafka: 2 zones → 3 zones" metin grafiği | COINBASE'S FIX AFTER MAY 2026 |

**VO (tam metin):**
> Why do engineers love the number three?
> Many systems keep data consistent by voting. A change only counts when a majority of copies agree.
> With two locations, lose one, and there's no majority left. With three, lose one, and the other two still decide.
> After the Amazon cooling failure in May 2026, Coinbase said it would move a key messaging system from two zones to three.
> A backup waits for you to switch to it. A quorum keeps working while part of it is gone.

**Açıklama:** Yedek ile çoğunluk (quorum) arasındaki fark. Coinbase'in AWS kesintisinden sonraki düzeltmesi.
**Hashtag:** #distributedsystems #aws #coinbase #engineering #hiddensystems
**Kaynak:** Coinbase retrospektifi (Cointelegraph, FX News Group üzerinden). Oylama ilkesi genel bilgidir, Coinbase'in kök nedeni olarak sunulmuyor.
