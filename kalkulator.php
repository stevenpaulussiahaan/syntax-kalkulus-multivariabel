<?php
require __DIR__ . '/includes/lib.php';
$pageTitle = 'Kalkulator Python';

$modes = [
    'parametrik_panjang'    => ['Panjang kurva parametrik', ['x(t)', 'y(t)', 't awal', 't akhir']],
    'parametrik_kemiringan' => ['Kemiringan garis singgung parametrik', ['x(t)', 'y(t)', 't₀']],
    'parametrik_luas'       => ['Luas di bawah kurva parametrik', ['x(t)', 'y(t)', 't awal', 't akhir']],
    'kutub_luas'            => ['Luas daerah kutub', ['r(t) (t = θ)', 'θ awal', 'θ akhir']],
    'kutub_panjang'         => ['Panjang kurva kutub', ['r(t) (t = θ)', 'θ awal', 'θ akhir']],
    'barisan'               => ['Suku-suku barisan', ['a(n)', 'n awal', 'n akhir']],
];

$result = null;
$error = null;
$mode = $_POST['mode'] ?? 'parametrik_panjang';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($modes[$mode])) {
    $args = [];
    foreach (array_keys($modes[$mode][1]) as $i) {
        $v = trim((string) ($_POST["a$i"] ?? ''));
        if ($v === '' || strlen($v) > 200) {
            $error = 'Semua kolom harus diisi (maks. 200 karakter).';
            break;
        }
        $args[] = $v;
    }
    if (!$error) {
        $raw = run_python('tools.py', array_merge([$mode], $args));
        if ($raw === null || $raw === '') {
            $error = 'Python tidak tersedia di server ini. Lihat README untuk opsi hosting yang mendukung Python.';
        } else {
            $result = json_decode($raw, true);
            if (!is_array($result)) {
                $error = 'Keluaran Python tidak dapat dibaca.';
            } elseif (isset($result['error'])) {
                $error = $result['error'];
                $result = null;
            }
        }
    }
}

require __DIR__ . '/includes/header.php';
?>
<h1>Kalkulator Numerik (Python)</h1>
<p>Gunakan peubah <code>t</code> (atau <code>n</code> untuk barisan). Fungsi yang didukung:
<code>sin cos tan sec csc cot exp ln sqrt abs sinh cosh</code>, konstanta <code>pi</code>, <code>e</code>, dan pangkat dengan <code>^</code>.
Batas boleh ditulis seperti <code>2*pi</code>.</p>

<form class="calc" method="post">
  <label>Jenis perhitungan
    <select name="mode" onchange="this.form.submit()">
      <?php foreach ($modes as $k => $m): ?>
        <option value="<?= e($k) ?>" <?= $k === $mode ? 'selected' : '' ?>><?= e($m[0]) ?></option>
      <?php endforeach; ?>
    </select>
  </label>
  <?php foreach ($modes[$mode][1] as $i => $label): ?>
    <label><?= e($label) ?>
      <input name="a<?= $i ?>" value="<?= e((string) ($_POST["a$i"] ?? '')) ?>" required>
    </label>
  <?php endforeach; ?>
  <button type="submit" name="go" value="1">Hitung</button>
</form>

<?php if ($error): ?><p class="box note"><?= e($error) ?></p><?php endif; ?>
<?php if ($result): ?>
  <h2>Hasil</h2>
  <pre><?= e(json_encode($result, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE)) ?></pre>
<?php endif; ?>
<?php require __DIR__ . '/includes/footer.php'; ?>
