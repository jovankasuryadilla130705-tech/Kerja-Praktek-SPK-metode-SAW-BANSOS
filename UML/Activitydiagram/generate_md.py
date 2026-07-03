# Generator Activity Diagram draw.io XML yang benar
# Semua elemen menggunakan koordinat ABSOLUT dengan parent="1"
# Swimlane hanya sebagai container visual/header

COL_W = 260   # lebar tiap kolom swimlane
ROW_H = 90    # jarak vertikal antar elemen
START_Y = 80  # y awal elemen pertama (di bawah header swimlane)
MARGIN_X = 40 # margin kiri dalam kolom
ACT_W = 180   # lebar activity box
ACT_H = 50    # tinggi activity box
DEC_W = 80    # lebar decision diamond
DEC_H = 80    # tinggi decision diamond
NODE_W = 30   # diameter start/end
HEADER_H = 30 # tinggi header swimlane

def rel_x(shape="activity"):
    """Koordinat x RELATIF terhadap swimlane kolom (tidak pakai offset kolom)"""
    if shape == "activity":
        return MARGIN_X
    elif shape == "decision":
        return (COL_W - DEC_W) // 2
    elif shape == "node":
        return (COL_W - NODE_W) // 2
    return 0

def center_x(col_idx, shape="activity"):
    """Titik tengah-x absolut untuk koneksi edge"""
    if shape == "activity":
        return abs_x(col_idx, "activity") + ACT_W // 2
    elif shape == "decision":
        return abs_x(col_idx, "decision") + DEC_W // 2
    elif shape == "node":
        return abs_x(col_idx, "node") + NODE_W // 2

def center_y(y, shape="activity"):
    if shape == "activity":
        return y + ACT_H // 2
    elif shape == "decision":
        return y + DEC_H // 2
    elif shape == "node":
        return y + NODE_W // 2

def build_xml(flow_num, col_names, elements_def, edges_def):
    """
    elements_def: list of (id, type, label, col_idx, y_pos)
      type: "start" | "end" | "activity" | "decision"
    edges_def: list of (src_id, dst_id, label)
    """
    num_cols = len(col_names)
    # tentukan tinggi diagram berdasarkan y terbesar + padding
    max_y = max(e[4] for e in elements_def)
    diagram_h = max_y + 200

    lines = []
    lines.append(f'<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1654" pageHeight="1169" math="0" shadow="0">')
    lines.append('  <root>')
    lines.append('    <mxCell id="0"/>')
    lines.append('    <mxCell id="1" parent="0"/>')

    # --- Swimlane kolom-kolom (masing-masing sebagai swimlane independen) ---
    total_w = num_cols * COL_W
    for i, col_name in enumerate(col_names):
        x = i * COL_W
        # Warna header per kolom
        if i == 0:
            fill = "#DAE8FC"
            stroke = "#6c8ebf"
        elif i == 1:
            fill = "#D5E8D4"
            stroke = "#82b366"
        else:
            fill = "#FFF2CC"
            stroke = "#d6b656"
        # Swimlane kolom langsung di bawah parent="1" agar edges bisa lintas kolom
        lines.append(f'    <mxCell id="A{flow_num}_col{i+1}" value="{col_name}" style="swimlane;html=1;startSize={HEADER_H};fillColor={fill};strokeColor={stroke};fontStyle=1;" vertex="1" parent="1">')
        lines.append(f'      <mxGeometry x="{x}" y="0" width="{COL_W}" height="{diagram_h}" as="geometry"/>')
        lines.append(f'    </mxCell>')

    # --- Elemen diagram ---
    elem_map = {}  # id -> (type, col_idx, y_pos)
    for e in elements_def:
        eid, etype, label, col_idx, y_pos = e
        elem_map[eid] = (etype, col_idx, y_pos)
        
        # Koordinat RELATIF terhadap swimlane kolom induk (tidak pakai offset kolom)
        if etype == "start":
            x = rel_x("node")
            style = "ellipse;aspect=fixed;fillColor=#000000;strokeColor=#000000;"
            lines.append(f'    <mxCell id="A{flow_num}_{eid}" value="" style="{style}" vertex="1" parent="A{flow_num}_col{col_idx+1}">')
            lines.append(f'      <mxGeometry x="{x}" y="{y_pos}" width="{NODE_W}" height="{NODE_W}" as="geometry"/>')
            lines.append(f'    </mxCell>')
        elif etype == "end":
            x = rel_x("node")
            style = "ellipse;aspect=fixed;fillColor=#000000;strokeColor=#000000;double=1;"
            lines.append(f'    <mxCell id="A{flow_num}_{eid}" value="" style="{style}" vertex="1" parent="A{flow_num}_col{col_idx+1}">')
            lines.append(f'      <mxGeometry x="{x}" y="{y_pos}" width="{NODE_W}" height="{NODE_W}" as="geometry"/>')
            lines.append(f'    </mxCell>')
        elif etype == "decision":
            x = rel_x("decision")
            style = "rhombus;whiteSpace=wrap;html=1;"
            lines.append(f'    <mxCell id="A{flow_num}_{eid}" value="{label}" style="{style}" vertex="1" parent="A{flow_num}_col{col_idx+1}">')
            lines.append(f'      <mxGeometry x="{x}" y="{y_pos}" width="{DEC_W}" height="{DEC_H}" as="geometry"/>')
            lines.append(f'    </mxCell>')
        else:  # activity
            x = rel_x("activity")
            style = "rounded=1;whiteSpace=wrap;html=1;arcSize=20;"
            lines.append(f'    <mxCell id="A{flow_num}_{eid}" value="{label}" style="{style}" vertex="1" parent="A{flow_num}_col{col_idx+1}">')
            lines.append(f'      <mxGeometry x="{x}" y="{y_pos}" width="{ACT_W}" height="{ACT_H}" as="geometry"/>')
            lines.append(f'    </mxCell>')

    # --- Edges ---
    for idx, e in enumerate(edges_def, 1):
        src_id, dst_id, label = e
        src_type, src_col, _ = elem_map[src_id]
        dst_type, dst_col, _ = elem_map[dst_id]

        edge_style_parts = ["edgeStyle=orthogonalEdgeStyle", "rounded=0", "orthogonalLoop=1", "jettySize=auto"]

        if src_col == dst_col:
            # Alur vertikal dalam kolom yang sama
            edge_style_parts += ["exitX=0.5", "exitY=1", "entryX=0.5", "entryY=0"]
        elif dst_col > src_col:
            # Ke kanan
            edge_style_parts += ["exitX=1", "exitY=0.5", "entryX=0", "entryY=0.5"]
        else:
            # Ke kiri
            edge_style_parts += ["exitX=0", "exitY=0.5", "entryX=1", "entryY=0.5"]

        edge_style = ";".join(edge_style_parts) + ";"
        val_attr = f' value="{label}"' if label else ' value=""'
        # Edge parent="1" agar draw.io bisa resolve source/target lintas swimlane
        lines.append(f'    <mxCell id="A{flow_num}_edge{idx}"{val_attr} style="{edge_style}" edge="1" source="A{flow_num}_{src_id}" target="A{flow_num}_{dst_id}" parent="1">')
        lines.append(f'      <mxGeometry relative="1" as="geometry"/>')
        lines.append(f'    </mxCell>')

    lines.append('  </root>')
    lines.append('</mxGraphModel>')
    return "\n".join(lines)


