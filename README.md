# Prediksi DBD

Sistem Prediksi Penyebaran Penyakit Demam Berdarah Dengue (DBD) menggunakan algoritma Random Forest.

## Deskripsi

Aplikasi web ini dibangun untuk RSUD Lubuk Basung, Kabupaten Agam. Sistem ini membantu memprediksi tingkat risiko penyebaran DBD berdasarkan data pasien menggunakan machine learning (Random Forest Classifier).

## Fitur

- **Dashboard** — Ringkasan statistik kasus DBD per bulan
- **Kelola Data Pasien** — CRUD data pasien DBD + import dari Excel
- **Training Model** — Latih model Random Forest dengan parameter yang dapat dikonfigurasi
- **Prediksi Risiko** — Prediksi tingkat risiko (Rendah/Sedang/Tinggi) berdasarkan usia, lama rawat, dan jenis kelamin
- **Perhitungan Manual** — Walkthrough 6 langkah Random Forest: Data Latih → Encoding → Bootstrap → Pohon Keputusan → Pohon Terbaik → Evaluasi. Menampilkan Gain, Entropy, threshold, dan aturan if-then untuk 15 pohon keputusan
- **Evaluasi Model** — Metrik accuracy, precision, recall, F1-score, MAE, RMSE, R2
- **Laporan** — Laporan kasus DBD per bulan/wilayah
- **Multi-User** — Admin, Petugas, Pimpinan dengan hak akses berbeda

## Tech Stack

- **Backend:** Python Flask
- **Database:** MySQL/MariaDB (XAMPP)
- **ML:** Scikit-learn (Random Forest)
- **Frontend:** HTML/CSS/JavaScript (Jinja2 templates)

---

## Instalasi (XAMPP — Windows)

### 1. Install XAMPP

Download & install XAMPP dari https://www.apachefriends.org. Pastikan **MySQL** sudah running di XAMPP Control Panel.

### 2. Import Database

