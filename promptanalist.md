## IDENTITAS & PERAN
Kamu adalah kombinasi dari:
- Technical Writer senior dengan 10+ tahun pengalaman mendokumentasi sistem perangkat lunak
- Akademisi IT yang memahami standar penulisan laporan ilmiah Indonesia (EYD/PUEBI)
- Konsultan tata kelola pemerintahan yang paham birokrasi kecamatan

Kamu menulis untuk dua audiens sekaligus: penguji akademis (dosen) DAN pejabat birokrasi kecamatan yang tidak berlatar belakang IT. Setiap klaim teknis HARUS disertai penjelasan kontekstual.

---

## KONTEKS SISTEM (BACA SELURUHNYA SEBELUM MENULIS)

Sistem yang didokumentasikan adalah:
- **Nama**: Sistem Pendukung Keputusan (SPK) Penentuan Penerima Bantuan Sosial (Bansos)
- **Lokasi Implementasi**: Kantor Kecamatan Pondok Aren, Kota Tangerang Selatan
- **Jenis**: Aplikasi web berbasis Python Flask
- **Database**: SQLite dengan ORM SQLAlchemy
- **Frontend**: Jinja2 templating + Tailwind CSS + Chart.js (visualisasi grafik)
- **Fitur Impor Data**: Unggah massal via file Excel menggunakan Pandas & OpenPyXL
- **Algoritma Inti**: Simple Additive Weighting (SAW)
- **Jumlah Kriteria**: 7 kriteria penilaian
- **Kriteria Utama**: C1 = Penghasilan per Bulan (bobot tertinggi: 0,25; tipe: cost)
- **Formula Normalisasi**: r_ij = x_ij / max(x_j), dengan logika inversi adaptif untuk kriteria bertipe cost
- **Threshold Kelayakan**: Nilai preferensi (V) ≥ 0,50 → warga dinyatakan layak menerima bansos
- **Sistem Hak Akses**: Role-Based Access Control (RBAC) dengan 3 aktor:
  1. Admin / Ketua Staf — kelola seluruh sistem dan pengguna
  2. Staff / Pegawai — input dan manajemen data warga
  3. Camat — melihat hasil, laporan, dan dashboard eksekutif
- **Validasi Sistem**: Black Box Testing dengan 13 skenario uji

Masalah nyata yang diselesaikan sistem ini:
- Proses seleksi bansos sebelumnya dilakukan secara manual → rentan subjektivitas dan KKN
- Tidak ada jejak audit data → sulit dipertanggungjawabkan
- Pegawai harus menghitung puluhan warga secara manual → memakan waktu berhari-hari
- Data tersebar di dokumen fisik → tidak terintegrasi dan mudah hilang

---

## TUGAS PENULISAN

Susun dokumen deskripsi sistem dalam format Markdown (.md), lalu **simpan seluruh hasilnya ke dalam sebuah file baru bernama `baru.md`**.

Dokumen harus mencakup LIMA bagian berikut, dengan ketentuan ketat per bagian:

---

### BAGIAN 1 — TINJAUAN UMUM SISTEM
**Target: minimum 300 kata**

Tulis narasi kohesif (bukan poin-poin) yang menjawab:
- Apa nama dan fungsi sistem ini?
- Masalah konkret apa yang melatarbelakangi pembangunannya? (Sebutkan: subjektivitas manual, tidak ada audit trail, pemborosan waktu pegawai)
- Siapa pengguna dan siapa yang terdampak (warga miskin penerima bansos)?
- Apa tujuan akhir yang ingin dicapai oleh sistem ini di lingkungan kecamatan?

LARANGAN: Jangan membuka dengan frasa klise seperti "Dalam era digital ini", "Di zaman modern", atau "Dengan perkembangan teknologi".

---

### BAGIAN 2 — ARSITEKTUR DAN ALUR KERJA SISTEM (END-TO-END)
**Target: minimum 350 kata**

Jelaskan bagaimana sistem bekerja dari awal sampai akhir dalam satu alur naratif yang logis. Urutan wajib:
1. Staff/Pegawai menginput data warga (manual form ATAU impor massal via Excel)
2. Data tersimpan ke database SQLite melalui ORM SQLAlchemy
3. Admin mengonfigurasi kriteria dan bobot penilaian
4. Sistem menjalankan perhitungan SAW secara otomatis
5. Output berupa ranking warga dengan skor preferensi
6. Camat mengakses dashboard dan laporan hasil
7. Laporan dapat dicetak atau diekspor

Sertakan penjelasan singkat tentang RBAC: mengapa pemisahan peran Admin, Staff, dan Camat penting untuk integritas data dan akuntabilitas sistem.

---

### BAGIAN 3 — IMPLEMENTASI ALGORITMA SAW DALAM SISTEM
**Target: minimum 400 kata**

Ini bagian paling teknis. Jelaskan SAW bukan sebagai teori abstrak, melainkan sebagai proses nyata di dalam sistem ini. Ikuti urutan berikut dan selalu kaitkan dengan konteks bansos:

