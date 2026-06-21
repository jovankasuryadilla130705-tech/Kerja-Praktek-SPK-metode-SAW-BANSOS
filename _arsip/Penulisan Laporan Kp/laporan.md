# BAB I PENDAHULUAN

## 1.1 Latar Belakang

Pengelolaan bantuan sosial adalah instrumen krusial pemerintah untuk menekan angka kemiskinan dan meningkatkan taraf hidup masyarakat prasejahtera. Agar program seperti Program Keluarga Harapan (PKH) berjalan efektif, penyalurannya harus transparan dan akurat (Altha Inas Shofyana et al., 2025; Purnomo et al., 2025). Akurasi data menjadi fondasi utama untuk mencapai tujuan kesejahteraan sosial tanpa adanya kecurangan dari pihak pelaksana (Limbong et al., 2023).

Namun, realita di Kantor Kecamatan Pondok Aren menunjukkan proses seleksi masih terhambat oleh subjektivitas dan inefisiensi manual. Berdasarkan data kependudukan (Dinas Kependudukan dan Pencatatan Sipil Kota Tangerang Selatan, 2025), dari sekitar 77.000 KK di 11 kelurahan, terdapat ±2.300 KK prasejahtera. Sementara itu, berdasarkan hasil observasi dan wawancara di instansi, kuota bansos rata-rata hanya 850 per tahun. Beban validasi yang hanya bertumpu pada 4–5 staf menyebabkan pengambilan keputusan menjadi lambat dan kurang transparan. Penilaian konvensional ini sering luput memperhatikan kriteria Kementerian Sosial, sehingga memicu risiko distribusi bantuan yang tidak adil (Altha Inas Shofyana et al., 2025).

Untuk mengatasi masalah tersebut, implementasi Sistem Pendukung Keputusan (SPK) menggunakan metode *Simple Additive Weighting* (SAW) menjadi solusi yang mendesak. SPK memfasilitasi komputasi cepat dengan biaya rendah (Limbong et al., 2023) untuk menghasilkan perankingan yang objektif (Larantukan et al., 2025). Pemilihan algoritma SAW didasarkan pada keunggulannya dalam mengolah kriteria kuantitatif dan kualitatif melalui proses normalisasi matriks serta penjumlahan terbobot (Adhika Pramita Widyassari et al., 2023; Naibaho, 2026). Metode ini secara ilmiah terbukti efektif memberikan urutan prioritas berdasarkan skor akhir tertinggi (Suprapto et al., 2024).

Sistem SPK tersebut dirancang berbasis web untuk meningkatkan aksesibilitas, akuntabilitas, dan validitas data seleksi. Platform ini memungkinkan petugas mengolah data secara *real-time* dan meminimalisasi risiko kehilangan dokumen fisik. Melalui Kerja Praktik berjudul "Sistem Pendukung Keputusan Kelayakan Penerima Bantuan Sosial Menggunakan Metode SAW Berbasis Web pada Kantor Kecamatan Pondok Aren", diharapkan terjadi transformasi pelayanan publik dari manual menuju digital. Dengan demikian, distribusi bantuan sosial dapat dipastikan lebih profesional, transparan, dan tepat sasaran bagi warga yang paling berhak.

## 1.2 Identifikasi Masalah

Berdasarkan uraian latar belakang di atas, permasalahan yang menjadi fokus penelitian ini dapat diidentifikasi sebagai berikut:

1. **Subjektivitas Penilaian.** Verifikasi manual oleh petugas rentan terhadap interpretasi individu, sehingga standar penilaian antarkëlurahan menjadi tidak seragam.
2. **Inefisiensi Data Manual.** Pengelolaan data konvensional mengakibatkan lambatnya rekapitulasi, tingginya risiko duplikasi, dan sulitnya pembaruan data secara *real-time*.
3. **Ketiadaan Sistem Pendukung Keputusan.** Belum adanya aplikasi perhitungan multikriteria membuat proses seleksi tidak transparan dan sulit dipertanggungjawabkan secara kuantitatif.

## 1.3 Tujuan Penulisan

Tujuan dari pelaksanaan Kerja Praktik dan penulisan laporan ini adalah:

1. **Pengembangan Perangkat Lunak.** Membangun aplikasi SPK berbasis web menggunakan metode SAW untuk menentukan kelayakan penerima bantuan secara otomatis dan objektif.
2. **Peningkatan Kualitas Layanan.** Mengoptimalkan efisiensi waktu, akurasi, dan transparansi proses seleksi di Kantor Kecamatan Pondok Aren melalui perankingan otomatis.
3. **Penerapan Ilmu Informatika.** Mengimplementasikan solusi metode SAW berbasis web di instansi kecamatan untuk mentransformasi seleksi manual menjadi keputusan digital yang terukur dan dapat dipertanggungjawabkan.

## 1.4 Batasan Permasalahan

Agar pembahasan tetap fokus dan terarah, batasan permasalahan ditetapkan sebagai berikut:

### 1.4.1 Batasan Masalah Penelitian

1. **Objek dan Lokasi.** Penelitian difokuskan pada pengolahan data warga di 11 kelurahan wilayah Kantor Kecamatan Pondok Aren. Data pengujian merupakan sampel yang disamarkan (*anonymized*).
2. **Kriteria Penilaian.** Parameter didasarkan pada standar indikator kemiskinan instansi dan regulasi Kementerian Sosial.
3. **Ruang Lingkup Keputusan.** Sistem berfokus pada perankingan dan penentuan status kelayakan berdasarkan ambang batas nilai preferensi menggunakan algoritma SAW.

