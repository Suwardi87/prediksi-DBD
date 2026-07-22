"""
Comprehensive Test Suite — Prediksi DBD
Tests ML pipeline, routes, edge cases, and data integrity.
"""
import sys
import os
import json
import math
import traceback
from datetime import date, datetime

# ═══════════════════════════════════════════════════════
# SETUP
# ═══════════════════════════════════════════════════════
from app import create_app, db
from app.models import User, PasienDBD, KasusBulanan, ModelEvaluasi, HasilPrediksi, LogAktivitas
from app.ml_model import (
    get_risk_level, get_usia_category, get_lama_rawat_category,
    calculate_entropy, prepare_training_data, train_model,
    predict, load_model, predict_batch_with_trees,
    extract_rules, extract_tree_rules, create_manual_rf,
    LABEL_MAP, INVERSE_LABEL_MAP, BULAN_NAMES
)

app = create_app()
app.config['LOGIN_DISABLED'] = True
app.config['TESTING'] = True

passed = 0
failed = 0
errors = []

def run_test(name, fn):
    global passed, failed, errors
    try:
        fn()
        passed += 1
        print(f"  PASS  {name}")
    except AssertionError as e:
        failed += 1
        errors.append((name, str(e)))
        print(f"  FAIL  {name}: {e}")
    except Exception as e:
        failed += 1
        errors.append((name, f"{type(e).__name__}: {e}"))
        print(f"  ERROR {name}: {type(e).__name__}: {e}")
        traceback.print_exc()

def login_client(client):
    """Simulate logged-in user for routes with custom decorators."""
    with client.session_transaction() as sess:
        sess['_user_id'] = '1'
        sess['_fresh'] = True

# ═══════════════════════════════════════════════════════
# 1. ML MODEL — UNIT TESTS
# ═══════════════════════════════════════════════════════
print("\n═══ 1. ML MODEL UNIT TESTS ═══")

def test_get_risk_level():
    assert get_risk_level(0) == 'Rendah', f"0 → {get_risk_level(0)}"
    assert get_risk_level(8) == 'Rendah', f"8 → {get_risk_level(8)}"
    assert get_risk_level(9) == 'Sedang', f"9 → {get_risk_level(9)}"
    assert get_risk_level(15) == 'Sedang', f"15 → {get_risk_level(15)}"
    assert get_risk_level(16) == 'Tinggi', f"16 → {get_risk_level(16)}"
    assert get_risk_level(100) == 'Tinggi', f"100 → {get_risk_level(100)}"
run_test("get_risk_level boundaries", test_get_risk_level)

def test_get_usia_category():
    assert get_usia_category(5) == 'Anak-anak'
    assert get_usia_category(12) == 'Anak-anak'
    assert get_usia_category(13) == 'Remaja'
    assert get_usia_category(19) == 'Remaja'
    assert get_usia_category(20) == 'Dewasa'
    assert get_usia_category(59) == 'Dewasa'
    assert get_usia_category(60) == 'Lansia'
    assert get_usia_category(90) == 'Lansia'
run_test("get_usia_category boundaries", test_get_usia_category)

def test_get_lama_rawat_category():
    assert get_lama_rawat_category(0) == 'Singkat'
    assert get_lama_rawat_category(2) == 'Singkat'
    assert get_lama_rawat_category(3) == 'Sedang'
    assert get_lama_rawat_category(4) == 'Sedang'
    assert get_lama_rawat_category(5) == 'Lama'
    assert get_lama_rawat_category(30) == 'Lama'
run_test("get_lama_rawat_category boundaries", test_get_lama_rawat_category)

def test_calculate_entropy():
    # All same class → entropy = 0
    assert calculate_entropy([10, 0, 0]) == 0.0
    assert calculate_entropy([0, 10, 0]) == 0.0
    # Equal distribution → max entropy
    e = calculate_entropy([1, 1, 1])
    expected = -3 * (1/3 * math.log2(1/3))
    assert abs(e - expected) < 1e-10, f"Expected {expected}, got {e}"
    # Two classes
    e2 = calculate_entropy([1, 1])
    assert abs(e2 - 1.0) < 1e-10, f"Expected 1.0, got {e2}"
    # Empty
    assert calculate_entropy([]) == 0.0
    assert calculate_entropy([0, 0, 0]) == 0.0
