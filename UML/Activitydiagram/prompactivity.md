## PERAN & KONTEKS

Bertindaklah sebagai **Senior System Analyst** yang ahli dalam pemodelan UML untuk sistem informasi
akademik. Saya sedang menyusun **Laporan Kerja Praktek (KP)** tentang Sistem Pendukung Keputusan
(SPK) berbasis web untuk **klasifikasi penerima Bantuan Sosial (Bansos)** di Kecamatan Pondok Aren,
Kota Tangerang Selatan, menggunakan metode **Simple Additive Weighting (SAW)**.

Stack teknologi: Python Flask · SQLite · SQLAlchemy ORM · Jinja2 · Tailwind CSS.

---

## BATASAN KERAS (NON-NEGOTIABLE)

> ⚠️ DILARANG mengarang, menambah, atau mengasumsikan aktor, tabel database, fitur, atau
> logika sistem di luar data aktual yang tercantum di bawah ini. Jika ada ambiguitas,
> gunakan data di bawah sebagai satu-satunya sumber kebenaran.

---

## DATA AKTUAL SISTEM

### A. Aktor

| Kode   | Nama Aktor         | Peran        |
|--------|--------------------|--------------|
| A1     | Admin (Ketua Staf) | Administrator — akses penuh termasuk konfigurasi & manajemen pengguna |
| A2     | Staff (Pegawai)    | Operator — input data warga, proses SPK, ekspor laporan |
| A3     | Camat              | Eksekutif — read-only pada dashboard & laporan |

### B. Tabel Database yang Relevan

- `users` — menyimpan data akun (id, username, password_hash, role)
- `login_history` — log autentikasi (user_id, timestamp, status)
- `kriteria` — data kriteria SAW (id, nama, bobot, tipe: benefit/cost)
- `sub_kriteria` — nilai konversi sub kriteria (id, kriteria_id, label, nilai_konversi)
- `warga` — data calon penerima bansos
- `classification_results` — hasil kalkulasi SAW (warga_id, nilai_preferensi, status_kelayakan)

### C. Logika Metode SAW (Urutan Wajib)

Ambil bobot kriteria dari tabel kriteria
Ambil nilai konversi dari tabel sub_kriteria
Bangun matriks keputusan X (baris = warga, kolom = kriteria)
Normalisasi matriks → r_ij:

Benefit: r_ij = x_ij / max(x_j)
Cost:    r_ij = min(x_j) / x_ij


Hitung nilai preferensi → V_i = Σ (w_j × r_ij)
Bandingkan V_i dengan threshold 0.50:

V_i ≥ 0.50 → Status: LAYAK
V_i < 0.50 → Status: TIDAK LAYAK


Simpan hasil ke tabel classification_results


---

## TUGAS: ACTIVITY DIAGRAM — 4 ALUR ESENSIAL

Hasilkan analisis untuk **4 alur berikut**, masing-masing terdiri dari:
1. Narasi step-by-step (Bahasa Indonesia formal, EYD)
2. Kode PlantUML (Format A)
3. XML draw.io (Format B)

---

### ALUR 1 — Login & Autentikasi

**Aktor terlibat:** Admin ATAU Staff ATAU Camat (pilih "Pengguna" sebagai aktor generik)
**Partisi/Swimlane:** `Pengguna` | `Sistem` | `Database`

**Logika alur wajib (berurutan):**
START

→ Pengguna membuka halaman Login

→ Pengguna mengisi username & password → submit form

→ [Sistem] Validasi field kosong

→ [Kosong] Tampilkan pesan error "Field tidak boleh kosong" → kembali ke form

→ [Sistem] Query tabel users berdasarkan username

→ [Username tidak ditemukan] Tampilkan "Akun tidak ditemukan" → kembali ke form

→ [Sistem] Verifikasi password_hash

→ [Password salah] Tampilkan "Password salah" → kembali ke form

→ [Sistem] Rekam log ke tabel login_history (status: SUCCESS)

