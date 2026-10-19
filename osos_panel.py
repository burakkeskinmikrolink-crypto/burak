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

from osos import iec62056 as iec, olcumler, veritabani

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


def son_degerler(db, okuma_id):
    if okuma_id is None:
        return {}
    return olcumler.degerleri_topla(
        (r["obis"], r["deger"], r["birim"])
        for r in db.execute("SELECT obis, deger, birim FROM degerler WHERE okuma_id=?", (okuma_id,))
    )


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
           s.seri_no, s.marka, s.eski_son_okuma, s.eski_durum
    FROM tum t
    LEFT JOIN modemler m ON m.imei = t.imei
    LEFT JOIN sb ON sb.imei = t.imei
    LEFT JOIN so ON so.imei = t.imei
    LEFT JOIN okumalar o ON o.id = so.oid
    LEFT JOIN sayaclar s ON s.seri_no = (
        SELECT seri_no FROM sayaclar WHERE modem_imei = t.imei
           OR (saha = m.saha AND m.saha != '') LIMIT 1)
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
        degerler = son_degerler(db, r["oid"])
        endeks = degerler.get("1.8.0", [("", "")])[0]
        alarm = olcumler.alarmlar(degerler) if durum in ("ok", "bagli") else []
        if durum == "sessiz":
            alarm = [("kritik", f"{esik_saat:g} saattir veri yok")]
        liste.append({
            "imei": r["imei"],
            "ad": r["ad"] or "(EnerClever listesinde yok)",
            "gsm": r["gsm"] or "",
            "sayac": r["seri_no"] or "",
            "marka": r["marka"] or "",
            "eski_son_okuma": r["eski_son_okuma"] or "",
            "eski_durum": r["eski_durum"] or "",
            "son_bag": son_bag,
            "son_oku": son_oku,
            "baglanti_adedi": r["adet"] or 0,
            "sayac_kimlik": r["sayac_kimlik"] or "",
            "endeks": endeks[0],
            "birim": endeks[1],
            "durum": durum,
            "fazlar": olcumler.faz_durumu(degerler),
            "alarmlar": alarm,
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
select,input{padding:8px 10px;border:1px solid var(--cizgi);border-radius:8px;background:var(--kart);color:var(--yazi);min-width:260px}
.tablo{overflow-x:auto;background:var(--kart);border:1px solid var(--cizgi);border-radius:10px}
table{border-collapse:collapse;width:100%}th,td{padding:8px 12px;text-align:left;border-bottom:1px solid var(--cizgi);white-space:nowrap}
th{font-size:12px;color:var(--soluk);font-weight:600;text-transform:uppercase;letter-spacing:.03em}
td.sayi{text-align:right;font-variant-numeric:tabular-nums}
.d{display:inline-flex;align-items:center;gap:6px}.d:before{content:"";width:8px;height:8px;border-radius:50%;background:currentColor}
.faz{display:inline-block;width:22px;text-align:center;font-size:11px;font-weight:600;border-radius:4px;margin-right:2px;
padding:1px 0;background:var(--cizgi);color:var(--soluk)}.faz.ok{background:var(--ok);color:#fff}
.faz.yok{background:var(--sessiz);color:#fff}.faz.dusuk,.faz.yuksek{background:var(--bagli);color:#fff}
.kritik{color:var(--sessiz)}.uyari{color:var(--bagli)}
.ikili{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:16px}
svg text{fill:var(--soluk);font-size:11px}
.ok{color:var(--ok)}.bagli{color:var(--bagli)}.sessiz{color:var(--sessiz)}.hic{color:var(--hic)}
pre{background:var(--kart);border:1px solid var(--cizgi);border-radius:10px;padding:12px;overflow:auto;font-size:12px}
h2{font-size:16px;margin:24px 0 8px}
"""


def sayfa(baslik, govde, yenile=False):
    meta = '<meta http-equiv="refresh" content="60">' if yenile else ""
    return f"""<!doctype html><html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">{meta}
<title>{html.escape(baslik)}</title><style>{CSS}</style></head><body>
<header><h1><a href="/" style="color:inherit">OSOS Panel</a></h1><a href="/">Sahalar</a><a href="/rapor">Enerji Raporu</a>
<span>{html.escape(baslik)}</span>
<span style="margin-left:auto">{dt.datetime.now():%d.%m.%Y %H:%M}</span></header>
<main>{govde}</main></body></html>"""


def faz_rozet(fazlar):
    if not any(fazlar):
        return ""
    adlar = {"ok": "normal", "yok": "faz yok", "dusuk": "düşük gerilim", "yuksek": "yüksek gerilim", None: "bilgi yok"}
    return "".join(f'<span class="faz {d or ""}" title="L{i}: {adlar[d]}">L{i}</span>'
                   for i, d in enumerate(fazlar, 1))


def alarm_metni(liste):
    if not liste:
        return ""
    seviye = "kritik" if any(s == "kritik" for s, _ in liste) else "uyari"
    ek = f" (+{len(liste) - 1})" if len(liste) > 1 else ""
    tum = "; ".join(m for _, m in liste)
    return f'<span class="{seviye}" title="{html.escape(tum)}">{html.escape(liste[0][1])}{ek}</span>'


def ana_sayfa(db, esik):
    liste = saha_listesi(db, esik)
    sayilar = {k: sum(1 for x in liste if x["durum"] == k) for k in DURUMLAR}
    kartlar = f'<div class="kart secili" data-f=""><small>Toplam saha</small><b>{len(liste)}</b></div>'
    for k, (ad, aciklama) in DURUMLAR.items():
        kartlar += (f'<div class="kart" data-f="{k}" title="{html.escape(aciklama)}">'
                    f'<small class="d {k}">{ad}</small><b>{sayilar[k]}</b></div>')
    alarmli = sum(1 for x in liste if x["alarmlar"])
    kartlar += (f'<div class="kart" data-f="alarm"><small class="d kritik">Alarm var</small>'
                f'<b>{alarmli}</b></div>')
    satirlar = ""
    for x in liste:
        e = html.escape
        satirlar += (
            f'<tr data-d="{x["durum"]}" data-a="{1 if x["alarmlar"] else ""}"><td><a href="/modem/{e(x["imei"])}">{e(x["ad"])}</a></td>'
            f'<td>{e(x["imei"])}</td><td>{e(x["gsm"])}</td><td>{e(x["sayac"])} {e(x["marka"])}</td>'
            f'<td><span class="d {x["durum"]}">{DURUMLAR[x["durum"]][0]}</span></td>'
            f'<td>{faz_rozet(x["fazlar"])}</td><td>{alarm_metni(x["alarmlar"])}</td>'
            f'<td title="{x["son_bag"] or ""}">{once(x["son_bag"])}</td>'
            f'<td title="{x["son_oku"] or ""}">{once(x["son_oku"])}</td>'
            f'<td class="sayi">{e(x["endeks"])} {e(x["birim"])}</td>'
            f'<td>{e(x["eski_durum"])}</td><td>{e(x["eski_son_okuma"])}</td></tr>'
        )
    if not liste:
        satirlar = ('<tr><td colspan="12">Henüz kayıt yok. Önce <code>envanter_yukle.py</code> ile '
                    'EnerClever listesini yükle ya da <code>osos_server.py</code> çalıştır.</td></tr>')
    govde = f"""
<div class="kartlar">{kartlar}</div>
<div class="arac"><input id="ara" placeholder="Saha, IMEI, GSM ya da sayaç ara">
<a href="/okumalar.csv">Son okumaları CSV indir</a></div>
<div class="tablo"><table><thead><tr><th>Saha / Modem</th><th>IMEI</th><th>GSM</th><th>Sayaç</th>
<th>Durum</th><th>Fazlar</th><th>Alarm</th><th>Son bağlantı</th><th>Son okuma</th><th>1.8.0</th><th>EnerClever durumu</th><th>EnerClever son okuma</th></tr></thead>
<tbody id="liste">{satirlar}</tbody></table></div>
<script>
let filtre="";const ara=document.getElementById("ara");
function uygula(){{const q=ara.value.toLowerCase();
document.querySelectorAll("#liste tr[data-d]").forEach(tr=>{{
tr.hidden=(filtre==="alarm"?!tr.dataset.a:(filtre&&tr.dataset.d!==filtre))||(q&&!tr.textContent.toLowerCase().includes(q));}});}}
ara.oninput=uygula;
document.querySelectorAll(".kart").forEach(k=>k.onclick=()=>{{filtre=k.dataset.f;
document.querySelectorAll(".kart").forEach(x=>x.classList.toggle("secili",x===k));uygula();}});
</script>"""
    return sayfa(f"Eşik: {esik} saat", govde, yenile=True)


def cizgi_grafik(seriler, baslik, birim, yukseklik=180):
    """Basit SVG çizgi grafik. seriler: [(ad, renk_degiskeni, [(zaman_str, deger), ...]), ...]"""
    noktalar = [(z, v) for _, _, liste in seriler for z, v in liste]
    if len(noktalar) < 2:
        return ""
    gen, sol, alt, ust = 640, 48, 22, 10
    zamanlar = sorted({z for z, _ in noktalar})
    xi = {z: i for i, z in enumerate(zamanlar)}
    vmin, vmax = min(v for _, v in noktalar), max(v for _, v in noktalar)
    if vmax == vmin:
        vmax, vmin = vmax + 1, vmin - 1
    def x(z):
        return sol + (gen - sol - 8) * xi[z] / max(1, len(zamanlar) - 1)
    def y(v):
        return ust + (yukseklik - ust - alt) * (1 - (v - vmin) / (vmax - vmin))
    svg = [f'<svg viewBox="0 0 {gen} {yukseklik}" width="100%" role="img" aria-label="{html.escape(baslik)}">']
    for v in (vmin, (vmin + vmax) / 2, vmax):
        svg.append(f'<line x1="{sol}" x2="{gen - 8}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="var(--cizgi)"/>'
                   f'<text x="{sol - 6}" y="{y(v) + 4:.1f}" text-anchor="end">{v:,.1f}</text>')
    svg.append(f'<text x="{sol}" y="{yukseklik - 4}">{zamanlar[0][5:16]}</text>'
               f'<text x="{gen - 8}" y="{yukseklik - 4}" text-anchor="end">{zamanlar[-1][5:16]}</text>')
    lejant = ""
    for ad, renk, liste in seriler:
        if not liste:
            continue
        yol = " ".join(f"{x(z):.1f},{y(v):.1f}" for z, v in liste)
        svg.append(f'<polyline points="{yol}" fill="none" stroke="{renk}" stroke-width="2">'
                   f'<title>{html.escape(ad)}</title></polyline>')
        lejant += f'<span class="d" style="color:{renk};margin-right:12px">{html.escape(ad)}</span>'
    svg.append("</svg>")
    return (f'<div class="tablo" style="padding:12px 14px"><b>{html.escape(baslik)}</b> '
            f'<small style="color:var(--soluk)">({birim})</small><div>{lejant}</div>{"".join(svg)}</div>')


def gecmis(db, imei, kodlar, adet=200):
    """Son okumalardaki belirli kodların zaman serisi: {kod: [(zaman, deger), ...]}"""
    seriler = {k: [] for k in kodlar}
    satirlar = db.execute(
        "SELECT o.zaman, d.obis, d.deger FROM okumalar o JOIN degerler d ON d.okuma_id = o.id "
        "WHERE o.id IN (SELECT id FROM okumalar WHERE imei=? AND bcc_dogru=1 ORDER BY id DESC LIMIT ?) "
        "ORDER BY o.zaman", (imei, adet))
    gorulen = set()
    for r in satirlar:
        k = iec.obis_kisa(r["obis"])
        v = olcumler.sayi(r["deger"])
        if k in seriler and v is not None and (r["zaman"], k) not in gorulen:
            gorulen.add((r["zaman"], k))
            seriler[k].append((r["zaman"], v))
    return seriler


def gunluk_tuketim(endeks_serisi):
    """1.8.0 serisinden günlük tüketim: [(gün, kWh), ...]"""
    gun_sonu = {}
    for z, v in endeks_serisi:
        gun_sonu[z[:10]] = v
    gunler = sorted(gun_sonu)
    return [(f"{g} 00:00", round(gun_sonu[g] - gun_sonu[o], 3))
            for o, g in zip(gunler, gunler[1:]) if gun_sonu[g] >= gun_sonu[o]]


def modem_sayfasi(db, imei):
    e = html.escape
    m = db.execute("SELECT * FROM modemler WHERE imei=?", (imei,)).fetchone()
    s = db.execute(
        "SELECT * FROM sayaclar WHERE modem_imei=? OR (saha=? AND saha!='') ORDER BY modem_imei=? DESC LIMIT 1",
        (imei, m["saha"] if m else "", imei),
    ).fetchone()
    son = db.execute("SELECT * FROM okumalar WHERE imei=? ORDER BY id DESC LIMIT 1", (imei,)).fetchone()
    degerler = son_degerler(db, son["id"] if son else None)

    bilgi = ""
    for etiket, deger in (
        ("Modem", m["ad"] if m else "(listede yok)"), ("IMEI", imei),
        ("GSM", m["gsm"] if m else ""), ("ICCID", m["iccid"] if m else ""),
        ("Sayaç", f'{s["seri_no"]} {s["marka"] or ""} {s["model"] or ""}' if s else ""),
        ("Saha Id", s["sube_kodu"] if s else ""),
        ("Bölge", " / ".join(x for x in ((s["bolge"] or ""), (s["alt_bolge"] or "")) if x) if s else ""),
        ("Sayaç kimliği", son["sayac_kimlik"] if son else ""),
        ("Son okuma", son["zaman"] if son else "—"),
        ("EnerClever durumu", f'{s["eski_durum"] or ""} {s["eski_son_okuma"] or ""}' if s else ""),
    ):
        if deger and str(deger).strip():
            bilgi += f"<tr><th>{etiket}</th><td>{e(str(deger))}</td></tr>"

    # Alarmlar
    alarm = olcumler.alarmlar(degerler)
    alarm_html = "".join(f'<li class="{sv}">{e(msj)}</li>' for sv, msj in alarm) or '<li class="ok">Sorun yok</li>'

    # Faz tablosu
    fazlar = olcumler.faz_durumu(degerler)
    faz_html = ""
    for olcu, hucreler in olcumler.faz_tablosu(degerler):
        faz_html += f"<tr><th>{olcu}</th>" + "".join(
            f'<td class="sayi">{e(h[0])} {e(h[1])}</td>' if h else '<td class="sayi">—</td>' for h in hucreler
        ) + "</tr>"
    if faz_html:
        faz_html = (f'<div class="tablo"><table><thead><tr><th>Faz</th>'
                    + "".join(f'<th><span class="faz {d or ""}">L{i + 1}</span></th>'
                              for i, d in enumerate(fazlar))
                    + f"</tr></thead>{faz_html}</table></div>")

    # Gruplu değerler
    gruplar, diger = olcumler.gruplu(degerler)
    grup_html = ""
    for grup, satirlar in gruplar:
        govde = "".join(
            f'<tr><td>{e(ad)}</td><td style="color:var(--soluk)">{e(kod)}</td>'
            f'<td class="sayi">{e(d)}</td><td>{e(b)}</td><td>{e(ek)}</td></tr>'
            for ad, kod, d, b, ek in satirlar)
        grup_html += (f'<div class="tablo"><table><thead><tr><th colspan="5">{e(grup)}</th></tr></thead>'
                      f"{govde}</table></div>")
    if diger:
        govde = "".join(f'<tr><td>{e(k)}</td><td class="sayi">{e(d)}</td><td>{e(b)}</td></tr>'
                        for k, d, b in diger)
        grup_html += (f'<div class="tablo"><table><thead><tr><th colspan="3">Diğer (sayacın gönderdiği tüm kodlar)'
                      f"</th></tr></thead>{govde}</table></div>")

    # Grafikler
    g = gecmis(db, imei, ["1.8.0", "32.7.0", "52.7.0", "72.7.0", "31.7.0", "51.7.0", "71.7.0"])
    gunluk = gunluk_tuketim(g["1.8.0"])
    grafikler = (
        cizgi_grafik([("Günlük tüketim", "var(--vurgu)", gunluk)], "Günlük tüketim", "kWh")
        + cizgi_grafik([("L1", "#d92d20", g["32.7.0"]), ("L2", "#f79009", g["52.7.0"]),
                        ("L3", "#1570ef", g["72.7.0"])], "Faz gerilimleri", "V")
        + cizgi_grafik([("L1", "#d92d20", g["31.7.0"]), ("L2", "#f79009", g["51.7.0"]),
                        ("L3", "#1570ef", g["71.7.0"])], "Faz akımları", "A")
    )

    okumalar = ""
    for r in db.execute("SELECT * FROM okumalar WHERE imei=? ORDER BY id DESC LIMIT 30", (imei,)):
        dg = son_degerler(db, r["id"])
        okumalar += f"<tr><td>{r['zaman']}</td>"
        for k in ("1.8.0", "1.8.1", "1.8.2", "1.8.3", "32.7.0", "52.7.0", "72.7.0"):
            okumalar += f'<td class="sayi">{e(dg.get(k, [("", "")])[0][0])}</td>'
        okumalar += f"<td>{'doğru' if r['bcc_dogru'] else 'HATALI'}</td></tr>"

    baglantilar = ""
    for r in db.execute("SELECT * FROM baglantilar WHERE imei=? ORDER BY id DESC LIMIT 30", (imei,)):
        ilk = bytes.fromhex(r["ilk_veri_hex"] or "")[:80]
        baglantilar += (f"<tr><td>{r['baslangic']}</td><td>{r['bitis'] or 'açık'}</td>"
                        f"<td>{e(r['ip'] or '')}</td><td>{r['protokol']}</td>"
                        f"<td class='sayi'>{r['toplam_byte'] or 0}</td>"
                        f"<td><code>{e(ilk.decode('ascii', 'replace'))}</code></td></tr>")

    govde = f"""
<div class="ikili">
<div class="tablo"><table>{bilgi}</table></div>
<div><div class="tablo" style="padding:12px 14px"><b>Alarmlar</b><ul style="margin:6px 0 0;padding-left:18px">{alarm_html}</ul></div>
<div style="margin-top:12px">{faz_html}</div></div>
</div>
<h2>Grafikler</h2><div class="ikili">{grafikler or '<p>Grafik için en az iki okuma gerekiyor.</p>'}</div>
<h2>Son okumadaki tüm değerler</h2><div class="ikili">{grup_html or '<p>Okuma yok.</p>'}</div>
<h2>Okuma geçmişi</h2><div class="tablo"><table><thead><tr><th>Zaman</th><th>1.8.0</th><th>T1</th><th>T2</th>
<th>T3</th><th>L1 V</th><th>L2 V</th><th>L3 V</th><th>BCC</th></tr></thead>
<tbody>{okumalar or '<tr><td colspan="9">Okuma yok</td></tr>'}</tbody></table></div>
<h2>Bağlantılar</h2><div class="tablo"><table><thead><tr><th>Başlangıç</th><th>Bitiş</th><th>IP</th>
<th>Prot.</th><th>Byte</th><th>İlk gelen veri</th></tr></thead>
<tbody>{baglantilar or '<tr><td colspan="6">Bağlantı yok</td></tr>'}</tbody></table></div>
<h2>Son ham okuma</h2><pre>{e(son['ham'] or '') if son else '—'}</pre>"""
    return sayfa(m["ad"] if m else imei, govde)


def okumalar_csv(db, esik):
    cikti = io.StringIO()
    w = csv.writer(cikti, delimiter=";")
    w.writerow(["Saha", "IMEI", "GSM", "Sayac", "Durum", "Son baglanti", "Son okuma", "1.8.0", "Birim",
                "EnerClever durumu", "EnerClever son okuma"])
    for x in saha_listesi(db, esik):
        w.writerow([x["ad"], x["imei"], x["gsm"], x["sayac"], DURUMLAR[x["durum"]][0],
                    x["son_bag"] or "", x["son_oku"] or "", x["endeks"], x["birim"],
                    x["eski_durum"], x["eski_son_okuma"]])
    return ("﻿" + cikti.getvalue()).encode("utf-8")  # Excel Türkçe karakterleri doğru açsın


RAPOR_KOLONLARI = ["Sayaç No", "Sayaç Adı", "Modem No", "Modem", "SIMKART GSM No", "Alt Bölge",
                   "Şehir", "Saha Adı", "Saha Id", "kWh"]


def _ay_sinirlari(ay):
    bas = dt.datetime.strptime(ay + "-01", "%Y-%m-%d")
    son = (bas + dt.timedelta(days=32)).replace(day=1)
    return bas, son


def enerji_raporu(db, ay):
    """EnerClever 'Enerji Raporu' ile aynı tablo, bizim okumalarımızdan.

    Aylık tüketim = ay sonundaki son 1.8.0 - ay başından önceki son 1.8.0
    (ay başından önce okuma yoksa ayın ilk okuması kullanılır).
    """
    bas, son = _ay_sinirlari(ay)
    bas_s, son_s = bas.strftime("%Y-%m-%d %H:%M:%S"), son.strftime("%Y-%m-%d %H:%M:%S")
    endeksler_imei = {}
    for r in db.execute(
        "SELECT o.imei, o.zaman, d.obis, d.deger FROM okumalar o JOIN degerler d ON d.okuma_id = o.id "
        "WHERE o.zaman < ? AND o.bcc_dogru = 1 ORDER BY o.zaman", (son_s,)
    ):
        if iec.obis_kisa(r["obis"]) != "1.8.0":
            continue
        try:
            deger = float(r["deger"])
        except ValueError:
            continue
        endeksler_imei.setdefault(r["imei"], []).append((r["zaman"], deger))

    eski = {r["seri_no"]: r["kwh"] for r in db.execute(
        "SELECT seri_no, kwh FROM aylik_tuketim WHERE ay=? AND kaynak='enerclever'", (ay,))}

    satirlar = []
    for r in db.execute(
        "SELECT s.*, m.ad modem_ad, m.gsm FROM sayaclar s LEFT JOIN modemler m ON m.imei = s.modem_imei "
        "ORDER BY s.seri_no"
    ):
        liste = endeksler_imei.get(r["modem_imei"], [])
        once = [d for z, d in liste if z < bas_s]
        icinde = [d for z, d in liste if z >= bas_s]
        kwh = None
        if icinde and (once or len(icinde) > 1):
            ilk = once[-1] if once else icinde[0]
            if icinde[-1] >= ilk:
                kwh = round(icinde[-1] - ilk, 3)
        satirlar.append({
            "Sayaç No": r["seri_no"], "Sayaç Adı": r["ad"] or "", "Modem No": r["modem_imei"] or "",
            "Modem": r["modem_ad"] or "", "SIMKART GSM No": r["gsm"] or "",
            "Alt Bölge": r["alt_bolge"] or r["bolge"] or "", "Şehir": r["sehir"] or "",
            "Saha Adı": r["saha"] or "", "Saha Id": r["sube_kodu"] or "",
            "kWh": kwh, "EnerClever kWh": eski.get(r["seri_no"]),
        })
    return satirlar


def _sayi(v):
    return "" if v is None else f"{v:,.3f}".replace(",", "X").replace(".", ",").replace("X", ".")


def rapor_sayfasi(db, ay):
    e = html.escape
    aylar = [r[0] for r in db.execute(
        "SELECT DISTINCT substr(zaman, 1, 7) FROM okumalar UNION "
        "SELECT DISTINCT ay FROM aylik_tuketim ORDER BY 1 DESC")]
    if ay not in aylar:
        aylar.insert(0, ay)
    secenek = "".join(f'<option{" selected" if a == ay else ""}>{a}</option>' for a in aylar)
    satirlar = enerji_raporu(db, ay)
    bizde = [x for x in satirlar if x["kWh"] is not None]
    eskide = [x for x in satirlar if x["EnerClever kWh"] is not None]
    kartlar = (
        f'<div class="kart"><small>Sayaç</small><b>{len(satirlar)}</b></div>'
        f'<div class="kart"><small class="d ok">Bizim sistemde tüketimi çıkan</small><b>{len(bizde)}</b></div>'
        f'<div class="kart"><small>Toplam kWh (bizim)</small><b>{_sayi(sum(x["kWh"] for x in bizde)).split(",")[0]}</b></div>'
        f'<div class="kart"><small>EnerClever raporunda olan</small><b>{len(eskide)}</b></div>'
    )
    govde_satir = ""
    for x in satirlar:
        govde_satir += "<tr>" + "".join(
            f'<td class="sayi">{_sayi(x[k])}</td>' if k == "kWh" else f"<td>{e(str(x[k]))}</td>"
            for k in RAPOR_KOLONLARI
        ) + f'<td class="sayi">{_sayi(x["EnerClever kWh"])}</td></tr>'
    baslik = "".join(f"<th>{e(k)}</th>" for k in RAPOR_KOLONLARI) + "<th>EnerClever kWh</th>"
    govde = f"""
<form class="arac"><label>Dönem <select name="ay" onchange="this.form.submit()">{secenek}</select></label>
<a href="/rapor.csv?ay={e(ay)}">Excel için indir (CSV)</a></form>
<div class="kartlar">{kartlar}</div>
<div class="tablo"><table><thead><tr>{baslik}</tr></thead><tbody>{govde_satir}</tbody></table></div>"""
    return sayfa(f"Enerji Raporu {ay}", govde)


def rapor_csv(db, ay):
    cikti = io.StringIO()
    w = csv.writer(cikti, delimiter=";")
    w.writerow(RAPOR_KOLONLARI)
    for x in enerji_raporu(db, ay):
        w.writerow([_sayi(x[k]).replace(".", "") if k == "kWh" else x[k] for k in RAPOR_KOLONLARI])
    return ("\ufeff" + cikti.getvalue()).encode("utf-8")


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
                elif url.path in ("/rapor", "/rapor.csv"):
                    q = parse_qs(url.query)
                    gecen = (dt.date.today().replace(day=1) - dt.timedelta(days=1)).strftime("%Y-%m")
                    ay = q.get("ay", [gecen])[0]
                    try:
                        _ay_sinirlari(ay)
                    except ValueError:
                        ay = gecen
                    if url.path == "/rapor":
                        self.gonder(200, rapor_sayfasi(db, ay))
                    else:
                        self.gonder(200, rapor_csv(db, ay), "text/csv; charset=utf-8",
                                    {"Content-Disposition": f"attachment; filename=EnerjiRaporu_{ay}.csv"})
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
