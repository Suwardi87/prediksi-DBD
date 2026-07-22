"""
Perhitungan Manual Routes — Sesuai Bab IV
163 data, 4 fitur (X1=Usia, X2=LamaRawat, X3=JK, X4=JumlahKasus)
15 pohon, setiap pohon HANYA 1 fitur untuk split.
Encoding: Rendah=1, Sedang=2, Tinggi=3
Grouping: Kasus 1-10=Rendah, 11-20=Sedang, >20=Tinggi
Pohon 5 = pohon terbaik (Gain tertinggi). Evaluasi pada 10 data uji.
"""
import os
import math
import numpy as np
from flask import Blueprint, render_template, jsonify
from flask_login import login_required

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

N_TEST = 10

BAB4_GAIN = {
    1: 0.59558818, 2: 0.034558397, 3: 0.066195604, 4: -0.001930068,
    5: 0.65403293, 6: 0.033807028, 7: 0.007208794, 8: 0.03702069,
    9: 0.6597991, 10: 0.023709616, 11: 0.004491452, 12: 0.001453179,
    13: 0.616055251, 14: 0.014241368, 15: 0.019288709,
}

BAB4_ENTROPY_AFTER = {
    1: 0.692344, 2: 1.30689651, 3: 1.23592389, 4: 1.28519682,
    5: 0.735984404, 6: 1.31736004, 7: 1.4063900, 8: 1.28442100,
    9: 0.74291800, 10: 1.22876400, 11: 1.38625852, 12: 1.37582041,
    13: 0.7746900, 14: 1.2506700, 15: 1.38342803,
}

BAB4_TEST_DATA = [
    {'jumlah_kasus': 12, 'risiko_aktual': 'Sedang'},
    {'jumlah_kasus': 12, 'risiko_aktual': 'Sedang'},
    {'jumlah_kasus': 7, 'risiko_aktual': 'Rendah'},
    {'jumlah_kasus': 7, 'risiko_aktual': 'Rendah'},
    {'jumlah_kasus': 18, 'risiko_aktual': 'Tinggi'},
    {'jumlah_kasus': 18, 'risiko_aktual': 'Tinggi'},
    {'jumlah_kasus': 18, 'risiko_aktual': 'Tinggi'},
    {'jumlah_kasus': 18, 'risiko_aktual': 'Tinggi'},
    {'jumlah_kasus': 21, 'risiko_aktual': 'Tinggi'},
    {'jumlah_kasus': 3, 'risiko_aktual': 'Rendah'},
]

BAB4_POHON5_THRESHOLDS = [12.60, 29.21]
BAB4_POHON5_RULES = [
    'IF Jumlah Kasus Perbulan < 12.60 THEN Risiko = Rendah',
    'IF Jumlah Kasus Perbulan >= 12.60 AND <= 29.21 THEN Risiko = Sedang',
    'IF Jumlah Kasus Perbulan > 29.21 THEN Risiko = Tinggi',
]


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


def _read_bootstrap_from_sheet(wb, pohon_name):
    ws = wb[pohon_name]
    headers = [ws.cell(row=1, column=c).value for c in range(1, ws.max_column + 1)]
    nos = [i for i, h in enumerate(headers) if h == 'No']
    rs = nos[1] if len(nos) >= 2 else None
    if rs is None:
        return []

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
    return samples


def _read_excel_entropy(wb, pohon_name):
    ws = wb[pohon_name]
    for r in range(1, min(ws.max_row + 1, 20)):
        for c in range(1, min(ws.max_column + 1, 25)):
            v = ws.cell(row=r, column=c).value
            if v and isinstance(v, str) and 'entropy root' in v.lower():
                return ws.cell(row=r, column=c + 1).value
    return None


