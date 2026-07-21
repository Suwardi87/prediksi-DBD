"""
Machine Learning Model - Random Forest
25 pohon keputusan, fitur: Usia, Lama Rawat Inap, Jenis Kelamin
Threshold risiko: Rendah (≤8), Sedang (9-15), Tinggi (>15)
"""
import os
import pickle
from sklearn.tree import _tree, DecisionTreeClassifier
import math
import numpy as np
import pandas as pd

# numpy, pandas, sklearn imports are done lazily inside functions to avoid 
# Windows deadlock on import with newer versions (pandas 3.x, scikit-learn 1.8.x)

# Path untuk menyimpan model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'random_forest_model.pkl')

# Pastikan folder models ada
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

# Mapping bulan ke angka
BULAN_MAP = {
    'Januari': 1, 'Februari': 2, 'Maret': 3, 'April': 4,
    'Mei': 5, 'Juni': 6, 'Juli': 7, 'Agustus': 8,
    'September': 9, 'Oktober': 10, 'November': 11, 'Desember': 12
}

BULAN_NAMES = ['', 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
               'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']

# Label encoding: Rendah=1, Sedang=2, Tinggi=3
LABEL_MAP = {'Rendah': 1, 'Sedang': 2, 'Tinggi': 3}
INVERSE_LABEL_MAP = {1: 'Rendah', 2: 'Sedang', 3: 'Tinggi'}


def get_risk_level(jumlah_kasus):
    """
    Tentukan tingkat risiko berdasarkan jumlah kasus per bulan.
      - Rendah : ≤ 8 kasus
      - Sedang : 9 – 15 kasus
      - Tinggi : > 15 kasus
    """
    if jumlah_kasus > 15:
        return 'Tinggi'
    elif jumlah_kasus >= 9:
        return 'Sedang'
    else:
        return 'Rendah'


def get_usia_category(usia):
    """Kategori usia pasien"""
    if usia <= 12:
        return 'Anak-anak'
    elif usia <= 19:
        return 'Remaja'
    elif usia <= 59:
        return 'Dewasa'
    else:
        return 'Lansia'


def get_lama_rawat_category(lama_rawat):
    """Kategori lama rawat inap"""
    if lama_rawat <= 2:
        return 'Singkat'
    elif lama_rawat <= 4:
        return 'Sedang'
    else:
        return 'Lama'


def prepare_training_data(pasien_list, kasus_bulanan_dict=None):
    """
    Siapkan data untuk training dari data pasien DBD.
    Fitur: Usia (X1), Lama Rawat Inap (X2), Jenis Kelamin (X3)
      target = tingkat risiko (Rendah/Sedang/Tinggi)
    
    Catatan: Jumlah Kasus Perbulan digunakan untuk menentukan tingkat risiko (target),
    tetapi bukan fitur model.
    
    Args:
        pasien_list: List of PasienDBD objects
        kasus_bulanan_dict: Dict {(bulan, tahun): jumlah_kasus} untuk lookup risiko & fitur
    
    Returns:
        DataFrame siap training
    """
    import pandas as pd  # Lazy import to avoid Windows hang on startup
    
    if not pasien_list:
        raise ValueError("Tidak ada data pasien untuk training")
    
    data = []
    
    for pasien in pasien_list:
        # Tentukan tingkat risiko dari jumlah kasus bulanan
        tingkat_risiko = None
        jumlah_kasus = None
        
        if kasus_bulanan_dict:
            key = (pasien.bulan, pasien.tahun)
            jumlah_kasus = kasus_bulanan_dict.get(key)
            if jumlah_kasus is not None:
                tingkat_risiko = get_risk_level(jumlah_kasus)
        
        if tingkat_risiko is None:
            continue  # Skip jika tidak bisa tentukan risiko
        
        # Encode jenis kelamin: L=1, P=0
        jk_encoded = 1 if pasien.jenis_kelamin == 'L' else 0
        
        # Hitung lama rawat jika belum ada
        lama_rawat = pasien.lama_rawat
        if lama_rawat is None and pasien.tanggal_masuk and pasien.tanggal_keluar:
            lama_rawat = (pasien.tanggal_keluar - pasien.tanggal_masuk).days
        if lama_rawat is None:
            lama_rawat = 3  # Default jika tidak tersedia
        
        row = {
            'usia': pasien.usia,
            'lama_rawat': lama_rawat,
            'jenis_kelamin': jk_encoded,
            'tingkat_risiko': tingkat_risiko
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    
    # Validasi data
    if len(df) < 3:
        raise ValueError(f"Data terlalu sedikit untuk training. Minimal 3 data, tersedia: {len(df)}")
    
    return df


# ════════════════════════════════════════════════════════════════
# PROSES PEMBUATAN POHON KEPUTUSAN
# ════════════════════════════════════════════════════════════════

def calculate_entropy(class_counts):
    """
    Hitung entropy:
    E(S) = -Σ pi * log2(pi)
    """
    total = sum(class_counts)
    if total == 0:
        return 0.0
    entropy = 0.0
    for count in class_counts:
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)
    return entropy