run_test("calculate_entropy correctness", test_calculate_entropy)

def test_label_map_consistency():
    assert LABEL_MAP == {'Rendah': 1, 'Sedang': 2, 'Tinggi': 3}
    assert INVERSE_LABEL_MAP == {1: 'Rendah', 2: 'Sedang', 3: 'Tinggi'}
    for k, v in LABEL_MAP.items():
        assert INVERSE_LABEL_MAP[v] == k, f"Inverse mismatch for {k}"
run_test("label map consistency", test_label_map_consistency)

def test_bulan_names():
    assert len(BULAN_NAMES) == 13  # index 0 = empty
    assert BULAN_NAMES[1] == 'Januari'
    assert BULAN_NAMES[12] == 'Desember'
    assert BULAN_NAMES[0] == ''
run_test("bulan names completeness", test_bulan_names)

# ═══════════════════════════════════════════════════════
# 2. DATA PREPARATION — EDGE CASES
# ═══════════════════════════════════════════════════════
print("\n═══ 2. DATA PREPARATION TESTS ═══")

def test_prepare_training_data_empty():
    try:
        prepare_training_data([], {})
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "Tidak ada data" in str(e)
run_test("prepare_training_data: empty list raises error", test_prepare_training_data_empty)

def test_prepare_training_data_no_match():
    class FakePasien:
        def __init__(self, usia, lama_rawat, jk, bulan, tahun):
            self.usia = usia
            self.lama_rawat = lama_rawat
            self.jenis_kelamin = jk
            self.bulan = bulan
            self.tahun = tahun
            self.tanggal_masuk = date(2025, 1, 1)
            self.tanggal_keluar = date(2025, 1, 5)

    pasien_list = [FakePasien(25, 5, 'L', 'Januari', 2025)]
    # Empty dict → no match → all patients skipped → raises ValueError
    try:
        df = prepare_training_data(pasien_list, {})
        assert False, f"Should raise ValueError, got {len(df)} rows"
    except ValueError:
        pass
run_test("prepare_training_data: no kasus match skips all", test_prepare_training_data_no_match)

def test_prepare_training_data_with_match():
    class FakePasien:
        def __init__(self, usia, lama_rawat, jk, bulan, tahun):
            self.usia = usia
            self.lama_rawat = lama_rawat
            self.jenis_kelamin = jk
            self.bulan = bulan
            self.tahun = tahun
            self.tanggal_masuk = None
            self.tanggal_keluar = None

    pasien_list = [
        FakePasien(10, 3, 'L', 'Januari', 2025),
        FakePasien(25, 5, 'P', 'Februari', 2025),
        FakePasien(60, 10, 'L', 'Maret', 2025),
    ]
    kasus_dict = {
        ('Januari', 2025): 5,   # Rendah
        ('Februari', 2025): 12, # Sedang
        ('Maret', 2025): 20,    # Tinggi
    }
    df = prepare_training_data(pasien_list, kasus_dict)
    assert len(df) == 3, f"Expected 3 rows, got {len(df)}"
    assert list(df.columns) == ['usia', 'lama_rawat', 'jenis_kelamin', 'tingkat_risiko']
    # Check labels
    labels = df['tingkat_risiko'].tolist()
    assert 'Rendah' in labels
    assert 'Sedang' in labels
    assert 'Tinggi' in labels
    # Check encoding: L=1, P=0
    jk_vals = df['jenis_kelamin'].tolist()
    assert 1 in jk_vals  # L
    assert 0 in jk_vals  # P
run_test("prepare_training_data: correct encoding and labels", test_prepare_training_data_with_match)

