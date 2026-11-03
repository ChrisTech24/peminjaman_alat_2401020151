# LAPORAN PRAKTIKUM PEMROGRAMAN WEB
## Sistem Peminjaman Alat — Tipe B

**Nama:** ................................................  
**NIM:** 2401020151  
**Kelas:** ................................................  

## 1. Identitas Studi Kasus

| Komponen | Keterangan |
|---|---|
| Tipe soal | B |
| Domain | Sistem Peminjaman Alat |
| Nama database | `peminjaman_alat_2401020151` |
| Route utama | `/peminjaman` |
| Tabel master | `alat` |
| Tabel utama | `peminjaman_alat` |
| Nilai numerik | `jumlah_alat` |

Laboratorium membutuhkan aplikasi untuk mencatat peminjaman alat. Petugas dapat menambah, melihat, mengubah, menghapus, mencari, dan memfilter data peminjaman. Sistem menolak kode peminjaman dan nomor identitas yang sama.

## 2. Rancangan Database

Database terdiri dari dua tabel dengan relasi satu-ke-banyak. Satu alat dapat mempunyai banyak data peminjaman. Kolom `peminjaman_alat.alat_id` merupakan foreign key yang mengarah ke `alat.id`.

### Tabel `alat`

| Kolom | Tipe dan ketentuan |
|---|---|
| `id` | BIGINT UNSIGNED, primary key, auto increment |
| `nama_alat` | VARCHAR(100), NOT NULL, UNIQUE |

### Tabel `peminjaman_alat`

| Kolom | Tipe dan ketentuan |
|---|---|
| `id` | BIGINT UNSIGNED, primary key, auto increment |
| `kode_peminjaman` | CHAR(10), NOT NULL, UNIQUE |
| `nama_peminjam` | VARCHAR(100), NOT NULL |
| `nomor_identitas` | VARCHAR(30), NOT NULL, UNIQUE |
| `jumlah_alat` | TINYINT UNSIGNED, CHECK 1–10 |
| `alat_id` | BIGINT UNSIGNED, NOT NULL, foreign key ke `alat.id` |
| `created_at` dan `updated_at` | Timestamp |

Foreign key menerapkan `ON UPDATE CASCADE` dan `ON DELETE RESTRICT`.

## 3. Data Awal Wajib

| Kode | Nama Peminjam | Nomor Identitas | Jumlah | Alat |
|---|---|---|---:|---|
| PM00000001 | Rina Kurnia | MHS-2201001 | 2 | Kamera |
| PM00000002 | Dedi Pranata | MHS-2201002 | 1 | Proyektor |
| PM00000003 | Mira Ananda | MHS-2201003 | 3 | Kamera |

## 4. Route Aplikasi

| Method | Route | Keterangan |
|---|---|---|
| GET | `/peminjaman` | Read, pencarian, dan filter |
| POST | `/peminjaman` | Create |
| GET | `/peminjaman/{id}/edit` | Form edit |
| PUT | `/peminjaman/{id}` | Update |
| DELETE | `/peminjaman/{id}` | Delete |

## 5. Implementasi Keamanan

- Input teks diproses dengan `trim()` dan `strip_tags()`.
- Kode peminjaman harus tepat 10 karakter alfanumerik.
- Nama peminjam harus 3–100 karakter.
- Nomor identitas harus 5–30 karakter dan unik.
- Jumlah alat harus berupa bilangan bulat 1–10.
- Alat wajib tersedia pada tabel master.
- Form menggunakan `@csrf`.
- Update menggunakan method spoofing `PUT`.
- Delete menggunakan method spoofing `DELETE`.
- `old()` digunakan untuk mempertahankan input ketika validasi gagal.
- Query menggunakan PDO `prepare()` dan `execute()`.
- Error ditangani menggunakan `try-catch`; detail dicatat dengan `report()`, sedangkan pengguna menerima pesan aman.

Fungsi `statusJumlah()` menampilkan **Banyak** jika jumlah alat `>= 3` dan **Sedikit** jika jumlah alat `< 3`. Fungsi tersebut ditampilkan pada Blade saat data diproses dengan perulangan.

## 6. Hasil Pengujian

Pengujian dilakukan pada `http://127.0.0.1:8000/peminjaman`.

| No. | Pengujian | Hasil |
|---:|---|---|
| 1 | Read | Berhasil. Tiga data awal tampil. |
| 2 | Create valid | Berhasil. Data PM00000004 berhasil ditambahkan dan feedback tampil. |
| 3 | Create tidak valid | Berhasil. Format kode tidak valid ditolak dan input lama tetap tampil. |
| 4 | Duplikat | Berhasil. Kode atau nomor identitas yang sudah digunakan ditolak. |
| 5 | Update | Berhasil. Data Rina berhasil diperbarui menjadi Rina Kurnia Meiga dengan jumlah 4. |
| 6 | Konflik Update | Berhasil. Nilai unik milik data lain ditolak. |
| 7 | Delete | Berhasil. Data Mira berhasil dihapus. |
| 8 | Pencarian | Berhasil. Pencarian kode PM00000001 menampilkan data yang sesuai. |
| 9 | Filter | Berhasil. Filter Kamera dan Proyektor menampilkan data sesuai alat. |
| 10 | Error handling | Berhasil. Saat koneksi bermasalah, pengguna menerima pesan aman: “Data tidak dapat dibaca. Periksa koneksi.” |

### Bukti Screenshot

Masukkan screenshot yang sudah diambil pada bagian berikut:

1. Read/data awal: screenshot halaman awal dengan tiga data.
2. Create valid: screenshot pesan “Data berhasil ditambahkan”.
3. Create tidak valid: screenshot pesan format kode tidak valid.
4. Duplikat: screenshot pesan kode/nomor identitas sudah digunakan.
5. Update: screenshot pesan “Data berhasil diperbarui”.
6. Delete: screenshot pesan “Data berhasil dihapus”.
7. Pencarian: screenshot URL dengan kata kunci `PM00000001`.
8. Filter Kamera: screenshot hasil filter Kamera.
9. Filter Proyektor: screenshot hasil filter Proyektor.
10. Error handling: screenshot pesan koneksi aman.

> Jangan menjalankan `migrate:fresh --seed` lagi setelah pengujian jika ingin mempertahankan kondisi database dan bukti pengujian saat ini. Data awal dibuktikan melalui screenshot sebelum pengujian.

## 7. Kendala dan Perbaikan

| Kendala | Perbaikan |
|---|---|
| Perintah `cd` dijalankan pada prompt `mysql>` | Keluar dengan `exit`, lalu menjalankan `cd /d` pada terminal biasa. |
| `Please provide a valid cache path` | Membuat folder `storage/framework/views`, `storage/framework/cache/data`, `storage/framework/sessions`, dan `bootstrap/cache`. |
| Data tidak dapat dibaca | Memastikan MySQL aktif, memeriksa `.env`, dan menjalankan migration serta seeder. |

## 8. Kesimpulan

Sistem Peminjaman Alat Tipe B berhasil dibuat dengan dua tabel berelasi dan memenuhi fitur CRUD, pencarian, filter, validasi, sanitasi, CSRF, prepared statement PDO, error handling, serta fungsi `statusJumlah()`. Seluruh sepuluh skenario pengujian berhasil dilakukan dan didokumentasikan melalui screenshot.