def extract_rules(tree, feature_names, model_classes=None):
    """Mengekstrak rules dari single Decision Tree"""
    if model_classes is None:
        model_classes = np.array([1, 2, 3])
    
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    rules = []

    def recurse(node, current_rule):
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            
            rule_left = current_rule.copy()
            rule_left.append(f"{name} <= {threshold:.2f}")
            recurse(tree_.children_left[node], rule_left)
            
            rule_right = current_rule.copy()
            rule_right.append(f"{name} > {threshold:.2f}")
            recurse(tree_.children_right[node], rule_right)
        else:
            value = tree_.value[node][0]
            class_idx = np.argmax(value)
            class_label = model_classes[class_idx] if class_idx < len(model_classes) else 2
            class_name = INVERSE_LABEL_MAP.get(class_label, f'Class {class_label}')
            
            rules.append({
                'rule': " AND ".join(current_rule),
                'class': class_name,
                'confidence': float(value[class_idx] / np.sum(value)) * 100
            })

    recurse(0, [])
    return rules

def create_manual_rf():
    """Membuat RandomForest yang menggunakan data bootstrap persis dari Excel (Hanya Pohon 5)"""
    from sklearn.ensemble import RandomForestClassifier
    # Sesuai permintaan dosen, gunakan 1 estimator saja yang diambil dari Pohon 5
    rf = RandomForestClassifier(n_estimators=1, criterion='entropy', max_features=None, random_state=42)
    
    # Inisialisasi properti dasar agar dikenali sebagai fitted model
    dummy_X = np.zeros((3, 3))
    dummy_y = np.array([1, 2, 3])
    rf.fit(dummy_X, dummy_y)
    rf.estimators_ = []
    
    excel_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Data DBD 15 Sampel.xlsx')
    excel_path = os.path.abspath(excel_path)
    try:
        xls = pd.ExcelFile(excel_path)
        features_order = ['Usia.1', 'Lama Rawat Inap.1', 'Jenis Kelamin.1']
        
        # Hanya gunakan Pohon 5 (Pohon Terbaik)
        sheet_name = 'Pohon 5'
        if sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            
            if 'Tingkat Resiko.1' in df.columns:
                y_col = df['Tingkat Resiko.1'].dropna()
                # Hanya ambil baris yang isinya 'Rendah', 'Sedang', atau 'Tinggi'
                valid_labels = ['Rendah', 'Sedang', 'Tinggi']
                y_col = y_col[y_col.isin(valid_labels)]
                n_samples = len(y_col)
                
                X_boot = np.zeros((n_samples, 3))
                
                for col_idx, col_name in enumerate(features_order):
                    if col_name in df.columns:
                        # Konversi ke numerik, ubah teks jadi NaN, lalu drop
                        vals = pd.to_numeric(df[col_name], errors='coerce').dropna().values
                        if len(vals) >= n_samples:
                            X_boot[:, col_idx] = vals[:n_samples]
                        else:
                            # Jika kurang dari n_samples (misal karena ada nilai nol/kosong di Excel)
                            # pad dengan 0
                            limit = min(len(vals), n_samples)
                            X_boot[:limit, col_idx] = vals[:limit]
                            
                y_boot_labels = y_col.values
                # Encode ke label asli (1, 2, 3)
                y_boot_class = np.array([LABEL_MAP.get(str(lbl).strip(), 2) for lbl in y_boot_labels])
                # Scikit-learn RF meng-encode kelas internal pohon sebagai indeks 0-based
                y_boot = np.searchsorted(dummy_y, y_boot_class)
                
                # Tambahkan dummy rows untuk ketiga class (0, 1, 2) dengan bobot 0
                # agar DecisionTree memiliki array tree.value berukuran 3 secara internal
                X_dummy = np.zeros((3, 3))
                y_dummy = np.array([0, 1, 2])
                X_boot_aug = np.vstack([X_boot, X_dummy])
                y_boot_aug = np.concatenate([y_boot, y_dummy])
                
                weights = np.ones(n_samples + 3)
                weights[-3:] = 0.0
                
                dt = DecisionTreeClassifier(criterion='entropy', max_features=None, random_state=42)
                dt.fit(X_boot_aug, y_boot_aug, sample_weight=weights)
                rf.estimators_.append(dt)
    except Exception as e:
        print("Gagal meload data excel:", e)
        
    return rf

