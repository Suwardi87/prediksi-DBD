# BAB IV
# ANALISA DAN PERANCANGAN

## 4.1 Analisa Sistem

Analisa sistem merupakan tahap awal yang penting dalam pengembangan sistem informasi. Pada tahap ini dilakukan pengkajian terhadap kebutuhan sistem yang akan dibangun berdasarkan permasalahan yang ada. Sistem yang akan dirancang adalah Sistem Prediksi Penyebaran Penyakit Demam Berdarah Dengue (DBD) pada RSUD Lubuk Basung menggunakan algoritma Random Forest.

Berdasarkan analisa yang telah dilakukan, sistem ini memiliki beberapa kebutuhan fungsional sebagai berikut:

1. Sistem dapat mengelola data pengguna dengan hak akses berbeda (Admin, Petugas, Pimpinan)
2. Sistem dapat mengelola data pasien DBD (tambah, ubah, hapus, lihat)
3. Sistem dapat melakukan import data pasien dari file Excel
4. Sistem dapat melakukan training model Random Forest dengan parameter yang dapat dikonfigurasi
5. Sistem dapat melakukan prediksi tingkat risiko penyebaran DBD
6. Sistem dapat menampilkan evaluasi model (accuracy, precision, recall, F1-score)
7. Sistem dapat menampilkan laporan dan visualisasi data kasus DBD
8. Sistem dapat mencatat log aktivitas pengguna

Adapun aktor yang terlibat dalam sistem ini adalah:

**Tabel 4.1 Deskripsi Aktor**

| No | Aktor | Deskripsi |
|----|-------|-----------|
| 1 | Admin | Pengguna dengan hak akses penuh untuk mengelola seluruh fitur sistem termasuk manajemen pengguna |
| 2 | Petugas | Pengguna yang bertugas mengelola data pasien, melakukan training model, dan prediksi |
| 3 | Pimpinan | Pengguna yang dapat melihat dashboard, laporan, dan hasil prediksi |

## 4.2 Perancangan Sistem Menggunakan UML

Perancangan sistem menggunakan Unified Modeling Language (UML) untuk menggambarkan interaksi dan alur kerja sistem secara visual. UML yang digunakan dalam perancangan sistem ini meliputi Use Case Diagram, Class Diagram, Activity Diagram, dan Sequence Diagram.

### 4.2.1 Use Case Diagram

Use Case Diagram menggambarkan interaksi antara aktor dengan sistem. Diagram ini menunjukkan fungsionalitas yang disediakan oleh sistem dan bagaimana aktor berinteraksi dengan fungsi-fungsi tersebut. Berikut adalah use case diagram Sistem Prediksi Penyebaran DBD:

**[Gambar 4.1 Use Case Diagram Sistem Prediksi DBD]**

*(Lihat file: Dokumen/UML/use_case_diagram.puml)*

Gambar 4.1 menunjukkan use case diagram sistem yang terdiri dari tiga aktor utama yaitu Admin, Petugas, dan Pimpinan. Masing-masing aktor memiliki hak akses yang berbeda terhadap use case yang tersedia dalam sistem.

**Tabel 4.2 Deskripsi Use Case**

| No | Use Case | Aktor | Deskripsi |
|----|----------|-------|-----------|
| 1 | Login | Admin, Petugas, Pimpinan | Proses autentikasi untuk masuk ke sistem menggunakan username dan password |
| 2 | Logout | Admin, Petugas, Pimpinan | Proses keluar dari sistem dan mengakhiri sesi pengguna |
| 3 | Kelola Pengguna | Admin | Menambah, mengubah, dan menghapus data pengguna sistem |
| 4 | Kelola Data Pasien | Admin, Petugas | Menambah, mengubah, menghapus, dan melihat data pasien DBD |
| 5 | Import Data Excel | Admin, Petugas | Mengimport data pasien dari file Excel (.xlsx) |
| 6 | Training Model | Admin, Petugas | Melatih model Random Forest dengan data yang tersedia |
| 7 | Prediksi Risiko | Admin, Petugas, Pimpinan | Melakukan prediksi tingkat risiko penyebaran DBD |
| 8 | Lihat Evaluasi Model | Admin, Petugas, Pimpinan | Melihat metrik evaluasi model (accuracy, precision, dll) |
| 9 | Lihat Dashboard | Admin, Petugas, Pimpinan | Melihat ringkasan statistik dan grafik |
| 10 | Lihat Laporan | Admin, Petugas, Pimpinan | Melihat laporan kasus DBD per bulan/wilayah |
| 11 | Kelola Wilayah | Admin | Mengelola data wilayah/kecamatan |
| 12 | Lihat Log Aktivitas | Admin | Melihat riwayat aktivitas pengguna dalam sistem |

