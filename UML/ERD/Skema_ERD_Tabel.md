# Skema Basis Data Fisik (ERD) - Sistem Klasifikasi Bansos

## Tabel 1: `users`
**Peran:** Menyimpan data akun seluruh pengguna sistem (Admin, Staff, Camat)

| No | Nama Kolom    | Tipe Data SQLite | Constraint                        |
|----|---------------|------------------|-----------------------------------|
| 1  | id            | INTEGER          | PRIMARY KEY, AUTOINCREMENT        |
| 2  | username      | VARCHAR          | UNIQUE, NOT NULL                  |
| 3  | password_hash | VARCHAR          | NOT NULL                          |
| 4  | nama_lengkap  | VARCHAR          | NOT NULL                          |
| 5  | foto_profil   | VARCHAR          | NULLABLE (path file gambar)       |
| 6  | role          | VARCHAR          | NOT NULL ('Admin'/'Staff'/'Camat')|
| 7  | is_active     | BOOLEAN          | NOT NULL, DEFAULT 1 (True)        |
| 8  | created_at    | DATETIME         | NOT NULL, DEFAULT CURRENT_TIMESTAMP|

**Relasi keluar:**
- `users.id` ← FK dari `login_history.user_id` (One-to-Many)

---

## Tabel 2: `login_history`
**Peran:** Mencatat riwayat setiap percobaan login ke sistem

| No | Nama Kolom | Tipe Data SQLite | Constraint                              |
|----|------------|------------------|-----------------------------------------|
| 1  | id         | INTEGER          | PRIMARY KEY, AUTOINCREMENT              |
| 2  | user_id    | INTEGER          | FOREIGN KEY → users.id, NOT NULL        |
| 3  | login_time | DATETIME         | NOT NULL, DEFAULT CURRENT_TIMESTAMP     |
| 4  | ip_address | VARCHAR          | NULLABLE                                |
| 5  | user_agent | TEXT             | NULLABLE                                |

**Relasi masuk:**
- `login_history.user_id` → FK ke `users.id` (Many-to-One)

---

## Tabel 3: `kriteria`
**Peran:** Menyimpan definisi kriteria penilaian yang digunakan dalam metode SAW

| No | Nama Kolom | Tipe Data SQLite | Constraint                        |
|----|------------|------------------|-----------------------------------|
| 1  | id         | INTEGER          | PRIMARY KEY, AUTOINCREMENT        |
| 2  | kode       | VARCHAR          | UNIQUE, NOT NULL                  |
| 3  | nama       | VARCHAR          | NOT NULL                          |
| 4  | tipe       | VARCHAR          | NOT NULL ('benefit' / 'cost')     |
| 5  | bobot      | FLOAT            | NOT NULL (nilai 0.0 hingga 1.0)   |

**Relasi keluar:**
- `kriteria.id` ← FK dari `sub_kriteria.kriteria_id` (One-to-Many)

---

## Tabel 4: `sub_kriteria`
**Peran:** Menyimpan label dan nilai konversi skor untuk setiap sub-kriteria turunan

| No | Nama Kolom  | Tipe Data SQLite | Constraint                         |
|----|-------------|------------------|------------------------------------|
| 1  | id          | INTEGER          | PRIMARY KEY, AUTOINCREMENT         |
| 2  | kriteria_id | INTEGER          | FOREIGN KEY → kriteria.id, NOT NULL|
| 3  | nama        | VARCHAR          | NOT NULL (label sub kriteria)      |
| 4  | skor        | INTEGER          | NOT NULL (nilai konversi)          |

**Relasi masuk:**
- `sub_kriteria.kriteria_id` → FK ke `kriteria.id` (Many-to-One)

---

## Tabel 5: `classification_results`
**Peran:** Menyimpan data lengkap warga beserta hasil kalkulasi SAW dan status kelayakan.
**Catatan desain penting:** Tabel ini secara fisik berdiri sendiri (standalone) — tidak memiliki Foreign Key ke tabel manapun.

| No | Nama Kolom          | Tipe Data SQLite | Constraint / Keterangan                    |
|----|---------------------|------------------|--------------------------------------------|
| 1  | id                  | INTEGER          | PRIMARY KEY, AUTOINCREMENT                 |
| 2  | nik                 | VARCHAR          | NOT NULL (Nomor Induk Kependudukan)        |
| 3  | no_kk               | VARCHAR          | NOT NULL (Nomor Kartu Keluarga)            |
| 4  | nama                | VARCHAR          | NOT NULL                                   |
| 5  | pekerjaan           | VARCHAR          | NULLABLE                                   |
| 6  | alamat              | TEXT             | NULLABLE                                   |
| 7  | kelurahan           | VARCHAR          | NULLABLE                                   |
| 8  | penghasilan         | VARCHAR          | NOT NULL (input kriteria SAW)              |
| 9  | jumlah_tanggungan   | VARCHAR          | NOT NULL (input kriteria SAW)              |
| 10 | status_rumah        | VARCHAR          | NOT NULL (input kriteria SAW)              |
| 11 | kondisi_bangunan    | VARCHAR          | NOT NULL (input kriteria SAW)              |
| 12 | sumber_air          | VARCHAR          | NOT NULL (input kriteria SAW)              |
| 13 | daya_listrik        | VARCHAR          | NOT NULL (input kriteria SAW)              |
| 14 | kriteria_details    | TEXT             | JSON string — skor tiap kriteria per warga |
| 15 | skor_saw            | FLOAT            | Hasil akhir V_i = Σ(w_j × r_ij)            |
| 16 | hasil_klasifikasi   | VARCHAR          | 'LAYAK' atau 'TIDAK LAYAK'                 |
| 17 | alasan              | TEXT             | NULLABLE (penjelasan hasil)                |
| 18 | created_at          | DATETIME         | NOT NULL, DEFAULT CURRENT_TIMESTAMP        |

**Relasi:** TIDAK ADA Foreign Key keluar maupun masuk (standalone table by design).