def extract_tree_rules(estimator, feature_names, model_classes):
    """
    Ekstrak aturan keputusan (IF-THEN rules) dari pohon keputusan
    """
    tree = estimator.tree_
    rules = []
    
    def recurse(node, conditions):
        # Leaf node
        if tree.children_left[node] == tree.children_right[node]:
            class_counts = tree.value[node].flatten()
            class_idx = class_counts.argmax()
            class_label = model_classes[class_idx]
            class_name = INVERSE_LABEL_MAP.get(class_label, f'Class {class_label}')
            
            if conditions:
                rule_str = "IF " + " AND ".join(conditions) + f" THEN Tingkat Risiko = {class_name}"
            else:
                rule_str = f"THEN Tingkat Risiko = {class_name}"
            
            rules.append(rule_str)
            return
        
        feature_idx = tree.feature[node]
        threshold = tree.threshold[node]
        fname = feature_names[feature_idx] if feature_idx < len(feature_names) else f'X{feature_idx + 1}'
        
        # Left child (feature <= threshold)
        recurse(tree.children_left[node], conditions + [f"{fname} ≤ {threshold:.2f}"])
        # Right child (feature > threshold)
        recurse(tree.children_right[node], conditions + [f"{fname} > {threshold:.2f}"])
    
    recurse(0, [])
    return rules


