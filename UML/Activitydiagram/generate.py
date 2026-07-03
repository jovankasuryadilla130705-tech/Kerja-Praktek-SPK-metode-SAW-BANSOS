import os

output_file = "ActivityDiagrams_Output.md"

flows = []

# ==========================================
# FLOW 1
# ==========================================
flow1 = {
    "title": "ALUR 1 — Autentikasi (Login & Logout)",
    "narasi": "Proses autentikasi dimulai ketika pengguna (Admin, Staff, atau Camat) membuka halaman Login. Pengguna kemudian mengisi username dan password pada form yang disediakan lalu menekan tombol Submit. Sistem pertama-tama akan melakukan validasi untuk memastikan tidak ada field yang kosong; jika ada yang kosong, sistem akan menampilkan pesan error dan mengembalikan pengguna ke form. Selanjutnya, sistem melakukan pencarian pada tabel `users` di database berdasarkan username. Jika username tidak ditemukan, sistem mencatat status FAILED pada tabel `login_history` dan menampilkan pesan \"Akun tidak ditemukan\". Jika username ditemukan, sistem memverifikasi kesesuaian `password_hash`. Apabila password salah, kegagalan dicatat kembali ke `login_history` beserta pesan \"Password salah\". Jika berhasil, sistem mencatat status SUCCESS, membuat session aktif yang menyimpan ID dan role pengguna, kemudian mengarahkan pengguna ke halaman dashboard yang sesuai dengan rolenya (Admin, Staff, atau Camat). Saat pengguna ingin keluar, mereka mengklik tombol Logout, yang memicu sistem untuk menghapus session aktif dan mengembalikan pengguna ke halaman Login.",
    "plantuml": """@startuml
|#DAE8FC| Pengguna |
|#D5E8D4| Sistem |
|#FFF2CC| Database |

| Pengguna |
start
:Membuka halaman Login;
:Mengisi username & password lalu klik Submit;

| Sistem |
if (Apakah field kosong?) then (Ya)
  :Tampilkan error "Field tidak boleh kosong";
  | Pengguna |
  :Kembali ke form;
  detach
else (Tidak)
  | Sistem |
  :Query tabel users WHERE username = input;
  
  | Database |
  :Cari username di tabel users;
  
  | Sistem |
  if (Username ditemukan?) then (Tidak)
    | Database |
    :Catat log FAILED ke login_history;
    | Sistem |
    :Tampilkan "Akun tidak ditemukan";
    | Pengguna |
    :Kembali ke form;
    detach
  else (Ya)
    | Sistem |
    :Verifikasi password_hash;
    if (Password salah?) then (Ya)
      | Database |
      :Catat log FAILED ke login_history;
      | Sistem |
      :Tampilkan "Password salah";
      | Pengguna |
      :Kembali ke form;
      detach
    else (Tidak)
      | Database |
      :Catat log SUCCESS ke login_history;
      | Sistem |
      :Buat session (simpan user_id & role);
      :Redirect ke dashboard sesuai role;
    endif
  endif
endif

| Pengguna |
:Klik tombol "Logout";

| Sistem |
:Hapus session aktif;
:Redirect ke halaman Login;
stop
@enduml""",
    "xml_nodes": [
        {"id": "start", "type": "start", "col": 1, "text": ""},
        {"id": "a1", "type": "activity", "col": 1, "text": "Membuka halaman Login"},
        {"id": "a2", "type": "activity", "col": 1, "text": "Mengisi username & password\nklik Submit"},
        {"id": "d1", "type": "decision", "col": 2, "text": "Field\nkosong?"},
        {"id": "a3", "type": "activity", "col": 2, "text": "Tampilkan error"},
        {"id": "a4", "type": "activity", "col": 2, "text": "Query tabel users"},
        {"id": "a5", "type": "activity", "col": 3, "text": "Cari username"},
        {"id": "d2", "type": "decision", "col": 2, "text": "Ditemukan?"},
        {"id": "a6", "type": "activity", "col": 3, "text": "Catat log FAILED"},
        {"id": "a7", "type": "activity", "col": 2, "text": "Tampilkan Akun tidak ditemukan"},
        {"id": "a8", "type": "activity", "col": 2, "text": "Verifikasi password_hash"},
        {"id": "d3", "type": "decision", "col": 2, "text": "Password\nsalah?"},
        {"id": "a9", "type": "activity", "col": 3, "text": "Catat log FAILED"},
        {"id": "a10", "type": "activity", "col": 2, "text": "Tampilkan Password salah"},
        {"id": "a11", "type": "activity", "col": 3, "text": "Catat log SUCCESS"},
        {"id": "a12", "type": "activity", "col": 2, "text": "Buat session & Redirect"},
        {"id": "a13", "type": "activity", "col": 1, "text": "Klik tombol Logout"},
        {"id": "a14", "type": "activity", "col": 2, "text": "Hapus session aktif"},
        {"id": "a15", "type": "activity", "col": 2, "text": "Redirect ke halaman Login"},
        {"id": "end", "type": "end", "col": 2, "text": ""}
    ],
    "xml_edges": [
        {"src": "start", "dst": "a1", "label": ""},
        {"src": "a1", "dst": "a2", "label": ""},
        {"src": "a2", "dst": "d1", "label": ""},
        {"src": "d1", "dst": "a3", "label": "Ya"},
        {"src": "a3", "dst": "a2", "label": ""},
        {"src": "d1", "dst": "a4", "label": "Tidak"},
        {"src": "a4", "dst": "a5", "label": ""},
        {"src": "a5", "dst": "d2", "label": ""},
        {"src": "d2", "dst": "a6", "label": "Tidak"},
        {"src": "a6", "dst": "a7", "label": ""},
        {"src": "a7", "dst": "a2", "label": ""},
        {"src": "d2", "dst": "a8", "label": "Ya"},
        {"src": "a8", "dst": "d3", "label": ""},
        {"src": "d3", "dst": "a9", "label": "Ya"},
        {"src": "a9", "dst": "a10", "label": ""},
        {"src": "a10", "dst": "a2", "label": ""},
        {"src": "d3", "dst": "a11", "label": "Tidak"},
        {"src": "a11", "dst": "a12", "label": ""},
        {"src": "a12", "dst": "a13", "label": ""},
        {"src": "a13", "dst": "a14", "label": ""},
        {"src": "a14", "dst": "a15", "label": ""},
        {"src": "a15", "dst": "end", "label": ""}
    ]
}
flows.append(flow1)

