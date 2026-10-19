#!/usr/bin/env python3
"""OSOS web paneli: sahaların durumu, son okumalar, sessiz modemler.

Ek paket gerektirmez. osos_server.py ile aynı veritabanını okur.

Kullanım:
    python osos_panel.py                 # http://localhost:8000
    python osos_panel.py --port 8080 --db osos.db --esik 26
"""

import argparse
import csv
import datetime as dt
import html
import io
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse

from osos import iec62056 as iec, veritabani

ENDEKS_KODLARI = ("1.8.0", "1.8.1", "1.8.2", "1.8.3")

DURUMLAR = {
    "ok": ("Okunuyor", "Son okuma eşik süresi içinde"),
    "bagli": ("Bağlanıyor, okunamıyor", "Modem merkeze geliyor ama sayaç cevap vermiyor"),
    "sessiz": ("Sessiz", "Eşik süresinden uzun zamandır haber yok"),
    "hic": ("Hiç bağlanmadı", "Bu sistemde hiç bağlantı kaydı yok"),
}


def zaman(s):
    try:
        return dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%S") if s else None
    except ValueError:
        return None


def once(t):
    if not t:
        return "—"
    fark = dt.datetime.now() - t
    sn = int(fark.total_seconds())
    if sn < 120:
        return "az önce"
    if sn < 3600:
        return f"{sn // 60} dk önce"
    if sn < 86400 * 2:
        return f"{sn // 3600} saat önce"
    return f"{sn // 86400} gün önce"


def endeksler(db, okuma_id):
    sonuc = {}
    if okuma_id is None:
        return sonuc
    for r in db.execute("SELECT obis, deger, birim FROM degerler WHERE okuma_id=?", (okuma_id,)):
        kisa = iec.obis_kisa(r["obis"])
        if kisa in ENDEKS_KODLARI and kisa not in sonuc:
            sonuc[kisa] = (r["deger"], r["birim"])
    return sonuc


def saha_listesi(db, esik_saat):
    sorgu = """
    WITH tum AS (
        SELECT imei FROM modemler
        UNION SELECT imei FROM baglantilar WHERE imei IS NOT NULL
        UNION SELECT imei FROM okumalar WHERE imei IS NOT NULL
    ),
    sb AS (SELECT imei, MAX(baslangic) son, COUNT(*) adet FROM baglantilar
           WHERE imei IS NOT NULL GROUP BY imei),
    so AS (SELECT imei, MAX(id) oid FROM okumalar GROUP BY imei)
    SELECT t.imei, m.ad, m.saha, m.gsm, sb.son son_bag, sb.adet,
           so.oid, o.zaman son_okuma, o.sayac_kimlik, o.bcc_dogru,
           s.seri_no, s.marka, s.eski_son_okuma
    FROM tum t
    LEFT JOIN modemler m ON m.imei = t.imei
    LEFT JOIN sb ON sb.imei = t.imei
    LEFT JOIN so ON so.imei = t.imei
    LEFT JOIN okumalar o ON o.id = so.oid
    LEFT JOIN sayaclar s ON s.saha = m.saha AND m.saha != ''
    ORDER BY m.ad IS NULL, m.ad
    """
    simdi = dt.datetime.now()
    esik = dt.timedelta(hours=esik_saat)
    liste = []
    for r in db.execute(sorgu):
        son_bag, son_oku = zaman(r["son_bag"]), zaman(r["son_okuma"])
        if son_oku and simdi - son_oku <= esik:
            durum = "ok"
        elif son_bag and simdi - son_bag <= esik:
            durum = "bagli"
        elif son_bag or son_oku:
            durum = "sessiz"
        else:
            durum = "hic"
        e = endeksler(db, r["oid"])
        liste.append({
            "imei": r["imei"],
            "ad": r["ad"] or "(EnerClever listesinde yok)",
            "gsm": r["gsm"] or "",
            "sayac": r["seri_no"] or "",
            "marka": r["marka"] or "",
            "eski_son_okuma": r["eski_son_okuma"] or "",
            "son_bag": son_bag,
            "son_oku": son_oku,
            "baglanti_adedi": r["adet"] or 0,
            "sayac_kimlik": r["sayac_kimlik"] or "",
            "endeks": e.get("1.8.0", ("", ""))[0],
            "birim": e.get("1.8.0", ("", ""))[1],
            "durum": durum,
        })
    return liste