### 1.4.2 Gambaran Sistem Informasi dan Sub-Sistem

1. **Platform dan Teknologi.** Aplikasi berbasis web dikembangkan menggunakan Python (*framework* Flask) dan basis data SQLite agar mudah diakses melalui peramban (*browser*).
2. **Sub-sistem Keputusan.** Mesin komputasi (*engine*) menggunakan algoritma SAW yang mencakup normalisasi matriks dan penjumlahan terbobot.
3. **Fungsionalitas.** Sistem bersifat *standalone* (tidak tersinkronisasi otomatis dengan pangkalan data kementerian) dengan fitur manajemen data, pembobotan, perhitungan SAW, dan pelaporan.

## 1.5 Metode Penelitian

Metode penelitian yang digunakan dalam Kerja Praktik ini meliputi dua pendekatan utama, yaitu pengumpulan data dan pengembangan sistem.

### 1.5.1 Metode Pengumpulan Data

1. **Metode Observasi.** Melakukan pengamatan langsung di Kantor Kecamatan Pondok Aren untuk memahami alur birokrasi, prosedur verifikasi, dan kendala teknis pendataan manual.
2. **Metode Wawancara.** Melaksanakan diskusi mendalam dengan staf Seksi Kemasyarakatan guna memperoleh informasi mengenai parameter kelayakan, bobot kriteria, dan kebutuhan fungsional sistem. Melalui wawancara ini, disepakati bahwa data penduduk disimulasikan secara valid demi menjaga kerahasiaan dokumen internal instansi.
3. **Studi Pustaka.** Mempelajari literatur ilmiah terkait Sistem Pendukung Keputusan, algoritma SAW, dan panduan penulisan laporan dari universitas.

### 1.5.2 Metode Pengembangan Sistem

Pengembangan sistem menggunakan metode *Waterfall* (*Linear Sequential Model*). Metode ini dipilih karena kebutuhan sistem telah terdefinisi secara jelas sejak awal melalui observasi dan wawancara, sehingga pengembangan dapat dilakukan secara linear dan terstruktur. Tahapannya meliputi:

1. **Analisis Kebutuhan.** Mengidentifikasi permasalahan sistem berjalan, menentukan tujuh kriteria penilaian, dan merumuskan kebutuhan fungsional aplikasi.
2. **Perancangan Sistem.** Menyusun arsitektur sistem menggunakan diagram UML, perancangan basis data (ERD), dan antarmuka pengguna (*mockup*).
3. **Implementasi.** Menerjemahkan rancangan ke dalam kode program menggunakan Python (*framework* Flask), basis data SQLite, dan logika perhitungan SAW.
4. **Pengujian.** Memvalidasi fungsionalitas sistem dan keluaran algoritma menggunakan data simulasi dengan ambang batas nilai preferensi kelayakan 0,50.
5. **Pemeliharaan.** Merumuskan saran pengembangan lanjutan, seperti integrasi aplikasi SIAK Terpusat dan pengembangan arsitektur *multi-user*.

## 1.6 Sistematika Penulisan

Laporan Kerja Praktik ini disusun dengan sistematika sebagai berikut:

1. **BAB I PENDAHULUAN.** Menguraikan Latar Belakang Masalah, Identifikasi Masalah, Tujuan Penulisan, Batasan Permasalahan, Metode Penelitian, dan Sistematika Penulisan.
2. **BAB II GAMBARAN UMUM INSTANSI.** Berisi profil Kantor Kecamatan Pondok Aren, struktur organisasi, wewenang, dan infrastruktur teknologi informasi.
3. **BAB III PEMBAHASAN.** Membahas Tinjauan Pustaka, analisis sistem berjalan, perancangan sistem usulan (UML), basis data, implementasi algoritma SAW, dan antarmuka sistem.
4. **BAB IV PENUTUP.** Berisi Kesimpulan atas hasil implementasi sistem dan Saran pengembangan di masa mendatang.

---

# BAB II GAMBARAN UMUM INSTANSI

## 2.1 Penjelasan Instansi Tempat Kerja Praktik

Kantor Kecamatan Pondok Aren merupakan unsur perangkat daerah yang menjalankan fungsi pelayanan publik dan pemerintahan umum di tingkat kewilayahan Kota Tangerang Selatan. Instansi ini berkedudukan di Jalan Graha Bintaro Nomor 1, Kelurahan Perigi Baru, Kecamatan Pondok Aren, Kota Tangerang Selatan.

Sebagai salah satu kecamatan dengan kepadatan penduduk tertinggi di Tangerang Selatan, instansi ini melayani wilayah seluas 29,88 km² yang mencakup 11 kelurahan: Perigi Baru, Perigi Lama, Pondok Kacang Barat, Pondok Kacang Timur, Pondok Pucung, Pondok Jaya, Pondok Aren, Jurang Mangu Barat, Jurang Mangu Timur, Pondok Karya, dan Pondok Betung. Secara strategis, instansi ini menjadi simpul penghubung antara kebijakan Pemerintah Kota dengan kebutuhan masyarakat di wilayah yang berbatasan langsung dengan Jakarta Selatan dan Kota Tangerang.

## 2.2 Sejarah, Struktur Organisasi, Tugas, dan Wewenang

### 2.2.1 Sejarah Singkat dan Transformasi Wilayah

