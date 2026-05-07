"""
=============================================================================
 app.py — Entry Point Aplikasi Flask: Sistem SPK Bansos Pondok Aren
=============================================================================
 File ini adalah entry point aplikasi Flask untuk Sistem Pendukung Keputusan
 (SPK) Kelayakan Penerima Bantuan Sosial di Kecamatan Pondok Aren,
 Kota Tangerang Selatan.

 Fitur Utama:
   1. Autentikasi Admin (Login / Logout)
   2. Dashboard Statistik & Grafik
   3. Klasifikasi Data (Manual & Import Massal via Excel/CSV)
   4. Manajemen Histori (Lihat, Edit, Hapus, Export Excel)
   5. Informasi Kriteria SPK

 Arsitektur:
   backend/
   ├── app.py      → Entry point & routing (file ini)
   ├── config.py   → Konfigurasi, bobot kriteria, ambang batas
   ├── spk.py      → Logika perhitungan SAW
   └── database/
       └── penduduk.db → Database SQLite

   frontend/
   ├── templates/  → Halaman HTML (Jinja2)
   └── static/     → CSS, JS, dan file statis

 Cara Menjalankan:
   $ cd backend
   $ python app.py
   → Buka http://127.0.0.1:5000 di browser
=============================================================================
"""

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, send_file, jsonify
)
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import pandas as pd
import os
import io
import json

import config
from spk import (
    get_data_from_db,
    hitung_status_kelayakan_dinamis,
)


# ===========================================================================
#  INISIALISASI APLIKASI FLASK
# ===========================================================================
# Template dan static files berada di folder ../frontend/
# agar pemisahan Frontend dan Backend tetap jelas.

app = Flask(
    __name__,
    template_folder='../frontend/templates',
    static_folder='../frontend/static',
)

# Muat konfigurasi dari config.py
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['DB_INIT_ERROR'] = None

# Pastikan folder database ada.
if not os.path.exists(config.DATABASE_DIR):
    os.makedirs(config.DATABASE_DIR)

# Hubungkan SQLAlchemy dengan aplikasi Flask.
db = SQLAlchemy()
db.init_app(app)


@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    Gunakan journal di memori agar SQLite tetap bisa menulis pada lingkungan
    yang gagal membuat file journal di disk.
    """
    try:
        cursor = dbapi_connection.cursor()
        cursor.execute('PRAGMA journal_mode=MEMORY')
        cursor.execute('PRAGMA synchronous=OFF')
        cursor.close()
    except Exception:
        # Abaikan koneksi non-SQLite atau koneksi yang belum siap.
        pass


# ===========================================================================
#  MODEL DATABASE (SQLAlchemy ORM)
# ===========================================================================
# Definisi model ditempatkan di sini agar app.py menjadi satu-satunya entry
# point. Untuk proyek berskala besar, model bisa dipindahkan ke models.py.
#
# Skema Tabel:
#   1. users                  → Data akun administrator
#   2. classification_results → Data warga & hasil klasifikasi SPK

class User(db.Model):
    """
    =========================================================================
     Tabel: users — Akun Administrator Sistem
    =========================================================================
     Kolom:
     ┌───────────────┬──────────────┬─────────────────────────────────────┐
     │ Nama Kolom    │ Tipe Data    │ Keterangan                          │
     ├───────────────┼──────────────┼─────────────────────────────────────┤
     │ id            │ Integer (PK) │ ID unik auto-increment              │
     │ username      │ String(50)   │ Nama pengguna, harus unik           │
     │ password_hash │ String(255)  │ Password yang sudah di-hash         │
     │ created_at    │ DateTime     │ Waktu akun dibuat (otomatis)        │
     └───────────────┴──────────────┴─────────────────────────────────────┘
    =========================================================================
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nama_lengkap = db.Column(db.String(100), nullable=True)
    foto_profil = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

class LoginHistory(db.Model):
    __tablename__ = 'login_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    login_time = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(50), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    
    user = db.relationship('User', backref=db.backref('login_histories', lazy=True, cascade="all, delete-orphan"))


class Kriteria(db.Model):
    __tablename__ = 'kriteria'
    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(10), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    tipe = db.Column(db.String(20), nullable=False) # 'Benefit' / 'Cost'
    bobot = db.Column(db.Float, nullable=False)
    
    sub_kriteria = db.relationship('SubKriteria', backref='kriteria', lazy=True, cascade="all, delete-orphan")


class SubKriteria(db.Model):
    __tablename__ = 'sub_kriteria'
    id = db.Column(db.Integer, primary_key=True)
    kriteria_id = db.Column(db.Integer, db.ForeignKey('kriteria.id'), nullable=False)
    nama = db.Column(db.String(255), nullable=False)
    skor = db.Column(db.Integer, nullable=False)



