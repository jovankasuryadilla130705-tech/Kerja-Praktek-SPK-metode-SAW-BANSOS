# Kriteria dan Sub-Kriteria Sistem Pendukung Keputusan (SPK) Bansos
Dokumen ini menjelaskan daftar kriteria, bobot, tipe kriteria, serta sub-kriteria beserta skornya yang digunakan dalam perhitungan kelayakan penerima Bantuan Sosial (Bansos) menggunakan metode **Simple Additive Weighting (SAW)**.

---

## 1. Daftar Kriteria Utama
Sistem ini menggunakan **7 kriteria utama** yang relevan dengan kondisi sosial ekonomi warga di Kecamatan Pondok Aren.

| Kode | Nama Kriteria | Tipe | Bobot Awal | Deskripsi |
| :---: | :--- | :---: | :---: | :--- |
| **C1** | Penghasilan | Cost | 0.25 (25%) | Tingkat pendapatan bulanan kepala keluarga / rumah tangga. |
| **C2** | Jumlah Tanggungan | Benefit | 0.20 (20%) | Jumlah anggota keluarga yang tidak/belum berpenghasilan dan menjadi tanggungan. |
| **C3** | Kepemilikan Aset | Cost | 0.15 (15%) | Kepemilikan kendaraan atau barang elektronik berharga tinggi. |
| **C4** | Status Rumah | Cost | 0.10 (10%) | Status kepemilikan tempat tinggal yang dihuni saat ini. |
| **C5** | Kondisi Bangunan | Cost | 0.10 (10%) | Keadaan fisik/material utama rumah tempat tinggal. |
| **C6** | Daya Listrik | Cost | 0.10 (10%) | Daya listrik (VA) terpasang di rumah tinggal warga. |
| **C7** | Sumber Air | Cost | 0.10 (10%) | Ketersediaan dan kualitas sumber air bersih untuk kebutuhan sehari-hari. |

> [!NOTE]
> Nilai bobot di atas merupakan bobot default saat inisiasi database (`seed_kriteria` di [app.py](file:///c:/Jovankasd/kerja%20praktek/Sistem%20Klasifikasi%20bansos(Final)/backend/app.py#L303-L340)). Nilai bobot ini dapat diubah oleh administrator secara dinamis melalui menu **Manajemen Kriteria** di aplikasi.

---

## 2. Detail Sub-Kriteria dan Pembobotan Skor
Setiap kriteria memiliki beberapa pilihan sub-kriteria yang diberi skor dari **1 hingga 5**. 

> [!IMPORTANT]
> **Peningkatan/Pembalikan Skor pada Kriteria Tipe Cost:**
> Agar rumus normalisasi SAW dapat disamakan ($r_{ij} = \frac{x_{ij}}{max(x_j)}$), kriteria bertipe **Cost** menggunakan pembalikan skor pada level sub-kriteria. Pilihan yang menunjukkan kondisi ekonomi **paling rendah / paling membutuhkan** diberi skor **5**, sedangkan kondisi ekonomi **lebih mapan / kurang membutuhkan** diberi skor **1**.

Berikut adalah rincian sub-kriteria untuk masing-masing kriteria:

### C1. Penghasilan (Cost)
*Makin rendah penghasilan warga, makin tinggi skor kebutuhan bantuan.*
* **Skor 5:** $\le$ Rp 500.000 / Tidak Tetap
* **Skor 4:** Rp 500.001 - Rp 1.000.000
* **Skor 3:** Rp 1.000.001 - Rp 2.000.000
* **Skor 2:** Rp 2.000.001 - Rp 3.000.000
* **Skor 1:** > Rp 3.000.000

### C2. Jumlah Tanggungan (Benefit)
*Makin banyak tanggungan keluarga, makin tinggi skor kebutuhan bantuan.*
* **Skor 5:** > 4 Orang
* **Skor 4:** 4 Orang
* **Skor 3:** 3 Orang
* **Skor 2:** 2 Orang
* **Skor 1:** 1 Orang

### C3. Kepemilikan Aset (Cost)
*Makin sedikit aset berharga yang dimiliki, makin tinggi skor kebutuhan bantuan.*
* **Skor 5:** Tidak Memiliki Aset Apapun
* **Skor 4:** Memiliki Sepeda / Elektronik Sederhana
* **Skor 3:** Memiliki 1 Motor (Lama/Biasa)
* **Skor 2:** Memiliki Motor > 1 atau Motor Baru
* **Skor 1:** Memiliki Mobil

### C4. Status Rumah (Cost)
*Makin tidak pasti status tempat tinggal warga, makin tinggi skor kebutuhan bantuan.*
* **Skor 5:** Tidak Memiliki Tempat Tinggal
* **Skor 4:** Bukan Milik Sendiri (Lahan Negara/Ilegal)
* **Skor 3:** Sewa / Kontrak
* **Skor 2:** Menumpang (Keluarga)
* **Skor 1:** Milik Sendiri

### C5. Kondisi Bangunan (Cost)
*Makin buruk kondisi fisik bangunan tempat tinggal, makin tinggi skor kebutuhan bantuan.*
* **Skor 5:** Tanah / Atap Rumbia / Seng Rusak
* **Skor 4:** Bambu / Anyaman (Gubug)
* **Skor 3:** Papan / Kayu
* **Skor 2:** Semi Permanen
* **Skor 1:** Permanen

### C6. Daya Listrik (Cost)
*Makin kecil daya listrik yang digunakan (atau tidak memiliki listrik), makin tinggi skor kebutuhan bantuan.*
* **Skor 5:** Tanpa Listrik / Numpang
* **Skor 4:** 450 VA
* **Skor 3:** 900 VA
* **Skor 2:** 1300 VA
* **Skor 1:** > 2200 VA

### C7. Sumber Air (Cost)
*Makin sulit akses terhadap air bersih yang layak, makin tinggi skor kebutuhan bantuan.*
* **Skor 5:** Air Hujan / Beli Eceran
* **Skor 4:** Sungai / Mata Air
* **Skor 3:** Sumur Gali (Timba/Bersama)
* **Skor 2:** Sumur Bor (Pompa Pribadi)
* **Skor 1:** PDAM

---

## 3. Penerapan dalam Metode SAW
Skor sub-kriteria di atas dimasukkan ke dalam matriks keputusan $X$, dinormalisasi menjadi matriks $R$, kemudian dikalikan dengan bobot $W$ untuk menghasilkan nilai preferensi akhir $V$.

### Rumus Normalisasi
Karena skor kriteria tipe *Cost* telah dibalik saat disimpan, perhitungan normalisasi di sistem disederhanakan menggunakan rumus bertipe benefit untuk seluruh kriteria:
$$r_{ij} = \frac{x_{ij}}{max(x_j)}$$

### Rumus Skor Akhir (Preferensi)
$$V_i = \sum_{j=1}^{n} (w_j \times r_{ij})$$

### Ambang Batas Kelayakan
Berdasarkan parameter `THRESHOLD_LAYAK` yang diatur di [config.py](file:///c:/Jovankasd/kerja%20praktek/Sistem%20Klasifikasi%20bansos(Final)/backend/config.py#L84):
* **Skor $V_i \ge 0.50$** $\rightarrow$ **Layak** (Mendapatkan bantuan sosial)
* **Skor $V_i < 0.50$** $\rightarrow$ **Tidak Layak** (Tidak mendapatkan bantuan sosial)

---
*Dokumen ini diperbarui secara berkala menyesuaikan dengan parameter yang terkonfigurasi pada sistem.*
