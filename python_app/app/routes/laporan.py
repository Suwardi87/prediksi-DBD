"""
Report Routes
"""
from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import KasusBulanan, HasilPrediksi
from app import db
from sqlalchemy import func

laporan_bp = Blueprint('laporan', __name__)

# Urutan bulan untuk sorting
BULAN_ORDER = {
    'Januari': 1, 'Februari': 2, 'Maret': 3, 'April': 4,
    'Mei': 5, 'Juni': 6, 'Juli': 7, 'Agustus': 8,
    'September': 9, 'Oktober': 10, 'November': 11, 'Desember': 12
}

@laporan_bp.route('/')
@login_required
def index():
    """Halaman laporan"""
    # Ambil daftar tahun yang tersedia di data
    tahun_list = db.session.query(KasusBulanan.tahun).distinct().order_by(KasusBulanan.tahun.desc()).all()
    tahun_list = [t[0] for t in tahun_list]
    
    # Default tahun = tahun terbaru yang ada di data
    default_tahun = tahun_list[0] if tahun_list else 2024
    tahun = request.args.get('tahun', default_tahun, type=int)
    
    kasus_bulanan = KasusBulanan.query.filter_by(tahun=tahun).all()
    # Urutkan per bulan
    kasus_bulanan.sort(key=lambda k: BULAN_ORDER.get(k.bulan, 0))
    
    prediksi = HasilPrediksi.query.filter_by(tahun_prediksi=tahun).all()
    
    return render_template('laporan/index.html', 
                          kasus_bulanan=kasus_bulanan,
                          prediksi=prediksi,
                          tahun=tahun,
                          tahun_list=tahun_list)
