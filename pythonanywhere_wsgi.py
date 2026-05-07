"""
Contoh isi file WSGI untuk PythonAnywhere.

Langkah pakai:
1. Upload / clone proyek ini ke home directory PythonAnywhere Anda.
2. Buka tab Web > WSGI configuration file.
3. Ganti isi file WSGI bawaan PythonAnywhere dengan adaptasi dari file ini.
4. Ubah nilai project_home sesuai username dan nama folder proyek Anda.
"""

import os
import sys


project_home = "/home/USERNAME_ANDA/Kerja-Praktek-SPK-metode-SAW-BANSOS"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

backend_path = os.path.join(project_home, "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

os.environ.setdefault("SPK_SECRET_KEY", "ganti-dengan-secret-random")
os.environ.setdefault("SPK_DEFAULT_ADMIN_USERNAME", "admin")
os.environ.setdefault("SPK_DEFAULT_ADMIN_PASSWORD", "ganti-password-awal")
os.environ.setdefault("FLASK_DEBUG", "0")

from app import app as application