CSS = """
:root{--bg:#f6f7f9;--kart:#fff;--yazi:#1d2330;--soluk:#667085;--cizgi:#e4e7ec;
--ok:#12805c;--bagli:#b54708;--sessiz:#c4320a;--hic:#667085;--vurgu:#1d6fb8}
@media (prefers-color-scheme:dark){:root{--bg:#12151b;--kart:#1b2029;--yazi:#e6e9ef;
--soluk:#98a2b3;--cizgi:#2c3340;--ok:#3ccb8f;--bagli:#f5a524;--sessiz:#f97066;--hic:#98a2b3;--vurgu:#5ba8ef}}
*{box-sizing:border-box}body{margin:0;font:14px/1.45 system-ui,-apple-system,Segoe UI,sans-serif;
background:var(--bg);color:var(--yazi)}a{color:var(--vurgu);text-decoration:none}
header{padding:18px 24px;border-bottom:1px solid var(--cizgi);background:var(--kart);
display:flex;align-items:baseline;gap:16px;flex-wrap:wrap}header h1{margin:0;font-size:20px}
header span{color:var(--soluk)}main{padding:20px 24px;max-width:1400px;margin:auto}
.kartlar{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-bottom:18px}
.kart{background:var(--kart);border:1px solid var(--cizgi);border-radius:10px;padding:14px 16px;cursor:pointer}
.kart b{display:block;font-size:28px;font-variant-numeric:tabular-nums}.kart small:not(.d){color:var(--soluk)}
.kart.secili{outline:2px solid var(--vurgu)}
.arac{display:flex;gap:10px;margin-bottom:10px;flex-wrap:wrap}
input{padding:8px 10px;border:1px solid var(--cizgi);border-radius:8px;background:var(--kart);color:var(--yazi);min-width:260px}
.tablo{overflow-x:auto;background:var(--kart);border:1px solid var(--cizgi);border-radius:10px}
table{border-collapse:collapse;width:100%}th,td{padding:8px 12px;text-align:left;border-bottom:1px solid var(--cizgi);white-space:nowrap}
th{font-size:12px;color:var(--soluk);font-weight:600;text-transform:uppercase;letter-spacing:.03em}
td.sayi{text-align:right;font-variant-numeric:tabular-nums}
.d{display:inline-flex;align-items:center;gap:6px}.d:before{content:"";width:8px;height:8px;border-radius:50%;background:currentColor}
.ok{color:var(--ok)}.bagli{color:var(--bagli)}.sessiz{color:var(--sessiz)}.hic{color:var(--hic)}
pre{background:var(--kart);border:1px solid var(--cizgi);border-radius:10px;padding:12px;overflow:auto;font-size:12px}
h2{font-size:16px;margin:24px 0 8px}
"""


def sayfa(baslik, govde, yenile=False):
    meta = '<meta http-equiv="refresh" content="60">' if yenile else ""
    return f"""<!doctype html><html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">{meta}
<title>{html.escape(baslik)}</title><style>{CSS}</style></head><body>
<header><h1><a href="/" style="color:inherit">OSOS Panel</a></h1><span>{html.escape(baslik)}</span>
<span style="margin-left:auto">{dt.datetime.now():%d.%m.%Y %H:%M}</span></header>
<main>{govde}</main></body></html>"""