# ==========================================
# FLOW 2
# ==========================================
flow2 = {
    "title": "ALUR 2 — Manajemen Profil & Keamanan",
    "narasi": "Alur manajemen profil dimulai saat pengguna mengakses menu Profil. Sistem melakukan query ke tabel `users` di database dan menampilkan data profil terkini. Pengguna memiliki dua opsi aksi: mengubah foto profil atau mengganti password. Jika memilih mengubah foto profil, pengguna mengunggah file gambar. Sistem kemudian memvalidasi format (harus .jpg atau .png) dan ukuran (maksimal 2MB). Jika tidak valid, muncul pesan error; jika valid, sistem menyimpan file, memperbarui field `foto_profil` di database, dan menampilkan notifikasi sukses. Di sisi lain, jika pengguna memilih mengganti password, mereka harus mengisi password lama, password baru, dan konfirmasi. Sistem pertama-tama memverifikasi kecocokan password lama dengan hash di database. Apabila cocok, sistem memvalidasi apakah password baru dan konfirmasi sama. Jika semua validasi terpenuhi, sistem akan melakukan hashing pada password baru, memperbarui field `password_hash` di database, dan memberikan notifikasi bahwa password berhasil diubah.",
    "plantuml": """@startuml
|#DAE8FC| Pengguna |
|#D5E8D4| Sistem |
|#FFF2CC| Database |

| Pengguna |
start
:Membuka menu Profil;

| Sistem |
:Query data profil;
| Database |
:Ambil data dari tabel users;
| Sistem |
:Tampilkan data profil;

| Pengguna |
fork
  :Memilih file gambar (Ubah Foto);
  :Klik Upload;
  | Sistem |
  if (Format & Ukuran Valid?) then (Tidak)
    :Tampilkan pesan error;
    | Pengguna |
    :Kembali ke form;
    detach
  else (Ya)
    | Sistem |
    :Simpan file ke server;
    | Database |
    :UPDATE foto_profil di tabel users;
    | Sistem |
    :Tampilkan "Foto profil diperbarui";
  endif

fork again
  | Pengguna |
  :Mengisi Form Ganti Password;
  | Sistem |
  :Verifikasi Password Lama;
  | Database |
  :Cek password_hash di tabel users;
  | Sistem |
  if (Password Lama cocok?) then (Tidak)
    :Tampilkan "Password lama salah";
    | Pengguna |
    :Kembali ke form;
    detach
  else (Ya)
    | Sistem |
    if (Password Baru == Konfirmasi?) then (Tidak)
      :Tampilkan "Konfirmasi tidak cocok";
      | Pengguna |
      :Kembali ke form;
      detach
    else (Ya)
      | Sistem |
      :Hash password baru;
      | Database |
      :UPDATE password_hash di tabel users;
      | Sistem |
      :Tampilkan "Password berhasil diubah";
    endif
  endif
end fork
stop
@enduml""",
    "xml_nodes": [
        {"id": "start", "type": "start", "col": 1, "text": ""},
        {"id": "a1", "type": "activity", "col": 1, "text": "Membuka menu Profil"},
        {"id": "a2", "type": "activity", "col": 2, "text": "Query data profil"},
        {"id": "a3", "type": "activity", "col": 3, "text": "Ambil data users"},
        {"id": "a4", "type": "activity", "col": 2, "text": "Tampilkan data profil"},
        {"id": "f1", "type": "activity", "col": 1, "text": "Ubah Foto Profil"},
        {"id": "d1", "type": "decision", "col": 2, "text": "File\nValid?"},
        {"id": "a5", "type": "activity", "col": 2, "text": "Tampilkan error file"},
        {"id": "a6", "type": "activity", "col": 2, "text": "Simpan file ke server"},
        {"id": "a7", "type": "activity", "col": 3, "text": "UPDATE foto_profil"},
        {"id": "a8", "type": "activity", "col": 2, "text": "Tampilkan sukses foto"},
        {"id": "f2", "type": "activity", "col": 1, "text": "Ganti Password"},
        {"id": "a9", "type": "activity", "col": 2, "text": "Verifikasi Pass Lama"},
        {"id": "a10", "type": "activity", "col": 3, "text": "Cek password_hash"},
        {"id": "d2", "type": "decision", "col": 2, "text": "Pass\nCocok?"},
        {"id": "a11", "type": "activity", "col": 2, "text": "Tampilkan Pass salah"},
        {"id": "d3", "type": "decision", "col": 2, "text": "Konfirm\nSama?"},
        {"id": "a12", "type": "activity", "col": 2, "text": "Tampilkan Konfirm beda"},
        {"id": "a13", "type": "activity", "col": 2, "text": "Hash password baru"},
        {"id": "a14", "type": "activity", "col": 3, "text": "UPDATE password_hash"},
        {"id": "a15", "type": "activity", "col": 2, "text": "Tampilkan sukses pass"},
        {"id": "end", "type": "end", "col": 2, "text": ""}
    ],
    "xml_edges": [
        {"src": "start", "dst": "a1", "label": ""},
        {"src": "a1", "dst": "a2", "label": ""},
        {"src": "a2", "dst": "a3", "label": ""},
        {"src": "a3", "dst": "a4", "label": ""},
        {"src": "a4", "dst": "f1", "label": "Opsi 1"},
        {"src": "a4", "dst": "f2", "label": "Opsi 2"},
        
        {"src": "f1", "dst": "d1", "label": ""},
        {"src": "d1", "dst": "a5", "label": "Tidak"},
        {"src": "a5", "dst": "f1", "label": ""},
        {"src": "d1", "dst": "a6", "label": "Ya"},
        {"src": "a6", "dst": "a7", "label": ""},
        {"src": "a7", "dst": "a8", "label": ""},
        {"src": "a8", "dst": "end", "label": ""},

        {"src": "f2", "dst": "a9", "label": ""},
        {"src": "a9", "dst": "a10", "label": ""},
        {"src": "a10", "dst": "d2", "label": ""},
        {"src": "d2", "dst": "a11", "label": "Tidak"},
        {"src": "a11", "dst": "f2", "label": ""},
        {"src": "d2", "dst": "d3", "label": "Ya"},
        {"src": "d3", "dst": "a12", "label": "Tidak"},
        {"src": "a12", "dst": "f2", "label": ""},
        {"src": "d3", "dst": "a13", "label": "Ya"},
        {"src": "a13", "dst": "a14", "label": ""},
        {"src": "a14", "dst": "a15", "label": ""},
        {"src": "a15", "dst": "end", "label": ""}
    ]
}
flows.append(flow2)

