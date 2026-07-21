"""
=====================================================
SISTEM PREDIKSI PENYEBARAN DBD - FULL PYTHON
RSUD Lubuk Basung - Kabupaten Agam
Algoritma: Random Forest (Scikit-learn)
=====================================================

Jalankan file ini untuk memulai aplikasi:
    python run.py

Web akan otomatis terbuka di browser!
"""

import os
import sys

# Fix Windows deadlock issue with NumPy/OpenBLAS threading
# Must be set BEFORE importing numpy/scipy/sklearn
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'

import webbrowser
import threading
from app import create_app

# Configuration
HOST = '127.0.0.1'
PORT = 5000
DEBUG = True

def open_browser():
    """Buka browser otomatis setelah server siap"""
    webbrowser.open(f'http://{HOST}:{PORT}')

if __name__ == '__main__':
    print("=" * 60)
    print("🏥 SISTEM PREDIKSI PENYEBARAN DBD")
    print("📍 RSUD Lubuk Basung - Kabupaten Agam")
    print("🔬 Algoritma: Random Forest")
    print("=" * 60)
    print()
    print(f"🌐 Server berjalan di: http://{HOST}:{PORT}")
    print("📝 Tekan Ctrl+C untuk menghentikan server")
    print("=" * 60)
    
    # Buka browser otomatis setelah 1.5 detik
    threading.Timer(1.5, open_browser).start()
    
    # Jalankan Flask app
    app = create_app()
    app.run(host=HOST, port=PORT, debug=DEBUG)
