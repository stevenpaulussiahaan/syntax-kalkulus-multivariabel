#!/usr/bin/env python3
"""Gambar untuk subbab 11.7-11.11. Jalankan: python3 -I python/figs_b11b.py"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
from math import factorial

OUT = "/tmp/kalkulus/assets/img"
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"figure.dpi": 130, "font.size": 10, "axes.grid": True,
                     "grid.alpha": .25, "axes.spines.top": False, "axes.spines.right": False})
C1, C2, C3, C4 = "#1d4ed8", "#c2410c", "#15803d", "#7c3aed"


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), facecolor="white")
    plt.close(fig)


# ---- 11.7 diagram keputusan
fig, ax = plt.subplots(figsize=(9, 6.2))
ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 8)
def box(x, y, w, h, text, fc="#eff6ff", ec=C1):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", fc=fc, ec=ec, lw=1.4))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=8.6)
def arr(x1, y1, x2, y2, t=None):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->", color="#444", lw=1.3))
    if t: ax.text((x1+x2)/2 + .08, (y1+y2)/2 + .08, t, fontsize=8, color=C2)
box(3.2, 7.1, 3.6, .75, "Deret ∑ a_n: apakah a_n → 0 ?")
box(0.1, 5.7, 2.9, .9, "Tidak: DIVERGEN\n(uji suku ke-n)", "#fee2e2", "#b91c1c")
arr(3.2, 7.45, 1.55, 6.62, "tidak")
box(3.4, 5.7, 3.2, .9, "Ya: kenali bentuknya\n(geometri, p, teleskop, ∑ deret pangkat)")
arr(5, 7.1, 5, 6.62, "ya")
box(0.1, 4.1, 3.0, 1.0, "Ada (-1)^n atau\ntanda bergantian?\n→ Uji Deret Berganti,\ncek |a_n| lebih dulu", "#fef9c3", "#a16207")
box(3.5, 4.1, 3.0, 1.0, "Ada n!, c^n, n^n ?\n→ Uji Rasio\n(atau Uji Akar bila\nberbentuk (...)^n)", "#dcfce7", C3)
box(6.9, 4.1, 3.0, 1.0, "Rasional / akar dari n ?\n→ Uji Banding Limit\ndengan deret-p", "#ede9fe", C4)
arr(5, 5.7, 1.6, 5.12); arr(5, 5.7, 5, 5.12); arr(5, 5.7, 8.4, 5.12)
box(0.1, 2.3, 3.0, 1.1, "Fungsi f(n) mudah diintegralkan\n(ln n, e^n, 1/(n ln n))\n→ Uji Integral", "#e0f2fe", C1)
box(3.5, 2.3, 3.0, 1.1, "Mirip deret yang dikenal\ntetapi tak pas untuk limit?\n→ Uji Banding biasa", "#e0f2fe", C1)
box(6.9, 2.3, 3.0, 1.1, "Ada sin, cos tak teratur?\n→ Uji Konvergensi Mutlak\nlalu banding dengan |a_n|", "#e0f2fe", C1)
arr(5, 4.1, 1.6, 3.42); arr(5, 4.1, 5, 3.42); arr(5, 4.1, 8.4, 3.42)
box(1.0, 0.5, 8.0, 1.0, "Tidak jalan? Cobalah: tulis ulang suku (pecahan parsial, rasionalisasi),\nbandingkan ukuran suku besar-besaran (dominasi), atau hitung jumlah parsial secara langsung.", "#f3f4f6", "#6b7280")
arr(5, 2.3, 5, 1.52)
save(fig, "b11-7-diagram.png")

# ---- 11.8 selang kekonvergenan
fig, ax = plt.subplots(figsize=(9, 3.6))
items = [("∑ (x-3)^n / n", 2, 4, "[", ")", 3),
         ("∑ (3x-2)^n /(n 5^n)", -1, 7/3, "[", ")", 2/3),
         ("∑ x^n / n^2", -1, 1, "[", "]", 0),
         ("∑ (2n)!/(n!)^2 x^n", -.25, .25, "[", ")", 0)]
for i, (lab, a, b, l, r, c) in enumerate(items):
    y = len(items) - i
    ax.plot([a, b], [y, y], color=C1, lw=3)
    ax.plot(a, y, "o", mfc=C1 if l == "[" else "white", mec=C1, ms=8, zorder=3)
    ax.plot(b, y, "o", mfc=C1 if r == "]" else "white", mec=C1, ms=8, zorder=3)
    ax.plot(c, y, "|", color=C2, ms=14)
    ax.text(-1.55, y + .22, lab, fontsize=9)
ax.set_ylim(.4, 4.9); ax.set_xlim(-1.6, 4.4); ax.set_yticks([])
ax.set_xlabel("x   (titik penuh = ujung ikut; titik kosong = ujung tidak ikut; garis oranye = pusat)")
save(fig, "b11-8-selang.png")

# ---- 11.9 jumlah parsial deret geometri
x = np.linspace(-1.6, .95, 600)
fig, ax = plt.subplots(figsize=(7.5, 4.6))
ax.plot(x, 1/(1-x), "k", lw=2.2, label="1/(1-x)")
for n, c in zip([2, 4, 8, 14], [C1, C2, C3, C4]):
    ax.plot(x, sum(x**k for k in range(n+1)), color=c, lw=1.3, label="jumlah parsial n=%d" % n)
ax.set_ylim(-4, 12); ax.axvline(-1, color="gray", ls=":"); ax.axvline(1, color="gray", ls=":")
ax.legend(fontsize=8); ax.set_xlabel("x")
save(fig, "b11-9-parsial.png")

# ---- 11.10 Taylor sin dan exp
x = np.linspace(-7, 7, 800)
fig, ax = plt.subplots(figsize=(8, 4.6))
ax.plot(x, np.sin(x), "k", lw=2.3, label="sin x")
for n, c in zip([1, 3, 5, 7, 9], [C1, C2, C3, C4, "#0891b2"]):
    y = sum((-1)**k * x**(2*k+1)/factorial(2*k+1) for k in range((n-1)//2 + 1))
    ax.plot(x, y, color=c, lw=1.3, label="T%d" % n)
ax.set_ylim(-3, 3); ax.legend(ncol=3, fontsize=8, loc="upper center"); ax.set_xlabel("x")
save(fig, "b11-10-taylor-sin.png")
x = np.linspace(-3, 3, 600)
fig, ax = plt.subplots(figsize=(7.5, 4.4))
ax.plot(x, np.exp(x), "k", lw=2.3, label="e^x")
for n, c in zip([1, 2, 3, 4], [C1, C2, C3, C4]):
    ax.plot(x, sum(x**k/factorial(k) for k in range(n+1)), color=c, lw=1.3, label="T%d" % n)
ax.set_ylim(-3, 15); ax.legend(fontsize=8); ax.set_xlabel("x")
save(fig, "b11-10-taylor-exp.png")

# ---- 11.11 ln(1+x) dan galat cos
x = np.linspace(-.95, 2.3, 800)
fig, ax = plt.subplots(figsize=(7.5, 4.6))
ax.plot(x, np.log(1+x), "k", lw=2.3, label="ln(1+x)")
for n, c in zip([1, 2, 3, 6, 9], [C1, C2, C3, C4, "#0891b2"]):
    ax.plot(x, sum((-1)**(k+1)*x**k/k for k in range(1, n+1)), color=c, lw=1.2, label="T%d" % n)
ax.axvline(1, color="gray", ls=":"); ax.set_ylim(-2.5, 2.5); ax.legend(fontsize=8, ncol=3); ax.set_xlabel("x")
save(fig, "b11-11-ln.png")
x = np.linspace(0, 2, 400)
T4 = 1 - x**2/2 + x**4/24
fig, ax = plt.subplots(figsize=(7.5, 4.2))
ax.semilogy(x[1:], np.abs(np.cos(x[1:]) - T4[1:]), color=C1, lw=2, label="galat sebenarnya |cos x - T4(x)|")
ax.semilogy(x[1:], x[1:]**6/720, color=C2, lw=1.8, ls="--", label="batas Taylor x^6/720")
ax.legend(fontsize=8); ax.set_xlabel("x")
save(fig, "b11-11-galat.png")
