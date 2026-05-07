"""
=============================================================================
 spk.py - Modul Perhitungan Sistem Pendukung Keputusan (SAW) Dinamis
=============================================================================
 File ini berisi logika perhitungan SPK yang independen dari jenis database.
 Data kriteria dan data warga dikirim dari app.py setelah diambil lewat ORM.
=============================================================================
"""

import config


def hitung_saw(data, kriteria_list):
    """
    Menghitung skor SAW dengan kriteria dinamis.

    Args:
        data (list[dict]): Data warga/calon dalam format numerik.
        kriteria_list (list[dict]): Daftar kriteria beserta bobot dan max_skor.
    """
    if not data or not kriteria_list:
        return []

    hasil_saw = []
    for d in data:
        d_copy = dict(d)
        skor_saw = 0.0

        for k in kriteria_list:
            k_id = str(k['id'])
            nilai = float(d['skor_dinamis'].get(k_id, 3))
            max_skor = float(k.get('max_skor', 5) or 5)

            if max_skor == 0:
                max_skor = 5.0

            # Skor cost di database sudah dibalik (1 kaya, 5 miskin),
            # jadi normalisasi cukup nilai / max_skor untuk semua kriteria.
            r = nilai / max_skor
            skor_saw += r * float(k['bobot'])

        d_copy['skor_saw'] = round(skor_saw, 4)
        hasil_saw.append(d_copy)

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
        return f"Sangat layak pada kriteria {relatif[0][0]}."

    if len(relatif) >= 2:
        return f"Kurang layak karena nilai rendah pada kriteria {relatif[-1][0]} dan {relatif[-2][0]}."
    return f"Kurang layak pada kriteria {relatif[-1][0]}."


def tentukan_kelayakan(hasil_saw, kriteria_list):
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


def hitung_status_kelayakan_dinamis(data_spk, id_target, kriteria_list):
    hasil_saw = hitung_saw(data_spk, kriteria_list)
    hasil_final = tentukan_kelayakan(hasil_saw, kriteria_list)

    for item in hasil_final:
        if str(item['id']) == str(id_target):
            return item['status_kelayakan'], item.get('alasan', ''), item.get('skor_saw', 0.0)

    return config.LABEL_TIDAK_LAYAK, '', 0.0
