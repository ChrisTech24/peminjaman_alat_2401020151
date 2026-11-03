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
| 4 | Duplikat | Berhasil. kode atau nomor identitas yang sudah digunakan ditolak. |
| 5 | Update | Berhasil. Data Rina berhasil diperbarui menjadi Rina Kurnia Meiga dengan jumlah 4. |
| 6 | Konflik Update | Berhasil. Nilai unik milik data lain ditolak. |
| 7 | Delete | Berhasil. Data Mira berhasil dihapus. |
| 8 | Pencarian | Berhasil. Pencarian kode PM00000001 menampilkan data yang sesuai. |
| 9 | Filter | Berhasil. Filter Kamera dan Proyektor menampilkan data sesuai alat. |
| 10 | Error handling | Berhasil. Saat koneksi bermasalah, pengguna menerima pesan aman: "Data tidak dapat dibaca. Periksa koneksi." |

### Bukti Screenshot

1. **Read/data awal**: ![Read](./Screenshot_2026-11-03_144459.png) - screenshot halaman awal dengan tiga data.
2. **Create valid**: ![Create Valid](./Screenshot_2026-11-03_144531.png) - screenshot pesan "Data berhasil ditambahkan".
3. **Create tidak valid**: ![Create Invalid](./Screenshot_2026-11-03_144602.png) - screenshot pesan format kode tidak valid.
4. **Duplikat**: ![Duplicate](./Screenshot_2026-11-03_144637.png) - screenshot pesan kode/nomor identitas sudah digunakan.
5. **Update**: ![Update](./Screenshot_2026-11-03_144658.png) - screenshot pesan "Data berhasil diperbarui".
6. **Delete**: ![Delete](./Screenshot_2026-11-03_144714.png) - screenshot pesan "Data berhasil dihapus".
7. **Pencarian**: ![Search](./Screenshot_2026-11-03_144737.png) - screenshot URL dengan kata kunci `PM00000001`.
8. **Filter Kamera**: ![Filter Kamera](./Screenshot_2026-11-03_144812.png) - screenshot hasil filter Kamera.
9. **Filter Proyektor**: ![Filter Proyektor](./Screenshot_2026-11-03_144822.png) - screenshot hasil filter Proyektor.
10. **Error handling**: ![Error Handling](./Screenshot_2026-11-03_144841.png) - screenshot pesan koneksi aman.

> Jangan menjalankan `migrate:fresh --seed` lagi setelah pengujian jika ingin mempertahankan kondisi database dan bukti pengujian saat ini. Data awal dibuktikan melalui screenshot sebelum pengujian.

## 7. Kendala dan Perbaikan

| Kendala | Perbaikan |
|---|---|
| Perintah `cd` dijalankan pada prompt `mysql>` | Keluar dengan `exit`, lalu menjalankan `cd /d` pada terminal biasa. |
| `Please provide a valid cache path` | Membuat folder `storage/framework/views`, `storage/framework/cache/data`, `storage/framework/sessions`, dan `bootstrap/cache`. |
| Data tidak dapat dibaca | Memastikan MySQL aktif, memeriksa `.env`, dan menjalankan migration serta seeder. |

## 8. Kesimpulan

Sistem Peminjaman Alat Tipe B berhasil dibuat dengan dua tabel berelasi dan memenuhi fitur CRUD, pencarian, filter, validasi, sanitasi, CSRF, prepared statement PDO, error handling, serta fungsi `statusJumlah()`. Sepuluh skenario pengujian berhasil dilakukan dan didokumentasikan melalui screenshot.

## 4. DDL dan DML

### 4.1 DDL (Data Definition Language)

DDL digunakan untuk membuat database, tabel, kolom, primary key, foreign key, constraint UNIQUE, constraint CHECK, serta aturan relasi.

```sql
CREATE DATABASE IF NOT EXISTS peminjaman_alat_2401020151;
USE peminjaman_alat_2401020151;

CREATE TABLE alat (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nama_alat VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE peminjaman_alat (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    kode_peminjaman CHAR(10) NOT NULL UNIQUE,
    nama_peminjam VARCHAR(100) NOT NULL,
    nomor_identitas VARCHAR(30) NOT NULL UNIQUE,
    jumlah_alat TINYINT UNSIGNED NOT NULL,
    alat_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL,
    CONSTRAINT jumlah_alat_check CHECK (jumlah_alat BETWEEN 1 AND 10),
    CONSTRAINT peminjaman_alat_alat_id_foreign
        FOREIGN KEY (alat_id) REFERENCES alat(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);
```

### 4.2 DML (Data Manipulation Language)

DML digunakan untuk memasukkan data awal dan memproses data melalui INSERT, SELECT, UPDATE, dan DELETE.

```sql
INSERT INTO alat (nama_alat) VALUES
('Kamera'),
('Proyektor');

INSERT INTO peminjaman_alat
    (kode_peminjaman, nama_peminjam, nomor_identitas,
     jumlah_alat, alat_id, created_at, updated_at)
VALUES
    ('PM00000001', 'Rina Kurnia', 'MHS-2201001', 2, 1, NOW(), NOW()),
    ('PM00000002', 'Dedi Pranata', 'MHS-2201002', 1, 2, NOW(), NOW()),
    ('PM00000003', 'Mira Ananda', 'MHS-2201003', 3, 1, NOW(), NOW());
```

Contoh operasi CRUD SQL:

```sql
-- Read
SELECT p.*, a.nama_alat
FROM peminjaman_alat AS p
JOIN alat AS a ON a.id = p.alat_id;

-- Create
INSERT INTO peminjaman_alat
    (kode_peminjaman, nama_peminjam, nomor_identitas,
     jumlah_alat, alat_id, created_at, updated_at)
VALUES
    ('PM00000004', 'Andi Saputra', 'MHS-2201004', 4, 1, NOW(), NOW());

-- Update
UPDATE peminjaman_alat
SET nama_peminjam = 'Rina Kurnia Meiga', jumlah_alat = 4,
    updated_at = NOW()
WHERE kode_peminjaman = 'PM00000001';

-- Delete
DELETE FROM peminjaman_alat
WHERE kode_peminjaman = 'PM00000003';
```

Berkas SQL lengkap tersedia pada `database/sql/tipe_b_ddl_dml.sql`. Implementasi aplikasi tetap menggunakan PDO prepared statement untuk query yang menerima input pengguna.