def extract_all_trees_details(model, X_test, y_test,
                              feature_names=None):
    """
    Ekstrak detail proses pembuatan setiap pohon keputusan.
    
    Untuk setiap pohon:
    1. Distribusi kelas pada bootstrap sample
    2. Entropy root
    3. Fitur split & threshold di root
    4. Information Gain
    5. Rules / aturan keputusan
    6. Evaluasi per pohon: MAE, RMSE, R2
    
    Returns:
        dict with 'trees', 'optimal_tree_idx', 'optimal_tree', 'evaluation_summary'
    """
    # Lazy import numpy/sklearn to avoid deadlock on Windows with newer versions
    import numpy as np
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score as sklearn_r2_score
    
    if feature_names is None:
        feature_names = ['Usia', 'Lama Rawat Inap', 'Jenis Kelamin', 'Jumlah Kasus']
    
    trees_details = []
    
    for i, estimator in enumerate(model.estimators_):
        tree = estimator.tree_
        
        # ── 1. Distribusi kelas di root (= bootstrap sample) ──
        # Catatan: sklearn modern mengembalikan tree.value sebagai fractions (sum=1.0),
        # bukan raw counts. Kalikan dengan weighted_n_node_samples untuk dapat counts asli.
        root_counts = tree.value[0].flatten()
        total_weighted = float(tree.weighted_n_node_samples[0])
        root_counts_scaled = root_counts * total_weighted
        total_samples = int(round(root_counts_scaled.sum()))
        class_dist = {}
        class_probs = {}
        for j, cls in enumerate(model.classes_):
            cls_name = INVERSE_LABEL_MAP.get(cls, f'Class {cls}')
            cnt = int(round(root_counts_scaled[j])) if j < len(root_counts_scaled) else 0
            class_dist[cls_name] = cnt
            class_probs[cls_name] = round(cnt / total_samples, 6) if total_samples > 0 else 0
        
        # ── 2. Entropy root ──
        root_entropy = calculate_entropy([round(c) for c in root_counts_scaled])
        
        # ── 3. Fitur dan threshold split di root ──
        root_feature_idx = tree.feature[0]
        root_threshold = tree.threshold[0]
        root_feature = (
            feature_names[root_feature_idx]
            if 0 <= root_feature_idx < len(feature_names)
            else 'Leaf'
        )
        
        # ── 4. Information Gain di root ──
        information_gain = 0.0
        left_entropy = 0.0
        right_entropy = 0.0
        left_count = 0
        right_count = 0
        
        if tree.children_left[0] >= 0 and tree.children_right[0] >= 0:
            left_w = float(tree.weighted_n_node_samples[tree.children_left[0]])
            right_w = float(tree.weighted_n_node_samples[tree.children_right[0]])
            left_counts = tree.value[tree.children_left[0]].flatten() * left_w
            right_counts = tree.value[tree.children_right[0]].flatten() * right_w
            left_entropy = calculate_entropy([round(c) for c in left_counts])
            right_entropy = calculate_entropy([round(c) for c in right_counts])
            left_count = int(round(left_counts.sum()))
            right_count = int(round(right_counts.sum()))
            lw = left_count / total_samples if total_samples > 0 else 0
            rw = right_count / total_samples if total_samples > 0 else 0
            information_gain = root_entropy - (lw * left_entropy + rw * right_entropy)
        
        # ── 5. Rules ──
        rules = extract_tree_rules(estimator, feature_names, model.classes_)
        
        # ── 6. Evaluasi per pohon (MAE, RMSE, R²) ──
        # Map prediksi melalui model.classes_ (tree predict mengembalikan
        # indeks 0-based, bukan label kelas asli)
        y_pred_raw = estimator.predict(X_test)
        y_pred_tree = model.classes_[y_pred_raw.astype(int)]
        if len(y_test) > 1:
            mae_tree = float(mean_absolute_error(y_test, y_pred_tree))
            mse_tree = float(mean_squared_error(y_test, y_pred_tree))
            rmse_tree = float(math.sqrt(mse_tree))
            r2_tree = float(sklearn_r2_score(y_test, y_pred_tree))
        else:
            mae_tree = rmse_tree = r2_tree = 0.0
        
        trees_details.append({
            'tree_id': i + 1,
            'name': f'Pohon {i + 1}',
            'total_samples': total_samples,
            'class_distribution': class_dist,
            'class_probabilities': class_probs,
            'root_entropy': round(root_entropy, 6),
            'root_feature': root_feature,
            'root_threshold': round(float(root_threshold), 2) if root_feature_idx >= 0 else None,
            'information_gain': round(information_gain, 6),
            'split_detail': {
                'left_entropy': round(left_entropy, 6),
                'right_entropy': round(right_entropy, 6),
                'left_samples': left_count,
                'right_samples': right_count
            },
            'n_leaves': int(tree.n_leaves),
            'max_depth': int(tree.max_depth),
            'rules': rules,
            'evaluation': {
                'mae': round(mae_tree, 4),
                'rmse': round(rmse_tree, 4),
                'r2': round(r2_tree, 4)
            }
        })
    
    # ── Cari pohon optimal ──
    # Pohon optimal = R² tertinggi di antara pohon yang TIDAK overfitting.
    # Pohon dengan R²=1.0 (sempurna) dianggap overfitting pada bootstrap
    # sample-nya. Jika semua pohon R²=1.0, gunakan pohon pertama.
    optimal_idx = 0
    if trees_details:
        # Filter pohon non-overfitting (R² < 1.0)
        non_overfit = [idx for idx in range(len(trees_details))
                       if trees_details[idx]['evaluation']['r2'] < 1.0]
        if non_overfit:
            best_r2 = max(trees_details[idx]['evaluation']['r2']
                         for idx in non_overfit)
            # Ambil semua pohon dengan R² terbaik (bisa ada ties)
            candidates = [idx for idx in non_overfit
                          if trees_details[idx]['evaluation']['r2'] == best_r2]
            # Tiebreaker: pilih pohon dengan indeks median (paling representatif)
            optimal_idx = candidates[len(candidates) // 2]
        else:
            # Semua pohon sempurna, pilih pohon pertama
            optimal_idx = 0
    
    return {
        'trees': trees_details,
        'optimal_tree_idx': optimal_idx + 1,  # 1-based
        'optimal_tree': trees_details[optimal_idx] if trees_details else None
    }


def train_model(data, n_estimators=25, max_depth=None, random_state=42):
    """
    Training model Random Forest.
    - n_estimators pohon keputusan (default 25)
    - 3 fitur: Usia, Lama Rawat Inap, Jenis Kelamin
    - Evaluasi: Stratified 5-Fold Cross-Validation
    - Metrik: Accuracy, Precision, Recall, F1, MAE, RMSE, R2
    
    Args:
        data: DataFrame dengan kolom features dan target
        n_estimators: Jumlah decision trees (default 25)
        max_depth: Kedalaman maksimum tree (default None = unlimited, tidak digunakan di UI)
        random_state: Seed untuk reproducibility
    
    Returns:
        dict: Hasil training dengan metrics dan model
    """
    # Lazy import numpy/sklearn to avoid deadlock on Windows with newer versions
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, f1_score,
        confusion_matrix, classification_report, mean_absolute_error, mean_squared_error,
        r2_score as sklearn_r2_score
    )
    from sklearn.model_selection import StratifiedKFold
    
    # Validasi input
    if data is None or len(data) == 0:
        raise ValueError("Data training kosong")
    
    # Fitur: Usia (X1), Lama Rawat Inap (X2), Jenis Kelamin (X3)
    feature_columns = ['usia', 'lama_rawat', 'jenis_kelamin']
    
    # Validasi kolom
    missing_cols = [col for col in feature_columns + ['tingkat_risiko'] if col not in data.columns]
    if missing_cols:
        raise ValueError(f"Kolom berikut tidak ditemukan: {missing_cols}")
    
    X = data[feature_columns].values
    y = data['tingkat_risiko'].values
    
    # Encode target labels: Rendah=1, Sedang=2, Tinggi=3
    y_encoded = np.array([LABEL_MAP.get(label, 2) for label in y])
    
    # Cek jumlah class
    unique_classes = np.unique(y_encoded)
    if len(unique_classes) < 2:
        raise ValueError(f"Data harus memiliki minimal 2 class berbeda. Ditemukan: {len(unique_classes)} class")
    
    # Cek minimal samples per class untuk StratifiedKFold
    n_folds = 5
    unique, counts = np.unique(y_encoded, return_counts=True)
    min_class_count = int(min(counts))
    if min_class_count < n_folds:
        raise ValueError(
            f"Setiap class harus memiliki minimal {n_folds} data untuk {n_folds}-Fold CV. "
            f"Class dengan data paling sedikit hanya memiliki {min_class_count} data."
        )
    
    # ═══════════════════════════════════════════════════════════════════
    # EVALUASI: Stratified K-Fold Cross-Validation (stabil & konsisten)
    # ═══════════════════════════════════════════════════════════════════
    # Dengan 40 data, single split hanya 8 test → 1 error = 12.5% swing.
    # K-Fold CV menggunakan SEMUA data untuk evaluasi → metrik stabil
    # meskipun parameter (n_estimators) diubah.
    
    skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=random_state)
    
    # Akumulasi metrik dari setiap fold
    cv_accuracy = []
    cv_precision = []
    cv_recall = []
    cv_f1 = []
    cv_mae = []
    cv_rmse = []
    cv_r2 = []
    all_y_test = []
    all_y_pred = []
    
    for fold_idx, (train_idx, test_idx) in enumerate(skf.split(X, y_encoded)):
        X_fold_train, X_fold_test = X[train_idx], X[test_idx]
        y_fold_train, y_fold_test = y_encoded[train_idx], y_encoded[test_idx]
        
        fold_model = RandomForestClassifier(
            n_estimators=n_estimators,
            criterion='entropy',
            max_features='sqrt',
            max_depth=max_depth,
            bootstrap=True,
            random_state=random_state,
            n_jobs=1
        )
        fold_model.fit(X_fold_train, y_fold_train)
        y_fold_pred = fold_model.predict(X_fold_test)
        
        cv_accuracy.append(accuracy_score(y_fold_test, y_fold_pred))
        cv_precision.append(precision_score(y_fold_test, y_fold_pred, average='weighted', zero_division=0))
        cv_recall.append(recall_score(y_fold_test, y_fold_pred, average='weighted', zero_division=0))
        cv_f1.append(f1_score(y_fold_test, y_fold_pred, average='weighted', zero_division=0))
        cv_mae.append(mean_absolute_error(y_fold_test, y_fold_pred))
        mse_fold = mean_squared_error(y_fold_test, y_fold_pred)
        cv_rmse.append(math.sqrt(mse_fold))
        cv_r2.append(sklearn_r2_score(y_fold_test, y_fold_pred) if len(y_fold_test) > 1 else 0.0)
        
        all_y_test.extend(y_fold_test.tolist())
        all_y_pred.extend(y_fold_pred.tolist())
    
    # Metrik rata-rata dari CV (stabil meskipun parameter diubah)
    accuracy = float(np.mean(cv_accuracy))
    precision = float(np.mean(cv_precision))
    recall = float(np.mean(cv_recall))
    f1 = float(np.mean(cv_f1))
    mae_val = float(np.mean(cv_mae))
    rmse_val = float(np.mean(cv_rmse))
    r2_val = float(np.mean(cv_r2))
    
    # Gabungan semua prediksi CV untuk confusion matrix & per-class metrics
    all_y_test = np.array(all_y_test)
    all_y_pred = np.array(all_y_pred)
    
    # ═══════════════════════════════════════════════════════════════════
    # MODEL FINAL: Train pada SELURUH data untuk disimpan & prediksi
    # ═══════════════════════════════════════════════════════════════════
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        criterion='entropy',
        max_features='sqrt',
        max_depth=max_depth,
        bootstrap=True,
        random_state=random_state,
        n_jobs=1
    )
    model.fit(X, y_encoded)
    
    # Untuk tree details, gunakan SELURUH data agar rules nya komprehensif
    X_test_for_trees = X
    y_test_for_trees = y_encoded
    
    # ── Metrik Klasifikasi (sudah dihitung dari CV di atas) ──
    
    # Per-class metrics dari gabungan semua fold
    precision_per_class = precision_score(all_y_test, all_y_pred, average=None, labels=[1,2,3], zero_division=0)
    recall_per_class = recall_score(all_y_test, all_y_pred, average=None, labels=[1,2,3], zero_division=0)
    f1_per_class = f1_score(all_y_test, all_y_pred, average=None, labels=[1,2,3], zero_division=0)
    
    # Confusion matrix dari gabungan semua fold
    cm = confusion_matrix(all_y_test, all_y_pred, labels=[1, 2, 3]).tolist()
    
    # Classification report
    try:
        class_report = classification_report(all_y_test, all_y_pred,
                                            labels=[1, 2, 3],
                                            target_names=['Rendah', 'Sedang', 'Tinggi'],
                                            output_dict=True,
                                            zero_division=0)
    except Exception:
        class_report = {
            'Rendah': {'precision': 0, 'recall': 0, 'f1-score': 0, 'support': 0},
            'Sedang': {'precision': 0, 'recall': 0, 'f1-score': 0, 'support': 0},
            'Tinggi': {'precision': 0, 'recall': 0, 'f1-score': 0, 'support': 0}
        }
    
    # ── Metrik MAE, RMSE, R² sudah dihitung dari CV ──
    
    # Feature importance (dari model final yang dilatih pada semua data)
    feature_names_list = ['Usia', 'Lama Rawat Inap', 'Jenis Kelamin']
    feature_importance = dict(zip(
        feature_names_list,
        model.feature_importances_.tolist()
    ))
    
    # ── Proses Pembuatan Pohon — ekstrak detail dari model final ──
    trees_info = extract_all_trees_details(
        model, X_test_for_trees, y_test_for_trees,
        feature_names=feature_names_list
    )
    
    # Save model
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump({
            'model': model,
            'feature_columns': feature_columns,
            'label_map': LABEL_MAP,
            'inverse_label_map': INVERSE_LABEL_MAP
        }, f)
    
    # Hitung metrik per kelas (dari gabungan seluruh fold CV)
    per_class_metrics = {}
    class_names = ['Rendah', 'Sedang', 'Tinggi']
    for i, class_name in enumerate(class_names):
        per_class_metrics[class_name] = {
            'precision': float(precision_per_class[i]) if i < len(precision_per_class) else 0.0,
            'recall': float(recall_per_class[i]) if i < len(recall_per_class) else 0.0,
            'f1_score': float(f1_per_class[i]) if i < len(f1_per_class) else 0.0,
            'support': int(class_report.get(class_name, {}).get('support', 0))
        }
    
    # Jumlah data train/test per fold
    n_per_fold = len(X) // n_folds
    
    return {
        'status': 'success',
        'metrics': {
            'accuracy': float(accuracy),
            'precision_weighted': float(precision),
            'recall_weighted': float(recall),
            'f1_score_weighted': float(f1),
            'mae': float(mae_val),
            'rmse': float(rmse_val),
            'r2_score': float(r2_val)
        },
        'cv_details': {
            'n_folds': n_folds,
            'fold_accuracies': [round(a, 4) for a in cv_accuracy],
            'fold_f1_scores': [round(f, 4) for f in cv_f1],
            'accuracy_std': float(np.std(cv_accuracy)),
            'f1_std': float(np.std(cv_f1))
        },
        'per_class_metrics': per_class_metrics,
        'confusion_matrix': cm,
        'feature_importance': feature_importance,
        'training_samples': len(X) - n_per_fold,
        'test_samples': n_per_fold,
        'total_data': len(X),
        'n_estimators': n_estimators,
        'max_depth': max_depth,
        'random_state': random_state,
        'model_type': 'Random Forest Classifier (Pohon Keputusan)',
        'evaluation_method': f'Stratified {n_folds}-Fold Cross-Validation',
        'trees_details': trees_info
    }


