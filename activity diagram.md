# Kumpulan Activity Diagram - Sistem SPK Klasifikasi Bansos (Metode SAW)

Dokumen ini berisi seluruh *Activity Diagram* dari fitur-fitur di dalam aplikasi. Untuk menghindari redundansi (pembuatan diagram berulang-ulang), *swimlane* Aktor telah digabungkan untuk fitur-fitur yang bisa diakses oleh lebih dari satu aktor secara bersamaan (misalnya: **Admin / Staff / Camat** pada fitur Login).

Anda dapat menyalin kode PlantUML di bawah setiap penjelasan, lalu membukanya di [PlantText.com](https://www.planttext.com/) atau memasukkannya ke **Draw.io** melalui menu `Arrange > Insert > Advanced > PlantUML`.

---

## 1. Activity Diagram: Autentikasi (Login)
**Aktor yang terlibat:** Admin, Staff, Camat
**Deskripsi:** Proses aktor masuk ke dalam sistem dengan memvalidasi username dan password.

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
:Membuka halaman web;
|Sistem (Web Application)|
:Menampilkan form Login;
|Pengguna (Admin / Staff / Camat)|
:Menginput username & password;
:Menekan tombol "Login";
|Sistem (Web Application)|
:Mencari data pengguna;
|Database|
:Mengecek kecocokan kredensial;
|Sistem (Web Application)|
if (Data Valid?) then (Tidak)
  :Menampilkan pesan\n"Username/Password salah";
  |Pengguna (Admin / Staff / Camat)|
  :Melihat pesan error;
  stop
else (Ya)
  |Sistem (Web Application)|
  :Membuat sesi (session) pengguna;
  :Mencatat riwayat login;
  :Mengarahkan ke halaman Dashboard;
  |Pengguna (Admin / Staff / Camat)|
  :Melihat halaman Dashboard;
  stop
endif
@enduml
```

---

## 2. Activity Diagram: Klasifikasi Data Bansos (Manual & Import)
**Aktor yang terlibat:** Admin, Staff
**Deskripsi:** Proses menginput data warga (bisa lewat form manual atau import file Excel), menghitung skor SAW, dan menyimpan hasil kelayakan.

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
:Membuka menu Klasifikasi Bansos;
|Sistem (Web Application)|
:Menampilkan opsi form Manual\n& upload Import Massal;
|Pengguna (Admin / Staff)|
if (Metode Input?) then (Import Excel)
  :Mengunggah file Excel/CSV;
  :Menekan tombol "Upload & Hitung";
else (Manual)
  :Menginput data warga\ndan nilai kriteria;
  :Menekan tombol "Hitung Manual";
endif

|Sistem (Web Application)|
:Memvalidasi kelengkapan data;
if (Data Valid?) then (Tidak)
  :Menampilkan pesan error;
  stop
else (Ya)
  :Melakukan perhitungan\nskor metode SAW;
  :Menetapkan status\n(Layak/Tidak Layak);
  |Database|
  :Menyimpan data warga\ndan hasil klasifikasi;
  |Sistem (Web Application)|
  :Mengarahkan ke halaman Histori;
  |Pengguna (Admin / Staff)|
  :Melihat daftar hasil klasifikasi;
  stop
endif
@enduml
```

---

## 3. Activity Diagram: Manajemen Kriteria & Sub-Kriteria
**Aktor yang terlibat:** Admin
**Deskripsi:** Proses menambah, mengubah, atau menghapus kriteria penilaian beserta bobotnya. Sistem memastikan total bobot selalu 1.0.

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
:Membuka menu Kriteria;
|Sistem (Web Application)|
:Menampilkan daftar Kriteria;
|Admin|
:Memilih aksi (Tambah / Edit / Hapus);
if (Aksi?) then (Hapus)
  :Konfirmasi Hapus;
else (Tambah / Edit)
  :Menginput data kriteria\n(kode, nama, bobot);
  :Menekan tombol Simpan;
  |Sistem (Web Application)|
  :Memvalidasi total bobot\n(maksimal 1.0);
  if (Valid?) then (Tidak)
    :Menampilkan pesan error\nlimit bobot;
    stop
  else (Ya)
  endif
endif

|Database|
:Mengeksekusi query\n(Insert / Update / Delete);
|Sistem (Web Application)|
:Memperbarui tampilan\ndaftar kriteria;
:Menampilkan pesan sukses;
|Admin|
:Melihat daftar kriteria terbaru;
stop
@enduml
```

---

## 4. Activity Diagram: Riwayat Klasifikasi (Lihat, Filter, & Export Excel)
**Aktor yang terlibat:** Admin, Staff, Camat
**Deskripsi:** Proses melihat daftar seluruh hasil klasifikasi warga, melakukan pencarian/filter kelurahan, dan mengunduh laporan dalam bentuk Excel.

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

|Pengguna (Admin/Staff/Camat)|
start
:Membuka menu Riwayat Klasifikasi;
|Sistem (Web Application)|
:Mengambil data histori dari database;
|Database|
:Mengembalikan record\nclassification_results;
|Sistem (Web Application)|
:Menampilkan tabel Riwayat Klasifikasi;

|Pengguna (Admin/Staff/Camat)|
if (Pilih Aksi?) then (Cari/Filter)
  :Memilih filter kelurahan\natau input pencarian nama;
  |Sistem (Web Application)|
  :Memperbarui tabel secara dinamis;
  |Pengguna (Admin/Staff/Camat)|
  :Melihat hasil filter;
  stop
else (Export Excel)
  |Pengguna (Admin/Staff/Camat)|
  :Menekan tombol "Export Excel";
  |Sistem (Web Application)|
  :Memproses data ke\nformat DataFrame (Excel);
  :Menghasilkan file .xlsx;
  :Mengirim file sebagai\nlampiran (attachment);
  |Pengguna (Admin/Staff/Camat)|
  :Mengunduh file laporan Excel;
  stop
endif
@enduml
```

---

## 5. Activity Diagram: Manajemen Pengguna (User Management)
**Aktor yang terlibat:** Admin
**Deskripsi:** Proses mendaftarkan akun baru untuk Staff atau Camat, serta menonaktifkan akun lama.

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
|Sistem (Web Application)|
:Menampilkan daftar pengguna aktif;
|Admin|
:Memilih aksi (Tambah Akun / Ubah Role);
:Mengisi form data pengguna baru;
:Menekan tombol Simpan;

|Sistem (Web Application)|
:Memvalidasi input\n(username unik, password kuat);
if (Valid?) then (Tidak)
  :Menampilkan notifikasi error;
  stop
else (Ya)
  :Melakukan hashing (enkripsi) password;
  |Database|
  :Menyimpan data ke tabel users;
  |Sistem (Web Application)|
  :Menampilkan pesan sukses;
  |Admin|
  :Melihat daftar pengguna terbaru;
  stop
endif
@enduml
```

---

## 6. Activity Diagram: Mengubah Profil & Password
**Aktor yang terlibat:** Admin, Staff, Camat
**Deskripsi:** Proses mengubah detail profil pribadi (nama lengkap, foto profil) dan mengganti kata sandi.

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

|Pengguna (Admin/Staff/Camat)|
start
:Membuka menu Profil;
|Sistem (Web Application)|
:Menampilkan form profil & ubah password;
|Pengguna (Admin/Staff/Camat)|
:Memasukkan data profil baru\natau password lama & baru;
:Menekan tombol Simpan Profil;

|Sistem (Web Application)|
:Memvalidasi password lama\n(jika mengganti password);
if (Valid?) then (Tidak)
  :Menampilkan error\n"Password Lama Salah";
  stop
else (Ya)
  |Database|
  :Memperbarui record user\ndi tabel users;
  |Sistem (Web Application)|
  :Memperbarui sesi (session) browser;
  :Menampilkan notifikasi sukses;
  |Pengguna (Admin/Staff/Camat)|
  :Melihat profil yang telah diperbarui;
  stop
endif
@enduml
```
