# Kumpulan Activity Diagram — Sistem SPK Klasifikasi Bansos (Metode SAW)
### Kecamatan Pondok Aren, Kota Tangerang Selatan

> **Cara Penggunaan:** Salin kode PlantUML di bawah setiap diagram, lalu buka di **[PlantText.com](https://www.planttext.com/)** atau di **Draw.io** melalui `Extras > Edit Diagram > pilih format PlantUML`.

---
---

## 1. Activity Diagram: Login & Logout
**Aktor:** Admin, Staff, Camat
**Rute Sistem:** `/` (GET), `/login` (POST), `/logout` (GET)
**Deskripsi:** Proses autentikasi pengguna untuk masuk dan keluar dari sistem. Aktor Login dan Logout adalah sama (Admin, Staff, Camat), sehingga dijadikan satu diagram.

```plantuml
@startuml
skinparam DefaultFontName Arial
skinparam DefaultFontSize 12
skinparam ActivityBackgroundColor #FEFECE
skinparam ActivityBorderColor #A80036
skinparam ActivityDiamondBackgroundColor #FEFECE
skinparam ActivityDiamondBorderColor #A80036
skinparam SwimlaneBorderColor #333333
skinparam SwimlaneTitleBackgroundColor #E2E2F0
skinparam ConditionEndStyle hline

|Pengguna (Admin / Staff / Camat)|
start
:Membuka URL aplikasi;

|Sistem (Web Application)|
if (Sudah Login?) then (Ya)
  :Redirect ke halaman Dashboard;
else (Tidak)
  :Menampilkan form Login;
  |Pengguna (Admin / Staff / Camat)|
  :Menginput username & password;
  :Menekan tombol "Login";
  |Database|
  :Mencari data pengguna\nberdasarkan username;
  :Mencocokkan hash password;
  |Sistem (Web Application)|
  if (Kredensial Valid & Aktif?) then (Tidak)
    :Menampilkan pesan\n"Username/Password salah";
    |Pengguna (Admin / Staff / Camat)|
    :Membaca pesan error;
    stop
  else (Ya)
    |Database|
    :Mencatat riwayat login\n(waktu, IP, browser);
    |Sistem (Web Application)|
    :Membuat sesi (session) pengguna;
    :Redirect ke halaman Dashboard;
    |Pengguna (Admin / Staff / Camat)|
    :Melihat Dashboard;
    :Menekan tombol "Logout";
    |Sistem (Web Application)|
    :Menghapus session pengguna;
    :Redirect ke halaman Login;
    stop
  endif
endif
@enduml
```

---

## 2. Activity Diagram: Dashboard Statistik
**Aktor:** Admin, Staff, Camat
**Rute Sistem:** `/dashboard` (GET)
**Deskripsi:** Proses menampilkan ringkasan statistik hasil klasifikasi bansos berupa kartu angka, grafik pie distribusi kelayakan, dan grafik bar per kelurahan.

```plantuml
@startuml
skinparam DefaultFontName Arial
skinparam DefaultFontSize 12
skinparam ActivityBackgroundColor #FEFECE
skinparam ActivityBorderColor #A80036
skinparam ActivityDiamondBackgroundColor #FEFECE
skinparam ActivityDiamondBorderColor #A80036
skinparam SwimlaneBorderColor #333333
skinparam SwimlaneTitleBackgroundColor #E2E2F0
skinparam ConditionEndStyle hline

|Pengguna (Admin / Staff / Camat)|
start
:Membuka halaman Dashboard;

|Sistem (Web Application)|
if (Sudah Login?) then (Tidak)
  :Redirect ke halaman Login;
  stop
else (Ya)
  |Database|
  :Menghitung total data warga;
  :Menghitung jumlah "Layak"\ndan "Tidak Layak";
  :Mengambil data per kelurahan;
  |Sistem (Web Application)|
  :Memproses data untuk\ngrafik Pie & Bar Chart;
  :Menampilkan halaman Dashboard\n(kartu statistik & grafik);
  |Pengguna (Admin / Staff / Camat)|
  :Membaca statistik dan grafik;
  stop
endif
@enduml
```

---

## 3. Activity Diagram: Klasifikasi Data Bansos (Input Manual)
**Aktor:** Admin, Staff
**Rute Sistem:** `/classification` (GET, POST)
**Deskripsi:** Proses menginput data warga satu per satu melalui form, menghitung skor SAW, dan menyimpan hasilnya ke database.

```plantuml
@startuml
skinparam DefaultFontName Arial
skinparam DefaultFontSize 12
skinparam ActivityBackgroundColor #FEFECE
skinparam ActivityBorderColor #A80036
skinparam ActivityDiamondBackgroundColor #FEFECE
skinparam ActivityDiamondBorderColor #A80036
skinparam SwimlaneBorderColor #333333
skinparam SwimlaneTitleBackgroundColor #E2E2F0
skinparam ConditionEndStyle hline

|Pengguna (Admin / Staff)|
start
:Membuka menu Klasifikasi;

|Sistem (Web Application)|
:Menampilkan form Input Manual\n(data warga & pilihan kriteria);

|Pengguna (Admin / Staff)|
:Mengisi data identitas warga\n(NIK, Nama, Alamat, dll.);
:Memilih nilai untuk\nsetiap kriteria (C1-C7);
:Menekan tombol "Hitung Manual";

|Sistem (Web Application)|
:Memvalidasi NIK (16 digit)\ndan kelengkapan semua kriteria;
if (Validasi Berhasil?) then (Tidak)
  :Menampilkan pesan error;
  |Pengguna (Admin / Staff)|
  :Membaca pesan error;
  stop
else (Ya)
  :Mengambil data historis\ndari database untuk normalisasi;
  :Menghitung normalisasi\nmatriks SAW (R = nilai / max);
  :Menghitung skor akhir\n(SAW = Σ bobot × R);
  :Membandingkan skor\ndengan threshold (≥ 0.50 = Layak);
  :Menghasilkan teks alasan\nkelayakan otomatis;
  |Database|
  :Menyimpan record baru ke\ntabel classification_results;
  |Sistem (Web Application)|
  :Redirect ke halaman Riwayat;
  |Pengguna (Admin / Staff)|
  :Melihat hasil klasifikasi\ndi tabel Riwayat;
  stop
endif
@enduml
```

---

## 4. Activity Diagram: Klasifikasi Data Bansos (Import Excel / CSV)
**Aktor:** Admin, Staff
**Rute Sistem:** `/classification` (POST dengan file upload)
**Deskripsi:** Proses mengunggah file Excel atau CSV berisi banyak data warga sekaligus untuk diproses secara massal (batch).

```plantuml
@startuml
skinparam DefaultFontName Arial
skinparam DefaultFontSize 12
skinparam ActivityBackgroundColor #FEFECE
skinparam ActivityBorderColor #A80036
skinparam ActivityDiamondBackgroundColor #FEFECE
skinparam ActivityDiamondBorderColor #A80036
skinparam SwimlaneBorderColor #333333
skinparam SwimlaneTitleBackgroundColor #E2E2F0
skinparam ConditionEndStyle hline

|Pengguna (Admin / Staff)|
start
:Membuka menu Klasifikasi;

|Sistem (Web Application)|
:Menampilkan tombol\nUnggah File (Excel/CSV);

|Pengguna (Admin / Staff)|
:Memilih file Excel/CSV\nberisi data warga;
:Menekan tombol\n"Upload & Proses";

|Sistem (Web Application)|
:Memvalidasi format file\n(hanya .csv, .xls, .xlsx);
if (Format Valid?) then (Tidak)
  :Menampilkan pesan\nerror format file;
  stop
else (Ya)
  :Membaca file ke\nDataFrame (pandas);
  :Memproses setiap baris data;
  if (NIK/KK 16 Digit &\nKriteria Cocok?) then (Tidak)
    :Membatalkan seluruh proses\n(rollback);
    :Menampilkan pesan error\ndetail baris bermasalah;
    stop
  else (Ya)
    :Menghitung skor SAW\nuntuk setiap warga;
    |Database|
    :Menyimpan semua record\nsekaligus (bulk insert);
    |Sistem (Web Application)|
    :Menampilkan pesan sukses\n"N data berhasil diproses";
    :Redirect ke halaman Riwayat;
    |Pengguna (Admin / Staff)|
    :Melihat hasil klasifikasi\ndi tabel Riwayat;
    stop
  endif
endif
@enduml
```

---

## 5. Activity Diagram: Riwayat Klasifikasi (Lihat & Cari)
**Aktor:** Admin, Staff, Camat
**Rute Sistem:** `/history` (GET), `/api/history` (GET, JSON)
**Deskripsi:** Proses melihat daftar seluruh hasil klasifikasi yang telah tersimpan, dengan kemampuan pencarian berdasarkan nama, NIK, atau kelurahan.

```plantuml
@startuml
skinparam DefaultFontName Arial
skinparam DefaultFontSize 12
skinparam ActivityBackgroundColor #FEFECE
skinparam ActivityBorderColor #A80036
skinparam ActivityDiamondBackgroundColor #FEFECE
skinparam ActivityDiamondBorderColor #A80036
skinparam SwimlaneBorderColor #333333
skinparam SwimlaneTitleBackgroundColor #E2E2F0
skinparam ConditionEndStyle hline

|Pengguna (Admin / Staff / Camat)|
start
:Membuka menu Riwayat Klasifikasi;

|Database|
:Mengambil semua record\nclassification_results;

|Sistem (Web Application)|
:Menampilkan tabel\ndaftar hasil klasifikasi;

|Pengguna (Admin / Staff / Camat)|
if (Ingin Mencari Data?) then (Ya)
  :Menginput kata kunci\n(Nama / NIK / Kelurahan)\natau memilih filter Kelurahan;
  |Sistem (Web Application)|
  |Database|
  :Menjalankan query\ndengan filter pencarian;
  |Sistem (Web Application)|
  :Memperbarui tabel hasil pencarian;
  |Pengguna (Admin / Staff / Camat)|
  :Melihat hasil yang sudah difilter;
  stop
else (Tidak)
  |Pengguna (Admin / Staff / Camat)|
  :Melihat seluruh data riwayat;
  stop
endif
@enduml
```

---

## 6. Activity Diagram: Edit Data Riwayat Klasifikasi
**Aktor:** Admin, Staff
**Rute Sistem:** `/edit/<id>` (GET, POST)
**Deskripsi:** Proses mengubah data warga yang sudah tersimpan. Sistem akan otomatis menghitung ulang skor SAW. Admin juga dapat mengganti hasil secara manual (override).

```plantuml
@startuml
skinparam DefaultFontName Arial
skinparam DefaultFontSize 12
skinparam ActivityBackgroundColor #FEFECE
skinparam ActivityBorderColor #A80036
skinparam ActivityDiamondBackgroundColor #FEFECE
skinparam ActivityDiamondBorderColor #A80036
skinparam SwimlaneBorderColor #333333
skinparam SwimlaneTitleBackgroundColor #E2E2F0
skinparam ConditionEndStyle hline

|Pengguna (Admin / Staff)|
start
:Memilih data di Riwayat\nlalu klik "Edit";

|Database|
:Mengambil record berdasarkan ID;

|Sistem (Web Application)|
:Menampilkan form Edit\nberisi data saat ini;

|Pengguna (Admin / Staff)|
:Mengubah data identitas\natau nilai kriteria;
:Menekan tombol "Simpan Perubahan";

|Sistem (Web Application)|
:Memvalidasi NIK (16 digit)\ndan kelengkapan kriteria;
if (Validasi Berhasil?) then (Tidak)
  :Menampilkan pesan error;
  stop
else (Ya)
  :Menghitung ulang skor SAW\ndengan data yang diperbarui;
  if (Admin Pilih\nOverride Manual?) then (Ya)
    :Menggunakan status\nyang dipilih Admin\n(Layak / Tidak Layak);
  else (Tidak)
    :Menggunakan hasil\nperhitungan SAW;
  endif
  |Database|
  :Memperbarui record\ndi tabel classification_results;
  |Sistem (Web Application)|
  :Menampilkan pesan sukses;
  :Redirect ke halaman Riwayat;
  |Pengguna (Admin / Staff)|
  :Melihat data yang telah diperbarui;
  stop
endif
@enduml
```

---

## 7. Activity Diagram: Hapus Data Riwayat Klasifikasi
**Aktor:** Admin, Staff
**Rute Sistem:** `/delete/<id>` (POST), `/delete_all` (POST — Admin Only)
**Deskripsi:** Proses menghapus satu record klasifikasi, atau seluruh data sekaligus. Hapus semua hanya bisa dilakukan oleh Admin.

```plantuml
@startuml
skinparam DefaultFontName Arial
skinparam DefaultFontSize 12
skinparam ActivityBackgroundColor #FEFECE
skinparam ActivityBorderColor #A80036
skinparam ActivityDiamondBackgroundColor #FEFECE
skinparam ActivityDiamondBorderColor #A80036
skinparam SwimlaneBorderColor #333333
skinparam SwimlaneTitleBackgroundColor #E2E2F0
skinparam ConditionEndStyle hline

|Pengguna (Admin / Staff)|
start
:Membuka halaman Riwayat Klasifikasi;

|Sistem (Web Application)|
:Menampilkan daftar data warga;

|Pengguna (Admin / Staff)|
if (Jenis Hapus?) then (Hapus Satu Data)
  :Memilih baris data\nlalu klik tombol "Hapus";
  |Sistem (Web Application)|
  if (Role Admin/Staff?) then (Ya)
    |Database|
    :Menghapus record\nberdasarkan ID;
    |Sistem (Web Application)|
    :Menampilkan pesan sukses;
    :Redirect ke Riwayat;
    stop
  else (Tidak)
    :Menampilkan pesan\n"Akses Ditolak";
    stop
  endif
else (Hapus Semua Data)
  :Menekan tombol\n"Hapus Seluruh Data";
  |Sistem (Web Application)|
  if (Role Admin?) then (Ya)
    |Database|
    :Menjalankan DELETE ALL\npada tabel classification_results;
    |Sistem (Web Application)|
    :Menampilkan pesan sukses;
    :Redirect ke Riwayat;
    stop
  else (Tidak — Staff/Camat)
    :Menampilkan pesan\n"Akses Ditolak";
    stop
  endif
endif
@enduml
```

---

## 8. Activity Diagram: Export Data ke Excel
**Aktor:** Admin, Staff, Camat
**Rute Sistem:** `/export/excel` (GET)
**Deskripsi:** Proses mengunduh seluruh data riwayat klasifikasi (atau yang sudah difilter) ke dalam file Excel (.xlsx).

```plantuml
@startuml
skinparam DefaultFontName Arial
skinparam DefaultFontSize 12
skinparam ActivityBackgroundColor #FEFECE
skinparam ActivityBorderColor #A80036
skinparam ActivityDiamondBackgroundColor #FEFECE
skinparam ActivityDiamondBorderColor #A80036
skinparam SwimlaneBorderColor #333333
skinparam SwimlaneTitleBackgroundColor #E2E2F0
skinparam ConditionEndStyle hline

|Pengguna (Admin / Staff / Camat)|
start
:Membuka halaman Riwayat Klasifikasi;
:Memilih filter kelurahan\n(opsional);
:Menekan tombol "Export Excel";

|Database|
:Mengambil data sesuai filter\ndari classification_results;

|Sistem (Web Application)|
:Memformat data ke\nDataFrame (pandas);
:Menambahkan kolom nama\nsub-kriteria per kriteria;
:Membuat file .xlsx\ndi memori (tanpa simpan ke disk);
:Mengirim file sebagai\nlampiran download;

|Pengguna (Admin / Staff / Camat)|
:Mengunduh file laporan Excel;
stop
@enduml
```

---

## 9. Activity Diagram: Manajemen Kriteria
**Aktor:** Admin
**Rute Sistem:** `/kriteria` (GET, POST)
**Deskripsi:** Proses mengelola kriteria penilaian SPK (tambah, edit, hapus, dan atur bobot). Sistem memastikan total bobot seluruh kriteria selalu tepat 1.0.

```plantuml
@startuml
skinparam DefaultFontName Arial
skinparam DefaultFontSize 12
skinparam ActivityBackgroundColor #FEFECE
skinparam ActivityBorderColor #A80036
skinparam ActivityDiamondBackgroundColor #FEFECE
skinparam ActivityDiamondBorderColor #A80036
skinparam SwimlaneBorderColor #333333
skinparam SwimlaneTitleBackgroundColor #E2E2F0
skinparam ConditionEndStyle hline

|Admin|
start
:Membuka menu Manajemen Kriteria;

|Database|
:Mengambil daftar kriteria;

|Sistem (Web Application)|
:Menampilkan tabel daftar Kriteria\nbeserta total bobot saat ini;

|Admin|
if (Pilih Aksi?) then (Tambah Kriteria)
  :Mengisi form: kode, nama,\ntipe, dan bobot;
  :Menekan "Simpan";
  |Sistem (Web Application)|
  if (Total Bobot Tidak\nMelebihi 1.0?) then (Tidak)
    :Menampilkan pesan error\n"Bobot melebihi batas";
    stop
  else (Ya)
    |Database|
    :Menyimpan kriteria baru;
  endif
else if (Pilih Aksi?) then (Edit Bobot Semua)
  :Mengubah nilai bobot\npada tabel;
  :Menekan "Simpan Semua Bobot";
  |Sistem (Web Application)|
  if (Total Bobot = 1.0?) then (Tidak)
    :Menampilkan pesan error\n"Total harus tepat 1.0";
    stop
  else (Ya)
    |Database|
    :Memperbarui semua bobot;
  endif
else (Hapus Kriteria)
  :Menekan tombol "Hapus"\npada baris kriteria;
  |Database|
  :Menghapus kriteria &\nsemua sub-kriterianya;
endif

|Sistem (Web Application)|
:Memperbarui tampilan\ntabel kriteria;
:Menampilkan pesan sukses;
|Admin|
:Melihat daftar kriteria terbaru;
stop
@enduml
```

---

## 10. Activity Diagram: Manajemen Sub-Kriteria
**Aktor:** Admin
**Rute Sistem:** `/sub-kriteria/<kriteria_id>` (GET, POST)
**Deskripsi:** Proses mengelola sub-kriteria (opsi jawaban dan skor) untuk setiap kriteria penilaian. Sub-kriteria menentukan nilai skor yang dipakai dalam perhitungan SAW.

```plantuml
@startuml
skinparam DefaultFontName Arial
skinparam DefaultFontSize 12
skinparam ActivityBackgroundColor #FEFECE
skinparam ActivityBorderColor #A80036
skinparam ActivityDiamondBackgroundColor #FEFECE
skinparam ActivityDiamondBorderColor #A80036
skinparam SwimlaneBorderColor #333333
skinparam SwimlaneTitleBackgroundColor #E2E2F0
skinparam ConditionEndStyle hline

|Admin|
start
:Memilih kriteria di halaman Kriteria\nlalu klik "Lihat Sub-Kriteria";

|Database|
:Mengambil data sub-kriteria\nberdasarkan kriteria_id;

|Sistem (Web Application)|
:Menampilkan tabel daftar\nSub-Kriteria beserta skor;

|Admin|
if (Pilih Aksi?) then (Tambah Sub-Kriteria)
  :Mengisi nama opsi & skor;
  :Menekan "Simpan";
  |Database|
  :Menyimpan sub-kriteria baru;
else if (Pilih Aksi?) then (Edit Sub-Kriteria)
  :Mengubah nama atau skor;
  :Menekan "Simpan";
  |Database|
  :Memperbarui data sub-kriteria;
else (Hapus Sub-Kriteria)
  :Menekan tombol "Hapus";
  |Database|
  :Menghapus data sub-kriteria;
endif

|Sistem (Web Application)|
:Memperbarui tampilan\ntabel sub-kriteria;
:Menampilkan pesan sukses;
|Admin|
:Melihat daftar sub-kriteria terbaru;
stop
@enduml
```

---

## 11. Activity Diagram: Manajemen Pengguna (User Management)
**Aktor:** Admin
**Rute Sistem:** `/users` (GET), `/users/create` (POST), `/users/edit-role/<id>` (POST), `/users/delete/<id>` (POST)
**Deskripsi:** Proses mengelola akun pengguna sistem (Staff dan Camat), termasuk mendaftarkan akun baru, mengubah role, dan menonaktifkan akun.

```plantuml
@startuml
skinparam DefaultFontName Arial
skinparam DefaultFontSize 12
skinparam ActivityBackgroundColor #FEFECE
skinparam ActivityBorderColor #A80036
skinparam ActivityDiamondBackgroundColor #FEFECE
skinparam ActivityDiamondBorderColor #A80036
skinparam SwimlaneBorderColor #333333
skinparam SwimlaneTitleBackgroundColor #E2E2F0
skinparam ConditionEndStyle hline

|Admin|
start
:Membuka menu Kelola Pengguna;

|Database|
:Mengambil daftar pengguna aktif;

|Sistem (Web Application)|
:Menampilkan tabel daftar pengguna;

|Admin|
if (Pilih Aksi?) then (Tambah Akun Baru)
  :Mengisi form: username,\npassword, nama, dan role;
  :Menekan "Buat Akun";
  |Sistem (Web Application)|
  if (Username Unik &\nPassword ≥ 6 Karakter?) then (Tidak)
    :Menampilkan pesan error;
    stop
  else (Ya)
    :Melakukan hash password\n(enkripsi aman);
    |Database|
    :Menyimpan akun baru\nke tabel users;
  endif
else if (Pilih Aksi?) then (Ubah Role)
  :Memilih role baru\n(Staff / Camat) pada akun lain;
  :Menekan "Simpan Role";
  |Sistem (Web Application)|
  if (Bukan Akun Sendiri?) then (Ya)
    |Database|
    :Memperbarui kolom role\npada tabel users;
  else (Tidak)
    :Menampilkan peringatan\n"Tidak bisa ubah role sendiri";
    stop
  endif
else (Nonaktifkan Akun)
  :Menekan tombol "Nonaktifkan"\npada baris akun lain;
  |Sistem (Web Application)|
  if (Bukan Akun Sendiri?) then (Ya)
    |Database|
    :Mengatur is_active = False\n(soft delete);
  else (Tidak)
    :Menampilkan peringatan\n"Tidak bisa hapus akun sendiri";
    stop
  endif
endif

|Sistem (Web Application)|
:Menampilkan pesan sukses;
:Memperbarui tabel pengguna;
|Admin|
:Melihat daftar pengguna terbaru;
stop
@enduml
```

---

## 12. Activity Diagram: Ubah Profil & Foto Profil
**Aktor:** Admin, Staff, Camat
**Rute Sistem:** `/profil` (GET, POST)
**Deskripsi:** Proses memperbarui nama lengkap dan foto profil pengguna yang sedang login.

```plantuml
@startuml
skinparam DefaultFontName Arial
skinparam DefaultFontSize 12
skinparam ActivityBackgroundColor #FEFECE
skinparam ActivityBorderColor #A80036
skinparam ActivityDiamondBackgroundColor #FEFECE
skinparam ActivityDiamondBorderColor #A80036
skinparam SwimlaneBorderColor #333333
skinparam SwimlaneTitleBackgroundColor #E2E2F0
skinparam ConditionEndStyle hline

|Pengguna (Admin / Staff / Camat)|
start
:Membuka menu Profil;

|Database|
:Mengambil data profil\npengguna saat ini;

|Sistem (Web Application)|
:Menampilkan form profil\n(nama lengkap & foto);

|Pengguna (Admin / Staff / Camat)|
:Mengubah nama lengkap\n(opsional);
:Memilih file foto baru\n(opsional);
:Menekan "Simpan Profil";

|Sistem (Web Application)|
if (Ada Upload Foto?) then (Ya)
  if (Format JPG/JPEG/PNG?) then (Tidak)
    :Menampilkan pesan error\n"Format foto tidak valid";
    stop
  else (Ya)
    :Menyimpan file foto\nke folder uploads/profiles;
    :Memperbarui path foto\ndi data pengguna;
  endif
else (Tidak)
endif

|Database|
:Memperbarui data profil\ndi tabel users;

|Sistem (Web Application)|
:Memperbarui data sesi (session)\ndengan info profil baru;
:Menampilkan pesan sukses;

|Pengguna (Admin / Staff / Camat)|
:Melihat profil yang telah diperbarui;
stop
@enduml
```

---

## 13. Activity Diagram: Ganti Password
**Aktor:** Admin, Staff, Camat
**Rute Sistem:** `/ganti-password` (GET, POST)
**Deskripsi:** Proses mengganti kata sandi pengguna. Sistem memverifikasi password lama sebelum menyimpan password baru yang sudah di-hash.

```plantuml
@startuml
skinparam DefaultFontName Arial
skinparam DefaultFontSize 12
skinparam ActivityBackgroundColor #FEFECE
skinparam ActivityBorderColor #A80036
skinparam ActivityDiamondBackgroundColor #FEFECE
skinparam ActivityDiamondBorderColor #A80036
skinparam SwimlaneBorderColor #333333
skinparam SwimlaneTitleBackgroundColor #E2E2F0
skinparam ConditionEndStyle hline

|Pengguna (Admin / Staff / Camat)|
start
:Membuka halaman Ganti Password;

|Sistem (Web Application)|
:Menampilkan form\n(password lama, baru, konfirmasi);

|Pengguna (Admin / Staff / Camat)|
:Mengisi password lama,\npassword baru, & konfirmasi;
:Menekan "Ganti Password";

|Database|
:Mengambil hash password\npengguna saat ini;

|Sistem (Web Application)|
if (Password Lama Cocok?) then (Tidak)
  :Menampilkan pesan\n"Password lama salah";
  stop
else (Ya)
  if (Password Baru =\nKonfirmasi Password?) then (Tidak)
    :Menampilkan pesan\n"Konfirmasi tidak cocok";
    stop
  else (Ya)
    if (Panjang Password\n≥ 6 Karakter?) then (Tidak)
      :Menampilkan pesan\n"Password minimal 6 karakter";
      stop
    else (Ya)
      :Membuat hash password baru;
      |Database|
      :Menyimpan hash password baru\nke tabel users;
      |Sistem (Web Application)|
      :Menampilkan pesan sukses;
      :Redirect ke halaman Dashboard;
      |Pengguna (Admin / Staff / Camat)|
      :Berhasil mengganti password;
      stop
    endif
  endif
endif
@enduml
```

---

## 14. Activity Diagram: Melihat Riwayat Login
**Aktor:** Admin, Staff, Camat
**Rute Sistem:** `/riwayat-login` (GET)
**Deskripsi:** Proses melihat log aktivitas login pribadi pengguna yang sedang aktif, menampilkan 20 riwayat login terakhir beserta waktu, IP address, dan informasi browser.

```plantuml
@startuml
skinparam DefaultFontName Arial
skinparam DefaultFontSize 12
skinparam ActivityBackgroundColor #FEFECE
skinparam ActivityBorderColor #A80036
skinparam ActivityDiamondBackgroundColor #FEFECE
skinparam ActivityDiamondBorderColor #A80036
skinparam SwimlaneBorderColor #333333
skinparam SwimlaneTitleBackgroundColor #E2E2F0
skinparam ConditionEndStyle hline

|Pengguna (Admin / Staff / Camat)|
start
:Membuka menu Riwayat Login;

|Database|
:Mengambil 20 riwayat login terakhir\nmilik pengguna yang sedang login;

|Sistem (Web Application)|
:Menampilkan tabel riwayat login\n(waktu, IP, browser);

|Pengguna (Admin / Staff / Camat)|
if (Ada Riwayat?) then (Ya)
  :Membaca daftar log aktivitas login;
  stop
else (Tidak Ada)
  |Sistem (Web Application)|
  :Menampilkan pesan\n"Belum ada riwayat login";
  stop
endif
@enduml
```

---

## 15. Activity Diagram: Melihat Informasi SPK
**Aktor:** Admin, Staff, Camat
**Rute Sistem:** `/informasi` (GET)
**Deskripsi:** Proses mengakses halaman referensi yang menampilkan penjelasan tentang metode SAW, daftar kriteria beserta bobot, dan ambang batas kelayakan.

```plantuml
@startuml
skinparam DefaultFontName Arial
skinparam DefaultFontSize 12
skinparam ActivityBackgroundColor #FEFECE
skinparam ActivityBorderColor #A80036
skinparam ActivityDiamondBackgroundColor #FEFECE
skinparam ActivityDiamondBorderColor #A80036
skinparam SwimlaneBorderColor #333333
skinparam SwimlaneTitleBackgroundColor #E2E2F0
skinparam ConditionEndStyle hline

|Pengguna (Admin / Staff / Camat)|
start
:Membuka menu Informasi SPK;

|Database|
:Mengambil seluruh data kriteria\nbeserta bobot (tabel kriteria);

|Sistem (Web Application)|
:Menampilkan halaman Informasi:\n- Tabel Kriteria & Bobot\n- Penjelasan Metode SAW\n- Ambang Batas Kelayakan;

|Pengguna (Admin / Staff / Camat)|
:Membaca informasi algoritma\ndan kriteria penilaian SPK;
stop
@enduml
```
