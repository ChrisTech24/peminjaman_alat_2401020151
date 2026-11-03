<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Latihan PHP Dasar</title>
</head>
<body>
    <h1>Hasil Praktikum PHP Dasar</h1>
    <p>Nama Mahasiswa: {{ $nama }}</p>

    <p>Daftar Nilai:</p>
    <ul>
        @foreach ($nilai as $n)
            <li>{{ $n }}</li>
        @endforeach
    </ul>

    <p>Nilai Rata-rata: {{ $rataRata }}</p>
    <p>Status Kelulusan: {{ $status }}</p>
</body>
</html>