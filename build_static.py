#!/usr/bin/env python3
"""Membuat situs statis ke dist/ (Netlify, GitHub Pages, dll.). Hanya pustaka standar.

    python3 build_static.py          # buat halaman HTML
    python3 build_pdf.py             # (opsional) buat PDF unduhan ke dist/unduh/ (butuh playwright + chromium)

Rumus memakai KaTeX lokal (assets/katex), jadi situs dan PDF bekerja tanpa internet.
"""
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
SITE = "Kalkulus Multivariabel"
AUTHOR = "web by: Steven Paulus Siahaan"
CH = {int(k): v for k, v in json.loads((ROOT / "includes" / "chapters.json").read_text(encoding="utf-8")).items()}
e = html.escape

HEAD_MATH = """<link rel="stylesheet" href="assets/katex/katex.min.css">
<script defer src="assets/katex/katex.min.js"></script>
<script defer src="assets/katex/contrib/auto-render.min.js"></script>
<script defer src="assets/math.js"></script>"""


def has_content(slug):
    return bool(slug) and (ROOT / "content" / f"{slug}.html").exists()


def fix_links(s):
    import re
    # tautan ke subbab yang belum ada dijadikan teks biasa
    s = re.sub(r'<a href="(b\d+-\d+)\.html">(.*?)</a>',
               lambda m: m.group(0) if has_content(m.group(1)) else m.group(2), s, flags=re.S)
    return (s.replace("kalkulator.php", "kalkulator.html").replace("chapter.php?s=", "")
             .replace('href="b', 'href="b').replace('href="b11-1"', 'href="b11-1.html"'))


def sidebar(active):
    out = []
    for num, ch in CH.items():
        items = []
        for no, title, slug in ch["sections"]:
            if has_content(slug):
                items.append(f'<li><a href="{slug}.html">{e(no)} {e(title)}</a></li>')
            else:
                items.append(f'<li class="soon">{e(no)} {e(title)}</li>')
        op = " open" if num == active else ""
        out.append(f'<details{op}><summary>Bab {num} · {e(ch["title"])}</summary><ul>{"".join(items)}</ul></details>')
    return "\n".join(out)


def page(title, body, active=None, extra_js="", bare=False):
    return f"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · {SITE}</title>
<link rel="stylesheet" href="assets/style.css">
{HEAD_MATH}
</head>
<body>
<header class="top">
  <a class="brand" href="index.html">∫∂ {SITE}</a>
  <nav><a href="index.html">Daftar Bab</a><a href="unduh.html">Unduh</a><a href="kalkulator.html">Kalkulator</a><a href="tentang.html">Tentang</a></nav>
