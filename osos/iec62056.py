"""IEC 62056-21 (Mode C) yardımcıları.

Luna, Köhler ve benzeri RS485 çıkışlı sayaçlar bu protokolü konuşur:
  1. 300 baud 7E1 ile  /?!<CR><LF>  (ya da /?<seri_no>!<CR><LF>) gönderilir
  2. Sayaç kimliğini döner:  /LUN5<sayaç bilgisi><CR><LF>
     4. karakter hız harfidir ('0'=300 ... '5'=9600)
  3. ACK 0 Z 0 <CR><LF> gönderilir (Z: istenen hız harfi)
  4. Veri gelir:  STX <satırlar> ! <CR><LF> ETX BCC

Bu modül hem seri porttan okuyan sayac_test.py hem de modem üzerinden
okuyan osos_server.py tarafından kullanılır.
"""

import re

STX = 0x02
ETX = 0x03
ACK = 0x06
NAK = 0x15

BAUD_HARFLERI = {
    "0": 300,
    "1": 600,
    "2": 1200,
    "3": 2400,
    "4": 4800,
    "5": 9600,
    "6": 19200,
}

# Örn: 1.8.0(012345.678*kWh)  veya  0-0:96.1.0(12345678)
_SATIR = re.compile(r"([0-9A-Za-z][0-9A-Za-z\-:.*&]*?)\(([^()]*)\)")


def istek(adres: str = "") -> bytes:
    """Okuma isteği: /?!\\r\\n  ya da  /?<adres>!\\r\\n"""
    return f"/?{adres}!\r\n".encode("ascii")


def ack(hiz_harfi: str = "0", mod: str = "0") -> bytes:
    """Seçenek onayı. mod '0' = veri okuma, '1' = programlama (kullanmıyoruz)."""
    return bytes([ACK]) + f"0{hiz_harfi}{mod}\r\n".encode("ascii")


def bcc(veri: bytes) -> int:
    """STX'ten sonraki byte'lardan ETX dahil XOR."""
    sonuc = 0
    for b in veri:
        sonuc ^= b
    return sonuc & 0x7F


def parity_temizle(veri: bytes) -> bytes:
    """8N1 okunan 7E1 verisindeki parity bitini atar."""
    return bytes(b & 0x7F for b in veri)


def parity_ekle(veri: bytes) -> bytes:
    """7 bitlik veriye çift (even) parity bitini 8. bit olarak ekler.

    Modemin seri portu 8N1 ayarlıysa ve değiştirilemiyorsa, sayacın 7E1
    beklentisini yazılımdan karşılamak için kullanılır.
    """
    cikti = bytearray()
    for b in veri:
        b &= 0x7F
        if bin(b).count("1") % 2:
            b |= 0x80
        cikti.append(b)
    return bytes(cikti)


class Kimlik:
    """Sayacın /XXXZ... cevabı."""

    def __init__(self, satir: str):
        satir = satir.strip()
        if not satir.startswith("/") or len(satir) < 5:
            raise ValueError(f"Geçersiz kimlik satırı: {satir!r}")
        self.ham = satir
        self.uretici = satir[1:4]
        self.hiz_harfi = satir[4]
        self.tanim = satir[5:]
        # Üretici kodunun 3. harfi küçükse sayaç 20 ms'de cevap verir
        self.hizli = self.uretici[2].islower()

    @property
    def baud(self) -> int:
        return BAUD_HARFLERI.get(self.hiz_harfi, 300)

    def __repr__(self) -> str:
        return f"Kimlik({self.ham!r})"


def veri_blogu_ayir(tampon: bytes):
    """Tamponda tam bir STX...ETX BCC bloğu varsa (blok, bcc_dogru) döner.

    Tam blok yoksa None döner.
    """
    bas = tampon.find(bytes([STX]))
    if bas < 0:
        return None
    son = tampon.find(bytes([ETX]), bas + 1)
    if son < 0 or son + 1 >= len(tampon):
        return None
    govde = tampon[bas + 1 : son + 1]  # ETX dahil
    gelen_bcc = tampon[son + 1] & 0x7F
    return tampon[bas + 1 : son], gelen_bcc == bcc(govde)


def obis_ayristir(metin: str):
    """Veri bloğundaki satırları [(obis, deger, birim), ...] listesine çevirir.

    Bir adreste birden fazla parantez varsa (ör. maksimum talep + zaman)
    hepsi ayrı satır olarak döner.
    """
    sonuclar = []
    for satir in metin.replace("\r", "").split("\n"):
        satir = satir.strip()
        if not satir or satir == "!":
            continue
        eslesmeler = list(_SATIR.finditer(satir))
        if not eslesmeler:
            continue
        adres = eslesmeler[0].group(1)
        # Aynı satırdaki sonraki parantezler ilk adrese aittir
        degerler = [eslesmeler[0].group(2)]
        kalan = satir[eslesmeler[0].end():]
        degerler += re.findall(r"\(([^()]*)\)", kalan)
        for deger in degerler:
            if "*" in deger:
                d, birim = deger.split("*", 1)
            else:
                d, birim = deger, ""
            sonuclar.append((adres, d, birim))
    return sonuclar


# Raporda öne çıkarılacak bilinen kodlar
OBIS_ACIKLAMA = {
    "0.0.0": "Sayaç seri no",
    "96.1.0": "Sayaç seri no",
    "0.9.1": "Saat",
    "0.9.2": "Tarih",
    "1.8.0": "Toplam aktif tüketim (T)",
    "1.8.1": "Tarife 1 (gündüz)",
    "1.8.2": "Tarife 2 (puant)",
    "1.8.3": "Tarife 3 (gece)",
    "2.8.0": "Toplam aktif üretim",
    "5.8.0": "Endüktif reaktif",
    "8.8.0": "Kapasitif reaktif",
    "1.6.0": "Maksimum talep",
    "32.7.0": "Gerilim L1",
    "52.7.0": "Gerilim L2",
    "72.7.0": "Gerilim L3",
    "31.7.0": "Akım L1",
    "51.7.0": "Akım L2",
    "71.7.0": "Akım L3",
    "F.F": "Hata kodu",
}


def obis_kisa(adres: str) -> str:
    """'1-0:1.8.0*255' -> '1.8.0'"""
    if ":" in adres:
        adres = adres.split(":", 1)[1]
    return adres.split("*", 1)[0].split("&", 1)[0]