### 4.2.2 Class Diagram

Class Diagram menggambarkan struktur statis dari sistem yang menunjukkan kelas-kelas, atribut, method, dan hubungan antar kelas. Diagram ini menjadi dasar dalam pengembangan sistem berbasis objek.

**[Gambar 4.2 Class Diagram Sistem Prediksi DBD]**

*(Lihat file: Dokumen/UML/class_diagram.puml)*

Gambar 4.2 menunjukkan class diagram sistem yang terdiri dari 9 kelas utama. Setiap kelas memiliki atribut dan method yang sesuai dengan fungsinya dalam sistem. Relasi antar kelas ditunjukkan dengan garis penghubung yang menjelaskan jenis hubungan seperti association dan dependency.

**Tabel 4.3 Deskripsi Kelas**

| No | Nama Kelas | Deskripsi |
|----|------------|-----------|
| 1 | User | Kelas untuk mengelola data pengguna sistem (login, logout, CRUD user) |
| 2 | PasienDBD | Kelas untuk mengelola data pasien DBD |
| 3 | Wilayah | Kelas untuk mengelola data wilayah/kecamatan |
| 4 | KasusBulanan | Kelas untuk menyimpan agregat kasus per bulan |
| 5 | DataTraining | Kelas untuk menyiapkan data training model |
| 6 | HasilPrediksi | Kelas untuk menyimpan hasil prediksi |
| 7 | ModelEvaluasi | Kelas untuk menyimpan metrik evaluasi model |
| 8 | LogAktivitas | Kelas untuk mencatat aktivitas pengguna |
| 9 | RandomForestModel | Kelas untuk mengelola model machine learning |

### 4.2.3 Activity Diagram

Activity Diagram menggambarkan alur aktivitas dalam sistem dari awal hingga akhir. Diagram ini menunjukkan urutan langkah-langkah yang dilakukan oleh aktor dalam menggunakan sistem.

#### 4.2.3.1 Activity Diagram Admin

**[Gambar 4.3 Activity Diagram Admin]**

*(Lihat file: Dokumen/UML/activity_diagram_admin.puml)*

Gambar 4.3 menunjukkan alur aktivitas Admin dalam menggunakan sistem. Admin memiliki akses penuh ke seluruh fitur sistem termasuk:
- Mengelola pengguna (tambah, edit, hapus)
- Mengelola data pasien DBD
- Melakukan training model Random Forest
- Melakukan prediksi risiko DBD
- Melihat laporan
- Mengelola wilayah
- Melihat log aktivitas

Alur dimulai dari proses login, kemudian Admin dapat memilih menu yang diinginkan dan melakukan berbagai aktivitas sesuai kebutuhan. Setelah selesai, Admin dapat logout dari sistem.

#### 4.2.3.2 Activity Diagram Petugas

**[Gambar 4.4 Activity Diagram Petugas]**

*(Lihat file: Dokumen/UML/activity_diagram_petugas.puml)*

Gambar 4.4 menunjukkan alur aktivitas Petugas dalam menggunakan sistem. Petugas memiliki akses untuk:
- Mengelola data pasien DBD (CRUD)
- Mengimport data dari file Excel
- Melakukan training model
- Melakukan prediksi risiko
- Melihat laporan

Petugas tidak memiliki akses untuk mengelola pengguna dan melihat log aktivitas. Aktivitas yang dapat dilakukan Petugas difokuskan pada pengelolaan data operasional dan analisis prediksi.

#### 4.2.3.3 Activity Diagram Pimpinan

**[Gambar 4.5 Activity Diagram Pimpinan]**

*(Lihat file: Dokumen/UML/activity_diagram_pimpinan.puml)*

Gambar 4.5 menunjukkan alur aktivitas Pimpinan dalam menggunakan sistem. Pimpinan memiliki akses terbatas yang berfokus pada:
- Melihat dashboard dan statistik
- Melakukan prediksi risiko
- Melihat evaluasi model
- Melihat dan mencetak laporan

Pimpinan tidak memiliki akses untuk mengelola data atau melakukan training model. Akses Pimpinan difokuskan pada monitoring dan pengambilan keputusan berdasarkan informasi yang disediakan sistem.

### 4.2.4 Sequence Diagram