def _read_pohon_features(wb, pohon_name):
    ws = wb[pohon_name]
    headers = [ws.cell(row=1, column=c).value for c in range(1, ws.max_column + 1)]
    nos = [i for i, h in enumerate(headers) if h == 'No']
    rs = nos[1] if len(nos) >= 2 else None
    if rs is None:
        return []
    features = []
    for i in range(rs, len(headers)):
        h = headers[i]
        if h and h in COL_MAP and COL_MAP[h] != 'tingkat_risiko':
            features.append(COL_MAP[h])
        elif h == 'Perhitungan root':
            break
    return features


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


def _calc_root_entropy(samples):
    counts = {'Rendah': 0, 'Sedang': 0, 'Tinggi': 0}
    for s in samples:
        r = s.get('tingkat_risiko', '')
        if r in counts:
            counts[r] += 1
    return _calc_entropy([counts['Rendah'], counts['Sedang'], counts['Tinggi']]), counts


def _find_best_split_single_feature(samples, feature_key):
    if not samples:
        return None, 0.0, None, None, None

    root_e, root_counts = _calc_root_entropy(samples)
    n = len(samples)

    values = sorted(set(float(s.get(feature_key, 0)) for s in samples))

    if len(values) <= 1:
        return None, 0.0, root_e, root_counts, None

    best_gain = -1
    best_threshold = None
    best_left = None
    best_right = None

    for i in range(len(values) - 1):
        threshold = (values[i] + values[i + 1]) / 2.0
        left = [s for s in samples if float(s.get(feature_key, 0)) <= threshold]
        right = [s for s in samples if float(s.get(feature_key, 0)) > threshold]
        if not left or not right:
            continue

        left_e, _ = _calc_root_entropy(left)
        right_e, _ = _calc_root_entropy(right)
        weighted_e = (len(left) / n) * left_e + (len(right) / n) * right_e
        gain = root_e - weighted_e

        if gain > best_gain:
            best_gain = gain
            best_threshold = threshold
            best_left = left
            best_right = right

    left_e = _calc_root_entropy(best_left)[0] if best_left else 0
    right_e = _calc_root_entropy(best_right)[0] if best_right else 0
    weighted_e_final = root_e - best_gain if best_gain > 0 else root_e

    return best_threshold, best_gain, root_e, root_counts, {
        'left_entropy': round(left_e, 6),
        'right_entropy': round(right_e, 6),
        'left_samples': len(best_left) if best_left else 0,
        'right_samples': len(best_right) if best_right else 0,
        'weighted_entropy': round(weighted_e_final, 6),
    }


FEATURE_NAMES = {
    'usia': 'Usia',
    'lama_rawat': 'Lama Rawat Inap',
    'jk': 'Jenis Kelamin',
    'jumlah_kasus': 'Jumlah Kasus Perbulan',
}

FEATURE_DISPLAY = {
    'usia': 'Usia (X1)',
    'lama_rawat': 'Lama Rawat Inap (X2)',
    'jk': 'Jenis Kelamin (X3)',
    'jumlah_kasus': 'Jumlah Kasus Perbulan (X4)',
}


def _majority_class(subset):
    counts = {'Rendah': 0, 'Sedang': 0, 'Tinggi': 0}
    for s in subset:
        r = s.get('tingkat_risiko', '')
        if r in counts:
            counts[r] += 1
    return max(counts, key=counts.get), counts


