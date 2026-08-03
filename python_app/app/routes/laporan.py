"""
Report Routes
"""
from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import KasusBulanan, HasilPrediksi, PasienDBD
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
    default_tahun = tahun_list[0] if tahun_list else 2025
    tahun = request.args.get('tahun', default_tahun, type=int)
    
    # Jumlah kasus dari baris data pasien di database (bukan nilai kolom Excel)
    from app.ml_model import get_risk_level
    agg = db.session.query(
        PasienDBD.bulan,
        func.count(PasienDBD.id).label('total')
    ).filter_by(tahun=tahun).group_by(PasienDBD.bulan).all()
    jumlah_per_bulan = {bulan: total for bulan, total in agg}
    # Pastikan semua 12 bulan tercakup (bulan tanpa data = 0)
    BULAN_NAMES = list(BULAN_ORDER.keys())
    for b in BULAN_NAMES:
        jumlah_per_bulan.setdefault(b, 0)
    risiko_per_bulan = {b: get_risk_level(jumlah_per_bulan[b]) for b in BULAN_NAMES}
    
    prediksi = HasilPrediksi.query.filter_by(tahun_prediksi=tahun).all()
    
    return render_template('laporan/index.html', 
                          bulan_labels=BULAN_NAMES,
                          jumlah_per_bulan=jumlah_per_bulan,
                          risiko_per_bulan=risiko_per_bulan,
                          prediksi=prediksi,
                          tahun=tahun,
                          tahun_list=tahun_list)
