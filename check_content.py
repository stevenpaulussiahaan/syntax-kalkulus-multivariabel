#!/usr/bin/env python3
"""Pemeriksa isi: delimiter rumus seimbang, tak ada '<' liar, tautan gambar ada. Pakai: python3 check_content.py"""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent
bad = 0
for f in sorted((root / "content").glob("*.html")):
    s = f.read_text(encoding="utf-8")
    probs = []
    if s.count("\\(") != s.count("\\)"): probs.append("\\( \\) tidak seimbang")
    if s.count("\\[") != s.count("\\]"): probs.append("\\[ \\] tidak seimbang")
    for m in re.finditer(r"\\\(.*?\\\)|\\\[.*?\\\]", s, re.S):
        if "<" in m.group(0): probs.append("'<'/'>' di dalam rumus: " + m.group(0)[:50]); break
    for img in re.findall(r'src="(assets/img/[^"]+)"', s):
        if not (root / img).exists(): probs.append("gambar hilang: " + img)
    for t in ("periksa sendiri", "TODO"):
        if t in s: probs.append("teks sisa: " + t)
    print(("OK   " if not probs else "MASALAH ") + f.name, "; ".join(probs))
    bad += bool(probs)
print("berkas bermasalah:", bad)
