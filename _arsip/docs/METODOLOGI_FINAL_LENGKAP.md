# BAB III
# ANALISIS DAN PERANCANGAN SISTEM

## 3.1 Analisis Sistem Berjalan vs Sistem Usulan
Sebelum merancang sistem, dilakukan analisis perbandingan antara proses yang ada sebelumnya dengan sistem yang diusulkan.

| Aspek | Sistem Berjalan (Manual) | Sistem Usulan (Terkomputerisasi) |
|---|---|---|
| **Objektivitas** | Penilaian subjektif berdasarkan pengamatan petugas. | Penilaian objektif dengan pembobotan SAW yang terukur. |
| **Kecepatan** | Data dihitung satu per satu, memakan waktu lama. | Kalkulasi otomatis (manual maupun massal/batch). |
| **Penyimpanan** | Arsip fisik atau file excel terpisah-pisah. | Database terpusat (SQLite) dengan histori yang rapi. |
| **Pelaporan** | Rekapitulasi dilakukan secara manual. | Fitur ekspor excel instan dengan filter kelurahan. |
| **Pencarian** | Mencari di tumpukan berkas/baris excel secara manual. | Pencarian dinamis berbasis NIK, Nama, dan Kelurahan. |

---

## 3.2 Arsitektur Sistem
Sistem ini menggunakan arsitektur **Monolithic Web Application** dengan alur data sebagai berikut:

```mermaid
graph LR
    User((Admin)) -- Request --> UI[Frontend: HTML/Tailwind/JS]
    UI -- AJAX/POST --> Flask[Backend: Flask API]
    Flask -- Query --> DB[(SQLite Database)]
    DB -- Result --> Flask
    Flask -- Logic/SAW --> Logic[Modul SPK: spk.py]
    Logic -- Score --> Flask
    Flask -- Response --> UI
```

---

## 3.3 Use Case Diagram
Use Case Diagram menggambarkan interaksi antara aktor (Admin Kecamatan) dengan fungsi-fungsi utama dalam sistem Pendukung Keputusan Bansos.

```mermaid
flowchart LR
    A[Admin Kecamatan]

    UC1([Login])
    UC2([Melihat Dashboard Statistik])
    UC3([Melakukan Klasifikasi Manual])
    UC4([Melakukan Import Massal dan Klasifikasi Batch])
    UC5([Melihat Informasi SPK])
    UC6([Mengelola Kriteria])
    UC7([Mengelola Sub-Kriteria])
    UC8([Melihat Histori Klasifikasi])
    UC9([Mencari dan Memfilter Histori])
    UC10([Mengekspor Histori ke Excel])
    UC11([Mengubah Data Histori dan Hitung Ulang SAW])
    UC12([Override Status Klasifikasi])
    UC13([Menghapus Satu Histori])
    UC14([Menghapus Seluruh Histori])
    UC15([Mengelola Profil Admin])
    UC16([Mengganti Password])
    UC17([Melihat Riwayat Login])
    UC18([Logout])

    A --- UC1
    A --- UC2
    A --- UC3
    A --- UC4
    A --- UC5
    A --- UC6
    A --- UC7
    A --- UC8
    A --- UC9
    A --- UC10
    A --- UC11
    A --- UC13
    A --- UC14
    A --- UC15
    A --- UC16
    A --- UC17
    A --- UC18

    UC11 -. include .-> UC12
    UC8 -. include .-> UC9
    UC8 -. include .-> UC10
```

---

## 3.4 Activity Diagram

### 3.4.1 Proses Login Admin
```mermaid
flowchart TD
    A([Mulai]) --> B[Admin membuka halaman login]
    B --> C[Admin mengisi username dan password]
    C --> D[Browser mengirim POST /login]
    D --> E{Database siap?}
    E -- Tidak --> F[Tampilkan pesan database bermasalah]
    F --> Z([Selesai])
    E -- Ya --> G[Backend mencari user berdasarkan username]
    G --> H{Password valid?}
    H -- Tidak --> I[Tampilkan pesan gagal login]
    I --> Z
    H -- Ya --> J[Simpan session user]
    J --> K[Simpan login_history]
    K --> L[Redirect ke dashboard]
    L --> Z
```

### 3.4.2 Proses Klasifikasi Manual
```mermaid
flowchart TD
    A([Mulai]) --> B[Admin membuka menu Klasifikasi Data]
    B --> C[Admin mengisi identitas warga dan memilih sub-kriteria]
    C --> D[Frontend memvalidasi NIK dan No. KK]
    D --> E[Browser mengirim POST /classification]
    E --> F[Backend mengekstrak skor dari sub-kriteria terpilih]
    F --> G{NIK dan No. KK valid?}
    G -- Tidak --> H[Tampilkan pesan validasi]
    H --> Z([Selesai])
    G -- Ya --> I[Ambil data pembanding dari database]
    I --> J[Tambahkan calon baru ke dataset SPK]
    J --> K[Hitung skor SAW dan status kelayakan]
    K --> L[Simpan record ke classification_results]
    L --> M[Commit database]
    M --> N[Redirect ke histori]
    N --> Z
```

