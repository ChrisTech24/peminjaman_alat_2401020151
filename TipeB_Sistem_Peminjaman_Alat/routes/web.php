<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Route;

Route::redirect('/', '/peminjaman');

function statusJumlah(int $jumlah): string
{
    return $jumlah >= 3 ? 'Banyak' : 'Sedikit';
}

Route::get('/peminjaman', function (Request $request) {
    $q = trim(strip_tags((string) $request->query('q', '')));
    $alatId = $request->query('alat_id', '');
    try {
        $pdo = DB::connection()->getPdo();
        $sql = 'SELECT p.*, a.nama_alat FROM peminjaman_alat p JOIN alat a ON a.id = p.alat_id WHERE 1=1';
        $params = [];
        if ($q !== '') {
            $sql .= ' AND (p.kode_peminjaman LIKE :kode OR p.nama_peminjam LIKE :nama OR p.nomor_identitas LIKE :identitas)';
            $params = ['kode' => "%$q%", 'nama' => "%$q%", 'identitas' => "%$q%"];
        }
        if ($alatId !== '') { $sql .= ' AND p.alat_id = :alat_id'; $params['alat_id'] = (int) $alatId; }
        $sql .= ' ORDER BY p.kode_peminjaman';
        $stmt = $pdo->prepare($sql); $stmt->execute($params);
        $peminjaman = $stmt->fetchAll(PDO::FETCH_ASSOC);
        $stmt = $pdo->prepare('SELECT id, nama_alat FROM alat ORDER BY nama_alat'); $stmt->execute();
        $alat = $stmt->fetchAll(PDO::FETCH_ASSOC);
        return view('peminjaman', compact('peminjaman', 'alat', 'q', 'alatId'));
    } catch (Throwable $error) { report($error); return response('Data tidak dapat dibaca. Periksa koneksi.', 500); }
})->name('peminjaman.index');

Route::post('/peminjaman', function (Request $request) {
    $data = $request->validate([
        'kode_peminjaman' => ['required','regex:/^[A-Za-z0-9]{10}$/'], 'nama_peminjam' => ['required','string','min:3','max:100'],
        'nomor_identitas' => ['required','string','min:5','max:30'], 'jumlah_alat' => ['required','integer','min:1','max:10'], 'alat_id' => ['required','integer'],
    ]);
    foreach ($data as $key => $value) { if (is_string($value)) { $data[$key] = trim(strip_tags($value)); } }
    try {
        $pdo = DB::connection()->getPdo();
        $check = $pdo->prepare('SELECT COUNT(*) FROM peminjaman_alat WHERE kode_peminjaman = :kode OR nomor_identitas = :identitas');
        $check->execute(['kode' => $data['kode_peminjaman'], 'identitas' => $data['nomor_identitas']]);
        if ((int) $check->fetchColumn() > 0) return back()->withInput()->with('gagal', 'Kode peminjaman atau nomor identitas sudah digunakan.');
        $stmt = $pdo->prepare('INSERT INTO peminjaman_alat (kode_peminjaman,nama_peminjam,nomor_identitas,jumlah_alat,alat_id,created_at,updated_at) VALUES (:kode_peminjaman,:nama_peminjam,:nomor_identitas,:jumlah_alat,:alat_id,NOW(),NOW())');
        $stmt->execute($data); return to_route('peminjaman.index')->with('berhasil', 'Data berhasil ditambahkan.');
    } catch (Throwable $error) { report($error); return back()->withInput()->with('gagal', 'Data gagal disimpan.'); }
})->name('peminjaman.store');

Route::get('/peminjaman/{id}/edit', function (int $id) {
    try { $pdo = DB::connection()->getPdo(); $s = $pdo->prepare('SELECT * FROM peminjaman_alat WHERE id=:id'); $s->execute(['id'=>$id]); $data=$s->fetch(PDO::FETCH_ASSOC); if (!$data) return to_route('peminjaman.index')->with('gagal','Data tidak ditemukan.'); $s=$pdo->prepare('SELECT id,nama_alat FROM alat ORDER BY nama_alat'); $s->execute(); $alat=$s->fetchAll(PDO::FETCH_ASSOC); return view('peminjaman-edit', compact('data','alat')); } catch (Throwable $error) { report($error); return to_route('peminjaman.index')->with('gagal','Form tidak dapat dibuka.'); }
})->name('peminjaman.edit');

Route::put('/peminjaman/{id}', function (Request $request, int $id) {
    $data = $request->validate(['kode_peminjaman'=>['required','regex:/^[A-Za-z0-9]{10}$/'],'nama_peminjam'=>['required','string','min:3','max:100'],'nomor_identitas'=>['required','string','min:5','max:30'],'jumlah_alat'=>['required','integer','min:1','max:10'],'alat_id'=>['required','integer']]);
    foreach ($data as $key=>$value) if (is_string($value)) $data[$key]=trim(strip_tags($value));
    try { $pdo=DB::connection()->getPdo(); $s=$pdo->prepare('SELECT COUNT(*) FROM peminjaman_alat WHERE (kode_peminjaman=:kode OR nomor_identitas=:identitas) AND id<>:id'); $s->execute(['kode'=>$data['kode_peminjaman'],'identitas'=>$data['nomor_identitas'],'id'=>$id]); if ((int)$s->fetchColumn()>0) return back()->withInput()->with('gagal','Nilai unik milik data lain.'); $s=$pdo->prepare('UPDATE peminjaman_alat SET kode_peminjaman=:kode_peminjaman,nama_peminjam=:nama_peminjam,nomor_identitas=:nomor_identitas,jumlah_alat=:jumlah_alat,alat_id=:alat_id,updated_at=NOW() WHERE id=:id'); $s->execute([...$data,'id'=>$id]); return to_route('peminjaman.index')->with('berhasil','Data berhasil diperbarui.'); } catch(Throwable $error){report($error);return back()->withInput()->with('gagal','Data gagal diperbarui.');}
})->name('peminjaman.update');

Route::delete('/peminjaman/{id}', function (int $id) { try { $s=DB::connection()->getPdo()->prepare('DELETE FROM peminjaman_alat WHERE id=:id'); $s->execute(['id'=>$id]); return to_route('peminjaman.index')->with('berhasil','Data berhasil dihapus.'); } catch(Throwable $error){report($error);return to_route('peminjaman.index')->with('gagal','Data gagal dihapus.');} })->name('peminjaman.destroy');