Buka **phpMyAdmin** (http://localhost/phpmyadmin), lalu:

1. Klik tab **Import**
2. Pilih file `db_prediksi_dbd.sql` dari folder project
3. Klik **Go** / **Import**

Database `db_prediksi_dbd` akan terbuat otomatis beserta semua data (163 pasien, 12 kasus bulanan, 2 user).

> **Catatan:** Jangan membuat database manual. Cukup import file `.sql` saja.
>
> **Auto-seed:** Jika database kosong (tanpa import SQL), aplikasi akan otomatis membuat user + import 163 pasien dari file Excel saat pertama dijalankan.

### 3. Jalankan Aplikasi

Buka **Command Prompt / PowerShell**, lalu:

```powershell
cd prediksi-DBD
python -m venv .venv
.venv\Scripts\activate
pip install -r python_app\requirements.txt
cd python_app
python run.py
```

Buka browser: **http://127.0.0.1:5000**

### Login

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Administrator |
| petugas | petugas123 | Petugas Kesehatan |

---

## Instalasi (Linux / macOS)

```bash
git clone https://github.com/Suwardi87/prediksi-DBD.git
cd prediksi-DBD
python3 -m venv .venv
source .venv/bin/activate
pip install -r python_app/requirements.txt
mysql -u root -e "CREATE DATABASE IF NOT EXISTS db_prediksi_dbd"
mysql -u root db_prediksi_dbd < db_prediksi_dbd.sql
cd python_app
python run.py
```

Buka browser: `http://127.0.0.1:5000`

---

## Instalasi (Google Colab)

Buka notebook `Colab_Prediksi_DBD.ipynb` di Google Colab, jalankan semua cell dari atas ke bawah.

> Colab otomatis pakai SQLite (tidak perlu XAMPP). Aplikasi auto-seed 163 pasien dari Excel.

---

## Troubleshooting

### "MySQL tidak ditemukan"
- Buka **XAMPP Control Panel** → klik **Start** di bagian MySQL
- Import `db_prediksi_dbd.sql` ke phpMyAdmin

### "Access denied for user 'root'"
- XAMPP default: user `root`, password kosong (`''`)
- Kalau ada password, edit `python_app/app/__init__.py` baris 29

### "Table doesn't exist"
- Database belum di-import. Ikuti langkah **Import Database** di atas

### Import SQL di phpMyAdmin gagal (file terlalu besar)
- Buka Command Prompt, jalankan:
  ```
  mysql -u root < db_prediksi_dbd.sql
  ```

---

## Struktur Project

```
prediksi-DBD/
├── db_prediksi_dbd.sql          # Database MySQL (schema + 163 pasien + 12 kasus bulanan + 2 user)
├── Data DBD 15 Sampel.xlsx      # Data Excel: 163 pasien + 15 sheet bootstrap pohon
├── Colab_Prediksi_DBD.ipynb     # Notebook Google Colab (SQLite, auto-seed)
├── Dokumen/                     # Dokumen & diagram UML
└── python_app/                  # Aplikasi Flask
    ├── run.py                   # Entry point
    ├── requirements.txt
    └── app/
        ├── __init__.py          # Flask app factory + auto-seed dari Excel
        ├── models.py            # Database models (7 tabel)
        ├── ml_model.py          # Random Forest logic + get_risk_level()
        ├── routes/
        │   ├── perhitungan.py   # Halaman Perhitungan Manual (15 pohon, Gain, Entropy)
        │   ├── prediksi.py      # Halaman Prediksi (single + batch)
        │   ├── training.py      # Halaman Training Model
        │   ├── evaluasi.py      # Halaman Evaluasi
        │   ├── data.py          # CRUD Data Pasien
        │   ├── auth.py          # Login/Logout
        │   └── ...              # Dashboard, Laporan, Log, Users, API
        └── templates/           # HTML templates (Jinja2)
```

## Database

7 tabel:
- `users` — Pengguna sistem (2 user: admin, petugas)
- `pasien_dbd` — Data pasien DBD (163 pasien)
- `kasus_bulanan` — Agregat kasus per bulan (12 bulan)
- `data_training` — Data training model
- `model_evaluasi` — Metrik evaluasi model
- `hasil_prediksi` — Hasil prediksi
- `log_aktivitas` — Log aktivitas pengguna

## Machine Learning

- **Algoritma:** Random Forest Classifier
- **Data:** 163 pasien DBD dari Kab. Agam (2024)
- **Fitur input:** X1=Usia, X2=Lama Rawat Inop, X3=Jenis Kelamin, X4=Jumlah Kasus Perbulan
- **Target:** Tingkat Risiko DBD
  - **Rendah** — ≤ 8 kasus per bulan
  - **Sedang** — 9–15 kasus per bulan
  - **Tinggi** — > 15 kasus per bulan
- **Model RF:** 15 pohon keputusan, setiap pohon menggunakan 1 fitur dengan 3-way split (2 threshold)
- **Pohon terbaik:** Pohon 5 (Jumlah Kasus Perbulan, Gain=0.654)
- **Evaluasi:** MAE, RMSE, R², Accuracy

## Halaman Perhitungan Manual

Halaman ini menampilkan proses perhitungan Random Forest secara step-by-step:

1. **Data Latih** — 163 data pasien + distribusi label
2. **Encoding** — Konversi kategori ke numerik + pengelompokan risiko
3. **Bootstrap** — 15 bootstrap sample (163 data per pohon, sampling with replacement)
4. **Pohon Keputusan** — Tabel hasil perhitungan (Gain, Entropy, Root Entropy) + detail perhitungan step-by-step per pohon (Entropy Root → 3 Split → Information Gain → Aturan if-then)
5. **Pohon Terbaik** — Pohon 5 dengan Gain tertinggi, lengkap dengan perhitungan entropy & gain
6. **Evaluasi** — Hasil prediksi 10 data uji + Confusion Matrix + MAE/RMSE/R²

Threshold dan feature setiap pohon diekstrak dari rules Bab IV (halaman 29-34 PDF).

## Lisensi

Tidak ada lisensi khusus. Untuk keperluan akademik/pribadi.

## Penulis

Suwardi87