class ClassificationResult(db.Model):
    """
    =========================================================================
     Tabel: classification_results — Data Warga & Hasil Klasifikasi SPK
    =========================================================================
     Kolom dibagi menjadi 3 kelompok:
       A. Data Identitas Warga (informasi pribadi)
       B. Kriteria Klasifikasi (dinamis, disimpan sebagai JSON)
       C. Hasil & Metadata (output klasifikasi SAW dan timestamp)

     ┌──────────────────────┬──────────────┬─────────────────────────────────────────┐
     │ Nama Kolom           │ Tipe Data    │ Keterangan                              │
     ├──────────────────────┼──────────────┼─────────────────────────────────────────┤
     │ id                   │ Integer (PK) │ ID unik auto-increment                  │
     │ nik                  │ String(20)   │ Nomor Induk Kependudukan (16 digit)     │
     │ no_kk                │ String(20)   │ Nomor Kartu Keluarga (16 digit)         │
     │ nama                 │ String(100)  │ Nama lengkap sesuai KTP                 │
     │ pekerjaan            │ String(100)  │ Jenis pekerjaan warga                   │
     │ alamat               │ Text         │ Alamat lengkap (Jalan, RT/RW, dsb.)     │
     │ kelurahan            │ String(100)  │ Kelurahan di Kec. Pondok Aren           │
     │ penghasilan          │ Integer      │ [Legacy] Penghasilan (kolom lama)        │
     │ jumlah_tanggungan    │ Integer      │ [Legacy] Tanggungan (kolom lama)         │
     │ status_rumah         │ String(50)   │ [Legacy] Status rumah (kolom lama)       │
     │ kondisi_bangunan     │ String(50)   │ [Legacy] Kondisi bangunan (kolom lama)   │
     │ sumber_air           │ String(50)   │ [Legacy] Sumber air (kolom lama)         │
     │ daya_listrik         │ String(50)   │ [Legacy] Daya listrik (kolom lama)       │
     │ kriteria_details     │ Text (JSON)  │ Skor per kriteria dinamis {krit_id:skor} │
     │ skor_saw             │ Float        │ Nilai skor dari metode SAW              │
     │ hasil_klasifikasi    │ String(20)   │ "Layak" / "Tidak Layak"                 │
     │ alasan               │ Text         │ Penjelasan otomatis hasil SAW           │
     │ created_at           │ DateTime     │ Waktu klasifikasi dilakukan             │
     └──────────────────────┴──────────────┴─────────────────────────────────────────┘
    =========================================================================
    """
    __tablename__ = 'classification_results'

    # --- A. Data Identitas Warga ---
    id = db.Column(db.Integer, primary_key=True)
    nik = db.Column(db.String(20), nullable=False)
    no_kk = db.Column(db.String(20), nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    pekerjaan = db.Column(db.String(100), nullable=False)
    alamat = db.Column(db.Text, nullable=False)
    kelurahan = db.Column(db.String(100), nullable=False)

    # --- B. Kriteria Klasifikasi (Legacy — data baru disimpan di kriteria_details) ---
    penghasilan = db.Column(db.Integer, nullable=False)
    jumlah_tanggungan = db.Column(db.Integer, nullable=False)
    status_rumah = db.Column(db.String(50), nullable=False)
    kondisi_bangunan = db.Column(db.String(50), nullable=False)
    sumber_air = db.Column(db.String(50), nullable=False)
    daya_listrik = db.Column(db.String(50), nullable=False)

    # --- C. Hasil & Metadata ---
    skor_saw = db.Column(db.Float, nullable=True)
    hasil_klasifikasi = db.Column(db.String(20), nullable=False)
    alasan = db.Column(db.Text, nullable=True)
    kriteria_details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Klasifikasi #{self.id} {self.nama}: {self.hasil_klasifikasi}>'


# ===========================================================================
#  INISIALISASI DATABASE & DATA AWAL
# ===========================================================================

def init_app():
    """
    Menjalankan inisialisasi saat aplikasi pertama kali dimulai:
      1. Membuat semua tabel database jika belum ada.
      2. Membuat akun admin default jika belum ada.
      3. Membuat folder upload jika belum ada.
    """
    # Buat tabel database berdasarkan definisi model di atas.
    db.create_all()

    # Pastikan kolom alasan ada di database (untuk migrasi schema dari versi sebelumnya)
    with db.engine.connect() as conn:
        try:
            conn.execute(db.text("ALTER TABLE classification_results ADD COLUMN alasan TEXT"))
            conn.commit()
        except Exception:
            pass
        try:
            conn.execute(db.text("ALTER TABLE classification_results ADD COLUMN kriteria_details TEXT"))
            conn.commit()
        except Exception:
            pass
        try:
            conn.execute(db.text("ALTER TABLE users ADD COLUMN nama_lengkap TEXT"))
            conn.commit()
        except Exception:
            pass
        try:
            conn.execute(db.text("ALTER TABLE users ADD COLUMN foto_profil TEXT"))
            conn.commit()
        except Exception:
            pass

    # Buat akun admin default jika belum ada di database.
    admin = User.query.filter_by(username=config.DEFAULT_ADMIN_USERNAME).first()
    if not admin:
        admin_baru = User(
            username=config.DEFAULT_ADMIN_USERNAME,
            password_hash=generate_password_hash(config.DEFAULT_ADMIN_PASSWORD)
        )
        db.session.add(admin_baru)
        db.session.commit()

    # Buat folder upload jika belum ada.
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        
    profiles_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'profiles')
    if not os.path.exists(profiles_dir):
        os.makedirs(profiles_dir)
        
    seed_kriteria()

def seed_kriteria():
    if Kriteria.query.count() > 0:
        return
        
    data_kriteria = [
        {'kode': 'C1', 'nama': 'Penghasilan', 'tipe': 'Cost', 'bobot': 0.25, 'subs': [
            {'> Rp 3.000.000': 1}, {'Rp 2.000.001 - Rp 3.000.000': 2}, {'Rp 1.000.001 - Rp 2.000.000': 3}, {'Rp 500.001 - Rp 1.000.000': 4}, {'≤ Rp 500.000 / Tidak Tetap': 5}
        ]},
        {'kode': 'C2', 'nama': 'Jumlah Tanggungan', 'tipe': 'Benefit', 'bobot': 0.20, 'subs': [
            {'1 Orang': 1}, {'2 Orang': 2}, {'3 Orang': 3}, {'4 Orang': 4}, {'> 4 Orang': 5}
        ]},
        {'kode': 'C3', 'nama': 'Kepemilikan Aset', 'tipe': 'Cost', 'bobot': 0.15, 'subs': [
            {'Memiliki Mobil': 1}, {'Memiliki Motor > 1 atau Motor Baru': 2}, {'Memiliki 1 Motor (Lama/Biasa)': 3}, {'Memiliki Sepeda / Elektronik Sederhana': 4}, {'Tidak Memiliki Aset Apapun': 5}
        ]},
        {'kode': 'C4', 'nama': 'Status Rumah', 'tipe': 'Cost', 'bobot': 0.10, 'subs': [
            {'Milik Sendiri': 1}, {'Menumpang (Keluarga)': 2}, {'Sewa / Kontrak': 3}, {'Bukan Milik Sendiri (Lahan Negara/Ilegal)': 4}, {'Tidak Memiliki Tempat Tinggal': 5}
        ]},
        {'kode': 'C5', 'nama': 'Kondisi Bangunan', 'tipe': 'Cost', 'bobot': 0.10, 'subs': [
            {'Permanen': 1}, {'Semi Permanen': 2}, {'Papan / Kayu': 3}, {'Bambu / Anyaman (Gubug)': 4}, {'Tanah / Atap Rumbia/Seng Rusak': 5}
        ]},
        {'kode': 'C6', 'nama': 'Daya Listrik', 'tipe': 'Cost', 'bobot': 0.10, 'subs': [
            {'> 2200 VA': 1}, {'1300 VA': 2}, {'900 VA': 3}, {'450 VA': 4}, {'Tanpa Listrik / Numpang': 5}
        ]},
        {'kode': 'C7', 'nama': 'Sumber Air', 'tipe': 'Cost', 'bobot': 0.10, 'subs': [
            {'PDAM': 1}, {'Sumur Bor (Pompa Pribadi)': 2}, {'Sumur Gali (Timba/Bersama)': 3}, {'Sungai / Mata Air': 4}, {'Air Hujan / Beli Eceran': 5}
        ]}
    ]

    for k_data in data_kriteria:
        k = Kriteria(kode=k_data['kode'], nama=k_data['nama'], tipe=k_data['tipe'], bobot=k_data['bobot'])
        db.session.add(k)
        db.session.flush() # get k.id
        for sub in k_data['subs']:
            for nama, skor in sub.items():
                sk = SubKriteria(kriteria_id=k.id, nama=nama, skor=skor)
                db.session.add(sk)
    db.session.commit()


