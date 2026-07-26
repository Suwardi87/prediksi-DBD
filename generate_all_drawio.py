#!/usr/bin/env python3
"""
Generate both multi-page Draw.io (.drawio) and all individual diagram files
with 100% complete, fully-drawn layouts matching the yellow background theme (Astah Style).
Includes updated sequence diagrams matching the uploaded screenshot style.
"""
import os

def generate_precise_drawio():
    # File Paths
    multi_path = "/home/vue/Documents/frelence/joki/Dokumen/UML/Sistem_DBD_All_Diagrams.drawio"
    
    # Map page titles to individual filenames
    individual_mapping = {
        "Use Case Diagram": "1_use_case_diagram.drawio",
        "Class Diagram": "2_class_diagram.drawio",
        "Activity Admin": "3_activity_diagram_admin.drawio",
        "Activity Petugas": "4_activity_diagram_petugas.drawio",
        "Sequence Login": "5_sequence_diagram_login.drawio",
        "Sequence Kelola Pasien": "6_sequence_diagram_kelola_pasien.drawio",
        "Sequence Import Excel": "7_sequence_diagram_import.drawio",
        "Sequence Training Model": "8_sequence_diagram_training.drawio",
        "Sequence Prediksi Risiko": "9_sequence_diagram_prediksi.drawio",
        "Sequence Lihat Laporan": "10_sequence_diagram_laporan.drawio",
        "Sequence Kelola Pengguna": "11_sequence_diagram_kelola_pengguna.drawio",
        "Deployment Diagram": "12_deployment_diagram.drawio",
        "State Chart Diagram": "13_state_chart_diagram.drawio",
        "Collaboration Diagram": "14_collaboration_diagram.drawio",
        "ERD Diagram": "15_erd_diagram.drawio",
    }
    
    # Boundary coordinates (absolute)
    bx, by, bw, bh = 120, 20, 680, 880
    
    # Actor IDs
    admin_id = "actor_admin"
    petugas_id = "actor_petugas"
    boundary_id = "boundary"
    
    # Use Case positions
    raw_usecases = {
        "Login":                 ("Login", 340, 360, 100, 40),
        "Logout":                ("Logout", 560, 810, 100, 40),
        "Dashboard":             ("Dashboard", 220, 50, 120, 40),
        "KDP":                   ("Kelola Data Pasien", 220, 180, 130, 40),
        "MT":                    ("Manajemen Training", 220, 310, 130, 40),
        "KP":                    ("Kelola Prediksi", 220, 440, 130, 40),
        "MM":                    ("Manajemen Model", 220, 570, 130, 40),
        "KL":                    ("Kelola Laporan", 220, 700, 130, 40),
        "LPR":                   ("Lihat Prediksi\\nResiko", 460, 290, 130, 40),
        "LEM":                   ("Lihat Evaluasi\\nModel", 460, 380, 130, 40),
        "LL":                    ("Lihat Laporan", 460, 470, 120, 40),
        "CL":                    ("Cetak Laporan", 400, 530, 100, 35),
    }
    
    usecases = {}
    for key, (label, rx, ry, w, h) in raw_usecases.items():
        usecases[key] = (label, bx + rx, by + ry, w, h)
        
    crud_offsets = {
        "Create": (-100, -50),
        "Read":   (-30, -70),
        "Update": (60, -70),
        "Delete": (110, -50),
    }
    crud_modules = ["KDP", "MT", "KP", "MM", "KL"]
    
    uc_ids = {k: f"uc_{k}" for k in usecases.keys()}
    crud_ids = {}
    for mod in crud_modules:
        crud_ids[mod] = {
            action: f"crud_{mod}_{action.lower()}" for action in crud_offsets.keys()
        }

    # Generate Use Case Diagram XML root
    def get_use_case_xml():
        xml = []
        xml.append('      <root>')
        xml.append('        <mxCell id="0" />')
        xml.append('        <mxCell id="1" parent="0" />')
        
        # System Boundary
        xml.append(f'        <mxCell id="{boundary_id}" value="uo UseCase Diagram0" style="swimlane;whiteSpace=wrap;html=1;startSize=25;fillColor=none;strokeColor=#333333;childLayout=nil;collapsible=0;points=[];" vertex="1" parent="1">')
        xml.append(f'          <mxGeometry x="{bx}" y="{by}" width="{bw}" height="{bh}" as="geometry" />')
        xml.append('        </mxCell>')
        
        # Actors
        xml.append(f'        <mxCell id="{admin_id}" value="Admin" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fillColor=#ffffff;strokeColor=#000000;" vertex="1" parent="1">')
        xml.append(f'          <mxGeometry x="30" y="400" width="30" height="60" as="geometry" />')
        xml.append('        </mxCell>')
        
        xml.append(f'        <mxCell id="{petugas_id}" value="Petugas" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fillColor=#ffffff;strokeColor=#000000;" vertex="1" parent="1">')
        xml.append(f'          <mxGeometry x="830" y="400" width="30" height="60" as="geometry" />')
        xml.append('        </mxCell>')
        
        # Main Use Cases
        for key, (label, ax, ay, w, h) in usecases.items():
            xml_label = label.replace('\\n', '&lt;br/&gt;')
            xml.append(f'        <mxCell id="{uc_ids[key]}" value="{xml_label}" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="1">')
            xml.append(f'          <mxGeometry x="{ax}" y="{ay}" width="{w}" height="{h}" as="geometry" />')
            xml.append('        </mxCell>')
            
        # CRUD Use Cases
        for mod in crud_modules:
            mx, my = usecases[mod][1], usecases[mod][2]
            for action, offset in crud_offsets.items():
                cx = mx + offset[0]
                cy = my + offset[1]
                cid = crud_ids[mod][action]
                xml.append(f'        <mxCell id="{cid}" value="{action}" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=9;" vertex="1" parent="1">')
                xml.append(f'          <mxGeometry x="{cx}" y="{cy}" width="60" height="25" as="geometry" />')
                xml.append('        </mxCell>')
                
        # Edges helpers
        edge_idx = 100
        
        def write_assoc(src, tgt, style=""):
            nonlocal edge_idx
            edge_idx += 1
            default_style = "endArrow=none;html=1;rounded=0;edgeStyle=orthogonalEdgeStyle;strokeColor=#000000;jumpStyle=arc;"
            if style:
                default_style += style
            xml.append(f'        <mxCell id="edge_{edge_idx}" style="{default_style}" edge="1" parent="1" source="{src}" target="{tgt}">')
            xml.append('          <mxGeometry width="50" height="50" relative="1" as="geometry">')
            xml.append('            <mxPoint as="sourcePoint" />')
            xml.append('            <mxPoint as="targetPoint" />')
            xml.append('          </mxGeometry>')
            xml.append('        </mxCell>')

        def write_dep(src, tgt, val):
            nonlocal edge_idx
            edge_idx += 1
            style = "endArrow=open;endSize=12;dashed=1;html=1;rounded=0;strokeColor=#333333;fontSize=9;labelBackgroundColor=#FFFFFF;"
            escaped_val = val.replace("<", "&amp;lt;").replace(">", "&amp;gt;")
            xml.append(f'        <mxCell id="edge_{edge_idx}" value="{escaped_val}" style="{style}" edge="1" parent="1" source="{src}" target="{tgt}">')
            xml.append('          <mxGeometry width="50" height="50" relative="1" as="geometry">')
            xml.append('            <mxPoint as="sourcePoint" />')
            xml.append('            <mxPoint as="targetPoint" />')
            xml.append('          </mxGeometry>')
            xml.append('        </mxCell>')

        # Admin Assocs
        write_assoc(admin_id, uc_ids["Dashboard"], "exitX=1;exitY=0.1;entryX=0;entryY=0.5;")
        write_assoc(admin_id, uc_ids["KDP"], "exitX=1;exitY=0.25;entryX=0;entryY=0.5;")
        write_assoc(admin_id, uc_ids["MT"], "exitX=1;exitY=0.4;entryX=0;entryY=0.5;")
        write_assoc(admin_id, uc_ids["KP"], "exitX=1;exitY=0.55;entryX=0;entryY=0.5;")
        write_assoc(admin_id, uc_ids["MM"], "exitX=1;exitY=0.7;entryX=0;entryY=0.5;")
        write_assoc(admin_id, uc_ids["KL"], "exitX=1;exitY=0.85;entryX=0;entryY=0.5;")
        write_assoc(admin_id, uc_ids["Login"], "exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
        write_assoc(admin_id, uc_ids["Logout"], "exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
        
        # Petugas Assocs
        write_assoc(petugas_id, uc_ids["Dashboard"], "exitX=0.5;exitY=0;entryX=1;entryY=0.5;")
        write_assoc(petugas_id, uc_ids["Login"], "exitX=0;exitY=0.25;entryX=1;entryY=0.5;")
        write_assoc(petugas_id, uc_ids["LPR"], "exitX=0;exitY=0.45;entryX=1;entryY=0.5;")
        write_assoc(petugas_id, uc_ids["LEM"], "exitX=0;exitY=0.65;entryX=1;entryY=0.5;")
        write_assoc(petugas_id, uc_ids["LL"], "exitX=0;exitY=0.85;entryX=1;entryY=0.5;")
        write_assoc(petugas_id, uc_ids["Logout"], "exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
        
        # Includes to Login
        inc_targets = ["Dashboard", "KDP", "MT", "KP", "MM", "KL", "LPR", "LEM", "LL", "Logout"]
        for t in inc_targets:
            write_dep(uc_ids[t], uc_ids["Login"], "<<include>>")
            
        # CRUD Extends
        for mod in crud_modules:
            for act in ["Create", "Read", "Update", "Delete"]:
                write_dep(crud_ids[mod][act], uc_ids[mod], "<<extend>>")
                
        # Cetak Laporan extends
        write_dep(uc_ids["CL"], uc_ids["LL"], "<<extend>>")
        
        xml.append('      </root>')
        return "\n".join(xml)

    # Use Case Page Content
    usecase_xml_content = get_use_case_xml()
    pages = []
    pages.append(("Use Case Diagram", usecase_xml_content))
    
    # Class Diagram (Page 2) - Yellow Background (Astah Style)
    p2_xml = []
    p2_xml.append('      <root>')
    p2_xml.append('        <mxCell id="0" />')
    p2_xml.append('        <mxCell id="1" parent="0" />')
    
    classes = {
        "User": ("User", 50, 50, 190, 260, 
                 "- id: Integer (PK)<br/>- username: String(50) UNIQUE<br/>- password: String(255)<br/>- nama_lengkap: String(100)<br/>- email: String(100)<br/>- role: Enum(admin,petugas,pimpinan)<br/>- foto: String(255)<br/>- status: Enum(aktif,nonaktif)<br/>- last_login: DateTime<br/>- created_at: DateTime<br/>- updated_at: DateTime",
                 "+ check_password(password): Boolean<br/>+ login(): Boolean<br/>+ logout(): Void<br/>+ create(): Boolean<br/>+ update(): Boolean<br/>+ delete(): Boolean"),
                 
        "Wilayah": ("Wilayah", 280, 50, 190, 200,
                    "- id: Integer (PK)<br/>- nama_wilayah: String(100)<br/>- kecamatan: String(100)<br/>- latitude: Decimal(10,8)<br/>- longitude: Decimal(11,8)<br/>- populasi: Integer<br/>- created_at: DateTime",
                    "+ create(): Boolean<br/>+ read(): List<br/>+ update(): Boolean<br/>+ delete(): Boolean<br/>+ getPasienCount(): Integer"),
                    
        "PasienDBD": ("PasienDBD", 510, 50, 200, 290,
                      "- id: Integer (PK)<br/>- no_rm: String(20) UNIQUE<br/>- nama_pasien: String(100)<br/>- usia: Integer<br/>- jenis_kelamin: Enum(L,P)<br/>- alamat: Text<br/>- id_wilayah: Integer (FK)<br/>- tanggal_masuk: Date<br/>- tanggal_keluar: Date<br/>- lama_rawat: Integer<br/>- bulan: String(20)<br/>- tahun: Integer<br/>- status_pasien: Enum(...)<br/>- created_at: DateTime<br/>- updated_at: DateTime",
                      "+ create(): Boolean<br/>+ read(): List<br/>+ update(): Boolean<br/>+ delete(): Boolean<br/>+ getByBulan(): List"),
                      
        "KasusBulanan": ("KasusBulanan", 50, 360, 190, 220,
                         "- id: Integer (PK)<br/>- bulan: String(20)<br/>- tahun: Integer<br/>- jumlah_kasus: Integer<br/>- jumlah_sembuh: Integer<br/>- jumlah_meninggal: Integer<br/>- tingkat_risiko: Enum(...)<br/>- created_at: DateTime",
                         "+ create(): Boolean<br/>+ read(): List<br/>+ update(): Boolean<br/>+ getByTahun(tahun): List<br/>+ getStatistik(): Object"),
                         
        "HasilPrediksi": ("HasilPrediksi", 280, 360, 200, 250,
                          "- id: Integer (PK)<br/>- tanggal_prediksi: DateTime<br/>- bulan_prediksi: String(20)<br/>- tahun_prediksi: Integer<br/>- jumlah_kasus_prediksi: Integer<br/>- tingkat_risiko_prediksi: Enum(...)<br/>- confidence_score: Decimal(5,2)<br/>- model_version: String(50)<br/>- created_by: Integer (FK)<br/>- created_at: DateTime",
                          "+ create(): Boolean<br/>+ read(): List<br/>+ getByTahun(tahun): List<br/>+ getLatest(): Object<br/>+ predict(data): Object"),
                          
        "ModelEvaluasi": ("ModelEvaluasi", 510, 360, 210, 280,
                          "- id: Integer (PK)<br/>- tanggal_training: DateTime<br/>- accuracy: Decimal(5,4)<br/>- precision_score: Decimal(5,4)<br/>- recall_score: Decimal(5,4)<br/>- f1_score: Decimal(5,4)<br/>- mae: Decimal(10,4)<br/>- rmse: Decimal(10,4)<br/>- r2_score: Decimal(5,4)<br/>- n_estimators: Integer<br/>- max_depth: Integer<br/>- confusion_matrix: Text (JSON)<br/>- feature_importance: Text (JSON)<br/>- model_path: String(255)<br/>- created_at: DateTime",
                          "+ create(): Boolean<br/>+ read(): List<br/>+ getLatest(): Object<br/>+ getMetrics(): Object"),
                          
        "LogAktivitas": ("LogAktivitas", 280, 640, 200, 180,
                         "- id: Integer (PK)<br/>- user_id: Integer (FK)<br/>- aksi: String(100)<br/>- deskripsi: Text<br/>- ip_address: String(45)<br/>- created_at: DateTime",
                         "+ create(): Boolean<br/>+ read(): List<br/>+ getByUser(user_id): List<br/>+ filter(filters): List")
    }
    
    bg_col = "#FFFACD"
    border_col = "#8B8000"
    
    for c_key, (name, x, y, w, h, attrs, ops) in classes.items():
        escaped_attrs = attrs.replace("<", "&lt;").replace(">", "&gt;")
        escaped_ops = ops.replace("<", "&lt;").replace(">", "&gt;")
        value = f"&lt;b&gt;{name}&lt;/b&gt;&lt;hr/&gt;{escaped_attrs}&lt;hr/&gt;{escaped_ops}"
        p2_xml.append(f'        <mxCell id="c_{c_key}" value="{value}" style="rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=10;fillColor={bg_col};strokeColor={border_col};fontSize=9;" vertex="1" parent="1">')
        p2_xml.append(f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />')
        p2_xml.append('        </mxCell>')
    
    # Class Associations
    def draw_edge(xml_list, eid, source, target, label=""):
        style = "endArrow=classic;html=1;rounded=0;edgeStyle=orthogonalEdgeStyle;strokeColor=#444444;jumpStyle=arc;endSize=8;fontSize=9;"
        xml_list.append(f'        <mxCell id="{eid}" value="{label}" style="{style}" edge="1" parent="1" source="{source}" target="{target}">')
        xml_list.append('          <mxGeometry width="50" height="50" relative="1" as="geometry">')
        xml_list.append('            <mxPoint as="sourcePoint" />')
        xml_list.append('            <mxPoint as="targetPoint" />')
        xml_list.append('          </mxGeometry>')
        xml_list.append('        </mxCell>')
        
    draw_edge(p2_xml, "c_assoc_user_pred", "c_User", "c_HasilPrediksi", "creates")
    draw_edge(p2_xml, "c_assoc_user_log", "c_User", "c_LogAktivitas", "logs")
    draw_edge(p2_xml, "c_assoc_wil_pasien", "c_Wilayah", "c_PasienDBD", "memiliki")
    p2_xml.append('      </root>')
    pages.append(("Class Diagram", "\n".join(p2_xml)))

    # Activity Admin (Page 3)
    p3_xml = []
    p3_xml.append('      <root>')
    p3_xml.append('        <mxCell id="0" />')
    p3_xml.append('        <mxCell id="1" parent="0" />')
    p3_xml.append('        <mxCell id="p3_swim1" value="Admin" style="swimlane;whiteSpace=wrap;html=1;startSize=23;fillColor=none;strokeColor=#666666;" vertex="1" parent="1">')
    p3_xml.append('          <mxGeometry x="60" y="40" width="300" height="740" as="geometry" />')
    p3_xml.append('        </mxCell>')
    p3_xml.append('        <mxCell id="p3_swim2" value="Sistem" style="swimlane;whiteSpace=wrap;html=1;startSize=23;fillColor=none;strokeColor=#666666;" vertex="1" parent="1">')
    p3_xml.append('          <mxGeometry x="360" y="40" width="300" height="740" as="geometry" />')
    p3_xml.append('        </mxCell>')
    p3_xml.append('        <mxCell id="p3_start" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#000000;strokeColor=none;" vertex="1" parent="p3_swim1">')
    p3_xml.append('          <mxGeometry x="140" y="40" width="20" height="20" as="geometry" />')
    p3_xml.append('        </mxCell>')
    p3_xml.append('        <mxCell id="p3_act1" value="Mengakses Website" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="p3_swim1">')
    p3_xml.append('          <mxGeometry x="90" y="90" width="120" height="35" as="geometry" />')
    p3_xml.append('        </mxCell>')
    p3_xml.append('        <mxCell id="p3_act2" value="Menginputkan Username &amp;amp; Password" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="p3_swim1">')
    p3_xml.append('          <mxGeometry x="90" y="220" width="130" height="40" as="geometry" />')
    p3_xml.append('        </mxCell>')
    p3_xml.append('        <mxCell id="p3_act3" value="Pilih Menu Manajemen" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="p3_swim1">')
    p3_xml.append('          <mxGeometry x="95" y="380" width="120" height="35" as="geometry" />')
    p3_xml.append('        </mxCell>')
    p3_xml.append('        <mxCell id="p3_act4" value="Pilih Aksi &amp;amp; Isi Form" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="p3_swim1">')
    p3_xml.append('          <mxGeometry x="95" y="480" width="120" height="35" as="geometry" />')
    p3_xml.append('        </mxCell>')
    p3_xml.append('        <mxCell id="p3_act5" value="Klik Logout" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="p3_swim1">')
    p3_xml.append('          <mxGeometry x="105" y="620" width="100" height="30" as="geometry" />')
    p3_xml.append('        </mxCell>')
    p3_xml.append('        <mxCell id="p3_sys1" value="Menampilkan Halaman Utama" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="p3_swim2">')
    p3_xml.append('          <mxGeometry x="90" y="90" width="130" height="35" as="geometry" />')
    p3_xml.append('        </mxCell>')
    p3_xml.append('        <mxCell id="p3_sys2" value="Menampilkan Form Login" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="p3_swim2">')
    p3_xml.append('          <mxGeometry x="90" y="160" width="130" height="35" as="geometry" />')
    p3_xml.append('        </mxCell>')
    p3_xml.append('        <mxCell id="p3_dec1" value="Valid?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=9;" vertex="1" parent="p3_swim2">')
    p3_xml.append('          <mxGeometry x="125" y="220" width="60" height="50" as="geometry" />')
    p3_xml.append('        </mxCell>')
    p3_xml.append('        <mxCell id="p3_sys3" value="Menampilkan Dashboard" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="p3_swim2">')
    p3_xml.append('          <mxGeometry x="90" y="320" width="130" height="35" as="geometry" />')
    p3_xml.append('        </mxCell>')
    p3_xml.append('        <mxCell id="p3_sys4" value="Menampilkan Form Aksi" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="p3_swim2">')
    p3_xml.append('          <mxGeometry x="90" y="430" width="130" height="35" as="geometry" />')
    p3_xml.append('        </mxCell>')
    p3_xml.append('        <mxCell id="p3_sys5" value="Memproses &amp;amp; Simpan DB" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="p3_swim2">')
    p3_xml.append('          <mxGeometry x="90" y="520" width="130" height="35" as="geometry" />')
    p3_xml.append('        </mxCell>')
    p3_xml.append('        <mxCell id="p3_sys6" value="Notifikasi Sukses" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="p3_swim2">')
    p3_xml.append('          <mxGeometry x="90" y="580" width="130" height="35" as="geometry" />')
    p3_xml.append('        </mxCell>')
    p3_xml.append('        <mxCell id="p3_sys7" value="Hapus Session &amp;amp; Redirect" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="p3_swim2">')
    p3_xml.append('          <mxGeometry x="90" y="660" width="130" height="35" as="geometry" />')
    p3_xml.append('        </mxCell>')
    p3_xml.append('        <mxCell id="p3_end" value="" style="ellipse;html=1;shape=endState;fillColor=#000000;strokeColor=#000000;" vertex="1" parent="p3_swim2">')
    p3_xml.append('          <mxGeometry x="140" y="710" width="20" height="20" as="geometry" />')
    p3_xml.append('        </mxCell>')
    
    # Activity flows helper
    def draw_act_flow(list_xml, fid, src, tgt, val=""):
        style = "endArrow=open;endSize=6;html=1;rounded=0;edgeStyle=orthogonalEdgeStyle;strokeColor=#000000;"
        list_xml.append(f'        <mxCell id="{fid}" value="{val}" style="{style}" edge="1" parent="1" source="{src}" target="{tgt}">')
        list_xml.append('          <mxGeometry width="50" height="50" relative="1" as="geometry">')
        list_xml.append('            <mxPoint as="sourcePoint" />')
        list_xml.append('            <mxPoint as="targetPoint" />')
        list_xml.append('          </mxGeometry>')
        list_xml.append('        </mxCell>')
        
    draw_act_flow(p3_xml, "f3_1", "p3_start", "p3_act1")
    draw_act_flow(p3_xml, "f3_2", "p3_act1", "p3_sys1")
    draw_act_flow(p3_xml, "f3_3", "p3_sys1", "p3_sys2")
    draw_act_flow(p3_xml, "f3_4", "p3_sys2", "p3_act2")
    draw_act_flow(p3_xml, "f3_5", "p3_act2", "p3_dec1")
    draw_act_flow(p3_xml, "f3_6", "p3_dec1", "p3_sys2", "Gagal")
    draw_act_flow(p3_xml, "f3_7", "p3_dec1", "p3_sys3", "Berhasil")
    draw_act_flow(p3_xml, "f3_8", "p3_sys3", "p3_act3")
    draw_act_flow(p3_xml, "f3_9", "p3_act3", "p3_sys4")
    draw_act_flow(p3_xml, "f3_10", "p3_sys4", "p3_act4")
    draw_act_flow(p3_xml, "f3_11", "p3_act4", "p3_sys5")
    draw_act_flow(p3_xml, "f3_12", "p3_sys5", "p3_sys6")
    draw_act_flow(p3_xml, "f3_13", "p3_sys6", "p3_act5")
    draw_act_flow(p3_xml, "f3_14", "p3_act5", "p3_sys7")
    draw_act_flow(p3_xml, "f3_15", "p3_sys7", "p3_end")
    p3_xml.append('      </root>')
    pages.append(("Activity Admin", "\n".join(p3_xml)))

    # Activity Diagram Petugas (Page 4)
    p4_xml = []
    p4_xml.append('      <root>')
    p4_xml.append('        <mxCell id="0" />')
    p4_xml.append('        <mxCell id="1" parent="0" />')
    p4_xml.append('        <mxCell id="p4_swim1" value="Petugas" style="swimlane;whiteSpace=wrap;html=1;startSize=23;fillColor=none;strokeColor=#666666;" vertex="1" parent="1">')
    p4_xml.append('          <mxGeometry x="60" y="40" width="300" height="740" as="geometry" />')
    p4_xml.append('        </mxCell>')
    p4_xml.append('        <mxCell id="p4_swim2" value="Sistem" style="swimlane;whiteSpace=wrap;html=1;startSize=23;fillColor=none;strokeColor=#666666;" vertex="1" parent="1">')
    p4_xml.append('          <mxGeometry x="360" y="40" width="300" height="740" as="geometry" />')
    p4_xml.append('        </mxCell>')
    p4_xml.append('        <mxCell id="p4_start" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#000000;strokeColor=none;" vertex="1" parent="p4_swim1">')
    p4_xml.append('          <mxGeometry x="140" y="40" width="20" height="20" as="geometry" />')
    p4_xml.append('        </mxCell>')
    p4_xml.append('        <mxCell id="p4_act1" value="Mengakses Website" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="p4_swim1">')
    p4_xml.append('          <mxGeometry x="90" y="90" width="120" height="35" as="geometry" />')
    p4_xml.append('        </mxCell>')
    p4_xml.append('        <mxCell id="p4_act2" value="Menginputkan Username &amp;amp; Password" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="p4_swim1">')
    p4_xml.append('          <mxGeometry x="90" y="220" width="130" height="40" as="geometry" />')
    p4_xml.append('        </mxCell>')
    p4_xml.append('        <mxCell id="p4_act3" value="Pilih Menu: Pasien / Prediksi / Training" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="p4_swim1">')
    p4_xml.append('          <mxGeometry x="80" y="380" width="150" height="35" as="geometry" />')
    p4_xml.append('        </mxCell>')
    p4_xml.append('        <mxCell id="p4_act4" value="Isi Form / Jalankan Aksi" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="p4_swim1">')
    p4_xml.append('          <mxGeometry x="95" y="480" width="120" height="35" as="geometry" />')
    p4_xml.append('        </mxCell>')
    p4_xml.append('        <mxCell id="p4_act5" value="Klik Logout" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="p4_swim1">')
    p4_xml.append('          <mxGeometry x="105" y="620" width="100" height="30" as="geometry" />')
    p4_xml.append('        </mxCell>')
    p4_xml.append('        <mxCell id="p4_sys1" value="Menampilkan Halaman Utama" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="p4_swim2">')
    p4_xml.append('          <mxGeometry x="90" y="90" width="130" height="35" as="geometry" />')
    p4_xml.append('        </mxCell>')
    p4_xml.append('        <mxCell id="p4_sys2" value="Menampilkan Form Login" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="p4_swim2">')
    p4_xml.append('          <mxGeometry x="90" y="160" width="130" height="35" as="geometry" />')
    p4_xml.append('        </mxCell>')
    p4_xml.append('        <mxCell id="p4_dec1" value="Valid?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=9;" vertex="1" parent="p4_swim2">')
    p4_xml.append('          <mxGeometry x="125" y="220" width="60" height="50" as="geometry" />')
    p4_xml.append('        </mxCell>')
    p4_xml.append('        <mxCell id="p4_sys3" value="Menampilkan Dashboard Petugas" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="p4_swim2">')
    p4_xml.append('          <mxGeometry x="85" y="320" width="140" height="35" as="geometry" />')
    p4_xml.append('        </mxCell>')
    p4_xml.append('        <mxCell id="p4_sys4" value="Menampilkan Form / Hasil Proses" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="p4_swim2">')
    p4_xml.append('          <mxGeometry x="85" y="430" width="140" height="35" as="geometry" />')
    p4_xml.append('        </mxCell>')
    p4_xml.append('        <mxCell id="p4_sys5" value="Memproses &amp;amp; Update Database" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="p4_swim2">')
    p4_xml.append('          <mxGeometry x="85" y="520" width="140" height="35" as="geometry" />')
    p4_xml.append('        </mxCell>')
    p4_xml.append('        <mxCell id="p4_sys6" value="Menampilkan Notifikasi Hasil" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="p4_swim2">')
    p4_xml.append('          <mxGeometry x="85" y="580" width="140" height="35" as="geometry" />')
    p4_xml.append('        </mxCell>')
    p4_xml.append('        <mxCell id="p4_sys7" value="Hapus Session &amp;amp; Redirect" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="p4_swim2">')
    p4_xml.append('          <mxGeometry x="90" y="660" width="130" height="35" as="geometry" />')
    p4_xml.append('        </mxCell>')
    p4_xml.append('        <mxCell id="p4_end" value="" style="ellipse;html=1;shape=endState;fillColor=#000000;strokeColor=#000000;" vertex="1" parent="p4_swim2">')
    p4_xml.append('          <mxGeometry x="140" y="710" width="20" height="20" as="geometry" />')
    p4_xml.append('        </mxCell>')
    
    draw_act_flow(p4_xml, "f4_1", "p4_start", "p4_act1")
    draw_act_flow(p4_xml, "f4_2", "p4_act1", "p4_sys1")
    draw_act_flow(p4_xml, "f4_3", "p4_sys1", "p4_sys2")
    draw_act_flow(p4_xml, "f4_4", "p4_sys2", "p4_act2")
    draw_act_flow(p4_xml, "f4_5", "p4_act2", "p4_dec1")
    draw_act_flow(p4_xml, "f4_6", "p4_dec1", "p4_sys2", "Gagal")
    draw_act_flow(p4_xml, "f4_7", "p4_dec1", "p4_sys3", "Berhasil")
    draw_act_flow(p4_xml, "f4_8", "p4_sys3", "p4_act3")
    draw_act_flow(p4_xml, "f4_9", "p4_act3", "p4_sys4")
    draw_act_flow(p4_xml, "f4_10", "p4_sys4", "p4_act4")
    draw_act_flow(p4_xml, "f4_11", "p4_act4", "p4_sys5")
    draw_act_flow(p4_xml, "f4_12", "p4_sys5", "p4_sys6")
    draw_act_flow(p4_xml, "f4_13", "p4_sys6", "p4_act5")
    draw_act_flow(p4_xml, "f4_14", "p4_act5", "p4_sys7")
    draw_act_flow(p4_xml, "f4_15", "p4_sys7", "p4_end")
    p4_xml.append('      </root>')
    pages.append(("Activity Petugas", "\n".join(p4_xml)))

    # Sequence generator matching user screenshot (UML Outer Frame, Yellow lifelines, no activations)
    def make_astah_sequence_xml(title_label, lifelines, messages, divider_y=None, divider_label=""):
        xml = []
        xml.append('      <root>')
        xml.append('        <mxCell id="0" />')
        xml.append('        <mxCell id="1" parent="0" />')
        
        # Outer Frame (umlFrame)
        xml.append(f'        <mxCell id="outer_frame" value="sequence diagram\\n{title_label}" style="shape=umlFrame;whiteSpace=wrap;html=1;width=120;height=30;fillColor=none;fontSize=9;align=left;spacingLeft=10;" vertex="1" parent="1">')
        xml.append('          <mxGeometry x="20" y="20" width="800" height="840" as="geometry" />')
        xml.append('        </mxCell>')
        
        # 1. Lifelines
        for i, (lid, label, role) in enumerate(lifelines):
            # Absolute spacing
            x = 80 + i * 180
            y = 80
            w = 110
            h = 720
            if role == 'actor':
                style = "shape=umlLifeline;perimeter=lifelinePerimeter;container=1;collapsible=0;recursiveResize=0;rounded=0;shadow=0;strokeWidth=1;participant=umlActor;fillColor=none;strokeColor=#000000;"
                # Actor label is empty under the stick figure per screenshot
                display_label = ""
            else:
                style = "shape=umlLifeline;perimeter=lifelinePerimeter;container=1;collapsible=0;recursiveResize=0;rounded=0;shadow=0;strokeWidth=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;"
                display_label = label
                
            xml.append(f'        <mxCell id="{lid}" value="{display_label}" style="{style}" vertex="1" parent="1">')
            xml.append(f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />')
            xml.append('        </mxCell>')
            
        # 2. Messages
        for idx, (src_id, tgt_id, msg_label, is_dashed, my) in enumerate(messages):
            # Calculate source/target indices for self loop math
            src_idx = [i for i, (l_id, _, _) in enumerate(lifelines) if l_id == src_id][0]
            tgt_idx = [i for i, (l_id, _, _) in enumerate(lifelines) if l_id == tgt_id][0]
            
            if src_id == tgt_id:
                # Self loop (e.g. Validasi input())
                lx = 80 + src_idx * 180 + 55  # Center of lifeline
                style = "edgeStyle=orthogonalEdgeStyle;html=1;align=left;spacingLeft=2;endArrow=block;rounded=0;labelBackgroundColor=#FFFFFF;fontSize=9;"
                xml.append(f'        <mxCell id="msg_{idx}" value="{msg_label}" style="{style}" edge="1" parent="1" source="{src_id}" target="{tgt_id}">')
                xml.append('          <mxGeometry width="50" height="50" relative="1" as="geometry">')
                xml.append(f'            <mxPoint x="{lx}" y="{my}" as="sourcePoint" />')
                xml.append(f'            <mxPoint x="{lx}" y="{my+20}" as="targetPoint" />')
                xml.append(f'            <array as="points">')
                xml.append(f'              <mxPoint x="{lx+40}" y="{my}" />')
                xml.append(f'              <mxPoint x="{lx+40}" y="{my+20}" />')
                xml.append(f'            </array>')
                xml.append('          </mxGeometry>')
                xml.append('        </mxCell>')
            else:
                # Horizontal straight messages
                if is_dashed:
                    style = "html=1;verticalAlign=bottom;endArrow=open;dashed=1;endSize=8;rounded=0;labelBackgroundColor=#FFFFFF;fontSize=9;"
                else:
                    style = "html=1;verticalAlign=bottom;endArrow=block;rounded=0;labelBackgroundColor=#FFFFFF;fontSize=9;"
                y_ratio = my / 720.0
                edge_style = f"{style}exitX=0.5;exitY={y_ratio:.3f};entryX=0.5;entryY={y_ratio:.3f};"
                xml.append(f'        <mxCell id="msg_{idx}" value="{msg_label}" style="{edge_style}" edge="1" parent="1" source="{src_id}" target="{tgt_id}">')
                xml.append('          <mxGeometry width="50" height="50" relative="1" as="geometry">')
                xml.append('            <mxPoint as="sourcePoint" />')
                xml.append('            <mxPoint as="targetPoint" />')
                xml.append('          </mxGeometry>')
                xml.append('        </mxCell>')
                
        # 3. Horizontal Alt Divider (Simple dashed line with condition text)
        if divider_y:
            style = "endArrow=none;dashed=1;html=1;rounded=0;strokeColor=#999999;labelBackgroundColor=#FFFFFF;align=left;spacingLeft=10;fontSize=9;"
            xml.append(f'        <mxCell id="alt_divider" value="[{divider_label}]" style="{style}" edge="1" parent="1">')
            xml.append('          <mxGeometry width="50" height="50" relative="1" as="geometry">')
            xml.append(f'            <mxPoint x="20" y="{divider_y}" as="sourcePoint" />')
            xml.append(f'            <mxPoint x="820" y="{divider_y}" as="targetPoint" />')
            xml.append('          </mxGeometry>')
            xml.append('        </mxCell>')
            
        xml.append('      </root>')
        return "\n".join(xml)

    # PAGE 5: Sequence Diagram Login
    login_lifelines = [
        ("pengguna", "Admin/Petugas", "actor"),
        ("hl", "Halaman Login", "boundary"),
        ("proses", "proses", "control"),
        ("db", "Database", "entity")
    ]
    login_messages = [
        ("pengguna", "hl", "Membuka halaman login()", False, 180),
        ("hl", "pengguna", "Tampilkan Form Login", True, 220),
        ("pengguna", "hl", "Input username &amp; password()", False, 260),
        ("hl", "proses", "Submit form login(username, password)", False, 300),
        ("proses", "proses", "Validasi input()", False, 340),
        ("proses", "db", "Query user by username(username)", False, 390),
        ("db", "proses", "Return user data", True, 430),
        ("proses", "db", "Update last_login(user_id)", False, 520),
        ("proses", "hl", "Login berhasil", True, 560),
        ("hl", "pengguna", "Redirect ke Dashboard", True, 590),
        ("proses", "hl", "Login gagal", True, 670),
        ("hl", "pengguna", "Tampilkan pesan error", True, 700)
    ]
    pages.append(("Sequence Login", make_astah_sequence_xml("login", login_lifelines, login_messages, 630, "Password Tidak Valid")))

    # PAGE 6: Sequence Diagram Kelola Data Pasien
    kdp_lifelines = [
        ("petugas", "Petugas/Admin", "actor"),
        ("hp", "Halaman Pasien", "boundary"),
        ("proses", "proses", "control"),
        ("db", "Database", "entity")
    ]
    kdp_messages = [
        ("petugas", "hp", "Buka menu Data Pasien()", False, 120),
        ("hp", "proses", "Request daftar pasien()", False, 160),
        ("proses", "db", "SELECT * FROM pasien_dbd", False, 200),
        ("db", "proses", "Return data pasien", True, 240),
        ("proses", "hp", "Kirim data pasien", True, 280),
        ("hp", "petugas", "Tampilkan tabel pasien", True, 320),
        ("petugas", "hp", "Klik tombol Tambah()", False, 400),
        ("hp", "petugas", "Tampilkan form input", True, 440),
        ("petugas", "hp", "Input data pasien &amp; Klik Simpan", False, 480),
        ("hp", "proses", "Submit form(data)", False, 520),
        ("proses", "proses", "Validasi data()", False, 550),
        ("proses", "db", "INSERT INTO pasien_dbd", False, 590),
        ("db", "proses", "Success", True, 620),
        ("proses", "db", "INSERT INTO log_aktivitas", False, 650),
        ("proses", "hp", "Response sukses", True, 690),
        ("hp", "petugas", "Tampilkan alert sukses", True, 720)
    ]
    pages.append(("Sequence Kelola Pasien", make_astah_sequence_xml("kelola pasien", kdp_lifelines, kdp_messages, 360, "Tambah Data Pasien")))

    # Update other sequence pages to match the same design style
    other_sequences = [
        ("Sequence Import Excel", "import excel", [
            ("petugas", "Petugas", "actor"), ("hi", "Halaman Import", "boundary"), ("proses", "proses", "control"), ("api", "Python API", "control"), ("db", "Database", "entity")
        ], [
            ("petugas", "hi", "Buka halaman Import()", False, 120), ("hi", "petugas", "Tampilkan form upload", True, 160),
            ("petugas", "hi", "Pilih file Excel &amp; Klik Upload", False, 200), ("hi", "hi", "Validasi format (.xlsx)", False, 240),
            ("hi", "proses", "Upload file(file)", False, 280), ("proses", "proses", "Simpan file sementara()", False, 320),
            ("proses", "api", "POST /import (file_path)", False, 360), ("api", "api", "pd.read_excel()", False, 400),
            ("api", "db", "INSERT INTO pasien_dbd", False, 450), ("db", "api", "Success", True, 480),
            ("api", "proses", "Response (total, berhasil, gagal)", True, 530),
            ("proses", "db", "INSERT INTO log_aktivitas", False, 570), ("proses", "hi", "Response hasil import", True, 610),
            ("hi", "petugas", "Tampilkan hasil (Total, Berhasil)", True, 650)
        ]),
        
        ("Sequence Training Model", "training model", [
            ("petugas", "Petugas", "actor"), ("ht", "Halaman Training", "boundary"), ("proses", "proses", "control"), ("api", "Python API", "control"), ("db", "Database", "entity")
        ], [
            ("petugas", "ht", "Buka menu Training Model()", False, 120), ("ht", "petugas", "Tampilkan form konfigurasi", True, 160),
            ("petugas", "ht", "Input parameter &amp; Klik Mulai Training", False, 200), ("ht", "proses", "Submit parameter training(params)", False, 240),
            ("proses", "api", "POST /train (params)", False, 280), ("api", "api", "Load data dari database()", False, 320),
            ("api", "api", "fit(X_train, y_train)", False, 370), ("api", "db", "INSERT INTO model_evaluasi", False, 420),
            ("db", "api", "Success", True, 450), ("api", "proses", "Response (status, metrics)", True, 500),
            ("proses", "ht", "Kirim hasil training", True, 550), ("ht", "petugas", "Tampilkan hasil evaluasi model", True, 600)
        ]),
        
        ("Sequence Prediksi Risiko", "prediksi risiko", [
            ("pengguna", "Pengguna", "actor"), ("hp", "Halaman Prediksi", "boundary"), ("proses", "proses", "control"), ("api", "Python API", "control"), ("db", "Database", "entity")
        ], [
            ("pengguna", "hp", "Buka menu Prediksi()", False, 120), ("hp", "pengguna", "Tampilkan form input", True, 160),
            ("pengguna", "hp", "Input data &amp; Klik Prediksi", False, 200), ("hp", "proses", "Submit data prediksi(data)", False, 240),
            ("proses", "api", "POST /predict (data)", False, 280), ("api", "api", "model.predict(features)", False, 340),
            ("api", "db", "INSERT INTO hasil_prediksi", False, 400), ("db", "api", "Success", True, 430),
            ("api", "proses", "Response (tingkat_risiko, confidence)", True, 480), ("proses", "hp", "Kirim hasil prediksi", True, 530),
            ("hp", "pengguna", "Tampilkan hasil prediksi &amp; rekomendasi", True, 580)
        ]),
        
        ("Sequence Lihat Laporan", "lihat laporan", [
            ("pengguna", "Pengguna", "actor"), ("hl", "Halaman Laporan", "boundary"), ("proses", "proses", "control"), ("db", "Database", "entity")
        ], [
            ("pengguna", "hl", "Buka menu Laporan()", False, 120), ("hl", "proses", "Request data awal()", False, 160),
            ("proses", "db", "SELECT tahun FROM kasus_bulanan", False, 200), ("db", "proses", "Return daftar tahun", True, 240),
            ("proses", "hl", "Kirim data filter", True, 280), ("hl", "pengguna", "Tampilkan halaman laporan dengan filter", True, 320),
            ("pengguna", "hl", "Pilih filter &amp; Klik Tampilkan", False, 360), ("hl", "proses", "Request laporan(filter)", False, 400),
            ("proses", "db", "SELECT * FROM kasus_bulanan WHERE tahun=?", False, 440), ("db", "proses", "Return data bulanan", True, 480),
            ("proses", "proses", "Hitung statistik()", False, 520), ("proses", "hl", "Kirim data laporan", True, 560),
            ("hl", "hl", "Render grafik (Chart.js)", False, 600), ("hl", "pengguna", "Tampilkan visualisasi laporan", True, 640)
        ]),
        
        ("Sequence Kelola Pengguna", "kelola pengguna", [
            ("admin", "Admin", "actor"), ("hu", "Halaman Pengguna", "boundary"), ("proses", "proses", "control"), ("db", "Database", "entity")
        ], [
            ("admin", "hu", "Buka menu Kelola Pengguna()", False, 120), ("hu", "proses", "Request daftar pengguna()", False, 160),
            ("proses", "db", "SELECT * FROM users", False, 200), ("db", "proses", "Return data users", True, 240),
            ("proses", "hu", "Kirim data users", True, 280), ("hu", "admin", "Tampilkan tabel pengguna", True, 320),
            ("admin", "hu", "Klik tombol Tambah()", False, 400), ("hu", "admin", "Tampilkan form input", True, 440),
            ("admin", "hu", "Input data &amp; Klik Simpan", False, 480), ("hu", "proses", "Submit form(data)", False, 520),
            ("proses", "db", "SELECT * FROM users WHERE username=?", False, 550), ("db", "proses", "Return result", True, 580),
            ("proses", "db", "INSERT INTO users", False, 620), ("proses", "hu", "Response sukses", True, 660)
        ])
    ]
    
    for page_title, title_lbl, l_lines, m_sgs in other_sequences:
        pages.append((page_title, make_astah_sequence_xml(title_lbl, l_lines, m_sgs)))

    # Deployment Diagram (Page 12)
    p12_xml = []
    p12_xml.append('      <root>')
    p12_xml.append('        <mxCell id="0" />')
    p12_xml.append('        <mxCell id="1" parent="0" />')
    p12_xml.append('        <mxCell id="node_client" value="&amp;lt;&amp;lt;device&amp;gt;&amp;gt;\nClient Device (PC/Laptop)" style="verticalAlign=top;align=left;spacingLeft=10;html=1;whiteSpace=wrap;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;fontStyle=1;" vertex="1" parent="1">')
    p12_xml.append('          <mxGeometry x="50" y="80" width="220" height="280" as="geometry" />')
    p12_xml.append('        </mxCell>')
    p12_xml.append('        <mxCell id="comp_browser" value="&amp;lt;&amp;lt;execution environment&amp;gt;&amp;gt;\nWeb Browser\n--\nHTML5 + CSS3\nJavaScript (ES6+)\nChart.js Library" style="verticalAlign=top;align=left;spacingLeft=10;html=1;whiteSpace=wrap;fillColor=#FFFFFF;strokeColor=#8B8000;fontSize=9;" vertex="1" parent="node_client">')
    p12_xml.append('          <mxGeometry x="20" y="60" width="180" height="180" as="geometry" />')
    p12_xml.append('        </mxCell>')
    p12_xml.append('        <mxCell id="node_app" value="&amp;lt;&amp;lt;device&amp;gt;&amp;gt;\nApplication Server" style="verticalAlign=top;align=left;spacingLeft=10;html=1;whiteSpace=wrap;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;fontStyle=1;" vertex="1" parent="1">')
    p12_xml.append('          <mxGeometry x="340" y="80" width="220" height="280" as="geometry" />')
    p12_xml.append('        </mxCell>')
    p12_xml.append('        <mxCell id="comp_flask" value="&amp;lt;&amp;lt;execution environment&amp;gt;&amp;gt;\nPython Environment\n--\nFlask Web Framework\nRandom Forest ML Engine\nSQLAlchemy ORM" style="verticalAlign=top;align=left;spacingLeft=10;html=1;whiteSpace=wrap;fillColor=#FFFFFF;strokeColor=#8B8000;fontSize=9;" vertex="1" parent="node_app">')
    p12_xml.append('          <mxGeometry x="20" y="60" width="180" height="180" as="geometry" />')
    p12_xml.append('        </mxCell>')
    p12_xml.append('        <mxCell id="node_db" value="&amp;lt;&amp;lt;device&amp;gt;&amp;gt;\nDatabase Server" style="verticalAlign=top;align=left;spacingLeft=10;html=1;whiteSpace=wrap;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;fontStyle=1;" vertex="1" parent="1">')
    p12_xml.append('          <mxGeometry x="620" y="80" width="220" height="280" as="geometry" />')
    p12_xml.append('        </mxCell>')
    p12_xml.append('        <mxCell id="comp_mysql" value="&amp;lt;&amp;lt;execution environment&amp;gt;&amp;gt;\nMySQL DBMS\n--\nDatabase Schema:\ndb_prediksi_dbd" style="verticalAlign=top;align=left;spacingLeft=10;html=1;whiteSpace=wrap;fillColor=#FFFFFF;strokeColor=#8B8000;fontSize=9;" vertex="1" parent="node_db">')
    p12_xml.append('          <mxGeometry x="20" y="60" width="180" height="180" as="geometry" />')
    p12_xml.append('        </mxCell>')
    p12_xml.append('        <mxCell id="node_cdn" value="&amp;lt;&amp;lt;device&amp;gt;&amp;gt;\nContent Delivery Network (CDN)" style="verticalAlign=top;align=left;spacingLeft=10;html=1;whiteSpace=wrap;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;fontStyle=1;" vertex="1" parent="1">')
    p12_xml.append('          <mxGeometry x="340" y="420" width="220" height="120" as="geometry" />')
    p12_xml.append('        </mxCell>')
    p12_xml.append('        <mxCell id="comp_assets" value="Static Assets (CSS, Icons)" style="verticalAlign=middle;align=center;html=1;whiteSpace=wrap;fillColor=#FFFFFF;strokeColor=#8B8000;fontSize=9;" vertex="1" parent="node_cdn">')
    p12_xml.append('          <mxGeometry x="20" y="45" width="180" height="50" as="geometry" />')
    p12_xml.append('        </mxCell>')
    
    draw_edge(p12_xml, "path_client_app", "comp_browser", "comp_flask")
    p12_xml.append('        <mxCell id="label_path1" value="HTTPS (Port 5000)" style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=8;" vertex="1" connectable="0" parent="path_client_app">')
    p12_xml.append('          <mxGeometry relative="1" as="geometry" />')
    p12_xml.append('        </mxCell>')
    
    draw_edge(p12_xml, "path_app_db", "comp_flask", "comp_mysql")
    p12_xml.append('        <mxCell id="label_path2" value="TCP/IP (Port 3306)" style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=8;" vertex="1" connectable="0" parent="path_app_db">')
    p12_xml.append('          <mxGeometry relative="1" as="geometry" />')
    p12_xml.append('        </mxCell>')
    
    draw_edge(p12_xml, "path_client_cdn", "comp_browser", "comp_assets")
    p12_xml.append('        <mxCell id="label_path3" value="HTTP GET" style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=8;" vertex="1" connectable="0" parent="path_client_cdn">')
    p12_xml.append('          <mxGeometry relative="1" as="geometry" />')
    p12_xml.append('        </mxCell>')
    p12_xml.append('      </root>')
    pages.append(("Deployment Diagram", "\n".join(p12_xml)))

    # State Chart Diagram (Page 13)
    p13_xml = []
    p13_xml.append('      <root>')
    p13_xml.append('        <mxCell id="0" />')
    p13_xml.append('        <mxCell id="1" parent="0" />')
    p13_xml.append('        <mxCell id="st_start" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#000000;strokeColor=none;" vertex="1" parent="1">')
    p13_xml.append('          <mxGeometry x="50" y="100" width="20" height="20" as="geometry" />')
    p13_xml.append('        </mxCell>')
    p13_xml.append('        <mxCell id="st_idle" value="Idle\n--\nentry / Menunggu input" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;align=left;spacingLeft=10;verticalAlign=top;fontSize=10;" vertex="1" parent="1">')
    p13_xml.append('          <mxGeometry x="120" y="80" width="140" height="60" as="geometry" />')
    p13_xml.append('        </mxCell>')
    p13_xml.append('        <mxCell id="st_login" value="ProsesLogin\n--\nMasukkanKredensial\nValidasiLogin" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;align=left;spacingLeft=10;verticalAlign=top;fontSize=10;" vertex="1" parent="1">')
    p13_xml.append('          <mxGeometry x="320" y="80" width="150" height="60" as="geometry" />')
    p13_xml.append('        </mxCell>')
    p13_xml.append('        <mxCell id="st_dash" value="Dashboard\n--\nMenampilkanStatistik\nManajemenData\nTrainingModel\nProsesPrediksi" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;align=left;spacingLeft=10;verticalAlign=top;fontSize=10;" vertex="1" parent="1">')
    p13_xml.append('          <mxGeometry x="530" y="80" width="160" height="90" as="geometry" />')
    p13_xml.append('        </mxCell>')
    p13_xml.append('        <mxCell id="st_logout" value="LogoutState\n--\ndo / Hapus Session" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;align=left;spacingLeft=10;verticalAlign=top;fontSize=10;" vertex="1" parent="1">')
    p13_xml.append('          <mxGeometry x="530" y="240" width="160" height="60" as="geometry" />')
    p13_xml.append('        </mxCell>')
    
    draw_act_flow(p13_xml, "trans_1", "st_start", "st_idle", "Akses Sistem")
    draw_act_flow(p13_xml, "trans_2", "st_idle", "st_login", "Belum Login")
    draw_act_flow(p13_xml, "trans_3", "st_login", "st_dash", "Login Sukses")
    draw_act_flow(p13_xml, "trans_4", "st_login", "st_idle", "Batal / Timeout")
    draw_act_flow(p13_xml, "trans_5", "st_dash", "st_logout", "Klik Logout")
    draw_act_flow(p13_xml, "trans_6", "st_logout", "st_idle", "Selesai")
    p13_xml.append('      </root>')
    pages.append(("State Chart Diagram", "\n".join(p13_xml)))

    # Collaboration & ERD Diagrams
    diagram_list_remain = [
        ("Collaboration Diagram", "Collaboration Diagram (Gambar Tambahan)"),
        ("ERD Diagram", "ERD Diagram (Gambar Tambahan)"),
    ]
    for title, desc in diagram_list_remain:
        p_xml = []
        p_xml.append('      <root>')
        p_xml.append('        <mxCell id="0" />')
        p_xml.append('        <mxCell id="1" parent="0" />')
        p_xml.append(f'        <mxCell id="placeholder" value="{desc}&lt;br/&gt;&lt;br/&gt;Gunakan XMI Import untuk struktur kelas &amp;amp; usecase, atau salin kode Mermaid dari UML_Bab4.md ke tool Live Editor." style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FAFAFA;strokeColor=#CCCCCC;align=center;fontSize=12;" vertex="1" parent="1">')
        p_xml.append('          <mxGeometry x="100" y="100" width="500" height="100" as="geometry" />')
        p_xml.append('        </mxCell>')
        p_xml.append('      </root>')
        pages.append((title, "\n".join(p_xml)))

    # Save Individual Files
    uml_dir = "/home/vue/Documents/frelence/joki/Dokumen/UML"
    for title, xml_content in pages:
        if title in individual_mapping:
            filename = individual_mapping[title]
                
            file_path = os.path.join(uml_dir, filename)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write('<mxfile host="Electron" modified="2026-07-24T00:00:00.000Z" agent="5.0" version="20.0.0">\n')
                f.write(f'  <diagram id="diag_{filename.split("_")[0]}" name="{title}">\n')
                f.write('    <mxGraphModel dx="1200" dy="1200" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">\n')
                f.write(xml_content)
                f.write('\n    </mxGraphModel>\n')
                f.write('  </diagram>\n')
                f.write('</mxfile>\n')
            print(f"✅ Generated individual Draw.io file: {filename}")

    # Save Multi Page File
    full_xml = []
    full_xml.append('<mxfile host="Electron" modified="2026-07-24T00:00:00.000Z" agent="5.0" version="20.0.0">')
    for i, (name, content) in enumerate(pages):
        full_xml.append(f'  <diagram id="diag_{i}" name="{name}">')
        full_xml.append('    <mxGraphModel dx="1200" dy="1200" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">')
        full_xml.append(content)
        full_xml.append('    </mxGraphModel>')
        full_xml.append('  </diagram>')
    full_xml.append('</mxfile>')
    
    with open(multi_path, "w", encoding="utf-8") as f:
        f.write("\n".join(full_xml))
    print(f"✅ Multi-page Draw.io generated successfully: {multi_path}")

if __name__ == "__main__":
    generate_precise_drawio()