def ana_sayfa(db, esik):
    liste = saha_listesi(db, esik)
    sayilar = {k: sum(1 for x in liste if x["durum"] == k) for k in DURUMLAR}
    kartlar = f'<div class="kart secili" data-f=""><small>Toplam saha</small><b>{len(liste)}</b></div>'
    for k, (ad, aciklama) in DURUMLAR.items():
        kartlar += (f'<div class="kart" data-f="{k}" title="{html.escape(aciklama)}">'
                    f'<small class="d {k}">{ad}</small><b>{sayilar[k]}</b></div>')
    satirlar = ""
    for x in liste:
        e = html.escape
        satirlar += (
            f'<tr data-d="{x["durum"]}"><td><a href="/modem/{e(x["imei"])}">{e(x["ad"])}</a></td>'
            f'<td>{e(x["imei"])}</td><td>{e(x["gsm"])}</td><td>{e(x["sayac"])} {e(x["marka"])}</td>'
            f'<td><span class="d {x["durum"]}">{DURUMLAR[x["durum"]][0]}</span></td>'
            f'<td title="{x["son_bag"] or ""}">{once(x["son_bag"])}</td>'
            f'<td title="{x["son_oku"] or ""}">{once(x["son_oku"])}</td>'
            f'<td class="sayi">{e(x["endeks"])} {e(x["birim"])}</td>'
            f'<td>{e(x["eski_son_okuma"])}</td></tr>'
        )
    if not liste:
        satirlar = ('<tr><td colspan="9">Henüz kayıt yok. Önce <code>envanter_yukle.py</code> ile '
                    'EnerClever listesini yükle ya da <code>osos_server.py</code> çalıştır.</td></tr>')
    govde = f"""
<div class="kartlar">{kartlar}</div>
<div class="arac"><input id="ara" placeholder="Saha, IMEI, GSM ya da sayaç ara">
<a href="/okumalar.csv">Son okumaları CSV indir</a></div>
<div class="tablo"><table><thead><tr><th>Saha / Modem</th><th>IMEI</th><th>GSM</th><th>Sayaç</th>
<th>Durum</th><th>Son bağlantı</th><th>Son okuma</th><th>1.8.0</th><th>EnerClever son okuma</th></tr></thead>
<tbody id="liste">{satirlar}</tbody></table></div>
<script>
let filtre="";const ara=document.getElementById("ara");
function uygula(){{const q=ara.value.toLowerCase();
document.querySelectorAll("#liste tr[data-d]").forEach(tr=>{{
tr.hidden=(filtre&&tr.dataset.d!==filtre)||(q&&!tr.textContent.toLowerCase().includes(q));}});}}
ara.oninput=uygula;
document.querySelectorAll(".kart").forEach(k=>k.onclick=()=>{{filtre=k.dataset.f;
document.querySelectorAll(".kart").forEach(x=>x.classList.toggle("secili",x===k));uygula();}});
</script>"""
    return sayfa(f"Eşik: {esik} saat", govde, yenile=True)


def modem_sayfasi(db, imei):
    e = html.escape
    m = db.execute("SELECT * FROM modemler WHERE imei=?", (imei,)).fetchone()
    s = db.execute("SELECT * FROM sayaclar WHERE saha=? AND saha!=''", (m["saha"] if m else "",)).fetchone()
    bilgi = ""
    for etiket, deger in (
        ("Modem", m["ad"] if m else "(listede yok)"), ("IMEI", imei),
        ("GSM", m["gsm"] if m else ""), ("ICCID", m["iccid"] if m else ""),
        ("Sayaç", f'{s["seri_no"]} {s["marka"] or ""} {s["model"] or ""}' if s else ""),
        ("EnerClever son okuma", s["eski_son_okuma"] if s else ""),
    ):
        bilgi += f"<tr><th>{etiket}</th><td>{e(deger or '')}</td></tr>"

    okumalar = ""
    for r in db.execute("SELECT * FROM okumalar WHERE imei=? ORDER BY id DESC LIMIT 50", (imei,)):
        en = endeksler(db, r["id"])
        okumalar += f"<tr><td>{r['zaman']}</td><td>{e(r['sayac_kimlik'] or '')}</td>"
        for k in ENDEKS_KODLARI:
            okumalar += f'<td class="sayi">{e(en.get(k, ("", ""))[0])}</td>'
        okumalar += f"<td>{'doğru' if r['bcc_dogru'] else 'HATALI'}</td></tr>"

    baglantilar = ""
    for r in db.execute("SELECT * FROM baglantilar WHERE imei=? ORDER BY id DESC LIMIT 50", (imei,)):
        ilk = bytes.fromhex(r["ilk_veri_hex"] or "")[:80]
        baglantilar += (f"<tr><td>{r['baslangic']}</td><td>{r['bitis'] or 'açık'}</td>"
                        f"<td>{e(r['ip'] or '')}</td><td>{r['protokol']}</td>"
                        f"<td class='sayi'>{r['toplam_byte'] or 0}</td>"
                        f"<td><code>{e(ilk.decode('ascii', 'replace'))}</code></td></tr>")

    son = db.execute("SELECT ham FROM okumalar WHERE imei=? ORDER BY id DESC LIMIT 1", (imei,)).fetchone()
    govde = f"""
<div class="tablo" style="max-width:640px"><table>{bilgi}</table></div>
<h2>Okumalar</h2><div class="tablo"><table><thead><tr><th>Zaman</th><th>Sayaç kimliği</th>
<th>1.8.0</th><th>T1</th><th>T2</th><th>T3</th><th>BCC</th></tr></thead>
<tbody>{okumalar or '<tr><td colspan="7">Okuma yok</td></tr>'}</tbody></table></div>
<h2>Bağlantılar</h2><div class="tablo"><table><thead><tr><th>Başlangıç</th><th>Bitiş</th><th>IP</th>
<th>Prot.</th><th>Byte</th><th>İlk gelen veri</th></tr></thead>
<tbody>{baglantilar or '<tr><td colspan="6">Bağlantı yok</td></tr>'}</tbody></table></div>
<h2>Son ham okuma</h2><pre>{e(son['ham'] or '') if son else '—'}</pre>"""
    return sayfa(m["ad"] if m else imei, govde)