# Jalankan inisialisasi dalam application context.
with app.app_context():
    try:
        init_app()
    except Exception as e:
        app.config['DB_INIT_ERROR'] = str(e)
        app.logger.exception('Inisialisasi database gagal')


# ===========================================================================
#  HELPER FUNCTIONS (Fungsi Pembantu)
# ===========================================================================

def is_logged_in():
    """Mengecek apakah pengguna sudah login dengan melihat session."""
    return 'user_id' in session


def database_siaga():
    """Mengecek apakah database berhasil diinisialisasi."""
    return not app.config.get('DB_INIT_ERROR')


def redirect_jika_database_bermasalah(target_endpoint):
    """
    Redirect dengan pesan error jika database belum siap digunakan.

    Returns:
        Response | None
    """
    if database_siaga():
        return None

    flash(
        'Database belum siap digunakan. Periksa file SQLite aplikasi terlebih dahulu.',
        'error'
    )
    return redirect(url_for(target_endpoint))


def extract_input_klasifikasi(form_data):
    """
    Mengekstrak 6 fitur kriteria klasifikasi dari data form HTML.
    Digunakan oleh route klasifikasi manual dan edit record.

    Parameter:
        form_data: request.form (ImmutableMultiDict dari Flask)

    Returns:
        dict: Dictionary berisi 6 fitur untuk perhitungan SPK.
    """
    details = {}
    for krit in Kriteria.query.all():
        sub_id = form_data.get(f'kriteria_{krit.id}')
        if sub_id:
            sub = SubKriteria.query.get(sub_id)
            if sub:
                details[str(krit.id)] = sub.skor
    return details


def buat_record_klasifikasi(data_identitas, input_klasifikasi, hasil, alasan='', skor_saw=0.0):
    """
    Membuat objek ClassificationResult baru dari data yang diberikan.

    Parameter:
        data_identitas (dict): Data pribadi warga (nik, nama, alamat, dsb.)
        input_klasifikasi (dict): 6 fitur kriteria dari extract_input_klasifikasi()
        hasil (str): Hasil prediksi ("Layak" / "Tidak Layak" / "Perlu Verifikasi")
        alasan (str): Penjelasan hasil prediksi
        skor_saw (float): Skor akhir metode SAW

    Returns:
        ClassificationResult: Objek ORM yang siap ditambahkan ke database.
    """
    return ClassificationResult(
        nik=data_identitas['nik'],
        no_kk=data_identitas['no_kk'],
        nama=data_identitas['nama'],
        pekerjaan=data_identitas['pekerjaan'],
        alamat=data_identitas['alamat'],
        kelurahan=data_identitas['kelurahan'],
        penghasilan=0,
        jumlah_tanggungan=0,
        status_rumah='',
        kondisi_bangunan='',
        sumber_air='',
        daya_listrik='',
        kriteria_details=json.dumps(input_klasifikasi) if input_klasifikasi else None,
        skor_saw=round(skor_saw, 4),
        hasil_klasifikasi=hasil,
        alasan=alasan,
    )


def get_opsi_form():
    """
    Mengembalikan dictionary berisi semua opsi dropdown form.
    Diambil dari config.py agar konsisten dan mudah diubah.
    Dikirim ke template Jinja2 untuk di-render secara dinamis.

    Returns:
        dict: Berisi daftar kelurahan dan opsi-opsi dropdown kriteria.
    """
    return {
        'daftar_kelurahan': config.DAFTAR_KELURAHAN,
        'opsi_status_rumah': config.OPSI_STATUS_RUMAH,
        'opsi_kondisi_bangunan': config.OPSI_KONDISI_BANGUNAN,
        'opsi_sumber_air': config.OPSI_SUMBER_AIR,
        'opsi_daya_listrik': config.OPSI_DAYA_LISTRIK,
    }


def simpan_perubahan_db(pesan_sukses, redirect_endpoint, pesan_error=None, **kwargs):
    """Commit perubahan database dengan rollback otomatis saat gagal."""
    try:
        db.session.commit()
        flash(pesan_sukses, 'success')
    except Exception as e:
        db.session.rollback()
        flash(
            pesan_error or f'Terjadi kesalahan saat menyimpan data: {str(e)}',
            'error'
        )
    return redirect(url_for(redirect_endpoint, **kwargs))


def baca_dataframe_upload(file_storage):
    """Validasi file upload lalu baca isinya langsung ke DataFrame tanpa menyimpan ke disk."""
    filename_aman = secure_filename(file_storage.filename or '')
    if not filename_aman:
        raise ValueError('Nama file tidak valid.')

    ekstensi = os.path.splitext(filename_aman)[1].lower()
    if ekstensi not in ['.csv', '.xls', '.xlsx']:
        raise ValueError('Format file harus .csv, .xls, atau .xlsx.')

    file_storage.stream.seek(0)
    if ekstensi == '.csv':
        return pd.read_csv(file_storage.stream), ekstensi
    return pd.read_excel(file_storage.stream), ekstensi


