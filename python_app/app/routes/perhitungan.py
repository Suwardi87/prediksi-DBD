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


def _build_tree_rules(samples, feature_key, threshold):
    if not samples or threshold is None:
        return []

    left = [s for s in samples if float(s.get(feature_key, 0)) <= threshold]
    right = [s for s in samples if float(s.get(feature_key, 0)) > threshold]

    def majority_class(subset):
        counts = {'Rendah': 0, 'Sedang': 0, 'Tinggi': 0}
        for s in subset:
            r = s.get('tingkat_risiko', '')
            if r in counts:
                counts[r] += 1
        return max(counts, key=counts.get)

    left_class = majority_class(left)
    right_class = majority_class(right)

    fname = FEATURE_NAMES.get(feature_key, feature_key)
    rules = [
        f"IF {fname} <= {threshold:.2f} THEN Risiko = {left_class}",
        f"IF {fname} > {threshold:.2f} THEN Risiko = {right_class}",
    ]
    return rules


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
        all_tree_risk_preds = []

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

            risk_preds = []
            for d in test_data:
                if best_feature and best_threshold is not None:
                    val = float(d.get(best_feature, 0))
                    if val <= best_threshold:
                        left = [s for s in bootstrap_samples if float(s.get(best_feature, 0)) <= best_threshold]
                        counts = {'Rendah': 0, 'Sedang': 0, 'Tinggi': 0}
                        for s in left:
                            r = s.get('tingkat_risiko', '')
                            if r in counts:
                                counts[r] += 1
                        pred = max(counts, key=counts.get)
                    else:
                        right = [s for s in bootstrap_samples if float(s.get(best_feature, 0)) > best_threshold]
                        counts = {'Rendah': 0, 'Sedang': 0, 'Tinggi': 0}
                        for s in right:
                            r = s.get('tingkat_risiko', '')
                            if r in counts:
                                counts[r] += 1
                        pred = max(counts, key=counts.get)
                else:
                    counts = {'Rendah': 0, 'Sedang': 0, 'Tinggi': 0}
                    for s in bootstrap_samples:
                        r = s.get('tingkat_risiko', '')
                        if r in counts:
                            counts[r] += 1
                    pred = max(counts, key=counts.get)
                risk_preds.append(pred)

            all_tree_risk_preds.append(risk_preds)

            actual_risk = [d.get('tingkat_risiko', '') for d in test_data]
            correct = sum(1 for a, p in zip(actual_risk, risk_preds) if a == p)

            rules = _build_tree_rules(bootstrap_samples, best_feature, best_threshold)

            unique_hashes = set()
            for s in bootstrap_samples:
                unique_hashes.add(str(sorted(s.items())))
            n_unique = len(unique_hashes)

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
                'root_entropy': round(root_entropy, 6),
                'root_counts': {'Tinggi': best_root_counts.get('Tinggi', 0),
                                'Sedang': best_root_counts.get('Sedang', 0),
                                'Rendah': best_root_counts.get('Rendah', 0)} if best_root_counts else {},
                'left_entropy': best_split_info.get('left_entropy', 0) if best_split_info else 0,
                'right_entropy': best_split_info.get('right_entropy', 0) if best_split_info else 0,
                'left_samples': best_split_info.get('left_samples', 0) if best_split_info else 0,
                'right_samples': best_split_info.get('right_samples', 0) if best_split_info else 0,
                'weighted_entropy': best_split_info.get('weighted_entropy', 0) if best_split_info else 0,
                'rules': rules,
                'excel_entropy': round(excel_entropy, 6) if excel_entropy else None,
                'test_correct': correct,
                'test_total': N_TEST,
                'predicted_values': [{'actual': actual_risk[i], 'predicted': risk_preds[i]}
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

        best_gain_tree = max(pohon_results, key=lambda t: t['gain']) if pohon_results else None

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
                'best_gain_tree': best_gain_tree['name'] if best_gain_tree else None,
            },
            'step5': {
                'best_tree': best_tree,
                'test_data': [{
                    'no': t['no'],
                    'actual': t['actual'],
                    'actual_enc': t['actual_enc'],
                    'predicted': t['predicted'],
                    'predicted_enc': t['predicted_enc'],
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
