# Sistem Klasifikasi Bansos

Proyek ini adalah aplikasi web Flask untuk klasifikasi kelayakan bantuan sosial menggunakan metode SAW. Repository ini sudah dirapikan agar lebih aman untuk dibagikan ke GitHub tanpa ikut membawa database lokal, file upload, atau kredensial yang sensitif.

## Struktur Singkat

- `backend/` berisi aplikasi Flask, konfigurasi, dan logika perhitungan.
- `frontend/` berisi template HTML, CSS, JavaScript, dan aset tampilan.
- `docs/` berisi dokumentasi metodologi.
- `.env` berisi konfigurasi lokal dan tidak ikut diunggah ke GitHub.
- `.env.example` adalah contoh konfigurasi untuk pengguna lain.

## Menjalankan Proyek Secara Lokal

1. Pastikan Python sudah terpasang.
2. Instal dependensi:

```bash
pip install -r requirements.txt
```

3. Periksa file `.env`.
   File ini sudah disiapkan untuk penggunaan lokal. Jika ingin mengubah secret atau akun admin awal, edit nilainya di sana.

4. Jalankan aplikasi:

```bash
cd backend
python app.py
```

5. Buka browser ke:

```text
http://127.0.0.1:5000
```

Catatan:
- Jika `DATABASE_URL` tidak diisi, aplikasi otomatis memakai `SQLite`.
- Ini cocok untuk penggunaan lokal, demo, dan deployment sederhana seperti PythonAnywhere.

## Catatan Keamanan Sebelum Upload ke GitHub

- Jangan unggah file `.env`.
- Jangan unggah folder `backend/database/`.
- Jangan unggah folder `uploads/` dan `frontend/static/uploads/`.
- Jangan unggah folder `instruksi/` jika repository akan dibuat publik.
- Jika ingin membuat repo publik, sebaiknya ganti nilai `SPK_SECRET_KEY` lokal Anda.

## File yang Sudah Dikecualikan dari Git

Lihat `.gitignore`. File itu sudah disiapkan agar file runtime dan data lokal tidak ikut ter-push.

## Saran Setelah Repository Dibuat

- Buat repository GitHub dalam mode `Private` jika proyek masih aktif digunakan.
- Jika ingin dijadikan `Public`, pastikan database lokal tidak ikut terunggah.
- Setelah akun admin berhasil masuk, pertimbangkan mengganti password admin melalui aplikasi.

## Deploy ke PythonAnywhere dengan SQLite

Pendekatan ini paling cocok jika Anda ingin tetap memakai `SQLite` agar sesuai dengan laporan proyek.

### 1. Buat akun dan Web App

Di PythonAnywhere:

1. Buat akun lalu login.
2. Buka menu `Web`.
3. Klik `Add a new web app`.
4. Pilih `Manual configuration`.
5. Pilih versi Python yang tersedia, misalnya Python 3.10 atau 3.11.

### 2. Unggah kode proyek

Ada dua cara:

1. Clone dari GitHub di Bash console PythonAnywhere.
2. Atau upload zip proyek lalu extract.

Jika memakai GitHub, biasanya langkahnya seperti ini:

```bash
git clone https://github.com/jovankasuryadilla130705-tech/Kerja-Praktek-SPK-metode-SAW-BANSOS.git
cd Kerja-Praktek-SPK-metode-SAW-BANSOS
pip3.10 install --user -r requirements.txt
```

Sesuaikan `pip3.10` dengan versi Python yang Anda pilih di PythonAnywhere.

### 3. Konfigurasi environment lokal

Buat file `.env` di root proyek, lalu isi misalnya:

```text
SPK_SECRET_KEY=ganti-dengan-secret-random
SPK_DEFAULT_ADMIN_USERNAME=admin
SPK_DEFAULT_ADMIN_PASSWORD=password-admin-awal
FLASK_DEBUG=0
```

Jangan isi `DATABASE_URL` jika ingin tetap memakai SQLite.

### 4. Atur file WSGI

Gunakan file contoh [pythonanywhere_wsgi.py](C:\Jovankasd\kerja praktek\Sistem Klasifikasi bansos(Final)\pythonanywhere_wsgi.py:1) sebagai referensi untuk isi file WSGI PythonAnywhere Anda.

Intinya:
- arahkan `project_home` ke folder proyek Anda di PythonAnywhere
- load `app` dari `backend/app.py`

### 5. Atur Static Files

Di tab `Web` PythonAnywhere, tambahkan static mapping:

- URL: `/static/`
- Directory: `/home/NAMA_ANDA/Kerja-Praktek-SPK-metode-SAW-BANSOS/frontend/static/`

Ganti `NAMA_ANDA` dengan username PythonAnywhere Anda.

### 6. Reload dan uji aplikasi

Setelah WSGI dan static file selesai:

1. Klik `Reload`
2. Buka URL aplikasi Anda
3. Login dengan akun admin
4. Tambahkan data manual
5. Cek histori

Jika data tetap ada setelah reload web app, berarti SQLite berjalan normal di PythonAnywhere.
