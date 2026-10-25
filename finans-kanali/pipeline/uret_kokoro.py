"""Senaryodan ses uretir (Kokoro TTS, ucretsiz, yerel). Cikti: <ad>.wav

Kurulum: pip install kokoro soundfile numpy  (espeak-ng de gerekir)
Kullanim: python uret_kokoro.py senaryo.txt cikti_adi [ses]
Not: bu makinede test edilmedi; kurulumu sende dene.
"""
import sys

import numpy as np
import soundfile as sf
from kokoro import KPipeline

if len(sys.argv) < 3:
    sys.exit(__doc__)
metin = open(sys.argv[1], encoding="utf-8").read()
ses = sys.argv[3] if len(sys.argv) > 3 else "af_heart"
boru = KPipeline(lang_code="a")  # Amerikan Ingilizcesi
parcalar = [np.asarray(a) for _, _, a in boru(metin, voice=ses)]
sf.write(f"{sys.argv[2]}.wav", np.concatenate(parcalar), 24000)