Sequence Diagram menggambarkan interaksi antar objek dalam urutan waktu. Diagram ini menunjukkan bagaimana objek-objek dalam sistem berkomunikasi satu sama lain untuk menyelesaikan suatu proses.

#### 4.2.4.1 Sequence Diagram Login

**[Gambar 4.6 Sequence Diagram Login]**

*(Lihat file: Dokumen/UML/sequence_diagram_login.puml)*

Gambar 4.6 menunjukkan alur proses login ke sistem. Pengguna memasukkan username dan password pada halaman login, kemudian sistem melakukan validasi dengan mencocokkan data di database. Jika valid, pengguna diarahkan ke dashboard. Jika tidak valid, sistem menampilkan pesan error.

#### 4.2.4.2 Sequence Diagram Kelola Data Pasien

**[Gambar 4.7 Sequence Diagram Kelola Data Pasien]**

*(Lihat file: Dokumen/UML/sequence_diagram_kelola_pasien.puml)*

Gambar 4.7 menunjukkan alur proses pengelolaan data pasien yang meliputi:
1. **Menampilkan daftar pasien**: Sistem mengambil data dari database dan menampilkan dalam bentuk tabel
2. **Tambah data pasien**: Pengguna mengisi form, sistem memvalidasi dan menyimpan ke database
3. **Edit data pasien**: Pengguna memilih data, mengubah informasi, dan menyimpan perubahan
4. **Hapus data pasien**: Pengguna mengkonfirmasi penghapusan, sistem menghapus data dari database

#### 4.2.4.3 Sequence Diagram Import Data Excel

**[Gambar 4.8 Sequence Diagram Import Data Excel]**

*(Lihat file: Dokumen/UML/sequence_diagram_import.puml)*

Gambar 4.8 menunjukkan alur proses import data dari file Excel. Pengguna memilih file Excel, kemudian sistem mengirim file ke Python API untuk diproses. API membaca file menggunakan Pandas, memvalidasi data, dan menyimpan ke database. Sistem menampilkan hasil import berupa jumlah data berhasil dan gagal.

#### 4.2.4.4 Sequence Diagram Training Model

**[Gambar 4.9 Sequence Diagram Training Model Random Forest]**

*(Lihat file: Dokumen/UML/sequence_diagram_training.puml)*

Gambar 4.9 menunjukkan alur proses training model Random Forest. Proses ini meliputi:
1. Pengguna mengatur parameter (n_estimators, max_depth, test_size)
2. Sistem mengirim request ke Python API
3. API memuat dan memproses data dari Excel
4. Model Random Forest dilatih dengan data training
5. Model dievaluasi dengan data testing
6. Metrik evaluasi (accuracy, precision, recall, F1) dihitung
7. Model dan hasil evaluasi disimpan
8. Hasil ditampilkan ke pengguna

#### 4.2.4.5 Sequence Diagram Prediksi Risiko

**[Gambar 4.10 Sequence Diagram Prediksi Risiko DBD]**

*(Lihat file: Dokumen/UML/sequence_diagram_prediksi.puml)*

Gambar 4.10 menunjukkan alur proses prediksi risiko DBD. Pengguna memasukkan parameter prediksi (bulan, jumlah kasus, usia, jenis kelamin, lama rawat). Sistem mengirim data ke Python API yang memuat model terlatih dan melakukan prediksi. Hasil prediksi berupa tingkat risiko (Tinggi/Sedang/Rendah), confidence score, dan rekomendasi tindakan ditampilkan ke pengguna.

#### 4.2.4.6 Sequence Diagram Lihat Laporan

**[Gambar 4.11 Sequence Diagram Lihat Laporan]**

*(Lihat file: Dokumen/UML/sequence_diagram_laporan.puml)*

Gambar 4.11 menunjukkan alur proses melihat laporan. Pengguna dapat memfilter laporan berdasarkan tahun dan jenis laporan (per bulan/per wilayah). Sistem mengambil data dari database, menghitung statistik, dan menampilkan dalam bentuk grafik dan tabel. Pengguna juga dapat mengexport laporan ke format PDF atau Excel.

#### 4.2.4.7 Sequence Diagram Kelola Pengguna

**[Gambar 4.12 Sequence Diagram Kelola Pengguna]**

*(Lihat file: Dokumen/UML/sequence_diagram_kelola_pengguna.puml)*

Gambar 4.12 menunjukkan alur proses pengelolaan pengguna oleh Admin. Proses ini meliputi menampilkan daftar pengguna, menambah pengguna baru (dengan validasi username unik dan hash password), mengubah status pengguna, dan menghapus pengguna dari sistem.