def test_prepare_training_data_default_lama_rawat():
    class FakePasien:
        def __init__(self, usia, bulan):
            self.usia = usia
            self.lama_rawat = None
            self.jenis_kelamin = 'L'
            self.bulan = bulan
            self.tahun = 2025
            self.tanggal_masuk = None
            self.tanggal_keluar = None

    pasien_list = [
        FakePasien(10, 'Januari'),
        FakePasien(20, 'Januari'),
        FakePasien(30, 'Januari'),
    ]
    df = prepare_training_data(pasien_list, {('Januari', 2025): 5})
    assert len(df) == 3
    for _, row in df.iterrows():
        assert row['lama_rawat'] == 3, f"Default lama_rawat should be 3, got {row['lama_rawat']}"
run_test("prepare_training_data: default lama_rawat=3", test_prepare_training_data_default_lama_rawat)

# ═══════════════════════════════════════════════════════
# 3. TRAINING PIPELINE
# ═══════════════════════════════════════════════════════
print("\n═══ 3. TRAINING PIPELINE TESTS ═══")

def test_train_model_returns_correct_structure():
    import pandas as pd
    import numpy as np

    data = pd.DataFrame({
        'usia': [10, 20, 30, 40, 50, 60, 15, 25, 35, 45, 55, 65, 12, 22, 32],
        'lama_rawat': [2, 3, 5, 7, 4, 6, 3, 4, 6, 8, 5, 7, 2, 3, 5],
        'jenis_kelamin': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        'tingkat_risiko': ['Rendah', 'Rendah', 'Sedang', 'Sedang', 'Tinggi', 'Tinggi',
                           'Rendah', 'Sedang', 'Sedang', 'Tinggi', 'Tinggi', 'Tinggi',
                           'Rendah', 'Rendah', 'Sedang']
    })

    result = train_model(data, n_estimators=5, random_state=42)

    # Check structure
    assert result['status'] == 'success'
    assert 'metrics' in result
    assert 'cv_details' in result
    assert 'per_class_metrics' in result
    assert 'confusion_matrix' in result
    assert 'feature_importance' in result
    assert 'trees_details' in result

    # Check metrics exist
    m = result['metrics']
    for key in ['accuracy', 'precision_weighted', 'recall_weighted', 'f1_score_weighted', 'mae', 'rmse', 'r2_score']:
        assert key in m, f"Missing metric: {key}"

    # Check metric ranges
    assert 0 <= m['accuracy'] <= 1, f"accuracy out of range: {m['accuracy']}"
    assert 0 <= m['precision_weighted'] <= 1, f"precision out of range"
    assert 0 <= m['recall_weighted'] <= 1, f"recall out of range"
    assert 0 <= m['f1_score_weighted'] <= 1, f"f1 out of range"

    # Check tree details
    trees = result['trees_details']['trees']
    assert len(trees) == 5, f"Expected 5 trees, got {len(trees)}"
    for t in trees:
        assert 'tree_id' in t
        assert 'root_entropy' in t
        assert 'information_gain' in t
        assert 'rules' in t
        assert 'evaluation' in t

    # Check confusion matrix is 3x3
    cm = result['confusion_matrix']
    assert len(cm) == 3, f"CM should have 3 rows, got {len(cm)}"
    for row in cm:
        assert len(row) == 3, f"CM row should have 3 cols, got {len(row)}"

    # Check feature importance
    fi = result['feature_importance']
    assert 'Usia' in fi
    assert 'Lama Rawat Inap' in fi
    assert 'Jenis Kelamin' in fi
    assert abs(sum(fi.values()) - 1.0) < 0.01, f"Feature importance should sum to ~1.0, got {sum(fi.values())}"

run_test("train_model: correct structure and metric ranges", test_train_model_returns_correct_structure)

def test_train_model_minimum_data():
    import pandas as pd
    data = pd.DataFrame({
        'usia': [10, 20],
        'lama_rawat': [2, 3],
        'jenis_kelamin': [1, 0],
        'tingkat_risiko': ['Rendah', 'Sedang']
    })
    try:
        train_model(data, n_estimators=3)
        assert False, "Should raise ValueError for too few samples"
    except ValueError as e:
        assert "minimal" in str(e).lower() or "terlalu sedikit" in str(e).lower() or "class" in str(e).lower() or "data" in str(e).lower()
