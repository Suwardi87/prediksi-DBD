"""
Evaluation Routes
Confusion Matrix, Accuracy, Precision, Recall, F1-Score sesuai BAB IV Revisi.
Best tree: Pohon 6 (R² tertinggi). Binary evaluation: Positive=Sedang.
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
    Hitung Confusion Matrix (binary: Sedang=Positive), Accuracy, Precision, Recall, F1.
    Best tree dari PenentuanPohonterbaik (R² tertinggi).
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
        best_entry = max(penentuan, key=lambda x: x.get('r2') or -999999)
        best_idx = best_entry.get('no', 6) - 1
        best_name = best_entry.get('name', f'Sampel {best_idx + 1}')
    else:
        best_idx = 5
        best_name = 'Sampel 6'

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

    cm_3x3 = [[0]*3 for _ in range(3)]
    for a, p in zip(actuals, predictions):
        cm_3x3[a-1][p-1] += 1

    POSITIVE = 2
    tp = sum(1 for a, p in zip(actuals, predictions) if a == POSITIVE and p == POSITIVE)
    fp = sum(1 for a, p in zip(actuals, predictions) if a != POSITIVE and p == POSITIVE)
    tn = sum(1 for a, p in zip(actuals, predictions) if a != POSITIVE and p != POSITIVE)
    fn = sum(1 for a, p in zip(actuals, predictions) if a == POSITIVE and p != POSITIVE)

    cm_binary = {
        'Rendah': {'positif': 0, 'negatif': 0},
        'Sedang': {'positif': 0, 'negatif': 0},
        'Tinggi': {'positif': 0, 'negatif': 0},
    }
    labels = {1: 'Rendah', 2: 'Sedang', 3: 'Tinggi'}
    for a, p in zip(actuals, predictions):
        lbl = labels[a]
        if p == POSITIVE:
            cm_binary[lbl]['positif'] += 1
        else:
            cm_binary[lbl]['negatif'] += 1

    accuracy = (tp + tn) / n if n > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return {
        'confusion_matrix': cm_3x3,
        'cm_binary': cm_binary,
        'tp': tp, 'fp': fp, 'tn': tn, 'fn': fn,
        'accuracy': round(accuracy, 4),
        'precision': round(precision, 4),
        'recall': round(recall, 4),
        'f1_score': round(f1, 4),
        'best_tree_name': best_name,
        'best_tree_idx': best_idx + 1,
        'thresholds': [round(t1, 2) if t1 else 0, round(t2, 2) if t2 else 0],
        'actuals': actuals,
        'predictions': predictions,
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