→ [Sistem] Buat session dengan data role pengguna

→ [Sistem] Redirect berdasarkan role:

→ Admin → /dashboard/admin

→ Staff → /dashboard/staff

→ Camat → /dashboard/camat

END

---

### ALUR 2 — Klasifikasi Bansos (Metode SAW)

**Aktor terlibat:** Admin, Staff
**Partisi/Swimlane:** `Admin/Staff` | `Sistem` | `Database`

**Logika alur wajib (berurutan):**
START

→ Admin/Staff membuka menu Klasifikasi Bansos

→ Admin/Staff memilih mode input:

→ [Manual] Mengisi form data warga satu per satu

→ [Import CSV] Mengunggah file CSV berisi data warga

→ [Sistem] Validasi data input

→ [Tidak valid] Tampilkan pesan error spesifik → kembali ke input

→ [Sistem] Query bobot kriteria dari tabel kriteria

→ [Sistem] Query nilai konversi dari tabel sub_kriteria

→ [Sistem] Bangun matriks keputusan X

→ [Sistem] Normalisasi matriks → r_ij

(Benefit: x_ij/max; Cost: min/x_ij)

→ [Sistem] Hitung nilai preferensi V_i = Σ(w_j × r_ij)

→ [Sistem] Evaluasi threshold (V_i ≥ 0.50 → LAYAK / < 0.50 → TIDAK LAYAK)

→ [Sistem] Simpan hasil ke tabel classification_results

→ [Sistem] Tampilkan tabel hasil klasifikasi ke layar

END

---

### ALUR 3 — Manajemen Data (CRUD Representatif)

**Konteks:** Gunakan **Manajemen Kriteria** sebagai studi kasus CRUD.
**Aktor terlibat:** Admin
**Partisi/Swimlane:** `Admin` | `Sistem` | `Database`

**Logika alur wajib (berurutan, mencakup semua operasi CRUD):**
START

→ Admin membuka menu Pengaturan SPK → Manajemen Kriteria

→ [Sistem] Query & tampilkan daftar kriteria dari tabel kriteria (READ)

→ Admin memilih aksi:
[CREATE]
→ Admin klik "Tambah Kriteria" → isi form (nama, bobot, tipe)
→ [Sistem] Validasi input (bobot harus numerik, total bobot ≤ 1.0)
    → [Tidak valid] Tampilkan error → kembali ke form
→ [Sistem] INSERT ke tabel `kriteria`
→ [Sistem] Tampilkan notifikasi sukses → refresh daftar

[UPDATE]
→ Admin klik "Edit" pada baris kriteria → form terisi data lama
→ Admin ubah data → submit
→ [Sistem] Validasi input
    → [Tidak valid] Tampilkan error → kembali ke form
→ [Sistem] UPDATE record di tabel `kriteria`
→ [Sistem] Tampilkan notifikasi sukses → refresh daftar

[DELETE]
→ Admin klik "Hapus" pada baris kriteria
→ [Sistem] Tampilkan konfirmasi dialog ("Yakin hapus?")
    → [Batal] Kembali ke daftar
    → [Konfirmasi] DELETE record dari tabel `kriteria`
→ [Sistem] Tampilkan notifikasi sukses → refresh daftar
END

---

### ALUR 4 — Ekspor Laporan Excel

**Aktor terlibat:** Admin, Staff, Camat
**Partisi/Swimlane:** `Pengguna` | `Sistem` | `Database`

**Logika alur wajib (berurutan):**
START

→ Pengguna membuka halaman Riwayat / Laporan

→ Pengguna (opsional) mengatur filter: periode tanggal, status kelayakan

→ Pengguna klik tombol "Ekspor Excel"

→ [Sistem] Query data dari tabel classification_results

JOIN warga untuk data lengkap penerima

→ [Sistem] Cek apakah data hasil query kosong

→ [Kosong] Tampilkan notifikasi "Tidak ada data untuk diekspor" → END

→ [Sistem] Generate file Excel menggunakan library (OpenPyXL)

