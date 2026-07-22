"""
Perhitungan Manual Routes — Sesuai Bab IV
163 data, 4 fitur (X1=Usia, X2=LamaRawat, X3=JK, X4=JumlahKasus)
m=√4=2, 15 pohon, Encoding: Rendah=1, Sedang=2, Tinggi=3
Grouping: Kasus 1-10=Rendah, 11-20=Sedang, >20=Tinggi
Pohon 5 = pohon terbaik. Evaluasi pada 10 data uji.
"""
import os
import math
import numpy as np
from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from sklearn.tree import DecisionTreeClassifier, export_text

perhitungan_bp = Blueprint('perhitungan', __name__)

EXCEL_PATH = os.path.normpath(os.path.join(
    os.path.dirname(__file__), '..', '..', '..', 'Data DBD 15 Sampel.xlsx'
))

LABEL_ENCODE = {'Rendah': 1, 'Sedang': 2, 'Tinggi': 3}
LABEL_DECODE = {1: 'Rendah', 2: 'Sedang', 3: 'Tinggi'}

COL_MAP = {
    'Usia': 'usia',
    'Lama Rawat Inap': 'lama_rawat',
    'Jumlah Kasus Per Bulan': 'jumlah_kasus',
    'Jumlah Kasus Perbulan': 'jumlah_kasus',
    'Jenis Kelamin': 'jk',
    'Tingkat Resiko': 'tingkat_risiko',
    'Nama': 'nama',
}

POHON_NAMES = [
    'Pohon 1', 'Pohon 2', 'Pohon 3', 'Pohon 4', 'Pohon 5',
    'Pohon 6', 'Pohon 7(BP)', 'Pohon 8 (BP)', 'Pohon 9', 'Pohon 10',
    'Pohon 11', 'Pohon 12', 'Pohon 13', 'Pohon 14', 'Pohon 15',
]

POHON_TARGET = {
    1: 'jumlah_kasus', 5: 'jumlah_kasus', 9: 'jumlah_kasus', 13: 'jumlah_kasus',
    2: 'usia', 8: 'usia', 10: 'usia', 14: 'usia',
    3: 'lama_rawat', 6: 'lama_rawat', 11: 'lama_rawat', 15: 'lama_rawat',
    4: 'jk', 7: 'jk', 12: 'jk',
}

POHON_TARGET_LABEL = {
    'jumlah_kasus': 'Jumlah Kasus Perbulan',
    'usia': 'Usia',
    'lama_rawat': 'Lama Rawat Inap',
    'jk': 'Jenis Kelamin',
}

GROUPING_RULES = {
    'jumlah_kasus': [(1, 10, 'Rendah'), (11, 20, 'Sedang'), (21, 999, 'Tinggi')],
    'usia': [(0, 17, 'Anak-anak'), (18, 59, 'Dewasa'), (60, 150, 'Lansia')],
    'lama_rawat': [(1, 2, 'Singkat'), (3, 4, 'Sedang'), (5, 99, 'Lama')],
    'jk': [(0, 0, 'Perempuan'), (1, 1, 'Laki-laki')],
}

N_TEST = 10


def _read_data_dbd(wb):
    ws = wb['Data_DBD']
    headers = [ws.cell(row=1, column=c).value for c in range(1, ws.max_column + 1)]
    data = []
    for r in range(2, ws.max_row + 1):
        row = {}
        for c, h in enumerate(headers):
            if h in COL_MAP:
                row[COL_MAP[h]] = ws.cell(row=r, column=c + 1).value
        if row.get('tingkat_risiko') in LABEL_ENCODE:
            data.append(row)
    return data


def _find_right_table(ws):
    headers = [ws.cell(row=1, column=c).value for c in range(1, ws.max_column + 1)]
    nos = [i for i, h in enumerate(headers) if h == 'No']
    if len(nos) >= 2:
        return nos[1]
    for i, h in enumerate(headers):
        if i >= 7 and h == 'No':
            return i
    return None


