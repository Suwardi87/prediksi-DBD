# UML Diagrams (Standard Astah) - Sistem Prediksi Penyebaran DBD RSUD Lubuk Basung

Dokumen ini berisi kumpulan diagram UML untuk **Sistem Prediksi Penyebaran DBD menggunakan Algoritma Random Forest di RSUD Lubuk Basung**, dirancang sesuai dengan **standardisasi Astah UML** berdasarkan dokumen [BABIV.pdf](file:///home/vue/Documents/frelence/joki/BABIV.pdf).

---

## 1. Use Case Diagram (Gambar 4.26)
Sesuai dengan standar Astah, hubungan aktor ke use case menggunakan garis solid asosiasi sederhana (tanpa mata panah), sedangkan relasi dependensi `<<include>>` dan `<<extend>>` menggunakan garis putus-putus berpanah dengan arah yang benar.

```mermaid
graph LR
    %% Actors
    Admin["&laquo;actor&raquo;<br/>Admin"]
    Petugas["&laquo;actor&raquo;<br/>Petugas"]

    %% Styling Actors (Astah Style)
    classDef actor fill:#fcf8e3,stroke:#8a6d3b,stroke-width:2px;
    class Admin,Petugas actor;

    subgraph Sistem_Prediksi_DBD ["Sistem Prediksi Penyebaran DBD"]
        %% Core Use Cases
        UC_Login(["Login"])
        UC_Logout(["Logout"])
        UC_Dashboard(["Lihat Dashboard"])

        %% Admin-Specific Use Cases
        UC_Kelola_Pengguna(["Kelola Pengguna"])
        UC_Kelola_Wilayah(["Kelola Wilayah"])
        UC_Log_Aktivitas(["Lihat Log Aktivitas"])

        %% Shared Use Cases (Admin & Petugas)
        UC_Kelola_Pasien(["Kelola Data Pasien"])
        UC_Import_Excel(["Import Data Excel"])
        UC_Training_Model(["Training Model"])
        UC_Prediksi_Risiko(["Prediksi Risiko"])
        UC_Lihat_Evaluasi(["Lihat Evaluasi Model"])
        UC_Lihat_Laporan(["Lihat Laporan"])

        %% Extends Use Cases
        UC_Cetak_Laporan(["Cetak Laporan"])
    end

    %% Admin Associations (Solid lines, no arrows)
    Admin --- UC_Login
    Admin --- UC_Logout
    Admin --- UC_Dashboard
    Admin --- UC_Kelola_Pengguna
    Admin --- UC_Kelola_Wilayah
    Admin --- UC_Log_Aktivitas
    Admin --- UC_Kelola_Pasien
    Admin --- UC_Import_Excel
    Admin --- UC_Training_Model
    Admin --- UC_Prediksi_Risiko
    Admin --- UC_Lihat_Evaluasi
    Admin --- UC_Lihat_Laporan

    %% Petugas Associations
    Petugas --- UC_Login
    Petugas --- UC_Logout
    Petugas --- UC_Dashboard
    Petugas --- UC_Kelola_Pasien
    Petugas --- UC_Import_Excel
    Petugas --- UC_Training_Model
    Petugas --- UC_Prediksi_Risiko
    Petugas --- UC_Lihat_Evaluasi
    Petugas --- UC_Lihat_Laporan

    %% Dependency Relationships
    UC_Kelola_Pengguna -.->|"<<include>>"| UC_Login
    UC_Kelola_Wilayah -.->|"<<include>>"| UC_Login
    UC_Log_Aktivitas -.->|"<<include>>"| UC_Login
    UC_Kelola_Pasien -.->|"<<include>>"| UC_Login
    UC_Import_Excel -.->|"<<include>>"| UC_Login
    UC_Training_Model -.->|"<<include>>"| UC_Login
    UC_Prediksi_Risiko -.->|"<<include>>"| UC_Login
    UC_Lihat_Evaluasi -.->|"<<include>>"| UC_Login
    UC_Lihat_Laporan -.->|"<<include>>"| UC_Login

    UC_Cetak_Laporan -.->|"<<extend>>"| UC_Lihat_Laporan
```

---

## 2. Class Diagram (Gambar 4.27)
Representasi kelas-kelas entitas database (skema relasional) lengkap dengan visibilitas (`-` untuk private, `+` untuk public), tipe data standard Astah, serta relasi asosiasi berarah beserta multiplisitasnya.

```mermaid
classDiagram
    class User {
        -id : int
        -username : string
        -password : string
        -nama_lengkap : string
        -email : string
        -role : enum
        -foto : string
        -status : enum
        -last_login : datetime
        -created_at : timestamp
        -updated_at : timestamp
        +check_password(password : string) : boolean
        +login() : boolean
        +logout() : void
        +create() : boolean
        +update() : boolean
        +delete() : boolean
    }

    class Wilayah {
        -id : int
        -nama_wilayah : string
        -kecamatan : string
        -latitude : decimal
        -longitude : decimal
        -populasi : int
        -created_at : timestamp
        +create() : boolean
        +read() : List
        +update() : boolean
        +delete() : boolean
        +getPasienCount() : int
    }

    class PasienDBD {
        -id : int
        -no_rm : string
        -nama_pasien : string
        -usia : int
        -jenis_kelamin : enum
        -alamat : text
        -id_wilayah : int
        -tanggal_masuk : date
        -tanggal_keluar : date
        -lama_rawat : int
        -bulan : string
        -tahun : int
        -status_pasien : enum
        -created_at : timestamp
        -updated_at : timestamp
        +create() : boolean
        +read() : List
        +update() : boolean
        +delete() : boolean
        +getByBulan() : List
    }

    class KasusBulanan {
        -id : int
        -bulan : string
        -tahun : int
        -jumlah_kasus : int
        -jumlah_sembuh : int
        -jumlah_meninggal : int
        -tingkat_risiko : enum
        -created_at : timestamp
        +create() : boolean
        +read() : List
        +update() : boolean
        +getByTahun(tahun : int) : List
        +getStatistik() : Object
    }

    class HasilPrediksi {
        -id : int
        -tanggal_prediksi : datetime
        -bulan_prediksi : string
        -tahun_prediksi : int
        -jumlah_kasus_prediksi : int
        -tingkat_risiko_prediksi : enum
        -confidence_score : decimal
        -model_version : string
        -created_by : int
        -created_at : timestamp
        +create() : boolean
        +read() : List
        +getByTahun(tahun : int) : List
        +getLatest() : Object
        +predict(data : Object) : Object
    }

    class ModelEvaluasi {
        -id : int
        -tanggal_training : datetime
        -accuracy : decimal
        -precision_score : decimal
        -recall_score : decimal
        -f1_score : decimal
        -mae : decimal
        -rmse : decimal
        -r2_score : decimal
        -n_estimators : int
        -max_depth : int
        -confusion_matrix : text
        -feature_importance : text
        -model_path : string
        -created_at : timestamp
        +create() : boolean
        +read() : List
        +getLatest() : Object
        +getMetrics() : Object
    }

    class LogAktivitas {
        -id : int
        -user_id : int
        -aksi : string
        -deskripsi : text
        -ip_address : string
        -created_at : timestamp
        +create() : boolean
        +read() : List
        +getByUser(user_id : int) : List
        +filter(filters : Object) : List
    }

    %% Associations and Multiplicity (Astah Style)
    User "1" --> "0..*" HasilPrediksi : creates
    User "1" --> "0..*" LogAktivitas : logs
    Wilayah "1" --> "0..*" PasienDBD : memiliki
```

---

## 3. Activity Diagram (Diagram Aktivitas)
Menggunakan format swimlane (partition) untuk membagi tanggung jawab antara Aktor dan Sistem.

### A. Activity Diagram Admin (Gambar 4.28)
```mermaid
flowchart TD
    subgraph Admin ["Partition: Admin"]
        Start([Mulai]) --> A_Akses[Mengakses Website]
        A_Input[Menginputkan Username & Password Admin]
        A_Manage[Pilih Menu Manajemen Data]
        A_Form[Pilih Aksi: Tambah/Edit/Hapus & Isi Form]
        A_Logout[Klik Logout]
    end

    subgraph Sistem ["Partition: Sistem"]
        S_Home[Menampilkan Halaman Utama]
        S_Login[Menampilkan Form Login]
        S_Auth{Validasi Login?}
        S_Dash[Menampilkan Dashboard Admin]
        S_Menu{Pilihan Menu}
        S_ActionForm[Menampilkan Form Aksi]
        S_Save[Memproses & Menyimpan ke Database]
        S_Success[Menampilkan Notifikasi Sukses & Refresh Halaman]
        S_Logout[Menghapus Session & Mengarahkan ke Home]
        End([Selesai])
    end

    %% Cross Partition Flows
    A_Akses --> S_Home
    S_Home --> S_Login
    S_Login --> A_Input
    A_Input --> S_Auth
    S_Auth -->|Gagal| S_Login
    S_Auth -->|Berhasil| S_Dash
    S_Dash --> A_Manage
    A_Manage --> S_Menu
    S_Menu --> A_Form
    A_Form --> S_ActionForm
    S_ActionForm --> S_Save
    S_Save --> S_Success
    S_Success --> A_Logout
    A_Logout --> S_Logout
    S_Logout --> End
```

### B. Activity Diagram Petugas (Gambar 4.29)
```mermaid
flowchart TD
    subgraph Petugas ["Partition: Petugas"]
        Start([Mulai]) --> P_Akses[Mengakses Website]
        P_Input[Menginputkan Username & Password]
        P_Select[Pilih Menu: Kelola Pasien / Prediksi / Training]
        P_Action[Isi Form / Jalankan Aksi]
        P_Logout[Klik Logout]
    end

    subgraph Sistem ["Partition: Sistem"]
        S_Home[Menampilkan Halaman Utama]
        S_Login[Menampilkan Form Login]
        S_Auth{Validasi Login?}
        S_Dash[Menampilkan Dashboard Petugas]
        S_Menu{Pilihan Menu}
        S_ActionForm[Menampilkan Form / Hasil Proses]
        S_Save[Memproses, Prediksi, & Update Database]
        S_Success[Menampilkan Hasil & Notifikasi Sukses]
        S_Logout[Menghapus Session & Mengarahkan ke Home]
        End([Selesai])
    end

    %% Cross Partition Flows
    P_Akses --> S_Home
    S_Home --> S_Login
    S_Login --> P_Input
    P_Input --> S_Auth
    S_Auth -->|Gagal| S_Login
    S_Auth -->|Berhasil| S_Dash
    S_Dash --> P_Select
    P_Select --> S_Menu
    S_Menu --> P_Action
    P_Action --> S_ActionForm
    S_ActionForm --> S_Save
    S_Save --> S_Success
    S_Success --> P_Logout
    P_Logout --> S_Logout
    S_Logout --> End
```

---

## 4. Sequence Diagram (Diagram Urutan)
Sequence Diagram di bawah ini menggunakan konvensi Astah di mana terdapat Aktor, Boundary (Halaman/UI), Control (Proses/API), dan Entity (Database/Model).

### A. Sequence Diagram Login (Gambar 4.31)
```mermaid
sequenceDiagram
    autonumber
    actor Pengguna as "Aktor: Pengguna"
    participant HalamanLogin as "boundary: Halaman Login"
    participant ControllerAuth as "control: Controller Auth"
    participant Database as "entity: Database"

    Pengguna->>HalamanLogin: Membuka halaman login()
    HalamanLogin-->>Pengguna: Tampilkan Form Login
    Pengguna->>HalamanLogin: Input username & password()
    HalamanLogin->>ControllerAuth: Submit form login(username, password)
    activate ControllerAuth
    ControllerAuth->>ControllerAuth: Validasi input()
    ControllerAuth->>Database: Query user by username(username)
    activate Database
    Database-->>ControllerAuth: Return user data
    deactivate Database
    
    alt Password Valid
        ControllerAuth->>ControllerAuth: Verify password()
        ControllerAuth->>ControllerAuth: Set session()
        ControllerAuth->>Database: Update last_login(user_id)
        ControllerAuth-->>HalamanLogin: Login berhasil
        HalamanLogin-->>Pengguna: Redirect ke Dashboard
    else Password Tidak Valid
        ControllerAuth-->>HalamanLogin: Login gagal
        deactivate ControllerAuth
        HalamanLogin-->>Pengguna: Tampilkan pesan error
    end
```

### B. Sequence Diagram Kelola Data Pasien (Gambar 4.32)
```mermaid
sequenceDiagram
    autonumber
    actor Petugas as "Aktor: Petugas"
    participant HalamanPasien as "boundary: Halaman Data Pasien"
    participant ControllerPasien as "control: Controller Pasien"
    participant Database as "entity: Database"

    Petugas->>HalamanPasien: Buka menu Data Pasien()
    HalamanPasien->>ControllerPasien: Request daftar pasien()
    activate ControllerPasien
    ControllerPasien->>Database: SELECT * FROM pasien_dbd
    activate Database
    Database-->>ControllerPasien: Return data pasien
    deactivate Database
    ControllerPasien-->>HalamanPasien: Kirim data pasien
    deactivate ControllerPasien
    HalamanPasien-->>Petugas: Tampilkan tabel pasien

    alt Tambah Data Pasien
        Petugas->>HalamanPasien: Klik tombol Tambah()
        HalamanPasien-->>Petugas: Tampilkan form input
        Petugas->>HalamanPasien: Input data pasien & Klik Simpan
        HalamanPasien->>ControllerPasien: Submit form(data)
        activate ControllerPasien
        ControllerPasien->>ControllerPasien: Validasi data()
        ControllerPasien->>Database: INSERT INTO pasien_dbd
        activate Database
        Database-->>ControllerPasien: Success
        deactivate Database
        ControllerPasien->>Database: INSERT INTO log_aktivitas
        ControllerPasien-->>HalamanPasien: Response sukses
        deactivate ControllerPasien
        HalamanPasien-->>Petugas: Tampilkan alert sukses
    end
```

### C. Sequence Diagram Import Data Excel (Gambar 4.33)
```mermaid
sequenceDiagram
    autonumber
    actor Petugas as "Aktor: Petugas"
    participant HalamanImport as "boundary: Halaman Import"
    participant ControllerImport as "control: Controller Import"
    participant FlaskAPI as "control: Python API (Flask)"
    participant Database as "entity: Database"

    Petugas->>HalamanImport: Buka halaman Import()
    HalamanImport-->>Petugas: Tampilkan form upload
    Petugas->>HalamanImport: Pilih file Excel & Klik Upload
    HalamanImport->>HalamanImport: Validasi format file (.xlsx)
    HalamanImport->>ControllerImport: Upload file(file)
    activate ControllerImport
    ControllerImport->>ControllerImport: Simpan file sementara()
    ControllerImport->>FlaskAPI: POST /import (file_path)
    activate FlaskAPI
    FlaskAPI->>FlaskAPI: Load Excel dengan Pandas pd.read_excel()
    FlaskAPI->>FlaskAPI: Validasi kolom data()
    FlaskAPI->>FlaskAPI: Preprocessing data()
    
    loop Untuk setiap baris data
        FlaskAPI->>FlaskAPI: Parse data pasien()
        FlaskAPI->>FlaskAPI: Validasi nilai()
        FlaskAPI->>Database: INSERT INTO pasien_dbd
        activate Database
        Database-->>FlaskAPI: Success
        deactivate Database
    end
    
    FlaskAPI->>FlaskAPI: Hitung jumlah berhasil/gagal()
    FlaskAPI-->>ControllerImport: Response (total, berhasil, gagal)
    deactivate FlaskAPI
    ControllerImport->>Database: INSERT INTO log_aktivitas
    ControllerImport-->>HalamanImport: Response hasil import
    deactivate ControllerImport
    HalamanImport-->>Petugas: Tampilkan hasil (Total, Berhasil, Gagal)
```

### D. Sequence Diagram Training Model (Gambar 4.34)
```mermaid
sequenceDiagram
    autonumber
    actor Petugas as "Aktor: Petugas"
    participant HalamanTraining as "boundary: Halaman Training"
    participant ControllerTraining as "control: Controller Training"
    participant FlaskAPI as "control: Python API (Flask)"
    participant RFModel as "entity: Random Forest Model"
    participant Database as "entity: Database"

    Petugas->>HalamanTraining: Buka menu Training Model()
    HalamanTraining-->>Petugas: Tampilkan form konfigurasi
    Petugas->>HalamanTraining: Input parameter & Klik Mulai Training
    HalamanTraining->>ControllerTraining: Submit parameter training(params)
    activate ControllerTraining
    ControllerTraining->>FlaskAPI: POST /train (params)
    activate FlaskAPI
    FlaskAPI->>FlaskAPI: Load data dari database()
    FlaskAPI->>FlaskAPI: Preprocessing data(cleaning, encoding)
    FlaskAPI->>FlaskAPI: Split data (training & testing)
    FlaskAPI->>FlaskAPI: Inisialisasi RandomForestClassifier()
    FlaskAPI->>RFModel: fit(X_train, y_train)
    FlaskAPI->>RFModel: predict(X_test)
    FlaskAPI->>RFModel: Calculate metrics(accuracy, precision, recall, f1)
    FlaskAPI->>RFModel: Calculate feature importance()
    RFModel-->>FlaskAPI: Return trained model
    FlaskAPI->>FlaskAPI: Save model to file (random_forest_model.pkl)
    FlaskAPI->>Database: INSERT INTO model_evaluasi(metrics, confusion_matrix)
    activate Database
    Database-->>FlaskAPI: Success
    deactivate Database
    FlaskAPI-->>ControllerTraining: Response (status, metrics, feature_importance)
    deactivate FlaskAPI
    ControllerTraining-->>HalamanTraining: Kirim hasil training
    deactivate ControllerTraining
    HalamanTraining-->>Petugas: Tampilkan hasil evaluasi model
```

### E. Sequence Diagram Prediksi Risiko (Gambar 4.35)
```mermaid
sequenceDiagram
    autonumber
    actor Pengguna as "Aktor: Pengguna"
    participant HalamanPrediksi as "boundary: Halaman Prediksi"
    participant ControllerPrediksi as "control: Controller Prediksi"
    participant FlaskAPI as "control: Python API (Flask)"
    participant RFModel as "entity: Random Forest Model"
    participant Database as "entity: Database"

    Pengguna->>HalamanPrediksi: Buka menu Prediksi()
    HalamanPrediksi-->>Pengguna: Tampilkan form input parameter
    Pengguna->>HalamanPrediksi: Input data & Klik Prediksi
    HalamanPrediksi->>HalamanPrediksi: Validasi input()
    HalamanPrediksi->>ControllerPrediksi: Submit data prediksi(data)
    activate ControllerPrediksi
    ControllerPrediksi->>FlaskAPI: POST /predict (data)
    activate FlaskAPI
    FlaskAPI->>FlaskAPI: Load model (random_forest_model.pkl)
    FlaskAPI->>FlaskAPI: Load encoder()
    FlaskAPI->>RFModel: model.predict(features)
    RFModel-->>FlaskAPI: prediction
    FlaskAPI->>RFModel: model.predict_proba(features)
    RFModel-->>FlaskAPI: probabilities
    FlaskAPI->>FlaskAPI: Decode prediction (Tinggi/Sedang/Rendah)
    FlaskAPI->>FlaskAPI: Generate rekomendasi()
    FlaskAPI->>Database: INSERT INTO hasil_prediksi(hasil, confidence)
    activate Database
    Database-->>FlaskAPI: Success
    deactivate Database
    FlaskAPI-->>ControllerPrediksi: Response (tingkat_risiko, confidence, rekomendasi)
    deactivate FlaskAPI
    ControllerPrediksi-->>HalamanPrediksi: Kirim hasil prediksi
    deactivate ControllerPrediksi
    HalamanPrediksi-->>Pengguna: Tampilkan hasil prediksi & rekomendasi
```

### F. Sequence Diagram Lihat Laporan (Gambar 4.36)
```mermaid
sequenceDiagram
    autonumber
    actor Pengguna as "Aktor: Pengguna"
    participant HalamanLaporan as "boundary: Halaman Laporan"
    participant ControllerLaporan as "control: Controller Laporan"
    participant Database as "entity: Database"

    Pengguna->>HalamanLaporan: Buka menu Laporan()
    HalamanLaporan->>ControllerLaporan: Request data awal()
    activate ControllerLaporan
    ControllerLaporan->>Database: SELECT tahun FROM kasus_bulanan
    activate Database
    Database-->>ControllerLaporan: Return daftar tahun
    deactivate Database
    ControllerLaporan-->>HalamanLaporan: Kirim data filter
    deactivate ControllerLaporan
    HalamanLaporan-->>Pengguna: Tampilkan halaman laporan dengan filter

    Pengguna->>HalamanLaporan: Pilih filter & Klik Tampilkan
    HalamanLaporan->>ControllerLaporan: Request laporan(filter)
    activate ControllerLaporan
    
    alt Laporan Per Bulan
        ControllerLaporan->>Database: SELECT * FROM kasus_bulanan WHERE tahun=?
        activate Database
        Database-->>ControllerLaporan: Return data bulanan
        deactivate Database
    else Laporan Per Wilayah
        ControllerLaporan->>Database: SELECT wilayah, COUNT(*) FROM pasien_dbd GROUP BY wilayah
        activate Database
        Database-->>ControllerLaporan: Return data wilayah
        deactivate Database
    end
    
    ControllerLaporan->>ControllerLaporan: Hitung statistik()
    ControllerLaporan-->>HalamanLaporan: Kirim data laporan
    deactivate ControllerLaporan
    HalamanLaporan->>HalamanLaporan: Render grafik (Chart.js)
    HalamanLaporan->>HalamanLaporan: Render tabel data
    HalamanLaporan-->>Pengguna: Tampilkan visualisasi laporan
```

### G. Sequence Diagram Kelola Pengguna (Gambar 4.37)
```mermaid
sequenceDiagram
    autonumber
    actor Admin as "Aktor: Admin"
    participant HalamanPengguna as "boundary: Halaman Pengguna"
    participant ControllerUser as "control: Controller User"
    participant Database as "entity: Database"

    Admin->>HalamanPengguna: Buka menu Kelola Pengguna()
    HalamanPengguna->>ControllerUser: Request daftar pengguna()
    activate ControllerUser
    ControllerUser->>Database: SELECT * FROM users
    activate Database
    Database-->>ControllerUser: Return data users
    deactivate Database
    ControllerUser-->>HalamanPengguna: Kirim data users
    deactivate ControllerUser
    HalamanPengguna-->>Admin: Tampilkan tabel pengguna

    alt Tambah Pengguna Baru
        Admin->>HalamanPengguna: Klik tombol Tambah()
        HalamanPengguna-->>Admin: Tampilkan form input
        Admin->>HalamanPengguna: Input data & Klik Simpan
        HalamanPengguna->>ControllerUser: Submit form(data)
        activate ControllerUser
        ControllerUser->>ControllerUser: Validasi username unik()
        ControllerUser->>Database: SELECT * FROM users WHERE username=?
        activate Database
        Database-->>ControllerUser: Return result
        deactivate Database
        
        alt Username Tersedia
            ControllerUser->>ControllerUser: Hash password()
            ControllerUser->>Database: INSERT INTO users
            activate Database
            Database-->>ControllerUser: Success
            deactivate Database
            ControllerUser->>Database: INSERT INTO log_aktivitas
            ControllerUser-->>HalamanPengguna: Response sukses
            HalamanPengguna-->>Admin: Tampilkan alert sukses
        else Username Sudah Ada
            ControllerUser-->>HalamanPengguna: Response error
            deactivate ControllerUser
            HalamanPengguna-->>Admin: Tampilkan pesan error
        end
    end
```

---

## 5. State Chart Diagram (Gambar 4.39)
Menggambarkan perubahan state sistem dari kondisi awal, proses login, dan alur sub-state saat berpindah fitur di dashboard.

```mermaid
stateDiagram-v2
    [*] --> Idle : Akses Sistem
    Idle : Menunggu input pengguna
    
    Idle --> ProsesLogin : Belum Login
    
    state ProsesLogin {
        [*] --> MasukkanKredensial
        MasukkanKredensial --> ValidasiLogin : Submit Form
        ValidasiLogin --> MasukkanKredensial : [Submit Invalid]
        ValidasiLogin --> LoginBerhasil : [Valid]
    }
    
    ProsesLogin --> Dashboard : Login Berhasil
    
    state Dashboard {
        [*] --> MenampilkanStatistik : Load Dashboard
        MenampilkanStatistik --> ManajemenData : [Menu Data]
        MenampilkanStatistik --> TrainingModel : [Menu Training]
        MenampilkanStatistik --> ProsesPrediksi : [Menu Prediksi]
        MenampilkanStatistik --> EvaluasiModel : [Menu Evaluasi]
        
        state ManajemenData {
            [*] --> TampilData
            TampilData --> TambahData : Klik Tambah
            TampilData --> EditData : Klik Edit
            TampilData --> HapusData : Klik Hapus
            
            TambahState : Input Data Pasien
            EditState : Update Data Pasien
            HapusState : Hapus Data Pasien
            
            TambahData --> SimpanData : Submit
            EditData --> SimpanData : Submit
            HapusData --> PermintaanHapus : Klik Hapus
            
            SimpanData --> TampilData : Sukses / Batal
            PermintaanHapus --> TampilData : Sukses / Batal
        }
        
        state TrainingModel {
            [*] --> KonfigurasiParameter
            KonfigurasiParameter --> ProsesTraining : Klik Mulai
            ProsesTraining --> HasilEvaluasi : Selesai
            HasilEvaluasi --> [*] : Kembali
        }
        
        state ProsesPrediksi {
            [*] --> InputDataPrediksi : Masukkan Parameter
            InputDataPrediksi --> ProsesRandomForest : Klik Prediksi
            ProsesRandomForest --> HasilPrediksi : Selesai
            HasilPrediksi --> TentukanRisiko : Cek Klasifikasi
            
            state TentukanRisiko <<choice>>
            TentukanRisiko --> RisikoRendah : < 12 kasus
            TentukanRisiko --> RisikoSedang : 12 - 17 kasus
            TentukanRisiko --> RisikoTinggi : >= 18 kasus
            
            RisikoRendah --> TampilRekomendasi
            RisikoSedang --> TampilRekomendasi
            RisikoTinggi --> TampilRekomendasi
            TampilRekomendasi --> [*] : Kembali
        }
        
        ManajemenData --> MenampilkanStatistik : Kembali
        TrainingModel --> MenampilkanStatistik : Kembali
        ProsesPrediksi --> MenampilkanStatistik : Kembali
        EvaluasiModel --> MenampilkanStatistik : Kembali
    }
    
    Dashboard --> LogoutState : Klik Logout
    LogoutState : Do / Hapus Session
    LogoutState --> Idle : Selesai
```

---

## 6. Deployment Diagram (Gambar 4.38)
Diagram deployment fisik yang menggambarkan topologi hardware, middleware, server web (Apache/Python), database (MySQL), dan protokol komunikasi yang digunakan.

```mermaid
graph TB
    subgraph ClientNode ["&laquo;device&raquo;<br/>Client Device (PC/Laptop/Mobile)"]
        subgraph WebBrowser ["&laquo;execution environment&raquo;<br/>Web Browser"]
            HTML["HTML5 + CSS3"]
            JS["JavaScript (ES6+)"]
            ChartJS["Chart.js Library"]
        end
    end

    subgraph AppServerNode ["&laquo;device&raquo;<br/>Application Server"]
        subgraph PythonEnv ["&laquo;execution environment&raquo;<br/>Python 3.8+ Environment"]
            Flask["Flask Web Framework"]
            MLEngine["Machine Learning Engine (Random Forest)"]
            SQLAlchemy["SQLAlchemy ORM"]
            RouteHandlers["Route Handlers"]
            Jinja2["Jinja2 Template Engine"]
        end
    end

    subgraph DBServerNode ["&laquo;device&raquo;<br/>Database Server"]
        subgraph MySQLEnv ["&laquo;execution environment&raquo;<br/>MySQL DBMS"]
            DatabaseSchema["Database: db_prediksi_dbd"]
            Tables["Tables:<br/>- users<br/>- pasien_dbd<br/>- wilayah<br/>- kasus_bulanan<br/>- hasil_prediksi<br/>- model_evaluasi<br/>- log_aktivitas"]
        end
    end

    subgraph CDNNode ["&laquo;device&raquo;<br/>Content Delivery Network (CDN)"]
        Assets["Static Assets:<br/>- Boxicons CDN<br/>- Google Fonts CDN"]
    end

    %% Communication Paths with Protocols (Astah Standard)
    WebBrowser -- "HTTPS / HTTP (Port 5000)" --> Flask
    WebBrowser -- "HTTP GET (Static Styles & Icons)" --> CDNNode
    
    %% Internal App Server Links
    RouteHandlers --> Jinja2
    RouteHandlers --> MLEngine
    RouteHandlers --> SQLAlchemy
    
    %% Server to Database connection
    SQLAlchemy -- "TCP/IP Connection (PyMySQL Port 3306)" --> DatabaseSchema
```
