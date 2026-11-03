<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void
    {
        Schema::create('alat', function (Blueprint $table) { $table->id(); $table->string('nama_alat', 100)->unique(); });
        Schema::create('peminjaman_alat', function (Blueprint $table) {
            $table->id(); $table->char('kode_peminjaman', 10)->unique(); $table->string('nama_peminjam', 100);
            $table->string('nomor_identitas', 30)->unique(); $table->unsignedTinyInteger('jumlah_alat'); $table->foreignId('alat_id')->constrained('alat')->restrictOnDelete()->cascadeOnUpdate(); $table->timestamps();
        });
        DB::statement('ALTER TABLE peminjaman_alat ADD CONSTRAINT jumlah_alat_check CHECK (jumlah_alat BETWEEN 1 AND 10)');
    }
    public function down(): void { Schema::dropIfExists('peminjaman_alat'); Schema::dropIfExists('alat'); }
};
