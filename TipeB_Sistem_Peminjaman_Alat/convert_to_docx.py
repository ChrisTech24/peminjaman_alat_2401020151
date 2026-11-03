from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Create document
doc = Document()

# Set default font
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)

# Title
title = doc.add_heading('LAPORAN PRAKTIKUM PEMROGRAMAN WEB', level=0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

# Subtitle
subtitle = doc.add_heading('Sistem Peminjaman Alat — Tipe B', level=1)
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

# Add metadata placeholders
doc.add_paragraph()
meta = doc.add_paragraph()
meta.add_run('Nama: ').bold = True
meta.add_run('.................................................\n')
meta.add_run('NIM: ').bold = True
meta.add_run('2401020151\n')
meta.add_run('Kelas: ').bold = True
meta.add_run('.................................................')

# ================================
# 1. Identitas Studi Kasus
# ================================
doc.add_heading('1. Identitas Studi Kasus', level=2)

table1 = doc.add_table(rows=7, cols=2, style='Light List Accent 1')
table1.autofit = True
data1 = [
    ('Tipe soal', 'B'),
    ('Domain', 'Sistem Peminjaman Alat'),
    ('Nama database', 'peminjaman_alat_2401020151'),
    ('Route utama', '/peminjaman'),
    ('Tabel master', 'alat'),
    ('Tabel utama', 'peminjaman_alat'),
    ('Nilai numerik', 'jumlah_alat'),
]
for i, (label, value) in enumerate(data1):
    table1.rows[i].cells[0].text = label
    table1.rows[i].cells[1].text = value
    for paragraph in table1.rows[i].cells[0].paragraphs:
        for run in paragraph.runs:
            run.bold = True

# ================================
# 2. Rancangan Database
# ================================
doc.add_heading('2. Rancangan Database', level=2)

p = doc.add_paragraph('Database terdiri dari dua tabel dengan relasi satu-ke-banyak. Satu alat dapat mempunyai banyak data peminjaman. Kolom `peminjaman_alat.alat_id` merupakan foreign key yang mengarah ke `alat.id`.')

doc.add_heading('Tabel `alat`', level=3)

table2 = doc.add_table(rows=2, cols=2, style='Light List Accent 1')
table2.rows[0].cells[0].text = 'Kolom'
table2.rows[0].cells[1].text = 'Tipe dan ketentuan'
table2.rows[1].cells[0].text = '`id`'
table2.rows[1].cells[1].text = 'BIGINT UNSIGNED, primary key, auto increment'
for p in table2.rows[1].cells[0].paragraphs:
    for run in p.runs:
        run.bold = True

doc.add_heading('Tabel `peminjaman_alat`', level=3)

table3 = doc.add_table(rows=8, cols=2, style='Light List Accent 1')
table3.autofit = True
data3 = [
    ('`id`', 'BIGINT UNSIGNED, primary key, auto increment'),
    ('`kode_peminjaman`', 'CHAR(10), NOT NULL, UNIQUE'),
    ('`nama_peminjam`', 'VARCHAR(100), NOT NULL'),
    ('`nomor_identitas`', 'VARCHAR(30), NOT NULL, UNIQUE'),
    ('`jumlah_alat`', 'TINYINT UNSIGNED, CHECK 1–10'),
    ('`alat_id`', 'BIGINT UNSIGNED, NOT NULL, foreign key ke `alat.id`'),
    ('`created_at` dan `updated_at`', 'Timestamp'),
]
for i, (col1, col2) in enumerate(data3):
    table3.rows[i].cells[0].text = col1
    table3.rows[i].cells[1].text = col2
    if i == 0:
        for p in table3.rows[i].cells[0].paragraphs:
            for run in p.runs:
                run.bold = True

# ================================
# 3. Data Awal Wajib
# ================================
doc.add_heading('3. Data Awal Wajib', level=2)

table4 = doc.add_table(rows=4, cols=5, style='Light List Accent 1')
table4.autofit = True
headers4 = ['Kode', 'Nama Peminjam', 'Nomor Identitas', 'Jumlah', 'Alat']
for i, h in enumerate(headers4):
    table4.rows[0].cells[i].text = h
    for p in table4.rows[0].cells[i].paragraphs:
        for run in p.runs:
            run.bold = True

data4 = [
    ('PM00000001', 'Rina Kurnia', 'MHS-2201001', '2', 'Kamera'),
    ('PM00000002', 'Dedi Pranata', 'MHS-2201002', '1', 'Proyektor'),
    ('PM00000003', 'Mira Ananda', 'MHS-2201003', '3', 'Kamera'),
]
for row_idx, row_data in enumerate(data4):
    for col_idx, cell_data in enumerate(row_data):
        table4.rows[row_idx + 1].cells[col_idx].text = cell_data

# ================================
# 4. Route Aplikasi
# ================================
doc.add_heading('4. Route Aplikasi', level=2)

table5 = doc.add_table(rows=6, cols=3, style='Light List Accent 1')
table5.autofit = True
headers5 = ['Method', 'Route', 'Keterangan']
for i, h in enumerate(headers5):
    table5.rows[0].cells[i].text = h
    for p in table5.rows[0].cells[i].paragraphs:
        for run in p.runs:
            run.bold = True

data5 = [
    ('GET', '/peminjaman', 'Read, pencarian, dan filter'),
    ('POST', '/peminjaman', 'Create'),
    ('GET', '/peminjaman/{id}/edit', 'Form edit'),
    ('PUT', '/peminjaman/{id}', 'Update'),
    ('DELETE', '/peminjaman/{id}', 'Delete'),
]
for row_idx, row_data in enumerate(data5):
    for col_idx, cell_data in enumerate(row_data):
        table5.rows[row_idx + 1].cells[col_idx].text = cell_data

# ================================
# 5. Implementasi Keamanan
# ================================
doc.add_heading('5. Implementasi Keamanan', level=2)

security_items = [
    'Input teks diproses dengan `trim()` dan `strip_tags()`.',
    'Kode peminjaman harus tepat 10 karakter alfanumerik.',
    'Nama peminjam harus 3–100 karakter.',
    'Nomor identitas harus 5–30 karakter dan unik.',
    'Jumlah alat harus berupa bilangan bulat 1–10.',
    'Alat wajib tersedia pada tabel master.',
    'Form menggunakan `@csrf`.',
    'Update menggunakan method spoofing `PUT`.',
    'Delete menggunakan method spoofing `DELETE`.',
    '`old()` digunakan untuk mempertahankan input ketika validasi gagal.',
    'Query menggunakan PDO `prepare()` dan `execute()`.',
    'Error ditangani menggunakan `try-catch`; detail dicatat dengan `report()`, sedangkan pengguna menerima pesan aman.',
    'Fungsi `statusJumlah()` menampilkan **Banyak** jika jumlah alat >= 3 dan **Sedikit** jika < 3.',
]
for item in security_items:
    p = doc.add_paragraph(item, style='List Bullet')

# ================================
# 6. Hasil Pengujian
# ================================
doc.add_heading('6. Hasil Pengujian', level=2)

p = doc.add_paragraph('Pengujian dilakukan pada `http://127.0.0.1:8000/peminjaman`.')

# Hasil table
table6 = doc.add_table(rows=11, cols=3, style='Light List Accent 1')
table6.autofit = True
headers6 = ['No.', 'Pengujian', 'Hasil']
for i, h in enumerate(headers6):
    table6.rows[0].cells[i].text = h
    for p in table6.rows[0].cells[i].paragraphs:
        for run in p.runs:
            run.bold = True

data6 = [
    ('1', 'Read', 'Berhasil. Tiga data awal tampil.'),
    ('2', 'Create valid', 'Berhasil. Data PM00000004 berhasil ditambahkan dan feedback tampil.'),
    ('3', 'Create tidak valid', 'Berhasil. Format kode tidak valid ditolak dan input lama tetap tampil.'),
    ('4', 'Duplikat', 'Berhasil. kode atau nomor identitas yang sudah digunakan ditolak.'),
    ('5', 'Update', 'Berhasil. Data Rina berhasil diperbarui menjadi Rina Kurnia Meiga dengan jumlah 4.'),
    ('6', 'Konflik Update', 'Berhasil. Nilai unik milik data lain ditolak.'),
    ('7', 'Delete', 'Berhasil. Data Mira berhasil dihapus.'),
    ('8', 'Pencarian', 'Berhasil. Pencarian kode PM00000001 menampilkan data yang sesuai.'),
    ('9', 'Filter', 'Berhasil. Filter Kamera dan Proyektor menampilkan data sesuai alat.'),
    ('10', 'Error handling', 'Berhasil. Saat koneksi bermasalah, pengguna menerima pesan aman: "Data tidak dapat dibaca. Periksa koneksi."'),
]
for row_idx, row_data in enumerate(data6):
    for col_idx, cell_data in enumerate(row_data):
        table6.rows[row_idx + 1].cells[col_idx].text = cell_data

# Bukti Screenshot section
doc.add_heading('Bukti Screenshot', level=3)

p = doc.add_paragraph('Masukkan screenshot yang sudah diambil pada bagian berikut:')
screenshot_items = [
    '1. Read/data awal: screenshot halaman awal dengan tiga data.',
    '2. Create valid: screenshot pesan "Data berhasil ditambahkan".',
    '3. Create tidak valid: screenshot pesan format kode tidak valid.',
    '4. Duplikat: screenshot pesan kode/nomor identitas sudah digunakan.',
    '5. Update: screenshot pesan "Data berhasil diperbarui".',
    '6. Delete: screenshot pesan "Data berhasil dihapus".',
    '7. Pencarian: screenshot URL dengan kata kunci `PM00000001`.',
    '8. Filter Kamera: screenshot hasil filter Kamera.',
    '9. Filter Proyektor: screenshot hasil filter Proyektor.',
    '10. Error handling: screenshot pesan koneksi aman.',
]
for item in screenshot_items:
    doc.add_paragraph(item, style='List Bullet')

p = doc.add_paragraph()
p.add_run('Catatan: ').bold = True
p.add_run('Jangan menjalankan `migrate:fresh --seed` lagi setelah pengujian jika ingin mempertahankan kondisi database dan bukti pengujian saat ini. Data awal dibuktikan melalui screenshot sebelum pengujian.')

# ================================
# 7. Kendala dan Perbaikan
# ================================
doc.add_heading('7. Kendala dan Perbaikan', level=2)

table7 = doc.add_table(rows=4, cols=2, style='Light List Accent 1')
table7.autofit = True
data7 = [
    ('Perintah `cd` dijalankan pada prompt `mysql>`', 'Keluar dengan `exit`, lalu menjalankan `cd /d` pada terminal biasa.'),
    ('`Please provide a valid cache path`', 'Membuat folder `storage/framework/views`, `storage/framework/cache/data`, `storage/framework/sessions`, dan `bootstrap/cache`.'),
    ('Data tidak dapat dibaca', 'Memastikan MySQL aktif, memeriksa `.env`, dan menjalankan migration serta seeder.'),
]
for i, (kendala, perbaikan) in enumerate(data7):
    table7.rows[i].cells[0].text = kendala
    table7.rows[i].cells[1].text = perbaikan
    for p in table7.rows[i].cells[0].paragraphs:
        for run in p.runs:
            run.bold = True

# ================================
# 8. Kesimpulan
# ================================
doc.add_heading('8. Kesimpulan', level=2)

conclusion = doc.add_paragraph()
conclusion.add_run('Sistem Peminjaman Alat Tipe B berhasil dibuat dengan dua tabel berelasi dan memenuhi fitur CRUD, pencarian, filter, validasi, sanitasi, CSRF, prepared statement PDO, error handling, serta fungsi `statusJumlah()`.').italic = True
doc.add_paragraph('Seluruh sepuluh skenario pengujian berhasil dilakukan dan didokumentasikan melalui screenshot.')

# ================================
# 4. DDL dan DML
# ================================
doc.add_heading('4. DDL dan DML', level=2)

doc.add_heading('4.1 DDL (Data Definition Language)', level=3)

p = doc.add_paragraph('DDL digunakan untuk membuat database, tabel, kolom, primary key, foreign key, constraint UNIQUE, constraint CHECK, serta aturan relasi.')

ddl_sql = """CREATE DATABASE IF NOT EXISTS peminjaman_alat_2401020151;
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
"""
doc.add_paragraph(ddl_sql)

doc.add_heading('4.2 DML (Data Manipulation Language)', level=3)

p = doc.add_paragraph('DML digunakan untuk memasukkan data awal dan memproses data melalui INSERT, SELECT, UPDATE, dan DELETE.')

dml_sql = """INSERT INTO alat (nama_alat) VALUES
('Kamera'),
('Proyektor');

INSERT INTO peminjaman_alat
    (kode_peminjaman, nama_peminjam, nomor_identitas,
     jumlah_alat, alat_id, created_at, updated_at)
VALUES
    ('PM00000001', 'Rina Kurnia', 'MHS-2201001', 2, 1, NOW(), NOW()),
    ('PM00000002', 'Dedi Pranata', 'MHS-2201002', 1, 2, NOW(), NOW()),
    ('PM00000003', 'Mira Ananda', 'MHS-2201003', 3, 1, NOW(), NOW());

Contoh operasi CRUD SQL:

Read
SELECT p.*, a.nama_alat
FROM peminjaman_alat AS p
JOIN alat AS a ON a.id = p.alat_id;

Create
INSERT INTO peminjaman_alat
    (kode_peminjaman, nama_peminjam, nomor_identitas,
     jumlah_alat, alat_id, created_at, updated_at)
VALUES
    ('PM00000004', 'Andi Saputra', 'MHS-2201004', 4, 1, NOW(), NOW());

Update
UPDATE peminjaman_alat
SET nama_peminjam = 'Rina Kurnia Meiga', jumlah_alat = 4,
    updated_at = NOW()
WHERE kode_peminjaman = 'PM00000001';

Delete
DELETE FROM peminjaman_alat
WHERE kode_peminjaman = 'PM00000003';
"""
doc.add_paragraph(dml_sql)

p = doc.add_paragraph()
p.add_run('Berkas SQL lengkap tersedia pada `database/sql/tipe_b_ddl_dml.sql`. ').bold = True
p.add_run('Implementasi aplikasi tetap menggunakan PDO prepared statement untuk query yang menerima input pengguna.')

# Save the document
output_path = 'Laporan_TipeB_Sistem_Peminjaman_Alat_FINAL.docx'
doc.save(output_path)
print(f'Document saved to {output_path}')