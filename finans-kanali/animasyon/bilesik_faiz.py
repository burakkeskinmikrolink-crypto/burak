"""Kodla animasyon ornegi: bilesik faiz. Cikti: bilesik_faiz.mp4 (ffmpeg gerekir).

Kullanim: python bilesik_faiz.py
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FFMpegWriter, FuncAnimation

ANAPARA, ORAN, YIL = 1000, 0.07, 40
yillar = np.arange(YIL + 1)
bilesik = ANAPARA * (1 + ORAN) ** yillar
basit = ANAPARA * (1 + ORAN * yillar)

fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=100)
fig.patch.set_facecolor("#0e1117")
ax.set_facecolor("#0e1117")
for s in ax.spines.values():
    s.set_color("#444")
ax.tick_params(colors="#ccc")
ax.set_xlim(0, YIL)
ax.set_ylim(0, bilesik[-1] * 1.08)
ax.set_xlabel("Years", color="#ccc")
ax.set_ylabel("Balance ($)", color="#ccc")
(c_line,) = ax.plot([], [], color="#4ade80", lw=4, label="Compound 7%")
(s_line,) = ax.plot([], [], color="#f87171", lw=4, label="Simple 7%")
ax.legend(facecolor="#0e1117", labelcolor="#eee", loc="upper left")
baslik = ax.set_title("", color="white", fontsize=20)


def kare(i):
    c_line.set_data(yillar[: i + 1], bilesik[: i + 1])
    s_line.set_data(yillar[: i + 1], basit[: i + 1])
    baslik.set_text(f"Year {i}: ${bilesik[i]:,.0f} vs ${basit[i]:,.0f}")
    return c_line, s_line, baslik


anim = FuncAnimation(fig, kare, frames=YIL + 1, blit=False)
anim.save("bilesik_faiz.mp4", writer=FFMpegWriter(fps=6))
print("bitti")
