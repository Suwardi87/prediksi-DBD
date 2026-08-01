"""
Prediction Routes
Prediksi individual (CEK HASIL) + batch dengan label Rendah/Sedang/Tinggi.
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models import HasilPrediksi
from app import db
from app.ml_model import predict, BULAN_NAMES, get_risk_level, get_recommendation
from datetime import datetime
import openpyxl

prediksi_bp = Blueprint('prediksi', __name__)

_ENC = {'Rendah': 1, 'Sedang': 2, 'Tinggi': 3}


def _get_best_tree_rules():
    """Baca rules + thresholds pohon terbaik dari Excel."""
    from app.routes.perhitungan import (
        EXCEL_PATH, POHON_NAMES,
        _read_pohon_thresholds, _read_bootstrap_from_sheet,
        _read_penentuan_pohon_terbaik, _majority_class,
    )
    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
    penentuan = _read_penentuan_pohon_terbaik(wb)
    if penentuan:
        best_entry = max(penentuan, key=lambda x: x.get('r2') or -999999)
        best_idx = best_entry.get('no', 6) - 1
    else:
        best_idx = 5

    pname = POHON_NAMES[best_idx]
    t1, t2 = _read_pohon_thresholds(wb, pname)
    bs = _read_bootstrap_from_sheet(wb, pname)
    left = [s for s in bs if float(s.get('jumlah_kasus', 0)) < t1]
    mid = [s for s in bs if t1 <= float(s.get('jumlah_kasus', 0)) <= t2]
    right = [s for s in bs if float(s.get('jumlah_kasus', 0)) > t2]
    l_cls = _majority_class(left)[0] if left else 'Sedang'
    m_cls = _majority_class(mid)[0] if mid else 'Sedang'
    r_cls = _majority_class(right)[0] if right else 'Tinggi'

    return {
        'pohon': best_idx + 1,
        't1': round(t1, 2) if t1 else 0,
        't2': round(t2, 2) if t2 else 0,
        'left_cls': l_cls,
        'mid_cls': m_cls,
        'right_cls': r_cls,
        'left_n': len(left),
        'mid_n': len(mid),
        'right_n': len(right),
        'left_counts': {k: v for k, v in _majority_class(left)[1].items() if v > 0} if left else {},
        'mid_counts': {k: v for k, v in _majority_class(mid)[1].items() if v > 0} if mid else {},
        'right_counts': {k: v for k, v in _majority_class(right)[1].items() if v > 0} if right else {},
    }


@prediksi_bp.route('/')
@login_required
def index():
    """Halaman prediksi"""
    return render_template('prediksi/index.html')


@prediksi_bp.route('/cek', methods=['POST'])
@login_required
def cek_prediksi():
    """Cek prediksi individual menggunakan rules Pohon Terbaik."""
    try:
        data = request.get_json() or {}
        jumlah_kasus = int(data.get('jumlah_kasus', 0))
        usia = int(data.get('usia', 0))
        jk = data.get('jenis_kelamin', 'L')
        lama_rawat = int(data.get('lama_rawat', 0))
        nama = data.get('nama', '')

        rules_info = _get_best_tree_rules()
        t1 = rules_info['t1']
        t2 = rules_info['t2']

        if jumlah_kasus < t1:
            risk = rules_info['left_cls']
            branch = 'Kiri'
            branch_condition = f'Jumlah Kasus < {t1}'
        elif jumlah_kasus <= t2:
            risk = rules_info['mid_cls']
            branch = 'Tengah'
            branch_condition = f'{t1} ≤ Jumlah Kasus ≤ {t2}'
        else:
            risk = rules_info['right_cls']
            branch = 'Kanan'
            branch_condition = f'Jumlah Kasus > {t2}'

        recommendation = get_recommendation(risk)
        risk_enc = _ENC.get(risk, 2)

        risk_colors = {'Rendah': '#22c55e', 'Sedang': '#f59e0b', 'Tinggi': '#ef4444'}

        return jsonify({
            'status': 'success',
            'nama': nama,
            'usia': usia,
            'jenis_kelamin': jk,
            'lama_rawat': lama_rawat,
            'jumlah_kasus': jumlah_kasus,
            'tingkat_risiko': risk,
            'risk_enc': risk_enc,
            'risk_color': risk_colors.get(risk, '#6b7280'),
            'branch': branch,
            'branch_condition': branch_condition,
            'rules': [
                f'IF Jumlah Kasus < {t1} THEN Risiko = {rules_info["left_cls"]}',
                f'IF {t1} ≤ Jumlah Kasus ≤ {t2} THEN Risiko = {rules_info["mid_cls"]}',
                f'IF Jumlah Kasus > {t2} THEN Risiko = {rules_info["right_cls"]}',
            ],
            'pohon': rules_info['pohon'],
            'thresholds': [t1, t2],
            'branch_info': {
                'left': {'cls': rules_info['left_cls'], 'n': rules_info['left_n'], 'counts': rules_info['left_counts']},
                'mid': {'cls': rules_info['mid_cls'], 'n': rules_info['mid_n'], 'counts': rules_info['mid_counts']},
                'right': {'cls': rules_info['right_cls'], 'n': rules_info['right_n'], 'counts': rules_info['right_counts']},
            },
            'recommendation': recommendation,
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@prediksi_bp.route('/predict', methods=['POST'])
@login_required
def make_prediction():
    """Buat prediksi — fitur: Usia, Lama Rawat, Jenis Kelamin, (Jumlah Kasus)"""
    try:
        data = request.get_json() or {}
        usia = data.get('usia', 25)
        lama_rawat = data.get('lama_rawat', 3)
        jenis_kelamin = data.get('jenis_kelamin', 'L')
        jumlah_kasus = data.get('jumlah_kasus')

        try:
            usia = int(usia)
            if usia < 0 or usia > 120:
                return jsonify({'status': 'error', 'message': 'Usia harus antara 0-120 tahun'}), 400
        except (ValueError, TypeError):
            return jsonify({'status': 'error', 'message': 'Usia harus berupa angka'}), 400

        try:
            lama_rawat = int(lama_rawat)
            if lama_rawat < 1:
                return jsonify({'status': 'error', 'message': 'Lama rawat minimal 1 hari'}), 400
        except (ValueError, TypeError):
            return jsonify({'status': 'error', 'message': 'Lama rawat harus berupa angka'}), 400

        if jenis_kelamin not in ('L', 'P'):
            return jsonify({'status': 'error', 'message': 'Jenis kelamin harus L atau P'}), 400

        if jumlah_kasus is not None:
            try:
                jumlah_kasus = int(jumlah_kasus)
                if jumlah_kasus < 0:
                    return jsonify({'status': 'error', 'message': 'Jumlah kasus tidak boleh negatif'}), 400
            except (ValueError, TypeError):
                return jsonify({'status': 'error', 'message': 'Jumlah kasus harus berupa angka'}), 400

        bulan = data.get('bulan', datetime.now().month)

        result = predict(
            usia=usia,
            lama_rawat=lama_rawat,
            jenis_kelamin=jenis_kelamin,
            jumlah_kasus=jumlah_kasus
        )

        bulan_nama = str(bulan)
        try:
            bulan_int = int(bulan)
            if 1 <= bulan_int <= 12:
                bulan_nama = BULAN_NAMES[bulan_int - 1]
            else:
                bulan_nama = BULAN_NAMES[datetime.now().month - 1]
        except (ValueError, TypeError):
            bulan_nama = str(bulan) if bulan else BULAN_NAMES[datetime.now().month - 1]

        prediksi = HasilPrediksi(
            tanggal_prediksi=datetime.now(),
            bulan_prediksi=bulan_nama,
            tahun_prediksi=datetime.now().year,
            jumlah_kasus_prediksi=None,
            tingkat_risiko_prediksi=result['prediction']['tingkat_risiko'],
            confidence_score=result['prediction']['confidence'],
            model_version='1.0.0',
            created_by=current_user.id
        )

        db.session.add(prediksi)
        db.session.commit()

        return jsonify(result)

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@prediksi_bp.route('/history')
@login_required
def history():
    """Riwayat prediksi"""
    predictions = HasilPrediksi.query.order_by(HasilPrediksi.tanggal_prediksi.desc()).limit(50).all()
    return render_template('prediksi/history.html', predictions=predictions)

@prediksi_bp.route('/batch', methods=['GET', 'POST'])
@login_required
def batch_predict():
    """Jalankan prediksi untuk sampel dari setiap bulan (variasi kasus)"""
    try:
        from app.models import PasienDBD, KasusBulanan
        from app.ml_model import predict_batch_with_trees

        all_months = KasusBulanan.query.order_by(KasusBulanan.tahun, KasusBulanan.bulan).all()
        pasiens = []
        seen = set()
        for kb in all_months:
            sample = PasienDBD.query.filter_by(bulan=kb.bulan, tahun=kb.tahun).first()
            if sample and sample.id not in seen:
                pasiens.append(sample)
                seen.add(sample.id)
            if len(pasiens) >= 10:
                break

        if len(pasiens) < 10:
            pasiens = PasienDBD.query.order_by(PasienDBD.id.asc()).limit(10).all()

        if not pasiens:
            return jsonify({'status': 'error', 'message': 'Data pasien kosong.'}), 404

        result = predict_batch_with_trees(pasiens)
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
