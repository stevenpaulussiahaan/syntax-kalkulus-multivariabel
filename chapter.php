<?php
require __DIR__ . '/includes/lib.php';

$slug = $_GET['s'] ?? '';
// Hanya izinkan slug yang terdaftar (mencegah path traversal).
$found = is_string($slug) ? find_section($slug) : null;
if ($found === null) {
    http_response_code(404);
    $pageTitle = 'Tidak ditemukan';
    require __DIR__ . '/includes/header.php';
    echo '<h1>Halaman tidak ditemukan</h1><p><a href="index.php">Kembali ke daftar bab</a></p>';
    require __DIR__ . '/includes/footer.php';
    exit;
}

[$bab, $idx] = $found;
$sec = chapters()[$bab]['sections'][$idx];
$file = __DIR__ . '/content/' . $slug . '.html';
$pageTitle = $sec[0] . ' ' . $sec[1];
$active = $bab;

$flat = flat_ready();
$pos = array_search($slug, array_column($flat, 'slug'), true);
$prev = $pos > 0 ? $flat[$pos - 1] : null;
$next = $pos < count($flat) - 1 ? $flat[$pos + 1] : null;

require __DIR__ . '/includes/header.php';
?>
<p class="crumb">Bab <?= $bab ?> · <?= e(chapters()[$bab]['title']) ?></p>
<h1><?= e($sec[0]) ?> <?= e($sec[1]) ?></h1>
<article class="materi">
<?php
if (is_file($file)) {
    readfile($file);
} else {
    echo '<p>Materi subbab ini belum tersedia.</p>';
}
?>
</article>
<nav class="pager">
  <?php if ($prev): ?><a href="chapter.php?s=<?= e($prev['slug']) ?>">← <?= e($prev['no']) ?> <?= e($prev['title']) ?></a><?php else: ?><span></span><?php endif; ?>
  <?php if ($next): ?><a href="chapter.php?s=<?= e($next['slug']) ?>"><?= e($next['no']) ?> <?= e($next['title']) ?> →</a><?php endif; ?>
</nav>
<?php require __DIR__ . '/includes/footer.php'; ?>