def resolve_db_path():
    """
    Menentukan path absolut ke file database SQLite untuk digunakan
    oleh modul SPK (yang membutuhkan path langsung, bukan URI SQLAlchemy).

    Returns:
        str: Path absolut ke file penduduk.db
    """
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    db_path = db_uri.replace('sqlite:///', '')

    # Jika path tidak absolut, gunakan fallback ke lokasi default.
    if not os.path.isabs(db_path):
        db_path = os.path.join(config.DATABASE_DIR, 'penduduk.db')

    return db_path




# ===========================================================================
#  ROUTE: AUTENTIKASI (Login, Logout)
# ===========================================================================

@app.route('/')
def login_page():
    """Menampilkan halaman login. Jika sudah login, redirect ke dashboard."""
    if is_logged_in():
        return redirect(url_for('dashboard'))
    return render_template(
        'index.html',
        database_ready=database_siaga(),
        database_error=app.config.get('DB_INIT_ERROR')
    )


@app.route('/health')
def health_check():
    """
    Endpoint ringan untuk mengecek kesiapan aplikasi dan database.
    Berguna untuk diagnosa tanpa harus membuka file SQLite manual.
    """
    status_code = 200 if database_siaga() else 503
    return jsonify({
        'status': 'ok' if database_siaga() else 'degraded',
        'database_ready': database_siaga(),
        'database_uri': app.config.get('SQLALCHEMY_DATABASE_URI'),
        'database_error': app.config.get('DB_INIT_ERROR'),
    }), status_code


