# Kumpulan Activity Diagram — Sistem SPK Klasifikasi Bansos (Metode SAW)
### Kecamatan Pondok Aren, Kota Tangerang Selatan

> **Cara Penggunaan:** Salin kode PlantUML, lalu buka di **[PlantText.com](https://www.planttext.com/)**.
>
> **Catatan teknis:** Seluruh loop validasi (`repeat...repeat while`) diposisikan di lane **Sistem** agar backward arrow tidak menyeberangi swimlane, sehingga garis tetap solid (tidak putus-putus).

---
---

## 1. Activity Diagram: Autentikasi (Login & Logout)
**Aktor:** Admin, Staff, Camat
**Deskripsi:** Proses masuk ke sistem menggunakan username dan password. Jika gagal, pengguna kembali ke form login. Setelah selesai menggunakan sistem, pengguna keluar (logout).

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

repeat
  |Pengguna (Admin / Staff / Camat)|
  :Menginput username\ndan password;
  :Menekan tombol "Login";
  |Database|
  :Mencari data pengguna\ndan mencocokkan hash password;
  |Sistem (Web Application)|
  backward:Menampilkan pesan\n"Username / Password salah";
repeat while (Login Berhasil?) is (Tidak)
-> Ya;

|Database|
:Mencatat riwayat login\n(waktu, IP address, browser);

|Sistem (Web Application)|
:Membuat sesi (session) pengguna;
:Mengarahkan ke halaman Dashboard;

|Pengguna (Admin / Staff / Camat)|
:Menggunakan sistem;
:Menekan tombol "Logout";

|Sistem (Web Application)|
:Menghapus sesi pengguna;
:Mengarahkan ke halaman Login;

|Pengguna (Admin / Staff / Camat)|
:Melihat halaman Login;
stop
@enduml
```

---

## 2. Activity Diagram: Dashboard & Informasi SPK
**Aktor:** Admin, Staff, Camat
**Deskripsi:** Proses mengakses halaman Dashboard (statistik klasifikasi) atau halaman Informasi SPK (penjelasan metode dan kriteria). Keduanya adalah halaman tampilan tanpa proses input.

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
:Memilih menu\n(Dashboard atau Informasi SPK);

if (Halaman yang Dipilih?) then (Dashboard)

  |Database|
  :Menghitung total data warga,\njumlah Layak & Tidak Layak,\ndan data per kelurahan;

  |Sistem (Web Application)|
  :Menampilkan kartu statistik\ngrafik Pie & Bar Chart;

  |Pengguna (Admin / Staff / Camat)|
  :Membaca ringkasan statistik;

else (Informasi SPK)

  |Database|
  :Mengambil seluruh data kriteria\nbeserta bobot penilaian;

  |Sistem (Web Application)|
  :Menampilkan Tabel Kriteria & Bobot,\npenjelasan Metode SAW,\ndan ambang batas kelayakan;

  |Pengguna (Admin / Staff / Camat)|
  :Membaca informasi algoritma SPK;

endif
stop
@enduml
```

---

## 3. Activity Diagram: Klasifikasi Data Bansos
**Aktor:** Admin, Staff
**Deskripsi:** Proses menginput data warga dan menghitung kelayakan menggunakan metode SAW. Tersedia dua metode: input manual satu per satu melalui form, atau import massal melalui file Excel/CSV. Jika data tidak valid, pengguna memperbaiki dan mengirim ulang.

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
:Menampilkan halaman Klasifikasi\n(form Manual & tombol Upload Excel);

|Pengguna (Admin / Staff)|
if (Metode Input?) then (Input Manual)

  :Mengisi form data warga\ndan memilih nilai tiap kriteria;
  :Menekan tombol "Hitung";

  |Sistem (Web Application)|
  repeat
    :Memvalidasi NIK (16 digit)\ndan kelengkapan semua kriteria;
    backward:Menampilkan pesan error validasi;
    |Pengguna (Admin / Staff)|
    :Memperbaiki data form;
    :Menekan tombol "Hitung";
    |Sistem (Web Application)|
  repeat while (Data Valid?) is (Tidak)
  -> Ya;

else (Import Excel / CSV)

  :Memilih file Excel/CSV;
  :Menekan tombol "Upload & Proses";

  |Sistem (Web Application)|
  repeat
    :Memvalidasi format file\ndan setiap baris data;
    backward:Menampilkan error baris\nbermasalah;
    |Pengguna (Admin / Staff)|
    :Memperbaiki file\ndan upload ulang;
    |Sistem (Web Application)|
  repeat while (File & Data Valid?) is (Tidak)
  -> Ya;

endif

:Menghitung skor SAW\n(Normalisasi + Pembobotan);
:Menetapkan status kelayakan\n(Skor ≥ 0.50 = Layak);
:Menghasilkan teks alasan otomatis;

|Database|
:Menyimpan data warga\ndan hasil ke classification_results;

|Sistem (Web Application)|
:Menampilkan pesan sukses;
:Mengarahkan ke halaman Riwayat;

|Pengguna (Admin / Staff)|
:Melihat hasil klasifikasi\ndi tabel Riwayat;
stop
@enduml
```

---

## 4. Activity Diagram: Riwayat Klasifikasi (Tampil, Cari & Export)
**Aktor:** Admin, Staff, Camat
**Deskripsi:** Proses melihat seluruh hasil klasifikasi yang tersimpan, melakukan pencarian/filter berdasarkan nama, NIK, atau kelurahan, serta mengunduh laporan dalam format Excel.

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
:Mengambil seluruh record\nclassification_results;

|Sistem (Web Application)|
:Menampilkan tabel\ndaftar hasil klasifikasi;

|Pengguna (Admin / Staff / Camat)|
if (Aksi?) then (Cari / Filter)

  :Menginput kata kunci pencarian\natau memilih filter kelurahan;

  |Database|
  :Menjalankan query dengan filter;

  |Sistem (Web Application)|
  :Memperbarui tampilan tabel;

  |Pengguna (Admin / Staff / Camat)|
  :Melihat hasil pencarian;

else (Export Excel)

  :Memilih filter kelurahan (opsional);
  :Menekan tombol "Export Excel";

  |Database|
  :Mengambil data sesuai filter;

  |Sistem (Web Application)|
  :Memformat data ke DataFrame;
  :Membuat file .xlsx di memori;
  :Mengirim file sebagai lampiran;

  |Pengguna (Admin / Staff / Camat)|
  :Mengunduh file laporan Excel;

endif
stop
@enduml
```

---

## 5. Activity Diagram: Edit & Hapus Data Riwayat
**Aktor:** Admin, Staff
**Deskripsi:** Proses mengubah data warga yang sudah tersimpan (dengan hitung ulang SAW) atau menghapusnya. Untuk edit, jika validasi gagal pengguna kembali ke form. Untuk hapus, pengguna diminta konfirmasi terlebih dahulu.

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
if (Aksi?) then (Edit)

  :Memilih data lalu\nmenekan tombol "Edit";

  |Database|
  :Mengambil record berdasarkan ID;

  |Sistem (Web Application)|
  :Menampilkan form Edit\nberisi data saat ini;

  repeat
    |Pengguna (Admin / Staff)|
    :Mengubah data identitas\natau nilai kriteria;
    :Menekan "Simpan Perubahan";
    |Sistem (Web Application)|
    :Memvalidasi NIK (16 digit)\ndan kelengkapan kriteria;
    backward:Menampilkan pesan error validasi;
    |Sistem (Web Application)|
  repeat while (Data Valid?) is (Tidak)
  -> Ya;

  :Menghitung ulang skor SAW;
  :Menetapkan status kelayakan\n(atau override manual oleh Admin);

  |Database|
  :Memperbarui record\ndi classification_results;

  |Sistem (Web Application)|
  :Menampilkan pesan sukses;
  :Mengarahkan ke halaman Riwayat;

  |Pengguna (Admin / Staff)|
  :Melihat data yang telah diperbarui;

else (Hapus)

  :Memilih data lalu\nmenekan tombol "Hapus";

  |Sistem (Web Application)|
  if (Konfirmasi Hapus?) then (Ya)

    |Database|
    :Menghapus record berdasarkan ID;

    |Sistem (Web Application)|
    :Menampilkan pesan sukses;
    :Mengarahkan ke halaman Riwayat;

    |Pengguna (Admin / Staff)|
    :Melihat daftar data terbaru;

  else (Tidak)

    |Sistem (Web Application)|
    :Kembali ke halaman Riwayat;

    |Pengguna (Admin / Staff)|
    :Melihat daftar data\n(tidak berubah);

  endif

endif
stop
@enduml
```

---

## 6. Activity Diagram: Manajemen Kriteria & Sub-Kriteria
**Aktor:** Admin
**Deskripsi:** Proses mengelola kriteria penilaian SPK (tambah, edit, hapus) beserta sub-kriteria (opsi jawaban dan skor) masing-masing. Sistem memastikan total bobot semua kriteria selalu tepat 1.0.

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
:Menampilkan tabel Kriteria\nbeserta total bobot;

|Admin|
if (Kelola?) then (Tambah Kriteria)

  |Sistem (Web Application)|
  repeat
    |Admin|
    :Mengisi form kriteria\n(kode, nama, tipe, bobot);
    :Menekan "Simpan";
    |Sistem (Web Application)|
    :Menghitung total bobot\n(existing + bobot baru);
    backward:Menampilkan error\n"Total bobot melebihi 1.0";
  repeat while (Total Bobot ≤ 1.0?) is (Tidak)
  -> Ya;

  |Database|
  :Menyimpan kriteria baru;

else if (Kelola?) then (Edit Kriteria)

  |Admin|
  :Mengubah data kriteria\n(nama, tipe, bobot);
  :Menekan "Simpan";

  |Database|
  :Memperbarui data kriteria;

else if (Kelola?) then (Hapus Kriteria)

  |Admin|
  :Menekan tombol "Hapus"\npada baris kriteria;

  |Sistem (Web Application)|
  if (Konfirmasi Hapus?) then (Ya)
    |Database|
    :Menghapus kriteria dan\nsemua sub-kriterianya;
  else (Tidak)
    :Kembali ke daftar Kriteria;
    stop
  endif

else (Kelola Sub-Kriteria)

  |Admin|
  :Memilih kriteria lalu\nklik "Lihat Sub-Kriteria";

  |Database|
  :Mengambil sub-kriteria\nberdasarkan kriteria_id;

  |Sistem (Web Application)|
  :Menampilkan tabel Sub-Kriteria;

  |Admin|
  :Memilih aksi (Tambah / Edit / Hapus)\ndan mengisi data opsi & skor;
  :Menekan "Simpan" atau "Hapus";

  |Database|
  :Mengeksekusi query\n(Insert / Update / Delete);

endif

|Sistem (Web Application)|
:Menampilkan pesan sukses;
:Memperbarui tampilan tabel;

|Admin|
:Melihat daftar terbaru;
stop
@enduml
```

---

## 7. Activity Diagram: Manajemen Pengguna
**Aktor:** Admin
**Deskripsi:** Proses mengelola akun pengguna sistem (Staff dan Camat), meliputi: tambah akun baru, ubah role, dan nonaktifkan akun. Admin tidak dapat mengubah atau menonaktifkan akunnya sendiri.

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
:Menampilkan tabel pengguna;

|Admin|
if (Aksi?) then (Tambah Akun)

  |Sistem (Web Application)|
  repeat
    |Admin|
    :Mengisi form: username,\npassword, nama, dan role;
    :Menekan "Buat Akun";
    |Sistem (Web Application)|
    :Memvalidasi username unik\ndan password ≥ 6 karakter;
    backward:Menampilkan pesan error validasi;
  repeat while (Validasi Berhasil?) is (Tidak)
  -> Ya;

  :Melakukan hash password\n(enkripsi aman);

  |Database|
  :Menyimpan akun baru ke tabel users;

else if (Aksi?) then (Ubah Role)

  |Admin|
  :Memilih pengguna lain;
  :Memilih role baru (Staff / Camat);
  :Menekan "Simpan";

  |Database|
  :Memperbarui kolom role\npada tabel users;

else (Nonaktifkan Akun)

  |Admin|
  :Memilih pengguna lain;
  :Menekan "Nonaktifkan";

  |Sistem (Web Application)|
  if (Konfirmasi?) then (Ya)
    |Database|
    :Mengatur is_active = False\n(soft delete);
  else (Tidak)
    :Kembali ke daftar pengguna;
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

## 8. Activity Diagram: Profil & Keamanan
**Aktor:** Admin, Staff, Camat
**Deskripsi:** Proses mengelola akun pribadi pengguna: memperbarui nama dan foto profil, mengganti password, serta melihat log riwayat login. Jika validasi gagal pada form profil atau password, pengguna memperbaiki dan mengirim ulang.

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
:Memilih menu Profil & Keamanan;

|Sistem (Web Application)|
:Menampilkan pilihan:\nEdit Profil, Ganti Password,\natau Riwayat Login;

|Pengguna (Admin / Staff / Camat)|
if (Menu yang Dipilih?) then (Edit Profil)

  |Database|
  :Mengambil data profil saat ini;

  |Sistem (Web Application)|
  :Menampilkan form profil\n(nama & foto);

  repeat
    |Pengguna (Admin / Staff / Camat)|
    :Mengubah nama lengkap\ndan/atau memilih foto baru;
    :Menekan "Simpan Profil";
    |Sistem (Web Application)|
    :Memvalidasi format foto\n(JPG, JPEG, atau PNG);
    backward:Menampilkan error\n"Format foto tidak valid";
  repeat while (Format Valid?) is (Tidak)
  -> Ya;

  :Menyimpan file foto\nke folder uploads/profiles;

  |Database|
  :Memperbarui data profil\ndi tabel users;

  |Sistem (Web Application)|
  :Memperbarui data sesi (session);
  :Menampilkan pesan sukses;

  |Pengguna (Admin / Staff / Camat)|
  :Melihat profil yang diperbarui;

else if (Menu yang Dipilih?) then (Ganti Password)

  |Sistem (Web Application)|
  :Menampilkan form\n(password lama, baru, konfirmasi);

  repeat
    |Pengguna (Admin / Staff / Camat)|
    :Mengisi password lama,\npassword baru, dan konfirmasi;
    :Menekan "Ganti Password";
    |Database|
    :Mengambil hash password\npengguna saat ini;
    |Sistem (Web Application)|
    :Memvalidasi: password lama cocok,\nkonfirmasi sesuai, panjang ≥ 6 karakter;
    backward:Menampilkan pesan error validasi;
  repeat while (Validasi Berhasil?) is (Tidak)
  -> Ya;

  :Membuat hash password baru;

  |Database|
  :Menyimpan hash password baru\nke tabel users;

  |Sistem (Web Application)|
  :Menampilkan pesan sukses;
  :Mengarahkan ke Dashboard;

  |Pengguna (Admin / Staff / Camat)|
  :Berhasil mengganti password;

else (Riwayat Login)

  |Database|
  :Mengambil 20 riwayat login\nterakhir milik pengguna aktif;

  |Sistem (Web Application)|
  :Menampilkan tabel riwayat login\n(waktu, IP address, browser);

  |Pengguna (Admin / Staff / Camat)|
  :Membaca log aktivitas login;

endif
stop
@enduml
```