# ==========================================
# FLOW 3
# ==========================================
flow3 = {
    "title": "ALUR 3 — Akses Dashboard & Statistik",
    "narasi": "Alur akses dashboard dimulai saat pengguna (Admin, Staff, atau Camat) mengklik menu Dashboard. Sistem secara otomatis melakukan query ke database, khususnya pada tabel `classification_results`, untuk mengambil rekapitulasi data. Data yang dicari meliputi total warga yang telah terklasifikasi, jumlah yang memiliki status LAYAK, dan jumlah yang berstatus TIDAK LAYAK. Sistem lalu mengecek ketersediaan data tersebut. Jika belum ada data sama sekali, sistem akan menampilkan pesan \"Belum ada data klasifikasi\" dan menampilkan dashboard dalam keadaan kosong. Namun, jika data tersedia, sistem melanjutkan dengan menghitung persentase warga yang LAYAK dan TIDAK LAYAK. Berdasarkan perhitungan ini, sistem me-render komponen visual berupa Pie Chart untuk menunjukkan proporsi kelayakan, serta Bar Chart untuk melihat distribusi klasifikasi per periode atau kriteria. Ringkasan statistik dan grafik tersebut kemudian ditampilkan secara komprehensif di halaman Dashboard untuk dianalisis oleh pengguna.",
    "plantuml": """@startuml
|#DAE8FC| Pengguna |
|#D5E8D4| Sistem |
|#FFF2CC| Database |

| Pengguna |
start
:Klik menu "Dashboard";

| Sistem |
:Query rekapitulasi data;
| Database |
:Ambil dari classification_results;
| Sistem |
if (Data tersedia?) then (Tidak)
  :Tampilkan pesan "Belum ada data";
  :Tampilkan dashboard kosong;
else (Ya)
  :Hitung persentase LAYAK & TIDAK LAYAK;
  :Render Pie Chart (proporsi);
  :Render Bar Chart (distribusi);
  :Tampilkan ringkasan & grafik di Dashboard;
endif

| Pengguna |
:Melihat data statistik;
stop
@enduml""",
    "xml_nodes": [
        {"id": "start", "type": "start", "col": 1, "text": ""},
        {"id": "a1", "type": "activity", "col": 1, "text": "Klik menu Dashboard"},
        {"id": "a2", "type": "activity", "col": 2, "text": "Query rekapitulasi"},
        {"id": "a3", "type": "activity", "col": 3, "text": "Ambil data klasifikasi"},
        {"id": "d1", "type": "decision", "col": 2, "text": "Data\nada?"},
        {"id": "a4", "type": "activity", "col": 2, "text": "Tampilkan belum ada data"},
        {"id": "a5", "type": "activity", "col": 2, "text": "Hitung persentase"},
        {"id": "a6", "type": "activity", "col": 2, "text": "Render Pie Chart"},
        {"id": "a7", "type": "activity", "col": 2, "text": "Render Bar Chart"},
        {"id": "a8", "type": "activity", "col": 2, "text": "Tampilkan Dashboard"},
        {"id": "a9", "type": "activity", "col": 1, "text": "Melihat data statistik"},
        {"id": "end", "type": "end", "col": 1, "text": ""}
    ],
    "xml_edges": [
        {"src": "start", "dst": "a1", "label": ""},
        {"src": "a1", "dst": "a2", "label": ""},
        {"src": "a2", "dst": "a3", "label": ""},
        {"src": "a3", "dst": "d1", "label": ""},
        {"src": "d1", "dst": "a4", "label": "Tidak"},
        {"src": "a4", "dst": "a9", "label": ""},
        {"src": "d1", "dst": "a5", "label": "Ya"},
        {"src": "a5", "dst": "a6", "label": ""},
        {"src": "a6", "dst": "a7", "label": ""},
        {"src": "a7", "dst": "a8", "label": ""},
        {"src": "a8", "dst": "a9", "label": ""},
        {"src": "a9", "dst": "end", "label": ""}
    ]
}
flows.append(flow3)