def load_model():
    """Load trained model from file"""
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            return pickle.load(f)
    return None


def predict(usia, lama_rawat, jenis_kelamin='L'):
    """
    Membuat prediksi tingkat risiko
    Fitur model: Usia, Lama Rawat Inap, Jenis Kelamin
    
    Args:
        usia: Usia pasien (tahun)
        lama_rawat: Lama rawat inap (hari)
        jenis_kelamin: 'L' atau 'P'
    
    Returns:
        dict: Hasil prediksi
    """
    import numpy as np  # Lazy import to avoid Windows hang on startup
    
    model_data = load_model()
    
    if model_data is None:
        # Gunakan rule-based jika model belum ada
        risk_level = 'Sedang'
        return {
            'status': 'success',
            'prediction': {
                'tingkat_risiko': risk_level,
                'confidence': 75.0,
                'probabilities': {
                    'Tinggi': 12.5,
                    'Sedang': 75.0,
                    'Rendah': 12.5
                }
            },
            'recommendation': get_recommendation(risk_level),
            'model_used': False
        }
    
    model = model_data['model']
    inverse_label_map = model_data.get('inverse_label_map', INVERSE_LABEL_MAP)
    
    # Prepare input — 3 fitur: Usia, Lama Rawat, JK
    jk_encoded = 1 if jenis_kelamin == 'L' else 0
    X = np.array([[usia, lama_rawat, jk_encoded]])
    
    # Predict
    prediction = model.predict(X)[0]
    probabilities = model.predict_proba(X)[0]
    
    risk_level = inverse_label_map.get(prediction, 'Sedang')
    confidence = max(probabilities) * 100
    
    # Map probabilities ke label
    classes = model.classes_
    prob_dict = {}
    for i, prob in enumerate(probabilities):
        label = inverse_label_map.get(classes[i], f'Class_{classes[i]}')
        prob_dict[label] = float(prob * 100)
    
    # Pastikan semua kategori ada
    for cat in ['Rendah', 'Sedang', 'Tinggi']:
        if cat not in prob_dict:
            prob_dict[cat] = 0.0
    
    return {
        'status': 'success',
        'prediction': {
            'tingkat_risiko': risk_level,
            'confidence': float(confidence),
            'probabilities': prob_dict
        },
        'recommendation': get_recommendation(risk_level),
        'model_used': True,
        'input_data': {
            'usia': usia,
            'kategori_usia': get_usia_category(usia),
            'lama_rawat': lama_rawat,
            'kategori_lama_rawat': get_lama_rawat_category(lama_rawat),
            'jenis_kelamin': jenis_kelamin
        }
    }


