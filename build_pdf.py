#!/usr/bin/env python3
"""Membuat PDF unduhan dari dist/_print ke dist_pdf_cache/ (lalu jalankan build_static.py lagi).

Butuh:  pip install playwright && playwright install chromium
Urutan: python3 build_static.py && python3 build_pdf.py && python3 build_static.py
"""
import shutil
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
PR = ROOT / "dist" / "_print"
OUT = ROOT / "dist_pdf_cache"
FOOT = ('<div style="width:100%;font-size:8px;color:#666;text-align:center;font-family:Arial">'
        'web by: Steven Paulus Siahaan &nbsp;·&nbsp; Halaman <span class="pageNumber"></span> / <span class="totalPages"></span></div>')


def main():
    if not PR.exists():
        sys.exit("Jalankan python3 build_static.py dulu.")
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    files = sorted(PR.glob("*.html"))
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page()
        for f in files:
            pg.goto(f.as_uri(), wait_until="load")
            pg.wait_for_selector("html[data-math-ready='1']", timeout=120000)
            pg.pdf(path=str(OUT / (f.stem + ".pdf")), format="A4", print_background=True,
                   margin={"top": "16mm", "bottom": "16mm", "left": "15mm", "right": "15mm"},
                   display_header_footer=True, header_template="<span></span>", footer_template=FOOT)
            print("PDF:", f.stem)
        br.close()


if __name__ == "__main__":
    main()