# ==========================================
# FLOW 4
# ==========================================
flow4 = {
    "title": "ALUR 4 — Klasifikasi Bansos (Metode SAW) [ALUR UTAMA]",
    "narasi": "Proses klasifikasi Bansos diawali oleh Admin atau Staff yang membuka menu Klasifikasi Bansos dan memilih mode input data. Pada mode manual, pengguna mengisi form data warga dan melakukan validasi kelengkapan. Jika terdapat field kosong atau tipe tidak valid, sistem mengembalikan error. Pada mode import CSV, file CSV divalidasi struktur dan formatnya, kemudian diparsing ke memori. Setelah data tersedia, sistem mengambil bobot dari tabel `kriteria` dan nilai konversi dari `sub_kriteria`. Sistem lalu membangun matriks keputusan X untuk seluruh data. Matriks tersebut dinormalisasi (nilai benefit dibagi nilai maksimal, sedangkan nilai minimal dibagi cost). Nilai preferensi dihitung dengan mengalikan matriks ternormalisasi dengan bobot kriteria. Sistem mengevaluasi nilai preferensi terhadap threshold 0.50; jika lebih besar atau sama, status warga ditetapkan LAYAK, dan sebaliknya TIDAK LAYAK. Terakhir, sistem menyimpan hasil ke tabel `classification_results` dan menampilkan tabel daftar hasil klasifikasi beserta nilai dan status kelayakannya.",
    "plantuml": """@startuml
|#DAE8FC| Admin/Staff |
|#D5E8D4| Sistem |
|#FFF2CC| Database |

| Admin/Staff |
start
:Membuka menu Klasifikasi Bansos;
:Memilih mode input;

fork
  :Mode Manual: Isi form warga;
  :Klik Proses;
  | Sistem |
  if (Validasi form valid?) then (Tidak)
    :Tampilkan error spesifik;
    | Admin/Staff |
    :Kembali ke form;
    detach
  else (Ya)
  endif

fork again
  | Admin/Staff |
  :Mode Import CSV: Unggah file;
  | Sistem |
  if (Format & struktur valid?) then (Tidak)
    :Tampilkan error format;
    | Admin/Staff |
    :Kembali;
    detach
  else (Ya)
    | Sistem |
    :Parsing CSV ke memori;
  endif
end fork

| Sistem |
:Query bobot kriteria;
| Database |
:Ambil dari tabel kriteria;
| Sistem |
:Query nilai konversi;
| Database |
:Ambil dari tabel sub_kriteria;
| Sistem |
:Bangun matriks keputusan X;
:Normalisasi matriks r_ij;
:Hitung nilai preferensi V_i;
if (V_i >= 0.50?) then (Ya)
  :Set Status = LAYAK;
else (Tidak)
  :Set Status = TIDAK LAYAK;
endif
:INSERT hasil ke klasifikasi;
| Database |
:Simpan ke classification_results;
| Sistem |
:Tampilkan tabel hasil klasifikasi;
stop
@enduml""",
    "xml_nodes": [
        {"id": "start", "type": "start", "col": 1, "text": ""},
        {"id": "a1", "type": "activity", "col": 1, "text": "Buka Klasifikasi Bansos"},
        {"id": "a2", "type": "activity", "col": 1, "text": "Pilih mode input"},
        {"id": "f1", "type": "activity", "col": 1, "text": "Mode Manual (Isi form)"},
        {"id": "d1", "type": "decision", "col": 2, "text": "Form\nValid?"},
        {"id": "a3", "type": "activity", "col": 2, "text": "Tampilkan error form"},
        {"id": "f2", "type": "activity", "col": 1, "text": "Mode Import CSV"},
        {"id": "d2", "type": "decision", "col": 2, "text": "Format\nValid?"},
        {"id": "a4", "type": "activity", "col": 2, "text": "Tampilkan error CSV"},
        {"id": "a5", "type": "activity", "col": 2, "text": "Parsing CSV"},
        {"id": "a6", "type": "activity", "col": 2, "text": "Query kriteria & sub"},
        {"id": "a7", "type": "activity", "col": 3, "text": "Ambil data kriteria"},
        {"id": "a8", "type": "activity", "col": 2, "text": "Bangun & Normalisasi Matriks"},
        {"id": "a9", "type": "activity", "col": 2, "text": "Hitung Preferensi (V)"},
        {"id": "d3", "type": "decision", "col": 2, "text": "V >= 0.50?"},
        {"id": "a10", "type": "activity", "col": 2, "text": "Status: LAYAK"},
        {"id": "a11", "type": "activity", "col": 2, "text": "Status: TIDAK LAYAK"},
        {"id": "a12", "type": "activity", "col": 3, "text": "INSERT classification_results"},
        {"id": "a13", "type": "activity", "col": 2, "text": "Tampilkan hasil"},
        {"id": "end", "type": "end", "col": 2, "text": ""}
    ],
    "xml_edges": [
        {"src": "start", "dst": "a1", "label": ""},
        {"src": "a1", "dst": "a2", "label": ""},
        {"src": "a2", "dst": "f1", "label": "Manual"},
        {"src": "a2", "dst": "f2", "label": "Import"},
        
        {"src": "f1", "dst": "d1", "label": ""},
        {"src": "d1", "dst": "a3", "label": "Tidak"},
        {"src": "a3", "dst": "f1", "label": ""},
        {"src": "d1", "dst": "a6", "label": "Ya"},

        {"src": "f2", "dst": "d2", "label": ""},
        {"src": "d2", "dst": "a4", "label": "Tidak"},
        {"src": "a4", "dst": "f2", "label": ""},
        {"src": "d2", "dst": "a5", "label": "Ya"},
        {"src": "a5", "dst": "a6", "label": ""},

        {"src": "a6", "dst": "a7", "label": ""},
        {"src": "a7", "dst": "a8", "label": ""},
        {"src": "a8", "dst": "a9", "label": ""},
        {"src": "a9", "dst": "d3", "label": ""},
        {"src": "d3", "dst": "a10", "label": "Ya"},
        {"src": "d3", "dst": "a11", "label": "Tidak"},
        {"src": "a10", "dst": "a12", "label": ""},
        {"src": "a11", "dst": "a12", "label": ""},
        {"src": "a12", "dst": "a13", "label": ""},
        {"src": "a13", "dst": "end", "label": ""}
    ]
}
flows.append(flow4)