def _build_tree_rules_deep(samples, feature_key, depth=0, max_depth=3):
    if not samples or depth >= max_depth:
        return []

    root_e, root_counts = _calc_root_entropy(samples)
    n = len(samples)

    all_same = len([c for c in root_counts.values() if c > 0]) <= 1
    if all_same or n <= 5:
        cls, cls_counts = _majority_class(samples)
        return [{'type': 'leaf', 'class': cls, 'counts': cls_counts, 'n': n}]

    values = sorted(set(float(s.get(feature_key, 0)) for s in samples))
    if len(values) <= 1:
        cls, cls_counts = _majority_class(samples)
        return [{'type': 'leaf', 'class': cls, 'counts': cls_counts, 'n': n}]

    best_gain = -1
    best_threshold = None
    best_left = None
    best_right = None

    for i in range(len(values) - 1):
        threshold = (values[i] + values[i + 1]) / 2.0
        left = [s for s in samples if float(s.get(feature_key, 0)) <= threshold]
        right = [s for s in samples if float(s.get(feature_key, 0)) > threshold]
        if not left or not right:
            continue
        left_e, _ = _calc_root_entropy(left)
        right_e, _ = _calc_root_entropy(right)
        weighted_e = (len(left) / n) * left_e + (len(right) / n) * right_e
        gain = root_e - weighted_e
        if gain > best_gain:
            best_gain = gain
            best_threshold = threshold
            best_left = left
            best_right = right

    if best_threshold is None or best_gain <= 0:
        cls, cls_counts = _majority_class(samples)
        return [{'type': 'leaf', 'class': cls, 'counts': cls_counts, 'n': n}]

    fname = FEATURE_NAMES.get(feature_key, feature_key)
    left_rules = _build_tree_rules_deep(best_left, feature_key, depth + 1, max_depth)
    right_rules = _build_tree_rules_deep(best_right, feature_key, depth + 1, max_depth)

    left_majority, left_counts = _majority_class(best_left)
    right_majority, right_counts = _majority_class(best_right)

    result = [{
        'type': 'split',
        'feature': fname,
        'threshold': round(best_threshold, 2),
        'gain': round(best_gain, 4),
        'left_class': left_majority,
        'left_counts': left_counts,
        'left_n': len(best_left),
        'right_class': right_majority,
        'right_counts': right_counts,
        'right_n': len(best_right),
    }]
    result.extend(left_rules)
    result.extend(right_rules)
    return result


def _build_rules_text(samples, feature_key):
    if not samples:
        return []

    value_counts = {}
    for s in samples:
        v = float(s.get(feature_key, 0))
        if v not in value_counts:
            value_counts[v] = {'Rendah': 0, 'Sedang': 0, 'Tinggi': 0}
        r = s.get('tingkat_risiko', '')
        if r in value_counts[v]:
            value_counts[v][r] += 1

    sorted_vals = sorted(value_counts.keys())
    fname = FEATURE_NAMES.get(feature_key, feature_key)

    transitions = []
    for i in range(len(sorted_vals) - 1):
        v1 = sorted_vals[i]
        v2 = sorted_vals[i + 1]
        c1 = max(value_counts[v1], key=value_counts[v1].get)
        c2 = max(value_counts[v2], key=value_counts[v2].get)
        if c1 != c2:
            threshold = (v1 + v2) / 2.0
            transitions.append((threshold, c1, c2))

    rules = []
    if not transitions:
        cls, counts = _majority_class(samples)
        rules.append(f"IF {fname} ANY THEN Risiko = {cls} ({counts})")
    else:
        for i, (thr, left_cls, right_cls) in enumerate(transitions):
            left_n = sum(1 for s in samples if float(s.get(feature_key, 0)) <= thr)
            right_n = sum(1 for s in samples if float(s.get(feature_key, 0)) > thr)
            left_c = {k: 0 for k in ['Rendah', 'Sedang', 'Tinggi']}
            right_c = {k: 0 for k in ['Rendah', 'Sedang', 'Tinggi']}
            for s in samples:
                v = float(s.get(feature_key, 0))
                r = s.get('tingkat_risiko', '')
                if v <= thr and r in left_c:
                    left_c[r] += 1
                elif v > thr and r in right_c:
                    right_c[r] += 1
            rules.append(f"IF {fname} <= {thr:.2f} THEN Risiko = {left_cls} (n={left_n}, {left_c})")
            rules.append(f"IF {fname} > {thr:.2f} THEN Risiko = {right_cls} (n={right_n}, {right_c})")

    return rules


