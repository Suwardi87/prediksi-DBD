"""
Perhitungan Manual Routes
Halaman khusus yang menampilkan langkah-langkah perhitungan manual Random Forest
"""
from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from app.models import PasienDBD, KasusBulanan, ModelEvaluasi
from app.ml_model import (
    get_risk_level, prepare_training_data, load_model,
    calculate_entropy, LABEL_MAP, INVERSE_LABEL_MAP
)
from app import db
import math
import json

perhitungan_bp = Blueprint('perhitungan', __name__)


@perhitungan_bp.route('/')
@login_required
def index():
    """Halaman perhitungan manual RF"""
    return render_template('perhitungan/index.html')


@perhitungan_bp.route('/hitung', methods=['POST'])
@login_required
def hitung():
    """Jalankan perhitungan manual step-by-step dan kembalikan data lengkap"""
    try:
        import numpy as np
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import StratifiedKFold
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score as sklearn_r2_score

        # ═══════════════════════════════════════════════
        # LANGKAH 1: INPUT DATA
        # ═══════════════════════════════════════════════
        pasien_list = PasienDBD.query.all()
        kasus_records = KasusBulanan.query.all()

        kasus_bulanan_dict = {}
        for kb in kasus_records:
            kasus_bulanan_dict[(kb.bulan, kb.tahun)] = kb.jumlah_kasus

        if not kasus_bulanan_dict:
            from sqlalchemy import func
            counts = db.session.query(
                PasienDBD.bulan, PasienDBD.tahun, func.count(PasienDBD.id)
            ).group_by(PasienDBD.bulan, PasienDBD.tahun).all()
            for bulan, tahun, count in counts:
                kasus_bulanan_dict[(bulan, tahun)] = count

        df = prepare_training_data(pasien_list, kasus_bulanan_dict)

        feature_columns = ['usia', 'lama_rawat', 'jenis_kelamin']
        X = df[feature_columns].values
        y_labels = df['tingkat_risiko'].values
        y_encoded = np.array([LABEL_MAP.get(label, 2) for label in y_labels])

        # Data input tabel
        input_data = []
        for i in range(len(df)):
            input_data.append({
                'no': i + 1,
                'usia': int(X[i][0]),
                'lama_rawat': int(X[i][1]),
                'jenis_kelamin': 'L' if X[i][2] == 1 else 'P',
                'tingkat_risiko': y_labels[i],
                'label': int(y_encoded[i])
            })

        # ═══════════════════════════════════════════════
        # LANGKAH 2 & 3: RANDOM SAMPLING + PEMBUATAN POHON
        # ═══════════════════════════════════════════════
        n_estimators = 1
        random_state = 42

        from app.ml_model import create_manual_rf
        model = create_manual_rf()

        # Ambil detail per pohon (3 pohon pertama sebagai contoh detail)
        trees_summary = []
        for i, estimator in enumerate(model.estimators_):
            tree = estimator.tree_
            feature_names = ['Usia', 'Lama Rawat Inap', 'Jenis Kelamin']

            # Distribusi kelas di root
            root_counts = tree.value[0].flatten()
            total_samples = int(root_counts.sum())
            class_dist = {}
            for j, cls in enumerate(model.classes_):
                cls_name = INVERSE_LABEL_MAP.get(cls, f'Class {cls}')
                cnt = int(root_counts[j]) if j < len(root_counts) else 0
                class_dist[cls_name] = cnt

            # Entropy root
            root_entropy = calculate_entropy(root_counts)

            # Fitur split root
            root_feature_idx = tree.feature[0]
            root_threshold = tree.threshold[0]
            root_feature = (
                feature_names[root_feature_idx]
                if 0 <= root_feature_idx < len(feature_names)
                else 'Leaf'
            )

            # Information Gain root
            ig = 0.0
            left_ent = right_ent = 0.0
            left_cnt = right_cnt = 0
            if tree.children_left[0] >= 0 and tree.children_right[0] >= 0:
                left_counts = tree.value[tree.children_left[0]].flatten()
                right_counts = tree.value[tree.children_right[0]].flatten()
                left_ent = calculate_entropy(left_counts)
                right_ent = calculate_entropy(right_counts)
                left_cnt = int(left_counts.sum())
                right_cnt = int(right_counts.sum())
                lw = left_cnt / total_samples if total_samples > 0 else 0
                rw = right_cnt / total_samples if total_samples > 0 else 0
                ig = root_entropy - (lw * left_ent + rw * right_ent)

            trees_summary.append({
                'tree_id': i + 1,
                'total_samples': total_samples,
                'class_dist': class_dist,
                'root_entropy': round(root_entropy, 4),
                'root_feature': root_feature,
                'root_threshold': round(float(root_threshold), 2) if root_feature_idx >= 0 else None,
                'information_gain': round(ig, 4),
                'left_entropy': round(left_ent, 4),
                'right_entropy': round(right_ent, 4),
                'left_samples': left_cnt,
                'right_samples': right_cnt,
                'n_leaves': int(tree.n_leaves),
                'max_depth': int(tree.max_depth)
            })

        # ═══════════════════════════════════════════════
        # LANGKAH 5: EVALUASI (MAE, RMSE, R²)
        # ═══════════════════════════════════════════════
        n_folds = 5
        skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=random_state)

        folds_detail = []
        all_y_test = []
        all_y_pred = []

        for fold_idx, (train_idx, test_idx) in enumerate(skf.split(X, y_encoded)):
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y_encoded[train_idx], y_encoded[test_idx]

            fold_model = RandomForestClassifier(
                n_estimators=n_estimators,
                criterion='entropy',
                max_features='sqrt',
                bootstrap=True,
                random_state=random_state,
                n_jobs=1
            )
            fold_model.fit(X_train, y_train)
            y_pred = fold_model.predict(X_test)

            mae = float(mean_absolute_error(y_test, y_pred))
            mse = float(mean_squared_error(y_test, y_pred))
            rmse = float(math.sqrt(mse))
            r2 = float(sklearn_r2_score(y_test, y_pred)) if len(y_test) > 1 else 0.0

            # Detail data test per fold
            test_detail = []
            for j in range(len(y_test)):
                test_detail.append({
                    'idx': int(test_idx[j]) + 1,
                    'actual': int(y_test[j]),
                    'actual_label': INVERSE_LABEL_MAP.get(int(y_test[j]), '?'),
                    'predicted': int(y_pred[j]),
                    'predicted_label': INVERSE_LABEL_MAP.get(int(y_pred[j]), '?'),
                    'error': abs(int(y_test[j]) - int(y_pred[j]))
                })

            folds_detail.append({
                'fold': fold_idx + 1,
                'train_size': len(train_idx),
                'test_size': len(test_idx),
                'mae': round(mae, 4),
                'rmse': round(rmse, 4),
                'r2': round(r2, 4),
                'test_data': test_detail
            })

            all_y_test.extend(y_test.tolist())
            all_y_pred.extend(y_pred.tolist())

        all_y_test = np.array(all_y_test)
        all_y_pred = np.array(all_y_pred)

        # Rata-rata metrik
        avg_mae = round(float(np.mean([f['mae'] for f in folds_detail])), 4)
        avg_rmse = round(float(np.mean([f['rmse'] for f in folds_detail])), 4)
        avg_r2 = round(float(np.mean([f['r2'] for f in folds_detail])), 4)

        # Perhitungan manual keseluruhan
        errors = (all_y_test - all_y_pred).tolist()
        abs_errors = [abs(e) for e in errors]
        sq_errors = [e ** 2 for e in errors]

        manual_mae = round(sum(abs_errors) / len(abs_errors), 4)
        manual_mse = sum(sq_errors) / len(sq_errors)
        manual_rmse = round(math.sqrt(manual_mse), 4)

        y_mean = float(np.mean(all_y_test))
        ss_res = sum(sq_errors)
        ss_tot = sum((yt - y_mean) ** 2 for yt in all_y_test.tolist())
        manual_r2 = round(1 - (ss_res / ss_tot) if ss_tot != 0 else 0.0, 4)

        eval_detail = {
            'n_data': len(all_y_test),
            'y_mean': round(y_mean, 4),
            'sum_abs_errors': round(sum(abs_errors), 4),
            'sum_sq_errors': round(ss_res, 4),
            'ss_tot': round(ss_tot, 4),
            'manual_mae': manual_mae,
            'manual_rmse': manual_rmse,
            'manual_r2': manual_r2,
            'avg_mae': avg_mae,
            'avg_rmse': avg_rmse,
            'avg_r2': avg_r2
        }

        return jsonify({
            'status': 'success',
            'input_data': input_data,
            'total_data': len(input_data),
            'n_estimators': n_estimators,
            'n_features': len(feature_columns),
            'm_features': int(math.sqrt(len(feature_columns))),
            'trees': trees_summary,
            'folds': folds_detail,
            'evaluation': eval_detail
        })

    except Exception as e:
        import traceback
        return jsonify({
            'status': 'error',
            'message': str(e),
            'trace': traceback.format_exc()
        }), 500