def alur_block(num, title, narasi, plantuml_code, col_names, elements_def, edges_def):
    xml = build_xml(num, col_names, elements_def, edges_def)
    return f"""---
### ALUR {num} — {title}

**Narasi:**
{narasi}

**Format A — PlantUML:**
```plantuml
{plantuml_code}
```

**Format B — XML draw.io:**
```xml
{xml}
```
"""

# ============================================================
# DATA SETIAP ALUR
# ============================================================

Y = START_Y  # helper awal, kita definisikan y tiap elemen manual

alur_blocks = []

# ─────────────────────────────────────────────────────────────
# ALUR 1 — Autentikasi (Login & Logout)
# ─────────────────────────────────────────────────────────────
a1_narasi = (
    "Proses autentikasi dimulai ketika Pengguna (Admin, Staff, atau Camat) mengakses halaman login "
    "dan memasukkan kredensial berupa username dan password. Sistem memvalidasi kelengkapan form; "
    "jika ada field kosong, sistem menampilkan pesan error dan mengembalikan pengguna ke form. "
    "Jika lengkap, sistem melakukan kueri ke tabel `users` untuk mencari username. Apabila username "
    "tidak ditemukan, sistem mencatat kegagalan pada tabel `login_history` dan menampilkan notifikasi "
    "error. Jika username ditemukan, sistem memverifikasi `password_hash`; jika salah, kegagalan "
    "kembali dicatat. Jika benar, sistem mencatat keberhasilan login, membuat sesi aktif berisi "
    "`user_id` dan `role`, lalu mengarahkan pengguna ke dashboard sesuai perannya. Untuk logout, "
    "pengguna mengeklik tombol Logout, sistem menghapus sesi aktif dan mengarahkan kembali ke "
    "halaman login."
)

a1_plantuml = """@startuml
|#DAE8FC|Pengguna|
start
:Membuka halaman Login;
:Mengisi username & password;
|#D5E8D4|Sistem|
:Validasi kelengkapan field;
if (Field kosong?) then (Ya)
  :Tampilkan error field wajib diisi;
  |Pengguna|
  :Kembali ke form;
  stop
else (Tidak)
  |Sistem|
  :Query tabel `users` WHERE username = input;
  if (Username ditemukan?) then (Tidak)
    |#FFF2CC|Database|
    :Catat log FAILED ke `login_history`;
    |Sistem|
    :Tampilkan "Akun tidak ditemukan";
    |Pengguna|
    :Kembali ke form;
    stop
  else (Ya)
    |Sistem|
    :Verifikasi password_hash;
    if (Password cocok?) then (Tidak)
      |Database|
      :Catat log FAILED ke `login_history`;
      |Sistem|
      :Tampilkan "Password salah";
      |Pengguna|
      :Kembali ke form;
      stop
    else (Ya)
      |Database|
      :Catat log SUCCESS ke `login_history`;
      |Sistem|
      :Buat session (user_id & role);
      :Redirect ke dashboard sesuai role;
      |Pengguna|
      :Klik tombol "Logout";
      |Sistem|
      :Hapus session aktif;
      :Redirect ke halaman Login;
      stop
    endif
  endif
endif
@enduml"""

# col: 0=Pengguna, 1=Sistem, 2=Database
a1_cols = ["Pengguna", "Sistem", "Database"]
a1_elems = [
    ("start",  "start",    "",                               0,  50),
    ("act1",   "activity", "Membuka halaman Login",          0, 110),
    ("act2",   "activity", "Isi username &amp; password",   0, 190),
    ("act3",   "activity", "Validasi kelengkapan field",     1, 190),
    ("dec1",   "decision", "Field\nKosong?",                 1, 270),
    ("err1",   "activity", "Error: field wajib diisi",       1, 380),
    ("back1",  "activity", "Kembali ke form",                0, 380),
    ("end1",   "end",      "",                               0, 460),
    ("act4",   "activity", "Query tabel users",              1, 480),
    ("dec2",   "decision", "Username\nDitemukan?",           1, 560),
    ("db1",    "activity", "Catat log FAILED",               2, 560),
    ("err2",   "activity", "Akun tidak ditemukan",           1, 670),
    ("back2",  "activity", "Kembali ke form",                0, 670),
    ("end2",   "end",      "",                               0, 750),
    ("act5",   "activity", "Verifikasi password_hash",       1, 770),
    ("dec3",   "decision", "Password\nCocok?",               1, 850),
    ("db2",    "activity", "Catat log FAILED",               2, 850),
    ("err3",   "activity", "Password salah",                 1, 960),
    ("back3",  "activity", "Kembali ke form",                0, 960),
    ("end3",   "end",      "",                               0,1040),
    ("db3",    "activity", "Catat log SUCCESS",              2,1060),
    ("act6",   "activity", "Buat session (user_id &amp; role)", 1, 1060),
    ("act7",   "activity", "Redirect ke dashboard",          1,1140),
    ("act8",   "activity", "Klik tombol Logout",             0,1140),
    ("act9",   "activity", "Hapus session aktif",            1,1220),
    ("act10",  "activity", "Redirect ke halaman Login",      1,1300),
    ("end4",   "end",      "",                               1,1380),
]
a1_edges = [
    ("start","act1",""), ("act1","act2",""), ("act2","act3",""),
    ("act3","dec1",""), ("dec1","err1","Ya"), ("err1","back1",""), ("back1","end1",""),
    ("dec1","act4","Tidak"), ("act4","dec2",""),
    ("dec2","db1","Tidak"), ("db1","err2",""), ("err2","back2",""), ("back2","end2",""),
    ("dec2","act5","Ya"), ("act5","dec3",""),
    ("dec3","db2","Tidak"), ("db2","err3",""), ("err3","back3",""), ("back3","end3",""),
    ("dec3","db3","Ya"), ("db3","act6",""), ("act6","act7",""), ("act7","act8",""),
    ("act8","act9",""), ("act9","act10",""), ("act10","end4",""),
]