## 4.3 Desain Sistem Secara Terinci

Desain sistem secara terinci menggambarkan tampilan antarmuka sistem yang akan dibangun, meliputi desain input, desain output, dan desain file (database).

### 4.3.1 Desain Input

Desain input menggambarkan rancangan tampilan form-form yang digunakan untuk memasukkan data ke dalam sistem.

#### 4.3.1.1 Desain Halaman Login

**[Gambar 4.13 Desain Halaman Login]**

Gambar 4.13 menunjukkan rancangan halaman login sistem. Halaman ini merupakan halaman pertama yang ditampilkan saat pengguna mengakses sistem.

**Tabel 4.4 Komponen Form Login**

| No | Komponen | Tipe | Keterangan |
|----|----------|------|------------|
| 1 | Logo | Image | Logo RSUD Lubuk Basung |
| 2 | Judul | Label | "Sistem Prediksi Penyebaran DBD" |
| 3 | Username | Text Input | Input username pengguna (required) |
| 4 | Password | Password Input | Input password pengguna (required) |
| 5 | Tombol Login | Button | Untuk submit form login |
| 6 | Copyright | Label | Informasi hak cipta |

#### 4.3.1.2 Desain Halaman Input Data Pasien

**[Gambar 4.14 Desain Halaman Input Data Pasien]**

Gambar 4.14 menunjukkan rancangan form input data pasien DBD. Form ini digunakan untuk menambah atau mengubah data pasien.

**Tabel 4.5 Komponen Form Input Data Pasien**

| No | Komponen | Tipe | Keterangan |
|----|----------|------|------------|
| 1 | No. RM | Text Input | Nomor rekam medis pasien (unik) |
| 2 | Nama Pasien | Text Input | Nama lengkap pasien |
| 3 | Usia | Number Input | Usia pasien dalam tahun (1-100) |
| 4 | Jenis Kelamin | Select | Pilihan: Laki-laki / Perempuan |
| 5 | Alamat | Textarea | Alamat lengkap pasien |
| 6 | Wilayah | Select | Pilihan wilayah dari database |
| 7 | Tanggal Masuk | Date Picker | Tanggal pasien masuk RS |
| 8 | Tanggal Keluar | Date Picker | Tanggal pasien keluar RS |
| 9 | Lama Rawat | Number Input | Lama rawat dalam hari (otomatis/manual) |
| 10 | Status Pasien | Select | Pilihan: Rawat Inap/Rawat Jalan/Sembuh/Meninggal |
| 11 | Tombol Simpan | Button | Menyimpan data ke database |
| 12 | Tombol Batal | Button | Membatalkan input dan kembali |

#### 4.3.1.3 Desain Halaman Import Data Excel

**[Gambar 4.15 Desain Halaman Import Data Excel]**

Gambar 4.15 menunjukkan rancangan halaman import data dari file Excel. Halaman ini menyediakan fasilitas untuk mengupload file Excel dan mengimport data secara massal.

**Tabel 4.6 Komponen Form Import Data**

| No | Komponen | Tipe | Keterangan |
|----|----------|------|------------|
| 1 | Petunjuk | Card | Panduan format file Excel yang diterima |
| 2 | Download Template | Link | Link untuk download template Excel |
| 3 | Pilih File | File Input | Input untuk memilih file Excel (.xlsx) |
| 4 | Tombol Upload | Button | Memulai proses import |
| 5 | Progress Bar | Progress | Menampilkan progress import |
| 6 | Hasil Import | Table | Menampilkan hasil import (berhasil/gagal) |

#### 4.3.1.4 Desain Halaman Training Model

**[Gambar 4.16 Desain Halaman Training Model]**

Gambar 4.16 menunjukkan rancangan halaman training model Random Forest. Pengguna dapat mengatur parameter model sebelum memulai proses training.

**Tabel 4.7 Komponen Form Training Model**

| No | Komponen | Tipe | Keterangan |
|----|----------|------|------------|
| 1 | n_estimators | Number Input | Jumlah pohon keputusan (10-500, default: 100) |
| 2 | max_depth | Select | Kedalaman maksimum pohon (Auto/5/10/15/20) |
| 3 | test_size | Range Slider | Proporsi data testing (10%-40%, default: 20%) |
| 4 | random_state | Number Input | Seed untuk reproducibility (default: 42) |
| 5 | Tombol Training | Button | Memulai proses training |
| 6 | Progress Card | Card | Menampilkan progress dan status training |
| 7 | Hasil Card | Card | Menampilkan hasil evaluasi model |

