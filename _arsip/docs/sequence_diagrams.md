# Sequence Diagrams: Sistem Klasifikasi Bansos (Metode SAW)

Dokumen ini berisi **6 Sequence Diagram** yang identik dengan 6 Activity Diagram yang sudah dibuat,
lengkap dengan pembagian lifeline **BCE (Boundary, Control, Entity)**:

| Stereotipe | Peran | Contoh di Sistem Ini |
|---|---|---|
| **«boundary»** | Antarmuka / UI yang berinteraksi langsung dengan pengguna | Halaman Login, Halaman Klasifikasi, Halaman Histori, dll. |
| **«control»** | Logika pemrosesan, validasi, dan kalkulasi | Sistem Flask (app.py), Modul SPK (spk.py) |
| **«entity»** | Data persisten / model database | Database `users`, `classification_results`, `kriteria`, `sub_kriteria` |

> **Cara Import ke Draw.io:**
> 1. Copy salah satu blok `@startuml ... @enduml` di bawah.
> 2. Buka Draw.io → menu **Arrange → Insert → Advanced → PlantUML...**
> 3. Paste kodenya → klik **Insert**.
> Draw.io akan otomatis menampilkan ikon BCE (boundary = lingkaran+garis, control = lingkaran+panah, entity = lingkaran+garis bawah).

---

## Diagram 1: Proses Login

```plantuml
@startuml
title Sequence Diagram — Proses Login

actor Admin

boundary "Halaman Login\n«boundary»" as UI
control "Sistem Flask\n(app.py) «control»" as App
entity "Database\n(users) «entity»" as DB

== Membuka Halaman ==
Admin -> UI : Membuka Halaman Login
activate UI
UI --> Admin : Menampilkan Form Login
deactivate UI

== Proses Login ==
Admin -> UI : Memasukkan Username & Password\nlalu Klik Tombol Login
activate UI
UI -> App : POST /login (username, password)
activate App

App -> DB : Query User berdasarkan username
activate DB
DB --> App : Kembalikan objek User
deactivate DB

App -> App : Verifikasi password_hash\n(check_password_hash)

alt [Kredensial VALID]
    App -> DB : INSERT riwayat login\n(LoginHistory)
    activate DB
    DB --> App : Konfirmasi simpan
    deactivate DB
    App -> App : Simpan session\n(user_id, username, foto_profil)
    App --> UI : HTTP Redirect → /dashboard
    UI --> Admin : Menampilkan Halaman Dashboard
else [Kredensial TIDAK VALID]
    App --> UI : Flash Message "Username atau password salah"
    UI --> Admin : Menampilkan Pesan Error\n(kembali ke form login)
end

deactivate App
deactivate UI
@enduml
```

---

## Diagram 2: Proses Klasifikasi Manual

```plantuml
@startuml
title Sequence Diagram — Proses Klasifikasi Manual

actor Admin

boundary "Halaman Klasifikasi\n«boundary»" as UI
control "Sistem Flask &\nModul SPK «control»" as App
entity "Database «entity»" as DB

== Membuka Halaman ==
Admin -> UI : Membuka Menu Klasifikasi Data
activate UI
UI -> App : GET /classification
activate App
App -> DB : Ambil daftar Kriteria & SubKriteria
activate DB
DB --> App : Data kriteria dinamis
deactivate DB
App --> UI : Render Halaman Form Klasifikasi (Tab Manual)
UI --> Admin : Menampilkan Form Input Data Warga
deactivate App
deactivate UI

== Mengisi dan Mengirim Form ==
Admin -> UI : Mengisi Data Identitas Warga\n(NIK, No KK, Nama, Pekerjaan,\nAlamat, Kelurahan)
Admin -> UI : Memilih Nilai Sub-Kriteria\n(C1–C7)
Admin -> UI : Klik Tombol "Klasifikasikan"
activate UI
UI -> App : POST /classification (data form)
activate App

App -> App : Validasi Format NIK & No KK\n(harus 16 digit angka)

alt [Format TIDAK VALID]
    App --> UI : Flash Error & Redirect
    UI --> Admin : Menampilkan Pesan Error Format
else [Format VALID]
    App -> DB : Ambil semua data warga\n(sebagai baseline SAW)
    activate DB
    DB --> App : Daftar data warga tersimpan
    deactivate DB

    App -> App : Ekstrak skor per kriteria dari form
    App -> App : Hitung Skor SAW\n(Normalisasi Matriks × Bobot Kriteria C1–C7)\n[modul spk.py]
    App -> App : Tentukan Status Kelayakan\n(Layak / Tidak Layak)\nberdasarkan Threshold SAW

    App -> DB : INSERT ClassificationResult baru\n(skor SAW, hasil, alasan, kriteria_details)
    activate DB
    DB --> App : Konfirmasi simpan sukses
    deactivate DB

    App --> UI : Flash Sukses & Redirect → /history
    UI --> Admin : Menampilkan Halaman Histori Data
end

deactivate App
deactivate UI
@enduml
```

