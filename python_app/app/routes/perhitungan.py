"""
Perhitungan Manual Routes — Alur Langkah RF dari Excel
Sesuai Bab IV: 163 data, 4 fitur, m=√4=2, 15 pohon, Entropy
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

LABEL_ENCODE = {'Rendah': 0, 'Sedang': 1, 'Tinggi': 2}
LABEL_DECODE = {0: 'Rendah', 1: 'Sedang', 2: 'Tinggi'}

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
    class_dist = {'Rendah': 0, 'Sedang': 0, 'Tinggi': 0}
    for s in samples:
        cls = s.get('tingkat_risiko')
        if cls in class_dist:
            class_dist[cls] += 1

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
        'class_dist': class_dist,
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


def _train_tree(samples, features_used):
    if not samples or not features_used:
        return None

    X = []
    y = []
    for s in samples:
        row = []
        for f in features_used:
            row.append(float(s.get(f, 0)))
        X.append(row)
        y.append(LABEL_ENCODE.get(s.get('tingkat_risiko'), 1))

    X = np.array(X)
    y = np.array(y)

    n_features = len(features_used)
    m_features = max(1, int(math.sqrt(n_features)))

    clf = DecisionTreeClassifier(
        criterion='entropy',
        max_features=m_features,
        random_state=42
    )
    clf.fit(X, y)

    tree = clf.tree_
    feature_names = [f.replace('_', ' ').title() for f in features_used]

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

    return {
        'clf': clf,
        'features_used': features_used,
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
    }


def _predict_all(clf, features_used, data_dbd):
    preds = []
    for d in data_dbd:
        row = [float(d.get(f, 0)) for f in features_used]
        p = clf.predict([row])[0]
        preds.append(int(p))
    return preds


def _compute_eval(actual_encoded, pred_encoded):
    actual = np.array(actual_encoded, dtype=float)
    pred = np.array(pred_encoded, dtype=float)
    n = len(actual)
    if n == 0:
        return {'mae': 0, 'rmse': 0, 'r2': 0}
    abs_err = np.abs(actual - pred)
    sq_err = (actual - pred) ** 2
    mae = float(np.mean(abs_err))
    mse = float(np.mean(sq_err))
    rmse = float(math.sqrt(mse))
    y_mean = float(np.mean(actual))
    ss_res = float(np.sum(sq_err))
    ss_tot = float(np.sum((actual - y_mean) ** 2))
    r2 = round(1 - ss_res / ss_tot, 4) if ss_tot > 0 else 0.0
    return {
        'mae': round(mae, 4),
        'rmse': round(rmse, 4),
        'r2': round(r2, 4),
        'ss_res': round(ss_res, 4),
        'ss_tot': round(ss_tot, 4),
        'y_mean': round(y_mean, 4),
        'sum_abs': round(float(np.sum(abs_err)), 4),
        'sum_sq': round(float(np.sum(sq_err)), 4),
        'n': n,
    }


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
                'jumlah_kasus': int(d.get('jumlah_kasus', 0)),
                'jk': int(d.get('jk', 0)),
                'jk_label': 'L' if d.get('jk') == 1 else 'P',
                'tingkat_risiko': d.get('tingkat_risiko', ''),
                'label_encoded': LABEL_ENCODE.get(d.get('tingkat_risiko'), 1),
            })

        pohon_results = []
        all_tree_preds = []

        for pohon_name in POHON_NAMES:
            pohon_data = _read_pohon(wb, pohon_name)
            if pohon_data is None or pohon_data['n_samples'] == 0:
                continue

            tree_info = _train_tree(pohon_data['samples'], pohon_data['features_used'])
            if tree_info is None:
                continue

            preds = _predict_all(tree_info['clf'], tree_info['features_used'], data_dbd)
            all_tree_preds.append(preds)

            class_dist = pohon_data['class_dist']
            total_bs = pohon_data['n_samples']
            proportions = {}
            for cls, cnt in class_dist.items():
                p = cnt / total_bs if total_bs > 0 else 0
                proportions[cls] = {'count': cnt, 'proportion': round(p, 4)}

            rules_lines = [l.strip() for l in tree_info['rules_text'].split('\n') if l.strip()]

            bootstrap_unique = len(set(
                hash(str(s)) for s in pohon_data['samples']
            ))

            pohon_results.append({
                'name': pohon_name,
                'id': len(pohon_results) + 1,
                'n_samples': total_bs,
                'n_unique': bootstrap_unique,
                'n_duplicates': total_bs - bootstrap_unique,
                'oob_pct': round((1 - bootstrap_unique / total_bs) * 100, 1) if total_bs > 0 else 0,
                'features_used': tree_info['features_used'],
                'n_features': tree_info['n_features'],
                'm_features': tree_info['m_features'],
                'class_dist': class_dist,
                'proportions': proportions,
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
            })

        voting_results = []
        actual_encoded = [LABEL_ENCODE.get(d.get('tingkat_risiko'), 1) for d in data_dbd]
        for i in range(total):
            votes = [all_tree_preds[t][i] for t in range(len(all_tree_preds))]
            from collections import Counter
            vote_counts = Counter(votes)
            final_pred = vote_counts.most_common(1)[0][0]
            voting_results.append({
                'no': i + 1,
                'actual': data_dbd[i].get('tingkat_risiko', ''),
                'actual_enc': actual_encoded[i],
                'votes': votes,
                'vote_labels': [LABEL_DECODE.get(v, '?') for v in votes],
                'final_pred_enc': final_pred,
                'final_pred': LABEL_DECODE.get(final_pred, '?'),
                'correct': actual_encoded[i] == final_pred,
            })

        correct_count = sum(1 for v in voting_results if v['correct'])
        accuracy = round(correct_count / total, 4) if total > 0 else 0

        final_pred_encoded = [v['final_pred_enc'] for v in voting_results]
        eval_voting = _compute_eval(actual_encoded, final_pred_encoded)

        per_tree_eval = []
        for t_idx, preds in enumerate(all_tree_preds):
            ev = _compute_eval(actual_encoded, preds)
            per_tree_eval.append({
                'name': pohon_results[t_idx]['name'] if t_idx < len(pohon_results) else f'Pohon {t_idx+1}',
                **ev,
            })

        return jsonify({
            'status': 'success',
            'step1': {
                'data': step1_data,
                'total': total,
                'features': ['Usia (X1)', 'Lama Rawat Inap (X2)', 'Jumlah Kasus (X3)', 'Jenis Kelamin (X4)'],
                'label_counts': label_counts,
                'encoding': {'Rendah': 0, 'Sedang': 1, 'Tinggi': 2},
            },
            'step2': {
                'note': 'Data diambil dari file Excel — encoding sudah dilakukan di Excel',
                'encoding_table': [
                    {'fitur': 'Jenis Kelamin', 'nilai_asli': 'L / P', 'nilai_encoding': '1 / 0'},
                    {'fitur': 'Tingkat Resiko', 'nilai_asli': 'Rendah / Sedang / Tinggi', 'nilai_encoding': '0 / 1 / 2'},
                ],
                'grouping_table': [
                    {'rentang': 'Kasus ≤ 8', 'risiko': 'Rendah', 'label': 0},
                    {'rentang': 'Kasus 9–15', 'risiko': 'Sedang', 'label': 1},
                    {'rentang': 'Kasus > 15', 'risiko': 'Tinggi', 'label': 2},
                ],
            },
            'step3': {
                'n': total,
                'm': m_features,
                'n_trees': len(pohon_results),
                'criterion': 'Entropy',
                'n_features_total': n_features_all,
                'formula_entropy': 'E(S) = -Σ pᵢ × log₂(pᵢ)',
                'formula_ig': 'IG(S,A) = E(S) - Σ (|Sᵥ|/|S|) × E(Sᵥ)',
            },
            'step4': {
                'trees': pohon_results,
                'best_tree_id': max(range(len(pohon_results)), key=lambda i: pohon_results[i]['ig']) + 1 if pohon_results else None,
            },
            'step7': {
                'voting_results': voting_results,
                'accuracy': accuracy,
                'correct_count': correct_count,
                'total': total,
            },
            'step8': {
                'voting_eval': eval_voting,
                'per_tree_eval': per_tree_eval,
            },
        })

    except Exception as e:
        import traceback
        return jsonify({
            'status': 'error',
            'message': str(e),
            'trace': traceback.format_exc(),
        }), 500