→ Buat header kolom (No, Nama, NIK, Nilai V, Status, Tanggal)

→ Isi baris data dari hasil query

→ Terapkan formatting (bold header, border cell)

→ [Sistem] Kirim file sebagai HTTP response (attachment)

→ Browser Pengguna mengunduh file .xlsx

END

---

## SPESIFIKASI FORMAT OUTPUT (WAJIB DIIKUTI UNTUK SETIAP ALUR)

### FORMAT A — PlantUML Swimlane

**Aturan teknis wajib:**

Gunakan sintaks partisi: |#WarnaPastel| Nama Partisi |
ORIENTASI: TOP-DOWN (default). DILARANG KERAS menggunakan left to right direction
Gunakan elemen berikut sesuai konteks:

start / stop                    → titik awal dan akhir

:Nama Aksi;                     → activity (aksi)

if (kondisi?) then (ya)         → percabangan

else (tidak) / endif

fork / fork again / end fork    → paralel (jika ada)

note right: teks                → anotasi opsional
Swimlane MINIMAL terdiri dari: satu partisi Aktor + satu partisi Sistem

satu partisi Database (jika ada interaksi DB)


Blok partisi harus TERTUTUP dengan benar
Kode harus bisa langsung di-paste ke planttext.com atau draw.io

(Insert > Advanced > Edit Diagram) TANPA error syntax


### FORMAT B — XML draw.io (mxGraphModel, Uncompressed)

**Aturan teknis wajib:**
STRUKTUR UMUM:

<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1"
           tooltips="1" connect="1" arrows="1" fold="1" page="1"
           pageScale="1" pageWidth="1654" pageHeight="1169" math="0" shadow="0">

<root>

<mxCell id="0"/>

<mxCell id="1" parent="0"/>

<!-- elemen diagram di sini -->

</root>

</mxGraphModel>
ATURAN GEOMETRI:

Canvas: width ≥ 1400px, height ≥ 1200px (sesuaikan per alur)
Swimlane container (kolom vertikal):

· Lebar tiap kolom: 250px

· Kolom 1 (Aktor)   : x="0"

· Kolom 2 (Sistem)  : x="250"

· Kolom 3 (Database): x="500"

· height = jumlah_elemen × 80 + padding (minimal 800px)
Elemen Activity (rounded rectangle):

· width="180" height="50"

· Posisi x = center kolom − 90 (margin kiri kolom + 35)

· Posisi y mulai dari y="80", increment +80px per elemen
Elemen Decision (diamond):

· width="80" height="80"

· x = center kolom − 40
Elemen Start (filled circle): width="30" height="30"
Elemen End (double circle): width="30" height="30"
Edge (panah):

· source dan target merujuk id elemen yang benar

· Label percabangan (Ya/Tidak) wajib dicantumkan sebagai value pada edge

· style="edgeStyle=orthogonalEdgeStyle;rounded=0;"

ATURAN ID:

Setiap <mxCell> memiliki id unik (format: alur_no_elemen, contoh: "A1_start", "A1_v1")
Tidak boleh ada id duplikat dalam satu file XML

VALIDASI AKHIR:

Semua tag XML harus tertutup dengan benar
Tidak boleh ada node/edge yang memiliki koordinat identik (overlap)
parent id swimlane container harus benar (elemen child merujuk id container-nya)


---

## URUTAN PENYAJIAN OUTPUT

Sajikan dengan heading pemisah yang konsisten:
ALUR 1 — Login & Autentikasi
Narasi:

[narasi step-by-step, ±150 kata]
Format A — PlantUML:

[blok kode @startuml ... @enduml]
Format B — XML draw.io:

[blok kode <mxGraphModel> ... </mxGraphModel>]

ALUR 2 — Klasifikasi Bansos (Metode SAW)
[dst.]

> Jangan tambahkan penjelasan di luar struktur di atas kecuali catatan teknis singkat
> jika ada keterbatasan sintaks yang perlu diketahui pengguna.