</header>
<div class="layout">
<aside class="side">
{sidebar(active)}
</aside>
<main>
<div class="printhead">{SITE} · {AUTHOR}</div>
<div class="credit">Web by: Steven Paulus Siahaan</div>
{body}
</main>
</div>
<footer class="foot"><span class="byline">{AUTHOR}</span><br>
Materi disusun dengan kata-kata sendiri mengikuti urutan topik buku <em>Multivariable Calculus, 7e</em> (J. Stewart). Gunakan bersama buku aslinya.</footer>
{extra_js}
<div class="badge-fixed">Web by: Steven Paulus Siahaan</div>
</body>
</html>
"""


def pdf_name(slug):
    return f"unduh/{slug}.pdf"


def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copytree(ROOT / "assets", DIST / "assets")
    pdf_dir = ROOT / "dist_pdf_cache"  # PDF hasil build_pdf.py disimpan di sini agar tidak hilang saat rebuild
    if pdf_dir.exists():
        shutil.copytree(pdf_dir, DIST / "unduh")

    flat = [(n, no, t, s) for n, ch in CH.items() for no, t, s in ch["sections"] if has_content(s)]
    have_pdf = lambda name: (DIST / name).exists()

    # Beranda
    cards = []
    for num, ch in CH.items():
        secs = [s for _, _, s in ch["sections"] if has_content(s)]
        total = len(ch["sections"])
        status = "Lengkap" if len(secs) == total else (f"{len(secs)}/{total} subbab" if secs else "Segera")
        btn = f'<a class="btn" href="{secs[0]}.html">Mulai belajar →</a>' if secs else ""
        cards.append(f'<article class="card{"" if secs else " disabled"}"><span class="badge">{status}</span>'
                     f'<h2>Bab {num}</h2><h3>{e(ch["title"])}</h3><p>{total} subbab</p>{btn}</article>')
    (DIST / "index.html").write_text(page(
        "Beranda",
        '<h1>Materi Kuliah Kalkulus Multivariabel</h1>'
        '<p class="lead">Catatan kuliah per bab dalam bahasa Indonesia, dengan turunan rumus, contoh soal berlangkah, '
        'dan grafik yang dibuat dengan Python. Seluruh materi dapat diunduh sebagai PDF.</p>'
        f'<p class="dl"><a href="unduh.html">⬇ Unduh bahan pembelajaran (PDF)</a></p>'
        f'<div class="grid">{"".join(cards)}</div>'), encoding="utf-8")

    # Halaman materi
    for i, (num, no, title, slug) in enumerate(flat):
        content = fix_links((ROOT / "content" / f"{slug}.html").read_text(encoding="utf-8"))
        prev = f'<a href="{flat[i-1][3]}.html">← {e(flat[i-1][1])} {e(flat[i-1][2])}</a>' if i > 0 else "<span></span>"
        nxt = f'<a href="{flat[i+1][3]}.html">{e(flat[i+1][1])} {e(flat[i+1][2])} →</a>' if i < len(flat) - 1 else ""
        dl = ""
        if have_pdf(pdf_name(slug)):
            dl = f'<p class="dl"><a href="{pdf_name(slug)}" download>⬇ PDF subbab ini</a>'
            if have_pdf(f"unduh/bab-{num}.pdf"):
                dl += f'<a href="unduh/bab-{num}.pdf" download>⬇ PDF Bab {num} lengkap</a>'
            dl += '<a href="unduh.html">Semua unduhan</a></p>'
        body = (f'<p class="crumb">Bab {num} · {e(CH[num]["title"])}</p><h1>{e(no)} {e(title)}</h1>{dl}'
                f'<article class="materi">{content}</article><nav class="pager">{prev}{nxt}</nav>')
        (DIST / f"{slug}.html").write_text(page(f"{no} {title}", body, active=num), encoding="utf-8")

    # Halaman unduhan
    rows = []
    if have_pdf("unduh/buku-lengkap.pdf"):
        rows.append('<p class="dl"><a href="unduh/buku-lengkap.pdf" download>⬇ Seluruh materi (satu PDF)</a></p>')
    for num, ch in CH.items():
        secs = [(no, t, s) for no, t, s in ch["sections"] if has_content(s)]
        if not secs:
            continue
        head = f'<h2>Bab {num} · {e(ch["title"])}</h2>'
        if have_pdf(f"unduh/bab-{num}.pdf"):
            head += f'<p class="dl"><a href="unduh/bab-{num}.pdf" download>⬇ PDF Bab {num} lengkap</a></p>'
        lis = "".join(
            f'<li>{e(no)} {e(t)} — <a href="{s}.html">baca</a>'
            + (f' · <a href="{pdf_name(s)}" download>PDF</a>' if have_pdf(pdf_name(s)) else "") + "</li>"
            for no, t, s in secs)
        rows.append(head + f"<ul>{lis}</ul>")
    note = "" if have_pdf("unduh/buku-lengkap.pdf") else "<p class='box note'>Berkas PDF belum dibuat. Jalankan <code>python3 build_pdf.py</code> lalu <code>python3 build_static.py</code> lagi.</p>"
    (DIST / "unduh.html").write_text(page("Unduh Bahan Pembelajaran",
        "<h1>Unduh Bahan Pembelajaran</h1><p>Semua berkas PDF memuat watermark dan rumus lengkap, dapat dibaca tanpa internet.</p>" + note + "".join(rows)), encoding="utf-8")

    # Kalkulator
    calc = """<h1>Kalkulator Numerik</h1>
