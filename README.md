# Tipe B — Sistem Peminjaman Alat

## Menjalankan
1. Buat database MySQL `peminjaman_alat_2401020151` (ganti NIM bila diperlukan).
2. Salin `.env.example` menjadi `.env`, isi `DB_DATABASE`, `DB_USERNAME`, dan `DB_PASSWORD`.
3. Jalankan `php artisan key:generate`.
4. Jalankan `php artisan migrate:fresh --seed`.
5. Jalankan `php artisan serve`, buka `/peminjaman`.

## Alur pembuatan database
Database memiliki tabel master `alat` dan tabel transaksi `peminjaman_alat`. Relasinya satu alat memiliki banyak peminjaman melalui `alat_id`. PK, FK, UNIQUE, NOT NULL, CHECK 1–10, cascade update, dan restrict delete diterapkan melalui migration.

## Alur pengujian wajib
1. Read: pastikan 3 data awal tampil.
2. Create valid: isi data baru, pastikan tersimpan dan feedback muncul.
3. Create invalid: kosongkan nama / jumlah di luar 1–10, pastikan error dan old input tampil.
4. Duplikat: gunakan kode atau nomor identitas yang sudah ada, pastikan ditolak.
5. Update: klik Edit, ubah data, pastikan tersimpan.
6. Konflik Update: ubah kode menjadi milik data lain, pastikan ditolak.
7. Delete: klik Hapus dan pastikan data hilang.
8. Pencarian: cari dengan kode, nama, lalu nomor identitas.
9. Filter: pilih Kamera atau Proyektor.
10. Error handling: matikan koneksi/database, pastikan pengguna mendapat pesan aman dan detail tercatat di log.

Semua query input menggunakan PDO prepared statement. Jangan commit `.env`.