# ==========================================
# FLOW 5
# ==========================================
flow5 = {
    "title": "ALUR 5 — Manajemen Data Warga (Edit & Hapus)",
    "narasi": "Proses manajemen data warga dimulai saat Admin atau Staff membuka menu Riwayat Data Warga. Sistem menampilkan daftar data dengan menggabungkan tabel `classification_results` dan `warga`. Pengguna dapat memfilter data dengan fungsi pencarian. Setelah data tampil, pengguna dapat memilih aksi Edit atau Hapus. Jika memilih Edit, form akan terisi dengan data lama warga. Pengguna mengubah data lalu menyimpannya; sistem memvalidasi perubahan tersebut, dan bila valid, sistem meng-update tabel `warga`, menghitung ulang nilai SAW, meng-update tabel `classification_results`, dan menampilkan notifikasi sukses. Jika pengguna memilih aksi Hapus, sistem akan menampilkan dialog konfirmasi terlebih dahulu. Apabila dikonfirmasi, sistem menghapus rekaman terkait pada tabel `classification_results` (dan bergantung pada aturan cascade, menghapus data di tabel warga jika diatur demikian). Setelah aksi selesai, daftar data akan di-refresh beserta kemunculan notifikasi kesuksesan proses.",
    "plantuml": """@startuml
|#DAE8FC| Admin/Staff |
|#D5E8D4| Sistem |
|#FFF2CC| Database |

| Admin/Staff |
start
:Membuka menu Riwayat Data Warga;
| Sistem |
:Query data hasil klasifikasi JOIN warga;
| Database |
:Ambil data;
| Sistem |
:Tampilkan daftar data;

| Admin/Staff |
:Mencari data (opsional);
:Pilih aksi pada baris data;

fork
  :Klik "Edit";
  :Ubah data & klik Simpan;
  | Sistem |
  if (Validasi perubahan?) then (Tidak valid)
    :Tampilkan error;
    | Admin/Staff |
    :Kembali ke form edit;
    detach
  else (Valid)
    | Sistem |
    :Recalculate nilai SAW;
    | Database |
    :UPDATE tabel warga & klasifikasi;
    | Sistem |
    :Notifikasi "Data diperbarui";
  endif

fork again
  | Admin/Staff |
  :Klik "Hapus";
  | Sistem |
  :Tampilkan konfirmasi;
  if (Yakin hapus?) then (Batal)
    | Admin/Staff |
    :Kembali ke daftar;
    detach
  else (Ya)
    | Database |
    :DELETE record dari klasifikasi;
    | Sistem |
    :Notifikasi "Data dihapus";
  endif
end fork

| Sistem |
:Refresh daftar data;
stop
@enduml""",
    "xml_nodes": [
        {"id": "start", "type": "start", "col": 1, "text": ""},
        {"id": "a1", "type": "activity", "col": 1, "text": "Membuka Riwayat Warga"},
        {"id": "a2", "type": "activity", "col": 2, "text": "Query data"},
        {"id": "a3", "type": "activity", "col": 3, "text": "Ambil data JOIN"},
        {"id": "a4", "type": "activity", "col": 2, "text": "Tampilkan daftar"},
        {"id": "a5", "type": "activity", "col": 1, "text": "Pilih aksi baris"},
        
        {"id": "f1", "type": "activity", "col": 1, "text": "Aksi Edit: Ubah & Simpan"},
        {"id": "d1", "type": "decision", "col": 2, "text": "Valid?"},
        {"id": "a6", "type": "activity", "col": 2, "text": "Tampilkan error edit"},
        {"id": "a7", "type": "activity", "col": 2, "text": "Recalculate SAW"},
        {"id": "a8", "type": "activity", "col": 3, "text": "UPDATE warga & klasifikasi"},
        
        {"id": "f2", "type": "activity", "col": 1, "text": "Aksi Hapus: Klik Hapus"},
        {"id": "d2", "type": "decision", "col": 2, "text": "Konfirmasi?"},
        {"id": "a9", "type": "activity", "col": 3, "text": "DELETE dari klasifikasi"},
        
        {"id": "a10", "type": "activity", "col": 2, "text": "Tampilkan Notifikasi"},
        {"id": "a11", "type": "activity", "col": 2, "text": "Refresh daftar"},
        {"id": "end", "type": "end", "col": 2, "text": ""}
    ],
    "xml_edges": [
        {"src": "start", "dst": "a1", "label": ""},
        {"src": "a1", "dst": "a2", "label": ""},
        {"src": "a2", "dst": "a3", "label": ""},
        {"src": "a3", "dst": "a4", "label": ""},
        {"src": "a4", "dst": "a5", "label": ""},
        
        {"src": "a5", "dst": "f1", "label": "Edit"},
        {"src": "a5", "dst": "f2", "label": "Hapus"},
        
        {"src": "f1", "dst": "d1", "label": ""},
        {"src": "d1", "dst": "a6", "label": "Tidak"},
        {"src": "a6", "dst": "f1", "label": ""},
        {"src": "d1", "dst": "a7", "label": "Ya"},
        {"src": "a7", "dst": "a8", "label": ""},
        {"src": "a8", "dst": "a10", "label": ""},
        
        {"src": "f2", "dst": "d2", "label": ""},
        {"src": "d2", "dst": "a5", "label": "Batal"},
        {"src": "d2", "dst": "a9", "label": "Ya"},
        {"src": "a9", "dst": "a10", "label": ""},
        
        {"src": "a10", "dst": "a11", "label": ""},
        {"src": "a11", "dst": "end", "label": ""}
    ]
}
flows.append(flow5)

