"""
Flask Application Factory
"""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Configuration
    app.config['SECRET_KEY'] = 'dbd-prediction-secret-key-2025'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Database: MySQL only (XAMPP)
    db_url = os.environ.get('DATABASE_URL', '')
    if not db_url:
        try:
            import pymysql
            conn = pymysql.connect(host='localhost', user='root', password='')
            conn.close()
            db_url = 'mysql+pymysql://root:@localhost/db_prediksi_dbd'
        except Exception:
            raise RuntimeError(
                'MySQL tidak ditemukan! '
                'Pastikan XAMPP MySQL sudah berjalan (start MySQL di XAMPP Control Panel). '
                'Import database: mysql -u root < db_prediksi_dbd.sql'
            )

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url

    if 'mysql' in db_url:
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_recycle': 300,
            'pool_pre_ping': True
        }
    else:
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Silakan login untuk mengakses halaman ini.'
    login_manager.login_message_category = 'warning'
    
    # User loader for Flask-Login
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    
    # Register blueprints
    from app.routes import main_bp
    from app.routes.auth import auth_bp
    from app.routes.data import data_bp
    from app.routes.users import users_bp
    from app.routes.training import training_bp
    from app.routes.prediksi import prediksi_bp
    from app.routes.evaluasi import evaluasi_bp
    from app.routes.perhitungan import perhitungan_bp
    from app.routes.api import api_bp
    from app.routes.laporan import laporan_bp
    from app.routes.log import log_bp
    from app.routes.data_uji import data_uji_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(data_bp, url_prefix='/data')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(training_bp, url_prefix='/training')
    app.register_blueprint(prediksi_bp, url_prefix='/prediksi')
    app.register_blueprint(evaluasi_bp, url_prefix='/evaluasi')
    app.register_blueprint(perhitungan_bp, url_prefix='/perhitungan')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(laporan_bp, url_prefix='/laporan')
    app.register_blueprint(log_bp, url_prefix='/log')
    app.register_blueprint(data_uji_bp, url_prefix='/data_uji')
    # Error handlers
    @app.errorhandler(403)
    def forbidden(e):
        from flask import render_template
        return render_template('403.html'), 403
    
    # Create database tables + auto-seed if empty
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f'[DB] Error creating tables: {e}')

        from app.models import User, PasienDBD, KasusBulanan
        if User.query.count() == 0:
            _seed_initial_data(app)

    return app


def _seed_initial_data(app):
    """Auto-seed users + import patients from Excel on first run (MySQL)."""
    import os
    from app.models import User, PasienDBD, KasusBulanan
    from werkzeug.security import generate_password_hash
    from collections import defaultdict
    from datetime import date

    # Seed users
    for uname, pw, role, nama in [
        ('admin', 'admin123', 'admin', 'Administrator'),
        ('petugas', 'petugas123', 'petugas', 'Petugas Kesehatan')
    ]:
        db.session.add(User(
            username=uname, password=generate_password_hash(pw),
            nama_lengkap=nama, role=role, status='aktif'))
    db.session.commit()

    # Try to import patients from Excel
    try:
        import pandas as pd
        from app.ml_model import get_risk_level

        excel_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Data DBD 15 Sampel.xlsx')
        if not os.path.exists(excel_path):
            excel_path = os.path.join(os.path.dirname(__file__), '..', 'Data DBD 15 Sampel.xlsx')
        if not os.path.exists(excel_path):
            print('[SEED] Excel not found, skipping patient import')
            return

        df = pd.read_excel(excel_path, sheet_name='Data_DBD')

        BULAN_KASUS = {
            'Januari': 12, 'Februari': 7, 'Maret': 14, 'April': 4,
            'Mei': 13, 'Juni': 15, 'Juli': 10, 'Agustus': 13,
            'September': 18, 'Oktober': 33, 'November': 21, 'Desember': 3
        }
        BULAN_ORDER = list(BULAN_KASUS.keys())
        reverse_map = defaultdict(list)
        for b, k in BULAN_KASUS.items():
            reverse_map[k].append(b)

        patients_by_kasus = defaultdict(list)
        for _, row in df.iterrows():
            patients_by_kasus[int(row['Jumlah Kasus Perbulan'])].append({
                'nama': str(row['Nama']).strip(),
                'usia': int(row['Usia']),
                'lama_rawat': int(row['Lama Rawat Inap']),
                'jk': 'L' if int(row['Jenis Kelamin']) == 1 else 'P',
            })

        tahun = 2024
        day_counter = {}
        p_no = 0
        for kasus_val in sorted(patients_by_kasus.keys()):
            patients = patients_by_kasus[kasus_val]
            bulans = reverse_map[kasus_val]
            mid = len(patients) // 2 if len(bulans) > 1 else len(patients)
            for i, p in enumerate(patients):
                p_no += 1
                bulan = bulans[0] if i < mid or len(bulans) == 1 else bulans[1]
                month_num = BULAN_ORDER.index(bulan) + 1
                day_counter[bulan] = day_counter.get(bulan, 0) + 2
                day = min(day_counter[bulan], 28)
                db.session.add(PasienDBD(
                    no_rm=f'RM-{tahun}-{p_no:04d}', nama_pasien=p['nama'],
                    usia=p['usia'], jenis_kelamin=p['jk'], alamat='Kab. Agam',
                    tanggal_masuk=date(tahun, month_num, day),
                    lama_rawat=p['lama_rawat'], bulan=bulan, tahun=tahun))
        db.session.commit()

        for bulan, jumlah in BULAN_KASUS.items():
            db.session.add(KasusBulanan(
                bulan=bulan, tahun=tahun, jumlah_kasus=jumlah,
                jumlah_sembuh=0, jumlah_meninggal=0,
                tingkat_risiko=get_risk_level(jumlah)))
        db.session.commit()
        print(f'[SEED] {p_no} patients + {len(BULAN_KASUS)} kasus bulanan imported')
    except Exception as e:
        print(f'[SEED] Patient import skipped: {e}')
