<?php
require __DIR__ . '/includes/lib.php';
$pageTitle = 'Tentang';
require __DIR__ . '/includes/header.php';
?>
<h1>Tentang Situs Ini</h1>
<p>Situs ini adalah catatan belajar untuk mata kuliah Kalkulus Multivariabel yang mengikuti urutan topik buku
<em>Multivariable Calculus, Seventh Edition</em> karya James Stewart. Seluruh penjelasan ditulis ulang dengan
kata-kata sendiri; soal dan contoh dalam situs ini adalah contoh baru, bukan salinan dari buku.</p>
<ul>
  <li><strong>PHP</strong> menyajikan halaman, navigasi bab, dan formulir kalkulator.</li>
  <li><strong>Python</strong> membuat gambar grafik (<code>python/generate_figures.py</code>) dan melakukan perhitungan numerik (<code>python/tools.py</code>).</li>
  <li><strong>MathJax</strong> menampilkan rumus matematika di peramban.</li>
</ul>
<p>Status materi: Bab 10 lengkap, Bab 11 baru subbab 11.1. Bab 12–17 akan ditambahkan.</p>
<?php require __DIR__ . '/includes/footer.php'; ?>
