#!/usr/bin/env python3
"""Membuat semua gambar materi ke assets/img/. Jalankan: python3 python/generate_figures.py"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "img")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"figure.dpi": 130, "font.size": 10, "axes.grid": True,
                     "grid.alpha": .25, "axes.spines.top": False, "axes.spines.right": False})
C1, C2, C3 = "#1d4ed8", "#c2410c", "#15803d"


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), facecolor="white")
    plt.close(fig)


def arrow_along(ax, x, y, idx, color):
    ax.annotate("", xy=(x[idx + 1], y[idx + 1]), xytext=(x[idx], y[idx]),
                arrowprops=dict(arrowstyle="->", color=color, lw=1.6))


# 10.1 parabola parametrik
t = np.linspace(-3, 5, 400)
x, y = t**2 - 2*t, t + 1
fig, ax = plt.subplots(figsize=(5, 4))
ax.plot(x, y, color=C1)
tt = np.arange(-2, 5)
ax.scatter(tt**2 - 2*tt, tt + 1, color=C2, zorder=3)
for k in tt:
    ax.annotate(f"t={k}", (k**2 - 2*k, k + 1), textcoords="offset points", xytext=(6, 4), fontsize=8)
arrow_along(ax, x, y, 300, C1)
ax.set(xlabel="x", ylabel="y", title=r"$x=t^2-2t,\ y=t+1$")
save(fig, "b10-1-parabola.png")

# lingkaran dua parametrisasi
th = np.linspace(0, 2*np.pi, 400)
fig, axs = plt.subplots(1, 2, figsize=(8, 3.8))
axs[0].plot(np.cos(th), np.sin(th), color=C1)
arrow_along(axs[0], np.cos(th), np.sin(th), 40, C1)
axs[0].set_title(r"$x=\cos t,\ y=\sin t$ (1x, berlawanan jarum jam)")
axs[1].plot(np.sin(2*th), np.cos(2*th), color=C2)
arrow_along(axs[1], np.sin(2*th), np.cos(2*th), 20, C2)
axs[1].set_title(r"$x=\sin 2t,\ y=\cos 2t$ (2x, searah jarum jam)")
for a in axs:
    a.set_aspect("equal"); a.title.set_fontsize(9)
save(fig, "b10-1-lingkaran.png")

# sikloid
r = 1
t = np.linspace(0, 4*np.pi, 800)
fig, ax = plt.subplots(figsize=(8, 2.8))
ax.plot(r*(t - np.sin(t)), r*(1 - np.cos(t)), color=C1, label="sikloid")
t0 = 2.2
cx, cy = r*t0, r
ax.plot(cx + r*np.cos(th), cy + r*np.sin(th), color="gray", lw=1)
px, py = r*(t0 - np.sin(t0)), r*(1 - np.cos(t0))
ax.plot([cx, px], [cy, py], color=C2); ax.scatter([px], [py], color=C2, zorder=3)
ax.set_aspect("equal"); ax.set(title="Sikloid: lintasan titik pada lingkaran yang menggelinding")
save(fig, "b10-1-sikloid.png")

# kurva Lissajous
t = np.linspace(0, 2*np.pi, 800)
fig, ax = plt.subplots(figsize=(4.2, 4))
ax.plot(np.cos(t), np.sin(2*t), color=C3); ax.set_title(r"Lissajous $x=\cos t,\ y=\sin 2t$")
save(fig, "b10-1-lissajous.png")

# keluarga konkoid
fig, axs = plt.subplots(2, 4, figsize=(10, 5))
tt = np.linspace(-np.pi/2 + .02, np.pi/2 - .02, 400)
tt2 = np.linspace(np.pi/2 + .02, 3*np.pi/2 - .02, 400)
for ax, a in zip(axs.flat, [-2, -1, -.5, -.2, 0, .5, 1, 2]):
    for seg in (tt, tt2):
        ax.plot(a + np.cos(seg), a*np.tan(seg) + np.sin(seg), color=C1, lw=1)
    ax.set(xlim=(-4, 4), ylim=(-4, 4), title=f"a = {a}"); ax.set_aspect("equal")
fig.suptitle(r"Keluarga $x=a+\cos t,\ y=a\tan t+\sin t$")
save(fig, "b10-1-konkoid.png")

# 10.2 contoh kurva dengan simpul
t = np.linspace(-2.2, 2.2, 500)
x, y = t**2, t**3 - 3*t
fig, ax = plt.subplots(figsize=(4.8, 4.4))
ax.plot(x, y, color=C1)
pts = {"(3,0) t=±√3": (3, 0), "(1,2) t=-1": (1, 2), "(1,-2) t=1": (1, -2), "(0,0) t=0": (0, 0)}
for lbl, (px, py) in pts.items():
    ax.scatter([px], [py], color=C2, zorder=3); ax.annotate(lbl, (px, py), textcoords="offset points", xytext=(6, 5), fontsize=8)
xs = np.linspace(2, 4.5, 10)
ax.plot(xs, np.sqrt(3)*(xs - 3), "--", color=C3, lw=1); ax.plot(xs, -np.sqrt(3)*(xs - 3), "--", color=C3, lw=1)
ax.set(xlim=(-.5, 5), ylim=(-4, 4), title=r"$x=t^2,\ y=t^3-3t$")
save(fig, "b10-2-simpul.png")

# luas satu busur sikloid
t = np.linspace(0, 2*np.pi, 400)
fig, ax = plt.subplots(figsize=(6, 2.8))
ax.fill_between(t - np.sin(t), 1 - np.cos(t), color=C1, alpha=.25); ax.plot(t - np.sin(t), 1 - np.cos(t), color=C1)
ax.set(title=r"Luas satu busur sikloid $=3\pi r^2$ (r=1)"); ax.set_aspect("equal")
save(fig, "b10-2-luas-sikloid.png")

# 10.3 sistem koordinat kutub (titik & representasi)
fig = plt.figure(figsize=(8, 3.8))
ax = fig.add_subplot(121, projection="polar")
for (rr, tt, c, lab) in [(1, 5*np.pi/4, C1, "(1, 5π/4)"), (2, 3*np.pi, C2, "(2, 3π)"), (2, -2*np.pi/3, C3, "(2, −2π/3)"), (-3, 3*np.pi/4, "k", "(−3, 3π/4)")]:
    ax.plot([tt, tt], [0, rr], color=c, lw=1) if rr > 0 else ax.plot([tt + np.pi]*2, [0, -rr], color=c, lw=1)
    ax.scatter([tt if rr > 0 else tt + np.pi], [abs(rr)], color=c, zorder=3, label=lab)
ax.set_rlim(0, 3.2); ax.legend(loc="upper left", bbox_to_anchor=(1.05, 1), fontsize=7); ax.set_title("Titik pada koordinat kutub", fontsize=9)
ax2 = fig.add_subplot(122, projection="polar")
th = np.linspace(-np.pi/2, np.pi/2, 300)
ax2.plot(th, 2*np.cos(th), color=C1); ax2.set_rlim(0, 2.2); ax2.set_title(r"$r=2\cos\theta$ (lingkaran)", fontsize=9)
save(fig, "b10-3-titik.png")

# kardioid + pembentukan
th = np.linspace(0, 2*np.pi, 600)
fig = plt.figure(figsize=(9, 3.6))
ax = fig.add_subplot(121); ax.plot(th, 1 + np.sin(th), color=C1); ax.set(xlabel="θ", ylabel="r", title=r"$r=1+\sin\theta$ pada koordinat Cartesius")
ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]); ax.set_xticklabels(["0", "π/2", "π", "3π/2", "2π"])
ax2 = fig.add_subplot(122, projection="polar"); ax2.plot(th, 1 + np.sin(th), color=C1); ax2.set_title("Kardioid", fontsize=9)
save(fig, "b10-3-kardioid.png")

# mawar 4 daun & r=sin(8θ/5)
fig = plt.figure(figsize=(9, 4))
ax = fig.add_subplot(121, projection="polar"); th = np.linspace(0, 2*np.pi, 800); ax.plot(th, np.cos(2*th), color=C1); ax.set_title(r"$r=\cos 2\theta$", fontsize=9)
ax = fig.add_subplot(122, projection="polar"); th = np.linspace(0, 10*np.pi, 4000); ax.plot(th, np.sin(8*th/5), color=C2, lw=.8); ax.set_title(r"$r=\sin(8\theta/5)$, $0\leq\theta\leq 10\pi$", fontsize=9)
save(fig, "b10-3-mawar.png")

# limacon
fig, axs = plt.subplots(2, 5, figsize=(11, 4.6), subplot_kw={"projection": "polar"})
th = np.linspace(0, 2*np.pi, 600)
for ax, c in zip(axs.flat, [2.5, 1.7, 1, .7, .5, .2, 0, -.2, -.5, -1]):
    ax.plot(th, 1 + c*np.sin(th), color=C1, lw=1); ax.set_title(f"c={c}", fontsize=8); ax.set_xticklabels([]); ax.set_yticklabels([])
fig.suptitle(r"Keluarga limaçon $r=1+c\sin\theta$")
save(fig, "b10-3-limacon.png")

# 10.4 luas kutub
fig = plt.figure(figsize=(9, 4))
ax = fig.add_subplot(121, projection="polar")
th = np.linspace(-np.pi/4, np.pi/4, 200); ax.fill_between(th, 0, np.cos(2*th), color=C1, alpha=.35); ax.plot(th, np.cos(2*th), color=C1)
ax.set_title(r"Satu kelopak $r=\cos 2\theta$", fontsize=9)
ax = fig.add_subplot(122, projection="polar")
th = np.linspace(0, 2*np.pi, 800); ax.plot(th, 3*np.sin(th), color=C1); ax.plot(th, 1 + np.sin(th), color=C2)
m = (th >= np.pi/6) & (th <= 5*np.pi/6)
ax.fill_between(th[m], 1 + np.sin(th[m]), 3*np.sin(th[m]), color=C3, alpha=.4)
ax.set_title(r"Di dalam $r=3\sin\theta$, di luar $r=1+\sin\theta$", fontsize=9)
save(fig, "b10-4-luas.png")

# 10.5 irisan kerucut
fig, axs = plt.subplots(1, 3, figsize=(11, 3.8))
p = 1; x = np.linspace(-4, 4, 200); axs[0].plot(x, x**2/(4*p), color=C1); axs[0].axhline(-p, color=C2, ls="--"); axs[0].scatter([0], [p], color=C3, zorder=3)
axs[0].set(title=r"Parabola $x^2=4py$ (p=1)", ylim=(-2, 5), xlim=(-4, 4)); axs[0].text(.2, p + .15, "F")
th = np.linspace(0, 2*np.pi, 400); a, b = 4, 3; c = np.sqrt(a*a - b*b)
axs[1].plot(a*np.cos(th), b*np.sin(th), color=C1); axs[1].scatter([-c, c], [0, 0], color=C3, zorder=3); axs[1].set_aspect("equal"); axs[1].set_title(r"Elips $x^2/16+y^2/9=1$")
a, b = 4, 3; u = np.linspace(-1.8, 1.8, 300)
axs[2].plot(a*np.cosh(u), b*np.sinh(u), color=C1); axs[2].plot(-a*np.cosh(u), b*np.sinh(u), color=C1)
xx = np.linspace(-9, 9, 10); axs[2].plot(xx, 3/4*xx, "--", color=C2, lw=1); axs[2].plot(xx, -3/4*xx, "--", color=C2, lw=1)
axs[2].scatter([-5, 5], [0, 0], color=C3, zorder=3); axs[2].set(xlim=(-9, 9), ylim=(-6, 6), title=r"Hiperbola $x^2/16-y^2/9=1$"); axs[2].set_aspect("equal")
save(fig, "b10-5-konik.png")

# 10.6 eksentrisitas
fig, axs = plt.subplots(2, 5, figsize=(11, 4.6), subplot_kw={"projection": "polar"})
th = np.linspace(0, 2*np.pi, 800)
for ax, e in zip(axs.flat, [.1, .5, .68, .86, .96, 1, 1.1, 1.4, 2, 4]):
    d = 1; r = e*d/(1 + e*np.cos(th)); r = np.where((r < 0) | (r > 15), np.nan, r)
    ax.plot(th, r, color=C1, lw=1); ax.set_title(f"e={e}", fontsize=8); ax.set_xticklabels([]); ax.set_yticklabels([])
    if e > 1: ax.set_rlim(0, 6)
fig.suptitle(r"Pengaruh eksentrisitas pada $r=\dfrac{ed}{1+e\cos\theta}$ (fokus di pusat)")
save(fig, "b10-6-eksentrisitas.png")

fig = plt.figure(figsize=(9, 4))
th = np.linspace(0, 2*np.pi, 600)
ax = fig.add_subplot(121, projection="polar"); ax.plot(th, 10/(3 - 2*np.cos(th)), color=C1); ax.set_title(r"$r=10/(3-2\cos\theta)$", fontsize=9)
ax = fig.add_subplot(122, projection="polar")
r = 12/(2 + 4*np.sin(th)); r = np.where((r < 0) | (r > 30), np.nan, r); ax.plot(th, r, color=C2); ax.set_rlim(0, 12); ax.set_title(r"$r=12/(2+4\sin\theta)$ (hiperbola)", fontsize=9)
save(fig, "b10-6-contoh.png")

# 11.1 barisan
n = np.arange(1, 21)
fig, axs = plt.subplots(1, 3, figsize=(11, 3.4))
axs[0].scatter(n, n/(n + 1), color=C1, s=18); axs[0].axhline(1, color=C2, ls="--"); axs[0].set_title(r"$a_n=n/(n+1)\to1$")
axs[1].scatter(n, (-1.0)**n, color=C1, s=18); axs[1].set_title(r"$a_n=(-1)^n$ divergen")
import math
axs[2].scatter(n, [math.factorial(int(k))/int(k)**int(k) for k in n], color=C1, s=18); axs[2].set_title(r"$a_n=n!/n^n\to0$")
for a in axs: a.set_xlabel("n")
save(fig, "b11-1-barisan.png")

# r^n
n = np.arange(0, 16)
fig, ax = plt.subplots(figsize=(7, 3.6))
for r_, c in [(1.1, C2), (.8, C1), (-.8, C3), (-1.1, "k")]:
    ax.plot(n, r_**n, "o-", ms=3, lw=.8, label=f"r={r_}", color=c)
ax.set_ylim(-5, 5); ax.legend(ncol=4, fontsize=8); ax.set_title(r"Barisan $r^n$ untuk beberapa nilai r")
save(fig, "b11-1-geometri.png")

print("Selesai:", sorted(os.listdir(OUT)))
