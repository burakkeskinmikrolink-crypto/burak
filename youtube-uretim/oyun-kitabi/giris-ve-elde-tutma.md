# 1. Giriş ve elde tutma (uzun video)

**Sorunumuz:** İzleyicinin %58'i ilk 40 saniyede ayrılıyor, sonrasında eğri düz gidiyor.
**Teşhis:** Eğrinin sonrası düzse video içeriği izleyiciyi tutuyor demektir. Sorun neredeyse tamamen **paketleme ile ilk 40 saniye arasındaki köprüde**. Bu iyi haber: düzeltilecek alan küçük ve ölçülebilir.

**Güven düzeyleri:**
- **Yüksek:** YouTube'un resmî kaynağı, akademik çalışma veya kamu kurumu.
- **Orta:** Saygın haber kaynağı, büyük veri setine dayanan şirket analizi ya da doğrulanmamış ama tutarlı belge.
- **Düşük:** Yöntemi belirsiz blog veya tek vaka.

> Not: Bu oturumda doğrudan sayfa açma (WebFetch) engelliydi. Bulgular WebSearch sonuç özetlerinden alındı. Linkleri bir kez açıp kontrol et.

---

## A. Ölçüm: "Intro" metriği tam olarak ne söylüyor?

| Bulgu | Kaynak | Güven |
|---|---|---|
| YouTube Studio'daki **Intro** metriği, izleyicilerin yüzde kaçının ilk 30 saniyeden sonra hâlâ izlediğini gösterir. Yüksek bir Intro değeri, açılışın küçük resim ve başlıkla uyuştuğunu ve içeriğin ilgiyi tuttuğunu yansıtabilir. | [YouTube Help – Measure key moments for audience retention](https://support.google.com/youtube/answer/9314415) | Yüksek |
| "Spikes" bir bölümün tekrar izlendiğini ya da paylaşıldığını, "Dips" ise terk edildiğini veya atlandığını gösterir. Veri yalnızca video düzeyindedir ve işlenmesi 1–2 gün sürer. | Aynı sayfa | Yüksek |
| YouTube evrensel bir "iyi elde tutma" oranı yayınlamıyor. Öneri, benzer uzunluktaki kendi videolarınla karşılaştırmak. | [vidIQ](https://vidiq.com/blog/post/increase-audience-retention-youtube/), [SocialRails](https://socialrails.com/blog/youtube-audience-retention-complete-guide) | Orta |
| "30 saniyede %50+ kalan videolar 'above typical intros' listesine girer" iddiası resmî kaynakta doğrulanamadı. | [Creator Essentials](https://www.creatoressentials.com/glossary/intro-retention/) | Düşük |
| Retention Rabbit'in 2025 kıyas raporu (10.000+ video): platform ortalaması %23,7, videoların yalnızca ~%16,8'i izleyicinin yarısından fazlasını tutuyor. Rakamlar ikincil kaynaklardan alındı. | [Retention Rabbit 2025 raporu (çeviri bağlantısı)](https://translate.google.com/translate?u=https://www.retentionrabbit.com/blog/2025-youtube-audience-retention-benchmark-report&hl=es&sl=en&tl=es&client=srp) | Orta-Düşük |
| YouTube'un sistemleri izleyicilere ayda milyonlarca memnuniyet anketi gösteriyor ve anketler öneri sistemini eğitmek için en önemli verilerden biri (Creator Insider'daki ürün yöneticisi açıklaması, vidIQ aktarımı). | [vidIQ – What the algorithm likes](https://vidiq.com/blog/post/youtube-algorithm-loves-these-video-metrics/) | Orta |

**Bizim için okuma:** %58'i 40 saniyede kaybetmek, Intro (30 sn) değerimizin kabaca **%45 civarında** olduğu anlamına geliyor. İlk iş olarak her videonun Intro değerini aynı uzunluktaki diğer videolarla karşılaştır. Hangi açılış türünün daha iyi tuttuğunu kendi verimiz söyleyecek.

---

## B. İlk 30–60 saniye: kanıtı olan teknikler

| # | Teknik | Kaynak / dayanak | Güven |
|---|---|---|---|
| 1 | **Paketlemeyle açılış uyumu.** İlk saniyeler, küçük resimdeki ve başlıktaki vaadi hemen doğrulamalı. Uyumsuzluk, ilk 30 saniyedeki terkin bir numaralı nedeni olarak tarif ediliyor. | [YouTube Help (Intro tanımı)](https://support.google.com/youtube/answer/9314415) | Yüksek |
| 2 | **İlk dakika en kritik dakika.** Sızdırılan MrBeast üretim rehberine göre izleyicilerin çoğu ilk 60 saniyede gidiyor. Açılış, küçük resimdeki beklentiyi karşılamalı ve hikâye hızla ilerlemeli. Örnek: "ilk 3 dakikayı ilk güne harcama". | [GIGAZINE](https://gigazine.net/gsc_news/en/20240917-mrbeast-youtube-production/), [Dexerto](https://www.dexerto.com/youtube/leaked-mrbeast-pdf-reveals-youtubers-secrets-to-video-success-2900841/) | Orta (belgenin gerçekliği resmî olarak doğrulanmadı) |
| 3 | **Yeniden bağlama (re-engagement) anları.** Aynı belgeye göre ~3. ve ~6. dakikada güçlü bir yeni gelişme ya da sürpriz konmalı. | Aynı kaynaklar | Orta |
| 4 | **Merak boşluğu (açık döngü).** Loewenstein'ın bilgi boşluğu kuramına göre merak, insan bilmediği ama ulaşılabilir görünen bir bilginin farkına varınca doğar. En güçlü merak, izleyicinin bir tahmini olduğu ama emin olmadığı anda ortaya çıkar. Hiç ön bilgisi olmayan konuda merak oluşmaz. | Loewenstein (1994), *Psychological Bulletin*; özet: [Nautilus](https://nautil.us/curiosity-depends-on-what-you-already-know-235803), [PBS NOVA](https://www.pbs.org/wgbh/nova/article/how-to-stimulate-curiosity/) | Yüksek (akademik) |
| 5 | **Hemen içeriğe gir.** "Hey guys, welcome back" türü girişler en pahalı kelimeler olarak tarif ediliyor. Eğitim kanalları için yazan senaristler ilk 30 saniyeyi her zaman yeniden yazıyor. | [Bryan Ng (X)](https://x.com/boomerrbryan/status/2104476454264373703) | Düşük (uzman görüşü) |
| 6 | **İlk 60 saniyeden sonrası.** ilk dakikayı %65'ten fazla izleyiciyle geçen videoların geri kalan ortalama izlenme süresi %58 daha yüksek. | [Retention Rabbit özeti (ikincil)](https://translate.google.com/translate?u=https://www.retentionrabbit.com/blog/2025-youtube-audience-retention-benchmark-report&hl=es&sl=en&tl=es&client=srp) | Düşük |

### Hook türleri ve hangi kanalda ne zaman kullanılır

| Hook türü | Örnek (bizim konulardan) | En uygun kanal |
|---|---|---|
| **Sonuçla açılış (cold open)** | "One building in London lost power — and Britons couldn't reach their money." | Hidden Systems |
| **Somut rakam şoku** | "Each penny cost almost four cents to make." | Centworks |
| **Yanlış inanışı yıkma** | "The padlock doesn't mean the site is safe." | Scam Engineer |
| **Sahnenin ortasından giriş (in medias res)** | Kasada "DECLINED" ekranı, hiçbir açıklama yapmadan | Hepsi |
| **Kişisel bahis** | "Your rewards card might not be welcome next year." | Centworks |

**Seçim kuralı:** Hook, küçük resimde **görünen şeyi** ilk 3 saniyede sese ve görüntüye dökmeli. Küçük resimde jeneratör varsa ilk karede jeneratör olmalı, ilk cümlede de "generator" kelimesi geçmeli.

---

## C. Tempo ve sahne değişimi

| Bulgu | Kaynak | Güven |
|---|---|---|
| Sahne değişim sıklığının elde tutmaya etkisini ölçen hakemli bir çalışma bulunamadı. Piyasada dolaşan "her 3 saniyede kesme" kuralları veriye dayanmıyor. | Arama sonucunda birincil veri çıkmadı | — |
| Yüzü olmayan (faceless) kanallarda görsel değişimin, anlatıcının yüzünün işlevini üstlendiği deneyimle sabit bir uygulama. | [Virvid – faceless algorithm (blog)](https://virvid.ai/blog/faceless-youtube-algorithm-retention-2026) | Düşük |

**Bizim uygulama kuralımız (deneyim kuralı, veriye dayalı değil, kendi verimizle test edilmeli):**
- **İlk 30 saniye:** Her 2–4 saniyede bir görsel değişim olsun (kesme, zoom, yazı, harita). Aynı stok görüntü 5 saniyeden uzun ekranda kalmasın.
- **30 sn – 2 dk:** Görsel değişim her 4–6 saniyede bir. Her yeni bilgide ekranda bir şey değişmeli.
- **Ders kısımları:** Animasyon, diyagram ve rakam grafikleri. "Konuşan stok görüntü" yerine anlatılanı gösteren grafik kullan.
- **Ses:** Sahne geçişlerinde 300–600 ms nefes payı, sonra kısa bir ses vurgusu (whoosh değil, ince bir ton). Ayrıntılar [gorsel-ve-ses.md](gorsel-ve-ses.md) içinde.

---

## D. Bizim senaryolarımız için ilk 40 saniye şablonu (v2)

Mevcut kural setimiz (şok cümlesi → vaat → kimlik → hikâye → 45. saniyeden sonra ders) doğru yönde. Ama elimizdeki %58 kayıp, **kimlik cümlesinin ve vaat cümlesinin momentum kırdığını** düşündürüyor. Bu bir hipotez ve test edilmeli.

| Zaman | Ne olmalı | Neden |
|---|---|---|
| 0–3 sn | Küçük resimdeki nesne ekranda + şok cümlesinin ilk yarısı | Paketleme uyumu (Help) |
| 3–8 sn | Şok cümlesinin somut sonucu (kim, ne kaybetti) | Bahsi somutlaştırmak |
| 8–14 sn | **Kısa ve somut vaat (≤15 kelime):** "By the end, you'll know the one switch that should have saved it." | Merak boşluğu: ulaşılabilir bir cevap (Loewenstein) |
| 14–20 sn | **Kimlik, hikâyenin içine gömülü (≤12 kelime):** "In my network control room, we rehearse this exact failure." | Kural korunur, ama ayrı bir "tanıtım" cümlesi gibi durmaz |
| 20–35 sn | Dramatize sahne: insan + an + tek bir gerilim detayı | Hikâye önce |
| **35–40 sn** | **İlk açık soru** (şu an ~50. saniyede) | Terk penceresi 40. saniyede kapanmadan yeni bir döngü aç |

**En önemli değişiklik:** İlk merak sorusunu 50. saniyeden **35–40. saniyeye** çekmek. İzleyicinin %58'i 40. saniyeye kadar gidiyor, yani onları tutacak soru bu pencerenin içinde gelmeli.

---

## E. Test planı (önümüzdeki 4 video)
1. Her videoda Intro (30 sn) yüzdesini ve 40. saniyedeki kalan izleyici oranını bir tabloya yaz.
2. İki açılış türünü dönüşümlü dene: (a) sonuçla açılış, (b) sahnenin ortasından giriş.
3. Kimlik cümlesini bir videoda ayrı cümle olarak, bir videoda hikâyeye gömülü olarak dene.
4. Küçük resmi Test & Compare ile test ederken Intro değerine de bak. Daha çok tıklanan ama Intro'su düşük olan küçük resim, YouTube'un izlenme süresi ölçütüne göre zaten kaybedecektir ([baslik-ve-kucuk-resim.md](baslik-ve-kucuk-resim.md)).