def _read_pohon(wb, pohon_name):
    ws = wb[pohon_name]
    rs = _find_right_table(ws)
    if rs is None:
        return None

    headers = [ws.cell(row=1, column=c).value for c in range(1, ws.max_column + 1)]
    right_headers = []
    for i in range(rs, len(headers)):
        h = headers[i]
        if h and h in COL_MAP:
            right_headers.append((i, COL_MAP[h]))
        elif h == 'Perhitungan root':
            break

    samples = []
    for r in range(2, ws.max_row + 1):
        no_val = ws.cell(row=r, column=rs + 1).value
        if no_val is None or not isinstance(no_val, (int, float)):
            break
        sample = {}
        for col_idx, feat_name in right_headers:
            sample[feat_name] = ws.cell(row=r, column=col_idx + 1).value
        if 'tingkat_risiko' in sample and sample['tingkat_risiko'] in LABEL_ENCODE:
            samples.append(sample)
        if len(samples) >= 163:
            break

    entropy_root = None
    for r in range(1, min(ws.max_row + 1, 20)):
        for c in range(1, min(ws.max_column + 1, 25)):
            v = ws.cell(row=r, column=c).value
            if v and isinstance(v, str) and 'entropy root' in v.lower():
                entropy_root = ws.cell(row=r, column=c + 1).value
                break
        if entropy_root is not None:
            break

    features_used = [fn for _, fn in right_headers if fn != 'tingkat_risiko']

    return {
        'samples': samples,
        'entropy_root': entropy_root,
        'features_used': features_used,
        'n_samples': len(samples),
    }


def _calc_entropy(counts):
    total = sum(counts)
    if total == 0:
        return 0.0
    ent = 0.0
    for c in counts:
        if c > 0:
            p = c / total
            ent -= p * math.log2(p)
    return ent


def _classify_value(value, feature_key):
    rules = GROUPING_RULES.get(feature_key, [])
    for lo, hi, label in rules:
        if lo <= value <= hi:
            return label
    return rules[-1][2] if rules else 'Tidak Diketahui'


def _predict_risk_from_value(predicted_value, feature_key):
    label = _classify_value(predicted_value, feature_key)
    if feature_key == 'jumlah_kasus':
        return label
    return label


