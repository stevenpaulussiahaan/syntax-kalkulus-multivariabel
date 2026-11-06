<?php
/** Daftar bab & subbab dibaca dari chapters.json (dipakai juga oleh build_static.py). */
$data = json_decode(file_get_contents(__DIR__ . '/chapters.json'), true);
$out = [];
foreach ($data as $num => $ch) { $out[(int) $num] = $ch; }
return $out;
