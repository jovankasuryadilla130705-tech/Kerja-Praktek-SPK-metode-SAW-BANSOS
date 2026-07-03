# Kumpulan Activity Diagram — Sistem SPK Klasifikasi Bansos (Metode SAW)
### Kecamatan Pondok Aren, Kota Tangerang Selatan

> **Cara Penggunaan:** Salin kode PlantUML di bawah setiap diagram, lalu buka di **[PlantText.com](https://www.planttext.com/)** atau di **Draw.io** melalui `Extras > Edit Diagram > pilih format PlantUML`.

---
---

## 1. Activity Diagram: Login
**Aktor:** Admin, Staff, Camat
**Deskripsi:** Proses autentikasi pengguna untuk masuk ke dalam sistem.

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
repeat :Menginput username\ndan password;
  :Menekan tombol "Login";

  |Database|
  :Mencari data pengguna\nberdasarkan username;
  :Mencocokkan hash password;

  |Sistem (Web Application)|
backward :Menampilkan pesan\n"Username / Password salah";
repeat while (Kredensial Valid?) is (Tidak) not (Ya)

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
**Deskripsi:** Proses keluar dari sistem.

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
**Deskripsi:** Proses menampilkan ringkasan statistik hasil klasifikasi bansos.

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
:Menghitung jumlah\n"Layak" dan "Tidak Layak";
:Mengambil data per kelurahan;

|Sistem (Web Application)|
:Memproses data untuk\ngrafik Pie & Bar Chart;
:Menampilkan halaman Dashboard\n(kartu statistik & grafik);

|Pengguna (Admin / Staff / Camat)|
:Membaca statistik dan grafik;
stop
@enduml
```

---

## 4. Activity Diagram: Klasifikasi Data Bansos (Input Manual)
**Aktor:** Admin, Staff
**Deskripsi:** Proses menginput data warga satu per satu melalui form, menghitung skor SAW, dan menyimpan hasilnya.

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
repeat :Mengisi data identitas warga\n(NIK, Nama, Alamat, dll.);
  :Memilih nilai untuk\nsetiap kriteria (C1-C7);
  :Menekan tombol "Hitung";

  |Sistem (Web Application)|
  :Memvalidasi NIK (16 digit)\ndan kelengkapan kriteria;

backward :Menampilkan pesan error validasi;
repeat while (Data Valid?) is (Tidak) not (Ya)

|Sistem (Web Application)|
:Menghitung normalisasi\nmatriks SAW (R = nilai / max);
:Menghitung skor akhir\n(SAW = Σ bobot × R);
:Menetapkan status kelayakan\n(≥ 0.50 = Layak);
:Menghasilkan teks alasan otomatis;

|Database|
:Menyimpan record baru ke\ntabel classification_results;

|Sistem (Web Application)|
:Mengarahkan ke halaman Riwayat;

|Pengguna (Admin / Staff)|
:Melihat hasil klasifikasi\ndi tabel Riwayat;
stop
@enduml
```

---

## 5. Activity Diagram: Klasifikasi Data Bansos (Import Excel / CSV)
**Aktor:** Admin, Staff
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
:Menampilkan form\nupload file (Excel/CSV);

|Pengguna (Admin / Staff)|
repeat :Memilih file Excel/CSV\nberisi data warga;
  :Menekan tombol "Upload & Proses";

  |Sistem (Web Application)|
  :Memvalidasi format file\n(.csv, .xls, .xlsx);
  :Membaca file ke DataFrame;
  :Memvalidasi setiap baris data\n(NIK 16 digit, kriteria cocok);

backward :Menampilkan pesan error\ndetail baris bermasalah;
repeat while (Seluruh Data Valid?) is (Tidak) not (Ya)

|Sistem (Web Application)|
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
**Deskripsi:** Proses melihat daftar seluruh hasil klasifikasi warga, dengan fitur pencarian dan filter kelurahan.

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
:Membuka menu\nRiwayat Klasifikasi;

|Database|
:Mengambil semua record\nclassification_results;

|Sistem (Web Application)|
:Menampilkan tabel\ndaftar hasil klasifikasi;

|Pengguna (Admin / Staff / Camat)|
:Menginput kata kunci pencarian\natau memilih filter kelurahan;

|Database|
:Menjalankan query\ndengan filter pencarian;

|Sistem (Web Application)|
:Memperbarui tabel\nhasil pencarian;

|Pengguna (Admin / Staff / Camat)|
:Melihat hasil yang\nsudah difilter;
stop
@enduml
```

---

## 7. Activity Diagram: Edit Data Riwayat Klasifikasi
**Aktor:** Admin, Staff
**Deskripsi:** Proses mengubah data warga yang sudah tersimpan. Sistem otomatis menghitung ulang skor SAW. Admin dapat mengganti hasil secara manual (override).

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
:Mengambil record\nberdasarkan ID;

|Sistem (Web Application)|
:Menampilkan form Edit\nberisi data saat ini;

|Pengguna (Admin / Staff)|
repeat :Mengubah data identitas\natau nilai kriteria;
  :Menekan tombol\n"Simpan Perubahan";

  |Sistem (Web Application)|
  :Memvalidasi NIK (16 digit)\ndan kelengkapan kriteria;

backward :Menampilkan pesan error validasi;
repeat while (Data Valid?) is (Tidak) not (Ya)

|Sistem (Web Application)|
:Menghitung ulang skor SAW\ndengan data yang diperbarui;
:Menetapkan status kelayakan\n(atau override manual oleh Admin);

|Database|
:Memperbarui record\ndi tabel classification_results;

|Sistem (Web Application)|
:Menampilkan pesan sukses;
:Mengarahkan ke halaman Riwayat;

|Pengguna (Admin / Staff)|
:Melihat data yang\ntelah diperbarui;
stop
@enduml
```

---

## 8. Activity Diagram: Hapus Data Riwayat Klasifikasi
**Aktor:** Admin, Staff
**Deskripsi:** Proses menghapus satu record klasifikasi dari tabel riwayat.

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
:Membuka halaman\nRiwayat Klasifikasi;

|Sistem (Web Application)|
:Menampilkan daftar data warga;

|Pengguna (Admin / Staff)|
:Memilih baris data\nlalu klik tombol "Hapus";

|Database|
:Menghapus record\nberdasarkan ID;

|Sistem (Web Application)|
:Menampilkan pesan\n"Data berhasil dihapus";
:Mengarahkan ke halaman Riwayat;

|Pengguna (Admin / Staff)|
:Melihat daftar data\nyang telah diperbarui;
stop
@enduml
```

---

## 9. Activity Diagram: Hapus Seluruh Data Riwayat
**Aktor:** Admin
**Deskripsi:** Proses menghapus seluruh record klasifikasi sekaligus. Hanya Admin yang memiliki akses untuk melakukan aksi ini.

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
:Membuka halaman\nRiwayat Klasifikasi;

|Sistem (Web Application)|
:Menampilkan daftar data warga;

|Admin|
:Menekan tombol\n"Hapus Seluruh Data";

|Database|
:Menjalankan DELETE ALL\npada tabel classification_results;

|Sistem (Web Application)|
:Menampilkan pesan\n"Seluruh data berhasil dihapus";
:Mengarahkan ke halaman Riwayat;

|Admin|
:Melihat halaman Riwayat\n(tabel kosong);
stop
@enduml
```

---

## 10. Activity Diagram: Export Data ke Excel
**Aktor:** Admin, Staff, Camat
**Deskripsi:** Proses mengunduh data riwayat klasifikasi ke file Excel (.xlsx).

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
:Membuka halaman\nRiwayat Klasifikasi;
:Memilih filter kelurahan\n(opsional);
:Menekan tombol\n"Export Excel";

|Database|
:Mengambil data sesuai filter\ndari classification_results;

|Sistem (Web Application)|
:Memformat data ke DataFrame;
:Membuat file .xlsx\ndi memori;
:Mengirim file sebagai\nlampiran download;

|Pengguna (Admin / Staff / Camat)|
:Mengunduh file\nlaporan Excel;
stop
@enduml
```

---

## 11. Activity Diagram: Manajemen Kriteria (Tambah)
**Aktor:** Admin
**Deskripsi:** Proses menambahkan kriteria penilaian SPK baru. Sistem memastikan total bobot seluruh kriteria tidak melebihi 1.0.

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
:Membuka menu\nManajemen Kriteria;

|Database|
:Mengambil daftar kriteria;

|Sistem (Web Application)|
:Menampilkan tabel\ndaftar Kriteria;

|Admin|
repeat :Mengisi form: kode, nama,\ntipe, dan bobot;
  :Menekan tombol "Simpan";

  |Sistem (Web Application)|
  :Menghitung total bobot\n(termasuk bobot baru);

backward :Menampilkan pesan error\n"Bobot melebihi batas 1.0";
repeat while (Total Bobot ≤ 1.0?) is (Tidak) not (Ya)

|Database|
:Menyimpan kriteria baru;

|Sistem (Web Application)|
:Menampilkan pesan sukses;
:Memperbarui tabel kriteria;

|Admin|
:Melihat daftar\nkriteria terbaru;
stop
@enduml
```

---

## 12. Activity Diagram: Manajemen Kriteria (Edit & Hapus)
**Aktor:** Admin
**Deskripsi:** Proses mengubah data kriteria atau menghapus kriteria dari daftar penilaian.

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
:Membuka menu\nManajemen Kriteria;

|Database|
:Mengambil daftar kriteria;

|Sistem (Web Application)|
:Menampilkan tabel\ndaftar Kriteria;

|Admin|
:Memilih kriteria yang\nakan diubah atau dihapus;
:Mengubah data kriteria\natau menekan "Hapus";

|Database|
:Mengeksekusi query\n(Update / Delete);

|Sistem (Web Application)|
:Menampilkan pesan sukses;
:Memperbarui tabel kriteria;

|Admin|
:Melihat daftar\nkriteria terbaru;
stop
@enduml
```

---

## 13. Activity Diagram: Manajemen Sub-Kriteria
**Aktor:** Admin
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
:Memilih kriteria\nlalu klik "Lihat Sub-Kriteria";

|Database|
:Mengambil data sub-kriteria\nberdasarkan kriteria_id;

|Sistem (Web Application)|
:Menampilkan tabel daftar\nSub-Kriteria beserta skor;

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
:Melihat daftar\nsub-kriteria terbaru;
stop
@enduml
```

---

## 14. Activity Diagram: Manajemen Pengguna (Tambah Akun)
**Aktor:** Admin
**Deskripsi:** Proses mendaftarkan akun baru untuk Staff atau Camat ke dalam sistem.

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
:Membuka menu\nKelola Pengguna;

|Database|
:Mengambil daftar\npengguna aktif;

|Sistem (Web Application)|
:Menampilkan tabel\ndaftar pengguna;

|Admin|
repeat :Mengisi form: username,\npassword, nama, dan role;
  :Menekan "Buat Akun";

  |Sistem (Web Application)|
  :Memvalidasi username unik\ndan password ≥ 6 karakter;

backward :Menampilkan pesan error validasi;
repeat while (Validasi Berhasil?) is (Tidak) not (Ya)

|Sistem (Web Application)|
:Melakukan hash password\n(enkripsi aman);

|Database|
:Menyimpan akun baru\nke tabel users;

|Sistem (Web Application)|
:Menampilkan pesan sukses;
:Memperbarui tabel pengguna;

|Admin|
:Melihat daftar\npengguna terbaru;
stop
@enduml
```

---

## 15. Activity Diagram: Manajemen Pengguna (Ubah Role & Nonaktifkan)
**Aktor:** Admin
**Deskripsi:** Proses mengubah role pengguna atau menonaktifkan akun pengguna lain (soft delete).

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
:Membuka menu\nKelola Pengguna;

|Sistem (Web Application)|
:Menampilkan tabel\ndaftar pengguna;

|Admin|
:Memilih pengguna lain\n(bukan akun sendiri);
:Memilih aksi\n(Ubah Role / Nonaktifkan);

|Database|
:Memperbarui data pengguna\n(role atau is_active = False);

|Sistem (Web Application)|
:Menampilkan pesan sukses;
:Memperbarui tabel pengguna;

|Admin|
:Melihat daftar\npengguna terbaru;
stop
@enduml
```

---

## 16. Activity Diagram: Ubah Profil & Foto Profil
**Aktor:** Admin, Staff, Camat
**Deskripsi:** Proses memperbarui nama lengkap dan mengunggah foto profil.

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
repeat :Mengubah nama lengkap\ndan/atau memilih foto baru;
  :Menekan "Simpan Profil";

  |Sistem (Web Application)|
  :Memvalidasi format foto\n(hanya JPG, JPEG, PNG);

backward :Menampilkan pesan error\n"Format foto tidak valid";
repeat while (Format Foto Valid?) is (Tidak) not (Ya)

|Sistem (Web Application)|
:Menyimpan file foto\nke folder uploads/profiles;

|Database|
:Memperbarui data profil\ndi tabel users;

|Sistem (Web Application)|
:Memperbarui data sesi\n(session) browser;
:Menampilkan pesan sukses;

|Pengguna (Admin / Staff / Camat)|
:Melihat profil yang\ntelah diperbarui;
stop
@enduml
```

---

## 17. Activity Diagram: Ganti Password
**Aktor:** Admin, Staff, Camat
**Deskripsi:** Proses mengganti kata sandi pengguna. Sistem memverifikasi password lama sebelum menerima password baru.

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
:Membuka halaman\nGanti Password;

|Sistem (Web Application)|
:Menampilkan form\n(password lama, baru, konfirmasi);

|Pengguna (Admin / Staff / Camat)|
repeat :Mengisi password lama,\npassword baru, & konfirmasi;
  :Menekan "Ganti Password";

  |Database|
  :Mengambil hash password\npengguna saat ini;

  |Sistem (Web Application)|
  :Memvalidasi:\n- Password lama cocok\n- Konfirmasi sesuai\n- Minimal 6 karakter;

backward :Menampilkan pesan error validasi;
repeat while (Validasi Berhasil?) is (Tidak) not (Ya)

|Sistem (Web Application)|
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
**Deskripsi:** Proses melihat log aktivitas login pribadi pengguna yang sedang aktif, menampilkan 20 riwayat login terakhir.

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
:Mengambil 20 riwayat\nlogin terakhir milik\npengguna yang login;

|Sistem (Web Application)|
:Menampilkan tabel\nriwayat login\n(waktu, IP, browser);

|Pengguna (Admin / Staff / Camat)|
:Membaca daftar\nlog aktivitas login;
stop
@enduml
```

---

## 19. Activity Diagram: Melihat Informasi SPK
**Aktor:** Admin, Staff, Camat
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
:Mengambil seluruh data\nkriteria beserta bobot;

|Sistem (Web Application)|
:Menampilkan halaman Informasi:\n- Tabel Kriteria & Bobot\n- Penjelasan Metode SAW\n- Ambang Batas Kelayakan;

|Pengguna (Admin / Staff / Camat)|
:Membaca informasi algoritma\ndan kriteria penilaian SPK;
stop
@enduml
```
