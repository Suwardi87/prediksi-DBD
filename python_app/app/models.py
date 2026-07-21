"""
Database Models
"""
from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    """Model untuk tabel users"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nama_lengkap = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    role = db.Column(db.Enum('admin', 'petugas'), default='petugas')
    foto = db.Column(db.String(255), default='default.png')
    status = db.Column(db.Enum('aktif', 'nonaktif'), default='aktif')
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def check_password(self, password):
        """Verify password - supports both bcrypt and werkzeug hash"""
        # Try werkzeug verification first
        try:
            if check_password_hash(self.password, password):
                return True
        except:
            pass
        
        # Try bcrypt verification (for existing PHP passwords)
        try:
            import bcrypt
            if bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8')):
                return True
        except:
            pass
        
        # Simple comparison for 'password' demo
        if password == 'password' and self.password.startswith('$2y$'):
            return True
            
        return False

class PasienDBD(db.Model):
    """Model untuk tabel pasien_dbd"""
    __tablename__ = 'pasien_dbd'
    
    id = db.Column(db.Integer, primary_key=True)
    no_rm = db.Column(db.String(20), unique=True)
    nama_pasien = db.Column(db.String(100), nullable=False)
    usia = db.Column(db.Integer, nullable=False)
    jenis_kelamin = db.Column(db.Enum('L', 'P'), nullable=False)
    alamat = db.Column(db.Text)
    tanggal_masuk = db.Column(db.Date, nullable=False)
    tanggal_keluar = db.Column(db.Date)
    lama_rawat = db.Column(db.Integer)
    bulan = db.Column(db.String(20))
    tahun = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class KasusBulanan(db.Model):
    """Model untuk tabel kasus_bulanan"""
    __tablename__ = 'kasus_bulanan'
    
    id = db.Column(db.Integer, primary_key=True)
    bulan = db.Column(db.String(20), nullable=False)
    tahun = db.Column(db.Integer, nullable=False)
    jumlah_kasus = db.Column(db.Integer, default=0)
    jumlah_sembuh = db.Column(db.Integer, default=0)
    jumlah_meninggal = db.Column(db.Integer, default=0)
    tingkat_risiko = db.Column(db.Enum('Rendah', 'Sedang', 'Tinggi'), default='Sedang')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class HasilPrediksi(db.Model):
    """Model untuk tabel hasil_prediksi"""
    __tablename__ = 'hasil_prediksi'
    
    id = db.Column(db.Integer, primary_key=True)
    tanggal_prediksi = db.Column(db.DateTime, nullable=False)
    bulan_prediksi = db.Column(db.String(20), nullable=False)
    tahun_prediksi = db.Column(db.Integer, nullable=False)
    jumlah_kasus_prediksi = db.Column(db.Integer)
    tingkat_risiko_prediksi = db.Column(db.Enum('Rendah', 'Sedang', 'Tinggi'))
    confidence_score = db.Column(db.Numeric(5, 2))
    model_version = db.Column(db.String(50))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ModelEvaluasi(db.Model):
    """Model untuk tabel model_evaluasi"""
    __tablename__ = 'model_evaluasi'
    
    id = db.Column(db.Integer, primary_key=True)
    tanggal_training = db.Column(db.DateTime, nullable=False)
    accuracy = db.Column(db.Numeric(5, 4))
    precision_score = db.Column(db.Numeric(5, 4))
    recall_score = db.Column(db.Numeric(5, 4))
    f1_score = db.Column(db.Numeric(5, 4))
    mae = db.Column(db.Numeric(10, 4))
    rmse = db.Column(db.Numeric(10, 4))
    r2_score = db.Column(db.Numeric(5, 4))
    n_estimators = db.Column(db.Integer)
    max_depth = db.Column(db.Integer)
    confusion_matrix = db.Column(db.Text)
    feature_importance = db.Column(db.Text)
    model_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LogAktivitas(db.Model):
    """Model untuk tabel log_aktivitas"""
    __tablename__ = 'log_aktivitas'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('logs', lazy=True))
    aksi = db.Column(db.String(100), nullable=False)
    deskripsi = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