#### 4.3.1.5 Desain Halaman Input Prediksi

**[Gambar 4.17 Desain Halaman Input Prediksi]**

Gambar 4.17 menunjukkan rancangan halaman input untuk prediksi risiko DBD. Pengguna memasukkan parameter yang diperlukan untuk melakukan prediksi.

**Tabel 4.8 Komponen Form Input Prediksi**

| No | Komponen | Tipe | Keterangan |
|----|----------|------|------------|
| 1 | Bulan | Select | Pilihan bulan (Januari-Desember) |
| 2 | Jumlah Kasus | Number Input | Perkiraan jumlah kasus DBD |
| 3 | Rata-rata Usia | Number Input | Rata-rata usia pasien (default: 25) |
| 4 | Jenis Kelamin | Select | Mayoritas jenis kelamin (L/P) |
| 5 | Lama Rawat | Number Input | Rata-rata lama rawat inap (default: 3) |
| 6 | Tombol Prediksi | Button | Memulai proses prediksi |
| 7 | Panduan | Card | Penjelasan klasifikasi tingkat risiko |

#### 4.3.1.6 Desain Halaman Input Pengguna

**[Gambar 4.18 Desain Halaman Input Pengguna]**

Gambar 4.18 menunjukkan rancangan form input untuk menambah atau mengubah data pengguna sistem.

**Tabel 4.9 Komponen Form Input Pengguna**

| No | Komponen | Tipe | Keterangan |
|----|----------|------|------------|
| 1 | Username | Text Input | Username untuk login (unik) |
| 2 | Password | Password Input | Password pengguna (min 6 karakter) |
| 3 | Konfirmasi Password | Password Input | Konfirmasi password |
| 4 | Nama Lengkap | Text Input | Nama lengkap pengguna |
| 5 | Email | Email Input | Alamat email |
| 6 | Role | Select | Pilihan: Admin/Petugas/Pimpinan |
| 7 | Status | Select | Pilihan: Aktif/Nonaktif |
| 8 | Foto | File Input | Upload foto profil (opsional) |
| 9 | Tombol Simpan | Button | Menyimpan data pengguna |

#### 4.3.1.7 Desain Halaman Input Wilayah

**[Gambar 4.19 Desain Halaman Input Wilayah]**

Gambar 4.19 menunjukkan rancangan form input untuk mengelola data wilayah.

**Tabel 4.10 Komponen Form Input Wilayah**

| No | Komponen | Tipe | Keterangan |
|----|----------|------|------------|
| 1 | Nama Wilayah | Text Input | Nama desa/kelurahan |
| 2 | Kecamatan | Text Input | Nama kecamatan |
| 3 | Populasi | Number Input | Jumlah penduduk |
| 4 | Tombol Simpan | Button | Menyimpan data wilayah |
| 5 | Tombol Batal | Button | Membatalkan input |

### 4.3.2 Desain Output

Desain output menggambarkan rancangan tampilan keluaran sistem yang berupa informasi, visualisasi, dan laporan.

#### 4.3.2.1 Desain Output Dashboard

**[Gambar 4.20 Desain Output Dashboard]**

Gambar 4.20 menunjukkan rancangan halaman dashboard yang menyajikan ringkasan informasi penting sistem.

**Tabel 4.11 Komponen Output Dashboard**

| No | Komponen | Keterangan |
|----|----------|------------|
| 1 | Kartu Total Kasus | Menampilkan total kasus DBD tahun berjalan |
| 2 | Kartu Pasien Laki-laki | Menampilkan jumlah dan persentase pasien laki-laki |
| 3 | Kartu Pasien Perempuan | Menampilkan jumlah dan persentase pasien perempuan |
| 4 | Kartu Bulan Tertinggi | Menampilkan bulan dengan kasus tertinggi |
| 5 | Grafik Trend | Grafik batang jumlah kasus per bulan |
| 6 | Diagram Risiko | Diagram donat distribusi tingkat risiko |
| 7 | Tabel Ringkasan | Tabel kasus per bulan dengan trend naik/turun |
| 8 | Status Model | Informasi akurasi dan tanggal training terakhir |
| 9 | Quick Actions | Tombol akses cepat ke fitur utama |

#### 4.3.2.2 Desain Output Hasil Prediksi

**[Gambar 4.21 Desain Output Hasil Prediksi]**

Gambar 4.21 menunjukkan rancangan tampilan hasil prediksi risiko DBD.

