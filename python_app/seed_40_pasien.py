"""
Seed 40 data pasien DBD dari Data-40.xlsx (Sheet: Data_Asli_Nama)
+ data kasus bulanan otomatis
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import PasienDBD, KasusBulanan
from datetime import date, timedelta

app = create_app()

# 40 data pasien dari sheet Data_Asli_Nama
DATA_PASIEN = [
    # (Bulan, Nama, Usia, Lama Rawat, Jumlah Kasus Perbulan, JK)
    ('Januari',   'Rezki Mhd',              18,  2, 12, 'L'),
    ('Januari',   'Selfiolla',               14,  4, 12, 'P'),
    ('Januari',   'M.Albiruni',              12,  1, 12, 'L'),
    ('Februari',  'Kalmani',                 66,  5,  7, 'L'),
    ('Februari',  'Nayra Dhika',              2,  3,  7, 'P'),
    ('Februari',  'Andri Naldi',             49,  4,  7, 'L'),
    ('Maret',     'Mayang',                  81,  5, 14, 'P'),
    ('Maret',     'Janibar',                 75,  4, 14, 'L'),
    ('Maret',     'Hendra Wadi',             37,  4, 14, 'L'),
    ('April',     'Yandril',                 40,  3,  4, 'L'),
    ('April',     'Romy Herina',             27,  1,  4, 'L'),
    ('April',     'Ilham Saputra',           28,  4,  4, 'L'),
    ('Mei',       'Basri',                   50,  5, 13, 'L'),
    ('Mei',       'Yuharni',                 64,  5, 13, 'P'),
    ('Mei',       'Tiara Putri',             19,  5, 13, 'P'),
    ('Juni',      'Fitri Novita',            28,  4, 15, 'P'),
    ('Juni',      'Elianti',                 68,  4, 15, 'P'),
    ('Juni',      'Reza Refninda',           29,  3, 15, 'L'),
    ('Juli',      'Aqlan Havizh',             3,  5, 10, 'L'),
    ('Juli',      'Dzacky Claresta',         15,  3, 10, 'L'),
    ('Juli',      'Arumi Putri',              9,  4, 10, 'P'),
    ('Agustus',   'Putri Maylia',            27,  9, 13, 'P'),
    ('Agustus',   'Muthi Navisa',            23,  3, 13, 'P'),
    ('Agustus',   'Mutia Diva',              21,  3, 13, 'P'),
    ('September', 'Zulfa Yenti',             56,  4, 18, 'P'),
    ('September', 'Syahlan Yuanda',          16,  2, 18, 'L'),
    ('September', 'Kenzi Romanja',           16,  2, 18, 'L'),
    ('Oktober',   'Naura Salsabila',         10,  2, 33, 'P'),
    ('Oktober',   'Reza Chaniago',           10,  3, 33, 'L'),
    ('Oktober',   'Humaira Denifa',           6,  4, 33, 'P'),
    ('November',  'Yanti Devina',            19,  5, 21, 'P'),
    ('November',  'Syafrizal',               61,  5, 21, 'L'),
    ('November',  'Weri Oktavia',            24,  3, 21, 'P'),
    ('Desember',  'Febrianto Angger',        22,  3,  3, 'L'),
    ('Desember',  'Desrizal',                34,  4,  3, 'L'),
    ('Desember',  'Aprillia Khairunnisa',    10,  6,  3, 'P'),
    ('Januari',   'Nini Efriza',             47,  2, 12, 'P'),
    ('Februari',  'Shecillia Hanifah',       15,  5,  7, 'P'),
    ('Maret',     'Haziq Arsyad',            10,  5, 14, 'L'),
    ('Juni',      'Yusuf Andrian',            7,  4, 15, 'L'),
]

# Mapping bulan ke angka (untuk tanggal)
BULAN_MAP = {
    'Januari': 1, 'Februari': 2, 'Maret': 3, 'April': 4,
    'Mei': 5, 'Juni': 6, 'Juli': 7, 'Agustus': 8,
    'September': 9, 'Oktober': 10, 'November': 11, 'Desember': 12
}

TAHUN = 2024  # Tahun data

with app.app_context():
    # --- 1. Hapus data pasien lama ---
    existing = PasienDBD.query.count()
    if existing > 0:
        print(f"Menghapus {existing} data pasien lama...")
        PasienDBD.query.delete()
        db.session.commit()
    
    # --- 2. Hapus data kasus bulanan lama ---
    existing_kb = KasusBulanan.query.count()
    if existing_kb > 0:
        print(f"Menghapus {existing_kb} data kasus bulanan lama...")
        KasusBulanan.query.delete()
        db.session.commit()

    # --- 3. Insert 40 data pasien ---
    print("Memasukkan 40 data pasien...")
    day_counter = {}  # track hari per bulan agar tanggal berbeda
    
    for i, (bulan, nama, usia, lama_rawat, jml_kasus, jk) in enumerate(DATA_PASIEN):
        bulan_num = BULAN_MAP[bulan]
        
        # Buat tanggal masuk yang berbeda per pasien dalam bulan yang sama
        if bulan not in day_counter:
            day_counter[bulan] = 1
        else:
            day_counter[bulan] += 2
        
        day = min(day_counter[bulan], 28)  # max 28 agar aman semua bulan
        tanggal_masuk = date(TAHUN, bulan_num, day)
        tanggal_keluar = tanggal_masuk + timedelta(days=lama_rawat)
        
        no_rm = f"RM-2024-{i+1:04d}"
        
        pasien = PasienDBD(
            no_rm=no_rm,
            nama_pasien=nama,
            usia=usia,
            jenis_kelamin=jk,
            alamat='Kab. Agam',
            tanggal_masuk=tanggal_masuk,
            tanggal_keluar=tanggal_keluar,
            lama_rawat=lama_rawat,
            bulan=bulan,
            tahun=TAHUN
        )
        db.session.add(pasien)
    
    db.session.commit()
    print(f"  -> {PasienDBD.query.count()} pasien berhasil ditambahkan")

    # --- 4. Insert data kasus bulanan berdasarkan jumlah kasus per bulan dari data ---
    # Ambil jumlah kasus unik per bulan dari data
    kasus_per_bulan = {}
    for bulan, nama, usia, lama_rawat, jml_kasus, jk in DATA_PASIEN:
        kasus_per_bulan[bulan] = jml_kasus  # semua pasien di bulan yg sama punya jml_kasus sama
    
    print("Memasukkan data kasus bulanan...")
    for bulan, jumlah in kasus_per_bulan.items():
        # Tentukan tingkat risiko
        if jumlah > 15:
            risiko = 'Tinggi'
        elif jumlah >= 9:
            risiko = 'Sedang'
        else:
            risiko = 'Rendah'
        
        kb = KasusBulanan(
            bulan=bulan,
            tahun=TAHUN,
            jumlah_kasus=jumlah,
            jumlah_sembuh=jumlah,
            jumlah_meninggal=0,
            tingkat_risiko=risiko
        )
        db.session.add(kb)
    
    db.session.commit()
    print(f"  -> {KasusBulanan.query.count()} data kasus bulanan berhasil ditambahkan")

    # --- 5. Ringkasan ---
    print("\n=== RINGKASAN SEED ===")
    print(f"Total Pasien     : {PasienDBD.query.count()}")
    print(f"Total Kasus/Bulan: {KasusBulanan.query.count()}")
    print("\nDetail per bulan:")
    for kb in KasusBulanan.query.order_by(KasusBulanan.id).all():
        jumlah_pasien_bulan = PasienDBD.query.filter_by(bulan=kb.bulan, tahun=kb.tahun).count()
        print(f"  {kb.bulan:12s} | {kb.jumlah_kasus:3d} kasus | {jumlah_pasien_bulan} pasien | Risiko: {kb.tingkat_risiko}")
    
    print("\nSelesai!")