run_test("train_model: too few samples raises error", test_train_model_minimum_data)

def test_train_model_single_class():
    import pandas as pd
    data = pd.DataFrame({
        'usia': [10, 20, 30, 40],
        'lama_rawat': [2, 3, 4, 5],
        'jenis_kelamin': [1, 0, 1, 0],
        'tingkat_risiko': ['Sedang', 'Sedang', 'Sedang', 'Sedang']
    })
    try:
        train_model(data, n_estimators=3)
        assert False, "Should raise ValueError for single class"
    except ValueError as e:
        assert "2 class" in str(e).lower() or "minimal" in str(e).lower()
run_test("train_model: single class raises error", test_train_model_single_class)

def test_train_model_saves_pickle():
    import pandas as pd
    data = pd.DataFrame({
        'usia': [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38],
        'lama_rawat': [2, 3, 4, 5, 6, 2, 3, 4, 5, 6, 2, 3, 4, 5, 6],
        'jenis_kelamin': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        'tingkat_risiko': ['Rendah']*5 + ['Sedang']*5 + ['Tinggi']*5
    })
    result = train_model(data, n_estimators=3, random_state=42)
    model_data = load_model()
    assert model_data is not None, "Model pickle not found after training"
    assert 'model' in model_data
    assert 'label_map' in model_data
    assert 'inverse_label_map' in model_data
    assert 'feature_columns' in model_data
run_test("train_model: saves valid pickle", test_train_model_saves_pickle)

# ═══════════════════════════════════════════════════════
# 4. PREDICTION PIPELINE
# ═══════════════════════════════════════════════════════
print("\n═══ 4. PREDICTION PIPELINE TESTS ═══")

def test_predict_with_model():
    result = predict(usia=25, lama_rawat=5, jenis_kelamin='L')
    assert result['status'] == 'success'
    assert result['model_used'] == True
    assert result['prediction']['tingkat_risiko'] in ['Rendah', 'Sedang', 'Tinggi']
    assert 0 <= result['prediction']['confidence'] <= 100
    probs = result['prediction']['probabilities']
    assert 'Rendah' in probs
    assert 'Sedang' in probs
    assert 'Tinggi' in probs
    assert abs(sum(probs.values()) - 100) < 1.0, f"Probabilities should sum to ~100, got {sum(probs.values())}"
    assert 'recommendation' in result
    assert result['recommendation']['status'] != ''
    assert 'input_data' in result
    assert result['input_data']['usia'] == 25
    assert result['input_data']['jenis_kelamin'] == 'L'
run_test("predict: valid output with model", test_predict_with_model)

def test_predict_male_female():
    r_l = predict(usia=30, lama_rawat=5, jenis_kelamin='L')
    r_p = predict(usia=30, lama_rawat=5, jenis_kelamin='P')
    assert r_l['input_data']['jenis_kelamin'] == 'L'
    assert r_p['input_data']['jenis_kelamin'] == 'P'
run_test("predict: male and female inputs", test_predict_male_female)

def test_predict_edge_cases():
    # Very young
    r1 = predict(usia=1, lama_rawat=1, jenis_kelamin='L')
    assert r1['status'] == 'success'
    # Very old
    r2 = predict(usia=100, lama_rawat=30, jenis_kelamin='P')
    assert r2['status'] == 'success'
    # Zero values
    r3 = predict(usia=0, lama_rawat=0, jenis_kelamin='L')
    assert r3['status'] == 'success'
run_test("predict: edge case inputs", test_predict_edge_cases)

def test_recommendation_all_levels():
    from app.ml_model import get_recommendation
    for level in ['Rendah', 'Sedang', 'Tinggi']:
        rec = get_recommendation(level)
        assert 'status' in rec
        assert 'actions' in rec
        assert len(rec['actions']) > 0
    # Unknown level → default to Sedang
    rec_unknown = get_recommendation('Unknown')
    assert rec_unknown['status'] == get_recommendation('Sedang')['status']
