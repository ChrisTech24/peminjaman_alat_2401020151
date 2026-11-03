-- Berkas: database/sql/pertemuan4_struktur.sql
-- Nama : Christian Aprilio Sihite
-- NIM  : 2401020151

CREATE DATABASE IF NOT EXISTS praktikum_web_2401020151
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE praktikum_web_2401020151;

CREATE TABLE program_studi (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nama_prodi VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE mahasiswa (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nim CHAR(10) NOT NULL UNIQUE,
    nama VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    usia TINYINT UNSIGNED NOT NULL,
    program_studi_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_mahasiswa_program_studi
        FOREIGN KEY (program_studi_id)
        REFERENCES program_studi(id)
        -- id prodi berubah, id di mahasiswa ikut berubah
        ON UPDATE CASCADE
        -- prodi yang masih punya mahasiswa tidak bisa dihapus
        ON DELETE RESTRICT,
    CONSTRAINT chk_usia
        CHECK (usia BETWEEN 17 AND 60)
) ENGINE=InnoDB;