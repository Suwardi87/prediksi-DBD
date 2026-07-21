from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import PasienDBD
from app.decorators import admin_or_petugas_required

data_uji_bp = Blueprint('data_uji', __name__)

@data_uji_bp.route('/')
@login_required
@admin_or_petugas_required
def index():
    """Menampilkan Data Uji (Testing Set)"""
    # Sebagai simulasi sederhana, kita ambil 20 data terakhir sebagai "Data Uji" 
    # di dunia nyata ini biasanya disisihkan saat split dataset
    page = request.args.get('page', 1, type=int)
    
    data_uji = PasienDBD.query.order_by(PasienDBD.id.desc()).paginate(
        page=page, per_page=15, error_out=False
    )
    
    return render_template('data_uji/index.html', data_uji=data_uji)
