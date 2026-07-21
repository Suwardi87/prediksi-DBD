"""
Evaluation Routes
"""
from flask import Blueprint, render_template
from flask_login import login_required
from app.models import ModelEvaluasi
import json

evaluasi_bp = Blueprint('evaluasi', __name__)

@evaluasi_bp.route('/')
@login_required
def index():
    """Halaman evaluasi model"""
    evaluations = ModelEvaluasi.query.order_by(ModelEvaluasi.tanggal_training.desc()).all()
    latest = evaluations[0] if evaluations else None
    
    # Parse JSON fields
    if latest:
        try:
            latest.confusion_matrix_data = json.loads(latest.confusion_matrix) if latest.confusion_matrix else []
            latest.feature_importance_data = json.loads(latest.feature_importance) if latest.feature_importance else {}
        except:
            latest.confusion_matrix_data = []
            latest.feature_importance_data = {}
    
    return render_template('evaluasi/index.html', evaluations=evaluations, latest=latest)