alur_blocks.append(alur_block(1,"Autentikasi (Login & Logout)",a1_narasi,a1_plantuml,a1_cols,a1_elems,a1_edges))

# ─────────────────────────────────────────────────────────────
# ALUR 2 — Manajemen Profil & Keamanan
# ─────────────────────────────────────────────────────────────
a2_narasi = (
    "Alur ini memfasilitasi pengguna untuk memperbarui informasi profil, mencakup foto profil dan "
    "password. Pengguna mengakses menu Profil, dan sistem menampilkan data terkini dari tabel `users`. "
    "Jika pengguna memilih ubah foto, mereka mengunggah file; sistem memvalidasi format (.jpg/.png) "
    "dan ukuran (maks. 2 MB). Jika tidak valid, sistem menampilkan error; jika valid, file disimpan "
    "dan field `foto_profil` di-update. Jika pengguna memilih ganti password, mereka mengisi password "
    "lama, password baru, dan konfirmasi. Sistem memverifikasi password lama dengan hash di database; "
    "jika tidak cocok, error ditampilkan. Selanjutnya sistem memvalidasi kecocokan password baru dengan "
    "konfirmasinya. Bila semua valid, password baru di-hash lalu `password_hash` di-update pada tabel "
    "`users`, diakhiri dengan notifikasi keberhasilan."
)

a2_plantuml = """@startuml
|#DAE8FC|Pengguna|
start
:Membuka menu Profil;
|#D5E8D4|Sistem|
:Query & tampilkan data profil dari `users`;
|Pengguna|
:Memilih aksi;
fork
  :Ubah Foto Profil;
  :Pilih file & klik Upload;
  |Sistem|
  :Validasi format (.jpg/.png) & ukuran ≤2MB;
  if (Valid?) then (Tidak)
    :Tampilkan pesan error format/ukuran;
    stop
  else (Ya)
    :Simpan file ke server;
    |#FFF2CC|Database|
    :UPDATE foto_profil di tabel `users`;
    |Sistem|
    :Notifikasi "Foto berhasil diperbarui";
    stop
  endif
fork again
  |Pengguna|
  :Ganti Password;
  :Isi Pass Lama, Pass Baru, Konfirmasi;
  |Sistem|
  :Verifikasi Password Lama;
  if (Cocok?) then (Tidak)
    :Tampilkan "Password lama salah";
    stop
  else (Ya)
    |Sistem|
    :Validasi Pass Baru == Konfirmasi;
    if (Sama?) then (Tidak)
      :Tampilkan "Konfirmasi tidak cocok";
      stop
    else (Ya)
      |Sistem|
      :Hash password baru;
      |Database|
      :UPDATE password_hash di tabel `users`;
      |Sistem|
      :Notifikasi "Password berhasil diubah";
      stop
    endif
  endif
end fork
@enduml"""

a2_cols = ["Pengguna", "Sistem", "Database"]
a2_elems = [
    ("start",  "start",    "",                                       0,  50),
    ("act1",   "activity", "Membuka menu Profil",                   0, 110),
    ("act2",   "activity", "Query data profil",                     1, 110),
    ("act3",   "activity", "Memilih aksi",                          0, 190),
    # Cabang Foto
    ("act4",   "activity", "Pilih file foto &amp; Upload",           0, 300),
    ("act5",   "activity", "Validasi format &amp; ukuran",           1, 300),
    ("dec1",   "decision", "Valid?",                                 1, 380),
    ("err1",   "activity", "Error format/ukuran",                   1, 490),
    ("end1",   "end",      "",                                       1, 570),
    ("db1",    "activity", "UPDATE foto_profil",                    2, 490),
    ("notif1", "activity", "Notifikasi foto berhasil",              1, 580),
    ("end2",   "end",      "",                                       1, 660),
    # Cabang Password
    ("act6",   "activity", "Pilih Ganti Password",                  0, 300),
    ("act7",   "activity", "Isi Pass Lama, Pass Baru, Konfirmasi",  0, 390),
    ("act8",   "activity", "Verifikasi Password Lama",              1, 750),
    ("dec2",   "decision", "Cocok?",                                1, 830),
    ("err2",   "activity", "Error password lama salah",             1, 940),
    ("end3",   "end",      "",                                       1,1020),
    ("dec3",   "decision", "Sama?",                                 1,1040),
    ("err3",   "activity", "Error konfirmasi tidak cocok",          1,1150),
    ("end4",   "end",      "",                                       1,1230),
    ("act9",   "activity", "Hash password baru",                    1,1150),
    ("db2",    "activity", "UPDATE password_hash",                  2,1150),
    ("notif2", "activity", "Notifikasi password berhasil",          1,1250),
    ("end5",   "end",      "",                                       1,1330),
]
a2_edges = [
    ("start","act1",""), ("act1","act2",""), ("act2","act3",""),
    ("act3","act4","Ubah Foto"), ("act4","act5",""), ("act5","dec1",""),
    ("dec1","err1","Tidak"), ("err1","end1",""),
    ("dec1","db1","Ya"), ("db1","notif1",""), ("notif1","end2",""),
    ("act3","act6","Ganti Password"), ("act6","act7",""), ("act7","act8",""),
    ("act8","dec2",""), ("dec2","err2","Tidak"), ("err2","end3",""),
    ("dec2","dec3","Ya"), ("dec3","err3","Tidak"), ("err3","end4",""),
    ("dec3","act9","Ya"), ("act9","db2",""), ("db2","notif2",""), ("notif2","end5",""),
]

alur_blocks.append(alur_block(2,"Manajemen Profil & Keamanan",a2_narasi,a2_plantuml,a2_cols,a2_elems,a2_edges))