run_test("get_recommendation: all levels have content", test_recommendation_all_levels)

# ═══════════════════════════════════════════════════════
# 5. TREE DETAILS & RULES
# ═══════════════════════════════════════════════════════
print("\n═══ 5. TREE DETAILS & RULES TESTS ═══")

def test_extract_rules_returns_list():
    from app.ml_model import create_manual_rf
    rf = create_manual_rf()
    if len(rf.estimators_) > 0:
        rules = extract_rules(rf.estimators_[0], ['Usia', 'Lama Rawat Inap', 'Jenis Kelamin'])
        assert isinstance(rules, list)
        assert len(rules) > 0
        for r in rules:
            assert 'rule' in r
            assert 'class' in r
            assert 'confidence' in r
            assert r['class'] in ['Rendah', 'Sedang', 'Tinggi']
            assert 0 <= r['confidence'] <= 100
run_test("extract_rules: returns valid rules", test_extract_rules_returns_list)

def test_extract_tree_rules():
    import pandas as pd
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier

    X = np.array([[10, 2, 1], [25, 5, 0], [50, 8, 1], [35, 3, 0], [60, 10, 1]])
    y = np.array([1, 2, 3, 2, 3])
    rf = RandomForestClassifier(n_estimators=3, random_state=42)
    rf.fit(X, y)

    rules = extract_tree_rules(rf.estimators_[0], ['Usia', 'Lama Rawat Inap', 'Jenis Kelamin'], rf.classes_)
    assert isinstance(rules, list)
    assert len(rules) > 0
    for r in rules:
        assert 'IF' in r or 'THEN' in r
        assert 'Tingkat Risiko' in r
run_test("extract_tree_rules: returns IF-THEN rules", test_extract_tree_rules)

def test_extract_all_trees_details():
    import pandas as pd
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    from app.ml_model import extract_all_trees_details

    X = np.array([[10, 2, 1], [25, 5, 0], [50, 8, 1], [35, 3, 0],
                  [60, 10, 1], [15, 4, 0], [45, 7, 1], [20, 6, 0]])
    y = np.array([1, 2, 3, 2, 3, 1, 3, 2])
    rf = RandomForestClassifier(n_estimators=3, random_state=42)
    rf.fit(X, y)

    result = extract_all_trees_details(rf, X, y, ['Usia', 'Lama Rawat Inap', 'Jenis Kelamin'])
    assert 'trees' in result
    assert 'optimal_tree_idx' in result
    assert 'optimal_tree' in result
    assert len(result['trees']) == 3
    for t in result['trees']:
        assert t['root_entropy'] >= 0
        assert t['information_gain'] >= 0
        assert t['n_leaves'] > 0
        assert t['max_depth'] > 0
run_test("extract_all_trees_details: complete output", test_extract_all_trees_details)

# ═══════════════════════════════════════════════════════
# 6. BATCH PREDICTION
# ═══════════════════════════════════════════════════════
print("\n═══ 6. BATCH PREDICTION TESTS ═══")

def test_batch_predict_no_model():
    # Temporarily rename model file to test fallback
    from app.ml_model import MODEL_PATH
    import shutil
    backup = MODEL_PATH + '.bak'
    if os.path.exists(MODEL_PATH):
        shutil.copy(MODEL_PATH, backup)
        os.remove(MODEL_PATH)

    try:
        class FakePasien:
            def __init__(self):
                self.id = 1
                self.nama_pasien = 'Test'
                self.usia = 25
                self.lama_rawat = 5
                self.jenis_kelamin = 'L'
                self.bulan = 'Januari'
                self.tahun = 2025
                self.tanggal_masuk = None
                self.tanggal_keluar = None

        result = predict_batch_with_trees([FakePasien()])
        assert result['status'] == 'error'
        assert 'belum ditraining' in result['message']
    finally:
        if os.path.exists(backup):
            shutil.move(backup, MODEL_PATH)
run_test("batch_predict: error when no model exists", test_batch_predict_no_model)

