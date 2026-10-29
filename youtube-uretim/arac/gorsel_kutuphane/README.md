# gorsel_kutuphane: telifsiz görsel arama, lisans kontrolü ve Ken Burns/parallax klip aracı

Hidden Systems, Centworks ve Scam Engineer videoları için bağımsız bir Python aracı.

**Ne yapar?**
1. **Arama:** Anahtar kelimeyle telifsiz görsel ve video arar. Kaynaklar: Wikimedia Commons, NASA Image and Video Library, Pexels, Pixabay.
2. **Lisans kontrolü:** Yalnızca **kamu malı, CC0, CC BY, CC BY-SA, Pexels License ve Pixabay Content License** kabul edilir. NC, ND, GFDL ve tanınmayan lisanslar otomatik olarak **reddedilir** ve indirilmez. CC BY ve CC BY-SA için TASL biçiminde (başlık, yazar, kaynak, lisans) atıf metni üretilir.
3. **Klip:** İndirilen görselden **Ken Burns** (yavaş zoom veya kaydırma) ya da **parallax** efektli **1920x1080** (uzun video) ve **1080x1920** (Shorts) klip üretir. ffmpeg kullanır.
4. **Atıf listesi:** Her proje için YouTube açıklamasına yapıştırılacak bir **`kaynaklar.txt`** üretir.

> Bu araç hukuki danışmanlık değildir. Lisans kararı kaynakların bildirdiği bilgiye dayanır. Şüpheli durumda araç "RED" verir, yine de kullanmadan önce dosya sayfasına bir kez bakın. Ayrıntılar: [`../../oyun-kitabi/gorsel-ve-ses.md`](../../oyun-kitabi/gorsel-ve-ses.md)

---

## Windows'ta kurulum (adım adım)

### 1. Python
1. https://www.python.org/downloads/windows/ adresinden **Python 3.10 veya üstünü** indirin.
2. Kurulumun ilk ekranında **"Add python.exe to PATH"** kutusunu işaretleyin.
3. Kontrol edin. **PowerShell**'i açın ve şunu yazın:
   ```powershell
   python --version
   ```

### 2. ffmpeg
1. https://www.gyan.dev/ffmpeg/builds/ adresinden **"ffmpeg-release-essentials.zip"** dosyasını indirin.
2. Zip dosyasını `C:\ffmpeg` klasörüne açın. Sonuçta `C:\ffmpeg\bin\ffmpeg.exe` dosyası olmalı.
3. `C:\ffmpeg\bin` klasörünü PATH'e ekleyin:
   - Başlat menüsünde "ortam değişkenleri" diye arayın ve **"Sistem ortam değişkenlerini düzenleyin"** seçeneğini açın.
   - **Ortam Değişkenleri…** → **Path** → **Düzenle** → **Yeni** → `C:\ffmpeg\bin` → **Tamam**.
4. **Yeni** bir PowerShell penceresi açın ve kontrol edin:
   ```powershell
   ffmpeg -version
   ```
   Alternatif: `winget install Gyan.FFmpeg` komutu da ffmpeg'i kurar.

### 3. Aracı kurun
PowerShell'de bu klasöre gidin (yolu kendi bilgisayarınıza göre değiştirin):
```powershell
cd C:\Users\<kullanici>\burak\youtube-uretim\arac\gorsel_kutuphane
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
PowerShell betik çalıştırmayı engellerse önce şu komutu verin:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### 4. API anahtarları (.env)
```powershell
copy .env.example .env
notepad .env
```
- **Pexels:** https://www.pexels.com/api/ adresinden ücretsiz anahtar alın ve `PEXELS_API_KEY` satırına yapıştırın.
- **Pixabay:** https://pixabay.com/api/docs/ sayfasında giriş yapınca anahtarınız görünür. `PIXABAY_API_KEY` satırına yapıştırın.
- **NASA:** Anahtar gerekmez.
- **Wikimedia:** Anahtar gerekmez, ama `WIKIMEDIA_USER_AGENT` satırına e-posta adresinizi yazın (Wikimedia politikası).

`.env` dosyası `.gitignore` içinde, yani git'e gönderilmez.

### 5. Testler (internet gerekmez)
```powershell
python -m unittest discover -s tests -t .
```
Testler sahte API yanıtları kullanır. ffmpeg kuruluysa, sahte bir test görselinden gerçekten 1920x1080 ve 1080x1920 klip de üretir.

---

## Kullanım

Tüm komutlar `python -m gorsel_kutuphane` ile çalışır. Proje dosyaları varsayılan olarak `.\projeler\<proje_adi>\` altında tutulur.

### 1) Arama
```powershell
python -m gorsel_kutuphane ara "diesel generator" --proje hs-04 --kaynak wikimedia,nasa,pexels,pixabay --adet 8
python -m gorsel_kutuphane ara "server room" --proje hs-04 --kaynak pexels,pixabay --tur video
```
Çıktı her sonucu numarası, kaynağı, lisans kategorisi ve **UYGUN (EVET/HAYIR)** bilgisiyle listeler. Sonuçlar `projeler\hs-04\son_arama.json` dosyasına kaydedilir.

### 2) İndirme
```powershell
python -m gorsel_kutuphane indir --proje hs-04 --secim 1,4,6
```
- Lisansı uygun olmayan seçimler **indirilmez** ve `[red]` olarak raporlanır.
- İndirilenler `projeler\hs-04\medya\` klasörüne gider ve `proje.json` dosyasına kaydedilir. `kaynaklar.txt` otomatik olarak güncellenir.

### 3) Klip üretme
```powershell
# Ken Burns: yatay ve dikey, 6 saniye, yavaş yakınlaşma
python -m gorsel_kutuphane klip --proje hs-04 --dosya medya\wikimedia_101_diesel-generator.jpg --efekt kenburns --hareket zoom_in --format ikisi --sure 6

