# Pengujian Black Box Testing
## Sistem Pendukung Keputusan (SPK) Klasifikasi Penerima Bantuan Sosial
### Kecamatan Pondok Aren — Metode Simple Additive Weighting (SAW)

---

## 1. Pendahuluan

### 1.1 Tujuan Pengujian

Pengujian ini bertujuan untuk memverifikasi bahwa seluruh fungsionalitas yang tersedia pada Sistem Pendukung Keputusan (SPK) Klasifikasi Penerima Bantuan Sosial berbasis metode SAW berjalan sesuai dengan kebutuhan dan spesifikasi yang telah dirancang. Pengujian dilakukan menggunakan metode **Black Box Testing**, yaitu pendekatan pengujian yang berfokus pada perilaku fungsional sistem dari sudut pandang pengguna tanpa memperhatikan struktur kode internal.

### 1.2 Ruang Lingkup Pengujian

Pengujian mencakup seluruh modul fungsional pada aplikasi web, meliputi:

1. Modul Autentikasi (Login & Logout)
2. Modul Dashboard Statistik
3. Modul Klasifikasi Data (Input Manual & Import Massal)
4. Modul Manajemen Kriteria & Sub-Kriteria
5. Modul Manajemen Histori (Lihat, Cari, Filter, Edit, Hapus)
6. Modul Export Data ke Excel
7. Modul Informasi SPK
8. Modul Profil Admin (Edit Profil & Ganti Password)

### 1.3 Metode Pengujian

| Aspek | Keterangan |
|:---|:---|
| **Metode** | Black Box Testing |
| **Teknik** | Equivalence Partitioning & Boundary Value Analysis |
| **Objek Uji** | Aplikasi web SPK Bansos Pondok Aren |
| **Lingkungan** | Browser Web (Google Chrome), Localhost (`http://127.0.0.1:5000`) |
| **Perangkat Lunak** | Python 3.x, Flask, SQLite, HTML, Tailwind CSS |

### 1.4 Definisi Kolom Tabel Pengujian

| Kolom | Keterangan |
|:---|:---|
| **No** | Nomor urut test case |
| **Identifikasi** | Kode unik test case (misal: TC-AUTH-01) |
| **Deskripsi Pengujian** | Penjelasan singkat skenario yang diuji |
| **Data/Kondisi Masukan** | Input yang diberikan kepada sistem |
| **Prosedur Pengujian** | Langkah-langkah yang dilakukan |
| **Hasil yang Diharapkan** | Output/perilaku sistem yang seharusnya terjadi |
| **Hasil Pengujian** | ✅ Berhasil / ❌ Gagal |
| **Keterangan** | Catatan tambahan jika diperlukan |

---

## 2. Pengujian Modul Autentikasi

### 2.1 Login

| No | Identifikasi | Deskripsi Pengujian | Data/Kondisi Masukan | Prosedur Pengujian | Hasil yang Diharapkan | Hasil Pengujian | Keterangan |
|:---:|:---|:---|:---|:---|:---|:---:|:---|
| 1 | TC-AUTH-01 | Login dengan kredensial valid | Username: `admin`, Password: sesuai `.env` | 1. Buka halaman `/` <br>2. Masukkan username dan password yang benar <br>3. Klik tombol Login | Sistem mengarahkan pengguna ke halaman Dashboard (`/dashboard`). Riwayat login tercatat di database. | ✅ Berhasil | — |
| 2 | TC-AUTH-02 | Login dengan password salah | Username: `admin`, Password: `passwordSalah123` | 1. Buka halaman `/` <br>2. Masukkan username benar, password salah <br>3. Klik tombol Login | Sistem menampilkan pesan error: *"Username atau password salah"* dan tetap berada di halaman login | ✅ Berhasil | — |
| 3 | TC-AUTH-03 | Login dengan username yang tidak terdaftar | Username: `user_tidak_ada`, Password: `apasaja` | 1. Buka halaman `/` <br>2. Masukkan username dan password yang tidak terdaftar <br>3. Klik tombol Login | Sistem menampilkan pesan error: *"Username atau password salah"* dan tetap berada di halaman login | ✅ Berhasil | — |
| 4 | TC-AUTH-04 | Login dengan field kosong | Username: *(kosong)*, Password: *(kosong)* | 1. Buka halaman `/` <br>2. Biarkan semua field kosong <br>3. Klik tombol Login | Browser memvalidasi field wajib diisi sebelum form dikirim (atribut `required` HTML) | ✅ Berhasil | Validasi dilakukan di sisi browser |
| 5 | TC-AUTH-05 | Akses halaman dashboard tanpa login | — (sesi tidak aktif) | 1. Buka URL `/dashboard` langsung tanpa login terlebih dahulu | Sistem mengarahkan pengguna ke halaman login (`/`) | ✅ Berhasil | Semua halaman terproteksi `is_logged_in()` |
| 6 | TC-AUTH-06 | Logout dari sistem | Pengguna dalam kondisi sudah login | 1. Login ke sistem <br>2. Klik tombol Logout dari sidebar/navbar | Session pengguna dihapus. Sistem mengarahkan ke halaman login. Akses ke `/dashboard` dialihkan kembali ke `/` | ✅ Berhasil | — |

---

## 3. Pengujian Modul Dashboard