### 3.4.3 Proses Import Massal dan Klasifikasi Batch
```mermaid
flowchart TD
    A([Mulai]) --> B[Admin memilih tab Import Massal]
    B --> C[Admin mengunggah file CSV/XLS/XLSX]
    C --> D[Browser mengirim file ke POST /classification]
    D --> E[Backend menyimpan file sementara]
    E --> F[Backend membaca file dengan pandas]
    F --> G[Ambil dataset SPK yang sudah ada]
    G --> H[Loop setiap baris data]
    H --> I[Validasi NIK dan No. KK]
    I --> J[Petakan nilai kolom ke sub-kriteria]
    J --> K[Isi skor default 3 jika tidak cocok]
    K --> L[Hitung SAW untuk calon]
    L --> M[Simpan record baru ke sesi database]
    M --> N{Masih ada baris?}
    N -- Ya --> H
    N -- Tidak --> O[Commit seluruh hasil import]
    O --> P[Hapus file sementara]
    P --> Q[Redirect ke histori]
    Q --> Z([Selesai])
```

---

## 3.5 Sequence Diagram

### 3.5.1 Skenario Klasifikasi Manual
```mermaid
sequenceDiagram
    actor Admin as Admin Kecamatan
    participant Browser as Browser (main.js)
    participant Backend as Flask Backend (app.py)
    participant DB as Database (penduduk.db)

    Admin->>Browser: Isi form warga dan pilih sub-kriteria
    Browser->>Backend: POST /classification
    Backend->>DB: SELECT kriteria dan sub_kriteria terpilih
    Backend->>DB: SELECT classification_results (dataset pembanding)
    DB-->>Backend: Dataset historis
    Backend->>Backend: hitung_status_kelayakan_dinamis()
    Backend->>DB: INSERT classification_results
    DB-->>Backend: Commit berhasil
    Backend-->>Browser: Redirect /history
    Browser-->>Admin: Histori dengan hasil baru tampil
```

### 3.5.2 Skenario Filter Histori dan Ekspor Excel
```mermaid
sequenceDiagram
    actor Admin as Admin Kecamatan
    participant Browser as Browser (main.js)
    participant Backend as Flask Backend (app.py)
    participant DB as Database (penduduk.db)

    Admin->>Browser: Pilih filter kelurahan / ketik pencarian
    Browser->>Backend: GET /api/history?kelurahan=...&search=...
    Backend->>DB: SELECT classification_results sesuai filter
    Backend->>DB: SELECT kriteria
    DB-->>Backend: Data histori dan kriteria
    Backend-->>Browser: JSON histori terurut skor_saw desc
    Browser-->>Admin: Tabel histori diperbarui
    Admin->>Browser: Klik Export Excel
    Browser->>Backend: GET /export/excel?kelurahan=...&search=...
    Backend->>DB: SELECT histori, kriteria, sub_kriteria
    DB-->>Backend: Data ekspor
    Backend-->>Browser: File .xlsx
    Browser-->>Admin: File berhasil diunduh
```

---

## 3.6 Class Diagram
Class Diagram memperlihatkan struktur kelas dan modul utama yang berjalan di lingkungan backend Flask dan SQLAlchemy.

```mermaid
classDiagram
    class User {
        +Integer id
        +String username
        +String password_hash
        +DateTime created_at
        +String nama_lengkap
        +String foto_profil
    }

    class ClassificationResult {
        +Integer id
        +String nik
        +String no_kk
        +String nama
        +String pekerjaan
        +String alamat
        +String kelurahan
        +Float skor_saw
        +String hasil_klasifikasi
        +String alasan
        +DateTime created_at
        +Text kriteria_details
    }

    class Kriteria {
        +Integer id
        +String kode
        +String nama
        +String tipe
        +Float bobot
    }

    class SubKriteria {
        +Integer id
        +Integer kriteria_id
        +String nama
        +Integer skor
    }

    class SPK_Logic {
        +get_kriteria_dari_db()
        +hitung_saw()
        +tentukan_kelayakan()
        +generate_alasan()
    }

    class App {
        +login()
        +dashboard()
        +classification()
        +history()
        +api_history()
        +export_excel()
    }

    ClassificationResult "1..*" -- "1" Kriteria : Referensi
    Kriteria "1" -- "1..*" SubKriteria : Memiliki
    App --> SPK_Logic : Memanggil
    App --> ClassificationResult : CRUD
    App --> User : Autentikasi
```

---

## 3.7 Perancangan Basis Data

### 3.7.1 Entity Relationship Diagram (ERD)
Sistem menggunakan database SQLite dengan skema relasional antar entitas admin, kriteria, dan hasil klasifikasi.