# ─────────────────────────────────────────────────────────────
# ALUR 3 — Akses Dashboard & Statistik
# ─────────────────────────────────────────────────────────────
a3_narasi = (
    "Seluruh aktor yang memiliki hak akses dapat membuka menu Dashboard untuk melihat ringkasan "
    "statistik. Saat halaman diakses, sistem menjalankan kueri ke tabel `classification_results` "
    "untuk merekap total warga terklasifikasi, jumlah berstatus LAYAK, dan jumlah TIDAK LAYAK. "
    "Sistem kemudian mengevaluasi apakah data tersedia. Jika belum ada data, sistem menampilkan "
    "pesan informatif dan merender dashboard kosong. Jika data tersedia, sistem menghitung persentase "
    "proporsi masing-masing status kelayakan, lalu merender Pie Chart untuk visualisasi proporsi "
    "dan Bar Chart untuk distribusi per periode. Keseluruhan ringkasan statistik dan grafik "
    "ditampilkan pada antarmuka dashboard. Pengguna dengan peran Camat hanya dapat melihat tanpa "
    "aksi tambahan, sementara Admin dan Staff dapat menggunakan data untuk keperluan operasional."
)

a3_plantuml = """@startuml
|#DAE8FC|Pengguna|
start
:Klik menu "Dashboard";
|#D5E8D4|Sistem|
:Query rekapitulasi dari `classification_results`;
|#FFF2CC|Database|
:Kembalikan data agregat;
|Sistem|
if (Data tersedia?) then (Tidak)
  :Tampilkan "Belum ada data klasifikasi";
  :Render dashboard kosong;
  stop
else (Ya)
  :Hitung persentase LAYAK & TIDAK LAYAK;
  :Render Pie Chart (proporsi kelayakan);
  :Render Bar Chart (distribusi);
  :Tampilkan ringkasan statistik & grafik;
  |Pengguna|
  :Melihat data dashboard;
  stop
endif
@enduml"""

a3_cols = ["Pengguna", "Sistem", "Database"]
a3_elems = [
    ("start",  "start",    "",                                 0,  50),
    ("act1",   "activity", "Klik menu Dashboard",              0, 110),
    ("act2",   "activity", "Query rekapitulasi data",          1, 110),
    ("db1",    "activity", "Kembalikan data agregat",          2, 110),
    ("dec1",   "decision", "Data\nTersedia?",                  1, 190),
    ("err1",   "activity", "Tampilkan pesan belum ada data",   1, 300),
    ("act3",   "activity", "Render dashboard kosong",          1, 380),
    ("end1",   "end",      "",                                 1, 460),
    ("act4",   "activity", "Hitung persentase",                1, 300),
    ("act5",   "activity", "Render Pie Chart",                 1, 380),
    ("act6",   "activity", "Render Bar Chart",                 1, 460),
    ("act7",   "activity", "Tampilkan statistik &amp; grafik", 1, 540),
    ("act8",   "activity", "Melihat data dashboard",           0, 540),
    ("end2",   "end",      "",                                 0, 620),
]
a3_edges = [
    ("start","act1",""), ("act1","act2",""), ("act2","db1",""), ("db1","dec1",""),
    ("dec1","err1","Tidak"), ("err1","act3",""), ("act3","end1",""),
    ("dec1","act4","Ya"), ("act4","act5",""), ("act5","act6",""),
    ("act6","act7",""), ("act7","act8",""), ("act8","end2",""),
]

alur_blocks.append(alur_block(3,"Akses Dashboard & Statistik",a3_narasi,a3_plantuml,a3_cols,a3_elems,a3_edges))

# ─────────────────────────────────────────────────────────────
# ALUR 4 — Klasifikasi Bansos (Metode SAW)
# ─────────────────────────────────────────────────────────────
a4_narasi = (
    "Alur utama ini dijalankan oleh Admin atau Staff untuk mengklasifikasikan kelayakan warga "
    "penerima bansos menggunakan metode SAW. Pengguna memilih mode input: manual (satu per satu) "
    "atau import file CSV. Pada mode manual, sistem memvalidasi kelengkapan dan tipe data setiap "
    "field; jika tidak valid, error ditampilkan per field. Pada mode CSV, sistem memvalidasi format "
    "file dan struktur kolom; jika tidak sesuai template, proses dikembalikan. Setelah data valid, "
    "sistem menjalankan algoritma SAW: mengambil bobot dari tabel `kriteria`, mengambil nilai "
    "konversi dari `sub_kriteria`, membangun matriks keputusan X, melakukan normalisasi (benefit: "
    "x/max, cost: min/x), lalu menghitung nilai preferensi V. Threshold 0.50 digunakan: V ≥ 0.50 "
    "berarti LAYAK, V < 0.50 berarti TIDAK LAYAK. Hasil disimpan ke `classification_results` dan "
    "ditampilkan dalam tabel."
)

a4_plantuml = """@startuml
|#DAE8FC|Admin/Staff|
start
:Membuka menu Klasifikasi Bansos;
:Memilih mode input;
fork
  :Mode MANUAL;
  :Isi form data warga → klik Proses;
  |#D5E8D4|Sistem|
  :Validasi field (kelengkapan & tipe data);
  if (Valid?) then (Tidak)
    :Tampilkan error per field;
    |Admin/Staff|
    :Kembali ke form;
    stop
  else (Ya)
  endif
fork again
  |Admin/Staff|
  :Mode IMPORT CSV;
  :Upload file .csv;
  |Sistem|
  :Validasi format & struktur kolom CSV;
  if (Valid?) then (Tidak)
    :Tampilkan "Format tidak sesuai template";
    |Admin/Staff|
    :Kembali ke form;
    stop
  else (Ya)
    |Sistem|
    :Parsing data CSV ke memori;
  endif
end fork
|#FFF2CC|Database|
:Query bobot dari tabel `kriteria`;
:Query nilai konversi dari `sub_kriteria`;
|Sistem|
:Bangun matriks keputusan X;
:Normalisasi matriks r_ij;
:Hitung V_i = Σ(w_j × r_ij);
if (V_i ≥ 0.50?) then (Ya)
  :Status: LAYAK;
else (Tidak)
  :Status: TIDAK LAYAK;
endif
|Database|
:INSERT hasil ke `classification_results`;
|Sistem|
:Tampilkan tabel hasil (NIK, Nama, V, Status);
stop
@enduml"""

