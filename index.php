<?php
require __DIR__ . '/includes/lib.php';
$pageTitle = 'Beranda';
require __DIR__ . '/includes/header.php';
?>
<h1>Materi Kuliah Kalkulus Multivariabel</h1>
<p class="lead">Catatan kuliah lengkap per bab, ditulis dalam bahasa Indonesia, lengkap dengan turunan rumus,
contoh soal berlangkah, dan grafik yang dihasilkan Python.</p>

<div class="grid">
<?php foreach (chapters() as $num => $ch):
    $first = null;
    foreach ($ch['sections'] as $s) { if ($s[2] !== null) { $first = $s[2]; break; } }
    $status = $ch['ready'] === true ? 'Tersedia' : ($ch['ready'] === 'partial' ? 'Sebagian' : 'Segera');
?>
  <article class="card <?= $first ? '' : 'disabled' ?>">
    <span class="badge <?= strtolower($status) ?>"><?= $status ?></span>
    <h2>Bab <?= $num ?></h2>
    <h3><?= e($ch['title']) ?></h3>
    <p><?= count($ch['sections']) ?> subbab</p>
    <?php if ($first): ?><a class="btn" href="chapter.php?s=<?= e($first) ?>">Mulai belajar →</a><?php endif; ?>
  </article>
<?php endforeach; ?>
</div>
<?php require __DIR__ . '/includes/footer.php'; ?>