```mermaid
erDiagram
    USERS ||--o{ LOGIN_HISTORY : mencatat
    KRITERIA ||--o{ SUB_KRITERIA : memiliki

    USERS {
        int id PK
        varchar username UK
        varchar password_hash
        datetime created_at
        text nama_lengkap
        text foto_profil
    }

    LOGIN_HISTORY {
        int id PK
        int user_id FK
        datetime login_time
        varchar ip_address
        text user_agent
    }

    KRITERIA {
        int id PK
        varchar kode UK
        varchar nama
        varchar tipe
        float bobot
    }

    SUB_KRITERIA {
        int id PK
        int kriteria_id FK
        varchar nama
        int skor
    }

    CLASSIFICATION_RESULTS {
        int id PK
        varchar nik
        varchar no_kk
        varchar nama
        varchar pekerjaan
        text alamat
        varchar kelurahan
        varchar hasil_klasifikasi
        datetime created_at
        text alasan
        float skor_saw
        text kriteria_details
    }
```

### 3.7.2 Kamus Data
Kamus data menjelaskan detail teknis dari tabel utama yang digunakan dalam sistem.

#### 1. Tabel `users` (Data Akun Admin)
| Atribut | Tipe Data | Deskripsi |
|---|---|---|
| `id` | Integer | Primary Key, identitas unik admin. |
| `username` | Varchar | Username untuk login (Unique). |
| `password_hash` | Varchar | Password yang telah di-enkripsi. |
| `nama_lengkap` | Text | Nama asli administrator. |

#### 2. Tabel `kriteria` (Master Kriteria)
| Atribut | Tipe Data | Deskripsi |
|---|---|---|
| `id` | Integer | Primary Key. |
| `kode` | Varchar | Kode kriteria (C1, C2, dst). |
| `tipe` | Varchar | Jenis kriteria (Benefit / Cost). |
| `bobot` | Float | Nilai bobot kepentingan (0 - 1). |

#### 3. Tabel `classification_results` (Data Histori)
| Atribut | Tipe Data | Deskripsi |
|---|---|---|
| `nik` | Varchar | Nomor Induk Kependudukan (16 digit). |
| `skor_saw` | Float | Nilai akhir preferensi hasil kalkulasi. |
| `hasil_klasifikasi` | Varchar | Keputusan akhir (Layak / Tidak Layak). |
| `kriteria_details` | Text/JSON | Detail skor tiap kriteria saat diproses. |

---

## 3.8 Implementasi Metode SAW

### 3.8.1 Kriteria dan Bobot
Sistem menggunakan 7 kriteria dengan bobot yang dapat dikonfigurasi secara dinamis:

| Kode | Nama Kriteria | Tipe | Bobot |
|---|---|---|---|
| C1 | Penghasilan | Cost | 0.25 |
| C2 | Jumlah Tanggungan | Benefit | 0.20 |
| C3 | Kepemilikan Aset | Cost | 0.15 |
| C4 | Status Rumah | Cost | 0.10 |
| C5 | Kondisi Bangunan | Cost | 0.10 |
| C6 | Daya Listrik | Cost | 0.10 |
| C7 | Sumber Air | Cost | 0.10 |

### 3.8.2 Rumus Perhitungan
1. **Normalisasi ($r_{ij}$):**
   $$r_{ij} = \frac{x_{ij}}{max(x_{j})}$$
   *(Catatan: Untuk kriteria Cost, skor sub-kriteria telah dibalik pada database sehingga kondisi paling membutuhkan memiliki skor tertinggi).*

2. **Nilai Preferensi ($V_i$):**
   $$V_i = \sum_{j=1}^{n} (w_j \times r_{ij})$$

### 3.8.3 Contoh Perhitungan Manual
Misalkan data alternatif **A1** dengan skor kriteria:
- C1: 5, C2: 4, C3: 4, C4: 3, C5: 4, C6: 4, C7: 3
- Max skor tiap kriteria: 5

**Normalisasi:**
- C1: 5/5 = 1.00
- C2: 4/5 = 0.80
- C3: 4/5 = 0.80
- C4: 3/5 = 0.60
- C5: 4/5 = 0.80
- C6: 4/5 = 0.80
- C7: 3/5 = 0.60

**Skor Akhir ($V_1$):**
$$V_1 = (1.00 \times 0.25) + (0.80 \times 0.20) + (0.80 \times 0.15) + (0.60 \times 0.10) + (0.80 \times 0.10) + (0.80 \times 0.10) + (0.60 \times 0.10)$$
$$V_1 = 0.25 + 0.16 + 0.12 + 0.06 + 0.08 + 0.08 + 0.06 = \mathbf{0.81}$$

**Keputusan:**
Karena $0.81 \geq 0.50$, maka status adalah **Layak**.
