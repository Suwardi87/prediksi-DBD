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
    """Buat prediksi — fitur: Usia, Lama Rawat, Jenis Kelamin, (Jumlah Kasus)"""
    try:
        data = request.get_json() or {}
        
        # Input utama model
        usia = data.get('usia', 25)
        lama_rawat = data.get('lama_rawat', 3)
        jenis_kelamin = data.get('jenis_kelamin', 'L')
        jumlah_kasus = data.get('jumlah_kasus')
        
        # ── Validasi input ──
        try:
            usia = int(usia)
            if usia < 0 or usia > 120:
                return jsonify({'status': 'error', 'message': 'Usia harus antara 0-120 tahun'}), 400
        except (ValueError, TypeError):
            return jsonify({'status': 'error', 'message': 'Usia harus berupa angka'}), 400
        
        try:
            lama_rawat = int(lama_rawat)
            if lama_rawat < 1:
                return jsonify({'status': 'error', 'message': 'Lama rawat minimal 1 hari'}), 400
        except (ValueError, TypeError):
            return jsonify({'status': 'error', 'message': 'Lama rawat harus berupa angka'}), 400
        
        if jenis_kelamin not in ('L', 'P'):
            return jsonify({'status': 'error', 'message': 'Jenis kelamin harus L atau P'}), 400
        
        if jumlah_kasus is not None:
            try:
                jumlah_kasus = int(jumlah_kasus)
                if jumlah_kasus < 0:
                    return jsonify({'status': 'error', 'message': 'Jumlah kasus tidak boleh negatif'}), 400
            except (ValueError, TypeError):
                return jsonify({'status': 'error', 'message': 'Jumlah kasus harus berupa angka'}), 400
        
        # Data konteks (disimpan ke DB)
        bulan = data.get('bulan', datetime.now().month)
        
        # Make prediction
        result = predict(
            usia=usia,
            lama_rawat=lama_rawat,
            jenis_kelamin=jenis_kelamin,
            jumlah_kasus=jumlah_kasus
        )
        
        # Resolve bulan to a name string
        bulan_nama = str(bulan)
        try:
            bulan_int = int(bulan)
            if 1 <= bulan_int <= 12:
                bulan_nama = BULAN_NAMES[bulan_int - 1]
            else:
                bulan_nama = BULAN_NAMES[datetime.now().month - 1]
        except (ValueError, TypeError):
            bulan_nama = str(bulan) if bulan else BULAN_NAMES[datetime.now().month - 1]
        
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
    """Jalankan prediksi untuk sampel dari setiap bulan (variasi kasus)"""
    try:
        from app.models import PasienDBD, KasusBulanan
        from app.ml_model import predict_batch_with_trees
        
        # Ambil 1 pasien dari setiap bulan untuk mendapatkan variasi kasus
        all_months = KasusBulanan.query.order_by(KasusBulanan.tahun, KasusBulanan.bulan).all()
        pasiens = []
        seen = set()
        for kb in all_months:
            sample = PasienDBD.query.filter_by(bulan=kb.bulan, tahun=kb.tahun).first()
            if sample and sample.id not in seen:
                pasiens.append(sample)
                seen.add(sample.id)
            if len(pasiens) >= 10:
                break
        
        if len(pasiens) < 10:
            # Fallback: ambil 10 pertama
            pasiens = PasienDBD.query.order_by(PasienDBD.id.asc()).limit(10).all()
            
        if not pasiens:
            return jsonify({'status': 'error', 'message': 'Data pasien kosong.'}), 404
            
        result = predict_batch_with_trees(pasiens)
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
