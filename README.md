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

## Testler

```
python -m unittest discover -s tests -t .
```

Sahte modem + sahte sayaçla uçtan uca okuma testi içerir.