a4_cols = ["Admin/Staff", "Sistem", "Database"]
a4_elems = [
    ("start",  "start",    "",                                       0,  50),
    ("act1",   "activity", "Buka menu Klasifikasi Bansos",          0, 110),
    ("act2",   "activity", "Memilih mode input",                    0, 190),
    # Cabang Manual
    ("act3",   "activity", "Mode MANUAL: Isi form warga",           0, 300),
    ("act4",   "activity", "Validasi field",                        1, 300),
    ("dec1",   "decision", "Valid?",                                 1, 380),
    ("err1",   "activity", "Error per field",                       1, 490),
    ("back1",  "activity", "Kembali ke form",                       0, 490),
    ("end1",   "end",      "",                                       0, 570),
    # Cabang CSV
    ("act5",   "activity", "Mode CSV: Upload file .csv",            0, 660),
    ("act6",   "activity", "Validasi format &amp; kolom CSV",        1, 660),
    ("dec2",   "decision", "Valid?",                                 1, 740),
    ("err2",   "activity", "Error format CSV",                      1, 850),
    ("back2",  "activity", "Kembali ke form",                       0, 850),
    ("end2",   "end",      "",                                       0, 930),
    ("act7",   "activity", "Parsing CSV ke memori",                 1, 850),
    # SAW
    ("db1",    "activity", "Query bobot dari `kriteria`",           2, 960),
    ("db2",    "activity", "Query nilai konversi",                  2,1050),
    ("act8",   "activity", "Bangun matriks keputusan X",            1, 960),
    ("act9",   "activity", "Normalisasi matriks r_ij",              1,1050),
    ("act10",  "activity", "Hitung V_i = Σ(w_j × r_ij)",           1,1140),
    ("dec3",   "decision", "V_i ≥ 0.50?",                          1,1230),
    ("act11",  "activity", "Status: LAYAK",                         1,1340),
    ("act12",  "activity", "Status: TIDAK LAYAK",                   1,1430),
    ("db3",    "activity", "INSERT ke classification_results",      2,1340),
    ("act13",  "activity", "Tampilkan tabel hasil klasifikasi",     1,1520),
    ("end3",   "end",      "",                                       1,1600),
]
a4_edges = [
    ("start","act1",""), ("act1","act2",""),
    ("act2","act3","Manual"), ("act3","act4",""), ("act4","dec1",""),
    ("dec1","err1","Tidak"), ("err1","back1",""), ("back1","end1",""),
    ("dec1","db1","Ya"),
    ("act2","act5","CSV"), ("act5","act6",""), ("act6","dec2",""),
    ("dec2","err2","Tidak"), ("err2","back2",""), ("back2","end2",""),
    ("dec2","act7","Ya"), ("act7","db1",""),
    ("db1","db2",""), ("db2","act8",""), ("act8","act9",""),
    ("act9","act10",""), ("act10","dec3",""),
    ("dec3","act11","Ya"), ("dec3","act12","Tidak"),
    ("act11","db3",""), ("act12","db3",""),
    ("db3","act13",""), ("act13","end3",""),
]

alur_blocks.append(alur_block(4,"Klasifikasi Bansos (Metode SAW) [ALUR UTAMA]",a4_narasi,a4_plantuml,a4_cols,a4_elems,a4_edges))

# ─────────────────────────────────────────────────────────────
# ALUR 5 — Manajemen Data Warga (Edit & Hapus)
# ─────────────────────────────────────────────────────────────
a5_narasi = (
    "Admin atau Staff menggunakan alur ini untuk mengelola riwayat data warga yang telah "
    "diklasifikasikan. Ketika menu Riwayat Data Warga dibuka, sistem menjalankan kueri JOIN antara "
    "tabel `classification_results` dan `warga` lalu menampilkan hasilnya. Pengguna dapat melakukan "
    "pencarian berdasarkan nama atau NIK untuk mempersempit tampilan. Untuk aksi Edit, pengguna "
    "mengeklik tombol Edit pada baris tertentu; sistem menampilkan form berisi data lama. Setelah "
    "pengguna memodifikasi data dan menyimpan, sistem memvalidasi input. Jika valid, sistem "
    "meng-update tabel `warga`, melakukan kalkulasi ulang nilai SAW, dan meng-update tabel "
    "`classification_results`. Untuk aksi Hapus, sistem menampilkan dialog konfirmasi. Jika "
    "dikonfirmasi, sistem menghapus record dari database. Setiap aksi yang berhasil diakhiri "
    "dengan notifikasi dan penyegaran daftar."
)

a5_plantuml = """@startuml
|#DAE8FC|Admin/Staff|
start
:Buka "Riwayat Data Warga";
|#FFF2CC|Database|
:Query JOIN classification_results & warga;
|#D5E8D4|Sistem|
:Tampilkan daftar data warga;
|Admin/Staff|
:Input pencarian (opsional);
|Sistem|
:Filter & tampilkan hasil;
|Admin/Staff|
:Pilih aksi pada baris data;
fork
  :Klik EDIT;
  |Sistem|
  :Tampilkan form dengan data lama;
  |Admin/Staff|
  :Ubah data → klik Simpan;
  |Sistem|
  :Validasi input;
  if (Valid?) then (Tidak)
    :Tampilkan pesan error;
    stop
  else (Ya)
    |Database|
    :UPDATE data di tabel `warga`;
    |Sistem|
    :Recalculate nilai SAW;
    |Database|
    :UPDATE tabel `classification_results`;
    |Sistem|
    :Notifikasi "Data berhasil diperbarui";
    stop
  endif
fork again
  |Admin/Staff|
  :Klik HAPUS;
  |Sistem|
  :Tampilkan dialog konfirmasi;
  if (Konfirmasi hapus?) then (Batal)
    :Kembali ke daftar;
    stop
  else (Konfirmasi)
    |Database|
    :DELETE dari `classification_results`;
    |Sistem|
    :Notifikasi "Data berhasil dihapus";
    stop
  endif
end fork
@enduml"""

