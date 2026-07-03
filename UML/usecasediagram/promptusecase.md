## PERAN & KONTEKS

Bertindaklah sebagai **Senior System Analyst** berpengalaman dalam perancangan sistem informasi akademik.
Saya sedang menyusun **Laporan Kerja Praktek (KP)** yang membahas Sistem Pendukung Keputusan (SPK)
berbasis web untuk **klasifikasi penerima Bantuan Sosial (Bansos)** di Kecamatan Pondok Aren,
Kota Tangerang Selatan, menggunakan metode **Simple Additive Weighting (SAW)**.

Sistem dibangun dengan Python Flask, SQLite, dan menerapkan **Role-Based Access Control (RBAC)**
dengan tiga aktor.

---

## BATASAN KERAS (WAJIB DIPATUHI)

> ⚠️ DILARANG KERAS mengarang, menambah, atau mengasumsikan aktor, fitur, menu, atau use case
> di luar data aktual yang tercantum di bawah ini. Seluruh output harus 100% bersumber dari
> daftar aktor dan fitur berikut — tidak lebih, tidak kurang.

---

## DATA AKTUAL SISTEM

### A. Daftar Aktor & Hak Akses

| No | Aktor              | Peran         | Deskripsi Singkat                                                   |
|----|--------------------|---------------|---------------------------------------------------------------------|
| 1  | Admin (Ketua Staf) | Administrator | Akses penuh ke seluruh fitur sistem termasuk konfigurasi & manajemen pengguna |
| 2  | Staff (Pegawai)    | Operator      | Akses operasional: input data warga, proses klasifikasi SPK, ekspor laporan   |
| 3  | Camat              | Eksekutif     | Akses baca (read-only) pada dashboard dan laporan hasil klasifikasi           |

### B. Daftar Fitur / Menu Sistem (Terperinci)

**1. Autentikasi** *(Semua Aktor)*
- Login
- Logout
- Kelola Profil
- Ganti Password
- Riwayat Login

**2. Dashboard** *(Semua Aktor)*
- Lihat rekap statistik data bansos
- Lihat grafik visualisasi

**3. Manajemen Data SPK** *(Admin & Staff)*
- Klasifikasi Bansos Manual (input satu per satu)
- Klasifikasi Bansos via Import CSV (massal)
- Lihat Riwayat Data Warga
- Edit Data Warga
- Hapus Data Warga
- Ekspor Laporan (Excel/PDF)
- Lihat Informasi Kriteria

**4. Pengaturan SPK** *(Khusus Admin)*
- Manajemen Kriteria & Bobot
- Manajemen Sub Kriteria

**5. Pengaturan Pengguna** *(Khusus Admin)*
- Manajemen Akun (tambah, edit, hapus akun pengguna)

---

## TUGAS & FORMAT OUTPUT YANG DIMINTA

Hasilkan **tiga bagian output** secara berurutan dan lengkap:

---

### OUTPUT 1 — Narasi Analisis Use Case

Tulis penjelasan naratif dalam **Bahasa Indonesia formal (EYD)**, dengan sub-bagian per aktor:
- Jelaskan **secara deskriptif** bagaimana masing-masing aktor (Admin, Staff, Camat) berinteraksi
  dengan sistem secara keseluruhan.
- Sebutkan use case mana yang bersifat **`<<include>>`** (dipanggil wajib) dan
  **`<<extend>>`** (opsional/kondisional) jika relevan.
- Panjang narasi: ±200–350 kata, padat dan akademis.

---

### OUTPUT 2 — Tabel Skenario Use Case

Buat tabel dengan **kolom berikut**:

| No | Nama Use Case | Aktor | Deskripsi Singkat | Pra-kondisi | Pasca-kondisi |
|----|---------------|-------|-------------------|-------------|---------------|

Ketentuan:
- Setiap fitur dari daftar di atas harus muncul sebagai **satu baris use case**.
- Gunakan notasi aktor yang konsisten: `Admin`, `Staff`, `Camat`, atau kombinasi seperti `Admin, Staff`.
- Isi kolom deskripsi dengan kalimat aktif dan ringkas (maks. 15 kata).

---

### OUTPUT 3A — Kode PlantUML

Hasilkan kode PlantUML lengkap untuk **Use Case Diagram** dengan ketentuan:
- Gunakan sintaks `@startuml` ... `@enduml`.
- Gunakan `actor`, `usecase`, `rectangle` untuk batas sistem.
- Tandai relasi `<<include>>` dan `<<extend>>` di tempat yang tepat secara logis.
- Kelompokkan use case dalam **paket/kotak** berdasarkan modul
  (Autentikasi, Dashboard, Manajemen SPK, Pengaturan SPK, Pengaturan Pengguna).
- Kode harus **langsung dapat di-paste** ke editor PlantUML atau menu
  `Insert > Advanced > Edit Diagram` di draw.io tanpa error.

---

### OUTPUT 3B — XML draw.io (mxGraphModel, Uncompressed)

Hasilkan XML draw.io format `<mxGraphModel>` yang **siap diimpor** via
`Extras > Edit Diagram` di draw.io, dengan ketentuan teknis:

**Layout & Geometri:**
- Aktor (Admin, Staff, Camat) ditempatkan di **sisi kiri** diagram, tersusun vertikal
  dengan jarak antar aktor minimal `y: 150px`.
- Use case berbentuk **ellipse** ditempatkan di **area tengah-kanan**.
- Setiap modul use case dikelompokkan dalam **swimlane/group box** terpisah.
- Koordinat `x` dan `y` pada `<mxGeometry>` harus **diperkirakan secara logis**
  sehingga tidak ada node yang menumpuk (overlap).
- Lebar canvas minimal: `width="1400"`, tinggi minimal: `height="1200"`.
- Koneksi antar aktor dan use case menggunakan `edge` dengan `style="endArrow=open"`.
- Label relasi `<<include>>` dan `<<extend>>` ditambahkan pada edge yang relevan.

**Format Elemen:**
- Aktor: style `shape=mxgraph.flowchart.actor` atau `shape=umlActor`.
- Use Case: style `ellipse`.
- Batas sistem: `rounded rectangle` atau `swimlane`.

**Validasi:** Pastikan tag XML tertutup dengan benar dan struktur `<mxCell>`
memiliki atribut `id`, `value`, `style`, `vertex/edge`, dan `<mxGeometry>` yang lengkap.

---

## FORMAT PENYAJIAN AKHIR

Sajikan ketiga output dengan memisah file dengan nama yang jelas di dalam folder usecasediagram:
OUTPUT 1 — Narasi Use Case.md
OUTPUT 2 — Tabel Skenario Use Case.md
OUTPUT 3A — Kode PlantUML
OUTPUT 3B — XML draw.io

Jangan tambahkan penjelasan di luar keempat bagian tersebut kecuali catatan teknis
singkat jika ada keterbatasan yang perlu diketahui.