**Tabel 4.12 Komponen Output Hasil Prediksi**

| No | Komponen | Keterangan |
|----|----------|------------|
| 1 | Tingkat Risiko | Label besar dengan warna indikator (Merah: Tinggi, Kuning: Sedang, Hijau: Rendah) |
| 2 | Confidence Score | Persentase tingkat keyakinan prediksi |
| 3 | Progress Bar Tinggi | Progress bar probabilitas risiko Tinggi |
| 4 | Progress Bar Sedang | Progress bar probabilitas risiko Sedang |
| 5 | Progress Bar Rendah | Progress bar probabilitas risiko Rendah |
| 6 | Data Input | Ringkasan data yang dimasukkan pengguna |
| 7 | Rekomendasi | Daftar rekomendasi tindakan berdasarkan tingkat risiko |
| 8 | Tombol Prediksi Ulang | Untuk melakukan prediksi dengan data baru |
| 9 | Tombol Riwayat | Untuk melihat riwayat prediksi |

#### 4.3.2.3 Desain Output Evaluasi Model

**[Gambar 4.22 Desain Output Evaluasi Model]**

Gambar 4.22 menunjukkan rancangan tampilan evaluasi model machine learning.

**Tabel 4.13 Komponen Output Evaluasi Model**

| No | Komponen | Keterangan |
|----|----------|------------|
| 1 | Tanggal Training | Waktu terakhir model dilatih |
| 2 | Card Accuracy | Menampilkan nilai akurasi dalam persentase |
| 3 | Card Precision | Menampilkan nilai precision dalam persentase |
| 4 | Card Recall | Menampilkan nilai recall dalam persentase |
| 5 | Card F1-Score | Menampilkan nilai F1-score dalam persentase |
| 6 | MAE, RMSE, R² | Menampilkan metrik error |
| 7 | Confusion Matrix | Tabel matriks konfusi hasil prediksi |
| 8 | Feature Importance | Diagram batang pentingnya setiap fitur |
| 9 | Parameter Model | Informasi konfigurasi parameter yang digunakan |

#### 4.3.2.4 Desain Output Laporan Per Bulan

**[Gambar 4.23 Desain Output Laporan Per Bulan]**

Gambar 4.23 menunjukkan rancangan tampilan laporan kasus DBD per bulan.

**Tabel 4.14 Komponen Output Laporan Per Bulan**

| No | Komponen | Keterangan |
|----|----------|------------|
| 1 | Filter Tahun | Dropdown untuk memilih tahun laporan |
| 2 | Kartu Total Kasus | Total kasus dalam periode yang dipilih |
| 3 | Kartu Rata-rata | Rata-rata kasus per bulan |
| 4 | Kartu Tertinggi | Bulan dengan kasus tertinggi |
| 5 | Grafik Trend | Visualisasi grafik trend bulanan |
| 6 | Tabel Detail | Tabel bulan, jumlah kasus, tingkat risiko, trend |
| 7 | Tombol Export PDF | Untuk export laporan ke PDF |
| 8 | Tombol Export Excel | Untuk export laporan ke Excel |

#### 4.3.2.5 Desain Output Laporan Per Wilayah

**[Gambar 4.24 Desain Output Laporan Per Wilayah]**

Gambar 4.24 menunjukkan rancangan tampilan laporan distribusi kasus per wilayah.

**Tabel 4.15 Komponen Output Laporan Per Wilayah**

| No | Komponen | Keterangan |
|----|----------|------------|
| 1 | Filter Periode | Pilihan rentang waktu laporan |
| 2 | Diagram Wilayah | Diagram batang distribusi kasus per wilayah |
| 3 | Tabel Wilayah | Nama wilayah, jumlah kasus, persentase |
| 4 | Tombol Cetak | Untuk mencetak laporan |

#### 4.3.2.6 Desain Output Daftar Data Pasien

**[Gambar 4.25 Desain Output Daftar Data Pasien]**

Gambar 4.25 menunjukkan rancangan tampilan daftar data pasien DBD.

**Tabel 4.16 Komponen Output Daftar Pasien**

| No | Komponen | Keterangan |
|----|----------|------------|
| 1 | Filter Pencarian | Input untuk mencari berdasarkan nama/alamat |
| 2 | Filter Bulan | Dropdown untuk filter berdasarkan bulan |
| 3 | Tombol Tambah | Tombol untuk menambah data baru |
| 4 | Tombol Import | Tombol untuk import dari Excel |
| 5 | Tabel Pasien | Kolom: No.RM, Nama, Usia, JK, Alamat, Tanggal, Lama Rawat |
| 6 | Kolom Aksi | Tombol detail, edit, hapus |
| 7 | Pagination | Navigasi halaman untuk data banyak |
| 8 | Info Total | Informasi jumlah data yang ditampilkan |