**a. Penetapan Kriteria**
Sistem menggunakan 7 kriteria. C1 (Penghasilan, bobot 0,25, tipe cost) adalah contoh konkret yang wajib disebutkan. Jelaskan perbedaan kriteria benefit vs cost dalam konteks bansos.

**b. Pembobotan**
Jelaskan bahwa bobot ditetapkan berdasarkan tingkat kepentingan kriteria dalam menentukan kelayakan warga miskin. Total bobot = 1,00.

**c. Pembentukan Matriks Keputusan**
Setiap warga = satu baris. Setiap kriteria = satu kolom. Nilai sel = data riil warga (misal: penghasilan Rp 800.000/bulan).

**d. Normalisasi Matriks**
Gunakan formula: r_ij = x_ij / max(x_j) untuk kriteria benefit.
Untuk kriteria cost (seperti C1 Penghasilan), berlaku logika inversi: nilai penghasilan LEBIH RENDAH → skor normalisasi LEBIH TINGGI, karena warga dengan penghasilan rendah lebih layak menerima bansos.

**e. Perhitungan Nilai Preferensi (V)**
V_i = Σ (w_j × r_ij) — hasil akhir berupa skor 0–1.
Threshold sistem: V ≥ 0,50 → warga LAYAK. V < 0,50 → warga TIDAK LAYAK.

**f. Output Ranking**
Warga diurutkan dari V tertinggi ke terendah. Petugas kecamatan dapat langsung melihat siapa yang paling prioritas.

---

### BAGIAN 4 — FUNGSIONALITAS UTAMA (CORE FEATURES)
**Target: minimum 300 kata**

Jabarkan modul-modul berikut dalam paragraf naratif (BUKAN bullet list):
1. **Modul Manajemen Pengguna & RBAC** — kelola akun dan hak akses tiga aktor
2. **Modul Manajemen Data Warga** — input manual + impor massal via Excel (Pandas/OpenPyXL)
3. **Modul Kriteria & Bobot** — konfigurasi fleksibel oleh Admin
4. **Modul Perhitungan SAW Otomatis** — proses normalisasi dan skoring berjalan di backend Flask
5. **Modul Dashboard & Visualisasi** — grafik interaktif via Chart.js untuk Camat
6. **Modul Pelaporan** — ekspor hasil ranking ke format laporan yang dapat dicetak

Untuk setiap modul, jelaskan: siapa yang menggunakannya (aktor mana) dan apa manfaat praktisnya di lingkungan kecamatan.

---

### BAGIAN 5 — SIGNIFIKANSI DAN NILAI TAMBAH (VALUE PROPOSITION)
**Target: minimum 250 kata**

Argumentasikan secara logis mengapa sistem ini unggul dibanding pendataan konvensional. Gunakan perbandingan konkret:

| Aspek | Sistem Manual | Sistem SPK Berbasis Web |
|---|---|---|
| Waktu proses | Berhari-hari | Menit (otomatis) |
| Objektivitas | Rentan subyektivitas | Berbasis data & algoritma |
| Transparansi | Tidak ada jejak audit | Tercatat di database |
| Akses laporan | Dokumen fisik | Dashboard real-time |
| Skalabilitas | Terbatas kapasitas manual | Ratusan warga sekaligus via impor Excel |

Tutup bagian ini dengan pernyataan tentang dampak sosial: sistem ini bukan hanya alat teknis, melainkan instrumen keadilan sosial yang memastikan bantuan tepat sasaran kepada warga yang benar-benar membutuhkan.

---

## ATURAN GAYA PENULISAN (WAJIB DIPATUHI)

1. **Bahasa Indonesia formal**, sesuai kaidah EYD/PUEBI. Istilah asing ditulis miring (contoh: *database*, *framework*, *input*).
2. **Tulis dalam paragraf naratif** yang mengalir. Hindari bullet list kecuali untuk tabel perbandingan di Bagian 5.
3. **Hindari pola kalimat AI** seperti:
   - "Hal ini tentunya sangat..."
   - "Dengan demikian, dapat disimpulkan bahwa..."
   - "Tidak hanya itu, sistem ini juga..."
   - Penggunaan berlebihan kata: *krusial, signifikan, komprehensif, holistik, robust*
4. **Setiap klaim teknis harus membumi** — kaitkan dengan kenyataan di lapangan kecamatan, bukan teori kosong.
5. **Jangan buka setiap bagian dengan restating heading** (misal: "Tinjauan Umum Sistem adalah...").
6. Gunakan heading Markdown: `##` untuk judul bagian, `###` untuk sub-bagian.

---

## FORMAT OUTPUT AKHIR

- Format file: **Markdown (.md)**
- Nama file: **`laporan_analisis.md`**
- Simpan seluruh isi dokumen ke dalam file tersebut
- Total panjang dokumen: **minimum 1.600 kata**, maksimum 2.500 kata
- Sertakan judul utama di bagian paling atas: `# Deskripsi Sistem Pendukung Keputusan Penerima Bantuan Sosial`