| No | Identifikasi | Deskripsi Pengujian | Data/Kondisi Masukan | Prosedur Pengujian | Hasil yang Diharapkan | Hasil Pengujian | Keterangan |
|:---:|:---|:---|:---|:---|:---|:---:|:---|
| 7 | TC-DASH-01 | Tampilan statistik saat data kosong | Database tidak memiliki data klasifikasi | 1. Login ke sistem <br>2. Buka halaman `/dashboard` | Halaman menampilkan angka `0` untuk Total Warga, Jumlah Layak, dan Jumlah Tidak Layak. Grafik ditampilkan kosong/tanpa data | ✅ Berhasil | — |
| 8 | TC-DASH-02 | Tampilan statistik setelah data ada | Database memiliki data klasifikasi | 1. Masukkan beberapa data melalui klasifikasi <br>2. Buka halaman `/dashboard` | Halaman menampilkan jumlah total warga, jumlah layak, jumlah tidak layak, dan grafik distribusi kelayakan serta grafik per kelurahan dengan data yang sesuai | ✅ Berhasil | — |
| 9 | TC-DASH-03 | Grafik distribusi kelayakan (Pie Chart) | Data dengan status Layak dan Tidak Layak | 1. Login ke sistem <br>2. Buka halaman `/dashboard` | Grafik Pie Chart tampil dan merepresentasikan proporsi status Layak dan Tidak Layak secara akurat | ✅ Berhasil | Menggunakan Chart.js |
| 10 | TC-DASH-04 | Grafik distribusi per kelurahan (Bar Chart) | Data dari beberapa kelurahan berbeda | 1. Masukkan data dari berbagai kelurahan <br>2. Buka halaman `/dashboard` | Grafik Bar Chart menampilkan setiap kelurahan sebagai label sumbu-X dengan jumlah warga yang tepat | ✅ Berhasil | — |

---

## 4. Pengujian Modul Klasifikasi Data

### 4.1 Input Manual

| No | Identifikasi | Deskripsi Pengujian | Data/Kondisi Masukan | Prosedur Pengujian | Hasil yang Diharapkan | Hasil Pengujian | Keterangan |
|:---:|:---|:---|:---|:---|:---|:---:|:---|
| 11 | TC-KLS-01 | Klasifikasi manual dengan data lengkap dan valid — warga "Layak" | NIK: 1234567890123456, No KK: 6543210987654321, Nama: Budi Santoso, Pekerjaan: Buruh, Kelurahan: Pondok Aren, Kriteria: C1=≤Rp500.000, C2=>4 Orang, C3=Tidak Memiliki Aset, C4=Tidak Memiliki Tempat Tinggal, C5=Tanah/Atap Rumbia, C6=Tanpa Listrik, C7=Air Hujan/Beli Eceran | 1. Login ke sistem <br>2. Buka halaman `/classification` <br>3. Isi seluruh field form manual dengan data di atas <br>4. Klik tombol Klasifikasikan | Sistem menyimpan data ke database, menghitung skor SAW, menetapkan status **"Layak"** (skor ≥ 0.50), dan menampilkan pesan sukses. Pengguna diarahkan ke halaman Histori | ✅ Berhasil | Skor SAW yang dihasilkan mendekati 1.00 |
| 12 | TC-KLS-02 | Klasifikasi manual dengan data lengkap dan valid — warga "Tidak Layak" | NIK: 9876543210987654, No KK: 1234567890123456, Nama: Siti Rahma, Pekerjaan: PNS, Kelurahan: Pondok Jaya, Kriteria: C1=>Rp3.000.000, C2=1 Orang, C3=Memiliki Mobil, C4=Milik Sendiri, C5=Permanen, C6=>2200VA, C7=PDAM | 1. Login ke sistem <br>2. Buka halaman `/classification` <br>3. Isi seluruh field form manual dengan data di atas <br>4. Klik tombol Klasifikasikan | Sistem menyimpan data, menghitung skor SAW, menetapkan status **"Tidak Layak"** (skor < 0.50), dan menampilkan pesan sukses. Pengguna diarahkan ke halaman Histori | ✅ Berhasil | Skor SAW yang dihasilkan mendekati 0.20 |
| 13 | TC-KLS-03 | Klasifikasi manual dengan NIK kurang dari 16 digit | NIK: `1234` (4 digit), field lain diisi lengkap | 1. Buka `/classification` <br>2. Isi NIK dengan 4 digit saja <br>3. Klik Klasifikasikan | Sistem menampilkan pesan error: *"NIK harus 16 digit angka"* dan tidak menyimpan data | ✅ Berhasil | Validasi dilakukan di backend (`app.py` baris 894) |
| 14 | TC-KLS-04 | Klasifikasi manual dengan NIK mengandung huruf | NIK: `12345678ABCD1234`, field lain diisi lengkap | 1. Buka `/classification` <br>2. Isi NIK dengan campuran huruf dan angka <br>3. Klik Klasifikasikan | Sistem menampilkan pesan error: *"NIK harus 16 digit angka"* dan tidak menyimpan data | ✅ Berhasil | Validasi `isdigit()` di backend |
| 15 | TC-KLS-05 | Klasifikasi manual dengan No. KK kurang dari 16 digit | No KK: `9876` (4 digit), field lain diisi lengkap | 1. Buka `/classification` <br>2. Isi No KK dengan 4 digit saja <br>3. Klik Klasifikasikan | Sistem menampilkan pesan error: *"No. KK harus 16 digit angka"* dan tidak menyimpan data | ✅ Berhasil | Validasi dilakukan di backend (`app.py` baris 898) |
| 16 | TC-KLS-06 | Klasifikasi manual dengan field identitas kosong | NIK dan Nama dibiarkan kosong | 1. Buka `/classification` <br>2. Biarkan field NIK atau Nama kosong <br>3. Klik Klasifikasikan | Browser menampilkan validasi field wajib (`required`) sebelum form dikirim, atau sistem tidak memproses data karena tidak ada NIK | ✅ Berhasil | Guard di `app.py` baris 890: `if request.form.get('nik')` |