a5_cols = ["Admin/Staff", "Sistem", "Database"]
a5_elems = [
    ("start",  "start",    "",                                   0,  50),
    ("act1",   "activity", "Buka Riwayat Data Warga",           0, 110),
    ("db1",    "activity", "Query JOIN data",                   2, 110),
    ("act2",   "activity", "Tampilkan daftar data",             1, 110),
    ("act3",   "activity", "Input pencarian (opsional)",        0, 190),
    ("act4",   "activity", "Filter &amp; tampilkan hasil",       1, 190),
    ("act5",   "activity", "Pilih aksi pada baris data",        0, 270),
    # Cabang Edit
    ("act6",   "activity", "Klik EDIT",                         0, 380),
    ("act7",   "activity", "Form data lama ditampilkan",        1, 380),
    ("act8",   "activity", "Ubah data → klik Simpan",           0, 460),
    ("act9",   "activity", "Validasi input",                    1, 460),
    ("dec1",   "decision", "Valid?",                             1, 540),
    ("err1",   "activity", "Tampilkan error",                   1, 650),
    ("end1",   "end",      "",                                   1, 730),
    ("db2",    "activity", "UPDATE tabel warga",                2, 650),
    ("act10",  "activity", "Recalculate nilai SAW",             1, 740),
    ("db3",    "activity", "UPDATE classification_results",     2, 740),
    ("notif1", "activity", "Notifikasi data diperbarui",        1, 830),
    ("end2",   "end",      "",                                   1, 910),
    # Cabang Hapus
    ("act11",  "activity", "Klik HAPUS",                        0, 380),
    ("act12",  "activity", "Tampilkan dialog konfirmasi",       1,1000),
    ("dec2",   "decision", "Konfirmasi?",                        1,1080),
    ("act13",  "activity", "Kembali ke daftar",                 1,1190),
    ("end3",   "end",      "",                                   1,1270),
    ("db4",    "activity", "DELETE dari database",              2,1190),
    ("notif2", "activity", "Notifikasi data dihapus",           1,1280),
    ("end4",   "end",      "",                                   1,1360),
]
a5_edges = [
    ("start","act1",""), ("act1","db1",""), ("db1","act2",""),
    ("act2","act3",""), ("act3","act4",""), ("act4","act5",""),
    ("act5","act6","Edit"), ("act6","act7",""), ("act7","act8",""),
    ("act8","act9",""), ("act9","dec1",""),
    ("dec1","err1","Tidak"), ("err1","end1",""),
    ("dec1","db2","Ya"), ("db2","act10",""), ("act10","db3",""), ("db3","notif1",""), ("notif1","end2",""),
    ("act5","act11","Hapus"), ("act11","act12",""), ("act12","dec2",""),
    ("dec2","act13","Batal"), ("act13","end3",""),
    ("dec2","db4","Konfirmasi"), ("db4","notif2",""), ("notif2","end4",""),
]

alur_blocks.append(alur_block(5,"Manajemen Data Warga (Edit & Hapus)",a5_narasi,a5_plantuml,a5_cols,a5_elems,a5_edges))

# ─────────────────────────────────────────────────────────────
# ALUR 6 — Ekspor Laporan Excel
# ─────────────────────────────────────────────────────────────
a6_narasi = (
    "Fitur ini tersedia bagi Admin, Staff, dan Camat untuk mengekstrak data klasifikasi ke format "
    "Excel (.xlsx). Pengguna membuka halaman Riwayat atau Laporan, lalu secara opsional mengatur "
    "filter berdasarkan rentang tanggal klasifikasi dan/atau status kelayakan (Semua, LAYAK, atau "
    "TIDAK LAYAK). Setelah pengguna mengeklik tombol Ekspor Excel, sistem menjalankan kueri ke "
    "tabel `classification_results` JOIN `warga` sesuai filter. Jika tidak ada data yang cocok, "
    "sistem membatalkan proses dan menampilkan notifikasi. Jika ada data, sistem menggunakan pustaka "
    "OpenPyXL untuk membuat file: membuat worksheet, menulis baris header (No, NIK, Nama, Nilai V, "
    "Status, Tanggal), mengisi baris data, lalu menerapkan format (bold header, border semua sel, "
    "auto-fit kolom). File dikirim sebagai HTTP response dengan header attachment sehingga browser "
    "pengguna mengunduhnya secara otomatis."
)

a6_plantuml = """@startuml
|#DAE8FC|Pengguna|
start
:Buka halaman Riwayat/Laporan;
:Atur filter (tanggal & status);
:Klik "Ekspor Excel";
|#FFF2CC|Database|
:Query `classification_results` JOIN `warga`\ndengan filter terpilih;
|#D5E8D4|Sistem|
if (Hasil query kosong?) then (Kosong)
  :Notifikasi "Tidak ada data";
  stop
else (Ada data)
  :Generate workbook OpenPyXL;
  :Buat worksheet & tulis header;
  :Isi baris data dari hasil query;
  :Terapkan format: bold, border, auto-fit;
  :Kirim file sebagai HTTP attachment;
  |Pengguna|
  :Browser mengunduh file `.xlsx`;
  stop
endif
@enduml"""

a6_cols = ["Pengguna", "Sistem", "Database"]
a6_elems = [
    ("start",  "start",    "",                                         0,  50),
    ("act1",   "activity", "Buka halaman Riwayat/Laporan",            0, 110),
    ("act2",   "activity", "Atur filter tanggal &amp; status",         0, 190),
    ("act3",   "activity", "Klik Ekspor Excel",                       0, 270),
    ("db1",    "activity", "Query data dengan filter",                 2, 270),
    ("dec1",   "decision", "Hasil\nKosong?",                          1, 350),
    ("err1",   "activity", "Notifikasi tidak ada data",               1, 460),
    ("end1",   "end",      "",                                         1, 540),
    ("act4",   "activity", "Generate workbook OpenPyXL",              1, 460),
    ("act5",   "activity", "Buat worksheet &amp; header",              1, 550),
    ("act6",   "activity", "Isi baris data",                          1, 640),
    ("act7",   "activity", "Format: bold, border, auto-fit",          1, 730),
    ("act8",   "activity", "Kirim file sebagai HTTP attachment",      1, 820),
    ("act9",   "activity", "Browser unduh file .xlsx",                0, 820),
    ("end2",   "end",      "",                                         0, 900),
]
a6_edges = [
    ("start","act1",""), ("act1","act2",""), ("act2","act3",""), ("act3","db1",""),
    ("db1","dec1",""), ("dec1","err1","Ya"), ("err1","end1",""),
    ("dec1","act4","Tidak"), ("act4","act5",""), ("act5","act6",""),
    ("act6","act7",""), ("act7","act8",""), ("act8","act9",""), ("act9","end2",""),
]