# ==========================================
# FLOW 6
# ==========================================
flow6 = {
    "title": "ALUR 6 — Ekspor Laporan Excel",
    "narasi": "Alur pengeksporan laporan diinisiasi oleh pengguna (Admin, Staff, atau Camat) melalui halaman Laporan atau Riwayat data. Pengguna dapat secara opsional mengatur filter berdasarkan rentang tanggal atau status kelayakan, kemudian menekan tombol Ekspor Excel. Sistem menanggapi dengan melakukan query ke database pada tabel `classification_results` dan `warga` sesuai filter yang diterapkan. Jika hasil pencarian tidak menemukan data (kosong), sistem akan menampilkan peringatan bahwa tidak ada data untuk diekspor dan alur berhenti. Apabila data tersedia, sistem memproses pembuatan file Excel menggunakan pustaka OpenPyXL. Prosesnya meliputi pembuatan worksheet baru, penulisan baris header (No, NIK, Nama, Nilai V, Status, Tanggal), dan pengisian baris data secara iteratif. Sistem juga menerapkan pengaturan formatting dasar seperti huruf tebal untuk header, penambahan border, serta penyesuaian lebar kolom otomatis. File Excel yang telah selesai di-generate kemudian dikirimkan sebagai HTTP response, sehingga browser pengguna secara otomatis mengunduhnya.",
    "plantuml": """@startuml
|#DAE8FC| Pengguna |
|#D5E8D4| Sistem |
|#FFF2CC| Database |

| Pengguna |
start
:Membuka halaman Laporan;
:Mengatur filter (opsional);
:Klik "Ekspor Excel";

| Sistem |
:Query data dengan filter;
| Database |
:Ambil data (classification_results JOIN warga);
| Sistem |
if (Hasil kosong?) then (Ya)
  :Tampilkan notifikasi "Tidak ada data";
  stop
else (Tidak)
  :Generate file Excel (OpenPyXL);
  :Tulis header & isi baris data;
  :Terapkan formatting & auto-fit;
  :Kirim response HTTP attachment;
endif

| Pengguna |
:Browser mengunduh file .xlsx;
stop
@enduml""",
    "xml_nodes": [
        {"id": "start", "type": "start", "col": 1, "text": ""},
        {"id": "a1", "type": "activity", "col": 1, "text": "Buka Laporan & Atur Filter"},
        {"id": "a2", "type": "activity", "col": 1, "text": "Klik Ekspor Excel"},
        {"id": "a3", "type": "activity", "col": 2, "text": "Query data berfilter"},
        {"id": "a4", "type": "activity", "col": 3, "text": "Ambil data DB"},
        {"id": "d1", "type": "decision", "col": 2, "text": "Kosong?"},
        {"id": "a5", "type": "activity", "col": 2, "text": "Tampilkan \"Tidak ada data\""},
        {"id": "a6", "type": "activity", "col": 2, "text": "Generate Excel (OpenPyXL)"},
        {"id": "a7", "type": "activity", "col": 2, "text": "Formatting Data"},
        {"id": "a8", "type": "activity", "col": 2, "text": "Kirim HTTP Response"},
        {"id": "a9", "type": "activity", "col": 1, "text": "Browser unduh file .xlsx"},
        {"id": "end", "type": "end", "col": 1, "text": ""}
    ],
    "xml_edges": [
        {"src": "start", "dst": "a1", "label": ""},
        {"src": "a1", "dst": "a2", "label": ""},
        {"src": "a2", "dst": "a3", "label": ""},
        {"src": "a3", "dst": "a4", "label": ""},
        {"src": "a4", "dst": "d1", "label": ""},
        {"src": "d1", "dst": "a5", "label": "Ya"},
        {"src": "a5", "dst": "end", "label": ""},
        {"src": "d1", "dst": "a6", "label": "Tidak"},
        {"src": "a6", "dst": "a7", "label": ""},
        {"src": "a7", "dst": "a8", "label": ""},
        {"src": "a8", "dst": "a9", "label": ""},
        {"src": "a9", "dst": "end", "label": ""}
    ]
}
flows.append(flow6)

# ==========================================
# FLOW 7
# ==========================================
flow7 = {
    "title": "ALUR 7 — Pengaturan SPK (Kriteria & Sub Kriteria)",
    "narasi": "Alur pengaturan SPK merupakan hak eksklusif Admin, dimulai dengan mengakses menu Pengaturan SPK. Admin dapat memilih antara sub-menu Manajemen Kriteria atau Manajemen Sub Kriteria. Pada Manajemen Kriteria, sistem menampilkan daftar kriteria dari database. Jika Admin ingin menambah atau mengedit kriteria, ia akan mengisi form (nama, bobot, tipe). Sistem kemudian memvalidasi bahwa nilai bobot bersifat numerik, di antara 0.0 sampai 1.0, dan total keseluruhan bobot kriteria tidak melebihi 1.0. Bila validasi gagal, muncul peringatan spesifik. Bila sukses, record akan dimasukkan atau diperbarui di tabel `kriteria`. Jika memilih Hapus, sistem terlebih dahulu memastikan tidak ada relasi di tabel `sub_kriteria`; jika kriteria masih digunakan, penghapusan ditolak. Proses serupa diterapkan pada Manajemen Sub Kriteria, di mana Admin mengelola data konversi nilai sub kriteria berdasarkan parent kriteria_id yang divalidasi keamanannya sebelum disimpan atau dihapus pada tabel `sub_kriteria`.",
    "plantuml": """@startuml
|#DAE8FC| Admin |
|#D5E8D4| Sistem |
|#FFF2CC| Database |

| Admin |
start
:Membuka menu Pengaturan SPK;
:Memilih Kriteria / Sub Kriteria;
| Sistem |
:Tampilkan daftar (READ database);

| Admin |
:Pilih Aksi (Tambah/Edit/Hapus);

fork
  :Tambah / Edit Kriteria;
  :Submit Form;
  | Sistem |
  if (Validasi bobot numerik & total <= 1?) then (Tidak valid)
    :Tampilkan error;
    | Admin |
    :Kembali ke form;
    detach
  else (Valid)
    | Database |
    :INSERT / UPDATE kriteria atau sub_kriteria;
    | Sistem |
    :Notifikasi berhasil;
  endif

fork again
  | Admin |
  :Klik Hapus;
  | Sistem |
  :Tampilkan konfirmasi;
  if (Konfirmasi?) then (Ya)
    | Database |
    :Cek relasi kriteria di sub_kriteria;
    | Sistem |
    if (Ada relasi?) then (Ya)
      :Tampilkan "Kriteria digunakan";
      detach
    else (Tidak)
      | Database |
      :DELETE dari tabel terkait;
      | Sistem |
      :Notifikasi dihapus;
    endif
  else (Batal)
    | Admin |
    :Kembali;
    detach
  endif
end fork

| Sistem |
:Refresh daftar;
stop
@enduml""",
    "xml_nodes": [
        {"id": "start", "type": "start", "col": 1, "text": ""},
        {"id": "a1", "type": "activity", "col": 1, "text": "Buka Pengaturan SPK"},
        {"id": "a2", "type": "activity", "col": 2, "text": "Tampilkan daftar (READ DB)"},
        {"id": "a3", "type": "activity", "col": 1, "text": "Pilih Aksi Kriteria"},
        
        {"id": "f1", "type": "activity", "col": 1, "text": "Submit Tambah/Edit"},
        {"id": "d1", "type": "decision", "col": 2, "text": "Valid\nBobot?"},
        {"id": "a4", "type": "activity", "col": 2, "text": "Tampilkan error form"},
        {"id": "a5", "type": "activity", "col": 3, "text": "INSERT/UPDATE DB"},
        
        {"id": "f2", "type": "activity", "col": 1, "text": "Klik Hapus"},
        {"id": "d2", "type": "decision", "col": 2, "text": "Yakin?"},
        {"id": "a6", "type": "activity", "col": 3, "text": "Cek relasi child"},
        {"id": "d3", "type": "decision", "col": 2, "text": "Ada\nRelasi?"},
        {"id": "a7", "type": "activity", "col": 2, "text": "Tolak hapus (Digunakan)"},
        {"id": "a8", "type": "activity", "col": 3, "text": "DELETE dari DB"},
        
        {"id": "a9", "type": "activity", "col": 2, "text": "Notifikasi Sukses"},
        {"id": "a10", "type": "activity", "col": 2, "text": "Refresh daftar"},
        {"id": "end", "type": "end", "col": 2, "text": ""}
    ],
    "xml_edges": [
        {"src": "start", "dst": "a1", "label": ""},
        {"src": "a1", "dst": "a2", "label": ""},
        {"src": "a2", "dst": "a3", "label": ""},
        
        {"src": "a3", "dst": "f1", "label": "Simpan"},
        {"src": "a3", "dst": "f2", "label": "Hapus"},
        
        {"src": "f1", "dst": "d1", "label": ""},
        {"src": "d1", "dst": "a4", "label": "Tidak"},
        {"src": "a4", "dst": "f1", "label": ""},
        {"src": "d1", "dst": "a5", "label": "Ya"},
        {"src": "a5", "dst": "a9", "label": ""},
        
        {"src": "f2", "dst": "d2", "label": ""},
        {"src": "d2", "dst": "a3", "label": "Batal"},
        {"src": "d2", "dst": "a6", "label": "Ya"},
        {"src": "a6", "dst": "d3", "label": ""},
        {"src": "d3", "dst": "a7", "label": "Ya"},
        {"src": "d3", "dst": "a8", "label": "Tidak"},
        {"src": "a7", "dst": "a3", "label": ""},
        {"src": "a8", "dst": "a9", "label": ""},
        
        {"src": "a9", "dst": "a10", "label": ""},
        {"src": "a10", "dst": "end", "label": ""}
    ]
}
flows.append(flow7)

