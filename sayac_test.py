#!/usr/bin/env python3
"""Sayacı USB-RS485 dönüştürücüyle doğrudan okur (IEC 62056-21 Mode C).

Amaç: sayaç ve RS485 kablosu sağlam mı, modemden bağımsız kanıtlamak.

Kullanım:
    pip install pyserial
    python sayac_test.py COM5                  # Windows
    python sayac_test.py /dev/ttyUSB0          # Linux
    python sayac_test.py COM5 --adres 400106101   # hatta birden çok sayaç varsa
    python sayac_test.py COM5 --hiz-degistirme    # hep 300 baud'da kal

Hiç cevap gelmezse:
  - A ile B kablolarını ters çevirip tekrar dene
  - --adres ile sayacın seri numarasını vermeyi dene
"""

import argparse
import sys
import time

from osos import iec62056 as iec

try:
    import serial
except ImportError:
    sys.exit("pyserial yüklü değil:  pip install pyserial")


def satir_oku(port, zaman_asimi: float) -> bytes:
    """\\n gelene kadar ya da süre dolana kadar okur."""
    bitis = time.time() + zaman_asimi
    tampon = b""
    while time.time() < bitis:
        parca = port.read(1)
        if parca:
            tampon += parca
            if tampon.endswith(b"\n"):
                break
    return tampon


def blok_oku(port, zaman_asimi: float):
    bitis = time.time() + zaman_asimi
    tampon = b""
    while time.time() < bitis:
        parca = port.read(port.in_waiting or 1)
        if parca:
            tampon += iec.parity_temizle(parca)
            sonuc = iec.veri_blogu_ayir(tampon)
            if sonuc:
                return sonuc, tampon
    return None, tampon


def yankiyi_at(cevap: bytes, gonderilen: bytes) -> bytes:
    """Bazı RS485 dönüştürücüler gönderdiğimizi geri okur."""
    if cevap.startswith(gonderilen):
        return cevap[len(gonderilen):]
    return cevap


def main():
    ap = argparse.ArgumentParser(description="IEC 62056-21 sayaç okuma testi")
    ap.add_argument("port", help="Seri port (COM5, /dev/ttyUSB0 ...)")
    ap.add_argument("--adres", default="", help="Sayaç seri no (boş = hattaki tek sayaç)")
    ap.add_argument("--hiz-degistirme", action="store_true",
                    help="Sayacın önerdiği hıza geçme, 300 baud'da oku")
    ap.add_argument("--zaman-asimi", type=float, default=90,
                    help="Veri bloğu için bekleme süresi (sn)")
    args = ap.parse_args()

    port = serial.Serial(args.port, 300, bytesize=serial.SEVENBITS,
                         parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE,
                         timeout=0.2)
    port.reset_input_buffer()

    istek = iec.istek(args.adres)
    print(f">> {istek!r}  (300 baud 7E1)")
    port.write(istek)
    port.flush()

    cevap = b""
    for _ in range(3):  # yankı satırı gelirse bir sonrakini bekle
        cevap = yankiyi_at(iec.parity_temizle(satir_oku(port, 3)), istek)
        if cevap.strip():
            break
    metin = cevap.decode("ascii", "replace").strip()
    if not metin.startswith("/"):
        print("<< Cevap yok ya da anlaşılmadı:", repr(cevap))
        print("   A/B kablolarını ters çevir, --adres ile tekrar dene.")
        sys.exit(1)

    kimlik = iec.Kimlik(metin)
    print(f"<< {kimlik.ham}")
    print(f"   Üretici: {kimlik.uretici}   Önerilen hız: {kimlik.baud} baud")

    hiz_harfi = "0" if args.hiz_degistirme else kimlik.hiz_harfi
    onay = iec.ack(hiz_harfi)
    time.sleep(0.03 if kimlik.hizli else 0.25)
    print(f">> ACK {onay[1:].decode().strip()}")
    port.write(onay)
    port.flush()
    if hiz_harfi != "0":
        time.sleep(0.3)
        port.baudrate = iec.BAUD_HARFLERI[hiz_harfi]

    print(f"   Veri bekleniyor ({port.baudrate} baud)...")
    t0 = time.time()
    sonuc, ham = blok_oku(port, args.zaman_asimi)
    port.close()

    if not sonuc:
        print(f"<< Veri bloğu tamamlanmadı. Gelen {len(ham)} byte:")
        print(ham.decode("ascii", "replace"))
        if hiz_harfi != "0":
            print("   --hiz-degistirme ile 300 baud'da tekrar dene.")
        sys.exit(2)

    blok, bcc_ok = sonuc
    print(f"   {len(blok)} byte, {time.time() - t0:.1f} sn, BCC {'DOĞRU' if bcc_ok else 'HATALI'}")
    print()
    print(f"{'OBIS':<16}{'DEĞER':>18}  BİRİM   AÇIKLAMA")
    for adres, deger, birim in iec.obis_ayristir(blok.decode("ascii", "replace")):
        aciklama = iec.OBIS_ACIKLAMA.get(iec.obis_kisa(adres), "")
        print(f"{adres:<16}{deger:>18}  {birim:<7} {aciklama}")

    with open("sayac_okuma.txt", "wb") as f:
        f.write(kimlik.ham.encode() + b"\r\n" + blok)
    print("\nHam veri sayac_okuma.txt dosyasına yazıldı.")


if __name__ == "__main__":
    main()
