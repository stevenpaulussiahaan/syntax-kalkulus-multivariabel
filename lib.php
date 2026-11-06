<?php
declare(strict_types=1);

const SITE_TITLE = 'Kalkulus Multivariabel';

function chapters(): array
{
    static $c = null;
    return $c ??= require __DIR__ . '/chapters.php';
}

function e(string $s): string
{
    return htmlspecialchars($s, ENT_QUOTES, 'UTF-8');
}

/** Cari subbab berdasarkan slug berkas. Mengembalikan [bab, indeks] atau null. */
function find_section(string $slug): ?array
{
    foreach (chapters() as $num => $ch) {
        foreach ($ch['sections'] as $i => $s) {
            if ($s[2] === $slug) {
                return [$num, $i];
            }
        }
    }
    return null;
}

/** Daftar datar subbab yang tersedia, untuk navigasi sebelumnya/berikutnya. */
function flat_ready(): array
{
    $out = [];
    foreach (chapters() as $num => $ch) {
        foreach ($ch['sections'] as $s) {
            if ($s[2] !== null) {
                $out[] = ['bab' => $num, 'no' => $s[0], 'title' => $s[1], 'slug' => $s[2]];
            }
        }
    }
    return $out;
}

/** Python tidak selalu ada di hosting; panggil dengan aman bila tersedia. */
function run_python(string $script, array $args = []): ?string
{
    if (!function_exists('shell_exec')) {
        return null;
    }
    $py = trim((string) @shell_exec('command -v python3 2>/dev/null'));
    if ($py === '') {
        return null;
    }
    $cmd = escapeshellcmd($py) . ' ' . escapeshellarg(__DIR__ . '/../python/' . $script);
    foreach ($args as $a) {
        $cmd .= ' ' . escapeshellarg((string) $a);
    }
    $out = @shell_exec($cmd . ' 2>&1');
    return $out === null ? null : $out;
}
