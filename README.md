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

## Deploy Gratis ke Render dengan Supabase Postgres

Pendekatan ini cocok jika Anda tidak memiliki kartu pembayaran dan ingin data tetap tersimpan.

### 1. Buat Web Service

Di Render Dashboard:

1. Klik `New` > `Web Service`.
2. Hubungkan repository GitHub ini.
3. Gunakan pengaturan berikut:

- Runtime: `Python`
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn --chdir backend app:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 300`

### 2. Buat Project Database di Supabase

Di Supabase:

1. Buat project baru.
2. Buka menu `Connect`.
3. Ambil connection string PostgreSQL.
4. Pastikan format URL mengandung `sslmode=require`.

### 3. Tambahkan Environment Variables di Render

Isi variabel ini di Render:

- `SPK_SECRET_KEY`: isi dengan string acak panjang
- `SPK_DEFAULT_ADMIN_USERNAME`: misalnya `admin`
- `SPK_DEFAULT_ADMIN_PASSWORD`: password awal admin
- `DATABASE_URL`: connection string PostgreSQL dari Supabase

Opsional:

- `FLASK_DEBUG`: kosongkan atau isi `0`

### 4. Hal yang Perlu Diketahui

- Render `free web service` masih bisa sleep saat idle, jadi akses pertama bisa terasa lambat.
- Database utama sekarang sebaiknya disimpan di Supabase, bukan SQLite lokal.
- Import massal tetap akan lebih berat daripada input manual karena diproses di server dalam satu request.
- Foto profil yang diunggah ke filesystem lokal hosting gratis tetap tidak persisten. Jadi data inti aman, tetapi upload file lokal belum ideal untuk hosting gratis.

### 5. Setelah Deploy Berhasil

Setelah aplikasi online:

1. Coba login dengan akun admin awal.
2. Tambahkan 1 data manual.
3. Refresh halaman histori.
4. Redeploy service dari Render lalu cek lagi apakah data masih ada.

Jika data tetap ada setelah redeploy, berarti koneksi ke Supabase sudah bekerja dengan benar.