@app.route('/login', methods=['POST'])
def login():
    """
    Memproses form login.
    Memverifikasi username dan password terhadap database.
    Jika berhasil, menyimpan user_id dan username ke session.
    """
    db_error_redirect = redirect_jika_database_bermasalah('login_page')
    if db_error_redirect:
        return db_error_redirect

    username = request.form.get('username')
    password = request.form.get('password')

    # Cari user berdasarkan username di database.
    user = User.query.filter_by(username=username).first()

    # Verifikasi password menggunakan hash comparison.
    if user and check_password_hash(user.password_hash, password):
        session['user_id'] = user.id
        session['username'] = user.username
        
        # Simpan informasi tambahan ke session
        session['nama_lengkap'] = user.nama_lengkap
        session['foto_profil'] = user.foto_profil
        
        # Catat riwayat login
        history = LoginHistory(
            user_id=user.id,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        db.session.add(history)
        db.session.commit()
        
        return redirect(url_for('dashboard'))

    # Login gagal — tampilkan pesan error.
    flash('Username atau password salah', 'error')
    return redirect(url_for('login_page'))


@app.route('/logout')
def logout():
    """Menghapus session dan redirect ke halaman login."""
    session.clear()
    return redirect(url_for('login_page'))


# ===========================================================================
#  ROUTE: PROFIL ADMIN & KEAMANAN
# ===========================================================================

@app.route('/profil', methods=['GET', 'POST'])
def profil():
    if not is_logged_in():
        return redirect(url_for('login_page'))
        
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        nama_lengkap = request.form.get('nama_lengkap', '').strip()
        user.nama_lengkap = nama_lengkap
        
        # Handle file upload
        if 'foto_profil' in request.files:
            file = request.files['foto_profil']
            if file and file.filename != '':
                filename = secure_filename(f"{user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
                # Simpan foto di dalam static agar bisa diakses via url_for('static')
                profiles_dir = os.path.join(app.static_folder, 'uploads', 'profiles')
                os.makedirs(profiles_dir, exist_ok=True)
                filepath = os.path.join(profiles_dir, filename)
                file.save(filepath)
                user.foto_profil = f"uploads/profiles/{filename}"
                
        db.session.commit()
        
        # Update session
        session['nama_lengkap'] = user.nama_lengkap
        session['foto_profil'] = user.foto_profil
        
        flash('Profil berhasil diperbarui.', 'success')
        return redirect(url_for('profil'))
        
    return render_template('profil.html', user=user)


@app.route('/ganti-password', methods=['GET', 'POST'])
def ganti_password():
    if not is_logged_in():
        return redirect(url_for('login_page'))
        
    if request.method == 'POST':
        password_lama = request.form.get('password_lama')
        password_baru = request.form.get('password_baru')
        konfirmasi_password = request.form.get('konfirmasi_password')
        
        user = User.query.get(session['user_id'])
        
        if not check_password_hash(user.password_hash, password_lama):
            flash('Password lama salah.', 'error')
        elif password_baru != konfirmasi_password:
            flash('Konfirmasi password tidak cocok.', 'error')
        elif len(password_baru) < 6:
            flash('Password baru minimal 6 karakter.', 'error')
        else:
            user.password_hash = generate_password_hash(password_baru)
            db.session.commit()
            flash('Password berhasil diubah.', 'success')
            return redirect(url_for('dashboard'))
            
    return render_template('ganti_password.html')


@app.route('/riwayat-login')
def riwayat_login():
    if not is_logged_in():
        return redirect(url_for('login_page'))
        
    histories = LoginHistory.query.filter_by(user_id=session['user_id']).order_by(LoginHistory.login_time.desc()).limit(20).all()
    return render_template('riwayat_login.html', histories=histories)


# ===========================================================================
#  ROUTE: DASHBOARD
# ===========================================================================

@app.route('/dashboard')
def dashboard():
    """
    Menampilkan halaman Dashboard dengan statistik ringkasan:
      - Total data warga yang sudah diklasifikasi
      - Jumlah & persentase warga Layak dan Tidak Layak
      - Grafik Pie (distribusi kelayakan)
      - Grafik Bar (perbandingan per kelurahan)
    """
    if not is_logged_in():
        return redirect(url_for('login_page'))
    db_error_redirect = redirect_jika_database_bermasalah('login_page')
    if db_error_redirect:
        return db_error_redirect

    # Hitung statistik keseluruhan.
    total_warga = ClassificationResult.query.count()
    jumlah_layak = ClassificationResult.query.filter_by(
        hasil_klasifikasi=config.LABEL_LAYAK
    ).count()
    jumlah_tidak_layak = ClassificationResult.query.filter_by(
        hasil_klasifikasi=config.LABEL_TIDAK_LAYAK
    ).count()

    # Hitung jumlah warga per kelurahan untuk grafik bar chart.
    kelurahan_data = db.session.query(
        ClassificationResult.kelurahan,
        db.func.count(ClassificationResult.id)
    ).group_by(ClassificationResult.kelurahan).all()

    # Format data chart: pisahkan label (nama kelurahan) dan data (jumlah).
    chart_labels = [k[0] for k in kelurahan_data]
    chart_data = [k[1] for k in kelurahan_data]

    return render_template(
        'dashboard.html',
        total=total_warga,
        layak=jumlah_layak,
        tidak_layak=jumlah_tidak_layak,
        chart_labels=json.dumps(chart_labels),
        chart_data=json.dumps(chart_data),
    )


# ===========================================================================
#  ROUTE: KLASIFIKASI DATA (Manual & Import Massal)
# ===========================================================================

@app.route('/classification', methods=['GET', 'POST'])
def classification():
    """
    Menampilkan halaman Klasifikasi Data dengan 2 mode input:
      1. Input Manual — admin mengisi form satu per satu.
      2. Import Massal — admin mengunggah file Excel/CSV.

    Pada POST:
      - Jika ada file yang diunggah → proses batch (Import Massal).
      - Jika ada data form → proses manual (Input Manual).
      - Hasil prediksi disimpan ke database, lalu redirect ke Histori.
    """
    if not is_logged_in():
        return redirect(url_for('login_page'))
    db_error_redirect = redirect_jika_database_bermasalah('login_page')
    if db_error_redirect:
        return db_error_redirect

    if request.method == 'POST':

        # === Mode 1: Import Massal (File Upload) ===
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                try:
                    df, _ = baca_dataframe_upload(file)

                    # Ambil data SPK dari database sekali saja (optimasi).
                    db_path = resolve_db_path()
                    data_spk = get_data_from_db(db_path)
                    kriteria_list = Kriteria.query.all()
                    subkriteria_map = {}
                    for sub in SubKriteria.query.all():
                        subkriteria_map.setdefault(sub.kriteria_id, []).append(sub)

                    # Proses setiap baris data dalam file.
                    for _, row in df.iterrows():
                        nik_val = str(row['nik']).strip()
                        if nik_val.endswith('.0'):
                            nik_val = nik_val[:-2]
                        no_kk_val = str(row['no_kk']).strip()
                        if no_kk_val.endswith('.0'):
                            no_kk_val = no_kk_val[:-2]

                        if len(nik_val) != 16 or not nik_val.isdigit():
                            raise ValueError(f"NIK harus 16 digit angka. Ditemukan: '{nik_val}'")
                        if len(no_kk_val) != 16 or not no_kk_val.isdigit():
                            raise ValueError(f"No. KK harus 16 digit angka. Ditemukan: '{no_kk_val}'")

                        input_klasifikasi = {}
                        for krit in kriteria_list:
                            val_str = ""
                            if krit.kode in row:
                                val_str = str(row[krit.kode])
                            elif krit.nama in row:
                                val_str = str(row[krit.nama])
                            elif 'penghasilan' in row and 'penghasilan' in krit.nama.lower():
                                val_str = str(row['penghasilan'])
                            elif 'jumlah_tanggungan' in row and 'tanggungan' in krit.nama.lower():
                                val_str = str(row['jumlah_tanggungan'])
                            elif 'kondisi_bangunan' in row and 'kondisi bangunan' in krit.nama.lower():
                                val_str = str(row['kondisi_bangunan'])
                            elif 'sumber_air' in row and ('sumber air' in krit.nama.lower() or 'sanitasi' in krit.nama.lower()):
                                val_str = str(row['sumber_air'])
                            elif 'daya_listrik' in row and 'daya listrik' in krit.nama.lower():
                                val_str = str(row['daya_listrik'])
                            elif 'status_rumah' in row and 'status rumah' in krit.nama.lower():
                                val_str = str(row['status_rumah'])

                            val_str = val_str.strip()
                            sub = None
                            if val_str:
                                val_lower = val_str.lower()
                                for kandidat_sub in subkriteria_map.get(krit.id, []):
                                    if val_lower in kandidat_sub.nama.lower():
                                        sub = kandidat_sub
                                        break
                            
                            if sub:
                                input_klasifikasi[str(krit.id)] = sub.skor
                            else:
                                input_klasifikasi[str(krit.id)] = 3

                        item_numerik_baru = {
                            'id': 'NEW',
                            'nama': 'Calon',
                            'nik': '0',
                            'skor_dinamis': input_klasifikasi,
                        }

                        data_kalkulasi = data_spk + [item_numerik_baru]
                        hasil, alasan, skor_saw = hitung_status_kelayakan_dinamis(data_kalkulasi, 'NEW', db_path)

                        # Update data baseline agar iterasi massal akurat.
                        item_numerik_baru['id'] = len(data_spk) + 10000
                        item_numerik_baru['status_kelayakan'] = hasil
                        item_numerik_baru['skor_saw'] = skor_saw
                        data_spk.append(item_numerik_baru)

                        # Buat record dan tambahkan ke database.
                        data_identitas = {
                            'nik': nik_val,
                            'no_kk': no_kk_val,
                            'nama': str(row['nama']),
                            'pekerjaan': str(row['pekerjaan']),
                            'alamat': str(row['alamat']),
                            'kelurahan': str(row['kelurahan']),
                        }
                        record_baru = buat_record_klasifikasi(
                            data_identitas, input_klasifikasi, hasil, alasan, skor_saw
                        )
                        db.session.add(record_baru)

                    # Simpan semua record sekaligus ke database.
                    return simpan_perubahan_db(
                        f'Sukses memproses {len(df)} data!',
                        'history',
                        'Gagal menyimpan hasil import ke database.'
                    )
                except Exception as e:
                    db.session.rollback()
                    flash(
                        f'Gagal memproses file. Pastikan format sesuai! Detail: {str(e)}',
                        'error'
                    )

                return redirect(url_for('history'))

        # === Mode 2: Input Manual (Form HTML) ===
        input_klasifikasi = extract_input_klasifikasi(request.form)

        # Guard: pastikan form manual benar-benar diisi (bukan submit kosong).
        if request.form.get('nik'):
            nik_val = request.form.get('nik', '').strip()
            no_kk_val = request.form.get('no_kk', '').strip()

            if len(nik_val) != 16 or not nik_val.isdigit():
                flash('NIK harus 16 digit angka', 'error')
                return redirect(url_for('classification'))
            
            if len(no_kk_val) != 16 or not no_kk_val.isdigit():
                flash('No. KK harus 16 digit angka', 'error')
                return redirect(url_for('classification'))

            db_path = resolve_db_path()
            data_spk = get_data_from_db(db_path)

            item_numerik_baru = {
                'id': 'NEW',
                'nama': 'Calon',
                'nik': '0',
                'skor_dinamis': input_klasifikasi,
            }
            data_spk.append(item_numerik_baru)

            # Hitung status kelayakan menggunakan SAW.
            hasil, alasan, skor_saw = hitung_status_kelayakan_dinamis(data_spk, 'NEW', db_path)

            # Kumpulkan data identitas dari form.
            data_identitas = {
                'nik': request.form.get('nik'),
                'no_kk': request.form.get('no_kk'),
                'nama': request.form.get('nama'),
                'pekerjaan': request.form.get('pekerjaan'),
                'alamat': request.form.get('alamat'),
                'kelurahan': request.form.get('kelurahan'),
            }

            # Simpan ke database.
            record_baru = buat_record_klasifikasi(
                data_identitas, input_klasifikasi, hasil, alasan, skor_saw
            )
            db.session.add(record_baru)
            return simpan_perubahan_db(
                f'Data klasifikasi manual tersimpan. Hasil = {hasil}',
                'history',
                'Gagal menyimpan data klasifikasi manual ke database.'
            )

    # GET request — tampilkan halaman form klasifikasi.
    # Kriteria dinamis
    daftar_kriteria = Kriteria.query.order_by(Kriteria.kode).all()
    # Opsi dropdown dikirim dari config agar template tidak perlu hardcode.
    return render_template('classification.html', daftar_kriteria=daftar_kriteria, **get_opsi_form())


# ===========================================================================
#  ROUTE: MANAJEMEN KRITERIA & SUB-KRITERIA
# ===========================================================================

@app.route('/kriteria', methods=['GET', 'POST'])
def kriteria():
    if not is_logged_in():
        return redirect(url_for('login_page'))
    db_error_redirect = redirect_jika_database_bermasalah('login_page')
    if db_error_redirect:
        return db_error_redirect

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            kode = request.form.get('kode')
            nama = request.form.get('nama')
            tipe = request.form.get('tipe')
            bobot = float(request.form.get('bobot'))
            
            # Validasi bobot persis 1.0
            total_current = db.session.query(db.func.sum(Kriteria.bobot)).scalar() or 0
            if round(total_current + bobot, 4) > 1.0:
                flash(f'Gagal tambah: Total bobot akan melebihi 1.0 (Sekarang: {round(total_current, 4)})', 'error')
                return redirect(url_for('kriteria'))
            
            baru = Kriteria(kode=kode, nama=nama, tipe=tipe, bobot=bobot)
            db.session.add(baru)
            return simpan_perubahan_db('Kriteria berhasil ditambahkan.', 'kriteria')
            
        elif action == 'edit':
            k_id = request.form.get('id')
            k = Kriteria.query.get_or_404(k_id)
            k.kode = request.form.get('kode')
            k.nama = request.form.get('nama')
            k.tipe = request.form.get('tipe')
            
            new_bobot = float(request.form.get('bobot'))
            total_current = db.session.query(db.func.sum(Kriteria.bobot)).scalar() or 0
            sum_others = total_current - k.bobot
            
            if round(sum_others + new_bobot, 4) > 1.0:
                 flash(f'Gagal edit: Total bobot melebihi 1.0 (Total akan menjadi: {round(sum_others + new_bobot, 4)})', 'error')
                 return redirect(url_for('kriteria'))
                 
            k.bobot = new_bobot
            return simpan_perubahan_db('Kriteria berhasil diupdate.', 'kriteria')
            
        elif action == 'delete':
            k_id = request.form.get('id')
            k = Kriteria.query.get_or_404(k_id)
            db.session.delete(k)
            return simpan_perubahan_db('Kriteria berhasil dihapus.', 'kriteria')
            
        elif action == 'save_all_bobot':
            total = 0.0
            updates = []
            for key, val in request.form.items():
                if key.startswith('bobot_'):
                    k_id = key.split('_')[1]
                    bobot_val = float(val)
                    total += bobot_val
                    updates.append((k_id, bobot_val))
                    
            if round(total, 4) != 1.0:
                flash(f'Total seluruh bobot harus persis 1.0! (Total saat ini: {round(total, 4)})', 'error')
                return redirect(url_for('kriteria'))
                
            for k_id, b_val in updates:
                k = Kriteria.query.get(k_id)
                if k:
                    k.bobot = b_val
            return simpan_perubahan_db('Seluruh bobot berhasil diperbarui.', 'kriteria')

    data_kriteria = Kriteria.query.order_by(Kriteria.kode).all()
    total_bobot = sum([k.bobot for k in data_kriteria])
    return render_template('kriteria.html', kriteria=data_kriteria, total_bobot=round(total_bobot, 4))


@app.route('/sub-kriteria/<int:kriteria_id>', methods=['GET', 'POST'])
def sub_kriteria(kriteria_id):
    if not is_logged_in():
        return redirect(url_for('login_page'))
    db_error_redirect = redirect_jika_database_bermasalah('login_page')
    if db_error_redirect:
        return db_error_redirect
        
    k = Kriteria.query.get_or_404(kriteria_id)
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            nama = request.form.get('nama')
            skor = int(request.form.get('skor'))
            baru = SubKriteria(kriteria_id=k.id, nama=nama, skor=skor)
            db.session.add(baru)
            return simpan_perubahan_db('Sub-Kriteria berhasil ditambahkan.', 'sub_kriteria', kriteria_id=k.id)
            
        elif action == 'edit':
            sk_id = request.form.get('id')
            sk = SubKriteria.query.get_or_404(sk_id)
            sk.nama = request.form.get('nama')
            sk.skor = int(request.form.get('skor'))
            return simpan_perubahan_db('Sub-Kriteria berhasil diupdate.', 'sub_kriteria', kriteria_id=k.id)
            
        elif action == 'delete':
            sk_id = request.form.get('id')
            sk = SubKriteria.query.get_or_404(sk_id)
            db.session.delete(sk)
            return simpan_perubahan_db('Sub-Kriteria berhasil dihapus.', 'sub_kriteria', kriteria_id=k.id)

    subs = SubKriteria.query.filter_by(kriteria_id=k.id).order_by(SubKriteria.skor.desc()).all()
    return render_template('sub_kriteria.html', kriteria=k, sub_kriteria=subs)


# ===========================================================================
#  ROUTE: INFORMASI KRITERIA SPK
# ===========================================================================

@app.route('/informasi')
def informasi():
    """Menampilkan halaman informasi kriteria dan bobot SPK."""
    if not is_logged_in():
        return redirect(url_for('login_page'))
    db_error_redirect = redirect_jika_database_bermasalah('login_page')
    if db_error_redirect:
        return db_error_redirect
    daftar_kriteria = Kriteria.query.order_by(Kriteria.kode).all()
    return render_template('informasi.html', daftar_kriteria=daftar_kriteria)


# ===========================================================================
#  ROUTE: MANAJEMEN HISTORI (Lihat, Cari, Hapus, Edit, Export)
# ===========================================================================

@app.route('/history')
def history():
    """
    Menampilkan halaman Manajemen Histori.
    Mendukung pencarian berdasarkan NIK, Nama, atau Kelurahan.
    Data ditampilkan urut dari yang terbaru (descending).
    """
    if not is_logged_in():
        return redirect(url_for('login_page'))
    db_error_redirect = redirect_jika_database_bermasalah('login_page')
    if db_error_redirect:
        return db_error_redirect

    # Ambil kata kunci pencarian dari query string (?search=...).
    search_query = request.args.get('search', '')
    query = ClassificationResult.query

    # Filter berdasarkan kata kunci jika ada.
    if search_query:
        search_term = f"%{search_query}%"
        query = query.filter(
            db.or_(
                ClassificationResult.nik.ilike(search_term),
                ClassificationResult.nama.ilike(search_term),
                ClassificationResult.kelurahan.ilike(search_term),
            )
        )

    # Urutkan dari yang terbaru dan kirim ke template.
    results = query.order_by(ClassificationResult.created_at.desc()).all()
    return render_template('history.html', results=results, search_query=search_query)


@app.route('/api/history')
def api_history():
    """Endpoint untuk mengambil data histori dalam format JSON dengan filter kelurahan."""
    if not is_logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
        
    kelurahan = request.args.get('kelurahan')
    search_query = request.args.get('search')
    query = ClassificationResult.query
    
    if kelurahan and kelurahan != 'all':
        query = query.filter_by(kelurahan=kelurahan)
        
    if search_query:
        search_term = f"%{search_query}%"
        query = query.filter(
            db.or_(
                ClassificationResult.nik.ilike(search_term),
                ClassificationResult.nama.ilike(search_term),
                ClassificationResult.kelurahan.ilike(search_term),
            )
        )
        
    # Urutkan berdasarkan skor_saw tertinggi (descending)
    results = query.order_by(ClassificationResult.skor_saw.desc()).all()
    
    kriteria_list = Kriteria.query.order_by(Kriteria.kode).all()
    data = []
    for r in results:
        details = {}
        if r.kriteria_details:
            try:
                details = json.loads(r.kriteria_details)
            except:
                pass
                
        detail_html = ""
        for k in kriteria_list:
            skor = details.get(str(k.id), 0)
            detail_html += f"<div class='text-[10px] sm:text-[11px] text-gray-500 whitespace-nowrap'><b>{k.kode}</b>: {skor}</div>"

        data.append({
            'id': r.id,
            'created_at': r.created_at.strftime('%d %b %Y %H:%M') if r.created_at else '',
            'created_at_time': r.created_at.strftime('%H:%M') if r.created_at else '',
            'nik': r.nik,
            'nama': r.nama,
            'kelurahan': r.kelurahan,
            'detail_html': detail_html,
            'hasil_klasifikasi': r.hasil_klasifikasi,
            'alasan': r.alasan,
            'skor_saw': round(r.skor_saw, 2) if r.skor_saw is not None else 0.00
        })
        
    return jsonify(data)


@app.route('/delete/<int:id>', methods=['POST'])
def delete_record(id):
    """Menghapus satu record klasifikasi berdasarkan ID."""
    if not is_logged_in():
        return redirect(url_for('login_page'))
    db_error_redirect = redirect_jika_database_bermasalah('login_page')
    if db_error_redirect:
        return db_error_redirect

    record = ClassificationResult.query.get_or_404(id)
    db.session.delete(record)
    return simpan_perubahan_db(
        'Data berhasil dihapus dari histori.',
        'history',
        'Gagal menghapus data dari histori.'
    )


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_record(id):
    """
    Menampilkan dan memproses halaman Edit Data Histori.

    GET  → Menampilkan form edit dengan data record yang ada.
    POST → Menyimpan perubahan, menghitung ulang prediksi SPK (atau override manual).
    """
    if not is_logged_in():
        return redirect(url_for('login_page'))
    db_error_redirect = redirect_jika_database_bermasalah('login_page')
    if db_error_redirect:
        return db_error_redirect

    record = ClassificationResult.query.get_or_404(id)

    if request.method == 'POST':
        nik_val = request.form.get('nik', '').strip()
        no_kk_val = request.form.get('no_kk', '').strip()

        if len(nik_val) != 16 or not nik_val.isdigit():
            flash('NIK harus 16 digit angka', 'error')
            return redirect(url_for('edit_record', id=record.id))
        
        if len(no_kk_val) != 16 or not no_kk_val.isdigit():
            flash('No. KK harus 16 digit angka', 'error')
            return redirect(url_for('edit_record', id=record.id))

        # Ekstrak 6 fitur klasifikasi dari form.
        input_klasifikasi = extract_input_klasifikasi(request.form)

        # Hitung ulang prediksi berdasarkan data baru.
        db_path = resolve_db_path()
        data_spk = get_data_from_db(db_path)

        # Hapus data lama dari list untuk digantikan data yang diperbarui.
        data_spk = [d for d in data_spk if d['id'] != record.id]

        # Konversi input baru ke format numerik.
        item_diperbarui = {
            'id': record.id,
            'nama': record.nama,
            'nik': record.nik,
            'skor_dinamis': input_klasifikasi,
        }
        data_spk.append(item_diperbarui)

        # Hitung ulang status kelayakan dengan data yang sudah diperbarui.
        hasil, alasan, skor_saw = hitung_status_kelayakan_dinamis(data_spk, record.id, db_path)

        # Cek apakah admin memilih untuk override hasil secara manual.
        manual_override = request.form.get('override_status')
        if manual_override and manual_override in [config.LABEL_LAYAK, config.LABEL_TIDAK_LAYAK]:
            hasil = manual_override

        record.nik = request.form.get('nik')
        record.no_kk = request.form.get('no_kk')
        record.nama = request.form.get('nama')
        record.pekerjaan = request.form.get('pekerjaan')
        record.alamat = request.form.get('alamat')
        record.kelurahan = request.form.get('kelurahan')
        record.kriteria_details = json.dumps(input_klasifikasi) if input_klasifikasi else None
        record.skor_saw = round(skor_saw, 4)
        record.hasil_klasifikasi = hasil
        record.alasan = alasan

        return simpan_perubahan_db(
            'Data histori berhasil diperbarui.',
            'history',
            'Gagal memperbarui data histori.'
        )

    # GET request — tampilkan form edit.
    daftar_kriteria = Kriteria.query.order_by(Kriteria.kode).all()
    # parse the currently selected kriteria details
    skor_terpilih = {}
    if record.kriteria_details:
        try:
            skor_terpilih = json.loads(record.kriteria_details)
        except:
            pass
            
    return render_template('edit_history.html', record=record, daftar_kriteria=daftar_kriteria, skor_terpilih=skor_terpilih, **get_opsi_form())


# ===========================================================================
#  ROUTE: EXPORT DATA KE EXCEL
# ===========================================================================

@app.route('/export/excel')
def export_excel():
    """
    Mengekspor data histori klasifikasi ke file Excel (.xlsx).
    Mendukung filter berdasarkan kelurahan.
    """
    if not is_logged_in():
        return redirect(url_for('login_page'))
    db_error_redirect = redirect_jika_database_bermasalah('login_page')
    if db_error_redirect:
        return db_error_redirect

    kelurahan_filter = request.args.get('kelurahan')
    search_query = request.args.get('search')
    query = ClassificationResult.query

    if kelurahan_filter and kelurahan_filter != 'all':
        query = query.filter_by(kelurahan=kelurahan_filter)

    if search_query:
        search_term = f"%{search_query}%"
        query = query.filter(
            db.or_(
                ClassificationResult.nik.ilike(search_term),
                ClassificationResult.nama.ilike(search_term),
                ClassificationResult.kelurahan.ilike(search_term),
            )
        )

    results = query.order_by(ClassificationResult.skor_saw.desc()).all()

    kriteria_list = Kriteria.query.order_by(Kriteria.kode).all()

    # Prefetch seluruh sub-kriteria dalam satu query (optimasi: hindari N×K query)
    all_subs = SubKriteria.query.all()
    sub_lookup = {}  # { (kriteria_id, skor): nama_sub }
    for s in all_subs:
        sub_lookup[(s.kriteria_id, s.skor)] = s.nama

    data = []
    for r in results:
        row_dict = {
            'Tgl/Waktu': r.created_at.strftime('%Y-%m-%d %H:%M') if r.created_at else '',
            'NIK': r.nik,
            'No KK': r.no_kk,
            'Nama Lengkap': r.nama,
            'Pekerjaan': r.pekerjaan,
            'Alamat': r.alamat,
            'Kelurahan': r.kelurahan,
        }
        
        details = {}
        if r.kriteria_details:
            try:
                details = json.loads(r.kriteria_details)
            except:
                pass
                
        for k in kriteria_list:
            skor = details.get(str(k.id), 0)
            nama_sub = sub_lookup.get((k.id, skor))
            row_dict[k.nama] = f"{nama_sub} (Skor: {skor})" if nama_sub else f"Skor: {skor}"
            
        row_dict['Skor SAW'] = r.skor_saw
        row_dict['Hasil Klasifikasi'] = r.hasil_klasifikasi
        row_dict['Alasan'] = r.alasan
        
        data.append(row_dict)

    # Buat file Excel di memori (tanpa menyimpan ke disk).
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Histori Klasifikasi')
    output.seek(0)
    
    filename = f"Histori_Bansos_{kelurahan_filter.replace(' ', '_') if kelurahan_filter and kelurahan_filter != 'all' else 'Semua'}.xlsx"

    return send_file(
        output,
        download_name=filename,
        as_attachment=True
    )


# ===========================================================================
#  ROUTE: HAPUS SELURUH DATA
# ===========================================================================

@app.route('/delete_all', methods=['POST'])
def delete_all():
    """Menghapus seluruh record di tabel classification_results."""
    if not is_logged_in():
        return redirect(url_for('login_page'))
    db_error_redirect = redirect_jika_database_bermasalah('login_page')
    if db_error_redirect:
        return db_error_redirect

    try:
        ClassificationResult.query.delete()
        db.session.commit()
        flash('Seluruh data histori berhasil dihapus!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Terjadi kesalahan saat menghapus data: {str(e)}', 'error')

    return redirect(url_for('history'))


# ===========================================================================
#  ENTRY POINT
# ===========================================================================

if __name__ == '__main__':
    # Debug diaktifkan hanya jika diminta lewat environment variable agar
    # perilaku default lebih aman untuk repo yang dibagikan.
    debug_mode = os.environ.get('FLASK_DEBUG', '').strip().lower() in ('1', 'true', 'yes')
    app.run(debug=debug_mode, use_reloader=False, port=5000)
