"""
=============================================================================
 config.py — Konfigurasi Terpusat Sistem SPK Bansos Pondok Aren
=============================================================================
 File ini berisi SELURUH parameter konfigurasi yang digunakan oleh aplikasi.
 Jika ada perubahan regulasi pemerintah (misalnya bobot penilaian berubah,
 kelurahan bertambah, atau ambang batas diperbarui), cukup ubah di file
 ini saja tanpa perlu menyentuh logika utama di app.py atau spk.py.
=============================================================================
"""

import os


def load_local_env():
    """Muat variabel dari file .env di root proyek jika file tersebut ada."""
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    env_path = os.path.join(root_dir, '.env')
    if not os.path.exists(env_path):
        return

    with open(env_path, 'r', encoding='utf-8') as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue

            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if key and key not in os.environ:
                os.environ[key] = value


load_local_env()

# ---------------------------------------------------------------------------
#  KONFIGURASI FLASK
# ---------------------------------------------------------------------------

# SECRET_KEY digunakan oleh Flask untuk mengenkripsi session & cookie.
# Untuk repo publik, jangan simpan nilai rahasia asli di source code.
SECRET_KEY = os.environ.get('SPK_SECRET_KEY', 'dev-secret-change-this-before-production')

# Lokasi database SQLite. Format: 'sqlite:///path/ke/file.db'
# Database disimpan di folder backend/database/ agar terpisah dari kode.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, 'database')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DATABASE_DIR, 'penduduk.db')

# Menonaktifkan notifikasi perubahan objek SQLAlchemy (menghemat memori).
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Folder untuk menyimpan file upload dari fitur Import Massal.
UPLOAD_FOLDER = os.path.join(BASE_DIR, '..', 'uploads')


# ---------------------------------------------------------------------------
#  PARAMETER SPK — AMBANG BATAS KELAYAKAN
# ---------------------------------------------------------------------------
# Skor akhir SAW dibandingkan dengan ambang batas berikut untuk
# menentukan status kelayakan warga:
#
#   skor >= THRESHOLD_LAYAK  → "Layak"
#   skor <  THRESHOLD_LAYAK  → "Tidak Layak"

THRESHOLD_LAYAK = 0.50        # Batas minimum skor untuk status "Layak"


# ---------------------------------------------------------------------------
#  DAFTAR KELURAHAN KECAMATAN PONDOK AREN
# ---------------------------------------------------------------------------
# Daftar 11 kelurahan resmi di Kecamatan Pondok Aren, Kota Tangerang Selatan.
# Digunakan untuk mengisi dropdown <select> di halaman Klasifikasi & Edit.

DAFTAR_KELURAHAN = [
    'Pondok Aren',
    'Jurang Mangu Barat',
    'Jurang Mangu Timur',
    'Pondok Jaya',
    'Pondok Kacang Barat',
    'Pondok Kacang Timur',
    'Perigi Baru',
    'Perigi Lama',
    'Pondok Pucung',
    'Pondok Karya',
    'Pondok Betung',
]


# ---------------------------------------------------------------------------
#  OPSI DROPDOWN UNTUK KRITERIA KLASIFIKASI
# ---------------------------------------------------------------------------
# Opsi-opsi ini digunakan pada formulir input manual dan edit data.
# Setiap list berisi pilihan yang valid untuk masing-masing kriteria.

# Status kepemilikan rumah warga.
OPSI_STATUS_RUMAH = [
    'Milik Sendiri',
    'Kontrak',
    'Sewa',
    'Menumpang',
    'Tanpa Tempat Tinggal',
]

# Material utama bangunan tempat tinggal.
OPSI_KONDISI_BANGUNAN = [
    'Semen/Batu Bata',
    'Kayu',
    'Bambu',
    'Tanah',
]

# Sumber air bersih yang digunakan sehari-hari.
OPSI_SUMBER_AIR = [
    'PDAM',
    'Sumur Bor',
    'Sumur Tangan',
    'Sungai/Hujan',
]

# Daya listrik terpasang di rumah (dalam VA).
OPSI_DAYA_LISTRIK = [
    'Tanpa Listrik',
    '450',
    '900',
    '1300',
    '>2200',
]


# ---------------------------------------------------------------------------
#  LABEL HASIL KLASIFIKASI
# ---------------------------------------------------------------------------

LABEL_LAYAK = 'Layak'
LABEL_TIDAK_LAYAK = 'Tidak Layak'


# ---------------------------------------------------------------------------
#  AKUN ADMIN DEFAULT
# ---------------------------------------------------------------------------
# Akun admin awal dibaca dari environment variable agar tidak hardcoded
# di repository publik. Nilai fallback hanya untuk development lokal.
DEFAULT_ADMIN_USERNAME = os.environ.get('SPK_DEFAULT_ADMIN_USERNAME', 'admin')
DEFAULT_ADMIN_PASSWORD = os.environ.get(
    'SPK_DEFAULT_ADMIN_PASSWORD',
    'change-me-before-production'
)