<p>Dijalankan langsung di peramban Anda (JavaScript, tanpa server). Gunakan peubah <code>t</code> (atau <code>n</code> untuk barisan).
Fungsi: <code>sin cos tan sec csc cot exp ln sqrt abs sinh cosh tanh asin acos atan</code>; konstanta <code>pi</code>, <code>e</code>; pangkat <code>^</code>.
Batas boleh berupa ekspresi, mis. <code>2*pi</code>. Gunakan <code>*</code> untuk perkalian.</p>
<form class="calc" id="calc">
  <label>Jenis perhitungan <select id="mode"></select></label>
  <div id="fields" style="display:grid;gap:10px"></div>
  <button type="submit">Hitung</button>
</form>
<p id="err" class="note" style="color:#b42318"></p>
<h2>Hasil</h2><pre id="out"></pre>
<p><small>Versi Python yang setara ada di <code>python/tools.py</code>.</small></p>"""
    (DIST / "kalkulator.html").write_text(page("Kalkulator", calc, extra_js='<script src="assets/calc.js"></script>'), encoding="utf-8")

    about = f"""<h1>Tentang Situs Ini</h1>
<p>Catatan belajar Kalkulus Multivariabel yang mengikuti urutan topik buku <em>Multivariable Calculus, Seventh Edition</em> (James Stewart),
yaitu Bab 10 sampai Bab 17. Bab 1–9 buku itu (kalkulus satu peubah) tidak termasuk dalam buku ini.
Penjelasan ditulis dengan kata-kata sendiri; contoh dan soal di sini adalah contoh baru.</p>
<ul><li><strong>Python</strong>: gambar grafik dan kalkulator acuan.</li><li><strong>JavaScript + KaTeX</strong>: rumus dan kalkulator di peramban.</li></ul>
<p class="byline">{AUTHOR}</p>"""
    (DIST / "tentang.html").write_text(page("Tentang", about), encoding="utf-8")
    (DIST / "404.html").write_text(page("Tidak ditemukan", '<h1>Halaman tidak ditemukan</h1><p><a href="index.html">Kembali ke beranda</a></p>'), encoding="utf-8")

    # Halaman cetak gabungan (untuk build_pdf.py), tidak ditautkan dari situs
    pr = DIST / "_print"
    pr.mkdir()
    def bare(title, inner):
        return (f'<!doctype html><html lang="id"><head><meta charset="utf-8"><title>{e(title)}</title>'
                f'<link rel="stylesheet" href="../assets/style.css"><link rel="stylesheet" href="../assets/katex/katex.min.css">'
                f'<script defer src="../assets/katex/katex.min.js"></script><script defer src="../assets/katex/contrib/auto-render.min.js"></script>'
                f'<script defer src="../assets/math.js"></script></head><body><main style="padding:0 6px">'
                f'<div class="printhead">{SITE} · {AUTHOR}</div>{inner}</main></body></html>')
    def sec_html(num, no, title, slug):
        c = fix_links((ROOT / "content" / f"{slug}.html").read_text(encoding="utf-8")).replace('src="assets/', 'src="../assets/')
        return f'<section><p class="crumb">Bab {num} · {e(CH[num]["title"])}</p><h1>{e(no)} {e(title)}</h1><article class="materi">{c}</article></section>'
    for n, no, t, s in flat:
        (pr / f"{s}.html").write_text(bare(f"{no} {t}", sec_html(n, no, t, s)), encoding="utf-8")
    allparts = []
    for num in CH:
        parts = [sec_html(n, no, t, s) for n, no, t, s in flat if n == num]
        if parts:
            (pr / f"bab-{num}.html").write_text(bare(f"Bab {num}", f'<h1 style="font-size:2.2rem">Bab {num}: {e(CH[num]["title"])}</h1>' + '<div style="break-after:page"></div>'.join(parts)), encoding="utf-8")
            allparts.append(f'<h1 style="font-size:2.4rem">Bab {num}: {e(CH[num]["title"])}</h1>' + '<div style="break-after:page"></div>'.join(parts))
    if allparts:
        (pr / "buku-lengkap.html").write_text(bare("Kalkulus Multivariabel", '<div style="break-after:page"></div>'.join(allparts)), encoding="utf-8")
    print(f"Selesai: {len(list(DIST.glob('*.html')))} halaman di {DIST} ({len(flat)} subbab berisi dari {sum(len(c['sections']) for c in CH.values())})")


if __name__ == "__main__":
    build()
