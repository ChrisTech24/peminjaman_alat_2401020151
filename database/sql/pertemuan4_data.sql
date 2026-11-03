-- Berkas: database/sql/pertemuan4_data.sql

USE praktikum_web_2401020151;

-- 1. Menambahkan 2 Program Studi
INSERT INTO program_studi (nama_prodi) VALUES
    ('Teknik Informatika'),
    ('Teknik Elektro');

-- 2. Menambahkan 4 Data Mahasiswa (1 data sementara)
INSERT INTO mahasiswa (nim, nama, email, usia, program_studi_id) VALUES
    ('2401020151', 'Christian Aprilio Sihite', 'christian@gmail.com', 20, 1),
    ('2401020152', 'Dina Mariana', 'dina@gmail.com', 19, 1),
    ('2401020201', 'Eko Prasetyo', 'eko@gmail.com', 21, 2),
    ('2401020999', 'Data Sementara', 'sementara@gmail.com', 18, 2);

-- 3. Memperbarui Email
UPDATE mahasiswa
SET email = 'dina.mariana@gmail.com'
WHERE nim = '2401020152';

-- 4. Menghapus Data Sementara
DELETE FROM mahasiswa
WHERE nim = '2401020999';

-- 5. Menampilkan Hasil Akhir (3 Mahasiswa) dengan JOIN
SELECT m.nim, m.nama, m.email, m.usia, p.nama_prodi
FROM mahasiswa AS m
JOIN program_studi AS p
    ON p.id = m.program_studi_id
ORDER BY m.nim;