def _predict_with_thresholds(jumlah_kasus, thresholds):
    if jumlah_kasus < thresholds[0]:
        return 'Rendah'
    elif jumlah_kasus <= thresholds[1]:
        return 'Sedang'
    else:
        return 'Tinggi'


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

        for pohon_idx, pohon_name in enumerate(POHON_NAMES):
            pohon_num = pohon_idx + 1
            bootstrap_samples = _read_bootstrap_from_sheet(wb, pohon_name)
            if not bootstrap_samples:
                continue

            pohon_features = _read_pohon_features(wb, pohon_name)
            excel_entropy = _read_excel_entropy(wb, pohon_name)

            best_threshold = None
            best_gain = -1
            best_feature = None
            best_split_info = None
            best_root_counts = None

            for feat in pohon_features:
                threshold, gain, root_e, root_counts, split_info = _find_best_split_single_feature(
                    bootstrap_samples, feat
                )
                if gain > best_gain:
                    best_gain = gain
                    best_threshold = threshold
                    best_feature = feat
                    best_split_info = split_info
                    best_root_counts = root_counts

            root_entropy = best_split_info['weighted_entropy'] + best_gain if best_split_info else 0

            rules_text = _build_rules_text(bootstrap_samples, best_feature)
            rules_deep = _build_tree_rules_deep(bootstrap_samples, best_feature)

            unique_hashes = set()
            for s in bootstrap_samples:
                unique_hashes.add(str(sorted(s.items())))
            n_unique = len(unique_hashes)

            bab4_gain = BAB4_GAIN.get(pohon_num, 0)
            bab4_entropy_after = BAB4_ENTROPY_AFTER.get(pohon_num, 0)

            pohon_results.append({
                'name': pohon_name,
                'id': pohon_num,
                'target_feature': best_feature,
                'target_label': FEATURE_NAMES.get(best_feature, best_feature),
                'target_display': FEATURE_DISPLAY.get(best_feature, best_feature),
                'n_samples': len(bootstrap_samples),
                'n_unique': n_unique,
                'n_duplicates': len(bootstrap_samples) - n_unique,
                'features_available': pohon_features,
                'best_feature': best_feature,
                'root_threshold': round(best_threshold, 2) if best_threshold else None,
                'gain': round(best_gain, 6),
                'gain_bab4': round(bab4_gain, 6),
                'root_entropy': round(root_entropy, 6),
                'root_counts': {'Tinggi': best_root_counts.get('Tinggi', 0),
                                'Sedang': best_root_counts.get('Sedang', 0),
                                'Rendah': best_root_counts.get('Rendah', 0)} if best_root_counts else {},
                'left_entropy': best_split_info.get('left_entropy', 0) if best_split_info else 0,
                'right_entropy': best_split_info.get('right_entropy', 0) if best_split_info else 0,
                'left_samples': best_split_info.get('left_samples', 0) if best_split_info else 0,
                'right_samples': best_split_info.get('right_samples', 0) if best_split_info else 0,
                'weighted_entropy': best_split_info.get('weighted_entropy', 0) if best_split_info else 0,
                'rules_text': rules_text,
                'rules_deep': rules_deep,
                'excel_entropy': round(excel_entropy, 6) if excel_entropy else None,
            })

        best_tree_idx = 4
        best_tree = pohon_results[best_tree_idx] if best_tree_idx < len(pohon_results) else None

        bab4_test_results = []
        for i, td in enumerate(BAB4_TEST_DATA):
            jk = td['jumlah_kasus']
            actual = td['risiko_aktual']
            predicted = _predict_with_thresholds(jk, BAB4_POHON5_THRESHOLDS)
            bab4_test_results.append({
                'no': i + 1,
                'jumlah_kasus': jk,
                'actual': actual,
                'actual_enc': LABEL_ENCODE.get(actual, 0),
                'predicted': predicted,
                'predicted_enc': LABEL_ENCODE.get(predicted, 0),
                'correct': actual == predicted,
            })

        bab4_correct = sum(1 for t in bab4_test_results if t['correct'])
        bab4_accuracy = round(bab4_correct / N_TEST, 4)

        bab4_actual_enc = [t['actual_enc'] for t in bab4_test_results]
        bab4_pred_enc = [t['predicted_enc'] for t in bab4_test_results]
        bab4_actual = np.array(bab4_actual_enc, dtype=float)
        bab4_pred = np.array(bab4_pred_enc, dtype=float)
        bab4_abs_err = np.abs(bab4_actual - bab4_pred)
        bab4_sq_err = (bab4_actual - bab4_pred) ** 2
        bab4_mae = round(float(np.mean(bab4_abs_err)), 4)
        bab4_rmse = round(float(math.sqrt(np.mean(bab4_sq_err))), 4)
        bab4_y_mean = float(np.mean(bab4_actual))
        bab4_ss_res = float(np.sum(bab4_sq_err))
        bab4_ss_tot = float(np.sum((bab4_actual - bab4_y_mean) ** 2))
        bab4_r2 = round(1 - bab4_ss_res / bab4_ss_tot, 4) if bab4_ss_tot > 0 else 0.0

        our_test_results = []
        if best_tree:
            for i in range(N_TEST):
                actual_risk = test_data[i].get('tingkat_risiko', '')
                jk_val = int(test_data[i].get('jumlah_kasus', 0))
                predicted_risk = _predict_with_thresholds(jk_val, BAB4_POHON5_THRESHOLDS)
                our_test_results.append({
                    'no': i + 1,
                    'jumlah_kasus': jk_val,
                    'actual': actual_risk,
                    'actual_enc': LABEL_ENCODE.get(actual_risk, 0),
                    'predicted': predicted_risk,
                    'predicted_enc': LABEL_ENCODE.get(predicted_risk, 0),
                    'correct': actual_risk == predicted_risk,
                })

        our_correct = sum(1 for t in our_test_results if t['correct'])
        our_accuracy = round(our_correct / N_TEST, 4)

        our_actual_enc = [t['actual_enc'] for t in our_test_results]
        our_pred_enc = [t['predicted_enc'] for t in our_test_results]
        our_actual = np.array(our_actual_enc, dtype=float)
        our_pred = np.array(our_pred_enc, dtype=float)
        our_abs_err = np.abs(our_actual - our_pred)
        our_sq_err = (our_actual - our_pred) ** 2
        our_mae = round(float(np.mean(our_abs_err)), 4)
        our_rmse = round(float(math.sqrt(np.mean(our_sq_err))), 4)
        our_y_mean = float(np.mean(our_actual))
        our_ss_res = float(np.sum(our_sq_err))
        our_ss_tot = float(np.sum((our_actual - our_y_mean) ** 2))
        our_r2 = round(1 - our_ss_res / our_ss_tot, 4) if our_ss_tot > 0 else 0.0

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
                'n_trees': len(pohon_results),
                'note': 'Setiap pohon dilatih dengan 163 data bootstrap. Setiap pohon menggunakan HANYA 1 fitur untuk split.',
            },
            'step4': {
                'trees': pohon_results,
            },
            'step5': {
                'best_tree': best_tree,
                'bab4_rules': BAB4_POHON5_RULES,
                'bab4_thresholds': BAB4_POHON5_THRESHOLDS,
                'bab4_test_data': bab4_test_results,
                'bab4_correct': bab4_correct,
                'bab4_accuracy': bab4_accuracy,
                'bab4_mae': bab4_mae,
                'bab4_rmse': bab4_rmse,
                'bab4_r2': bab4_r2,
                'our_test_data': our_test_results,
                'our_correct': our_correct,
                'our_accuracy': our_accuracy,
                'our_mae': our_mae,
                'our_rmse': our_rmse,
                'our_r2': our_r2,
            },
            'step6': {
                'bab4_mae': bab4_mae,
                'bab4_rmse': bab4_rmse,
                'bab4_r2': bab4_r2,
                'bab4_accuracy': bab4_accuracy,
                'bab4_correct': bab4_correct,
                'our_mae': our_mae,
                'our_rmse': our_rmse,
                'our_r2': our_r2,
                'our_accuracy': our_accuracy,
                'our_correct': our_correct,
                'n_test': N_TEST,
            },
        })

    except Exception as e:
        import traceback
        return jsonify({
            'status': 'error',
            'message': str(e),
            'trace': traceback.format_exc(),
        }), 500
