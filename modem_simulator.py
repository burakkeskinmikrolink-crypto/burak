#!/usr/bin/env python3
"""Sahte modemler: osos_server.py'ye bağlanıp sayaç gibi cevap verir.

Gerçek modem yokken sunucuyu, veritabanını ve paneli uçtan uca denemek
ve sunumda canlı göstermek için.

Kullanım (üç ayrı pencerede):
    python osos_server.py --port 9000 --oku --bekle 1
    python modem_simulator.py --port 9000 --adet 20
    python osos_panel.py                     # http://localhost:8000

Veritabanında EnerClever listesi yüklüyse onun IMEI'lerini kullanır,
yoksa uydurma IMEI üretir. Bir kısmı "sayaç cevap vermiyor", bir kısmı
"hiç bağlanmıyor" gibi davranır; panelde tüm durumlar görünür.
"""

import argparse
import asyncio
import random

from osos import iec62056 as iec, veritabani

MARKALAR = [("/LUN5LUNA-ELEKTRIK", "LUNA"), ("/KHL5X5", "KOHLER")]


def veri_blogu(seri: str, endeks: float) -> bytes:
    t1, t2 = endeks * 0.55, endeks * 0.2
    metin = (
        f"0.0.0({seri})\r\n"
        f"1.8.0({endeks:010.3f}*kWh)\r\n"
        f"1.8.1({t1:010.3f}*kWh)\r\n"
        f"1.8.2({t2:010.3f}*kWh)\r\n"
        f"1.8.3({endeks - t1 - t2:010.3f}*kWh)\r\n"
        f"32.7.0({random.uniform(222, 235):05.1f}*V)\r\n"
        "!\r\n"
    )
    govde = metin.encode() + bytes([iec.ETX])
    return bytes([iec.STX]) + govde + bytes([iec.bcc(govde)])


async def modem(host, port, imei, seri, davranis, aralik):
    kimlik = random.choice(MARKALAR)[0]
    endeks = random.uniform(1000, 90000)
    while True:
        if davranis != "kapali":
            try:
                r, w = await asyncio.open_connection(host, port)
                w.write(f"IMEI:{imei};SW:AMRBGS5 1.540\r\n".encode())
                await w.drain()
                bitis = asyncio.get_running_loop().time() + 20
                while asyncio.get_running_loop().time() < bitis:
                    try:
                        satir = await asyncio.wait_for(r.readuntil(b"\n"), 20)
                    except (asyncio.TimeoutError, asyncio.IncompleteReadError):
                        break
                    if davranis == "sayac_yok":
                        continue  # RS485 kopuk: sayaç hiç cevap vermez
                    if satir.startswith(b"/?"):
                        await asyncio.sleep(random.uniform(0.2, 1.5))  # şebeke gecikmesi
                        w.write(kimlik.encode() + b"\r\n")
                    elif satir[:1] == bytes([iec.ACK]):
                        endeks += random.uniform(0.5, 30)
                        blok = veri_blogu(seri, endeks)
                        for i in range(0, len(blok), 40):  # parça parça
                            w.write(blok[i:i + 40])
                            await w.drain()
                            await asyncio.sleep(0.05)
                        await asyncio.sleep(0.5)
                        break
                    await w.drain()
                w.close()
            except OSError as e:
                print(f"{imei}: bağlanamadı ({e})")
        await asyncio.sleep(aralik * random.uniform(0.8, 1.2))


async def ana(args):
    db = veritabani.baglan(args.db)
    kayitlar = db.execute(
        "SELECT m.imei, s.seri_no FROM modemler m LEFT JOIN sayaclar s ON s.saha=m.saha AND m.saha!='' "
        "ORDER BY RANDOM() LIMIT ?", (args.adet,)
    ).fetchall()
    db.close()
    liste = [(r["imei"], r["seri_no"] or str(random.randint(10**8, 10**9))) for r in kayitlar]
    while len(liste) < args.adet:
        liste.append((f"3587410{random.randint(10**7, 10**8 - 1)}", str(random.randint(10**8, 10**9))))

    gorevler = []
    for i, (imei, seri) in enumerate(liste):
        z = random.random()
        davranis = "sayac_yok" if z < args.sayac_yok else "kapali" if z < args.sayac_yok + args.kapali else "normal"
        print(f"{imei}  sayaç {seri}  -> {davranis}")
        gorevler.append(modem(args.host, args.port, imei, seri, davranis, args.aralik))
    await asyncio.gather(*gorevler)


def main():
    ap = argparse.ArgumentParser(description="Sahte modem simülatörü")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=9000)
    ap.add_argument("--adet", type=int, default=10)
    ap.add_argument("--aralik", type=float, default=60, help="Her modem kaç saniyede bir bağlansın")
    ap.add_argument("--sayac-yok", type=float, default=0.15, help="Sayacı cevap vermeyen modem oranı")
    ap.add_argument("--kapali", type=float, default=0.1, help="Hiç bağlanmayan modem oranı")
    ap.add_argument("--db", default="osos.db")
    try:
        asyncio.run(ana(ap.parse_args()))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
