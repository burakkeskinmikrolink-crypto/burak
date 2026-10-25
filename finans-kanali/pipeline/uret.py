"""Senaryo metninden ses (mp3) ve altyazı (srt) uretir. Ucretsiz: edge-tts.

Kurulum: pip install edge-tts
Kullanim: python uret.py senaryo.txt cikti_adi [ses]
"""
import asyncio
import sys

import edge_tts


async def main(senaryo, cikti, ses):
    metin = open(senaryo, encoding="utf-8").read()
    iletisim = edge_tts.Communicate(metin, ses)
    alt = edge_tts.SubMaker()
    with open(f"{cikti}.mp3", "wb") as f:
        async for parca in iletisim.stream():
            if parca["type"] == "audio":
                f.write(parca["data"])
            elif parca["type"] in ("WordBoundary", "SentenceBoundary"):
                alt.feed(parca)
    with open(f"{cikti}.srt", "w", encoding="utf-8") as f:
        f.write(alt.get_srt())


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    ses = sys.argv[3] if len(sys.argv) > 3 else "en-US-AndrewNeural"
    asyncio.run(main(sys.argv[1], sys.argv[2], ses))