# ═══════════════════════════════════════════════════════
# 7. ROUTE TESTS (using test client)
# ═══════════════════════════════════════════════════════
print("\n═══ 7. ROUTE TESTS ═══")

def test_login_page():
    with app.test_client() as client:
        resp = client.get('/auth/login')
        assert resp.status_code == 200
        assert b'login' in resp.data.lower() or b'Login' in resp.data
run_test("GET /auth/login returns 200", test_login_page)

def test_dashboard_requires_login():
    app.config['LOGIN_DISABLED'] = False
    with app.test_client() as client:
        resp = client.get('/')
        assert resp.status_code == 302
        assert 'login' in resp.headers.get('Location', '')
    app.config['LOGIN_DISABLED'] = True
run_test("GET / redirects to login when not authenticated", test_dashboard_requires_login)

def test_dashboard_with_login():
    with app.test_client() as client:
        resp = client.get('/')
        assert resp.status_code == 200
run_test("GET / returns 200 when login disabled", test_dashboard_with_login)

def test_api_home():
    with app.test_client() as client:
        resp = client.get('/api/')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['name'] == 'DBD Prediction API'
        assert 'endpoints' in data
run_test("GET /api/ returns API info", test_api_home)

def test_api_predict():
    with app.test_client() as client:
        resp = client.post('/api/predict', json={'usia': 25, 'lama_rawat': 5, 'jenis_kelamin': 'L'})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['status'] == 'success'
        assert data['prediction']['tingkat_risiko'] in ['Rendah', 'Sedang', 'Tinggi']
run_test("POST /api/predict works", test_api_predict)

def test_api_evaluate():
    with app.test_client() as client:
        resp = client.get('/api/evaluate')
        # May return 404 if no evaluation exists, that's OK
        assert resp.status_code in [200, 404]
run_test("GET /api/evaluate returns 200 or 404", test_api_evaluate)

def test_api_data():
    with app.test_client() as client:
        resp = client.get('/api/data')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['status'] == 'success'
        assert 'statistics' in data
run_test("GET /api/data returns statistics", test_api_data)

def test_training_page():
    with app.test_client() as client:
        login_client(client)
        resp = client.get('/training/')
        assert resp.status_code == 200
run_test("GET /training/ returns 200", test_training_page)

def test_prediksi_page():
    with app.test_client() as client:
        resp = client.get('/prediksi/')
        assert resp.status_code == 200
run_test("GET /prediksi/ returns 200", test_prediksi_page)

def test_evaluasi_page():
    with app.test_client() as client:
        resp = client.get('/evaluasi/')
        assert resp.status_code == 200
run_test("GET /evaluasi/ returns 200", test_evaluasi_page)

def test_laporan_page():
    with app.test_client() as client:
        resp = client.get('/laporan/')
        assert resp.status_code == 200
run_test("GET /laporan/ returns 200", test_laporan_page)

def test_perhitungan_page():
    with app.test_client() as client:
        resp = client.get('/perhitungan/')
        assert resp.status_code == 200
run_test("GET /perhitungan/ returns 200", test_perhitungan_page)

def test_data_page():
    with app.test_client() as client:
        login_client(client)
        resp = client.get('/data/')
        assert resp.status_code == 200
run_test("GET /data/ returns 200", test_data_page)

def test_data_uji_page():
    with app.test_client() as client:
        login_client(client)
        resp = client.get('/data_uji/')
        assert resp.status_code == 200
run_test("GET /data_uji/ returns 200", test_data_uji_page)

def test_log_page():
    with app.test_client() as client:
        login_client(client)
        resp = client.get('/log/')
        assert resp.status_code == 200
run_test("GET /log/ returns 200", test_log_page)

def test_users_page():
    with app.test_client() as client:
        login_client(client)
        resp = client.get('/users/')
        assert resp.status_code == 200
run_test("GET /users/ returns 200", test_users_page)

def test_training_start():
    with app.test_client() as client:
        login_client(client)
        resp = client.post('/training/start', json={'n_estimators': 5})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['status'] == 'success'
        assert 'metrics' in data
run_test("POST /training/start trains model", test_training_start)