### 4.2 Import Massal (File Upload)

| No | Identifikasi | Deskripsi Pengujian | Data/Kondisi Masukan | Prosedur Pengujian | Hasil yang Diharapkan | Hasil Pengujian | Keterangan |
|:---:|:---|:---|:---|:---|:---|:---:|:---|
| 17 | TC-IMP-01 | Import file Excel (.xlsx) berformat benar | File `.xlsx` dengan kolom: `nik`, `no_kk`, `nama`, `pekerjaan`, `alamat`, `kelurahan`, `C1`—`C7` atau nama kriteria | 1. Login ke sistem <br>2. Buka `/classification` tab Import <br>3. Pilih file `.xlsx` yang valid <br>4. Klik tombol Upload/Import | Sistem memproses semua baris, menghitung skor SAW untuk setiap baris, menyimpan ke database, dan menampilkan pesan sukses: *"Sukses memproses N data!"* | ✅ Berhasil | Contoh file: `DummyData_warga.xlsx` yang tersedia di root proyek |
| 18 | TC-IMP-02 | Import file CSV berformat benar | File `.csv` berisi data warga dengan kolom yang sesuai | 1. Pilih file `.csv` yang valid <br>2. Klik tombol Import | Sistem berhasil membaca dan memproses data CSV, menyimpan hasilnya ke database | ✅ Berhasil | — |
| 19 | TC-IMP-03 | Import file dengan format tidak didukung | File berekstensi `.pdf` atau `.txt` | 1. Coba upload file `.pdf` atau `.txt` <br>2. Klik Import | Sistem menampilkan pesan error: *"Format file harus .csv, .xls, atau .xlsx."* dan tidak memproses file | ✅ Berhasil | Validasi di fungsi `baca_dataframe_upload()` |
| 20 | TC-IMP-04 | Import file Excel dengan NIK tidak valid (tidak 16 digit) | File `.xlsx` berisi baris dengan NIK berjumlah 5 digit | 1. Upload file `.xlsx` yang memiliki data NIK tidak valid <br>2. Klik Import | Sistem menampilkan pesan error yang mencantumkan detail NIK bermasalah: *"NIK harus 16 digit angka. Ditemukan: '12345'"* | ✅ Berhasil | Validasi per baris di loop import `app.py` baris 798 |
| 21 | TC-IMP-05 | Import file Excel dengan kolom sub-kriteria tidak dikenali | File `.xlsx` dengan nilai kriteria yang tidak cocok dengan sub-kriteria manapun | 1. Upload file dengan nilai kriteria yang tidak terdaftar <br>2. Klik Import | Sistem tetap berhasil memproses, nilai kriteria yang tidak dikenali menggunakan skor default `3` (nilai tengah) | ✅ Berhasil | Fallback skor default di `app.py` baris 835 |
| 22 | TC-IMP-06 | Import tanpa memilih file | Form import dikirim tanpa memilih file | 1. Buka tab Import <br>2. Klik tombol Import tanpa memilih file | Sistem tidak memproses apapun karena kondisi `file.filename != ''` tidak terpenuhi | ✅ Berhasil | Guard di `app.py` baris 777 |

---

## 5. Pengujian Modul Manajemen Kriteria

### 5.1 Manajemen Kriteria

