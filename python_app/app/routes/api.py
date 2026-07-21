"""
API Routes - for external access
"""
from flask import Blueprint, jsonify, request
from app.models import KasusBulanan, HasilPrediksi, ModelEvaluasi
from app.ml_model import predict, train_model, prepare_training_data
from app import db
from datetime import datetime
import json

api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def home():
    """API info"""
    return jsonify({
        'name': 'DBD Prediction API',
        'version': '1.0.0',
        'description': 'API untuk prediksi penyebaran DBD menggunakan Random Forest',
        'endpoints': {
            '/api/train': 'POST - Train model',
            '/api/predict': 'POST - Make prediction',
            '/api/evaluate': 'GET - Get model evaluation',
            '/api/data': 'GET - Get data statistics'
        }
    })

@api_bp.route('/train', methods=['POST'])
def api_train():
    """API endpoint untuk training"""
    try:
        data = request.get_json() or {}
        n_estimators = data.get('n_estimators', 100)
        random_state = data.get('random_state', 42)
        
        from app.models import PasienDBD
        pasien_list = PasienDBD.query.all()
        
        if not pasien_list:
            return jsonify({
                'status': 'error',
                'message': 'No training data available'
            }), 400
        
        kasus_records = KasusBulanan.query.all()
        kasus_bulanan_dict = {(kb.bulan, kb.tahun): kb.jumlah_kasus for kb in kasus_records}
        
        if not kasus_bulanan_dict:
            from sqlalchemy import func
            counts = db.session.query(
                PasienDBD.bulan, PasienDBD.tahun, func.count(PasienDBD.id)
            ).group_by(PasienDBD.bulan, PasienDBD.tahun).all()
            for bulan, tahun, count in counts:
                kasus_bulanan_dict[(bulan, tahun)] = count
        
        df = prepare_training_data(pasien_list, kasus_bulanan_dict)
        result = train_model(df, n_estimators=n_estimators, random_state=random_state)
        
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
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api_bp.route('/predict', methods=['POST'])
def api_predict():
    """API endpoint untuk prediksi"""
    try:
        data = request.get_json() or {}
        
        result = predict(
            usia=data.get('usia', 25),
            lama_rawat=data.get('lama_rawat', 3),
            jenis_kelamin=data.get('jenis_kelamin', 'L')
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api_bp.route('/evaluate')
def api_evaluate():
    """API endpoint untuk evaluasi"""
    latest = ModelEvaluasi.query.order_by(ModelEvaluasi.tanggal_training.desc()).first()
    
    if not latest:
        return jsonify({'status': 'error', 'message': 'No model evaluation found'}), 404
    
    return jsonify({
        'status': 'success',
        'evaluation': {
            'tanggal_training': latest.tanggal_training.isoformat() if latest.tanggal_training else None,
            'accuracy': float(latest.accuracy) if latest.accuracy else 0,
            'precision': float(latest.precision_score) if latest.precision_score else 0,
            'recall': float(latest.recall_score) if latest.recall_score else 0,
            'f1_score': float(latest.f1_score) if latest.f1_score else 0,
            'n_estimators': latest.n_estimators
        }
    })

@api_bp.route('/data')
def api_data():
    """API endpoint untuk statistik data"""
    kasus = KasusBulanan.query.all()
    
    total_kasus = sum(k.jumlah_kasus for k in kasus)
    
    return jsonify({
        'status': 'success',
        'statistics': {
            'total_records': len(kasus),
            'total_kasus': total_kasus,
            'data': [{
                'bulan': k.bulan,
                'tahun': k.tahun,
                'jumlah_kasus': k.jumlah_kasus,
                'tingkat_risiko': k.tingkat_risiko
            } for k in kasus]
        }
    })