---

## Diagram 3: Proses Import Massal dan Klasifikasi Batch

```plantuml
@startuml
title Sequence Diagram — Proses Import Massal dan Klasifikasi Batch

actor Admin

boundary "Halaman Import Massal\n«boundary»" as UI
control "Sistem Flask &\nModul SPK «control»" as App
entity "Database «entity»" as DB

== Membuka Tab Import ==
Admin -> UI : Membuka Menu Klasifikasi Data
Admin -> UI : Memilih Tab "Import Massal"
activate UI
UI -> App : GET /classification
activate App
App --> UI : Render Form Upload File
UI --> Admin : Menampilkan Form Upload (Excel/CSV)
deactivate App
deactivate UI

== Upload dan Validasi File ==
Admin -> UI : Memilih File Excel/CSV\nlalu Klik Upload
activate UI
UI -> App : POST /classification (file)
activate App

App -> App : Validasi Ekstensi File\n(.csv, .xls, .xlsx)

alt [Ekstensi TIDAK VALID]
    App --> UI : Flash Error Format File
    UI --> Admin : Menampilkan Pesan Error Format
else [Ekstensi VALID]
    App -> App : Baca file ke DataFrame (Pandas)
    App -> App : Validasi NIK & No KK setiap baris\n(harus 16 digit angka)

    alt [Data Baris TIDAK VALID]
        App --> UI : Flash Error Detail Baris Salah
        UI --> Admin : Menampilkan Pesan Error Baris
    else [Data Baris VALID]
        App -> DB : Ambil data warga baseline
        activate DB
        DB --> App : Daftar data warga tersimpan
        deactivate DB

        App -> DB : Ambil Kriteria & SubKriteria
        activate DB
        DB --> App : Data kriteria & sub-kriteria
        deactivate DB

        loop [Iterasi setiap baris data]
            App -> App : Petakan nilai kolom ke Sub-Kriteria (C1–C7)
            App -> App : Hitung Skor SAW\n& Tentukan Status Kelayakan
            App -> App : Buat objek ClassificationResult\n(tambahkan ke session)
        end

        App -> DB : Batch Commit\n(Simpan semua record sekaligus)
        activate DB
        DB --> App : Konfirmasi simpan sukses (N record)
        deactivate DB

        App --> UI : Flash Sukses "Berhasil proses N data"\n& Redirect → /history
        UI --> Admin : Menampilkan Halaman Histori Data
    end
end

deactivate App
deactivate UI
@enduml
```

---

## Diagram 4: Proses Filter, Pencarian, dan Ekspor Histori