Nama "Pondok Aren" memiliki nilai historis yang kuat, diambil dari kondisi alam masa lampau di mana wilayah ini merupakan kampung besar yang banyak ditumbuhi pohon aren (*Arenga pinnata*). Lintasan sejarah instansi ini dapat dirangkum dalam beberapa tonggak waktu penting sebagai berikut:

1. **Tahun 1981–1982:** Pembentukan Kecamatan Pondok Aren sebagai hasil pemekaran dari Kecamatan Ciledug saat masih di bawah administrasi Kabupaten Tangerang, Provinsi Jawa Barat.
2. **Tahun 1983:** Peresmian gedung pelayanan pertama oleh Bupati Tangerang (H. Tajus Sobirin) di atas lahan eks perkebunan karet PTP XI di wilayah Desa Pondok Aren.
3. **Tahun 2005:** Perpindahan kantor ke lokasi saat ini di Kelurahan Perigi Baru karena lokasi kantor lama diklaim oleh pengembang Bintaro Jaya.
4. **Tahun 2008–Sekarang:** Integrasi penuh ke dalam wilayah otonom Kota Tangerang Selatan setelah pembentukannya disahkan melalui UU No. 51 Tahun 2008.

### 2.2.2 Struktur Organisasi

Struktur organisasi Kecamatan Pondok Aren disusun untuk mendukung pelayanan prima kepada masyarakat. Pimpinan tertinggi adalah seorang Camat (saat ini dijabat oleh H. Hendra Gunawan, S.H., M.Si.) yang bertanggung jawab kepada Wali Kota. Secara visual, susunan hierarki dan pembagian tugas dalam organisasi tersebut dapat diamati pada Gambar 1 berikut.

*Gambar 1 – Struktur Organisasi Kecamatan Pondok Aren*

Berdasarkan struktur organisasi di atas, rincian tugas pokok dan wewenang fungsional pada setiap bagian dijabarkan secara lengkap pada Tabel 1 berikut.

**Tabel 1 – Tugas Pokok dan Wewenang Fungsional Kecamatan Pondok Aren**

| Jabatan / Bagian | Tugas Pokok dan Wewenang |
|---|---|
| Camat | Mengoordinasikan penyelenggaraan pemerintahan umum, membina kelurahan, serta menjaga ketenteraman dan ketertiban wilayah. |
| Sekretaris Camat | Mengelola administrasi internal yang mencakup tata usaha, kepegawaian, keuangan, dan penyusunan laporan akuntabilitas kinerja. |
| Seksi Tata Pemerintahan | Mengelola administrasi kependudukan, pertanahan, monografi kecamatan, serta pembinaan administrasi kelurahan. |
| Seksi Pelayanan Umum | Menyelenggarakan Pelayanan Administrasi Terpadu Kecamatan (PATEN) serta memproses perizinan dan non-perizinan. |
| Seksi Ketenteraman dan Ketertiban | Melakukan pengawasan penegakan Perda, koordinasi dengan aparat keamanan, dan menjaga ketertiban umum. |
| Seksi Ekonomi dan Pembangunan | Memfasilitasi pembangunan sarana prasarana fisik, pemeliharaan fasilitas umum, dan pemantauan ekonomi lokal. |
| Seksi Kemasyarakatan | Membina lembaga kemasyarakatan (LPM, PKK, Karang Taruna), memfasilitasi pemberdayaan sosial, serta mengelola program bantuan sosial di wilayah kecamatan. |

## 2.3 Penjelasan Unit Tempat Riset (Seksi Kemasyarakatan)

Riset Kerja Praktik ini difokuskan pada Seksi Kemasyarakatan, yang memiliki tugas pokok membina lembaga kemasyarakatan dan memfasilitasi pemberdayaan sosial di wilayah Kecamatan Pondok Aren. Unit ini bertanggung jawab langsung terhadap proses pendataan, verifikasi, dan penentuan prioritas calon penerima berbagai program bantuan sosial, seperti Bantuan Langsung Tunai (BLT), Program Keluarga Harapan (PKH), dan Bantuan Pangan Non-Tunai (BPNT).

Kompleksitas penentuan prioritas penerima bantuan yang saat ini masih dilakukan secara manual mendorong perlunya dukungan Sistem Pendukung Keputusan (SPK) di unit ini. Fokus riset pada Seksi Kemasyarakatan diambil karena relevansinya yang tinggi dengan tujuan membangun sistem berbasis algoritma *Simple Additive Weighting* (SAW), guna menghasilkan keputusan seleksi yang lebih objektif, transparan, dan terukur.

## 2.4 Infrastruktur Teknologi Informasi

Infrastruktur teknologi informasi (TI) di Kantor Kecamatan Pondok Aren dirancang secara menyeluruh untuk mendukung implementasi Sistem Pemerintahan Berbasis Elektronik (SPBE).

### 2.4.1 Jaringan dan Konektivitas

Konektivitas di area kantor memanfaatkan jaringan *fiber optic* (FO) dengan topologi *Local Area Network* (LAN). Instansi ini telah mengimplementasikan protokol IPv6 dan *Virtual Private Network* (VPN) yang dikelola oleh Diskominfo Kota Tangerang Selatan. Konfigurasi jaringan ini sangat esensial karena VPN menjamin keamanan transmisi data internal, sementara IPv6 memastikan stabilitas skalabilitas aksesibilitas ketika sistem pendukung keputusan (SPK) berbasis web yang dibangun diakses secara bersamaan oleh staf pelayanan.

### 2.4.2 Perangkat Keras

