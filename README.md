# Prediksi DBD

Sistem Prediksi Penyebaran Penyakit Demam Berdarah Dengue (DBD) menggunakan algoritma Random Forest.

## Deskripsi

Aplikasi web ini dibangun untuk RSUD Lubuk Basung, Kabupaten Agam. Sistem ini membantu memprediksi tingkat risiko penyebaran DBD berdasarkan data pasien menggunakan machine learning (Random Forest Classifier).

## Fitur

- **Dashboard** — Ringkasan statistik kasus DBD per bulan
- **Kelola Data Pasien** — CRUD data pasien DBD + import dari Excel
- **Training Model** — Latih model Random Forest dengan parameter yang dapat dikonfigurasi
- **Prediksi Risiko** — Prediksi tingkat risiko (Rendah/Sedang/Tinggi) berdasarkan usia, lama rawat, dan jenis kelamin
- **Evaluasi Model** — Metrik accuracy, precision, recall, F1-score, MAE, RMSE, R2
- **Laporan** — Laporan kasus DBD per bulan/wilayah
- **Multi-User** — Admin, Petugas, Pimpinan dengan hak akses berbeda

## Tech Stack

- **Backend:** Python Flask
- **Database:** MySQL/MariaDB
- **ML:** Scikit-learn (Random Forest)
- **Frontend:** HTML/CSS/JavaScript (Jinja2 templates)

## Instalasi

### Prasyarat

- Python 3.10+
- MySQL/MariaDB

### Setup

**Linux / macOS:**
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

**Windows:**
```powershell
git clone https://github.com/Suwardi87/prediksi-DBD.git
cd prediksi-DBD
python -m venv .venv
.venv\Scripts\activate
pip install -r python_app\requirements.txt
mysql -u root -e "CREATE DATABASE IF NOT EXISTS db_prediksi_dbd"
mysql -u root db_prediksi_dbd < db_prediksi_dbd.sql
cd python_app
python run.py
```

Buka browser: `http://127.0.0.1:5000` (otomatis terbuka)

### Login

| Username | Password |
|----------|----------|
| admin | admin123 |
| petugas | petugas123 |

## Struktur Project

```
prediksi-DBD/
├── db_prediksi_dbd.sql          # Database schema + data (163 pasien)
├── Data DBD 15 Sampel.xlsx      # Data Excel untuk training
├── requirements.txt (di python_app/)
├── Dokumen/                     # Dokumen & diagram UML
└── python_app/                  # Aplikasi Flask
    ├── run.py                   # Entry point
    ├── requirements.txt
    └── app/
        ├── __init__.py          # Flask app factory
        ├── models.py            # Database models
        ├── ml_model.py          # Random Forest logic
        ├── routes/              # Halaman-halaman web
        └── templates/           # HTML templates
```

## Database

7 tabel:
- `users` — Pengguna sistem
- `pasien_dbd` — Data pasien DBD
- `kasus_bulanan` — Agregat kasus per bulan
- `data_training` — Data training model
- `model_evaluasi` — Metrik evaluasi model
- `hasil_prediksi` — Hasil prediksi
- `log_aktivitas` — Log aktivitas pengguna

## Machine Learning

- **Algoritma:** Random Forest Classifier
- **Fitur:** Usia, Lama Rawat Inap, Jenis Kelamin
- **Target:** Tingkat Risiko DBD (Rendah ≤8, Sedang 9-15, Tinggi >15 kasus)
- **Evaluasi:** Stratified 5-Fold Cross-Validation

## Lisensi

Tidak ada lisensi khusus. Untuk keperluan akademik/pribadi.

## Penulis

Suwardi87