def okumalar_csv(db, esik):
    cikti = io.StringIO()
    w = csv.writer(cikti, delimiter=";")
    w.writerow(["Saha", "IMEI", "GSM", "Sayac", "Durum", "Son baglanti", "Son okuma", "1.8.0", "Birim"])
    for x in saha_listesi(db, esik):
        w.writerow([x["ad"], x["imei"], x["gsm"], x["sayac"], DURUMLAR[x["durum"]][0],
                    x["son_bag"] or "", x["son_oku"] or "", x["endeks"], x["birim"]])
    return ("﻿" + cikti.getvalue()).encode("utf-8")  # Excel Türkçe karakterleri doğru açsın


def isleyici_olustur(db_yolu, esik):
    class Isleyici(BaseHTTPRequestHandler):
        def gonder(self, kod, icerik, tur="text/html; charset=utf-8", ek=None):
            self.send_response(kod)
            self.send_header("Content-Type", tur)
            for k, v in (ek or {}).items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(icerik if isinstance(icerik, bytes) else icerik.encode("utf-8"))

        def do_GET(self):
            url = urlparse(self.path)
            db = veritabani.baglan(db_yolu)
            try:
                if url.path == "/":
                    self.gonder(200, ana_sayfa(db, esik))
                elif url.path.startswith("/modem/"):
                    self.gonder(200, modem_sayfasi(db, unquote(url.path[7:])))
                elif url.path == "/okumalar.csv":
                    self.gonder(200, okumalar_csv(db, esik), "text/csv; charset=utf-8",
                                {"Content-Disposition": "attachment; filename=osos_okumalar.csv"})
                elif url.path == "/api/sahalar":
                    q = parse_qs(url.query)
                    liste = saha_listesi(db, float(q.get("esik", [esik])[0]))
                    for x in liste:
                        x["son_bag"] = str(x["son_bag"] or "")
                        x["son_oku"] = str(x["son_oku"] or "")
                    self.gonder(200, json.dumps(liste, ensure_ascii=False), "application/json; charset=utf-8")
                else:
                    self.gonder(404, sayfa("Bulunamadı", "<p>Sayfa yok.</p>"))
            finally:
                db.close()

        def log_message(self, *a):
            pass

    return Isleyici


def main():
    ap = argparse.ArgumentParser(description="OSOS web paneli")
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--db", default="osos.db")
    ap.add_argument("--esik", type=float, default=26, help="Kaç saat haber yoksa 'sessiz' sayılsın")
    args = ap.parse_args()
    srv = ThreadingHTTPServer((args.host, args.port), isleyici_olustur(args.db, args.esik))
    print(f"Panel: http://localhost:{args.port}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
