"""
Main Routes - Dashboard
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import KasusBulanan, ModelEvaluasi, HasilPrediksi
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    """Dashboard utama"""
    latest = KasusBulanan.query.order_by(KasusBulanan.tahun.desc()).first()
    tahun = latest.tahun if latest else 2025
    
    # Get kasus bulanan
    kasus_bulanan = KasusBulanan.query.filter_by(tahun=tahun).order_by(
        db.case(
            (KasusBulanan.bulan == 'Januari', 1),
            (KasusBulanan.bulan == 'Februari', 2),
            (KasusBulanan.bulan == 'Maret', 3),
            (KasusBulanan.bulan == 'April', 4),
            (KasusBulanan.bulan == 'Mei', 5),
            (KasusBulanan.bulan == 'Juni', 6),
            (KasusBulanan.bulan == 'Juli', 7),
            (KasusBulanan.bulan == 'Agustus', 8),
            (KasusBulanan.bulan == 'September', 9),
            (KasusBulanan.bulan == 'Oktober', 10),
            (KasusBulanan.bulan == 'November', 11),
            (KasusBulanan.bulan == 'Desember', 12),
        )
    ).all()
    
    # Calculate statistics
    total_kasus = sum(k.jumlah_kasus for k in kasus_bulanan)
    
    # Distribusi risiko
    distribusi_risiko = {'Tinggi': 0, 'Sedang': 0, 'Rendah': 0}
    bulan_tertinggi = ''
    kasus_tertinggi = 0
    
    for k in kasus_bulanan:
        if k.tingkat_risiko in distribusi_risiko:
            distribusi_risiko[k.tingkat_risiko] += 1
        if k.jumlah_kasus > kasus_tertinggi:
            kasus_tertinggi = k.jumlah_kasus
            bulan_tertinggi = k.bulan
    
    # Get model info
    model_info = ModelEvaluasi.query.order_by(ModelEvaluasi.tanggal_training.desc()).first()
    
    return render_template('dashboard.html',
        kasus_bulanan=kasus_bulanan,
        total_kasus=total_kasus,
        distribusi_risiko=distribusi_risiko,
        bulan_tertinggi=bulan_tertinggi,
        kasus_tertinggi=kasus_tertinggi,
        model_info=model_info,
        tahun=tahun
    )