Perangkat keras (*hardware*) yang digunakan untuk operasional pelayanan di Kantor Kecamatan Pondok Aren meliputi empat kategori utama berikut:

1. **Komputer Operasional (*Client*).** Menjalankan sistem operasi Windows 10 dengan spesifikasi prosesor kelas menengah, memori RAM 4–8 GB, dan media penyimpanan *Hard Disk Drive* (HDD) berkapasitas 500 GB hingga 1 TB. Spesifikasi ini sangat memadai untuk mengeksekusi aplikasi SPK berbasis web yang dikembangkan.
2. ***Server* Lokal dan Jaringan.** Menggunakan Router Mikrotik seri RB yang bertindak sebagai *firewall* utama untuk sistem keamanan data dan manajemen *bandwidth*, serta *switch* Gigabit untuk kelancaran distribusi data antarruangan.
3. **Perangkat Biometrik.** Terdiri atas pemindai sidik jari, kamera digital (*webcam* e-KTP), dan *iris scanner* yang terintegrasi langsung dengan aplikasi SIAK pusat.
4. **Perangkat Cetak.** Menggunakan *printer laser jet* standar untuk pencetakan dokumen di kertas HVS, dan *printer thermal* khusus untuk mencetak blangko KTP-el.

### 2.4.3 Perangkat Lunak

Sistem informasi (*software*) yang digunakan dalam operasional Kantor Kecamatan Pondok Aren terdiri atas tiga aplikasi utama berikut:

1. **SIAK Terpusat.** Aplikasi utama dari Kemendagri untuk pengelolaan *database* kependudukan secara *real-time*.
2. **SIMPONIE.** Inovasi aplikasi untuk manajemen perizinan *online* di tingkat kecamatan.
3. **Sobat Dukcapil.** Platform pelayanan daring untuk permohonan akta dan kartu identitas secara mandiri.

## 2.5 Proses Bisnis Instansi

Proses bisnis di Kantor Kecamatan Pondok Aren berfokus pada peningkatan efisiensi layanan melalui digitalisasi alur kerja.

### 2.5.1 Alur Pelayanan Administrasi (PATEN)

Prosedur standar pelayanan umum mengikuti tahapan yang telah terstruktur, meliputi: penerimaan berkas, verifikasi kelengkapan melalui sistem SIAK, pemrosesan (*entry* data atau perekaman biometrik), pencetakan dokumen, dan penyerahan langsung kepada pemohon.

### 2.5.2 Program Inovatif "Jemput Bola"

Selain melayani di kantor, instansi juga menjalankan program SAPA WARGA yang melibatkan tim teknis untuk mendatangi lingkungan warga secara langsung. Program ini dirancang khusus untuk melakukan perekaman data kependudukan bagi kelompok rentan yang sulit mengakses layanan kantor, seperti lansia dan penyandang disabilitas.

### 2.5.3 Alur Verifikasi dan Seleksi Calon Penerima Bantuan Sosial

Proses bisnis yang terkait langsung dengan penelitian ini adalah mekanisme seleksi penerima bantuan sosial di Seksi Kemasyarakatan. Untuk memberikan gambaran yang komprehensif, tahapan prosedur konvensional tersebut divisualisasikan dalam bagan alir (*flowchart*) pada Gambar 2 berikut.

*Gambar 2 – Flowchart Alur Verifikasi dan Seleksi Calon Penerima Bantuan Sosial*

Berdasarkan bagan alir di atas, rincian penjelasan dari setiap prosedur administratif yang diterapkan adalah sebagai berikut:

1. **Pengajuan Data.** Pihak kelurahan mengirimkan data usulan dalam bentuk dokumen cetak atau *spreadsheet*. Karena tidak ada format baku, staf kecamatan harus menyesuaikan struktur data secara manual sebelum diproses.
2. **Rekapitulasi Manual.** Penggabungan data dari 11 kelurahan dilakukan menggunakan aplikasi perkantoran standar. Proses ini memakan waktu lama dan rentan terhadap kesalahan (*human error*) seperti duplikasi atau ketidakkonsistenan penulisan nama.
3. **Verifikasi Lapangan.** Petugas melakukan kunjungan fisik ke rumah warga untuk memeriksa kondisi tempat tinggal, penghasilan, dan tanggungan. Penilaian ini bersifat subjektif karena murni bergantung pada interpretasi visual petugas tanpa instrumen pengukur yang terstandarisasi.
4. **Penetapan Prioritas.** Daftar penerima bantuan ditetapkan melalui musyawarah konsensus internal. Keputusan diambil secara kualitatif, bukan kuantitatif, sehingga sering menyulitkan instansi saat diminta pertanggungjawaban oleh masyarakat mengenai dasar urutan prioritas.
5. **Penyaluran.** Daftar penerima tahap akhir dikirimkan kembali ke kelurahan untuk didistribusikan kepada warga yang berhak.

Kelemahan utama dari alur kerja ini adalah ketiadaan mekanisme perhitungan pembobotan yang objektif. Oleh karena itu, penerapan Sistem Pendukung Keputusan menggunakan algoritma SAW dalam Kerja Praktik ini dirancang untuk menggantikan musyawarah subjektif tersebut dengan kalkulasi sistem yang akurat dan dapat dipertanggungjawabkan.

## 2.6 Tinjauan Pustaka

### 2.6.1 Sistem Pendukung Keputusan (SPK)

**a. Definisi Menurut Para Ahli**

