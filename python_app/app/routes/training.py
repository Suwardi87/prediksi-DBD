"""
Training Routes
Data training dari PasienDBD, 5 pohon keputusan, fitur: Usia, Lama Rawat, JK
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models import PasienDBD, KasusBulanan, ModelEvaluasi
from app import db
from app.ml_model import prepare_training_data, train_model, get_risk_level
from app.decorators import admin_or_petugas_required
from datetime import datetime
import json

training_bp = Blueprint('training', __name__)

@training_bp.route('/')
@login_required
@admin_or_petugas_required
def index():
    """Halaman training model"""
    last_training = ModelEvaluasi.query.order_by(ModelEvaluasi.tanggal_training.desc()).first()
    jumlah_pasien = PasienDBD.query.count()
    jumlah_kasus_bulanan = KasusBulanan.query.count()
    return render_template('training/index.html', 
                          last_training=last_training,
                          jumlah_pasien=jumlah_pasien,
                          jumlah_kasus_bulanan=jumlah_kasus_bulanan)

@training_bp.route('/start', methods=['POST'])
@login_required
@admin_or_petugas_required
def start_training():
    """Mulai training model"""
    try:
        # Get parameters from request — default 5 pohon
        data = request.get_json() or {}
        n_estimators = data.get('n_estimators', 5)
        
        # Random state: tetap 42 agar hasil konsisten & reproducible
        random_state = data.get('random_state', 42)
        
        # ── Data dari PasienDBD ──
        pasien_list = PasienDBD.query.all()
        
        if not pasien_list:
            return jsonify({
                'status': 'error',
                'message': 'Tidak ada data pasien untuk training. Silakan tambahkan data pasien terlebih dahulu.'
            }), 400
        
        # Bangun lookup jumlah kasus bulanan untuk menentukan tingkat risiko
        kasus_bulanan_dict = {}
        
        # Coba dari tabel KasusBulanan dulu
        kasus_records = KasusBulanan.query.all()
        for kb in kasus_records:
            kasus_bulanan_dict[(kb.bulan, kb.tahun)] = kb.jumlah_kasus
        
        # Jika tidak ada data KasusBulanan, hitung dari PasienDBD
        if not kasus_bulanan_dict:
            from sqlalchemy import func
            counts = db.session.query(
                PasienDBD.bulan, 
                PasienDBD.tahun, 
                func.count(PasienDBD.id)
            ).group_by(PasienDBD.bulan, PasienDBD.tahun).all()
            for bulan, tahun, count in counts:
                kasus_bulanan_dict[(bulan, tahun)] = count
        
        # Prepare and train — fitur: Usia, Lama Rawat, Jenis Kelamin
        df = prepare_training_data(pasien_list, kasus_bulanan_dict)
        result = train_model(
            df,
            n_estimators=n_estimators,
            random_state=random_state
        )
        
        # Save evaluation to database — termasuk MAE, RMSE, R²
        evaluation = ModelEvaluasi(
            tanggal_training=datetime.now(),
            accuracy=result['metrics']['accuracy'],
            precision_score=result['metrics']['precision_weighted'],
            recall_score=result['metrics']['recall_weighted'],
            f1_score=result['metrics']['f1_score_weighted'],
            mae=result['metrics']['mae'],
            rmse=result['metrics']['rmse'],
            r2_score=result['metrics']['r2_score'],
            n_estimators=n_estimators,
            confusion_matrix=json.dumps(result['confusion_matrix']),
            feature_importance=json.dumps(result['feature_importance']),
            model_path='models/random_forest_model.pkl'
        )
        
        db.session.add(evaluation)
        db.session.commit()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