| No | Identifikasi | Deskripsi Pengujian | Data/Kondisi Masukan | Prosedur Pengujian | Hasil yang Diharapkan | Hasil Pengujian | Keterangan |
|:---:|:---|:---|:---|:---|:---|:---:|:---|
| 23 | TC-KRT-01 | Menampilkan daftar kriteria | Database memiliki 7 kriteria awal (C1—C7) | 1. Login <br>2. Buka halaman `/kriteria` | Halaman menampilkan seluruh 7 kriteria (C1—C7) beserta nama, tipe, bobot, dan total bobot 1.0 | ✅ Berhasil | — |
| 24 | TC-KRT-02 | Menambah kriteria baru dengan bobot valid | Kode: `C8`, Nama: `Kondisi Kesehatan`, Tipe: `Cost`, Bobot: `0.00` (total bobot sudah 1.0) | 1. Buka `/kriteria` <br>2. Klik tombol Tambah Kriteria <br>3. Isi semua field | Karena total bobot sudah 1.0, penambahan dengan bobot `> 0` ditolak dengan pesan: *"Gagal tambah: Total bobot akan melebihi 1.0"* | ✅ Berhasil | Validasi di `app.py` baris 970—973 |
| 25 | TC-KRT-03 | Mengedit bobot kriteria — total tetap 1.0 | Bobot C1 diubah dari 0.25 menjadi 0.20, diimbangi dengan perubahan kriteria lain | 1. Buka `/kriteria` <br>2. Edit bobot C1 menjadi 0.20 <br>3. Simpan perubahan | Sistem menyimpan perubahan bobot dan menampilkan pesan sukses: *"Kriteria berhasil diupdate."* Total bobot tetap valid | ✅ Berhasil | — |
| 26 | TC-KRT-04 | Mengedit bobot kriteria — total melebihi 1.0 | Bobot C1 diubah dari 0.25 menjadi 0.90 (sehingga total > 1.0) | 1. Buka `/kriteria` <br>2. Edit bobot C1 menjadi 0.90 <br>3. Klik Simpan | Sistem menolak perubahan dan menampilkan pesan error: *"Gagal edit: Total bobot melebihi 1.0"* | ✅ Berhasil | Validasi di `app.py` baris 990—992 |
| 27 | TC-KRT-05 | Simpan semua bobot sekaligus — total valid (= 1.0) | Semua bobot diatur ulang sehingga totalnya persis 1.0 | 1. Buka `/kriteria` <br>2. Ubah nilai semua bobot melalui fitur "Simpan Semua Bobot" <br>3. Total diatur = 1.0 | Sistem menyimpan semua bobot sekaligus dan menampilkan pesan sukses: *"Seluruh bobot berhasil diperbarui."* | ✅ Berhasil | Aksi `save_all_bobot` di `app.py` baris 1003 |
| 28 | TC-KRT-06 | Simpan semua bobot — total tidak sama dengan 1.0 | Semua bobot diatur sehingga totalnya = 0.85 (bukan 1.0) | 1. Ubah bobot sehingga total < 1.0 <br>2. Klik Simpan Semua Bobot | Sistem menolak penyimpanan dan menampilkan pesan error: *"Total seluruh bobot harus persis 1.0!"* | ✅ Berhasil | Validasi `round(total, 4) != 1.0` di `app.py` baris 1013 |
| 29 | TC-KRT-07 | Menghapus sebuah kriteria | Kriteria yang ada di database (misal: C7) | 1. Buka `/kriteria` <br>2. Klik tombol Hapus pada baris kriteria C7 <br>3. Konfirmasi penghapusan | Kriteria beserta seluruh sub-kriterianya (cascade delete) terhapus dari database. Daftar kriteria diperbarui. | ✅ Berhasil | Cascade delete via `relationship` SQLAlchemy |

### 5.2 Manajemen Sub-Kriteria

| No | Identifikasi | Deskripsi Pengujian | Data/Kondisi Masukan | Prosedur Pengujian | Hasil yang Diharapkan | Hasil Pengujian | Keterangan |
|:---:|:---|:---|:---|:---|:---|:---:|:---|
| 30 | TC-SKR-01 | Menampilkan sub-kriteria dari sebuah kriteria | Kriteria C1 memiliki 5 sub-kriteria | 1. Buka `/kriteria` <br>2. Klik ikon/tombol kelola sub-kriteria pada C1 | Halaman `/sub-kriteria/1` menampilkan 5 opsi sub-kriteria C1 beserta nama dan skor masing-masing | ✅ Berhasil | — |
| 31 | TC-SKR-02 | Menambah sub-kriteria baru | Nama: `Tanpa Penghasilan Sama Sekali`, Skor: `5` pada kriteria C1 | 1. Buka halaman sub-kriteria C1 <br>2. Isi form tambah sub-kriteria <br>3. Klik Simpan | Sub-kriteria baru tersimpan dan muncul dalam daftar sub-kriteria C1 | ✅ Berhasil | — |
| 32 | TC-SKR-03 | Mengedit sub-kriteria yang ada | Ubah nama sub-kriteria dari `≤ Rp 500.000 / Tidak Tetap` menjadi `≤ Rp 400.000 / Tidak Tetap`, skor tetap `5` | 1. Buka halaman sub-kriteria <br>2. Klik Edit pada sub-kriteria yang dipilih <br>3. Ubah nama dan klik Simpan | Perubahan nama sub-kriteria tersimpan. Pesan sukses: *"Sub-Kriteria berhasil diupdate."* | ✅ Berhasil | — |
| 33 | TC-SKR-04 | Menghapus sub-kriteria | Satu sub-kriteria dari C1 | 1. Buka halaman sub-kriteria C1 <br>2. Klik Hapus pada salah satu sub-kriteria | Sub-kriteria terhapus dari database. Daftar sub-kriteria diperbarui. | ✅ Berhasil | — |

---

## 6. Pengujian Modul Manajemen Histori

### 6.1 Tampilan dan Pencarian

