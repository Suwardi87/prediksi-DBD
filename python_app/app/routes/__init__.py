"""
Main Routes - Dashboard
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import KasusBulanan, ModelEvaluasi, HasilPrediksi, PasienDBD
from app import db
from sqlalchemy import func

main_bp = Blueprint('main', __name__)

BULAN_NAMES = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
               'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']

@main_bp.route('/')
@login_required
def index():
    """Dashboard utama"""
    latest = KasusBulanan.query.order_by(KasusBulanan.tahun.desc()).first()
    tahun = latest.tahun if latest else 2025
    
    # Hitung jumlah kasus dari baris data pasien di database (bukan nilai kolom Excel)
    from app.ml_model import get_risk_level
    agg = db.session.query(
        PasienDBD.bulan,
        func.count(PasienDBD.id).label('total')
    ).filter_by(tahun=tahun).group_by(PasienDBD.bulan).all()
    jumlah_per_bulan = {bulan: total for bulan, total in agg}
    # Pastikan semua 12 bulan tercakup (bulan tanpa data = 0)
    for b in BULAN_NAMES:
        jumlah_per_bulan.setdefault(b, 0)
    risiko_per_bulan = {b: get_risk_level(jumlah_per_bulan[b]) for b in BULAN_NAMES}
    
    # Calculate statistics
    total_kasus = sum(jumlah_per_bulan.values())
    
    # Distribusi risiko dari 12 bulan (dari jumlah pasien asli per bulan di database)
    distribusi_risiko = {'Tinggi': 0, 'Sedang': 0, 'Rendah': 0}
    bulan_tertinggi = ''
    kasus_tertinggi = 0
    
    for b in BULAN_NAMES:
        jumlah = jumlah_per_bulan[b]
        risiko = risiko_per_bulan[b]
        distribusi_risiko[risiko] += 1
        if jumlah > kasus_tertinggi:
            kasus_tertinggi = jumlah
            bulan_tertinggi = b
    
    # Get model info
    model_info = ModelEvaluasi.query.order_by(ModelEvaluasi.tanggal_training.desc()).first()
    
    return render_template('dashboard.html',
        bulan_labels=BULAN_NAMES,
        jumlah_per_bulan=jumlah_per_bulan,
        risiko_per_bulan=risiko_per_bulan,
        kasus_data=[jumlah_per_bulan[b] for b in BULAN_NAMES],
        risiko_data=[risiko_per_bulan[b] for b in BULAN_NAMES],
        total_kasus=total_kasus,
        distribusi_risiko=distribusi_risiko,
        bulan_tertinggi=bulan_tertinggi,
        kasus_tertinggi=kasus_tertinggi,
        model_info=model_info,
        tahun=tahun
    )