### 4.3.3 Desain File (Database)

Desain file atau database menggambarkan struktur tabel yang digunakan untuk menyimpan data dalam sistem. Sistem menggunakan MySQL sebagai database management system.

#### 4.3.3.1 Tabel Users

**Tabel 4.17 Struktur Tabel users**

| No | Field | Tipe Data | Size | Keterangan |
|----|-------|-----------|------|------------|
| 1 | id | INT | 11 | Primary Key, Auto Increment |
| 2 | username | VARCHAR | 50 | Username unik untuk login |
| 3 | password | VARCHAR | 255 | Password terenkripsi (bcrypt) |
| 4 | nama_lengkap | VARCHAR | 100 | Nama lengkap pengguna |
| 5 | email | VARCHAR | 100 | Alamat email pengguna |
| 6 | role | ENUM | - | admin, petugas, pimpinan |
| 7 | foto | VARCHAR | 255 | Nama file foto profil |
| 8 | status | ENUM | - | aktif, nonaktif |
| 9 | last_login | DATETIME | - | Waktu login terakhir |
| 10 | created_at | TIMESTAMP | - | Waktu data dibuat |
| 11 | updated_at | TIMESTAMP | - | Waktu data diupdate |

#### 4.3.3.2 Tabel Wilayah

**Tabel 4.18 Struktur Tabel wilayah**

| No | Field | Tipe Data | Size | Keterangan |
|----|-------|-----------|------|------------|
| 1 | id | INT | 11 | Primary Key, Auto Increment |
| 2 | nama_wilayah | VARCHAR | 100 | Nama desa/kelurahan |
| 3 | kecamatan | VARCHAR | 100 | Nama kecamatan |
| 4 | latitude | DECIMAL | 10,8 | Koordinat latitude |
| 5 | longitude | DECIMAL | 11,8 | Koordinat longitude |
| 6 | populasi | INT | 11 | Jumlah penduduk |
| 7 | created_at | TIMESTAMP | - | Waktu data dibuat |

#### 4.3.3.3 Tabel Pasien DBD

**Tabel 4.19 Struktur Tabel pasien_dbd**

| No | Field | Tipe Data | Size | Keterangan |
|----|-------|-----------|------|------------|
| 1 | id | INT | 11 | Primary Key, Auto Increment |
| 2 | no_rm | VARCHAR | 20 | Nomor rekam medis (unik) |
| 3 | nama_pasien | VARCHAR | 100 | Nama lengkap pasien |
| 4 | usia | INT | 11 | Usia pasien dalam tahun |
| 5 | jenis_kelamin | ENUM | - | L (Laki-laki), P (Perempuan) |
| 6 | alamat | TEXT | - | Alamat lengkap pasien |
| 7 | id_wilayah | INT | 11 | Foreign Key ke tabel wilayah |
| 8 | tanggal_masuk | DATE | - | Tanggal pasien masuk RS |
| 9 | tanggal_keluar | DATE | - | Tanggal pasien keluar RS |
| 10 | lama_rawat | INT | 11 | Durasi rawat inap (hari) |
| 11 | bulan | VARCHAR | 20 | Nama bulan (Januari-Desember) |
| 12 | tahun | INT | 4 | Tahun kasus |
| 13 | status_pasien | ENUM | - | rawat_inap, rawat_jalan, sembuh, meninggal |
| 14 | created_at | TIMESTAMP | - | Waktu data dibuat |
| 15 | updated_at | TIMESTAMP | - | Waktu data diupdate |

#### 4.3.3.4 Tabel Kasus Bulanan

**Tabel 4.20 Struktur Tabel kasus_bulanan**

| No | Field | Tipe Data | Size | Keterangan |
|----|-------|-----------|------|------------|
| 1 | id | INT | 11 | Primary Key, Auto Increment |
| 2 | bulan | VARCHAR | 20 | Nama bulan |
| 3 | tahun | INT | 4 | Tahun |
| 4 | jumlah_kasus | INT | 11 | Total kasus DBD bulan tersebut |
| 5 | jumlah_sembuh | INT | 11 | Jumlah pasien sembuh |
| 6 | jumlah_meninggal | INT | 11 | Jumlah pasien meninggal |
| 7 | tingkat_risiko | ENUM | - | Rendah, Sedang, Tinggi |
| 8 | created_at | TIMESTAMP | - | Waktu data dibuat |