| No | Identifikasi | Deskripsi Pengujian | Data/Kondisi Masukan | Prosedur Pengujian | Hasil yang Diharapkan | Hasil Pengujian | Keterangan |
|:---:|:---|:---|:---|:---|:---|:---:|:---|
| 34 | TC-HIS-01 | Menampilkan seluruh histori klasifikasi | Database memiliki data klasifikasi | 1. Login <br>2. Buka halaman `/history` | Halaman menampilkan seluruh data histori klasifikasi, diurutkan dari yang terbaru (descending berdasarkan `created_at`) | ✅ Berhasil | — |
| 35 | TC-HIS-02 | Pencarian histori berdasarkan NIK | Kata kunci: NIK yang terdaftar (misal: `1234567890123456`) | 1. Buka `/history` <br>2. Ketik NIK di kolom pencarian <br>3. Submit | Halaman menampilkan hanya data yang NIK-nya mengandung kata kunci pencarian | ✅ Berhasil | Pencarian `ilike` di `app.py` baris 1107 |
| 36 | TC-HIS-03 | Pencarian histori berdasarkan Nama | Kata kunci: Nama yang terdaftar (misal: `Budi`) | 1. Buka `/history` <br>2. Ketik nama di kolom pencarian <br>3. Submit | Halaman menampilkan semua record yang namanya mengandung kata kunci `Budi` | ✅ Berhasil | Pencarian case-insensitive |
| 37 | TC-HIS-04 | Pencarian histori berdasarkan Kelurahan | Kata kunci: `Pondok Aren` | 1. Buka `/history` <br>2. Ketik nama kelurahan di kolom pencarian <br>3. Submit | Halaman menampilkan hanya data warga dari Kelurahan Pondok Aren | ✅ Berhasil | — |
| 38 | TC-HIS-05 | Pencarian dengan kata kunci yang tidak ditemukan | Kata kunci: `DataTidakAda` | 1. Buka `/history` <br>2. Masukkan kata kunci yang tidak terdaftar <br>3. Submit | Halaman menampilkan daftar kosong (tidak ada data yang cocok) tanpa error | ✅ Berhasil | — |
| 39 | TC-HIS-06 | Filter histori berdasarkan kelurahan (API) | Parameter: `?kelurahan=Pondok Aren` | 1. Buka `/history` <br>2. Pilih salah satu kelurahan dari dropdown filter | Tabel histori diperbarui secara dinamis (AJAX) menampilkan hanya data dari kelurahan yang dipilih | ✅ Berhasil | Endpoint `/api/history` menangani filter ini |

### 6.2 Edit Data Histori

| No | Identifikasi | Deskripsi Pengujian | Data/Kondisi Masukan | Prosedur Pengujian | Hasil yang Diharapkan | Hasil Pengujian | Keterangan |
|:---:|:---|:---|:---|:---|:---|:---:|:---|
| 40 | TC-EDT-01 | Edit data identitas warga | Ubah nama dari `Budi Santoso` menjadi `Budi Santoso S.` | 1. Buka `/history` <br>2. Klik tombol Edit pada record yang dipilih <br>3. Ubah nama <br>4. Klik Simpan | Perubahan nama tersimpan, skor SAW dihitung ulang, dan halaman histori menampilkan data yang sudah diperbarui dengan pesan sukses | ✅ Berhasil | — |
| 41 | TC-EDT-02 | Edit data kriteria dan hitung ulang SAW | Ubah pilihan C1 dari `≤Rp500.000` menjadi `>Rp3.000.000` pada warga yang sebelumnya Layak | 1. Buka form edit record <br>2. Ubah pilihan sub-kriteria C1 <br>3. Klik Simpan | Skor SAW dihitung ulang menggunakan data yang diperbarui. Status kelayakan berubah menjadi **"Tidak Layak"**. Perubahan tersimpan ke database | ✅ Berhasil | Logika hitung ulang di `app.py` baris 1246 |
| 42 | TC-EDT-03 | Edit data dengan override status manual | Pilih `Override Status: Layak` meski skor SAW < 0.50 | 1. Buka form edit record <br>2. Pilih opsi override status menjadi "Layak" <br>3. Klik Simpan | Status tersimpan sebagai **"Layak"** meski skor SAW sebenarnya di bawah ambang batas (0.50). Override berjalan dengan benar | ✅ Berhasil | Logika override di `app.py` baris 1253—1255 |
| 43 | TC-EDT-04 | Edit dengan NIK kurang dari 16 digit | NIK diubah menjadi `12345` (5 digit) | 1. Buka form edit record <br>2. Ubah NIK menjadi 5 digit <br>3. Klik Simpan | Sistem menolak perubahan, menampilkan pesan error: *"NIK harus 16 digit angka"*, data tidak tersimpan | ✅ Berhasil | Validasi di `app.py` baris 1218 |

### 6.3 Hapus Data Histori

| No | Identifikasi | Deskripsi Pengujian | Data/Kondisi Masukan | Prosedur Pengujian | Hasil yang Diharapkan | Hasil Pengujian | Keterangan |
|:---:|:---|:---|:---|:---|:---|:---:|:---|
| 44 | TC-DEL-01 | Hapus satu record histori | ID record yang ada di database | 1. Buka `/history` <br>2. Klik tombol Hapus pada salah satu baris data <br>3. Konfirmasi penghapusan | Record terhapus dari database. Halaman histori diperbarui tanpa data tersebut. Pesan sukses: *"Data berhasil dihapus dari histori."* | ✅ Berhasil | Route `/delete/<id>` di `app.py` baris 1180 |
| 45 | TC-DEL-02 | Hapus semua data histori sekaligus | Beberapa data ada di database | 1. Buka `/history` <br>2. Klik tombol "Hapus Semua Data" <br>3. Konfirmasi penghapusan | Seluruh record di tabel `classification_results` terhapus. Dashboard kembali menunjukkan angka `0`. Pesan sukses: *"Seluruh data histori berhasil dihapus!"* | ✅ Berhasil | Route `/delete_all` di `app.py` baris 1380 |
| 46 | TC-DEL-03 | Hapus record dengan ID tidak valid | Akses URL `/delete/99999` (ID tidak ada) | 1. Coba kirim POST request ke `/delete/99999` | Sistem mengembalikan respons `404 Not Found` | ✅ Berhasil | `get_or_404()` di `app.py` |

