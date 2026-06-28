import json
import os

FILE_SAVE = "data_skor.json"

def muat_semua_data():
    """Memuat semua data pemain dari file JSON"""
    if not os.path.exists(FILE_SAVE):
        return {}
    try:
        with open(FILE_SAVE, "r") as f:
            return json.load(f)
    except:
        return {}

def simpan_semua_data(data):
    """Menyimpan data ke file JSON"""
    with open(FILE_SAVE, "w") as f:
        json.dump(data, f, indent=4)

def simpan_skor_pemain(nama, jenis_pesawat, skor_baru):
    """Menyimpan atau mengupdate high score pemain berdasarkan jenis pesawat"""
    nama = nama.strip().upper()
    if not nama:
        return
        
    data = muat_semua_data()
    
    if nama not in data:
        data[nama] = {
            "PESAWAT_BIASA": 0,
            "PESAWAT_BOMBER": 0,
            "PESAWAT_RAPTOR": 0
        }
        
    if skor_baru > data[nama].get(jenis_pesawat, 0):
        data[nama][jenis_pesawat] = skor_baru
        
    simpan_semua_data(data)

def ambil_high_score_pemain(nama, jenis_pesawat):
    """Mengambil high score milik pemain untuk pesawat tertentu"""
    nama = nama.strip().upper()
    data = muat_semua_data()
    if nama in data:
        return data[nama].get(jenis_pesawat, 0)
    return 0