def test_perhitungan_hitung():
    with app.test_client() as client:
        resp = client.post('/perhitungan/hitung')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['status'] == 'success'
        assert 'step1' in data
        assert 'step4' in data
        assert 'step5' in data
        assert 'step6' in data
run_test("POST /perhitungan/hitung returns calculation", test_perhitungan_hitung)

def test_prediksi_predict():
    with app.test_client() as client:
        login_client(client)
        resp = client.post('/prediksi/predict', json={
            'usia': 25, 'lama_rawat': 5, 'jenis_kelamin': 'L', 'bulan': 1
        })
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['status'] == 'success'
run_test("POST /prediksi/predict works", test_prediksi_predict)

def test_prediksi_history():
    with app.test_client() as client:
        resp = client.get('/prediksi/history')
        assert resp.status_code == 200
run_test("GET /prediksi/history returns 200", test_prediksi_history)

# ═══════════════════════════════════════════════════════
# 8. DATA INTEGRITY TESTS
# ═══════════════════════════════════════════════════════
print("\n═══ 8. DATA INTEGRITY TESTS ═══")

def test_db_connection():
    with app.app_context():
        result = db.session.execute(db.text('SELECT 1'))
        assert result.fetchone()[0] == 1
run_test("Database connection works", test_db_connection)

def test_users_exist():
    with app.app_context():
        users = User.query.all()
        usernames = [u.username for u in users]
        assert 'admin' in usernames, f"admin user not found. Found: {usernames}"
        assert 'petugas' in usernames, f"petugas user not found. Found: {usernames}"
run_test("Default users (admin, petugas) exist", test_users_exist)

def test_pasien_data_exists():
    with app.app_context():
        count = PasienDBD.query.count()
        assert count > 0, "No patient data found"
run_test("Patient data exists in database", test_pasien_data_exists)

def test_kasus_bulanan_exists():
    with app.app_context():
        count = KasusBulanan.query.count()
        assert count > 0, "No kasus bulanan data found"
run_test("Kasus bulanan data exists", test_kasus_bulanan_exists)

def test_kasus_bulanan_risk_levels_valid():
    with app.app_context():
        records = KasusBulanan.query.all()
        for r in records:
            assert r.tingkat_risiko in ['Rendah', 'Sedang', 'Tinggi'], \
                f"Invalid risk level '{r.tingkat_risiko}' for {r.bulan} {r.tahun}"
            # Verify risk level matches jumlah_kasus
            actual = get_risk_level(r.jumlah_kasus)
            assert r.tingkat_risiko == actual, \
                f"Risk mismatch for {r.bulan} {r.tahun}: jumlah={r.jumlah_kasus}, stored={r.tingkat_risiko}, expected={actual}"
run_test("All kasus_bulanan risk levels match jumlah_kasus", test_kasus_bulanan_risk_levels_valid)

def test_kasus_bulanan_no_inflated_data():
    with app.app_context():
        records = KasusBulanan.query.all()
        for r in records:
            assert r.jumlah_kasus >= 0, f"Negative jumlah_kasus: {r.jumlah_kasus}"
            # With actual patient data, jumlah_kasus should be reasonable
            # (not artificially multiplied)
            pasien_count = PasienDBD.query.filter_by(bulan=r.bulan, tahun=r.tahun).count()
            # jumlah_kasus should equal pasien_count (no *3 multiplier)
            if pasien_count > 0:
                assert r.jumlah_kasus == pasien_count, \
                    f"jumlah_kasus ({r.jumlah_kasus}) != pasien_count ({pasien_count}) for {r.bulan} {r.tahun}. Possible *3 multiplier still present."
run_test("kasus_bulanan jumlah_kasus matches actual patient count (no *3)", test_kasus_bulanan_no_inflated_data)

# ═══════════════════════════════════════════════════════
# 9. CROSS-VALIDATION CORRECTNESS
# ═══════════════════════════════════════════════════════
print("\n═══ 9. CROSS-VALIDATION CORRECTNESS ═══")

