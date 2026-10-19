"""Sunucu, panel ve envanter araçlarının ortak SQLite yapısı."""

import sqlite3

SEMA = """
CREATE TABLE IF NOT EXISTS baglantilar (
    id INTEGER PRIMARY KEY, baslangic TEXT, bitis TEXT,
    ip TEXT, port INTEGER, protokol TEXT,
    imei TEXT, iccid TEXT, ilk_veri_hex TEXT, toplam_byte INTEGER
);
CREATE TABLE IF NOT EXISTS okumalar (
    id INTEGER PRIMARY KEY, zaman TEXT, baglanti_id INTEGER,
    imei TEXT, sayac_kimlik TEXT, bcc_dogru INTEGER, ham TEXT
);
CREATE TABLE IF NOT EXISTS degerler (
    okuma_id INTEGER, obis TEXT, deger TEXT, birim TEXT
);
-- EnerClever'dan aktarılan saha listesi
CREATE TABLE IF NOT EXISTS modemler (
    imei TEXT PRIMARY KEY, ad TEXT, saha TEXT, gsm TEXT, iccid TEXT,
    musteri TEXT, aciklama TEXT
);
CREATE TABLE IF NOT EXISTS sayaclar (
    seri_no TEXT PRIMARY KEY, ad TEXT, saha TEXT, marka TEXT, model TEXT,
    bolge TEXT, alt_bolge TEXT, eski_son_okuma TEXT
);
CREATE INDEX IF NOT EXISTS ix_bag_imei ON baglantilar(imei);
CREATE INDEX IF NOT EXISTS ix_oku_imei ON okumalar(imei);
CREATE INDEX IF NOT EXISTS ix_deger_okuma ON degerler(okuma_id);
"""


def baglan(yol: str) -> sqlite3.Connection:
    db = sqlite3.connect(yol, check_same_thread=False)
    db.row_factory = sqlite3.Row
    db.executescript(SEMA)
    db.commit()
    return db


def saha_adi(ad: str) -> str:
    """EnerClever adlarını ortak saha anahtarına çevirir.

    'M-B34_M1523_BOGAZICI_KAPSAL' ve 'S-B34_M1523_BOGAZICI_KAPSAL'
    ikisi de 'B34_M1523_BOGAZICI_KAPSAL' olur; modem ile sayaç böyle eşleşir.
    """
    ad = (ad or "").strip()
    if len(ad) > 2 and ad[1] == "-" and ad[0].upper() in "MS":
        ad = ad[2:]
    return ad.upper()