Sistem Pendukung Keputusan (SPK) didefinisikan sebagai kerangka kerja terkomputerisasi yang dirancang untuk membantu individu atau organisasi dalam memecahkan masalah semi-terstruktur dengan memanfaatkan pengolahan data dan model matematis. Sejalan dengan hal tersebut, SPK dirancang untuk membantu otoritas dalam mempertimbangkan banyak kriteria yang kompleks secara objektif (Altha Inas Shofyana et al., 2025). Sistem ini berfungsi sebagai sistem informasi interaktif yang menyediakan pemodelan dan manipulasi data untuk mendukung pengambilan keputusan yang lebih berkualitas (Limbong et al., 2023).

**b. Karakteristik dan Komponen SPK**

Karakteristik utama SPK adalah kemampuannya dalam melakukan komputasi data dalam jumlah besar secara cepat dengan biaya operasional yang relatif rendah (Limbong et al., 2023). Komponen SPK umumnya terdiri atas modul manajemen kriteria untuk penyesuaian bobot, modul masukan alternatif data warga, serta mesin perhitungan algoritma yang menghasilkan keluaran objektif berupa nilai preferensi (Altha Inas Shofyana et al., 2025).

**c. Tujuan SPK dalam Pengambilan Keputusan**

Tujuan utama SPK bukan untuk menggantikan peran otoritas pengambil keputusan, melainkan untuk meningkatkan efektivitas keputusan yang diambil (Limbong et al., 2023). Dalam konteks tata kelola di Kecamatan Pondok Aren, SPK bertujuan mengubah data mentah kondisi sosial-ekonomi masyarakat menjadi landasan komputasi ilmiah yang akuntabel, sehingga membantu pihak kecamatan menentukan prioritas penerima bantuan secara tepat sasaran.

**d. Proses Pengambilan Keputusan**

Proses pengambilan keputusan dalam SPK melibatkan identifikasi masalah, penentuan kriteria penilaian, pencarian alternatif solusi, hingga evaluasi menggunakan model matematis (Altha Inas Shofyana et al., 2025). Proses ini memungkinkan konversi data kualitatif yang bersifat subjektif dari hasil observasi lapangan menjadi nilai kuantitatif yang terukur dan objektif (Limbong et al., 2023).

### 2.6.2 Metode *Simple Additive Weighting* (SAW)

**a. Konsep Dasar SAW**

Metode SAW, yang lazim dikenal sebagai metode penjumlahan terbobot, merupakan salah satu metode pengambilan keputusan multikriteria (*Multi-Criteria Decision Making*/MCDM) yang banyak digunakan karena kesederhanaan dan ketepatannya (Altha Inas Shofyana et al., 2025). Konsep dasar metode ini adalah mencari penjumlahan terbobot dari *rating* kinerja pada setiap alternatif di seluruh atribut. Keunggulannya terletak pada efisiensi waktu pemrosesan komputasi serta kemampuannya dalam menghasilkan urutan prioritas yang transparan (Adhika Pramita Widyassari et al., 2023).

**b. Langkah-Langkah Perhitungan**

Berdasarkan literatur (Altha Inas Shofyana et al., 2025; Naibaho, 2026), kalkulasi SAW dilakukan melalui dua tahap utama, yaitu normalisasi matriks dan penjumlahan terbobot.

**Tahap 1: Normalisasi Matriks**

Normalisasi bertujuan untuk menyamakan skala penilaian setiap kriteria karena masing-masing kriteria memiliki satuan dan rentang nilai yang berbeda. Rumus normalisasi dibedakan berdasarkan tipe kriteria sebagai berikut:

- **Kriteria *Benefit* (Keuntungan):** Digunakan apabila nilai yang lebih besar menunjukkan kondisi yang lebih baik.

$$r_{ij} = \frac{x_{ij}}{\max(x_{ij})}$$

- **Kriteria *Cost* (Biaya):** Digunakan apabila nilai yang lebih kecil menunjukkan kondisi yang lebih baik.

$$r_{ij} = \frac{\min(x_{ij})}{x_{ij}}$$

**Tahap 2: Penjumlahan Terbobot**

Setelah normalisasi selesai dilakukan, nilai preferensi akhir ($V_i$) untuk setiap alternatif dihitung dengan menjumlahkan hasil perkalian antara bobot kriteria ($w_j$) dan nilai ternormalisasi ($r_{ij}$), sebagaimana dirumuskan berikut:

$$V_i = \sum_{j=1}^{n} w_j \cdot r_{ij}$$

### 2.6.3 Aplikasi Berbasis Web

**a. Pengertian Aplikasi Web dan Arsitektur *Client-Server***

Aplikasi berbasis web beroperasi menggunakan model arsitektur *client-server*, di mana *browser* klien mengirimkan permintaan (*request*) melalui jaringan dan *server* memberikan respons berupa data yang kemudian ditampilkan kepada pengguna.

**b. Pengembangan Sisi Depan (*Frontend*)**

Antarmuka pengguna (*frontend*) sistem dikembangkan menggunakan HTML sebagai kerangka struktur halaman, Tailwind CSS (*CLI/Local Build*) untuk penataan tampilan, dan JavaScript untuk interaktivitas antarmuka.

**c. Pengembangan Sisi Belakang (*Backend*)**

Sisi belakang (*backend*) sistem menangani seluruh logika bisnis menggunakan Python dengan *framework* Flask, *templating engine* Jinja2 untuk penghasil halaman dinamis, dan *Object-Relational Mapping* (ORM) SQLAlchemy untuk pengelolaan basis data.

