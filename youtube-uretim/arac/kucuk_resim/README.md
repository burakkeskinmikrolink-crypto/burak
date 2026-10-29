# kucuk_resim: A/B testine hazır küçük resim üreticisi (Pillow)

Takvimdeki 12 uzun video (tüm `-v2` senaryoları) için **2'şer varyant** (A ve B) üretir. Toplam 24 PNG, 1280x720. Ek olarak telefonda nasıl görüneceklerini gösteren önizleme ızgaraları üretir.

## Çıktılar (`cikti/`)
| Dosya | Ne |
|---|---|
| `cikti/<ID>_A.png`, `cikti/<ID>_B.png` | Test & Compare'e yüklenecek küçük resimler (1280x720) |
| `cikti/onizleme/telefon_izgara.png` | **Hepsi tek görselde:** YouTube mobil ana sayfa akışı boyutunda (360 px genişlik), koyu tema, süre rozeti ve başlık satırıyla |
| `cikti/onizleme/kucuk_izgara.png` | Hepsi tek görselde: "Sıradaki" ve arama listesi boyutunda (168 px) |
| `cikti/onizleme/<ID>_AB_telefon.png` | Her video için A ve B yan yana, telefon boyutunda |

## Kurallar (kodla zorlanır, testle doğrulanır)
- **En fazla 4 kelime.** Daha fazlası `KuralHatasi` verir.
- **Kalın, büyük yazı:** Inter Display Black. Yazı kutuya sığan en büyük puntoyla, en fazla 3 satıra otomatik bölünür. Testler her varyantın en az **95 punto** (telefonda ~27 px) olmasını şart koşar.
- **Tek ana nesne:** Sağda vektör tarzında çizilmiş tek bir ikon var (jeneratör, fatura, termometre, telefon, fiş, kart, kilit…). Fotoğraf kullanılmadığı için telif riski yok.
- **Yüksek kontrast:** Yazı ile arka plan arasında WCAG kontrastı ≥ 4.5. Yazıda kalın kontur ve gölge var.
- **Süre rozetinden uzak:** Yazı sol blokta kalır, sağ alt köşedeki "8:00" rozeti yazının üstüne binmez.
- **Kanal temaları** (`temalar.py`):
  - **Hidden Systems:** koyu lacivert-siyah, **kırmızı** vurgu
  - **Centworks:** koyu antrasit, **altın ve yeşil** vurgu
  - **Scam Engineer:** **açık ve renkli** (gökyüzü mavisi → sıcak sarı), mavi ve turuncu vurgu, kırmızı yok. Bir test bunu kontrol eder.

## Font ve lisans
- **Inter / Inter Display** (Rasmus Andersson ve Inter Project Authors), **SIL Open Font License 1.1**. Google Fonts'ta da yayımlanıyor: https://fonts.google.com/specimen/Inter
- Font dosyaları ve lisans metni `fonts/` klasöründe (`OFL.txt`). OFL, fontla üretilen görsellerin (küçük resimler) ticari kullanımına izin verir. Fontun kendisi tek başına satılamaz.

## Kurulum ve kullanım
```bash
pip install Pillow
python uret.py                    # 12 video × 2 varyant + önizlemeler
python uret.py --sadece HS-07     # tek video
python -m unittest discover -s tests -t .   # 9 test
```
Windows PowerShell'de de aynı komutlar çalışır (`python` yerine gerekirse `py`).

## Yeni video eklemek
`videolar.json` dosyasına şu yapıda bir kayıt ekle:
- `id`, `kanal`, `baslik`
- Her varyant için `yazi` (≤4 kelime), `vurgu` (vurgulanacak kelimelerin sıra numaraları, 0'dan başlar), `nesne` (`cizim.py` içindeki `NESNELER` listesinden) ve `ayar` (nesneye özel parametreler)

Sonra `python uret.py --sadece <ID>` komutunu çalıştır.

## Senaryolardaki konseptten farklar
Telefonda okunurluk testi yüzünden üç varyantın yazısı v2 senaryosundaki öneriden biraz değişti:
| Video | Senaryodaki öneri | Üretilen |
|---|---|---|
| CW-05 A | +$284/MONTH | +$284 A MONTH |
| CW-05 B | WHAT IF IT CONTINUES? | WHAT IF RATES RISE? |
| SE-04 A | "MEDICARE" ISN'T CALLING | MEDICARE ISN'T CALLING |

## Test & Compare'e yükleme
1. Videonun ayrıntılar sayfasında **Test & Compare**'i aç.
2. `<ID>_A.png` ve `<ID>_B.png` dosyalarını yükle. Varsa mevcut küçük resim kontrol grubu olarak kalabilir.
3. Sonucu (Winner / Performed same / Inconclusive) ve Intro (30 sn) değerini `../../haftalik-analiz-sablonu.md` dosyasına yaz.
