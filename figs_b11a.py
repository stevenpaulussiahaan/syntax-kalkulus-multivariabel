#!/usr/bin/env python3
"""Gambar subbab 11.2-11.6. Jalankan: python3 -I python/figs_b11a.py"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = "/tmp/kalkulus/assets/img"
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"figure.dpi": 130, "font.size": 10, "axes.grid": True,
                     "grid.alpha": .25, "axes.spines.top": False, "axes.spines.right": False})
C1, C2, C3 = "#1d4ed8", "#c2410c", "#15803d"


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), facecolor="white")
    plt.close(fig)


# 11.2 jumlah parsial
fig, ax = plt.subplots(1, 2, figsize=(9, 3.4), facecolor="white")
n = np.arange(1, 16)
ax[0].plot(n, 2 - 2.0 ** (1 - n), "o", color=C1)
ax[0].axhline(2, color=C2, ls="--")
ax[0].set_title("Geometri 1 + 1/2 + 1/4 + ...: $s_n \\to 2$")
ax[0].set_xlabel("n"); ax[0].set_ylabel("$s_n$")
n2 = np.arange(1, 201)
ax[1].plot(n2, np.cumsum(1 / n2), color=C1, label="$s_n$ (harmonik)")
ax[1].plot(n2, np.log(n2 + 1), color=C2, ls="--", label="$\\ln(n+1)$")
ax[1].set_title("Harmonik: $s_n$ tumbuh tanpa batas")
ax[1].set_xlabel("n"); ax[1].legend()
save(fig, "b11-2-sumparsial.png")

# 11.2 teleskop
fig, ax = plt.subplots(figsize=(5.2, 3.4), facecolor="white")
n = np.arange(1, 21)
ax.bar(n, 1 / (n * (n + 1)), color=C2, alpha=.7, label="suku $a_n=1/(n(n+1))$")
ax.plot(n, 1 - 1 / (n + 1), "o-", color=C1, label="$s_n=1-1/(n+1)$")
ax.axhline(1, color="k", ls="--", lw=1)
ax.set_xlabel("n"); ax.legend(loc="center right")
ax.set_title("Deret teleskop: $s_n \\to 1$")
save(fig, "b11-2-teleskop.png")

# 11.3 uji integral
fig, ax = plt.subplots(1, 2, figsize=(9, 3.4), facecolor="white")
x = np.linspace(1, 7.2, 300)
f = lambda t: 1 / t ** 2
for k, (title, rects) in enumerate([("Persegi panjang di atas kurva: $s_n\\geq\\int_1^{n+1}f$", "left"),
                                    ("Persegi panjang di bawah kurva: $s_n-a_1\\leq\\int_1^{n}f$", "right")]):
    ax[k].plot(x, f(x), color=C1, lw=2)
    for i in range(1, 7):
        if rects == "left":
            ax[k].bar(i, f(i), width=1, align="edge", color=C2, alpha=.35, edgecolor=C2)
        else:
            ax[k].bar(i, f(i + 1), width=1, align="edge", color=C3, alpha=.35, edgecolor=C3)
    ax[k].set_title(title, fontsize=9); ax[k].set_xlabel("x")
    ax[k].set_xlim(.8, 7.2)
save(fig, "b11-3-integral.png")

# 11.3 taksiran sisa
fig, ax = plt.subplots(figsize=(5.6, 3.5), facecolor="white")
n = np.arange(1, 16)
s = np.cumsum(1 / np.arange(1, 4001) ** 3)
true = 1.2020569031595942
ax.plot(n, s[:15], "o", color=C1, label="$s_n$")
ax.plot(n, s[:15] + 1 / (2 * (n + 1) ** 2), "-", color=C3, label="batas bawah $s_n+\\int_{n+1}^\\infty$")
ax.plot(n, s[:15] + 1 / (2 * n ** 2), "-", color=C2, label="batas atas $s_n+\\int_n^\\infty$")
ax.axhline(true, color="k", ls="--", lw=1)
ax.set_ylim(1.0, 1.4); ax.set_xlabel("n"); ax.legend(fontsize=8)
ax.set_title("Menjepit jumlah $\\sum 1/n^3$")
save(fig, "b11-3-taksiran.png")

# 11.4 perbandingan
fig, ax = plt.subplots(figsize=(6, 3.5), facecolor="white")
n = np.arange(1, 13)
ax.bar(n - .2, 1 / n ** 2, width=.4, color=C2, alpha=.7, label="$b_n=1/n^2$ (konvergen)")
ax.bar(n + .2, 1 / (n ** 2 + n), width=.4, color=C1, alpha=.8, label="$a_n=1/(n^2+n)$")
ax.set_xlabel("n"); ax.legend()
ax.set_title("$0\\leq a_n\\leq b_n$: yang kecil ikut konvergen")
save(fig, "b11-4-banding.png")

# 11.5 zigzag
fig, ax = plt.subplots(figsize=(6.4, 3.5), facecolor="white")
n = np.arange(1, 25)
s = np.cumsum((-1.0) ** (n - 1) / n)
ax.plot(n, s, "o-", color=C1, ms=4, label="$s_n$ (harmonik berganti tanda)")
ax.axhline(np.log(2), color=C2, ls="--", label="$\\ln 2$")
ax.set_xlabel("n"); ax.legend()
ax.set_title("Jumlah parsial berayun mengapit jumlah deret")
save(fig, "b11-5-zigzag.png")

# 11.6 rasio
fig, ax = plt.subplots(figsize=(6.4, 3.5), facecolor="white")
n = np.arange(1, 31)
ax.plot(n, (n + 1) ** 2 / (2 * n ** 2), "o-", color=C1, ms=4, label="$\\sum n^2/2^n$: rasio $\\to1/2$")
ax.plot(n, 2.0 ** 0 * (n / (n + 1.0)) ** n, "s-", color=C3, ms=4, label="$\\sum n!/n^n$: rasio $\\to1/e$")
ax.plot(n, 1 / (1 + 1.0 / n), "^-", color=C2, ms=4, label="$\\sum 1/n$: rasio $\\to1$ (tak tentu)")
ax.axhline(1, color="k", ls="--", lw=1)
ax.set_xlabel("n"); ax.set_ylabel("$|a_{n+1}/a_n|$"); ax.legend(fontsize=8)
ax.set_title("Perilaku rasio suku berurutan")
save(fig, "b11-6-rasio.png")