**d. Basis Data SQLite**

SQLite dipilih sebagai sistem manajemen basis data karena sifatnya yang *serverless* dan tidak memerlukan proses instalasi terpisah. Karakteristik ini sangat ideal untuk diimplementasikan di infrastruktur instansi kecamatan yang memerlukan sistem operasional secara *standalone* yang praktis dan mudah dipelihara.

### 2.6.4 Penelitian Terdahulu

Untuk memperkuat landasan ilmiah penelitian ini, dilakukan kajian terhadap sejumlah penelitian terdahulu yang relevan. Hasil pemetaan penelitian tersebut — mencakup karya Widyassari (2023), Limbong (2023), Sudi (2024), Suprapto (2024), Shofyana (2025), Larantukan (2025), Muarif (2025), Purnomo (2025), dan Naibaho (2026) — dirangkum dalam Tabel 2 berikut.

*(Tabel 2 – Penelitian Terdahulu)*

**Analisis Perbandingan Penelitian Terdahulu**

Berdasarkan kajian terhadap penelitian-penelitian di atas, kebaruan (*novelty*) dari penelitian Kerja Praktik ini terletak pada tiga aspek utama:

1. **Pendekatan Arsitektur Teknologi.** Menggunakan *microframework* Flask (Python) dan basis data *serverless* SQLite, yang membedakannya dari mayoritas penelitian terdahulu yang umumnya menggunakan PHP atau *framework* berbasis Java.
2. **Kustomisasi Kriteria Berbasis Empiris.** Tujuh kriteria sosial-ekonomi yang digunakan dikalibrasi secara spesifik berdasarkan hasil wawancara dan kondisi demografis nyata Kecamatan Pondok Aren, bukan hanya mengadopsi kriteria generik.
3. **Otomatisasi Pemrosesan Kelompok (*Batch Processing*).** Sistem dilengkapi fitur klasifikasi data massal menggunakan pustaka Pandas, yang memungkinkan petugas memproses ratusan data warga sekaligus melalui satu berkas *spreadsheet*.

---

# BAB III PEMBAHASAN

## 3.1 Prosedur Kerja Praktik

### 3.1.1 Perancangan Sistem

**a. Analisis Sistem Berjalan**

Prosedur saat ini berjalan melalui pengajuan data dari 11 kelurahan, rekapitulasi manual, verifikasi lapangan, dan musyawarah penetapan prioritas. Kelemahan fatalnya adalah tingginya tingkat subjektivitas dalam setiap tahapan penilaian dan ketiadaan hasil akhir berupa perankingan matematis yang dapat dipertanggungjawabkan secara kuantitatif.

**b. Analisis Sistem Usulan**

Sistem usulan dirancang untuk mentransformasi proses konvensional menjadi digital melalui digitalisasi data terpusat dan penetapan pembobotan kriteria yang baku. Sebagai dasar perhitungan, tujuh kriteria penilaian beserta tipe dan bobot masing-masing, yang disepakati melalui wawancara dengan instansi, dirangkum dalam Tabel 3 berikut.

**Tabel 3 – Bobot Kriteria Sistem Usulan**

| Kode | Nama Kriteria | Tipe | Bobot |
|:---:|---|:---:|:---:|
| C1 | Penghasilan | *Cost* | 0,25 |
| C2 | Jumlah Tanggungan | *Benefit* | 0,20 |
| C3 | Kepemilikan Aset | *Cost* | 0,15 |
| C4 | Status Rumah | *Cost* | 0,10 |
| C5 | Kondisi Bangunan | *Cost* | 0,10 |
| C6 | Daya Listrik | *Cost* | 0,10 |
| C7 | Sumber Air | *Cost* | 0,10 |
| **Total** | | | **1,00** |

**c. Keunggulan Sistem Usulan**

Dibandingkan dengan proses manual yang berjalan, sistem usulan menawarkan sejumlah keunggulan signifikan, yaitu: objektivitas penilaian berbasis perhitungan matematis, kecepatan pemrosesan data, transparansi hasil perankingan, akuntabilitas yang dapat diaudit, aksesibilitas melalui *browser*, serta potensi integrasi dengan sistem data kependudukan.

**d. *Activity Diagram* Sistem Berjalan**

Untuk memberikan gambaran yang lebih jelas mengenai alur kerja sistem manual yang sedang berjalan, berikut disajikan *activity diagram* pada Gambar 3.

*Gambar 3 – Activity Diagram Sistem Berjalan*

**e. *Activity Diagram* Sistem Usulan**

Sebagai perbandingan, *activity diagram* sistem usulan menggambarkan alur kerja yang lebih terstruktur dan efisien, mencakup proses Login, Klasifikasi Manual, *Import* Massal, Filter & Ekspor, Edit Histori, dan Manajemen Kriteria.

*Gambar 4 – Activity Diagram Sistem Usulan*

**f. Normalisasi**

Pada implementasi sistem ini, baik kriteria bertipe *benefit* maupun *cost* menggunakan bentuk normalisasi yang sama, sebagaimana ditunjukkan pada persamaan berikut:

$$r_{ij} = \frac{x_{ij}}{\max(x_{ij})}$$

Penyeragaman rumus ini dimungkinkan karena skor untuk kriteria *cost* telah dibalik sejak tahap pendefinisian sub-kriteria, sehingga kondisi yang semakin membutuhkan bantuan akan memperoleh skor yang semakin tinggi dengan nilai maksimal 5.