#### 4.3.3.5 Tabel Hasil Prediksi

**Tabel 4.21 Struktur Tabel hasil_prediksi**

| No | Field | Tipe Data | Size | Keterangan |
|----|-------|-----------|------|------------|
| 1 | id | INT | 11 | Primary Key, Auto Increment |
| 2 | tanggal_prediksi | DATETIME | - | Waktu prediksi dilakukan |
| 3 | bulan_prediksi | VARCHAR | 20 | Bulan yang diprediksi |
| 4 | tahun_prediksi | INT | 4 | Tahun prediksi |
| 5 | jumlah_kasus_prediksi | INT | 11 | Jumlah kasus input prediksi |
| 6 | tingkat_risiko_prediksi | ENUM | - | Rendah, Sedang, Tinggi |
| 7 | confidence_score | DECIMAL | 5,2 | Skor keyakinan (0-100%) |
| 8 | model_version | VARCHAR | 50 | Versi model yang digunakan |
| 9 | created_by | INT | 11 | Foreign Key ke tabel users |
| 10 | created_at | TIMESTAMP | - | Waktu data dibuat |

#### 4.3.3.6 Tabel Model Evaluasi

**Tabel 4.22 Struktur Tabel model_evaluasi**

| No | Field | Tipe Data | Size | Keterangan |
|----|-------|-----------|------|------------|
| 1 | id | INT | 11 | Primary Key, Auto Increment |
| 2 | tanggal_training | DATETIME | - | Waktu training dilakukan |
| 3 | accuracy | DECIMAL | 5,4 | Nilai akurasi model (0-1) |
| 4 | precision_score | DECIMAL | 5,4 | Nilai precision (0-1) |
| 5 | recall_score | DECIMAL | 5,4 | Nilai recall (0-1) |
| 6 | f1_score | DECIMAL | 5,4 | Nilai F1-score (0-1) |
| 7 | mae | DECIMAL | 10,4 | Mean Absolute Error |
| 8 | rmse | DECIMAL | 10,4 | Root Mean Squared Error |
| 9 | r2_score | DECIMAL | 5,4 | R-squared score |
| 10 | n_estimators | INT | 11 | Jumlah pohon keputusan |
| 11 | max_depth | INT | 11 | Kedalaman maksimum pohon |
| 12 | confusion_matrix | TEXT | - | Matriks konfusi dalam format JSON |
| 13 | feature_importance | TEXT | - | Pentingnya fitur dalam format JSON |
| 14 | model_path | VARCHAR | 255 | Path file model tersimpan |
| 15 | created_at | TIMESTAMP | - | Waktu data dibuat |

#### 4.3.3.7 Tabel Log Aktivitas

**Tabel 4.23 Struktur Tabel log_aktivitas**

| No | Field | Tipe Data | Size | Keterangan |
|----|-------|-----------|------|------------|
| 1 | id | INT | 11 | Primary Key, Auto Increment |
| 2 | user_id | INT | 11 | Foreign Key ke tabel users |
| 3 | aksi | VARCHAR | 100 | Jenis aktivitas yang dilakukan |
| 4 | deskripsi | TEXT | - | Detail aktivitas |
| 5 | ip_address | VARCHAR | 45 | Alamat IP pengguna |
| 6 | created_at | TIMESTAMP | - | Waktu aktivitas |

### 4.3.4 Relasi Antar Tabel

**[Gambar 4.26 Entity Relationship Diagram (ERD)]**

Gambar 4.26 menunjukkan relasi antar tabel dalam database sistem. Berikut adalah penjelasan relasi:

**Tabel 4.24 Relasi Antar Tabel**

| No | Tabel | Foreign Key | Referensi | Tipe Relasi | Keterangan |
|----|-------|-------------|-----------|-------------|------------|
| 1 | pasien_dbd | id_wilayah | wilayah(id) | Many to One | Setiap pasien berasal dari satu wilayah |
| 2 | hasil_prediksi | created_by | users(id) | Many to One | Setiap prediksi dibuat oleh satu user |
| 3 | log_aktivitas | user_id | users(id) | Many to One | Setiap log aktivitas dilakukan oleh satu user |

Relasi antar tabel menggunakan foreign key untuk menjaga integritas data. Aksi ON DELETE SET NULL digunakan agar data tidak hilang jika data referensi dihapus.
