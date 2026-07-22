"""
Prediction Routes
Prediksi menggunakan 3 fitur: Usia, Lama Rawat Inap, Jenis Kelamin
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models import HasilPrediksi
from app import db
from app.ml_model import predict, BULAN_NAMES, get_risk_level
from datetime import datetime

prediksi_bp = Blueprint('prediksi', __name__)

@prediksi_bp.route('/')
@login_required
def index():
    """Halaman prediksi"""
    bulan_list = BULAN_NAMES[1:]  # Skip empty first element
    return render_template('prediksi/index.html', bulan_list=bulan_list)

@prediksi_bp.route('/predict', methods=['POST'])
@login_required
def make_prediction():
    """Buat prediksi — fitur: Usia, Lama Rawat, Jenis Kelamin"""
    try:
        data = request.get_json() or {}
        
        # Input utama model (3 fitur)
        usia = data.get('usia', 25)
        lama_rawat = data.get('lama_rawat', 3)
        jenis_kelamin = data.get('jenis_kelamin', 'L')
        
        # Data konteks (disimpan ke DB)
        bulan = data.get('bulan', datetime.now().month)
        
        # Make prediction — 3 fitur
        result = predict(
            usia=usia,
            lama_rawat=lama_rawat,
            jenis_kelamin=jenis_kelamin
        )
        
        # Resolve bulan to a name string
        bulan_nama = str(bulan)
        try:
            bulan_int = int(bulan)
            if 1 <= bulan_int <= 12:
                bulan_nama = BULAN_NAMES[bulan_int]
        except (ValueError, TypeError):
            # bulan is already a string like 'Januari'
            bulan_nama = str(bulan) if bulan else BULAN_NAMES[datetime.now().month]
        
        # Save to database
        prediksi = HasilPrediksi(
            tanggal_prediksi=datetime.now(),
            bulan_prediksi=bulan_nama,
            tahun_prediksi=datetime.now().year,
            jumlah_kasus_prediksi=None,
            tingkat_risiko_prediksi=result['prediction']['tingkat_risiko'],
            confidence_score=result['prediction']['confidence'],
            model_version='1.0.0',
            created_by=current_user.id
        )
        
        db.session.add(prediksi)
        db.session.commit()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@prediksi_bp.route('/history')
@login_required
def history():
    """Riwayat prediksi"""
    predictions = HasilPrediksi.query.order_by(HasilPrediksi.tanggal_prediksi.desc()).limit(50).all()
    return render_template('prediksi/history.html', predictions=predictions)

@prediksi_bp.route('/batch', methods=['GET', 'POST'])
@login_required
def batch_predict():
    """Jalankan prediksi untuk 10 data pasien terakhir untuk halaman Prediksi Risiko"""
    try:
        from app.models import PasienDBD
        from app.ml_model import predict_batch_with_trees
        
        # Ambil 10 data terakhir secara random atau id descending
        pasiens = PasienDBD.query.order_by(PasienDBD.id.desc()).limit(10).all()
        if not pasiens:
            return jsonify({'status': 'error', 'message': 'Data pasien kosong. Silakan import data terlebih dahulu.'})
            
        result = predict_batch_with_trees(pasiens)
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