---

## 7. Pengujian Modul Export Data

| No | Identifikasi | Deskripsi Pengujian | Data/Kondisi Masukan | Prosedur Pengujian | Hasil yang Diharapkan | Hasil Pengujian | Keterangan |
|:---:|:---|:---|:---|:---|:---|:---:|:---|
| 47 | TC-EXP-01 | Export seluruh histori ke Excel | Database memiliki data klasifikasi | 1. Buka `/history` <br>2. Klik tombol Export Excel (tanpa filter) | Browser mengunduh file Excel (`.xlsx`) bernama `Histori_Bansos_Semua.xlsx` berisi semua data histori | ✅ Berhasil | — |
| 48 | TC-EXP-02 | Export histori dengan filter kelurahan | Pilih filter kelurahan `Pondok Aren` sebelum export | 1. Pilih kelurahan `Pondok Aren` dari dropdown filter <br>2. Klik Export Excel | Browser mengunduh file Excel bernama `Histori_Bansos_Pondok_Aren.xlsx` yang hanya berisi data dari Kelurahan Pondok Aren | ✅ Berhasil | Nama file dinamis berdasarkan filter |
| 49 | TC-EXP-03 | Export saat data kosong | Database tidak memiliki data klasifikasi | 1. Kosongkan semua histori <br>2. Klik Export Excel | Browser mengunduh file Excel kosong (hanya baris header kolom, tanpa baris data) | ✅ Berhasil | — |
| 50 | TC-EXP-04 | Struktur kolom file Excel yang diekspor | File hasil export | 1. Lakukan export <br>2. Buka file Excel yang diunduh | File Excel memiliki kolom: Tgl/Waktu, NIK, No KK, Nama Lengkap, Pekerjaan, Alamat, Kelurahan, C1—C7 (nama kriteria dan skor), Skor SAW, Hasil Klasifikasi, Alasan | ✅ Berhasil | Kolom kriteria bersifat dinamis sesuai data di database |

---

## 8. Pengujian Modul Informasi SPK

| No | Identifikasi | Deskripsi Pengujian | Data/Kondisi Masukan | Prosedur Pengujian | Hasil yang Diharapkan | Hasil Pengujian | Keterangan |
|:---:|:---|:---|:---|:---|:---|:---:|:---|
| 51 | TC-INF-01 | Menampilkan halaman informasi SPK | Pengguna sudah login | 1. Login <br>2. Buka halaman `/informasi` | Halaman menampilkan penjelasan metode SAW, daftar kriteria (C1—C7) beserta tipe dan bobot masing-masing, serta informasi ambang batas kelayakan (0.50) | ✅ Berhasil | — |
| 52 | TC-INF-02 | Akses halaman informasi tanpa login | Pengguna belum login | 1. Akses langsung URL `/informasi` tanpa login | Sistem mengarahkan ke halaman login | ✅ Berhasil | Proteksi `is_logged_in()` |

---

## 9. Pengujian Modul Profil Admin

### 9.1 Edit Profil

| No | Identifikasi | Deskripsi Pengujian | Data/Kondisi Masukan | Prosedur Pengujian | Hasil yang Diharapkan | Hasil Pengujian | Keterangan |
|:---:|:---|:---|:---|:---|:---|:---:|:---|
| 53 | TC-PRF-01 | Menampilkan halaman profil | Pengguna sudah login | 1. Login <br>2. Buka `/profil` | Halaman menampilkan data profil admin saat ini (username, nama lengkap, foto profil) | ✅ Berhasil | — |
| 54 | TC-PRF-02 | Memperbarui nama lengkap admin | Nama lengkap baru: `Admin Kecamatan Pondok Aren` | 1. Buka `/profil` <br>2. Ubah nama lengkap <br>3. Klik Simpan | Nama lengkap tersimpan di database. Session diperbarui. Pesan sukses: *"Profil berhasil diperbarui."* | ✅ Berhasil | — |
| 55 | TC-PRF-03 | Upload foto profil format valid (.jpg) | File gambar `.jpg` berukuran normal | 1. Buka `/profil` <br>2. Upload foto `.jpg` <br>3. Klik Simpan | Foto profil tersimpan di folder `uploads/profiles/`. URL foto diperbarui di session dan tampilan halaman | ✅ Berhasil | — |

### 9.2 Ganti Password

