# Laporan Analisis Website: Sistem Klasifikasi Bansos (Metode SAW)

## 1. Pendahuluan
Website ini merupakan aplikasi **Sistem Pendukung Keputusan (SPK)** yang dirancang untuk membantu proses klasifikasi dan seleksi penerima Bantuan Sosial (Bansos) di Kecamatan Pondok Aren. Sistem ini dikembangkan untuk mengotomatisasi proses penilaian manual yang cenderung subjektif menjadi lebih terstruktur dan objektif dengan menggunakan algoritma **Simple Additive Weighting (SAW)**.

## 2. Arsitektur dan Teknologi
Berdasarkan peninjauan pada struktur repositori, aplikasi ini dibangun menggunakan pendekatan monolitik dengan _stack_ teknologi sebagai berikut:
- **Backend:** Python dengan framework **Flask**. Flask menangani routing, autentikasi, serta logika bisnis utama.
- **Database:** **SQLite** digunakan sebagai database default lokal melalui ORM **SQLAlchemy**.
- **Frontend:** **HTML**, **Tailwind CSS** (untuk penataan gaya), dan Vanilla **JavaScript** (beserta pustaka Chart.js untuk visualisasi data pada dashboard).
- **Pemrosesan Data:** Menggunakan **Pandas** dan **OpenPyXL** untuk memproses impor data massal dari file Excel (XLS/XLSX) dan CSV, serta ekspor hasil klasifikasi.

## 3. Analisis Fitur Utama
Sistem ini dirancang khusus untuk administrator internal dengan berbagai fitur yang terintegrasi secara baik:
- **Dashboard Analitik:** Menyediakan ringkasan visual seperti total data, distribusi status kelayakan (Layak/Tidak Layak), dan grafik demografi per kelurahan.
- **Klasifikasi Data (Manual & Massal):** Mendukung input data satuan maupun _batch processing_ melalui unggahan file Excel.
- **Manajemen Kriteria Dinamis:** Fitur unggulan di mana admin dapat menambah, mengedit, menghapus, serta mengatur bobot dan sub-kriteria beserta skornya secara dinamis melalui UI.
- **Manajemen Histori:** Seluruh hasil klasifikasi disimpan secara permanen. Admin dapat melakukan pencarian, penyaringan (_filtering_), perhitungan ulang, override status, hingga ekspor data ke Excel.

## 4. Analisis Algoritma (Metode SAW)
Algoritma SAW diimplementasikan secara dinamis di dalam modul `backend/spk.py`. Prosesnya meliputi:
1. **Pemetaan Skor:** Skor _Cost_ (misal: penghasilan tinggi) telah dibalik pada level sub-kriteria di database. Sehingga kondisi yang semakin "membutuhkan" (miskin) mendapat skor numerik lebih tinggi (misal: 5).
2. **Normalisasi:** Berkat pembalikan skor di atas, rumus normalisasi disederhanakan menjadi `r = nilai / max_skor` untuk seluruh kriteria (tidak perlu logika percabangan _Cost/Benefit_ saat normalisasi matematika).
3. **Penentuan Preferensi:** Sistem menghitung skor akhir (Skor SAW) yang merupakan akumulasi dari perkalian nilai normalisasi dengan bobot kriteria.
4. **Penentuan Status:** Warga dinyatakan **"Layak"** jika `skor_saw >= THRESHOLD_LAYAK` (secara bawaan di-_set_ 0.50), dan **"Tidak Layak"** jika sebaliknya. Sistem juga menghasilkan teks alasan/justifikasi secara dinamis berdasarkan kriteria apa yang paling berpengaruh bagi kandidat tersebut.

## 5. Kelebihan Sistem
- **Objektivitas:** Mengurangi bias manusia berkat penilaian berbasis formula matematis (SAW).
- **Fleksibilitas:** Manajemen kriteria yang dinamis memungkinkan pengguna (Kecamatan) untuk menyesuaikan indikator kemiskinan dan bobotnya di masa depan tanpa perlu mengubah source code aplikasi.
- **Alur Kerja Terintegrasi:** Dukungan _bulk import/export_ sangat menguntungkan instansi pemerintahan yang biasanya memegang data kependudukan dalam format _spreadsheet_.
- **Dokumentasi Baik:** Kode ditulis dengan cukup terstruktur dan proyek didokumentasikan dengan jelas melalui `README.md`.

## 6. Keterbatasan & Saran Pengembangan
Meskipun aplikasi sudah berfungsi dengan baik untuk skenario Kerja Praktek, ada beberapa poin yang dapat dikembangkan untuk level _production_:
- **Database Skala Besar:** Saat ini menggunakan SQLite. Jika volume data warga menjadi sangat masif dan ada beban konkuren (akses bersamaan), sangat disarankan untuk bermigrasi ke **PostgreSQL** atau **MySQL**.
- **Role Management:** Sistem ini masih bersifat _single-role_ (hanya Admin). Pengembangan ke depan bisa menambahkan level akses (misal: Petugas Lapangan untuk input data, Kepala Camat khusus untuk _view/approval_ laporan).
- **Audit Trail Lanjutan:** Selain riwayat log login, sistem bisa ditambahkan _log_ terkait siapa dan kapan suatu bobot kriteria diubah, untuk akuntabilitas.
- **Keamanan Deployment:** Pastikan `.env`, direktori `uploads/`, dan file database (`.db`) tidak dipublikasikan ke repository publik untuk melindungi data privasi warga yang sesungguhnya.

## 7. Kesimpulan
Aplikasi **Sistem Klasifikasi Bansos** ini adalah sebuah perangkat lunak fungsional yang sukses menerjemahkan proses manual yang lambat ke dalam alur digital terotomatisasi. Integrasi metode SAW di dalamnya diimplementasikan secara cerdas dengan pendekatan dinamis, sehingga aplikasi tidak kaku terhadap perubahan kebijakan kriteria penilaian bansos di masa mendatang. Secara keseluruhan, struktur kodenya terorganisir dengan rapi dan siap untuk dikembangkan lebih jauh.
