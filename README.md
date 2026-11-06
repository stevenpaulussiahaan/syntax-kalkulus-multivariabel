# Kalkulus Multivariabel (Stewart, Bab 10-17)

Materi kuliah berbahasa Indonesia, 58 subbab, dengan rumus KaTeX, gambar matplotlib,
kalkulator JavaScript, dan unduhan PDF per subbab / per bab / buku lengkap.
Web by: Steven Paulus Siahaan.

## Isi repositori
| Berkas / folder | Fungsi |
|---|---|
| `content/*.html` | Isi materi, satu berkas per subbab (mis. `b12-3.html`) |
| `includes/chapters.json` | Daftar bab dan subbab (sumber tunggal) |
| `build_static.py` | Python: membuat situs statis ke `dist/` |
| `build_pdf.py` | Python + Playwright: membuat semua PDF |
| `check_content.py` | Python: memeriksa rumus dan gambar di `content/` |
| `python/*.py` | Python: pembuat gambar (matplotlib) dan alat bantu |
| `*.php`, `includes/*.php` | Versi PHP situs (hosting PHP / Docker) |
| `Dockerfile` | Menjalankan versi PHP + Python di Docker |
| `assets/` | CSS, JS kalkulator, KaTeX lokal, gambar, logo |
| `netlify.toml` | Netlify: `publish = "dist"` |

## Menambah ke GitHub
    git init
    git add .
    git commit -m "Kalkulus Multivariabel"
    git branch -M main
    git remote add origin https://github.com/USERNAME/NAMA-REPO.git
    git push -u origin main
(atau di github.com: New repository, lalu Upload files dan seret seluruh isi folder ini.)

## Membangun situs statis
    python3 build_static.py                  # HTML ke dist/
    pip install playwright && playwright install chromium
    python3 build_pdf.py                     # PDF ke dist_pdf_cache/
    python3 build_static.py                  # sisipkan PDF ke dist/unduh/
    rm -rf dist/_print
Upload isi folder `dist/` ke Netlify / Vercel (publish directory: `dist`).
Bila deploy otomatis dari GitHub, commit juga folder `dist/` hasil build.

## Versi PHP
    php -S localhost:8000
Kalkulator versi PHP memakai Python (`shell_exec`); di hosting tanpa Python, pakai versi statis
(kalkulator JavaScript di `assets/calc.js`).

## Mengedit materi
1. Ubah `content/bXX-Y.html` (HTML dengan rumus `\( ... \)` dan `\[ ... \]`; di dalam rumus
   pakai `\lt` dan `\gt`, bukan `<` dan `>`).
2. `python3 check_content.py` untuk memeriksa.
3. Bangun ulang seperti langkah di atas.
