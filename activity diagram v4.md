# Kumpulan Activity Diagram — Sistem SPK Klasifikasi Bansos (Metode SAW)
### Kecamatan Pondok Aren, Kota Tangerang Selatan

> **Cara Penggunaan:** Salin kode PlantUML, lalu buka di **[PlantText.com](https://www.planttext.com/)**.

---
---

## 1. Activity Diagram: Login
**Aktor:** Admin, Staff, Camat
**Deskripsi:** Proses autentikasi pengguna. Jika gagal, pengguna kembali ke form login dan mencoba lagi.

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
:Menampilkan form Login;

|Pengguna (Admin / Staff / Camat)|
:Menginput username\ndan password;
:Menekan tombol "Login";

|Sistem (Web Application)|
:Mencari data pengguna;

|Database|
:Mencocokkan hash password;

|Sistem (Web Application)|
while (Login Berhasil?) is (Tidak)
  :Menampilkan pesan\n"Username / Password salah";
  |Pengguna (Admin / Staff / Camat)|
  :Menginput ulang username\ndan password;
  :Menekan tombol "Login";
  |Sistem (Web Application)|
  :Mencari data pengguna;
  |Database|
  :Mencocokkan hash password;
  |Sistem (Web Application)|
endwhile (Ya)

|Database|
:Mencatat riwayat login\n(waktu, IP, browser);

|Sistem (Web Application)|
:Membuat sesi (session) pengguna;
:Mengarahkan ke halaman Dashboard;

|Pengguna (Admin / Staff / Camat)|
:Melihat halaman Dashboard;
stop
@enduml
```

---

## 2. Activity Diagram: Logout
**Aktor:** Admin, Staff, Camat
**Deskripsi:** Proses keluar dari sistem dan mengakhiri sesi.

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
:Menekan tombol "Logout";

|Sistem (Web Application)|
:Menghapus session pengguna;
:Mengarahkan ke halaman Login;

|Pengguna (Admin / Staff / Camat)|
:Melihat halaman Login;
stop
@enduml
```

---

## 3. Activity Diagram: Dashboard Statistik
**Aktor:** Admin, Staff, Camat
**Deskripsi:** Proses menampilkan ringkasan statistik hasil klasifikasi bansos berupa kartu angka dan grafik.

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

|Database|
:Menghitung total data warga;
:Menghitung jumlah "Layak"\ndan "Tidak Layak";
:Mengambil data per kelurahan;

|Sistem (Web Application)|
:Memproses data untuk\ngrafik Pie & Bar Chart;
:Menampilkan kartu statistik\ndan grafik;

|Pengguna (Admin / Staff / Camat)|
:Membaca statistik dan grafik;
stop
@enduml
```

---

## 4. Activity Diagram: Klasifikasi Data Bansos (Input Manual)
**Aktor:** Admin, Staff
**Deskripsi:** Proses menginput data warga satu per satu melalui form. Jika validasi gagal, pengguna memperbaiki dan mengirim ulang form.

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
:Mengisi data identitas warga\ndan memilih nilai tiap kriteria;
:Menekan tombol "Hitung";

|Sistem (Web Application)|
:Memvalidasi NIK (16 digit)\ndan kelengkapan semua kriteria;

while (Data Valid?) is (Tidak)
  :Menampilkan pesan error validasi;
  |Pengguna (Admin / Staff)|
  :Memperbaiki data pada form;
  :Menekan tombol "Hitung";
  |Sistem (Web Application)|
  :Memvalidasi NIK (16 digit)\ndan kelengkapan semua kriteria;
endwhile (Ya)

:Menghitung normalisasi\nmatriks SAW;
:Menghitung skor akhir\n(SAW = Σ bobot × R);
:Menetapkan status kelayakan\n(≥ 0.50 = Layak);
:Menghasilkan teks alasan otomatis;

|Database|
:Menyimpan record baru ke\ntabel classification_results;

|Sistem (Web Application)|
:Menampilkan pesan sukses;
:Mengarahkan ke halaman Riwayat;

|Pengguna (Admin / Staff)|
:Melihat hasil klasifikasi\ndi tabel Riwayat;
stop
@enduml
```

---

## 5. Activity Diagram: Klasifikasi Data Bansos (Import Excel / CSV)
**Aktor:** Admin, Staff
**Deskripsi:** Proses mengunggah file Excel/CSV berisi banyak data warga sekaligus. Jika file atau data baris tidak valid, pengguna mengupload ulang file yang sudah diperbaiki.

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
:Menampilkan form Upload File;

|Pengguna (Admin / Staff)|
:Memilih file Excel/CSV\nberisi data warga;
:Menekan "Upload & Proses";

|Sistem (Web Application)|
:Memvalidasi format file\n(.csv, .xls, .xlsx);
:Membaca file ke DataFrame;
:Memvalidasi setiap baris\n(NIK 16 digit, kriteria cocok);

while (Seluruh Data Valid?) is (Tidak)
  :Membatalkan proses (rollback);
  :Menampilkan pesan error\ndetail baris bermasalah;
  |Pengguna (Admin / Staff)|
  :Memperbaiki file Excel/CSV;
  :Memilih ulang file yang sudah diperbaiki;
  :Menekan "Upload & Proses";
  |Sistem (Web Application)|
  :Memvalidasi format file;
  :Membaca file ke DataFrame;
  :Memvalidasi setiap baris;
endwhile (Ya)

:Menghitung skor SAW\nuntuk setiap warga;

|Database|
:Menyimpan semua record\nsekaligus (bulk insert);

|Sistem (Web Application)|
:Menampilkan pesan sukses\n"N data berhasil diproses";
:Mengarahkan ke halaman Riwayat;

|Pengguna (Admin / Staff)|
:Melihat hasil klasifikasi\ndi tabel Riwayat;
stop
@enduml
```

---

## 6. Activity Diagram: Riwayat Klasifikasi (Lihat & Cari)
**Aktor:** Admin, Staff, Camat
**Deskripsi:** Proses melihat seluruh hasil klasifikasi dengan fitur pencarian nama/NIK dan filter kelurahan.

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
:Menginput kata kunci pencarian\natau memilih filter kelurahan;

|Database|
:Menjalankan query\ndengan filter;

|Sistem (Web Application)|
:Memperbarui tampilan tabel;

|Pengguna (Admin / Staff / Camat)|
:Melihat hasil pencarian;
stop
@enduml
```

---

## 7. Activity Diagram: Edit Data Riwayat Klasifikasi
**Aktor:** Admin, Staff
**Deskripsi:** Proses mengubah data warga yang sudah tersimpan. Jika validasi gagal, pengguna kembali memperbaiki form edit.

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
:Menekan "Simpan Perubahan";

|Sistem (Web Application)|
:Memvalidasi NIK (16 digit)\ndan kelengkapan kriteria;

while (Data Valid?) is (Tidak)
  :Menampilkan pesan error validasi;
  |Pengguna (Admin / Staff)|
  :Memperbaiki data pada form edit;
  :Menekan "Simpan Perubahan";
  |Sistem (Web Application)|
  :Memvalidasi NIK (16 digit)\ndan kelengkapan kriteria;
endwhile (Ya)

:Menghitung ulang skor SAW;
:Menetapkan status kelayakan\n(atau override manual oleh Admin);

|Database|
:Memperbarui record\ndi tabel classification_results;

|Sistem (Web Application)|
:Menampilkan pesan sukses;
:Mengarahkan ke halaman Riwayat;

|Pengguna (Admin / Staff)|
:Melihat data yang telah diperbarui;
stop
@enduml
```

---

## 8. Activity Diagram: Hapus Satu Data Riwayat
**Aktor:** Admin, Staff
**Deskripsi:** Proses menghapus satu record klasifikasi. Jika dibatalkan, pengguna kembali ke halaman Riwayat.

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
:Memilih data dan\nmenekan tombol "Hapus";

|Sistem (Web Application)|
if (Konfirmasi Hapus?) then (Ya)
  |Database|
  :Menghapus record\nberdasarkan ID;
  |Sistem (Web Application)|
  :Menampilkan pesan\n"Data berhasil dihapus";
  :Mengarahkan ke halaman Riwayat;
  |Pengguna (Admin / Staff)|
  :Melihat daftar data terbaru;
else (Tidak)
  |Sistem (Web Application)|
  :Kembali ke halaman Riwayat;
  |Pengguna (Admin / Staff)|
  :Melihat daftar data (tidak berubah);
endif
stop
@enduml
```

---

## 9. Activity Diagram: Hapus Seluruh Data Riwayat
**Aktor:** Admin
**Deskripsi:** Proses menghapus seluruh record klasifikasi sekaligus. Hanya Admin yang memiliki akses fitur ini.

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
:Membuka halaman Riwayat Klasifikasi;

|Sistem (Web Application)|
:Menampilkan daftar data warga;

|Admin|
:Menekan tombol\n"Hapus Seluruh Data";

|Sistem (Web Application)|
if (Konfirmasi Hapus Semua?) then (Ya)
  |Database|
  :Menjalankan DELETE ALL\npada tabel classification_results;
  |Sistem (Web Application)|
  :Menampilkan pesan\n"Seluruh data berhasil dihapus";
  :Mengarahkan ke halaman Riwayat;
  |Admin|
  :Melihat halaman Riwayat\n(tabel kosong);
else (Tidak)
  |Sistem (Web Application)|
  :Kembali ke halaman Riwayat;
  |Admin|
  :Melihat daftar data (tidak berubah);
endif
stop
@enduml
```

---

## 10. Activity Diagram: Export Data ke Excel
**Aktor:** Admin, Staff, Camat
**Deskripsi:** Proses mengunduh data riwayat klasifikasi ke file Excel (.xlsx). Tidak ada validasi input.

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
:Memilih filter kelurahan (opsional);
:Menekan tombol "Export Excel";

|Database|
:Mengambil data sesuai filter\ndari classification_results;

|Sistem (Web Application)|
:Memformat data ke DataFrame;
:Membuat file .xlsx di memori;
:Mengirim file sebagai\nlampiran download;

|Pengguna (Admin / Staff / Camat)|
:Mengunduh file laporan Excel;
stop
@enduml
```

---

## 11. Activity Diagram: Tambah Kriteria
**Aktor:** Admin
**Deskripsi:** Proses menambahkan kriteria penilaian baru. Jika total bobot melebihi 1.0, Admin memperbaiki nilai bobot dan mengirim ulang form.

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
:Menampilkan tabel daftar Kriteria\ndan form Tambah Kriteria;

|Admin|
:Mengisi form: kode, nama,\ntipe, dan bobot;
:Menekan tombol "Simpan";

|Sistem (Web Application)|
:Menghitung total bobot\n(existing + bobot baru);

while (Total Bobot ≤ 1.0?) is (Tidak)
  :Menampilkan pesan error\n"Total bobot melebihi 1.0";
  |Admin|
  :Memperbaiki nilai bobot\npada form;
  :Menekan tombol "Simpan";
  |Sistem (Web Application)|
  :Menghitung total bobot;
endwhile (Ya)

|Database|
:Menyimpan kriteria baru;

|Sistem (Web Application)|
:Menampilkan pesan sukses;
:Memperbarui tabel kriteria;

|Admin|
:Melihat daftar kriteria terbaru;
stop
@enduml
```

---

## 12. Activity Diagram: Edit & Hapus Kriteria
**Aktor:** Admin
**Deskripsi:** Proses mengubah data kriteria yang ada atau menghapusnya dari daftar penilaian.

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
:Menampilkan tabel daftar Kriteria;

|Admin|
:Memilih kriteria yang\nakan diubah atau dihapus;

if (Aksi?) then (Edit)
  :Mengubah data kriteria;
  :Menekan "Simpan";
  |Database|
  :Memperbarui data kriteria;
else (Hapus)
  |Sistem (Web Application)|
  if (Konfirmasi Hapus?) then (Ya)
    |Database|
    :Menghapus kriteria beserta\nsemua sub-kriterianya;
  else (Tidak)
    :Kembali ke daftar Kriteria;
    |Admin|
    :Melihat daftar (tidak berubah);
    stop
  endif
endif

|Sistem (Web Application)|
:Menampilkan pesan sukses;
:Memperbarui tabel kriteria;

|Admin|
:Melihat daftar kriteria terbaru;
stop
@enduml
```

---

## 13. Activity Diagram: Manajemen Sub-Kriteria
**Aktor:** Admin
**Deskripsi:** Proses mengelola sub-kriteria (opsi jawaban beserta skor) untuk setiap kriteria penilaian.

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
:Memilih kriteria lalu\nklik "Lihat Sub-Kriteria";

|Database|
:Mengambil sub-kriteria\nberdasarkan kriteria_id;

|Sistem (Web Application)|
:Menampilkan tabel\nSub-Kriteria beserta skor;

|Admin|
:Memilih aksi\n(Tambah / Edit / Hapus);
:Mengisi atau mengubah\nnama opsi dan skor;
:Menekan "Simpan" atau "Hapus";

|Database|
:Mengeksekusi query\n(Insert / Update / Delete);

|Sistem (Web Application)|
:Menampilkan pesan sukses;
:Memperbarui tabel sub-kriteria;

|Admin|
:Melihat daftar sub-kriteria terbaru;
stop
@enduml
```

---

## 14. Activity Diagram: Tambah Akun Pengguna
**Aktor:** Admin
**Deskripsi:** Proses mendaftarkan akun baru untuk Staff atau Camat. Jika validasi gagal (username duplikat atau password terlalu pendek), Admin memperbaiki form dan mengirim ulang.

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
:Menampilkan tabel pengguna\ndan form Tambah Akun;

|Admin|
:Mengisi form: username,\npassword, nama, dan role;
:Menekan "Buat Akun";

|Sistem (Web Application)|
:Memvalidasi username unik\ndan password ≥ 6 karakter;

while (Validasi Berhasil?) is (Tidak)
  :Menampilkan pesan error validasi;
  |Admin|
  :Memperbaiki data pada form;
  :Menekan "Buat Akun";
  |Sistem (Web Application)|
  :Memvalidasi username unik\ndan password ≥ 6 karakter;
endwhile (Ya)

:Melakukan hash password\n(enkripsi aman);

|Database|
:Menyimpan akun baru\nke tabel users;

|Sistem (Web Application)|
:Menampilkan pesan sukses;
:Memperbarui tabel pengguna;

|Admin|
:Melihat daftar pengguna terbaru;
stop
@enduml
```

---

## 15. Activity Diagram: Ubah Role & Nonaktifkan Pengguna
**Aktor:** Admin
**Deskripsi:** Proses mengubah role pengguna lain atau menonaktifkan akun mereka (soft delete). Admin tidak dapat mengubah atau menonaktifkan akunnya sendiri.

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
:Menampilkan tabel pengguna;

|Admin|
:Memilih pengguna lain dan\nmemilih aksi (Ubah Role / Nonaktifkan);

if (Aksi?) then (Ubah Role)
  :Memilih role baru\n(Staff / Camat);
  :Menekan "Simpan";
  |Database|
  :Memperbarui kolom role\npada tabel users;
else (Nonaktifkan)
  |Sistem (Web Application)|
  if (Konfirmasi Nonaktifkan?) then (Ya)
    |Database|
    :Mengatur is_active = False\n(soft delete);
  else (Tidak)
    :Kembali ke daftar pengguna;
    |Admin|
    :Melihat daftar (tidak berubah);
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

## 16. Activity Diagram: Ubah Profil & Foto Profil
**Aktor:** Admin, Staff, Camat
**Deskripsi:** Proses memperbarui nama lengkap dan foto profil. Jika format foto tidak valid, pengguna memilih ulang file foto.

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
:Mengubah nama lengkap\ndan/atau memilih foto baru;
:Menekan "Simpan Profil";

|Sistem (Web Application)|
:Memvalidasi format foto\n(hanya JPG, JPEG, PNG);

while (Format Foto Valid?) is (Tidak)
  :Menampilkan pesan error\n"Format foto tidak valid";
  |Pengguna (Admin / Staff / Camat)|
  :Memilih ulang file foto;
  :Menekan "Simpan Profil";
  |Sistem (Web Application)|
  :Memvalidasi format foto;
endwhile (Ya)

:Menyimpan file foto\nke folder uploads/profiles;

|Database|
:Memperbarui data profil\ndi tabel users;

|Sistem (Web Application)|
:Memperbarui data sesi (session);
:Menampilkan pesan sukses;

|Pengguna (Admin / Staff / Camat)|
:Melihat profil yang telah diperbarui;
stop
@enduml
```

---

## 17. Activity Diagram: Ganti Password
**Aktor:** Admin, Staff, Camat
**Deskripsi:** Proses mengganti kata sandi. Jika validasi gagal (password lama salah, konfirmasi tidak cocok, atau terlalu pendek), pengguna memperbaiki form dan mencoba lagi.

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
:Mengisi password lama,\npassword baru, dan konfirmasi;
:Menekan "Ganti Password";

|Database|
:Mengambil hash password\npengguna saat ini;

|Sistem (Web Application)|
:Memvalidasi:\n- Password lama cocok\n- Konfirmasi sesuai\n- Minimal 6 karakter;

while (Validasi Berhasil?) is (Tidak)
  :Menampilkan pesan error validasi;
  |Pengguna (Admin / Staff / Camat)|
  :Memperbaiki isian form;
  :Menekan "Ganti Password";
  |Database|
  :Mengambil hash password\npengguna saat ini;
  |Sistem (Web Application)|
  :Memvalidasi kembali;
endwhile (Ya)

:Membuat hash password baru;

|Database|
:Menyimpan hash password\nbaru ke tabel users;

|Sistem (Web Application)|
:Menampilkan pesan sukses;
:Mengarahkan ke Dashboard;

|Pengguna (Admin / Staff / Camat)|
:Berhasil mengganti password;
stop
@enduml
```

---

## 18. Activity Diagram: Melihat Riwayat Login
**Aktor:** Admin, Staff, Camat
**Deskripsi:** Proses melihat log 20 aktivitas login terakhir milik pengguna yang sedang aktif.

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
:Mengambil 20 riwayat login\nterakhir milik pengguna aktif;

|Sistem (Web Application)|
:Menampilkan tabel riwayat login\n(waktu, IP address, browser);

|Pengguna (Admin / Staff / Camat)|
:Membaca log aktivitas login;
stop
@enduml
```

---

## 19. Activity Diagram: Melihat Informasi SPK
**Aktor:** Admin, Staff, Camat
**Deskripsi:** Proses mengakses halaman informasi yang menampilkan penjelasan metode SAW, daftar kriteria, bobot, dan ambang batas kelayakan.

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
:Mengambil seluruh data\nkriteria beserta bobot;

|Sistem (Web Application)|
:Menampilkan halaman Informasi:\n- Tabel Kriteria & Bobot SPK\n- Penjelasan Metode SAW\n- Ambang Batas Kelayakan;

|Pengguna (Admin / Staff / Camat)|
:Membaca informasi algoritma\ndan kriteria penilaian;
stop
@enduml
```
