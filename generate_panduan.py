#!/usr/bin/env python3
"""
Generate Panduan PDF - Sistem Prediksi DBD Random Forest
"""
from fpdf import FPDF
import os

PAGE_W = 210  # A4 width
MARGIN = 10
USABLE = PAGE_W - 2 * MARGIN  # 190mm usable width


class PanduanPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('Helvetica', 'I', 8)
            self.set_text_color(150, 150, 150)
            self.set_xy(MARGIN, 10)
            self.cell(USABLE, 5, 'Panduan Sistem Prediksi DBD - Random Forest',
                      align='R')
            self.set_draw_color(200, 200, 200)
            self.line(MARGIN, 17, PAGE_W - MARGIN, 17)
            self.set_xy(MARGIN, 19)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Halaman {self.page_no()}', align='C')

    # ── Text helpers ──

    def _reset_x(self):
        self.set_x(MARGIN)

    def chapter_title(self, title):
        self._reset_x()
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(0, 100, 0)
        self.multi_cell(USABLE, 12, title)
        self.set_draw_color(0, 100, 0)
        self.line(MARGIN, self.get_y(), PAGE_W - MARGIN, self.get_y())
        self.ln(4)
        self.set_text_color(0, 0, 0)

    def section_title(self, title):
        self._reset_x()
        self.set_font('Helvetica', 'B', 13)
        self.set_text_color(0, 70, 150)
        self.multi_cell(USABLE, 10, title)
        self.set_text_color(0, 0, 0)
        self.ln(1)

    def sub_title(self, title):
        self._reset_x()
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(60, 60, 60)
        self.multi_cell(USABLE, 8, title)
        self.set_text_color(0, 0, 0)

    def body(self, text):
        self._reset_x()
        self.set_font('Helvetica', '', 11)
        self.multi_cell(USABLE, 6, text)
        self.ln(2)

    def bullet(self, text):
        self.set_font('Helvetica', '', 11)
        self.set_x(MARGIN + 5)
        indent_w = USABLE - 5
        self.multi_cell(indent_w, 6, f'- {text}')
        self.ln(1)

    def code(self, text):
        self._reset_x()
        self.set_font('Courier', '', 8)
        self.set_fill_color(240, 240, 240)
        self.set_text_color(50, 50, 50)
        self.multi_cell(USABLE, 4.5, text, border=1, fill=True)
        self.ln(2)
        self.set_text_color(0, 0, 0)

    # ── Table helpers ──

    def table(self, header_cols, rows, col_widths):
        """Build a complete table in one call."""
        total = sum(col_widths)
        if total > USABLE:
            # Scale down
            scale = USABLE / total
            col_widths = [w * scale for w in col_widths]

        # Header
        self._reset_x()
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(0, 100, 0)
        self.set_text_color(255, 255, 255)
        for i, col in enumerate(header_cols):
            self.cell(col_widths[i], 8, str(col), border=1, align='C', fill=True)
        self.ln()

        # Rows
        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', '', 10)
        for row in rows:
            self._reset_x()
            for i, val in enumerate(row):
                self.cell(col_widths[i], 7, str(val), border=1, align='C')
            self.ln()
        self.ln(2)

    def info_box(self, title, text):
        self._reset_x()
        self.set_fill_color(230, 245, 255)
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(0, 70, 150)
        self.multi_cell(USABLE, 7, title, border=1, fill=True)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(40, 40, 40)
        self._reset_x()
        self.multi_cell(USABLE, 6, text, border=1, fill=True)
        self.ln(3)
        self.set_text_color(0, 0, 0)

    def warn_box(self, title, text):
        self._reset_x()
        self.set_fill_color(255, 245, 230)
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(200, 80, 0)
        self.multi_cell(USABLE, 7, title, border=1, fill=True)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(60, 40, 0)
        self._reset_x()
        self.multi_cell(USABLE, 6, text, border=1, fill=True)
        self.ln(3)
        self.set_text_color(0, 0, 0)