```plantuml
@startuml
title Sequence Diagram — Proses Filter, Pencarian, dan Ekspor Histori

actor Admin

boundary "Halaman Histori\n«boundary»" as UI
control "Sistem Flask\n(app.py) «control»" as App
entity "Database\n(classification_results) «entity»" as DB

== Membuka Halaman Histori ==
Admin -> UI : Membuka Halaman Histori Data
activate UI
UI -> App : GET /history
activate App
App -> DB : SELECT semua ClassificationResult\n(ORDER BY created_at DESC)
activate DB
DB --> App : Daftar histori klasifikasi
deactivate DB
App --> UI : Render tabel histori
UI --> Admin : Menampilkan Daftar Histori Klasifikasi
deactivate App
deactivate UI

== Alt 1: Pencarian Data ==
alt [Admin Melakukan Pencarian]
    Admin -> UI : Memasukkan Kata Kunci\n(NIK / Nama / Kelurahan) & Enter
    activate UI
    UI -> App : GET /history?search=keyword
    activate App
    App -> DB : SELECT dengan filter ILIKE\n(nik, nama, atau kelurahan)
    activate DB
    DB --> App : Hasil data yang cocok
    deactivate DB
    App --> UI : Render tabel hasil pencarian
    UI --> Admin : Menampilkan Hasil Pencarian
    deactivate App
    deactivate UI

== Alt 2: Ekspor ke Excel ==
else [Admin Melakukan Export Excel]
    Admin -> UI : (Opsional) Memilih Filter Kelurahan\nlalu Klik "Export Excel"
    activate UI
    UI -> App : GET /export-excel (+ parameter filter)
    activate App
    App -> DB : SELECT data sesuai filter kelurahan/keyword
    activate DB
    DB --> App : Data siap export
    deactivate DB
    App -> App : Petakan Sub-Kriteria ke Label teks\n(lookup skor → nama sub-kriteria)
    App -> App : Buat file .xlsx\n(menggunakan Pandas + openpyxl)
    App --> UI : Response sebagai file attachment\n(Content-Disposition: attachment)
    UI --> Admin : Browser mendownload File Excel
    deactivate App
    deactivate UI
end
@enduml
```

---

## Diagram 5: Proses Edit Histori dan Override Status

```plantuml
@startuml
title Sequence Diagram — Proses Edit Histori dan Override Status

actor Admin

boundary "Halaman Histori /\nForm Edit «boundary»" as UI
control "Sistem Flask &\nModul SPK «control»" as App
entity "Database\n(classification_results) «entity»" as DB

== Membuka Form Edit ==
Admin -> UI : Membuka Halaman Histori
Admin -> UI : Klik Tombol "Edit" pada Record
activate UI
UI -> App : GET /edit/<id>
activate App
App -> DB : SELECT ClassificationResult\nberdasarkan ID
activate DB
DB --> App : Data record terpilih
deactivate DB
App -> DB : Ambil daftar Kriteria & SubKriteria
activate DB
DB --> App : Data kriteria dinamis
deactivate DB
App --> UI : Render Form Edit\n(terisi data record terkini)
UI --> Admin : Menampilkan Form Edit Data Warga
deactivate App
deactivate UI

== Mengedit dan Menyimpan ==
Admin -> UI : Mengubah Data Identitas dan/atau\nNilai Sub-Kriteria (C1–C7)
Admin -> UI : (Opsional) Memilih Override Status\nManual (Layak / Tidak Layak)
Admin -> UI : Klik Tombol "Simpan Perubahan"
activate UI
UI -> App : POST /edit/<id> (data form)
activate App

App -> App : Validasi Format NIK & No KK\n(harus 16 digit angka)

alt [Format TIDAK VALID]
    App --> UI : Flash Error & Redirect ke form edit
    UI --> Admin : Menampilkan Pesan Error Format
else [Format VALID]
    App -> DB : Ambil data warga baseline\n(untuk kalkulasi SAW ulang)
    activate DB
    DB --> App : Daftar data warga
    deactivate DB

    App -> App : Hitung Ulang Skor SAW\ndengan data yang diperbarui\n[modul spk.py]

    alt [Admin Mengisi Override Status]
        App -> App : Gunakan status override manual\n(bukan hasil kalkulasi SAW)
    else [Tidak ada Override]
        App -> App : Gunakan hasil kalkulasi SAW
    end

    App -> DB : UPDATE ClassificationResult\n(skor_saw, hasil_klasifikasi, kriteria_details)
    activate DB
    DB --> App : Konfirmasi update sukses
    deactivate DB

    App --> UI : Flash Sukses & Redirect → /history
    UI --> Admin : Menampilkan Halaman Histori Data
end

deactivate App
deactivate UI
@enduml
```

