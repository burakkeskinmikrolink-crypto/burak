# Finans Kanalı – Strateji ve Ücretsiz Üretim Hattı

> Rakamlar blog/araç sitelerinden; denetlenmiş veri değil. Kendi YouTube Studio verinle doğrula.

## 1. Neden finans?
- Faceless kanallarda CPM'i en yüksek niş: kişisel finans/yatırım ~$15–40 CPM, creator RPM kabaca $8–25.
- Reklam dışında gelir: affiliate (aracı kurum, bütçe uygulaması, kurs), sponsor, ürün.
- Animasyonlu hikâye nişi ~$9–13 RPM; finans bunun yaklaşık 1,5–2 katı.

## 2. İki kritik bulgu
### a) Dil/ülke her şeyden önemli
- Türkiye RPM tahminleri çok düşük (~$0.2–1.5 / 1000 izlenme, kaynaklar tutarsız).
- ABD/UK/Kanada/Avustralya izleyicisi 10–50 kat fazla öder.
- **Öneri:** Ana kanal İngilizce (Tier-1 izleyici). Türkçe versiyon, aynı senaryoyu çevirerek ikinci aşamada denenebilir (düşük gelir ama ek maliyet yok).

### b) YouTube "inauthentic content" politikası
- Toplu üretilen, şablon, sadece konu/başlık değişen videolar kanal bazında gelir dışı kalabilir.
- AI "persona"nın finans/sağlık/hukuk tavsiyesi vermesi monetize edilmeyen kategoride.
- Çözüm: **eğitim odaklı** anlatım ("X nasıl çalışır"), yatırım tavsiyesi verme, özgün araştırma + kendi yazdığın senaryo + kendi kurgun, her videoda farklı yapı. Haftada 2–3 kaliteli video, günde 5 çöp video değil.
- Resmi kaynak: YouTube Partner Program politikaları sayfasını oluşturmadan önce kontrol et (Temmuz 2026 rehberi ve olası 2027 eşik değişikliği tek kaynaktan, doğrulanmadı).

## 2b. Önceki sohbetteki karar (korundu)
- Kanal: **İngilizce, animasyonlu "para ve ekonomi nasıl işler"** eğitim kanalı. Yatırım tavsiyesi yok, mekanizma anlatımı var.
- Neden uyuyor: finans anlatımı grafik/eğri/sayıya dayanır; kodla animasyon için ideal, tamamen ücretsiz kalır.
- Mevsim: finans CPM'i yıl içinde dalgalanır (kaynağa göre ocakta ~18–20, kasımda ~35–40 $). Sonbahar açılışı yüksek dönemle örtüşür.
- Gelir örneği: 100 bin izlenme/ay × ~10 $ RPM ≈ 1.000 $/ay (yalnız reklam). Affiliate ve sponsor eklenince artar; ilk gelir orta rekabette 3–6 ay.
- Elenenler: ABD'li yaşlılara hikâye fabrikası (politika riski), uyku/ASMR (düşük RPM, tekrar riski). İkinci sıra: B2B/otomasyon (Apps Script) kendi işini gösteren kanal.
- **Sınır:** Hidden Systems = "sistemler nasıl çöker"; bu kanal = "para nasıl işler". Konular çakışmasın.

## 3. Konumlandırma
"Karmaşık para konularını 8 dakikada animasyonla anlatan kanal."
Konu havuzu: enflasyon, bileşik faiz, merkez bankaları, borsa temelleri, ETF vs hisse, kredi puanı, vergi temelleri, ekonomi tarihi (1929, 2008), şirket nasıl para kazanır.
Kaçın: "şunu al/sat", garanti getiri, kripto pump, kişisel finansal tavsiye. Her videoya "eğitim amaçlıdır, yatırım tavsiyesi değildir" notu.

## 4. Ücretsiz üretim hattı
| Adım | Araç (ücretsiz) |
|---|---|
| Konu/anahtar kelime | YouTube arama otomatik tamamlama, Google Trends, rakip kanalların en çok izlenen videoları |
| Araştırma | Resmi kaynaklar (FRED, World Bank, SEC, merkez bankası), kaynakları not et |
| Senaryo | Sen yazarsın, Claude taslak/denetim yardımcı olur (insan katkısı şart) |
| Ses | Kokoro TTS (yerel, ücretsiz; `pipeline/uret_kokoro.py`), yedek: `edge-tts` (`uret.py`) |
| Görsel | Kodla animasyon: matplotlib (`animasyon/bilesik_faiz.py` çalışan örnek), Manim; Canva/Inkscape ek |
| Kurgu | DaVinci Resolve veya CapCut ücretsiz, otomasyon için ffmpeg |
| Altyazı | Whisper (yerel) |
| Thumbnail | Canva / Photopea |
| Analiz | YouTube Studio |

`pipeline/` klasöründeki betik: senaryo metninden ses + altyazı (SRT) üretir. Kurgu ve görsel insan işi kalır, bu bilerek böyle.

## 5. 90 gün yol haritası
- **Hafta 1:** Kanal adı, logo, banner, ilk 10 konu, 3 senaryo.
- **Hafta 2–4:** 6–8 video. Her biri kendi araştırma + özgün grafik.
- **Ay 2:** Analitik; en iyi 2 formatı çoğalt, zayıfı bırak. Shorts: videodan kesit.
- **Ay 3:** Affiliate linkleri, e-posta listesi (ücretsiz Substack), topluluk sekmesi.
- Monetizasyon eşiği: 1.000 abone + 4.000 izlenme saati (veya 10M Shorts izlenme). Eşiğin değişebileceğini kontrol et.

## 6. Gerçekçi beklenti
İlk 3–6 ay gelir yok denecek kadar az. Başarı verisi olarak: ilk 10 videoda tutma oranı (>%40) ve tıklanma oranı (>%4).