# ==========================================
# FLOW 8
# ==========================================
flow8 = {
    "title": "ALUR 8 — Manajemen Akun (Khusus Admin)",
    "narasi": "Fitur manajemen pengguna hanya diakses oleh Admin. Admin memulai dengan membuka menu Manajemen Akun. Sistem menarik data akun terkini dari tabel `users` untuk ditampilkan. Saat Admin menambah akun baru, ia mengisi detail seperti username, role, dan password. Sistem akan memvalidasi apakah username tersebut belum digunakan. Jika lolos validasi, password diamankan dengan hashing (menggunakan bcrypt/Werkzeug) sebelum dieksekusi INSERT ke database dengan status `is_active` secara default adalah True. Saat Admin melakukan edit pada akun yang sudah ada, ia bisa merubah nama atau role. Jika field password baru diisi, sistem me-hash password tersebut dan memperbaruinya; jika dibiarkan kosong, password lama tetap dipertahankan sebelum UPDATE dilakukan pada tabel `users`. Fitur terakhir adalah menonaktifkan atau mengaktifkan akun melalui tombol toggle. Admin akan diminta memberikan konfirmasi pada dialog; jika menyetujui, sistem melakukan UPDATE untuk membalik nilai boolean `is_active` pada database, lalu me-refresh tabel data akun secara otomatis.",
    "plantuml": """@startuml
|#DAE8FC| Admin |
|#D5E8D4| Sistem |
|#FFF2CC| Database |

| Admin |
start
:Buka menu Manajemen Akun;
| Sistem |
:Tampilkan daftar users (READ);

| Admin |
:Pilih aksi;

fork
  :Tambah Akun Baru (Isi form);
  | Sistem |
  if (Username sudah ada?) then (Ya)
    :Tampilkan error spesifik;
    | Admin |
    :Kembali ke form;
    detach
  else (Tidak)
    | Sistem |
    :Hash password;
    | Database |
    :INSERT ke tabel users;
  endif

fork again
  | Admin |
  :Edit Akun;
  :Ubah role/password;
  | Sistem |
  if (Password diisi?) then (Ya)
    :Hash password baru;
  else (Tidak)
    :Lewati hashing;
  endif
  | Database |
  :UPDATE record di tabel users;

fork again
  | Admin |
  :Klik Toggle Status (Aktif/Nonaktif);
  | Sistem |
  :Tampilkan konfirmasi;
  if (Yakin?) then (Ya)
    | Database |
    :UPDATE field is_active;
  else (Tidak)
    | Admin |
    :Batal, kembali;
    detach
  endif
end fork

| Sistem |
:Tampilkan Notifikasi;
:Refresh daftar akun;
stop
@enduml""",
    "xml_nodes": [
        {"id": "start", "type": "start", "col": 1, "text": ""},
        {"id": "a1", "type": "activity", "col": 1, "text": "Buka Manajemen Akun"},
        {"id": "a2", "type": "activity", "col": 2, "text": "Tampilkan daftar (READ DB)"},
        {"id": "a3", "type": "activity", "col": 1, "text": "Pilih Aksi Akun"},
        
        {"id": "f1", "type": "activity", "col": 1, "text": "Tambah Akun Baru"},
        {"id": "d1", "type": "decision", "col": 2, "text": "Username\nAda?"},
        {"id": "a4", "type": "activity", "col": 2, "text": "Tampilkan error username"},
        {"id": "a5", "type": "activity", "col": 2, "text": "Hash password"},
        {"id": "a6", "type": "activity", "col": 3, "text": "INSERT ke tabel users"},
        
        {"id": "f2", "type": "activity", "col": 1, "text": "Edit Akun"},
        {"id": "d2", "type": "decision", "col": 2, "text": "Pass\nDiisi?"},
        {"id": "a7", "type": "activity", "col": 2, "text": "Hash pass baru"},
        {"id": "a8", "type": "activity", "col": 3, "text": "UPDATE tabel users"},
        
        {"id": "f3", "type": "activity", "col": 1, "text": "Toggle Aktif/Nonaktif"},
        {"id": "d3", "type": "decision", "col": 2, "text": "Yakin?"},
        {"id": "a9", "type": "activity", "col": 3, "text": "UPDATE is_active"},
        
        {"id": "a10", "type": "activity", "col": 2, "text": "Tampilkan Notifikasi"},
        {"id": "a11", "type": "activity", "col": 2, "text": "Refresh daftar akun"},
        {"id": "end", "type": "end", "col": 2, "text": ""}
    ],
    "xml_edges": [
        {"src": "start", "dst": "a1", "label": ""},
        {"src": "a1", "dst": "a2", "label": ""},
        {"src": "a2", "dst": "a3", "label": ""},
        
        {"src": "a3", "dst": "f1", "label": "Tambah"},
        {"src": "a3", "dst": "f2", "label": "Edit"},
        {"src": "a3", "dst": "f3", "label": "Toggle"},
        
        {"src": "f1", "dst": "d1", "label": ""},
        {"src": "d1", "dst": "a4", "label": "Ya"},
        {"src": "a4", "dst": "f1", "label": ""},
        {"src": "d1", "dst": "a5", "label": "Tidak"},
        {"src": "a5", "dst": "a6", "label": ""},
        {"src": "a6", "dst": "a10", "label": ""},
        
        {"src": "f2", "dst": "d2", "label": ""},
        {"src": "d2", "dst": "a7", "label": "Ya"},
        {"src": "d2", "dst": "a8", "label": "Tidak"},
        {"src": "a7", "dst": "a8", "label": ""},
        {"src": "a8", "dst": "a10", "label": ""},
        
        {"src": "f3", "dst": "d3", "label": ""},
        {"src": "d3", "dst": "a3", "label": "Batal"},
        {"src": "d3", "dst": "a9", "label": "Ya"},
        {"src": "a9", "dst": "a10", "label": ""},
        
        {"src": "a10", "dst": "a11", "label": ""},
        {"src": "a11", "dst": "end", "label": ""}
    ]
}
flows.append(flow8)