alur_blocks.append(alur_block(6,"Ekspor Laporan Excel",a6_narasi,a6_plantuml,a6_cols,a6_elems,a6_edges))

# ─────────────────────────────────────────────────────────────
# ALUR 7 — Pengaturan SPK (Kriteria & Sub Kriteria)
# ─────────────────────────────────────────────────────────────
a7_narasi = (
    "Alur eksklusif Admin untuk mengonfigurasi parameter inti metode SAW. Admin membuka menu "
    "Pengaturan SPK dan memilih sub-menu. Di Manajemen Kriteria, sistem menampilkan daftar dari "
    "tabel `kriteria`. Untuk tambah atau edit, Admin mengisi form (nama, bobot 0–1, tipe benefit/"
    "cost); sistem memvalidasi bahwa bobot bertipe numerik dan total seluruh bobot tidak melebihi "
    "1.0. Jika valid, sistem INSERT atau UPDATE ke tabel. Untuk hapus, sistem memeriksa apakah "
    "kriteria memiliki relasi di tabel `sub_kriteria`. Jika ada relasi, penghapusan dicegah untuk "
    "menjaga integritas referensial. Jika tidak ada, data dihapus. Di Manajemen Sub Kriteria, "
    "alur dan validasi yang sama diterapkan, namun merujuk pada tabel `sub_kriteria` dengan "
    "field: label, nilai_konversi, dan kriteria_id sebagai foreign key."
)

a7_plantuml = """@startuml
|#DAE8FC|Admin|
start
:Membuka menu Pengaturan SPK;
|#FFF2CC|Database|
:Query daftar kriteria dari `kriteria`;
|#D5E8D4|Sistem|
:Tampilkan daftar kriteria;
|Admin|
:Pilih aksi;
fork
  :Tambah / Edit Kriteria;
  :Isi form (nama, bobot, tipe);
  |Sistem|
  :Validasi bobot numerik & total ≤ 1.0;
  if (Valid?) then (Tidak)
    :Tampilkan pesan error spesifik;
    stop
  else (Ya)
    |Database|
    :INSERT / UPDATE tabel `kriteria`;
    |Sistem|
    :Notifikasi "Berhasil";
    stop
  endif
fork again
  |Admin|
  :Hapus Kriteria;
  |Sistem|
  :Tampilkan dialog konfirmasi;
  if (Konfirmasi?) then (Batal)
    stop
  else (Ya)
    |Database|
    :Cek relasi di tabel `sub_kriteria`;
    if (Ada relasi?) then (Ya)
      |Sistem|
      :Tampilkan "Tidak dapat dihapus\nada sub kriteria terkait";
      stop
    else (Tidak)
      :DELETE dari tabel `kriteria`;
      |Sistem|
      :Notifikasi "Berhasil dihapus";
      stop
    endif
  endif
end fork
@enduml"""

a7_cols = ["Admin", "Sistem", "Database"]
a7_elems = [
    ("start",  "start",    "",                                    0,  50),
    ("act1",   "activity", "Buka Pengaturan SPK",                0, 110),
    ("db1",    "activity", "Query daftar kriteria",              2, 110),
    ("act2",   "activity", "Tampilkan daftar kriteria",          1, 110),
    ("act3",   "activity", "Pilih aksi",                         0, 190),
    # Cabang Tambah/Edit
    ("act4",   "activity", "Tambah / Edit Kriteria",             0, 300),
    ("act5",   "activity", "Isi form (nama, bobot, tipe)",       0, 380),
    ("act6",   "activity", "Validasi bobot &amp; total ≤ 1.0",   1, 380),
    ("dec1",   "decision", "Valid?",                              1, 460),
    ("err1",   "activity", "Error validasi bobot",               1, 570),
    ("end1",   "end",      "",                                    1, 650),
    ("db2",    "activity", "INSERT/UPDATE `kriteria`",           2, 570),
    ("notif1", "activity", "Notifikasi berhasil",                1, 660),
    ("end2",   "end",      "",                                    1, 740),
    # Cabang Hapus
    ("act7",   "activity", "Hapus Kriteria",                     0, 300),
    ("act8",   "activity", "Dialog konfirmasi",                  1, 760),
    ("dec2",   "decision", "Konfirmasi?",                         1, 840),
    ("end3",   "end",      "",                                    1, 950),
    ("db3",    "activity", "Cek relasi sub_kriteria",            2, 950),
    ("dec3",   "decision", "Ada\nRelasi?",                       1, 960),
    ("err2",   "activity", "Error: tidak bisa dihapus",          1,1070),
    ("end4",   "end",      "",                                    1,1150),
    ("db4",    "activity", "DELETE dari `kriteria`",             2,1070),
    ("notif2", "activity", "Notifikasi berhasil dihapus",        1,1160),
    ("end5",   "end",      "",                                    1,1240),
]
a7_edges = [
    ("start","act1",""), ("act1","db1",""), ("db1","act2",""), ("act2","act3",""),
    ("act3","act4","Tambah/Edit"), ("act4","act5",""), ("act5","act6",""), ("act6","dec1",""),
    ("dec1","err1","Tidak"), ("err1","end1",""),
    ("dec1","db2","Ya"), ("db2","notif1",""), ("notif1","end2",""),
    ("act3","act7","Hapus"), ("act7","act8",""), ("act8","dec2",""),
    ("dec2","end3","Batal"),
    ("dec2","db3","Konfirmasi"), ("db3","dec3",""),
    ("dec3","err2","Ya"), ("err2","end4",""),
    ("dec3","db4","Tidak"), ("db4","notif2",""), ("notif2","end5",""),
]

alur_blocks.append(alur_block(7,"Pengaturan SPK (Kriteria & Sub Kriteria)",a7_narasi,a7_plantuml,a7_cols,a7_elems,a7_edges))