def generate():
    pdf = PanduanPDF(format='A4')
    pdf.set_margins(MARGIN, MARGIN, MARGIN)
    pdf.set_auto_page_break(auto=True, margin=22)
    pdf.add_page()

    # ════════ COVER ════════
    pdf.ln(30)
    pdf.set_font('Helvetica', 'B', 28)
    pdf.set_text_color(0, 80, 0)
    pdf.cell(0, 15, 'PANDUAN SISTEM', align='C')
    pdf.ln(15)
    pdf.cell(0, 15, 'PREDIKSI DBD', align='C')
    pdf.ln(15)
    pdf.set_font('Helvetica', '', 18)
    pdf.set_text_color(0, 100, 200)
    pdf.cell(0, 12, 'Metode Random Forest', align='C')
    pdf.ln(15)
    pdf.set_draw_color(0, 100, 0)
    pdf.set_line_width(0.8)
    mid = PAGE_W / 2
    pdf.line(mid - 50, pdf.get_y(), mid + 50, pdf.get_y())
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 7, 'RSUD Lubuk Basung', align='C')
    pdf.ln(7)
    pdf.cell(0, 7, 'Tahun 2025', align='C')
    pdf.ln(15)
    pdf.set_font('Helvetica', 'I', 10)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 6, 'Instalasi, Penggunaan, Metodologi, dan Testing', align='C')

    # ════════ DAFTAR ISI ════════
    pdf.add_page()
    pdf.chapter_title('Daftar Isi')
    isi = [
        '1. Pengenalan Sistem',
        '2. Metodologi Random Forest (Bab IV)',
        '3. Pengelompokan Data (Tabel 4.1 & 4.2)',
        '4. Hasil Evaluasi Model',
        '5. Instalasi & Menjalankan Program',
        '6. Login & Hak Akses',
        '7. Cara Menggunakan Sistem',
        '8. Cara Testing',
        '9. Keamanan Sistem',
        '10. File Excel & Database',
        '11. Troubleshooting',
    ]
    for item in isi:
        pdf.set_font('Helvetica', '', 12)
        pdf._reset_x()
        pdf.multi_cell(USABLE, 8, item)
        pdf.ln(0)

    # ════════ BAB 1 ════════
    pdf.add_page()
    pdf.chapter_title('1. Pengenalan Sistem')

    pdf.section_title('1.1 Deskripsi')
    pdf.body(
        'Sistem Prediksi DBD adalah aplikasi web yang menggunakan algoritma '
        'Random Forest untuk memprediksi pola penyebaran penyakit Demam '
        'Berdarah Dengue (DBD). Dibangun dengan Python (Flask) dan '
        'mengimplementasikan metodologi Bab IV skripsi.'
    )

    pdf.section_title('1.2 Tujuan')
    pdf.bullet('Memprediksi tingkat risiko (Rendah/Sedang/Tinggi)')
    pdf.bullet('Menampilkan proses perhitungan RF transparan')
    pdf.bullet('Dashboard monitoring kasus DBD bulanan')
    pdf.bullet('Laporan untuk instansi terkait')

    pdf.section_title('1.3 Teknologi')
    pdf.table(
        ['Komponen', 'Teknologi'],
        [
            ['Backend', 'Python 3 + Flask'],
            ['Database', 'MySQL (XAMPP)'],
            ['ML', 'scikit-learn'],
            ['Frontend', 'HTML + CSS + JS'],
            ['Data', 'MS Excel (.xlsx)'],
        ],
        [50, 140]
    )

    pdf.section_title('1.4 Fitur Utama')
    pdf.table(
        ['Fitur', 'Status'],
        [
            ['Dashboard kasus DBD', 'Tersedia'],
            ['Training Random Forest', 'Tersedia'],
            ['Prediksi tingkat risiko', 'Tersedia'],
            ['Perhitungan (entropy, gain)', 'Tersedia'],
            ['Evaluasi (MAE, RMSE, R2)', 'Tersedia'],
            ['Manajemen data pasien', 'Tersedia'],
            ['Manajemen user', 'Tersedia'],
            ['Log aktivitas', 'Tersedia'],
            ['Laporan bulanan', 'Tersedia'],
        ],
        [120, 70]
    )

    # ════════ BAB 2 ════════
    pdf.add_page()
    pdf.chapter_title('2. Metodologi Random Forest')

    pdf.section_title('2.1 Apa itu Random Forest?')
    pdf.body(
        'Random Forest adalah algoritma ensemble yang menggabungkan banyak '
        'pohon keputusan untuk prediksi yang lebih akurat. Bayangkan bertanya '
        'ke 15 orang ahli lalu ambil suara terbanyak.'
    )

    pdf.section_title('2.2 Cara Kerja (5 Langkah)')

    pdf.sub_title('Langkah 1: Bootstrap Sampling')
    pdf.body(
        'Dari 163 data pasien, diambil 15 sampel acak dengan pengembalian. '
        'Tiap sampel 163 data, ada yang muncul berulang.'
    )

    pdf.sub_title('Langkah 2: Pembentukan Pohon')
    pdf.body(
        'Untuk setiap sampel, dibangun satu pohon keputusan. '
        'Menggunakan Entropy dan Information Gain untuk pilih fitur terbaik.'
    )

    pdf.sub_title('Langkah 3: Split 3-Arah')
    pdf.body(
        'Setiap node dipisah jadi 3 cabang:\n'
        '- Kiri: nilai < T1\n'
        '- Tengah: T1 <= nilai <= T2\n'
        '- Kanan: nilai > T2'
    )

    pdf.sub_title('Langkah 4: Voting')
    pdf.body('15 pohon memberi pendapat. Hasil = mayoritas suara.')

    pdf.sub_title('Langkah 5: Evaluasi')
    pdf.body(
        'Tiap pohon dievaluasi MAE, RMSE, R2. '
        'Pohon terbaik dipilih berdasarkan keseimbangan ketiganya.'
    )

    pdf.section_title('2.3 Fitur yang Digunakan')
    pdf.table(
        ['Kode', 'Fitur', 'Tipe'],
        [
            ['X1', 'Usia', 'Numerik'],
            ['X2', 'Lama Rawat Inap', 'Numerik'],
            ['X3', 'Jenis Kelamin', 'Kategorikal'],
            ['X4', 'Jumlah Kasus Perbulan', 'Numerik'],
        ],
        [25, 100, 65]
    )

    # ════════ BAB 3 ════════
    pdf.add_page()
    pdf.chapter_title('3. Pengelompokan Data (Tabel 4.1 & 4.2)')

    pdf.section_title('3.1 Tabel 4.1 - Data Pasien')
    pdf.body(
        'Sumber: 163 pasien DBD RSUD Lubuk Basung tahun 2025 '
        '(Januari - Desember). Kolom: nama, usia, lama rawat, JK, '
        'jumlah kasus per bulan.'
    )

    pdf.section_title('3.2 Tabel 4.2 - Pengelompokan')

    pdf.sub_title('Usia')
    pdf.table(
        ['Kategori', 'Rentang'],
        [
            ['Anak-anak', '0 - 17 tahun'],
            ['Dewasa', '18 - 59 tahun'],
            ['Lansia', '>= 60 tahun'],
        ],
        [95, 95]
    )

    pdf.sub_title('Lama Rawat Inop')
    pdf.table(
        ['Kategori', 'Rentang'],
        [
            ['Singkat', '1 - 2 hari'],
            ['Sedang', '3 - 4 hari'],
            ['Lama', '>= 5 hari'],
        ],
        [95, 95]
    )

    pdf.sub_title('Jumlah Kasus Perbulan (Target)')
    pdf.table(
        ['Risiko', 'Rentang', 'Label'],
        [
            ['Rendah', '1 - 10 kasus', '1'],
            ['Sedang', '11 - 20 kasus', '2'],
            ['Tinggi', '> 20 kasus', '3'],
        ],
        [50, 90, 50]
    )

    pdf.sub_title('Jenis Kelamin')
    pdf.table(
        ['Kode', 'Kategori', 'Encoding'],
        [
            ['L', 'Laki-laki', '1'],
            ['P', 'Perempuan', '0'],
        ],
        [40, 90, 60]
    )

    pdf.info_box(
        'Penting:',
        'Threshold (1-10/11-20/>20) sudah disinkronkan ke program, '
        'Excel, dan database. Jangan ubah tanpa seizin pembimbing.'
    )

    # ════════ BAB 4 ════════
    pdf.add_page()
    pdf.chapter_title('4. Hasil Evaluasi Model')

    pdf.section_title('4.1 Pohon Terbaik: Pohon 5')
    pdf.body(
        'Dari 15 pohon, Pohon 5 dipilih karena keseimbangan MAE, RMSE, '
        'dan R2 terbaik.'
    )
    pdf.table(
        ['Metrik', 'Nilai', 'Keterangan'],
        [
            ['MAE', '20.60', 'Kesalahan absolut rata-rata'],
            ['RMSE', '0.742', 'Akar dari MSE'],
            ['R2', '0.993', 'Koefisien determinasi'],
        ],
        [40, 40, 110]
    )

    pdf.section_title('4.2 Aturan Pohon 5')
    pdf.code(
        'IF Jumlah Kasus < 12.60 THEN Rendah\n'
        'IF 12.60 <= Jumlah Kasus <= 29.21 THEN Sedang\n'
        'IF Jumlah Kasus > 29.21 THEN Tinggi'
    )

    pdf.section_title('4.3 Evaluasi Final (10 Data Uji)')
    pdf.table(
        ['Metrik', 'Nilai', 'Rumus'],
        [
            ['MAE', '0.7', '7/10'],
            ['RMSE', '0.837', 'Akar(0.7)'],
            ['R2', '0.0789', '1 - 7/7.60'],
        ],
        [35, 35, 120]
    )

    pdf.info_box(
        'Catatan:',
        'R2=0.993 (per pohon) vs R2=0.0789 (final) berbeda karena '
        'memprediksi target berbeda: nilai numerik vs kelas terenkoding.'
    )

    # ════════ BAB 5 ════════
    pdf.add_page()
    pdf.chapter_title('5. Instalasi & Menjalankan')

    pdf.section_title('5.1 Persyaratan')
    pdf.bullet('Python 3.10+')
    pdf.bullet('XAMPP (MySQL)')
    pdf.bullet('pip (Python package manager)')

    pdf.section_title('5.2 Langkah Instalasi')

    pdf.sub_title('1. Install XAMPP')
    pdf.body(
        'Download dari apachefriends.org. Buka XAMPP Control Panel, '
        'klik Start pada MySQL.'
    )

    pdf.sub_title('2. Install Dependencies')
    pdf.code('cd python_app\npip install -r requirements.txt')

    pdf.sub_title('3. Import Database')
    pdf.body('Buat database "db_prediksi_dbd" di phpMyAdmin, lalu import SQL.')
    pdf.code('mysql -u root < db_prediksi_dbd.sql')

    pdf.sub_title('4. Jalankan Aplikasi')
    pdf.code('cd python_app\npython run.py')
    pdf.body('Buka browser: http://localhost:5000')

    pdf.section_title('5.3 SECRET_KEY (Opsional)')
    pdf.code(
        '# Linux/Mac:\n'
        'export SECRET_KEY="kunci-rahasia-anda"\n\n'
        '# Windows PowerShell:\n'
        '$env:SECRET_KEY="kunci-rahasia-anda"'
    )

    pdf.warn_box(
        'Peringatan:',
        'Tanpa SECRET_KEY, sistem pakai dev key. '
        'TIDAK aman untuk production!'
    )

    # ════════ BAB 6 ════════
    pdf.add_page()
    pdf.chapter_title('6. Login & Hak Akses')

    pdf.section_title('6.1 Akun Default')
    pdf.table(
        ['Username', 'Password', 'Role'],
        [
            ['admin', 'admin123', 'Administrator'],
            ['petugas', 'petugas123', 'Petugas'],
        ],
        [45, 60, 85]
    )
    pdf.warn_box(
        'Peringatan:',
        'Ganti password default setelah login pertama! '
        'Minimal 6 karakter.'
    )

    pdf.section_title('6.2 Hak Akses')
    pdf.table(
        ['Fitur', 'Admin', 'Petugas'],
        [
            ['Dashboard', 'Ya', 'Ya'],
            ['Data Pasien', 'Ya', 'Ya'],
            ['Import Excel', 'Ya', 'Ya'],
            ['Training Model', 'Ya', 'Ya'],
            ['Prediksi', 'Ya', 'Ya'],
            ['Perhitungan', 'Ya', 'Ya'],
            ['Evaluasi', 'Ya', 'Ya'],
            ['Manajemen User', 'Ya', 'Tidak'],
            ['Log Aktivitas', 'Ya', 'Tidak'],
        ],
        [90, 50, 50]
    )

    # ════════ BAB 7 ════════
    pdf.add_page()
    pdf.chapter_title('7. Cara Menggunakan Sistem')

    pdf.section_title('7.1 Dashboard')
    pdf.body(
        'Ringkasan kasus DBD per bulan, distribusi risiko, '
        'bulan dengan kasus tertinggi.'
    )

    pdf.section_title('7.2 Training Model')
    pdf.body(
        '1. Buka menu "Training Model"\n'
        '2. Jumlah pohon default: 15 (sesuai Bab IV)\n'
        '3. Klik "Start Training"\n'
        '4. Tunggu hingga selesai\n'
        '5. Hasil evaluasi tampil otomatis'
    )

    pdf.section_title('7.3 Prediksi')
    pdf.body(
        '1. Buka menu "Prediksi Risiko"\n'
        '2. Input: Usia (0-120), Lama Rawat (min 1), JK (L/P)\n'
        '3. Opsional: Jumlah Kasus Perbulan\n'
        '4. Klik "Prediksi"\n'
        '5. Hasil: Risiko + Confidence + Rekomendasi'
    )

    pdf.section_title('7.4 Perhitungan Manual')
    pdf.body(
        'Menampilkan proses RF secara transparan:\n'
        '- Data pasien\n'
        '- Encoding & pengelompokan\n'
        '- Bootstrap sampling (15 sampel)\n'
        '- Pembentukan 15 pohon (entropy, gain)\n'
        '- Evaluasi & pohon terbaik'
    )

    pdf.section_title('7.5 Evaluasi')
    pdf.body(
        'Metrik performa: Accuracy, Precision, Recall, F1, '
        'MAE=0.7, RMSE=0.837, R2=0.0789.'
    )

    pdf.section_title('7.6 Import Excel')
    pdf.body(
        'Menu Data > Import. Upload .xlsx dengan kolom: '
        'Nama, Usia, Lama Rawat, Jenis Kelamin.'
    )

    # ════════ BAB 8 ════════
    pdf.add_page()
    pdf.chapter_title('8. Cara Testing')

    pdf.section_title('8.1 Automated Test (52 Tests)')
    pdf.code('cd python_app\npython -m pytest test_comprehensive.py -v')
    pdf.body('Mencakup:')
    pdf.bullet('Threshold risiko (Tabel 4.2)')
    pdf.bullet('Training (15 pohon, 4 fitur)')
    pdf.bullet('Prediksi (3 dan 4 fitur)')
    pdf.bullet('Evaluasi (MAE, RMSE, R2)')
    pdf.bullet('Semua halaman web')
    pdf.bullet('API dengan autentikasi')
    pdf.bullet('Database connection')

    pdf.section_title('8.2 Manual via Browser')
    pdf.code('cd python_app\npython run.py')
    pdf.body('Buka http://localhost:5000, login: admin/admin123')
    pdf.bullet('Dashboard: threshold baru')
    pdf.bullet('Perhitungan: tabel 1-10/11-20/>20')
    pdf.bullet('Training: default 15 pohon')
    pdf.bullet('Prediksi: validasi input')
    pdf.bullet('Evaluasi: MAE=0.7, RMSE=0.837')
    pdf.bullet('API tanpa login: redirect')

    pdf.section_title('8.3 API Test')
    pdf.code(
        '# Login untuk dapat cookie\n'
        'curl -c c.txt -X POST localhost:5000/auth/login \\\n'
        '  -d "username=admin&password=admin123"\n\n'
        '# Predict dengan cookie\n'
        'curl -b c.txt -X POST localhost:5000/api/predict \\\n'
        '  -H "Content-Type: application/json" \\\n'
        "  -d '{\"usia\":25,\"lama_rawat\":3,\"jk\":\"L\"}'"
    )

    # ════════ BAB 9 ════════
    pdf.add_page()
    pdf.chapter_title('9. Keamanan Sistem')

    pdf.section_title('9.1 Autentikasi')
    pdf.body(
        'Semua halaman & API butuh login. Password disimpan sebagai '
        'hash (werkzeug), bukan plaintext.'
    )

    pdf.section_title('9.2 Role-Based Access')
    pdf.table(
        ['Endpoint', 'Auth', 'Role'],
        [
            ['/dashboard', 'Login', 'Semua'],
            ['/api/train', 'Login', 'Semua'],
            ['/api/predict', 'Login', 'Semua'],
            ['/api/evaluate', 'Login', 'Semua'],
            ['/api/data', 'Login', 'Semua'],
            ['/users', 'Login', 'Admin'],
            ['/log', 'Login', 'Admin'],
        ],
        [65, 40, 85]
    )

    pdf.section_title('9.3 SECRET_KEY')
    pdf.code('export SECRET_KEY="kunci-unik-dan-panjang"')

    pdf.section_title('9.4 Validasi Input')
    pdf.bullet('Usia: angka 0-120')
    pdf.bullet('Lama Rawat: minimal 1 hari')
    pdf.bullet('JK: hanya L atau P')
    pdf.bullet('Password: minimal 6 karakter')
    pdf.bullet('n_estimators: 1-100 (default 15)')

    pdf.section_title('9.5 SQL Injection')
    pdf.body(
        'Sistem pakai ORM (SQLAlchemy). Tidak ada raw SQL. '
        'Aman dari SQL injection.'
    )

    # ════════ BAB 10 ════════
    pdf.add_page()
    pdf.chapter_title('10. File Excel & Database')

    pdf.section_title('10.1 File Excel')
    pdf.table(
        ['File', 'Sheets', 'Status'],
        [
            ['Data DBD 15 Sampel.xlsx', '23', 'Lengkap'],
            ['Data DBD 15 Sampel(try).xlsx', '19', 'Client'],
        ],
        [85, 35, 70]
    )

    pdf.section_title('10.2 Sheet di File Utama (23)')
    pdf.body(
        '1. Data_DBD (163 pasien)\n'
        '2-16. Pohon 1 s/d Pohon 15\n'
        '17. Ringkasan_Perhitungan\n'
        '18. Rules_Semua_Pohon\n'
        '19. Pohon_Terbaik\n'
        '20. Pengujian_Pohon5\n'
        '21. Random_Sampling\n'
        '22. PerhitunganRF\n'
        '23. PenentuanPohonterbaik (R2 override)'
    )

    pdf.section_title('10.3 Database MySQL')
    pdf.table(
        ['Tabel', 'Isi', 'Jumlah'],
        [
            ['users', 'Akun user', '2+'],
            ['pasien_dbd', 'Data pasien', '163'],
            ['kasus_bulanan', 'Kasus per bulan', '12'],
            ['hasil_prediksi', 'Riwayat', 'Variabel'],
            ['model_evaluasi', 'Training', 'Variabel'],
            ['log_aktivitas', 'Log user', 'Variabel'],
        ],
        [55, 85, 50]
    )

    pdf.section_title('10.4 Backup')
    pdf.code(
        '# Export\n'
        'mysqldump -u root db_prediksi_dbd > backup.sql\n\n'
        '# Import\n'
        'mysql -u root db_prediksi_dbd < backup.sql'
    )

    # ════════ BAB 11 ════════
    pdf.add_page()
    pdf.chapter_title('11. Troubleshooting')

    pdf.section_title('11.1 MySQL tidak ditemukan')
    pdf.warn_box(
        'Error MySQL!',
        'Start MySQL di XAMPP Control Panel. Pastikan status hijau.'
    )

    pdf.section_title('11.2 Training gagal - data sedikit')
    pdf.body('Import data Excel dulu via Data > Import.')
    pdf.code('cd python_app && python seed_40_pasien.py')

    pdf.section_title('11.3 Training gagal - 1 class')
    pdf.body(
        'Pastikan ada variasi kasus per bulan (Rendah, Sedang, Tinggi). '
        'Cek tabel KasusBulanan.'
    )

    pdf.section_title('11.4 Prediksi error - feature mismatch')
    pdf.body('Hapus model lama, train ulang:')
    pdf.code(
        'rm python_app/app/models/random_forest_model.pkl\n'
        '# lalu train ulang via web'
    )

    pdf.section_title('11.5 Excel tidak terbaca')
    pdf.body(
        'Pastikan "Data DBD 15 Sampel.xlsx" ada di root project. '
        'Cek nama sheet: Data_DBD, Pohon 1-15.'
    )

    pdf.section_title('11.6 Session hilang setelah restart')
    pdf.body('Set SECRET_KEY via env var (lihat Bab 5.3).')

    pdf.section_title('11.7 Reset Database')
    pdf.code(
        'mysql -u root -e "DROP DATABASE db_prediksi_dbd;"\n'
        'mysql -u root -e "CREATE DATABASE db_prediksi_dbd;"\n'
        'cd python_app && python run.py  # auto-seed'
    )

    # ════════ PENUTUP ════════
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(0, 80, 0)
    pdf.cell(0, 15, '--- SELESAI ---', align='C')
    pdf.ln(15)
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(0, 7,
                   'Dokumen ini menjelaskan sistem Prediksi DBD dengan '
                   'Random Forest. Hubungi developer untuk pertanyaan.',
                   align='C')
    pdf.ln(15)
    pdf.set_font('Helvetica', 'I', 10)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 7, 'Versi: 1.0 | 2025 | RSUD Lubuk Basung', align='C')

    # Save
    output_path = os.path.join(os.path.dirname(__file__),
                               'Panduan_Sistem_Prediksi_DBD.pdf')
    pdf.output(output_path)
    print(f'PDF saved: {output_path}')
    print(f'Pages: {pdf.page_no()}')


if __name__ == '__main__':
    generate()