---

## Diagram 6: Proses Manajemen Kriteria dan Sub-Kriteria

```plantuml
@startuml
title Sequence Diagram — Proses Manajemen Kriteria dan Sub-Kriteria

actor Admin

boundary "Halaman Kriteria /\nSub-Kriteria «boundary»" as UI
control "Sistem Flask\n(app.py) «control»" as App
entity "Database\n(kriteria, sub_kriteria) «entity»" as DB

== Membuka Halaman Kriteria ==
Admin -> UI : Membuka Menu Kriteria
activate UI
UI -> App : GET /kriteria
activate App
App -> DB : SELECT semua Kriteria\n(ORDER BY kode)
activate DB
DB --> App : Daftar kriteria & total bobot
deactivate DB
App --> UI : Render Halaman Daftar Kriteria\n(nama, tipe, bobot, total bobot)
UI --> Admin : Menampilkan Daftar Kriteria
deactivate App
deactivate UI

== Cabang A: Kelola Kriteria ==
alt [Admin Memilih Kelola Kriteria]
    Admin -> UI : Memilih Aksi Kriteria\n(Tambah / Edit / Hapus)
    activate UI
    UI -> App : POST /kriteria\n(action=add/edit/delete, data form)
    activate App

    alt [Aksi = Tambah atau Edit Kriteria]
        App -> DB : Hitung total bobot saat ini\n(SUM bobot semua kriteria)
        activate DB
        DB --> App : Total bobot saat ini
        deactivate DB
        App -> App : Validasi: total bobot baru ≤ 1.0

        alt [Total Bobot MELEBIHI 1.0]
            App --> UI : Flash Error Bobot
            UI --> Admin : Menampilkan Pesan Error Bobot
        else [Total Bobot VALID]
            App -> DB : INSERT / UPDATE Kriteria
            activate DB
            DB --> App : Konfirmasi simpan
            deactivate DB
            App --> UI : Flash Sukses & Redirect → /kriteria
            UI --> Admin : Menampilkan Halaman Kriteria Diperbarui
        end

    else [Aksi = Hapus Kriteria]
        App -> DB : DELETE Kriteria\n(cascade hapus sub-kriteria terkait)
        activate DB
        DB --> App : Konfirmasi hapus
        deactivate DB
        App --> UI : Flash Sukses & Redirect → /kriteria
        UI --> Admin : Menampilkan Halaman Kriteria Diperbarui
    end

    deactivate App
    deactivate UI

== Cabang B: Kelola Sub-Kriteria ==
else [Admin Memilih Kelola Sub-Kriteria]
    Admin -> UI : Membuka Halaman Sub-Kriteria\n(pilih satu Kriteria)
    activate UI
    UI -> App : GET /sub-kriteria/<kriteria_id>
    activate App
    App -> DB : SELECT SubKriteria\nberdasarkan kriteria_id
    activate DB
    DB --> App : Daftar sub-kriteria & skor
    deactivate DB
    App --> UI : Render Halaman Sub-Kriteria
    UI --> Admin : Menampilkan Daftar Sub-Kriteria
    deactivate App

    Admin -> UI : Memilih Aksi Sub-Kriteria\n(Tambah / Edit / Hapus) lalu Submit
    UI -> App : POST /sub-kriteria/<kriteria_id>\n(action=add/edit/delete, data form)
    activate App
    App -> DB : INSERT / UPDATE / DELETE SubKriteria
    activate DB
    DB --> App : Konfirmasi operasi
    deactivate DB
    App --> UI : Flash Sukses & Redirect → /sub-kriteria/<id>
    UI --> Admin : Menampilkan Halaman Sub-Kriteria Diperbarui
    deactivate App
    deactivate UI
end
@enduml
```
