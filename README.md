# OSOS – kendi okuma sistemimiz

Sahadaki ECL-BGS5 modemler (Cinterion BGS5) sayacın RS485 portuna bağlı ve
açılınca bir merkeze (bugün `10.124.132.180:80`) kendileri bağlanıyor.
Plan: modemlerin merkez adresini bizim sunucumuza çevirmek ve sayaçları
kendi yazılımımızla okumak.

## Dosyalar

| Dosya | Ne işe yarar |
|---|---|
| `sayac_test.py` | Sayacı laptop + USB-RS485 ile doğrudan okur. Sayaç ve kablo sağlam mı? |
| `osos_server.py` | Modemlerin bağlanacağı merkez. Gelen her byte'ı kaydeder, istenirse modem üzerinden sayacı okur, SQLite'a yazar. |
| `osos_panel.py` | Web paneli: sahaların durumu (okunuyor / bağlanıyor ama okunamıyor / sessiz / hiç bağlanmadı), son endeksler, CSV indirme. |
| `envanter_yukle.py` | EnerClever'dan kopyalanan modem ve sayaç listesini içeri alır; modem ile sayaç saha adından eşleşir. |
| `enerclever_analiz.py` | EnerClever'daki mevcut durumu modem tipine, bölgeye, sayaca göre özetler; okunmayan sahaları CSV'ye yazar. |
| `modem_simulator.py` | Sahte modemler. Gerçek modem yokken tüm sistemi uçtan uca çalıştırıp göstermek için. |
| `osos/iec62056.py` | Luna, Köhler vb. sayaçların konuştuğu IEC 62056-21 protokolü. |

## Kurulum

```
pip install -r requirements.txt
```

## 1. Sayacı doğrudan oku (masada ya da sahada)

```
python sayac_test.py COM5                       # Windows
python sayac_test.py /dev/ttyUSB0               # Linux
python sayac_test.py COM5 --adres 400106101     # hatta birden çok sayaç varsa
python sayac_test.py COM5 --hiz-degistirme      # 300 baud'da kal
```

Cevap gelmezse A/B kablolarını ters çevirip tekrar dene.

## 2. Merkez sunucuyu çalıştır

```
python osos_server.py --port 80                  # sadece dinle: modem kendini nasıl tanıtıyor?
python osos_server.py --port 80 --oku            # bağlanan modem üzerinden sayacı oku
python osos_server.py --port 80 --oku --periyot 60   # bağlantı açıksa saatte bir oku
python osos_server.py --port 80 --udp            # UDP gelirse onu da kaydet
python osos_server.py --rapor                    # son bağlantı ve okumaları göster
```

- Her bağlantı `logs/<tarih>.log` dosyasına hex + metin olarak yazılır.
- IMEI ve ICCID gelen veride geçiyorsa otomatik bulunur.
- `--oku` modemi şeffaf köprü varsayar: sayaca `/?!` gönderir, okumayı
  300 baud'da tutar (modemin seri portu okuma ortasında hız değiştiremez).
- Modemin seri portu 8N1 ise `--parity-ekle` ile 7E1 yazılımdan sağlanır.

Sunucu, modemlerin SIM'lerinin çıktığı Vodafone APN'inden erişilebilir bir
adreste olmalı.

## 3. EnerClever listesini içeri al

EnerClever → Modemler → "Sayfada" kutusunu en büyüğe al → tabloyu başlıklarıyla
seç, kopyala → Excel'e yapıştır → CSV kaydet (ya da bir .txt'ye yapıştır).
Aynısını Sayaçlar / Sayaç Okumaları sayfası için de yap.

```
python envanter_yukle.py modemler.csv sayaclar.csv
```

EnerClever → Sayaç Durum Kontrol → Excel ile indirilen `meterStatusList_*.xls`
dosyası da doğrudan yüklenir (modem IMEI, sayaç, eski sistemdeki durum ve son okuma):

```
python envanter_yukle.py meterStatusList_20.10.2026_00_48_32.xls
python enerclever_analiz.py --csv sorunlu_sahalar.csv   # mevcut durum raporu + sahaya gidilecek liste
python envanter_yukle.py EnerjiRaporu_55.xls             # aylık kWh + modem GSM numaraları
```

## 4. Paneli aç

```
python osos_panel.py            # http://localhost:8000
```

- **Sahalar:** her sahanın durumu, L1/L2/L3 faz durumu, alarmlar (faz yok, düşük/yüksek
  gerilim, sayaç hata kodu, düşük güç faktörü, akım dengesizliği, sessiz modem).
- **Modem sayfası:** faz tablosu (gerilim, akım, güç faktörü), sayacın gönderdiği tüm
  değerler (tarifeler, reaktif, maksimum talep, kesinti sayıları, hata kodu ve bilinmeyen
  kodlar dahil), gerilim/akım/günlük tüketim grafikleri, okuma ve bağlantı geçmişi.
- **Enerji Raporu:** EnerClever "Enerji Raporu" ile aynı kolonlarda aylık kWh, yanında
  EnerClever'ın aynı ay değeri; Excel için CSV.

## Modem olmadan deneme (sunum için de)

Üç ayrı pencerede:

```
python osos_server.py --port 9000 --oku --bekle 1
python modem_simulator.py --port 9000 --adet 20 --aralik 30
python osos_panel.py
```

## Testler

```
python -m unittest discover -s tests -t .
```

Sahte modem + sahte sayaçla uçtan uca okuma testi içerir.
