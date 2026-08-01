"""
Evaluation Routes
Confusion Matrix, Accuracy, Precision, Recall, F1-Score sesuai BAB IV.
Semua nilai dibaca dari Excel (tanpa hardcode).
"""
from flask import Blueprint, render_template
from flask_login import login_required
from app.models import ModelEvaluasi
import json
import openpyxl

evaluasi_bp = Blueprint('evaluasi', __name__)

_ENC = {'Rendah': 1, 'Sedang': 2, 'Tinggi': 3}


def _compute_bab4_metrics():
    """
    Hitung Confusion Matrix, Accuracy, Precision, Recall, F1-Score
    dari Excel: Data Uji (actuals) + Pohon 11 rules (predictions).
    """
    from app.routes.perhitungan import (
        EXCEL_PATH, POHON_NAMES,
        _read_test_actuals, _read_pohon_thresholds,
        _read_bootstrap_from_sheet, _read_penentuan_pohon_terbaik,
        _majority_class,
    )

    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)

    penentuan = _read_penentuan_pohon_terbaik(wb)
    if penentuan:
        best_entry = min(penentuan, key=lambda x: x.get('mae') or 999999)
        best_idx = best_entry.get('no', 11) - 1
    else:
        best_idx = 10

    t1, t2 = _read_pohon_thresholds(wb, POHON_NAMES[best_idx])
    bs = _read_bootstrap_from_sheet(wb, POHON_NAMES[best_idx])
    left = [s for s in bs if float(s.get('jumlah_kasus', 0)) < t1]
    mid = [s for s in bs if t1 <= float(s.get('jumlah_kasus', 0)) <= t2]
    right = [s for s in bs if float(s.get('jumlah_kasus', 0)) > t2]
    left_cls = _majority_class(left)[0] if left else 'Sedang'
    mid_cls = _majority_class(mid)[0] if mid else 'Tinggi'
    right_cls = _majority_class(right)[0] if right else 'Tinggi'

    test_data = _read_test_actuals(wb)
    actuals = [t['risk_enc'] for t in test_data]
    predictions = []
    for t in test_data:
        jk = t['jumlah_kasus']
        if jk < t1:
            predictions.append(_ENC.get(left_cls, 2))
        elif jk <= t2:
            predictions.append(_ENC.get(mid_cls, 3))
        else:
            predictions.append(_ENC.get(right_cls, 3))

    n = len(actuals)
    cm = [[0]*3 for _ in range(3)]
    for a, p in zip(actuals, predictions):
        cm[a-1][p-1] += 1

    correct = sum(cm[c][c] for c in range(3))
    accuracy = correct / n

    tp = correct
    fp = n - correct
    fn = n - correct

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        'confusion_matrix': cm,
        'tp': tp, 'fp': fp, 'fn': fn,
        'accuracy': round(accuracy, 4),
        'precision': round(precision, 4),
        'recall': round(recall, 4),
        'f1_score': round(f1, 4),
    }


@evaluasi_bp.route('/')
@login_required
def index():
    """Halaman evaluasi model"""
    bab4_metrics = _compute_bab4_metrics()
    evaluations = ModelEvaluasi.query.order_by(ModelEvaluasi.tanggal_training.desc()).all()
    latest = evaluations[0] if evaluations else None

    if latest:
        try:
            latest.confusion_matrix_data = json.loads(latest.confusion_matrix) if latest.confusion_matrix else bab4_metrics['confusion_matrix']
            latest.feature_importance_data = json.loads(latest.feature_importance) if latest.feature_importance else {}
        except Exception:
            latest.confusion_matrix_data = bab4_metrics['confusion_matrix']
            latest.feature_importance_data = {}

        latest.mae = bab4_metrics['accuracy']
        latest.rmse = bab4_metrics['precision']
        latest.r2_score = bab4_metrics['f1_score']

    return render_template('evaluasi/index.html', evaluations=evaluations, latest=latest, bab4_metrics=bab4_metrics)
