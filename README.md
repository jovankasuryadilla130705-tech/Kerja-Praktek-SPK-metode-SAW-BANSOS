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

## Deploy ke Render dengan SQLite Persisten

Pendekatan ini cocok untuk proyek Anda saat ini karena aplikasi masih memakai Flask + SQLite.

### 1. Buat Web Service

Di Render Dashboard:

1. Klik `New` > `Web Service`.
2. Hubungkan repository GitHub ini.
3. Gunakan pengaturan berikut:

- Runtime: `Python`
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn --chdir backend app:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 300`

### 2. Tambahkan Persistent Disk

Masih di halaman service Render:

1. Tambahkan `Persistent Disk`.
2. Gunakan mount path:

```text
/opt/render/project/src/render_data
```

3. Pilih ukuran disk paling kecil dulu, misalnya `1 GB`.

Catatan: menurut dokumentasi Render, filesystem normal bersifat ephemeral dan hanya data di bawah mount path disk yang akan tetap ada setelah restart atau redeploy.

### 3. Tambahkan Environment Variables

Isi variabel ini di Render:

- `SPK_SECRET_KEY`: isi dengan string acak panjang
- `SPK_DEFAULT_ADMIN_USERNAME`: misalnya `admin`
- `SPK_DEFAULT_ADMIN_PASSWORD`: password awal admin
- `SPK_DATA_DIR`: `/opt/render/project/src/render_data`

Opsional:

- `FLASK_DEBUG`: kosongkan atau isi `0`

### 4. Hal yang Perlu Diketahui

- Render `free web service` tidak cocok untuk SQLite persisten karena free service tidak mendukung persistent disk dan bisa spin down. Jika ingin data tetap ada, gunakan instance berbayar yang mendukung disk.
- Import massal tetap akan lebih berat daripada input manual karena diproses di server dalam satu request.
- Konfigurasi proyek ini sudah diarahkan agar database SQLite dan file upload admin disimpan ke folder persistent tersebut.

### 5. Setelah Deploy Berhasil

Setelah aplikasi online:

1. Coba login dengan akun admin awal.
2. Tambahkan 1 data manual.
3. Refresh halaman histori.
4. Redeploy service dari Render lalu cek lagi apakah data masih ada.

Jika data tetap ada setelah redeploy, berarti persistent disk sudah bekerja dengan benar.