# Ken Burns hareketleri: zoom_in, zoom_out, pan_left, pan_right, pan_up, pan_down
python -m gorsel_kutuphane klip --proje hs-04 --dosya medya\xxx.jpg --hareket pan_right --format dikey

# Parallax (ön plan olmadan): bulanık arka plan + daha hızlı kayan ön kesit ("sözde parallax")
python -m gorsel_kutuphane klip --proje hs-04 --dosya medya\xxx.jpg --efekt parallax

# Gerçek parallax: GIMP veya Photoshop ile ayırdığınız saydam ön plan PNG'sini verin
python -m gorsel_kutuphane klip --proje hs-04 --dosya medya\arka.jpg --efekt parallax --on-plan medya\on_plan.png
```
Klipler `projeler\hs-04\klipler\` klasörüne `..._zoom_in_1920x1080.mp4` / `..._1080x1920.mp4` adlarıyla yazılır (H.264, 30 fps, sessiz). DaVinci Resolve veya başka bir kurgu programına doğrudan alınabilir.

### 4) Atıf listesi
```powershell
python -m gorsel_kutuphane kaynaklar --proje hs-04
```
`projeler\hs-04\kaynaklar.txt` dosyası iki bölüm içerir:
- **Attribution required:** CC BY ve CC BY-SA öğeleri, TASL biçiminde ve "modified: cropped, animated" notuyla
- **Public domain, Pexels and Pixabay:** Zorunlu olmasa da iyi uygulama olarak kaynak gösterilen öğeler

Metni YouTube açıklamasının sonundaki **VISUAL CREDITS** bölümüne yapıştırın.

---

## Lisans kuralları (özet)
| Kaynak / lisans | Karar | Atıf |
|---|---|---|
| Kamu malı, PD-*, Public Domain Mark | ✅ | Zorunlu değil, yine de yazılır |
| CC0 | ✅ | Zorunlu değil, yine de yazılır |
| CC BY (tüm sürümler) | ✅ | **Zorunlu** (TASL) |
| CC BY-SA (tüm sürümler) | ✅ | **Zorunlu** (TASL). Uyarlama aynı lisansla paylaşılmalı, `kaynaklar.txt` bunu not eder |
| Pexels License | ✅ | Zorunlu değil. Tanınabilir kişi veya markayla onay ima etme |
| Pixabay Content License | ✅ | Zorunlu değil. Tanınabilir kişi, logo ve marka için dikkat |
| NASA | ✅ (açıklamada "©" veya "copyright" yoksa) | "NASA onayını ima etmez" notu. NASA logosu kullanılamaz |
| CC BY-NC, CC BY-ND, GFDL, "All rights reserved", tanınmayan | ❌ | İndirilmez |

## Ağ erişimi olmayan ortamlar
Kod internete erişemediği bir ortamda yazıldı ve test edildi. API çağrıları gerçek uç noktalara yöneliktir ve belgelerine göre kurgulandı, ama **canlı API ile ilk çalıştırmayı siz yapacaksınız**. Bir kaynak hata verirse (`[uyarı] pexels: ...`), diğer kaynaklar çalışmaya devam eder.

## Klasör yapısı
```
gorsel_kutuphane/
├── gorsel_kutuphane/
│   ├── cli.py            komut satırı (ara, indir, klip, kaynaklar)
│   ├── config.py         .env okuma
│   ├── licenses.py       lisans sınıflandırma + atıf metni
│   ├── indirme.py        lisans kontrollü indirme
│   ├── efektler.py       Ken Burns / parallax (ffmpeg)
│   ├── proje.py          proje klasörü, proje.json, kaynaklar.txt
│   ├── models.py         MediaItem veri modeli
│   └── kaynaklar/        wikimedia.py, nasa.py, pexels.py, pixabay.py
├── tests/                sahte verilerle birim testleri (internet gerekmez)
├── requirements.txt
├── .env.example
└── README.md
```
