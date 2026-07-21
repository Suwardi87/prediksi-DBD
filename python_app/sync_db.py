import sys
import pandas as pd
from datetime import datetime, date
import random

from app import create_app, db
from app.models import PasienDBD, KasusBulanan

app = create_app()

def sync_data():
    excel_path = r"c:\xampp\htdocs\PrediksiPenyebaranPenyakitMenularDemamBerdarahDongue\Data DBD 15 Sampel.xlsx"
    
    with app.app_context():
        # Hapus data pasien dan kasus bulanan yang ada
        print("Menghapus data lama...")
        PasienDBD.query.delete()
        KasusBulanan.query.delete()
        db.session.commit()
        
        # Baca Data_DBD
        print("Membaca sheet Data_DBD...")
        df = pd.read_excel(excel_path, sheet_name='Data_DBD')
        
        # Hapus baris kosong
        df = df.dropna(subset=['Nama', 'Tingkat Resiko'])
        print(f"Total data dari Excel: {len(df)}")
        
        # Buat pemetaan Jumlah Kasus Perbulan ke Bulan/Tahun agar konsisten
        unique_kasus = df['Jumlah Kasus Perbulan'].unique()
        bulan_list = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 
                      'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
        tahun = 2024
        
        kasus_to_month = {}
        for i, val in enumerate(unique_kasus):
            bln = bulan_list[i % 12]
            thn = tahun - (i // 12)
            kasus_to_month[val] = (bln, thn)
            
            # Buat entry KasusBulanan
            kb = KasusBulanan(
                bulan=bln,
                tahun=thn,
                jumlah_kasus=int(val),
                jumlah_sembuh=int(val * 0.8), # dummy
                jumlah_meninggal=0,
                tingkat_risiko='Sedang' # dummy
            )
            db.session.add(kb)
            
        # Import data pasien
        for index, row in df.iterrows():
            nama = str(row['Nama'])
            usia = int(row['Usia'])
            lama_rawat = int(row['Lama Rawat Inap'])
            jk = 'L' if row['Jenis Kelamin'] == 1 else 'P'
            tingkat_resiko = str(row['Tingkat Resiko'])
            kasus_val = row['Jumlah Kasus Perbulan']
            
            bln, thn = kasus_to_month[kasus_val]
            
            # Buat tanggal dummy sesuai bulan/tahun
            # (Hanya butuh bulan/tahun yang cocok dengan kasus bulanan)
            month_idx = bulan_list.index(bln) + 1
            tgl_masuk = date(thn, month_idx, random.randint(1, 28))
            
            pasien = PasienDBD(
                no_rm=f"RM-{str(index+1).zfill(4)}",
                nama_pasien=nama,
                usia=usia,
                jenis_kelamin=jk,
                tanggal_masuk=tgl_masuk,
                lama_rawat=lama_rawat,
                bulan=bln,
                tahun=thn,
                alamat='Batam'
            )
            db.session.add(pasien)
            
        db.session.commit()
        print("Sinkronisasi 163 data berhasil!")

if __name__ == '__main__':
    sync_data()