def _train_tree_regression(samples, features_used, target_feature):
    if not samples or not features_used:
        return None

    feature_cols = [f for f in features_used if f != target_feature]
    if not feature_cols:
        feature_cols = features_used[:]

    X = []
    y = []
    for s in samples:
        row = [float(s.get(f, 0)) for f in feature_cols]
        X.append(row)
        y.append(float(s.get(target_feature, 0)))

    X = np.array(X)
    y = np.array(y)

    n_features = len(feature_cols)
    m_features = max(1, int(math.sqrt(n_features)))

    clf = DecisionTreeClassifier(
        criterion='entropy',
        max_features=m_features,
        random_state=42
    )
    clf.fit(X, y)

    tree = clf.tree_
    feature_names = [f.replace('_', ' ').title() for f in feature_cols]

    root_counts = tree.value[0].flatten()
    total_w = float(tree.weighted_n_node_samples[0])
    root_counts_abs = (root_counts * total_w).astype(float)
    root_entropy = _calc_entropy(root_counts_abs.tolist())

    feat_idx = tree.feature[0]
    root_ig = 0.0
    root_feature = None
    root_threshold = None
    left_entropy = 0.0
    right_entropy = 0.0
    left_samples = 0
    right_samples = 0

    if feat_idx >= 0 and tree.children_left[0] >= 0 and tree.children_right[0] >= 0:
        root_feature = feature_names[feat_idx]
        root_threshold = round(float(tree.threshold[0]), 4)

        left_w = float(tree.weighted_n_node_samples[tree.children_left[0]])
        right_w = float(tree.weighted_n_node_samples[tree.children_right[0]])
        left_counts = (tree.value[tree.children_left[0]].flatten() * left_w).astype(float)
        right_counts = (tree.value[tree.children_right[0]].flatten() * right_w).astype(float)
        left_entropy = _calc_entropy(left_counts.tolist())
        right_entropy = _calc_entropy(right_counts.tolist())
        left_samples = int(round(left_counts.sum()))
        right_samples = int(round(right_counts.sum()))
        total_s = left_samples + right_samples
        if total_s > 0:
            root_ig = root_entropy - (left_samples / total_s * left_entropy + right_samples / total_s * right_entropy)

    rules_text = export_text(clf, feature_names=feature_names)

    n_leaves = int(tree.n_leaves)
    max_depth = int(tree.max_depth)

    predicted_values = []
    for s in samples:
        row = [float(s.get(f, 0)) for f in feature_cols]
        pred = clf.predict([row])[0]
        predicted_values.append(pred)

    actual_values = [float(s.get(target_feature, 0)) for s in samples]
    mae = float(np.mean(np.abs(np.array(actual_values) - np.array(predicted_values))))
    rmse = float(math.sqrt(np.mean((np.array(actual_values) - np.array(predicted_values)) ** 2)))
    y_mean = float(np.mean(actual_values))
    ss_res = float(np.sum((np.array(actual_values) - np.array(predicted_values)) ** 2))
    ss_tot = float(np.sum((np.array(actual_values) - y_mean) ** 2))
    r2 = round(1 - ss_res / ss_tot, 4) if ss_tot > 0 else 0.0

    return {
        'clf': clf,
        'feature_cols': feature_cols,
        'target_feature': target_feature,
        'feature_names': feature_names,
        'root_entropy': round(root_entropy, 4),
        'root_ig': round(root_ig, 4),
        'root_feature': root_feature,
        'root_threshold': root_threshold,
        'left_entropy': round(left_entropy, 4),
        'right_entropy': round(right_entropy, 4),
        'left_samples': left_samples,
        'right_samples': right_samples,
        'n_leaves': n_leaves,
        'max_depth': max_depth,
        'rules_text': rules_text,
        'n_samples': len(samples),
        'n_features': n_features,
        'm_features': m_features,
        'mae': round(mae, 4),
        'rmse': round(rmse, 4),
        'r2': round(r2, 4),
        'ss_res': round(ss_res, 4),
        'ss_tot': round(ss_tot, 4),
    }


def _predict_risk(clf, feature_cols, target_feature, data_point):
    row = [float(data_point.get(f, 0)) for f in feature_cols]
    predicted_value = clf.predict([row])[0]
    risk_label = _classify_value(predicted_value, target_feature)
    return risk_label, predicted_value


@perhitungan_bp.route('/')
@login_required
def index():
    return render_template('perhitungan/index.html')


