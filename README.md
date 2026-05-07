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