def get_recommendation(risk_level):
    """Mendapatkan rekomendasi berdasarkan tingkat risiko"""
    recommendations = {
        'Tinggi': {
            'status': '⚠️ WASPADA TINGGI',
            'actions': [
                'Segera lakukan fogging massal di seluruh wilayah',
                'Aktifkan posko kesehatan darurat',
                'Sosialisasi pencegahan ke masyarakat',
                'Koordinasi dengan Dinas Kesehatan',
                'Siapkan kapasitas ruang rawat inap tambahan'
            ]
        },
        'Sedang': {
            'status': '⚡ PERHATIAN',
            'actions': [
                'Tingkatkan monitoring kasus harian',
                'Lakukan fogging di area fokus',
                'Edukasi masyarakat tentang PSN (Pemberantasan Sarang Nyamuk)',
                'Siapkan stok obat dan alat kesehatan'
            ]
        },
        'Rendah': {
            'status': '✅ TERKENDALI',
            'actions': [
                'Lanjutkan program pencegahan rutin',
                'Monitoring berkala kondisi lingkungan',
                'Edukasi berkelanjutan ke masyarakat',
                'Evaluasi program yang berjalan'
            ]
        }
    }
    return recommendations.get(risk_level, recommendations['Sedang'])

def predict_batch_with_trees(pasien_list):
    """
    Prediksi batch data pasien dan kembalikan detail voting tiap pohon
    """
    import numpy as np
    from app.models import KasusBulanan, PasienDBD
    
    model_data = load_model()
    if not model_data:
        return {'status': 'error', 'message': 'Model belum ditraining'}
        
    model = model_data['model']
    inverse_label_map = model_data.get('inverse_label_map', INVERSE_LABEL_MAP)
    
    results = []
    
    for pasien in pasien_list:
        jk_encoded = 1 if pasien.jenis_kelamin == 'L' else 0
        lama_rawat = pasien.lama_rawat
        if lama_rawat is None and pasien.tanggal_masuk and pasien.tanggal_keluar:
            lama_rawat = (pasien.tanggal_keluar - pasien.tanggal_masuk).days
        if lama_rawat is None:
            lama_rawat = 3
            
        X = np.array([[pasien.usia, lama_rawat, jk_encoded]])
        
        # Get individual tree predictions
        tree_votes = []
        # Batasi penampilan maksimal 5 pohon pertama untuk UI (walau n_estimators > 5)
        trees_to_show = model.estimators_[:5]
        for tree in trees_to_show:
            # Tree prediction mengembalikan kelas asli (bukan array probabilitas),
            # jadi langsung pakai tanpa np.argmax
            pred_class = int(tree.predict(X)[0])
            tree_votes.append(inverse_label_map.get(pred_class, 'Sedang'))
            
        # Get final prediction
        final_pred_idx = model.predict(X)[0]
        final_pred = inverse_label_map.get(final_pred_idx, 'Sedang')
        
        # Get actual risk
        kasus_bulanan = KasusBulanan.query.filter_by(bulan=pasien.bulan, tahun=pasien.tahun).first()
        if kasus_bulanan:
            jml_kasus = kasus_bulanan.jumlah_kasus
        else:
            jml_kasus = PasienDBD.query.filter_by(bulan=pasien.bulan, tahun=pasien.tahun).count()
            
        aktual = get_risk_level(jml_kasus)
        
        results.append({
            'id': pasien.id,
            'nama': pasien.nama_pasien,
            'usia': pasien.usia,
            'lama_rawat': lama_rawat,
            'jumlah_kasus': jml_kasus,
            'jenis_kelamin': pasien.jenis_kelamin,
            'tree_votes': tree_votes,
            'final_prediction': final_pred,
            'aktual': aktual,
            'status_prediksi': 'Benar' if final_pred == aktual else 'Salah'
        })
        
    return {'status': 'success', 'data': results}