# ─────────────────────────────────────────────────────────────
# ALUR 8 — Manajemen Akun (Khusus Admin)
# ─────────────────────────────────────────────────────────────
a8_narasi = (
    "Fitur eksklusif Admin untuk mengelola seluruh akun pengguna sistem. Admin membuka menu "
    "Pengaturan Pengguna → Manajemen Akun; sistem menampilkan daftar akun dari tabel `users`. "
    "Untuk tambah akun, Admin mengisi form username, password, dan memilih role (Admin/Staff/"
    "Camat). Sistem memvalidasi keunikan username dan kekuatan password; jika valid, sistem "
    "melakukan hashing password menggunakan bcrypt/Werkzeug, lalu INSERT ke tabel `users` "
    "dengan `is_active = True`. Untuk edit akun, Admin dapat memperbarui nama, role, dan "
    "password. Jika field password diisi, sistem akan me-hash ulang; jika kosong, password lama "
    "dipertahankan. Untuk nonaktifkan/aktifkan, Admin mengklik toggle; sistem menampilkan "
    "dialog konfirmasi. Setelah dikonfirmasi, sistem meng-update field `is_active` (toggle "
    "True ↔ False) dan menampilkan notifikasi perubahan."
)

a8_plantuml = """@startuml
|#DAE8FC|Admin|
start
:Buka menu "Manajemen Akun";
|#FFF2CC|Database|
:Query daftar akun dari `users`;
|#D5E8D4|Sistem|
:Tampilkan daftar akun;
|Admin|
:Pilih aksi;
fork
  :Tambah Akun Baru;
  :Isi form (username, password, role);
  |Sistem|
  :Validasi keunikan username & kekuatan password;
  if (Valid?) then (Tidak)
    :Tampilkan pesan error;
    stop
  else (Ya)
    |Sistem|
    :Hash password (bcrypt/Werkzeug);
    |Database|
    :INSERT ke `users` (is_active=True);
    |Sistem|
    :Notifikasi "Akun berhasil dibuat";
    stop
  endif
fork again
  |Admin|
  :Edit Akun / Ubah Role;
  :Ubah data → Submit;
  |Sistem|
  if (Password baru diisi?) then (Ya)
    |Sistem|
    :Hash password baru;
    |Database|
    :UPDATE password_hash & data lain;
  else (Tidak)
    |Database|
    :UPDATE data selain password;
  endif
  |Sistem|
  :Notifikasi "Akun berhasil diperbarui";
  stop
fork again
  |Admin|
  :Toggle Aktif / Nonaktif;
  |Sistem|
  :Tampilkan dialog konfirmasi;
  if (Setuju?) then (Batal)
    stop
  else (Konfirmasi)
    |Database|
    :UPDATE is_active (True ↔ False);
    |Sistem|
    :Notifikasi perubahan status;
    stop
  endif
end fork
@enduml"""

a8_cols = ["Admin", "Sistem", "Database"]
a8_elems = [
    ("start",  "start",    "",                                       0,  50),
    ("act1",   "activity", "Buka Manajemen Akun",                   0, 110),
    ("db1",    "activity", "Query daftar akun",                     2, 110),
    ("act2",   "activity", "Tampilkan daftar akun",                 1, 110),
    ("act3",   "activity", "Pilih aksi",                            0, 190),
    # Cabang Tambah
    ("act4",   "activity", "Tambah Akun Baru",                      0, 300),
    ("act5",   "activity", "Isi form (username, pass, role)",       0, 380),
    ("act6",   "activity", "Validasi username &amp; password",       1, 380),
    ("dec1",   "decision", "Valid?",                                  1, 460),
    ("err1",   "activity", "Error validasi",                         1, 570),
    ("end1",   "end",      "",                                        1, 650),
    ("act7",   "activity", "Hash password (bcrypt)",                 1, 570),
    ("db2",    "activity", "INSERT ke `users` (is_active=True)",     2, 570),
    ("notif1", "activity", "Notifikasi akun dibuat",                 1, 660),
    ("end2",   "end",      "",                                        1, 740),
    # Cabang Edit
    ("act8",   "activity", "Edit Akun / Ubah Role",                  0, 300),
    ("act9",   "activity", "Ubah data → Submit",                     0, 380),
    ("dec2",   "decision", "Pass baru\ndiisi?",                      1, 760),
    ("act10",  "activity", "Hash password baru",                     1, 870),
    ("db3",    "activity", "UPDATE password_hash &amp; data",        2, 870),
    ("db4",    "activity", "UPDATE data selain password",            2, 960),
    ("notif2", "activity", "Notifikasi akun diperbarui",             1, 960),
    ("end3",   "end",      "",                                        1,1040),
    # Cabang Toggle
    ("act11",  "activity", "Toggle Aktif/Nonaktif",                  0, 300),
    ("act12",  "activity", "Dialog konfirmasi",                      1,1060),
    ("dec3",   "decision", "Setuju?",                                 1,1140),
    ("end4",   "end",      "",                                        1,1250),
    ("db5",    "activity", "UPDATE is_active (True↔False)",          2,1250),
    ("notif3", "activity", "Notifikasi perubahan status",            1,1340),
    ("end5",   "end",      "",                                        1,1420),
]
a8_edges = [
    ("start","act1",""), ("act1","db1",""), ("db1","act2",""), ("act2","act3",""),
    ("act3","act4","Tambah"), ("act4","act5",""), ("act5","act6",""), ("act6","dec1",""),
    ("dec1","err1","Tidak"), ("err1","end1",""),
    ("dec1","act7","Ya"), ("act7","db2",""), ("db2","notif1",""), ("notif1","end2",""),
    ("act3","act8","Edit"), ("act8","act9",""), ("act9","dec2",""),
    ("dec2","act10","Ya"), ("act10","db3",""), ("db3","notif2",""),
    ("dec2","db4","Tidak"), ("db4","notif2",""),
    ("notif2","end3",""),
    ("act3","act11","Aktif/Nonaktif"), ("act11","act12",""), ("act12","dec3",""),
    ("dec3","end4","Batal"),
    ("dec3","db5","Konfirmasi"), ("db5","notif3",""), ("notif3","end5",""),
]

alur_blocks.append(alur_block(8,"Manajemen Akun (Khusus Admin)",a8_narasi,a8_plantuml,a8_cols,a8_elems,a8_edges))

# ──────────────────────────────────────────────
# TULIS KE FILE
# ──────────────────────────────────────────────
out_path = r"c:\Jovankasd\kerja praktek\Sistem Klasifikasi bansos(Final)\UML\Activitydiagram\activity_diagrams.md"
with open(out_path, "w", encoding="utf-8") as f:
    f.write("# Dokumentasi Activity Diagram — SPK Bansos SAW\n\n")
    for block in alur_blocks:
        f.write(block)

print(f"Selesai! File ditulis ke: {out_path}")