**g. *Entity Relationship Diagram* (ERD)**

Hubungan antar entitas dalam basis data sistem diilustrasikan melalui *Entity Relationship Diagram* (ERD) pada Gambar 11 berikut. Diagram ini menggambarkan bagaimana data pengguna, kriteria, dan hasil klasifikasi saling berelasi.

*Gambar 11 – Entity Relationship Diagram (ERD)*

Relasi antar entitas yang terbentuk adalah sebagai berikut: tabel `users` berelasi satu-ke-banyak (1:N) dengan `login_history`, serta tabel `kriteria` berelasi satu-ke-banyak (1:N) dengan `sub_kriteria`. Adapun tabel `classification_results` menyimpan rekam jejak detail skor kriteria dalam format JSON.

**h. *Sequence Diagram***

Interaksi antara pengguna, antarmuka, dan sistem *backend* untuk setiap skenario utama digambarkan melalui *sequence diagram* yang mencakup skenario Login Admin, Klasifikasi Manual, *Import Batch*, Filter & Ekspor, serta Edit Histori.

### 3.1.2 Perancangan Perangkat Lunak: *Flowchart*

Alur kerja perangkat lunak secara keseluruhan — mulai dari penerimaan input data hingga penyimpanan hasil ke basis data — digambarkan dalam *flowchart* pada Gambar 17 berikut.

*Gambar 17 – Flowchart Proses Klasifikasi Data Warga*

Berdasarkan *flowchart* tersebut, perangkat lunak dirancang untuk mendukung dua mode input (manual dan massal), mencakup proses validasi data, perhitungan SAW, penentuan status kelayakan, penyimpanan ke basis data, serta penayangan hasil pada halaman histori.

## 3.2 Analisis dan Pembahasan

### 3.2.1 Pembahasan Algoritma

Implementasi algoritma SAW dikemas di dalam modul `spk.py` sebagai komponen inti sistem. Nilai kriteria yang bermakna "biaya terkecil" — contohnya penghasilan terendah pada kriteria C1 — langsung dikonversi menjadi skor prioritas terbesar (5) sejak tahap pendefinisian sub-kriteria. Dengan pendekatan ini, keseluruhan proses normalisasi cukup menggunakan satu rumus tunggal yang berlaku untuk semua kriteria, sehingga logika komputasi menjadi lebih efisien dan mudah diaudit.

### 3.2.2 Rancangan Layar

Antarmuka sistem dirancang dengan mengutamakan kemudahan penggunaan oleh petugas kecamatan. Berikut adalah deskripsi singkat setiap halaman yang diimplementasikan dalam sistem:

1. **Halaman Login** *(Gambar 18)* — Halaman autentikasi untuk memverifikasi identitas Admin sebelum mengakses sistem.
2. **Halaman *Dashboard*** *(Gambar 19)* — Halaman utama yang menampilkan ringkasan statistik data warga dan aktivitas terkini.
3. **Halaman Klasifikasi Data** *(Gambar 20)* — Halaman untuk memasukkan data warga secara manual maupun melalui *import* berkas massal.
4. **Halaman Histori** *(Gambar 21)* — Halaman yang menampilkan seluruh rekam hasil klasifikasi yang pernah dilakukan beserta detailnya.
5. **Halaman Manajemen Kriteria** *(Gambar 22)* — Halaman untuk mengelola kriteria dan bobot penilaian secara dinamis.
6. **Halaman Informasi SPK** *(Gambar 23)* — Halaman yang memuat penjelasan tentang metode SAW dan cara kerja sistem.
7. **Halaman Profil dan Riwayat Login** *(Gambar 24 & 25)* — Halaman pengelolaan data akun dan rekam jejak akses sistem oleh pengguna.

### 3.2.3 Implementasi dan Integrasi Alur Data

Sistem mengintegrasikan *routing* Flask dengan antarmuka berbasis Jinja2 untuk menghasilkan respons halaman yang dinamis. Pemrosesan dokumen *spreadsheet* yang diunggah pengguna dieksekusi secara instan di memori (*in-memory processing*) melalui pustaka Pandas, tanpa perlu menyimpan berkas sementara ke *server*, sehingga proses lebih cepat dan aman.

### 3.2.4 Pengujian Sistem

Pengujian sistem dilakukan dalam dua tahap untuk memastikan kebenaran algoritma sekaligus keandalan fungsionalitas aplikasi secara menyeluruh.

**a. Pengujian Algoritma SAW (Uji Coba dengan Contoh Data)**

Untuk memvalidasi keakuratan algoritma, dilakukan uji coba terhadap lima data sampel warga. Hasil perhitungan SAW beserta status kelayakan masing-masing warga berdasarkan *threshold* 0,50 dapat dilihat pada Tabel 5 berikut.

**Tabel 5 – Hasil Uji Coba Program**

| No | Nama | Kelurahan | Skor SAW | Status |
|:---:|---|---|:---:|---|
| 1 | Dewi Aminah | Pondok Jaya | 0,92 | Layak |
| 2 | Hadi Lestari | Perigi Lama | 0,90 | Layak |
| 3 | Lestari Setiawan | Pondok Aren | 0,50 | Layak |
| 4 | Ayu Lestari | Perigi Baru | 0,27 | Tidak Layak |
| 5 | Tri Setiawan | Pondok Aren | 0,24 | Tidak Layak |

Perhitungan manual algoritma SAW terhadap data sampel di atas dilakukan sebagai berikut:

