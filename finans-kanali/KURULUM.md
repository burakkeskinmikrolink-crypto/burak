# Kurulum: Sıfırdan Adım Adım

## A. Hesaplar (ücretsiz, ~30 dk)
1. Yeni bir Google hesabı aç (ana hesabından ayrı; kanal ve AdSense için temiz kalsın).
2. youtube.com → profil → "Kanal oluştur" → **Marka hesabı** olarak oluştur (ileride yönetici ekleyebilirsin).
3. Kanal ayarları: ülke = senin ülken (ödemeler için), içerik dili = İngilizce, anahtar kelimeler = ekonomi, para, iş modelleri.
4. Telefonla doğrulama (youtube.com/verify) → 15 dk+ videolar ve özel küçük resim açılır.
5. İki adımlı doğrulamayı aç.
6. Kanal adı: kısa, söylenebilir, `.com` ve @handle müsait olsun. "Hidden Systems"ten ayrı bir marka olmalı.

## B. Marka (ücretsiz)
- Logo/banner: Canva ücretsiz şablon. Renkler: koyu arka plan + 1 vurgu rengi (örnekteki gibi yeşil).
- Banner 2560×1440, güvenli alan ortada 1546×423.
- Hakkında metni: "Her gün gördüğün şeylerin görünmeyen ekonomisi. Haftada 1–2 video." + iletişim e-postası.
- Sabit ilk video: kanalın ne olduğunu anlatan 60 sn.

## C. Bilgisayar kurulumu (Windows/Mac/Linux, hepsi ücretsiz)
1. **Python 3.10+** kur (python.org).
2. **ffmpeg** kur (Windows: `winget install ffmpeg`; Mac: `brew install ffmpeg`; Linux: `apt install ffmpeg`).
3. **espeak-ng** kur (Kokoro ses motoru için gerekli).
4. Terminal:
   ```
   python -m venv .venv
   .venv\Scripts\activate        # Mac/Linux: source .venv/bin/activate
   pip install matplotlib numpy soundfile kokoro edge-tts
   ```
5. Test: `python animasyon/bilesik_faiz.py` → mp4 çıkıyorsa grafik tarafı hazır.
6. Test: `python pipeline/uret_kokoro.py senaryo.txt deneme` → deneme.wav çıkıyorsa ses hazır. Olmazsa yedek: `python pipeline/uret.py senaryo.txt deneme`.
7. Kurgu için **DaVinci Resolve** (ücretsiz sürüm) veya CapCut kur.
   Telif: müzik için YouTube Ses Kitaplığı (Studio → Ses kitaplığı), harici müzik kullanma.

## D. Bir videonun üretim akışı (haftada 1–2 video için ~6–10 saat)
1. **Konu seç** (KONULAR.md) + 3 zorunlu soruyu yanıtla.
2. **Araştır** (2 saat): 2–3 kaynak, rakamları bir tabloya yaz. Kaynak linklerini kaydet.
3. **Senaryo yaz** (1–2 saat), SENARYO_SABLONU.md'ye göre, 6–9 dk ≈ 900–1300 kelime. Claude'dan taslak/hata denetimi iste ama anlatımı kendin şekillendir. Rakamları kaynakla yeniden kontrol et.
4. **Ses üret**: `uret_kokoro.py`. Dinle, telaffuz hatalarını düzelt (zor kelimeleri fonetik yaz).
5. **Animasyon** (2–4 saat): her videoda 4–8 sahne. Matplotlib ile grafik/eğri, Canva/Inkscape ile ikon ve metin kartları. Her sahne = sesteki bir cümle.
6. **Kurgu**: ses + sahneleri Resolve'de hizala, altyazı ekle (Whisper veya `uret.py`'nin SRT'si), ses altına hafif müzik.
7. **Küçük resim**: Canva, 1280×720, en fazla 3–4 kelime, yüksek kontrast, rakam içeren. Başlık ile aynı vaadi ver (clickbait yok).
8. **Yükle**: başlık (merak + anahtar kelime), açıklama (özet + kaynaklar + "eğitim amaçlıdır"), 3–5 etiket, bölümler (chapters).
   - "Altered content" sorusunda: gerçekçi sahte kişi/olay üretmiyorsan genelde işaretlemek gerekmez; yine de YouTube'un güncel yönergesini oku, şüphede işaretle.
9. İlk 48 saatte YouTube Studio → Analitik: tıklanma oranı (hedef >%4), tutma (hedef >%40). Düşükse küçük resim/başlığı değiştir.

## E. Para kazanma kurulumu
1. Eşik: YouTube Ortaklık Programı gereksinimini Studio → Kazanç sekmesinde kontrol et (1.000 abone + 4.000 saat civarı; değişmiş olabilir, resmi sayfa geçerli).
2. Uygun olunca AdSense hesabı bağla, PIN/vergi bilgisi (ABD vergi formu W-8BEN, YouTube yönlendirir).
3. Gelir sırası: reklam → affiliate (açıklamada, tavsiye değil, "kullandığım araç" bağlamında; ifşa et) → sponsor.
4. Yıldız kural: yatırım/al-sat tavsiyesi yok, garanti getiri yok.

## F. Takvim
- **Hafta 1:** hesaplar, marka, kurulum, 3 senaryo taslağı.
- **Hafta 2–3:** ilk 3 video (yayına hemen çıkma; 3 hazır olunca bir hafta arayla yayınla).
- **Ay 2:** haftada 1–2 video, analiz, 20 konunun en iyi 5'ine odaklan.
- **Ay 3:** Shorts (videodan 30 sn'lik kesit), affiliate, değerlendirme: tutan format neyse onu büyüt.

## G. Sık düşülen hatalar
- Aynı şablon + sadece konu değişimi (politika riski).
- Doğrulanmamış rakam kullanmak (güvenilirlik = YMYL).
- Başlığı abartıp tutmayı düşürmek.
- İlk 10 videoyu görmeden büyük karar vermek: veriyi bekle.