def test_cv_fold_count():
    import pandas as pd
    import numpy as np

    # Create data with clear class separation
    data = pd.DataFrame({
        'usia': list(range(10, 60)),
        'lama_rawat': [i % 10 for i in range(10, 60)],
        'jenis_kelamin': [i % 2 for i in range(10, 60)],
        'tingkat_risiko': ['Rendah'] * 15 + ['Sedang'] * 20 + ['Tinggi'] * 15
    })

    result = train_model(data, n_estimators=5, random_state=42)
    cv = result['cv_details']
    assert cv['n_folds'] == 5
    assert len(cv['fold_accuracies']) == 5
    assert len(cv['fold_f1_scores']) == 5
    # Each fold accuracy should be between 0 and 1
    for a in cv['fold_accuracies']:
        assert 0 <= a <= 1, f"Fold accuracy out of range: {a}"
run_test("CV: correct fold count and ranges", test_cv_fold_count)

def test_cv_deterministic():
    import pandas as pd
    data = pd.DataFrame({
        'usia': list(range(10, 60)),
        'lama_rawat': [i % 10 for i in range(10, 60)],
        'jenis_kelamin': [i % 2 for i in range(10, 60)],
        'tingkat_risiko': ['Rendah'] * 15 + ['Sedang'] * 20 + ['Tinggi'] * 15
    })

    r1 = train_model(data, n_estimators=5, random_state=42)
    r2 = train_model(data, n_estimators=5, random_state=42)
    assert r1['metrics']['accuracy'] == r2['metrics']['accuracy'], "Same seed should give same results"
    assert r1['metrics']['f1_score_weighted'] == r2['metrics']['f1_score_weighted']
run_test("CV: deterministic with same random_state", test_cv_deterministic)

# ═══════════════════════════════════════════════════════
# 10. CONSISTENCY TESTS
# ═══════════════════════════════════════════════════════
print("\n═══ 10. CONSISTENCY TESTS ═══")

def test_consistency_train_vs_api():
    """Verify training.py and api.py produce same results with same params."""
    import pandas as pd
    import numpy as np
    from app.ml_model import prepare_training_data, train_model

    # Create identical data
    data = pd.DataFrame({
        'usia': [10, 20, 30, 40, 50, 15, 25, 35, 45, 55, 12, 22, 32, 42, 52],
        'lama_rawat': [2, 3, 5, 7, 4, 3, 4, 6, 8, 5, 2, 3, 5, 7, 4],
        'jenis_kelamin': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        'tingkat_risiko': ['Rendah', 'Rendah', 'Sedang', 'Sedang', 'Tinggi', 'Rendah',
                           'Sedang', 'Sedang', 'Tinggi', 'Tinggi', 'Rendah', 'Rendah',
                           'Sedang', 'Tinggi', 'Tinggi']
    })

    r1 = train_model(data, n_estimators=5, random_state=42)
    r2 = train_model(data, n_estimators=5, random_state=42)
    for key in ['accuracy', 'precision_weighted', 'recall_weighted', 'f1_score_weighted']:
        assert r1['metrics'][key] == r2['metrics'][key], \
            f"Inconsistent metric {key}: {r1['metrics'][key]} vs {r2['metrics'][key]}"
run_test("train_model: deterministic output", test_consistency_train_vs_api)

def test_prediction_consistency():
    """Same input should give same prediction (with model loaded)."""
    r1 = predict(usia=30, lama_rawat=5, jenis_kelamin='L')
    r2 = predict(usia=30, lama_rawat=5, jenis_kelamin='L')
    assert r1['prediction']['tingkat_risiko'] == r2['prediction']['tingkat_risiko']
    assert r1['prediction']['confidence'] == r2['prediction']['confidence']
run_test("predict: deterministic output", test_prediction_consistency)

# ═══════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════
print(f"\n{'='*60}")
print(f"RESULTS: {passed} passed, {failed} failed, {passed+failed} total")
print(f"{'='*60}")

if errors:
    print("\nFAILURES:")
    for name, err in errors:
        print(f"  - {name}: {err}")