| No | Identifikasi | Deskripsi Pengujian | Data/Kondisi Masukan | Prosedur Pengujian | Hasil yang Diharapkan | Hasil Pengujian | Keterangan |
|:---:|:---|:---|:---|:---|:---|:---:|:---|
| 56 | TC-PSW-01 | Ganti password dengan data valid | Password lama: benar, Password baru: `passwordBaru123`, Konfirmasi: `passwordBaru123` | 1. Buka `/ganti-password` <br>2. Isi semua field dengan benar <br>3. Klik Simpan | Password berhasil diubah. Pesan sukses ditampilkan. Pengguna diarahkan ke Dashboard | ✅ Berhasil | — |
| 57 | TC-PSW-02 | Ganti password dengan password lama salah | Password lama: `passwordSalah`, Password baru: `passwordBaru123` | 1. Buka `/ganti-password` <br>2. Masukkan password lama yang salah <br>3. Klik Simpan | Sistem menampilkan pesan error: *"Password lama salah."* Password tidak berubah | ✅ Berhasil | Validasi `check_password_hash()` di `app.py` baris 678 |
| 58 | TC-PSW-03 | Ganti password — konfirmasi tidak cocok | Password baru: `passwordBaru123`, Konfirmasi: `passwordBeda456` | 1. Buka `/ganti-password` <br>2. Isi password baru dan konfirmasi yang berbeda <br>3. Klik Simpan | Sistem menampilkan pesan error: *"Konfirmasi password tidak cocok."* Password tidak berubah | ✅ Berhasil | Validasi di `app.py` baris 680 |
| 59 | TC-PSW-04 | Ganti password — kurang dari 6 karakter | Password baru: `abc` (3 karakter), Konfirmasi: `abc` | 1. Buka `/ganti-password` <br>2. Masukkan password baru yang terlalu pendek <br>3. Klik Simpan | Sistem menampilkan pesan error: *"Password baru minimal 6 karakter."* Password tidak berubah | ✅ Berhasil | Validasi `len(password_baru) < 6` di `app.py` baris 682 |

---

## 10. Pengujian Riwayat Login

| No | Identifikasi | Deskripsi Pengujian | Data/Kondisi Masukan | Prosedur Pengujian | Hasil yang Diharapkan | Hasil Pengujian | Keterangan |
|:---:|:---|:---|:---|:---|:---|:---:|:---|
| 60 | TC-RWY-01 | Menampilkan riwayat login | Pengguna pernah login beberapa kali | 1. Login ke sistem <br>2. Buka `/riwayat-login` | Halaman menampilkan daftar riwayat login (maksimum 20 entri terbaru) beserta waktu login dan alamat IP | ✅ Berhasil | — |
| 61 | TC-RWY-02 | Riwayat login tercatat setiap login berhasil | — | 1. Logout dari sistem <br>2. Login kembali <br>3. Buka `/riwayat-login` | Entri baru dengan timestamp terkini dan IP address tercatat di daftar riwayat | ✅ Berhasil | Login history disimpan di tabel `login_history` |

---

## 11. Pengujian Logika Perhitungan SAW

| No | Identifikasi | Deskripsi Pengujian | Data/Kondisi Masukan | Prosedur Pengujian | Hasil yang Diharapkan | Hasil Pengujian | Keterangan |
|:---:|:---|:---|:---|:---|:---|:---:|:---|
| 62 | TC-SAW-01 | Verifikasi skor SAW — semua kriteria maksimum | C1=5, C2=5, C3=5, C4=5, C5=5, C6=5, C7=5 (skor maksimum semua kriteria) | 1. Input manual warga dengan skor tertinggi di semua kriteria <br>2. Lihat skor SAW di histori | Skor SAW = **(5/5×0.25) + (5/5×0.20) + (5/5×0.15) + (5/5×0.10) + (5/5×0.10) + (5/5×0.10) + (5/5×0.10) = 1.00**. Status: **Layak** | ✅ Berhasil | Verifikasi matematis mengkonfirmasi implementasi di `spk.py` |
| 63 | TC-SAW-02 | Verifikasi skor SAW — semua kriteria minimum | C1=1, C2=1, C3=1, C4=1, C5=1, C6=1, C7=1 (skor minimum semua kriteria) | 1. Input manual warga dengan skor terendah di semua kriteria <br>2. Lihat skor SAW di histori | Skor SAW = **(1/5×0.25) + (1/5×0.20) + (1/5×0.15) + (1/5×0.10) + (1/5×0.10) + (1/5×0.10) + (1/5×0.10) = 0.20**. Status: **Tidak Layak** | ✅ Berhasil | — |
| 64 | TC-SAW-03 | Verifikasi ambang batas kelayakan (0.50) | Skor SAW tepat di angka 0.50 | Hitung manual skor yang menghasilkan tepat 0.50 lalu verifikasi status | Warga dengan skor SAW = 0.50 mendapat status **"Layak"** (batas: `skor >= 0.50`) | ✅ Berhasil | Ambang batas `THRESHOLD_LAYAK = 0.50` di `config.py` |
| 65 | TC-SAW-04 | Verifikasi skor SAW — contoh di README | C1=5, C2=4, C3=4, C4=3, C5=4, C6=4, C7=3 | 1. Input data dengan skor seperti contoh README <br>2. Lihat skor SAW | Skor SAW = **(1.00×0.25) + (0.80×0.20) + (0.80×0.15) + (0.60×0.10) + (0.80×0.10) + (0.80×0.10) + (0.60×0.10) = 0.81**. Status: **Layak** | ✅ Berhasil | Sesuai contoh perhitungan di `README.md` |

