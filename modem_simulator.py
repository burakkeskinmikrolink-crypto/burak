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
import time

from osos import iec62056 as iec, veritabani

MARKALAR = [("/LUN5LUNA-ELEKTRIK", "LUNA"), ("/KHL5X5", "KOHLER")]


def veri_blogu(seri: str, endeks: float, faz_kaybi: int = 0) -> bytes:
    """Trifaze bir sayacın kısa okumasına benzer veri bloğu."""
    t1, t2 = endeks * 0.55, endeks * 0.2
    v = [random.uniform(224, 236) for _ in range(3)]
    a = [random.uniform(3, 18) for _ in range(3)]
    if faz_kaybi:
        v[faz_kaybi - 1], a[faz_kaybi - 1] = 0.0, 0.0
    pf = [random.uniform(0.88, 0.99) for _ in range(3)]
    p = [v[i] * a[i] * pf[i] / 1000 for i in range(3)]
    simdi = time.localtime()
    satirlar = [
        f"0.0.0({seri})", "0.2.0(V1.04)",
        time.strftime("0.9.1(%H:%M:%S)", simdi), time.strftime("0.9.2(%y-%m-%d)", simdi),
        f"1.8.0({endeks:010.3f}*kWh)", f"1.8.1({t1:010.3f}*kWh)", f"1.8.2({t2:010.3f}*kWh)",
        f"1.8.3({endeks - t1 - t2:010.3f}*kWh)", "2.8.0(000000.000*kWh)",
        f"5.8.0({endeks * 0.18:010.3f}*kvarh)", f"8.8.0({endeks * 0.02:010.3f}*kvarh)",
        f"1.6.0({max(p) * 3.1:06.3f}*kW)({time.strftime('%y-%m-%d', simdi)} 14:15)",
        f"32.7.0({v[0]:05.1f}*V)", f"52.7.0({v[1]:05.1f}*V)", f"72.7.0({v[2]:05.1f}*V)",
        f"31.7.0({a[0]:06.2f}*A)", f"51.7.0({a[1]:06.2f}*A)", f"71.7.0({a[2]:06.2f}*A)",
        f"33.7.0({pf[0]:.2f})", f"53.7.0({pf[1]:.2f})", f"73.7.0({pf[2]:.2f})",
        f"13.7.0({sum(pf) / 3:.2f})", f"14.7.0({random.uniform(49.95, 50.05):.2f}*Hz)",
        f"1.7.0({sum(p):06.3f}*kW)",
        f"C.7.0({random.randint(10, 60):04d})", f"C.7.1({random.randint(1, 20):04d})",
        f"C.7.2({random.randint(1, 20):04d})", f"C.7.3({random.randint(1, 20):04d})",
        "F.F(00000000)", "!",
    ]
    govde = ("\r\n".join(satirlar) + "\r\n").encode() + bytes([iec.ETX])
    return bytes([iec.STX]) + govde + bytes([iec.bcc(govde)])


async def modem(host, port, imei, seri, davranis, aralik):
    kimlik = random.choice(MARKALAR)[0]
    faz_kaybi = random.choice([1, 2, 3]) if davranis == "faz_kaybi" else 0
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
                        blok = veri_blogu(seri, endeks, faz_kaybi)
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
        if z < args.sayac_yok:
            davranis = "sayac_yok"
        elif z < args.sayac_yok + args.kapali:
            davranis = "kapali"
        elif z < args.sayac_yok + args.kapali + args.faz_kaybi:
            davranis = "faz_kaybi"
        else:
            davranis = "normal"
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
    ap.add_argument("--faz-kaybi", type=float, default=0.08, help="Bir fazı olmayan sayaç oranı")
    ap.add_argument("--db", default="osos.db")
    try:
        asyncio.run(ana(ap.parse_args()))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