@perhitungan_bp.route('/hitung', methods=['POST'])
@login_required
def hitung():
    try:
        import openpyxl
        wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)

        data_dbd = _read_data_dbd(wb)
        total = len(data_dbd)
        n_features_all = 4
        m_features = int(math.sqrt(n_features_all))

        label_counts = {'Rendah': 0, 'Sedang': 0, 'Tinggi': 0}
        for d in data_dbd:
            lr = d.get('tingkat_risiko')
            if lr in label_counts:
                label_counts[lr] += 1

        step1_data = []
        for i, d in enumerate(data_dbd):
            step1_data.append({
                'no': i + 1,
                'nama': d.get('nama', ''),
                'usia': int(d.get('usia', 0)),
                'lama_rawat': int(d.get('lama_rawat', 0)),
                'jk': int(d.get('jk', 0)),
                'jk_label': 'L' if d.get('jk') == 1 else 'P',
                'jumlah_kasus': int(d.get('jumlah_kasus', 0)),
                'tingkat_risiko': d.get('tingkat_risiko', ''),
                'tingkat_risiko_encoded': LABEL_ENCODE.get(d.get('tingkat_risiko'), 0),
            })

        test_data = data_dbd[:N_TEST]
        train_data = data_dbd[N_TEST:]

        pohon_results = []
        all_tree_risk_preds = []

        for pohon_idx, pohon_name in enumerate(POHON_NAMES):
            pohon_num = pohon_idx + 1
            pohon_data = _read_pohon(wb, pohon_name)
            if pohon_data is None or pohon_data['n_samples'] == 0:
                continue

            target_feature = POHON_TARGET.get(pohon_num, 'jumlah_kasus')
            target_label = POHON_TARGET_LABEL.get(target_feature, target_feature)

            tree_info = _train_tree_regression(
                pohon_data['samples'], pohon_data['features_used'], target_feature
            )
            if tree_info is None:
                continue

            risk_preds = []
            predicted_values = []
            for d in test_data:
                risk_label, pred_val = _predict_risk(
                    tree_info['clf'], tree_info['feature_cols'], target_feature, d
                )
                risk_preds.append(risk_label)
                predicted_values.append(pred_val)

            all_tree_risk_preds.append(risk_preds)

            actual_risk = [d.get('tingkat_risiko', '') for d in test_data]
            correct = sum(1 for a, p in zip(actual_risk, risk_preds) if a == p)

            rules_lines = [l.strip() for l in tree_info['rules_text'].split('\n') if l.strip()]

            bootstrap_unique = len(set(hash(str(s)) for s in pohon_data['samples']))

            pohon_results.append({
                'name': pohon_name,
                'id': pohon_num,
                'target_feature': target_feature,
                'target_label': target_label,
                'n_samples': pohon_data['n_samples'],
                'n_unique': bootstrap_unique,
                'n_duplicates': pohon_data['n_samples'] - bootstrap_unique,
                'features_used': tree_info['feature_cols'],
                'n_features': tree_info['n_features'],
                'm_features': tree_info['m_features'],
                'entropy_root_excel': round(pohon_data['entropy_root'], 4) if pohon_data['entropy_root'] else None,
                'entropy_root_calc': tree_info['root_entropy'],
                'best_feature': tree_info['root_feature'],
                'root_threshold': tree_info['root_threshold'],
                'ig': tree_info['root_ig'],
                'left_entropy': tree_info['left_entropy'],
                'right_entropy': tree_info['right_entropy'],
                'left_samples': tree_info['left_samples'],
                'right_samples': tree_info['right_samples'],
                'n_leaves': tree_info['n_leaves'],
                'max_depth': tree_info['max_depth'],
                'rules': rules_lines,
                'mae': tree_info['mae'],
                'rmse': tree_info['rmse'],
                'r2': tree_info['r2'],
                'ss_res': tree_info['ss_res'],
                'ss_tot': tree_info['ss_tot'],
                'test_correct': correct,
                'test_total': N_TEST,
                'predicted_values': [{'actual': float(test_data[i].get(target_feature, 0)),
                                     'predicted': predicted_values[i]}
                                    for i in range(N_TEST)],
            })

        best_tree_idx = 4
        best_tree = pohon_results[best_tree_idx] if best_tree_idx < len(pohon_results) else None

        test_results = []
        if best_tree:
            for i in range(N_TEST):
                actual_risk = test_data[i].get('tingkat_risiko', '')
                predicted_risk = all_tree_risk_preds[best_tree_idx][i]
                test_results.append({
                    'no': i + 1,
                    'actual': actual_risk,
                    'actual_enc': LABEL_ENCODE.get(actual_risk, 0),
                    'predicted': predicted_risk,
                    'predicted_enc': LABEL_ENCODE.get(predicted_risk, 0),
                    'correct': actual_risk == predicted_risk,
                })

        correct_count = sum(1 for t in test_results if t['correct'])
        accuracy = round(correct_count / N_TEST, 4) if N_TEST > 0 else 0

        actual_enc = [t['actual_enc'] for t in test_results]
        pred_enc = [t['predicted_enc'] for t in test_results]
        actual_arr = np.array(actual_enc, dtype=float)
        pred_arr = np.array(pred_enc, dtype=float)

        abs_err = np.abs(actual_arr - pred_arr)
        sq_err = (actual_arr - pred_arr) ** 2
        mae_final = round(float(np.mean(abs_err)), 4)
        rmse_final = round(float(math.sqrt(np.mean(sq_err))), 4)
        y_mean = float(np.mean(actual_arr))
        ss_res_final = float(np.sum(sq_err))
        ss_tot_final = float(np.sum((actual_arr - y_mean) ** 2))
        r2_final = round(1 - ss_res_final / ss_tot_final, 4) if ss_tot_final > 0 else 0.0

        per_tree_test_eval = []
        for t_idx, preds in enumerate(all_tree_risk_preds):
            p = preds[:N_TEST]
            pe_enc = [LABEL_ENCODE.get(pr, 0) for pr in p]
            ae = [LABEL_ENCODE.get(test_data[i].get('tingkat_risiko', ''), 0) for i in range(N_TEST)]
            pe_arr = np.array(pe_enc, dtype=float)
            ae_arr = np.array(ae, dtype=float)
            pe_mae = round(float(np.mean(np.abs(ae_arr - pe_arr))), 4)
            pe_rmse = round(float(math.sqrt(np.mean((ae_arr - pe_arr) ** 2))), 4)
            pe_y_mean = float(np.mean(ae_arr))
            pe_ss_res = float(np.sum((ae_arr - pe_arr) ** 2))
            pe_ss_tot = float(np.sum((ae_arr - pe_y_mean) ** 2))
            pe_r2 = round(1 - pe_ss_res / pe_ss_tot, 4) if pe_ss_tot > 0 else 0.0
            pe_correct = sum(1 for a, pr in zip(ae, pe_enc) if a == pr)
            per_tree_test_eval.append({
                'name': pohon_results[t_idx]['name'] if t_idx < len(pohon_results) else f'Pohon {t_idx+1}',
                'mae': pe_mae, 'rmse': pe_rmse, 'r2': pe_r2,
                'correct': pe_correct, 'total': N_TEST,
            })

        return jsonify({
            'status': 'success',
            'step1': {
                'data': step1_data,
                'total': total,
                'n_train': len(train_data),
                'n_test': N_TEST,
                'features': ['Usia (X1)', 'Lama Rawat Inap (X2)', 'Jenis Kelamin (X3)', 'Jumlah Kasus Perbulan (X4)'],
                'label_counts': label_counts,
                'encoding': {'Rendah': 1, 'Sedang': 2, 'Tinggi': 3},
            },
            'step2': {
                'encoding_table': [
                    {'fitur': 'Jenis Kelamin (X3)', 'nilai_asli': 'Laki-laki (L) / Perempuan (P)', 'nilai_encoding': '1 / 0'},
                    {'fitur': 'Tingkat Resiko (Target)', 'nilai_asli': 'Rendah / Sedang / Tinggi', 'nilai_encoding': '1 / 2 / 3'},
                ],
                'grouping_table': [
                    {'fitur': 'Jumlah Kasus', 'rentang': '1 – 10', 'risiko': 'Rendah', 'label': 1},
                    {'fitur': 'Jumlah Kasus', 'rentang': '11 – 20', 'risiko': 'Sedang', 'label': 2},
                    {'fitur': 'Jumlah Kasus', 'rentang': '> 20', 'risiko': 'Tinggi', 'label': 3},
                ],
            },
            'step3': {
                'n': total,
                'm': m_features,
                'n_trees': len(pohon_results),
                'criterion': 'Entropy',
                'n_features_total': n_features_all,
            },
            'step4': {
                'trees': pohon_results,
                'best_tree_name': best_tree['name'] if best_tree else None,
                'best_tree_id': best_tree['id'] if best_tree else None,
            },
            'step5': {
                'best_tree': best_tree,
                'test_data': [{
                    'no': t['no'],
                    'actual': t['actual'],
                    'predicted': t['predicted'],
                    'correct': t['correct'],
                } for t in test_results],
                'accuracy': accuracy,
                'correct_count': correct_count,
                'total_test': N_TEST,
            },
            'step6': {
                'mae': mae_final,
                'rmse': rmse_final,
                'r2': r2_final,
                'ss_res': round(ss_res_final, 4),
                'ss_tot': round(ss_tot_final, 4),
                'y_mean': round(y_mean, 4),
                'n_test': N_TEST,
                'per_tree_eval': per_tree_test_eval,
            },
        })

    except Exception as e:
        import traceback
        return jsonify({
            'status': 'error',
            'message': str(e),
            'trace': traceback.format_exc(),
        }), 500
