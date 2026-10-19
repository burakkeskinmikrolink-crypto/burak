# OSOS Sunucusu — Kurulum Notu (VF Sistem Ekibi)

Bu not, OSOS modemlerinin bağlandığı sunucuda (10.124.132.180, 80/TCP) çalışacak
yeni toplama yazılımının kurulumu içindir. Yazılım tek bir Python dosyasıdır, ek
servis ya da veritabanı sunucusu gerektirmez (yerleşik SQLite kullanır).

Modemler bu adrese kendileri bağlandığı için **modem tarafında hiçbir değişiklik
yapılmaz**; yalnızca bu sunucuda 80. portu dinleyen yazılım değişir.

---

## 1. Gereken bilgiler (kuruluma başlamadan)

- Sunucunun işletim sistemi (Windows Server / Linux)
- 80/TCP portunu şu an hangi uygulamanın dinlediği (eski yazılım) ve durdurma yetkisi
- Sunucuya erişim (RDP / SSH)
- Python 3.9+ kurulu mu

> **Önemli:** 80. portu aynı anda tek uygulama dinleyebilir. Yeni yazılım
> başlatılmadan önce eski toplama yazılımı durdurulmalıdır. Bu an itibarıyla eski
> panelin veri alması durur; geri dönüş için eski yazılım yeniden başlatılır.

---

## 2. Dosyalar

Kaynak: GitHub deposu, `claude/zen-cray-79rksu` dalı (ZIP olarak indirilebilir).
Sunucuda bir klasöre çıkarın, örn. `C:\OSOS` ya da `/opt/osos`.

Çalışması için gerekenler:
- `osos_server.py`, `osos_panel.py`
- `osos/` klasörü (iec62056.py, veritabani.py, olcumler.py)

Python standart kütüphanesi yeter; sunucu için ek paket gerekmez.
(EnerClever .xls listelerini aktarmak isterseniz: `pip install xlrd`)

---

## 3. Kurulum

### Linux
```bash
cd /opt/osos
python3 --version                 # 3.9+ olmalı
sudo python3 osos_server.py --port 80 --oku --db veri/osos.db --log-klasoru veri/logs
```

### Windows Server
```bat
cd C:\OSOS
python osos_server.py --port 80 --oku --db veri\osos.db --log-klasoru veri\logs
```
Güvenlik duvarı 80/TCP'ye gelen bağlantılara zaten izin veriyordur (eski yazılım
da aynı portu kullanıyordu); vermiyorsa 80/TCP gelen kural eklenir.

Başladığında ekranda şunu yazar:
```
TCP dinleniyor: ('0.0.0.0', 80)  (oku=açık)
```

---

## 4. İlk doğrulama

Yazılım açıldıktan sonra modemler bağlandıkça her bağlantı hem ekrana hem
`veri/logs/<tarih>.log` dosyasına yazılır. Örnek:
```
[358741052021927] Bağlantı açıldı
[358741052021927] << 42 byte  hex=...  metin='...'
```
İlk bağlantıları gördüğünüzde kurulum doğru demektir.

Son durumu görmek için:
```
python osos_server.py --rapor --db veri/osos.db
```

---

## 5. Sürekli çalışma (servis)

Test bağlantıları görüldükten sonra yazılım bir servis olarak çalıştırılmalıdır
ki sunucu yeniden başlasa da otomatik açılsın.

- **Linux (systemd):** `/etc/systemd/system/osos.service`
  ```ini
  [Unit]
  Description=OSOS toplama sunucusu
  After=network.target

  [Service]
  WorkingDirectory=/opt/osos
  ExecStart=/usr/bin/python3 /opt/osos/osos_server.py --port 80 --oku --db /opt/osos/veri/osos.db --log-klasoru /opt/osos/veri/logs
  Restart=always

  [Install]
  WantedBy=multi-user.target
  ```
  ```bash
  sudo systemctl enable --now osos
  ```

- **Windows:** Görev Zamanlayıcı ile "bilgisayar açılışında, kullanıcı oturumundan
  bağımsız" çalışacak bir görev; eylem `python C:\OSOS\osos_server.py --port 80 --oku ...`.

---

## 6. Panel (isteğe bağlı, ayrı port)

Toplanan veriyi web arayüzünde görmek için, aynı ya da başka bir makinede:
```
python osos_panel.py --port 8000 --db veri/osos.db
```
Tarayıcıdan `http://<sunucu>:8000`. Panel yalnızca okur, toplama sunucusunu etkilemez.

---

## 7. Geri dönüş

Sorun olursa yeni yazılım durdurulur (Ctrl+C ya da servis stop) ve eski toplama
yazılımı yeniden başlatılır. Modemler aynı adrese bağlanmaya devam ettiği için
eski panel kaldığı yerden veri almaya döner. Modem tarafında hiçbir kalıcı
değişiklik yapılmadığından geri dönüş birkaç dakikadır.

---

## 8. İletişim

İlk bağlantı logları (`veri/logs/<tarih>.log`) kurulum sonrası tarafımıza
iletilirse, modemlerin gönderdiği veri biçimine göre okuma doğrulanıp
tamamlanır.