- **Vektor Bobot (W):** $W = [0{,}25;\ 0{,}20;\ 0{,}15;\ 0{,}10;\ 0{,}10;\ 0{,}10;\ 0{,}10]$
- **Matriks Keputusan (X) dan Normalisasi (R):** Karena inversi logika data pada kriteria *cost*, normalisasi dilakukan secara linear terhadap nilai maksimum (5) untuk semua kriteria.
- **Penjumlahan Terbobot ($V_i$):** Nilai preferensi akhir masing-masing alternatif adalah:

$$V_1\ \text{(Dewi Aminah)} = 0{,}92$$

$$V_2\ \text{(Hadi Lestari)} = 0{,}90$$

$$V_3\ \text{(Lestari Setiawan)} = 0{,}50$$

$$V_4\ \text{(Ayu Lestari)} = 0{,}27$$

$$V_5\ \text{(Tri Setiawan)} = 0{,}24$$

Berdasarkan hasil di atas, dengan penetapan *threshold* sebesar 0,50, sistem berhasil menentukan status kelayakan seluruh data sampel dengan akurasi logika matematis 100%, sesuai dengan ekspektasi yang diharapkan.

**b. Pengujian Fungsional (*Black Box Testing*)**

Pengujian fungsional dilakukan menggunakan teknik *Equivalence Partitioning* pada empat modul utama, yaitu Autentikasi, Klasifikasi (Manual dan Massal), Manajemen Kriteria, serta Histori dan Ekspor. Seluruh skenario pengujian menghasilkan status **Valid** dan tidak ditemukan *bug* pada logika bisnis sistem, sehingga aplikasi dinyatakan lulus pengujian fungsional.

### 3.2.5 Penggunaan Program (*User Guide*)

Sistem ini dioperasikan oleh Admin Kecamatan melalui serangkaian langkah yang intuitif. Alur penggunaan dimulai dari proses Login untuk masuk ke sistem, dilanjutkan dengan pembukaan *Dashboard* untuk memantau ringkasan data. Selanjutnya, petugas dapat melakukan Klasifikasi Data warga secara Manual maupun melalui fitur *Import* massal. Hasil klasifikasi dapat ditinjau pada halaman Histori dan diekspor ke format Excel untuk keperluan pelaporan. Pengelolaan bobot dan kriteria penilaian dilakukan melalui halaman Manajemen Kriteria, sementara pengaturan akun dan keamanan dikelola melalui halaman Profil.

---

# BAB IV PENUTUP

## 4.1 Kesimpulan

Berdasarkan seluruh tahapan Kerja Praktik yang telah dilaksanakan di Kantor Kecamatan Pondok Aren, dapat disimpulkan bahwa Sistem Pendukung Keputusan (SPK) kelayakan penerima bantuan sosial berbasis web telah berhasil dirancang dan dibangun menggunakan Python (Flask, Jinja2, SQLAlchemy) dengan basis data SQLite. Implementasi algoritma *Simple Additive Weighting* (SAW) terbukti efektif dalam mengatasi permasalahan subjektivitas penilaian lapangan melalui penetapan tujuh kriteria sosial-ekonomi yang terstandarisasi. Sistem ini menghasilkan perankingan yang transparan dan akuntabel dengan mekanisme ambang batas skor kelayakan sebesar 0,50, sehingga setiap keputusan yang dihasilkan dapat dijelaskan secara matematis kepada seluruh pemangku kepentingan. Validasi melalui pengujian *Black Box Testing* mengonfirmasi bahwa seluruh fungsi aplikasi berjalan tanpa kegagalan maupun cacat kritikal, dan pengujian algoritma terhadap data sampel mencapai akurasi logika matematis 100%. Dengan demikian, sistem ini siap menjadi landasan transformasi digital proses seleksi bantuan sosial di Kecamatan Pondok Aren.

## 4.2 Saran

Guna memaksimalkan dampak sistem yang telah dibangun dan menjamin keberlanjutannya dalam jangka panjang, terdapat beberapa rekomendasi pengembangan yang perlu dipertimbangkan oleh pihak instansi maupun pengembang selanjutnya. Pertama, sistem sangat disarankan untuk diintegrasikan dengan aplikasi SIAK Terpusat agar validasi data kependudukan dapat dilakukan secara otomatis dan meminimalisasi potensi kesalahan input. Kedua, perlu dilakukan *stress testing* terhadap performa komputasi sistem menggunakan volume data berskala massal — yakni ribuan data warga — untuk memastikan stabilitasnya dalam kondisi operasional nyata. Ketiga, penerapan arsitektur *multi-user* dengan pemberian hak akses yang terdifferensiasi bagi staf di masing-masing kelurahan akan meningkatkan efisiensi dan keamanan pengelolaan data secara signifikan. Keempat, pengembangan modul dinamis yang memungkinkan penetapan standar kriteria berbeda untuk setiap variasi program bantuan — seperti BLT, PKH, dan BPNT — akan memperluas jangkauan kegunaan sistem. Kelima, migrasi basis data dari SQLite ke MySQL atau PostgreSQL sangat dianjurkan pada fase implementasi operasional penuh guna mencegah terjadinya *database lock* saat diakses secara bersamaan. Keenam dan terakhir, penyusunan *user manual* yang komprehensif perlu segera dilakukan untuk memastikan keberlanjutan operasional dan kemudahan pemeliharaan aplikasi oleh staf yang berwenang di masa mendatang.