# ==========================================
# GENERATE XML DRAW.IO HELPER
# ==========================================
def generate_drawio_xml(flow_num, nodes, edges):
    xml_header = f'''<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1654" pageHeight="1169" math="0" shadow="0">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <mxCell id="A{flow_num}_container" value="" style="swimlane;startSize=0;childLayout=stackLayout;horizontal=1;horizontalStack=1;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;" vertex="1" parent="1">
      <mxGeometry x="0" y="0" width="780" height="{max(1000, len(nodes)*100)}" as="geometry"/>
    </mxCell>
    <mxCell id="A{flow_num}_col1" value="Pengguna/Aktor" style="swimlane;whiteSpace=wrap;html=1;" vertex="1" parent="A{flow_num}_container">
      <mxGeometry x="0" y="0" width="260" height="{max(1000, len(nodes)*100)}" as="geometry"/>
    </mxCell>
    <mxCell id="A{flow_num}_col2" value="Sistem" style="swimlane;whiteSpace=wrap;html=1;" vertex="1" parent="A{flow_num}_container">
      <mxGeometry x="260" y="0" width="260" height="{max(1000, len(nodes)*100)}" as="geometry"/>
    </mxCell>
    <mxCell id="A{flow_num}_col3" value="Database" style="swimlane;whiteSpace=wrap;html=1;" vertex="1" parent="A{flow_num}_container">
      <mxGeometry x="520" y="0" width="260" height="{max(1000, len(nodes)*100)}" as="geometry"/>
    </mxCell>'''

    xml_elements = ""
    # Place nodes sequentially by Y
    y_counters = {1: 80, 2: 80, 3: 80}
    # To make layout simple, we assign a sequential row counter overall to avoid overlaps across columns
    current_y = 100
    
    node_geometry = {}
    for i, node in enumerate(nodes):
        node_id = f"A{flow_num}_{node['id']}"
        parent = f"A{flow_num}_col{node['col']}"
        
        if node['type'] == 'start':
            style = "ellipse;aspect=fixed;fillColor=#000000;strokeColor=#000000;"
            w, h = 30, 30
            x = 115
        elif node['type'] == 'end':
            style = "ellipse;aspect=fixed;fillColor=#000000;strokeColor=#000000;double=1;"
            w, h = 30, 30
            x = 115
        elif node['type'] == 'decision':
            style = "rhombus;whiteSpace=wrap;html=1;"
            w, h = 80, 80
            x = 90
        else: # activity
            style = "rounded=1;whiteSpace=wrap;html=1;arcSize=50;"
            w, h = 180, 50
            x = 40
            
        y = current_y
        current_y += 100
        node_geometry[node['id']] = {"x": x, "y": y, "col": node['col']}
        
        val_escaped = node['text'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
        xml_elements += f'''
    <mxCell id="{node_id}" value="{val_escaped}" style="{style}" vertex="1" parent="{parent}">
      <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>
    </mxCell>'''

    for i, edge in enumerate(edges):
        edge_id = f"A{flow_num}_edge_{i}"
        src_id = f"A{flow_num}_{edge['src']}"
        dst_id = f"A{flow_num}_{edge['dst']}"
        val_escaped = edge['label'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
        
        # Edge styling based on routing
        src_col = [n['col'] for n in nodes if n['id'] == edge['src']][0]
        dst_col = [n['col'] for n in nodes if n['id'] == edge['dst']][0]
        
        if src_col != dst_col:
            # Cross-column routing
            exitX = "1" if src_col < dst_col else "0"
            entryX = "0" if src_col < dst_col else "1"
            style = f"edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX={exitX};exitY=0.5;entryX={entryX};entryY=0.5;"
        else:
            style = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"
            
        xml_elements += f'''
    <mxCell id="{edge_id}" value="{val_escaped}" style="{style}" edge="1" parent="1" source="{src_id}" target="{dst_id}">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>'''

    xml_footer = '''
  </root>
</mxGraphModel>'''
    
    return xml_header + xml_elements + xml_footer

# ==========================================
# WRITE TO FILE
# ==========================================
with open(output_file, 'w', encoding='utf-8') as f:
    for i, flow in enumerate(flows):
        f.write(f"### {flow['title']}\n\n")
        f.write(f"**Narasi:**\n{flow['narasi']}\n\n")
        f.write("**Format A — PlantUML:**\n```plantuml\n")
        f.write(f"{flow['plantuml']}\n```\n\n")
        f.write("**Format B — XML draw.io:**\n```xml\n")
        
        xml_content = generate_drawio_xml(i+1, flow['xml_nodes'], flow['xml_edges'])
        f.write(f"{xml_content}\n```\n\n")
        f.write("---\n\n")
