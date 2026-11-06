<?php
/** @var string $pageTitle */
$active = $active ?? null;
?><!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($pageTitle) ?> · <?= e(SITE_TITLE) ?></title>
<link rel="stylesheet" href="assets/style.css">
<script>
window.MathJax = {
  tex: { inlineMath: [['\\(', '\\)']], displayMath: [['\\[', '\\]']] },
  svg: { fontCache: 'global' }
};
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
</head>
<body>
<header class="top">
  <a class="brand" href="index.php">∫∂ <?= e(SITE_TITLE) ?></a>
  <nav>
    <a href="index.php">Daftar Bab</a>
    <a href="kalkulator.php">Kalkulator Python</a>
    <a href="tentang.php">Tentang</a>
  </nav>
</header>
<div class="layout">
<aside class="side">
<?php foreach (chapters() as $num => $ch): ?>
  <details <?= ($active === $num) ? 'open' : '' ?>>
    <summary>Bab <?= $num ?> · <?= e($ch['title']) ?></summary>
    <ul>
    <?php foreach ($ch['sections'] as $s): ?>
      <?php if ($s[2] !== null): ?>
        <li><a href="chapter.php?s=<?= e($s[2]) ?>"><?= e($s[0]) ?> <?= e($s[1]) ?></a></li>
      <?php else: ?>
        <li class="soon"><?= e($s[0]) ?> <?= e($s[1]) ?></li>
      <?php endif; ?>
    <?php endforeach; ?>
    </ul>
  </details>
<?php endforeach; ?>
</aside>
<main>
<div class="credit">Web by: Steven Paulus Siahaan</div>