---

## 12. Pengujian Keamanan Akses

| No | Identifikasi | Deskripsi Pengujian | Data/Kondisi Masukan | Prosedur Pengujian | Hasil yang Diharapkan | Hasil Pengujian | Keterangan |
|:---:|:---|:---|:---|:---|:---|:---:|:---|
| 66 | TC-SEC-01 | Akses seluruh halaman terproteksi tanpa login | Akses langsung `/dashboard`, `/classification`, `/history`, `/kriteria`, `/informasi`, `/profil` | 1. Tanpa login, ketik URL halaman terproteksi secara langsung di browser | Seluruh halaman mengarahkan pengguna ke halaman login (`/`) | ✅ Berhasil | Semua route menggunakan guard `is_logged_in()` |
| 67 | TC-SEC-02 | Akses API JSON tanpa login | Akses langsung `/api/history` | 1. Tanpa login, akses URL `/api/history` | Endpoint mengembalikan respons JSON `{"error": "Unauthorized"}` dengan status HTTP `401` | ✅ Berhasil | Guard di `app.py` baris 1127 |
| 68 | TC-SEC-03 | Proteksi session setelah logout | Setelah logout, mencoba akses halaman terproteksi | 1. Login ke sistem <br>2. Logout <br>3. Tekan tombol "Back" di browser atau akses `/dashboard` langsung | Sistem tetap mengarahkan ke halaman login karena session telah dibersihkan | ✅ Berhasil | `session.clear()` di route `/logout` |

---

## 13. Ringkasan Hasil Pengujian

| No | Modul yang Diuji | Jumlah Test Case | Berhasil (✅) | Gagal (❌) | Persentase Keberhasilan |
|:---:|:---|:---:|:---:|:---:|:---:|
| 1 | Autentikasi (Login & Logout) | 6 | 6 | 0 | 100% |
| 2 | Dashboard Statistik | 4 | 4 | 0 | 100% |
| 3 | Klasifikasi Manual | 6 | 6 | 0 | 100% |
| 4 | Import Massal | 6 | 6 | 0 | 100% |
| 5 | Manajemen Kriteria | 7 | 7 | 0 | 100% |
| 6 | Manajemen Sub-Kriteria | 4 | 4 | 0 | 100% |
| 7 | Tampilan & Pencarian Histori | 6 | 6 | 0 | 100% |
| 8 | Edit Data Histori | 4 | 4 | 0 | 100% |
| 9 | Hapus Data Histori | 3 | 3 | 0 | 100% |
| 10 | Export Data ke Excel | 4 | 4 | 0 | 100% |
| 11 | Informasi SPK | 2 | 2 | 0 | 100% |
| 12 | Profil Admin | 3 | 3 | 0 | 100% |
| 13 | Ganti Password | 4 | 4 | 0 | 100% |
| 14 | Riwayat Login | 2 | 2 | 0 | 100% |
| 15 | Logika Perhitungan SAW | 4 | 4 | 0 | 100% |
| 16 | Keamanan Akses | 3 | 3 | 0 | 100% |
| | **Total Keseluruhan** | **68** | **68** | **0** | **100%** |

---

## 14. Kesimpulan

Berdasarkan hasil pengujian Black Box Testing yang telah dilakukan terhadap **68 test case** yang mencakup seluruh modul fungsional Sistem Pendukung Keputusan (SPK) Klasifikasi Penerima Bantuan Sosial menggunakan metode SAW, diperoleh kesimpulan sebagai berikut:

1. **Seluruh 68 test case berhasil dieksekusi sesuai hasil yang diharapkan**, dengan tingkat keberhasilan **100%**.

2. **Modul Autentikasi** berfungsi dengan baik, termasuk validasi kredensial, proteksi session, dan pencatatan riwayat login.

3. **Modul Klasifikasi Data** (manual dan import massal) berhasil melakukan validasi input (NIK/No KK 16 digit) dan menghitung skor SAW dengan benar sesuai algoritma yang telah dirancang.

4. **Logika Perhitungan SAW** terbukti akurat secara matematis. Hasil pengujian TC-SAW-04 menunjukkan kesesuaian dengan contoh perhitungan yang tercantum dalam dokumentasi proyek (skor 0.81 untuk data contoh di README).

5. **Manajemen Kriteria** menerapkan validasi bobot dengan baik — sistem menolak perubahan apabila total bobot tidak persis sama dengan 1.0.

6. **Keamanan akses** telah diterapkan secara konsisten pada semua endpoint, baik halaman web (redirect ke login) maupun endpoint API JSON (respons 401 Unauthorized).

7. **Fitur Export Excel** menghasilkan file dengan struktur kolom yang dinamis mengikuti jumlah dan nama kriteria yang terdaftar di database.

Sistem ini dinyatakan **layak dan siap digunakan** sesuai dengan fungsionalitas yang telah dirancang dalam lingkup proyek kerja praktek ini.

---

*Dokumen ini dibuat sebagai bagian dari laporan Kerja Praktek — Sistem Klasifikasi Penerima Bantuan Sosial Kecamatan Pondok Aren.*
*Metode Pengujian: Black Box Testing | Tanggal Pengujian: Mei 2026*
