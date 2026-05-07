"""
=============================================================================
 spk.py — Modul Perhitungan Sistem Pendukung Keputusan (SAW) Dinamis
=============================================================================
 File ini berisi seluruh logika perhitungan SPK untuk menentukan kelayakan
 penerima Bantuan Sosial (Bansos) dengan Kriteria Dinamis.
=============================================================================
"""

import sqlite3
import json
import config


def get_kriteria_dari_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM kriteria")
        kriteria = [dict(row) for row in cursor.fetchall()]
        
        # Ambil max skor untuk setiap kriteria dari tabel sub_kriteria
        for k in kriteria:
            cursor.execute("SELECT MAX(skor) as max_skor FROM sub_kriteria WHERE kriteria_id = ?", (k['id'],))
            row = cursor.fetchone()
            k['max_skor'] = row['max_skor'] if row and row['max_skor'] else 5
    except sqlite3.OperationalError:
        kriteria = []
    conn.close()
    return kriteria


def get_data_from_db(db_path):
    """
    Mengambil seluruh data warga dari database SQLite.
    Untuk data lama, jika kriteria_details kosong, kita buat fallback
    (walaupun tidak 100% akurat untuk kriteria dinamis).
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM classification_results")
        baris_data = cursor.fetchall()
        data_numerik = []

        for baris in baris_data:
            details_str = baris['kriteria_details']
            skor_dinamis = {}
            if details_str:
                try:
                    skor_dinamis = json.loads(details_str)
                except:
                    pass
            
            data_numerik.append({
                'id': baris['id'],
                'nama': baris['nama'],
                'nik': baris['nik'],
                'skor_dinamis': skor_dinamis,  # dict of str(kriteria_id) -> skor
            })
    except sqlite3.OperationalError:
        data_numerik = []

    conn.close()
    return data_numerik


def hitung_saw(data, db_path):
    """
    Menghitung skor SAW dengan kriteria dinamis.
    """
    kriteria_list = get_kriteria_dari_db(db_path)
    if not data or not kriteria_list:
        return []

    hasil_saw = []
    for d in data:
        d_copy = dict(d)
        skor_saw = 0.0
        
        for k in kriteria_list:
            k_id = str(k['id'])
            nilai = float(d['skor_dinamis'].get(k_id, 3)) # fallback 3
            max_skor = float(k.get('max_skor', 5))
            
            # Guard: hindari pembagi nol jika tidak ada sub-kriteria
            if max_skor == 0:
                max_skor = 5.0
            
            # Berdasarkan instruksi: Cost dan Benefit sama-sama menggunakan nilai / max_skor
            # karena nilai Cost sudah "dibalik" skornya di database (1=Kaya, 5=Miskin)
            r = nilai / max_skor
                
            skor_saw += r * k['bobot']

        d_copy['skor_saw'] = round(skor_saw, 4)
        hasil_saw.append(d_copy)

    # Urutkan
    hasil_saw.sort(key=lambda x: x.get('skor_saw', 0), reverse=True)
    return hasil_saw


def generate_alasan_dinamis(item, kriteria_list, status_kelayakan):
    relatif = []
    for k in kriteria_list:
        skor = float(item['skor_dinamis'].get(str(k['id']), 3))
        if k['tipe'] == 'Cost':
            r = (5.0 - skor) / 4.0 
        else:
            r = (skor - 1.0) / 4.0
        relatif.append((k['nama'], r))
        
    relatif.sort(key=lambda x: x[1], reverse=True)
    
    if not relatif:
        return ""
        
    if status_kelayakan == config.LABEL_LAYAK:
        if len(relatif) >= 2:
            return f"Sangat layak karena memiliki skor baik pada kriteria {relatif[0][0]} dan {relatif[1][0]}."
        else:
            return f"Sangat layak pada kriteria {relatif[0][0]}."
    else:
        if len(relatif) >= 2:
            return f"Kurang layak karena nilai rendah pada kriteria {relatif[-1][0]} dan {relatif[-2][0]}."
        else:
            return f"Kurang layak pada kriteria {relatif[-1][0]}."


def tentukan_kelayakan(hasil_saw, db_path):
    kriteria_list = get_kriteria_dari_db(db_path)
    hasil_final = []
    
    for item in hasil_saw:
        skor_saw = item.get('skor_saw', 0)

        if skor_saw >= config.THRESHOLD_LAYAK:
            status_kelayakan = config.LABEL_LAYAK
        else:
            status_kelayakan = config.LABEL_TIDAK_LAYAK

        alasan = generate_alasan_dinamis(item, kriteria_list, status_kelayakan)

        item_final = dict(item)
        item_final['status_kelayakan'] = status_kelayakan
        item_final['alasan'] = alasan
        hasil_final.append(item_final)

    hasil_final.sort(key=lambda x: x.get('skor_saw', 0), reverse=True)
    return hasil_final

def hitung_status_kelayakan_dinamis(data_spk, id_target, db_path):
    hasil_saw = hitung_saw(data_spk, db_path)
    hasil_final = tentukan_kelayakan(hasil_saw, db_path)

    for item in hasil_final:
        if str(item['id']) == str(id_target):
            return item['status_kelayakan'], item.get('alasan', ''), item.get('skor_saw', 0.0)

    return config.LABEL_TIDAK_LAYAK, '', 0.0
