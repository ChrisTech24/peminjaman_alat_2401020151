-- DDL (Data Definition Language)
-- Database: peminjaman_alat_2401020151

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

-- DML (Data Manipulation Language)

INSERT INTO alat (nama_alat) VALUES
('Kamera'),
('Proyektor');

INSERT INTO peminjaman_alat
    (kode_peminjaman, nama_peminjam, nomor_identitas, jumlah_alat, alat_id, created_at, updated_at)
VALUES
    ('PM00000001', 'Rina Kurnia', 'MHS-2201001', 2, 1, NOW(), NOW()),
    ('PM00000002', 'Dedi Pranata', 'MHS-2201002', 1, 2, NOW(), NOW()),
    ('PM00000003', 'Mira Ananda', 'MHS-2201003', 3, 1, NOW(), NOW());

-- Contoh DML untuk pengujian CRUD
-- INSERT INTO peminjaman_alat (...) VALUES (...);
-- UPDATE peminjaman_alat SET nama_peminjam = 'Rina Kurnia Meiga' WHERE id = 1;
-- DELETE FROM peminjaman_alat WHERE id = 3;
-- SELECT p.*, a.nama_alat
-- FROM peminjaman_alat p
-- JOIN alat a ON a.id = p.alat_id;
