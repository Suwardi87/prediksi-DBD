#!/usr/bin/env python3
"""
Generate a proper Astah .asta file (ZIP with XML) for Use Case Diagram
matching Gambar 4.26 from BABIV.pdf exactly, and XMI files for import.
"""
import uuid
import zipfile
import os

def jude_id():
    """Generate a JUDE-style ID"""
    return str(uuid.uuid4())

def create_asta_file():
    output_path = "/home/vue/Documents/frelence/joki/Dokumen/UML/UseCase_DBD.asta"
    
    # IDs for all elements
    project_id = jude_id()
    diagram_id = jude_id()
    
    # Actor IDs
    admin_id = jude_id()
    petugas_id = jude_id()
    
    # Use Case IDs
    uc_ids = {}
    uc_names = [
        "Dashboard", "Kelola Data Pasien", "Manajemen Training",
        "Kelola Prediksi", "Manajemen Model", "Kelola Laporan",
        "Login", "Lihat Prediksi Resiko", "Lihat Evaluasi Model",
        "Lihat Laporan", "Cetak Laporan", "Logout"
    ]
    for name in uc_names:
        uc_ids[name] = jude_id()
    
    # CRUD IDs for each module
    crud_modules = ["Dashboard", "Kelola Data Pasien", "Manajemen Training",
                    "Kelola Prediksi", "Manajemen Model", "Kelola Laporan"]
    crud_ids = {}
    for module in crud_modules:
        crud_ids[module] = {
            "Create": jude_id(),
            "Read": jude_id(),
            "Update": jude_id(),
            "Delete": jude_id(),
        }
    
    # Positions matching the original Astah diagram
    positions = {
        "Dashboard":              (280, 60, 120, 40),
        "Kelola Data Pasien":     (260, 200, 130, 45),
        "Manajemen Training":     (260, 320, 130, 45),
        "Kelola Prediksi":        (260, 440, 130, 40),
        "Manajemen Model":        (260, 560, 130, 45),
        "Kelola Laporan":         (260, 690, 130, 40),
        "Login":                  (470, 370, 100, 40),
        "Lihat Prediksi Resiko":  (650, 230, 130, 45),
        "Lihat Evaluasi Model":   (650, 330, 130, 45),
        "Lihat Laporan":          (650, 430, 120, 40),
        "Cetak Laporan":          (580, 530, 120, 40),
        "Logout":                 (700, 770, 100, 40),
    }
    
    # CRUD positions (relative to parent module)
    crud_offsets = {
        "Create": (-150, -20, 80, 30),
        "Read":   (-60, -55, 70, 30),
        "Update": (50, -55, 80, 30),
        "Delete": (140, -20, 80, 30),
    }
    
    # ========================================
    # Build the Astah-compatible XMI/XML
    # ========================================
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<JUDE version="8.0">\n'
    xml += f'  <project id="{project_id}" name="Sistem Prediksi DBD">\n'
    
    # ---- Model Elements ----
    xml += '    <model>\n'
    
    # Actors
    xml += f'      <actor id="{admin_id}" name="Admin"/>\n'
    xml += f'      <actor id="{petugas_id}" name="Petugas"/>\n'
    
    # Use Cases
    for name in uc_names:
        xml += f'      <usecase id="{uc_ids[name]}" name="{name}"/>\n'
    
    # CRUD Use Cases
    for module in crud_modules:
        for crud_name, crud_id in crud_ids[module].items():
            xml += f'      <usecase id="{crud_id}" name="{crud_name}"/>\n'
    
    # Associations: Admin
    admin_assocs = ["Dashboard", "Kelola Data Pasien", "Manajemen Training",
                    "Kelola Prediksi", "Manajemen Model", "Kelola Laporan", "Login", "Logout"]
    for uc_name in admin_assocs:
        aid = jude_id()
        xml += f'      <association id="{aid}" source="{admin_id}" target="{uc_ids[uc_name]}"/>\n'
    
    # Associations: Petugas
    petugas_assocs = ["Dashboard", "Login", "Lihat Prediksi Resiko",
                      "Lihat Evaluasi Model", "Lihat Laporan", "Logout"]
    for uc_name in petugas_assocs:
        aid = jude_id()
        xml += f'      <association id="{aid}" source="{petugas_id}" target="{uc_ids[uc_name]}"/>\n'
    
    # Include relationships (to Login)
    include_sources = ["Dashboard", "Kelola Data Pasien", "Manajemen Training",
                       "Kelola Prediksi", "Manajemen Model", "Kelola Laporan",
                       "Lihat Prediksi Resiko", "Lihat Evaluasi Model", "Lihat Laporan"]
    for uc_name in include_sources:
        iid = jude_id()
        xml += f'      <include id="{iid}" source="{uc_ids[uc_name]}" target="{uc_ids["Login"]}"/>\n'
    
    # Extend relationships (CRUD to parent)
    for module in crud_modules:
        for crud_name, crud_id in crud_ids[module].items():
            eid = jude_id()
            xml += f'      <extend id="{eid}" source="{crud_id}" target="{uc_ids[module]}"/>\n'
    
    # Extend: Cetak Laporan -> Lihat Laporan
    eid = jude_id()
    xml += f'      <extend id="{eid}" source="{uc_ids["Cetak Laporan"]}" target="{uc_ids["Lihat Laporan"]}"/>\n'
    
    xml += '    </model>\n'
    
    # ---- Diagram Presentation ----
    xml += f'    <diagram id="{diagram_id}" name="UseCase Diagram" type="UseCaseDiagram">\n'
    xml += '      <presentations>\n'
    
    # System boundary
    xml += f'        <subject x="100" y="20" w="700" h="730" label="Sistem Prediksi DBD"/>\n'
    
    # Actor presentations
    xml += f'        <actorPresentation modelRef="{admin_id}" x="30" y="400" label="Admin"/>\n'
    xml += f'        <actorPresentation modelRef="{petugas_id}" x="830" y="350" label="Petugas"/>\n'
    
    # Use Case presentations
    for name in uc_names:
        x, y, w, h = positions[name]
        xml += f'        <usecasePresentation modelRef="{uc_ids[name]}" x="{x}" y="{y}" w="{w}" h="{h}" label="{name}"/>\n'
    
    # CRUD presentations
    for module in crud_modules:
        px, py, pw, ph = positions[module]
        for crud_name, crud_id in crud_ids[module].items():
            ox, oy, ow, oh = crud_offsets[crud_name]
            x = px + ox
            y = py + oy
            xml += f'        <usecasePresentation modelRef="{crud_id}" x="{x}" y="{y}" w="{ow}" h="{oh}" label="{crud_name}"/>\n'
    
    xml += '      </presentations>\n'
    xml += '    </diagram>\n'
    xml += '  </project>\n'
    xml += '</JUDE>\n'
    
    # Save as .asta (ZIP containing the XML)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Method 1: Save as plain XML (some Astah versions accept this)
    xml_path = output_path.replace('.asta', '.xml')
    with open(xml_path, 'w', encoding='utf-8') as f:
        f.write(xml)
    print(f"✅ XML file saved: {xml_path}")
    
    # Method 2: Save as ZIP (.asta format)
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('project.xml', xml)
    print(f"✅ ASTA file saved: {output_path}")
    
    # Also save the XMI format (more standard for import)
    create_standard_xmi(output_path.replace('.asta', '_standard.xmi'), 
                        admin_id, petugas_id, uc_ids, crud_ids, crud_modules)


def create_standard_xmi(output_path, admin_id, petugas_id, uc_ids, crud_ids, crud_modules):
    """Create standard XMI 2.1 format that Astah can import"""
    
    xml = '''<?xml version="1.0" encoding="UTF-8"?>
<xmi:XMI xmi:version="2.1" xmlns:xmi="http://schema.omg.org/spec/XMI/2.1" xmlns:uml="http://schema.omg.org/spec/UML/2.1">
  <uml:Model xmi:type="uml:Model" name="Sistem Prediksi DBD" xmi:id="model1">
'''
    
    # Actors
    xml += f'    <packagedElement xmi:type="uml:Actor" xmi:id="{admin_id}" name="Admin"/>\n'
    xml += f'    <packagedElement xmi:type="uml:Actor" xmi:id="{petugas_id}" name="Petugas"/>\n'
    
    # Use Cases
    for name, uid in uc_ids.items():
        xml += f'    <packagedElement xmi:type="uml:UseCase" xmi:id="{uid}" name="{name}"/>\n'
    
    # CRUD Use Cases
    for module in crud_modules:
        for crud_name, crud_id in crud_ids[module].items():
            unique_name = f"{crud_name}"
            xml += f'    <packagedElement xmi:type="uml:UseCase" xmi:id="{crud_id}" name="{unique_name}"/>\n'
    
    # Associations: Admin
    admin_assocs = ["Dashboard", "Kelola Data Pasien", "Manajemen Training",
                    "Kelola Prediksi", "Manajemen Model", "Kelola Laporan", "Login", "Logout"]
    for uc_name in admin_assocs:
        aid = jude_id()
        e1 = jude_id()
        e2 = jude_id()
        xml += f'''    <packagedElement xmi:type="uml:Association" xmi:id="{aid}">
      <memberEnd xmi:id="{e1}" type="{admin_id}"/>
      <memberEnd xmi:id="{e2}" type="{uc_ids[uc_name]}"/>
    </packagedElement>
'''
    
    # Associations: Petugas
    petugas_assocs = ["Dashboard", "Login", "Lihat Prediksi Resiko",
                      "Lihat Evaluasi Model", "Lihat Laporan", "Logout"]
    for uc_name in petugas_assocs:
        aid = jude_id()
        e1 = jude_id()
        e2 = jude_id()
        xml += f'''    <packagedElement xmi:type="uml:Association" xmi:id="{aid}">
      <memberEnd xmi:id="{e1}" type="{petugas_id}"/>
      <memberEnd xmi:id="{e2}" type="{uc_ids[uc_name]}"/>
    </packagedElement>
'''
    
    # Include dependencies
    include_sources = ["Dashboard", "Kelola Data Pasien", "Manajemen Training",
                       "Kelola Prediksi", "Manajemen Model", "Kelola Laporan",
                       "Lihat Prediksi Resiko", "Lihat Evaluasi Model", "Lihat Laporan"]
    for uc_name in include_sources:
        iid = jude_id()
        xml += f'    <packagedElement xmi:type="uml:Include" xmi:id="{iid}" includingCase="{uc_ids[uc_name]}" addition="{uc_ids["Login"]}"/>\n'
    
    # Extend dependencies
    for module in crud_modules:
        for crud_name, crud_id in crud_ids[module].items():
            eid = jude_id()
            xml += f'    <packagedElement xmi:type="uml:Extend" xmi:id="{eid}" extension="{crud_id}" extendedCase="{uc_ids[module]}"/>\n'
    
    # Cetak Laporan extends Lihat Laporan
    eid = jude_id()
    xml += f'    <packagedElement xmi:type="uml:Extend" xmi:id="{eid}" extension="{uc_ids["Cetak Laporan"]}" extendedCase="{uc_ids["Lihat Laporan"]}"/>\n'
    
    xml += '''  </uml:Model>
</xmi:XMI>
'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml)
    print(f"✅ Standard Use Case XMI 2.1 file saved: {output_path}")


def create_class_diagram_xmi():
    """Create standard XMI 2.1 for Class Diagram"""
    output_path = "/home/vue/Documents/frelence/joki/Dokumen/UML/Class_Diagram_DBD_standard.xmi"
    
    class_ids = {
        "User": jude_id(),
        "Wilayah": jude_id(),
        "PasienDBD": jude_id(),
        "KasusBulanan": jude_id(),
        "HasilPrediksi": jude_id(),
        "ModelEvaluasi": jude_id(),
        "LogAktivitas": jude_id(),
    }
    
    classes_data = {
        "User": {
            "attributes": [
                ("id", "int"), ("username", "string"), ("password", "string"),
                ("nama_lengkap", "string"), ("email", "string"), ("role", "enum"),
                ("foto", "string"), ("status", "enum"), ("last_login", "datetime"),
                ("created_at", "timestamp"), ("updated_at", "timestamp")
            ],
            "operations": [
                "check_password(password: string): boolean",
                "login(): boolean",
                "logout(): void",
                "create(): boolean",
                "update(): boolean",
                "delete(): boolean"
            ]
        },
        "Wilayah": {
            "attributes": [
                ("id", "int"), ("nama_wilayah", "string"), ("kecamatan", "string"),
                ("latitude", "decimal"), ("longitude", "decimal"), ("populasi", "int"),
                ("created_at", "timestamp")
            ],
            "operations": [
                "create(): boolean",
                "read(): List",
                "update(): boolean",
                "delete(): boolean",
                "getPasienCount(): int"
            ]
        },
        "PasienDBD": {
            "attributes": [
                ("id", "int"), ("no_rm", "string"), ("nama_pasien", "string"),
                ("usia", "int"), ("jenis_kelamin", "enum"), ("alamat", "text"),
                ("id_wilayah", "int"), ("tanggal_masuk", "date"), ("tanggal_keluar", "date"),
                ("lama_rawat", "int"), ("bulan", "string"), ("tahun", "int"),
                ("status_pasien", "enum"), ("created_at", "timestamp"), ("updated_at", "timestamp")
            ],
            "operations": [
                "create(): boolean",
                "read(): List",
                "update(): boolean",
                "delete(): boolean",
                "getByBulan(): List"
            ]
        },
        "KasusBulanan": {
            "attributes": [
                ("id", "int"), ("bulan", "string"), ("tahun", "int"),
                ("jumlah_kasus", "int"), ("jumlah_sembuh", "int"), ("jumlah_meninggal", "int"),
                ("tingkat_risiko", "enum"), ("created_at", "timestamp")
            ],
            "operations": [
                "create(): boolean",
                "read(): List",
                "update(): boolean",
                "getByTahun(tahun: int): List",
                "getStatistik(): Object"
            ]
        },
        "HasilPrediksi": {
            "attributes": [
                ("id", "int"), ("tanggal_prediksi", "datetime"), ("bulan_prediksi", "string"),
                ("tahun_prediksi", "int"), ("jumlah_kasus_prediksi", "int"),
                ("tingkat_risiko_prediksi", "enum"), ("confidence_score", "decimal"),
                ("model_version", "string"), ("created_by", "int"), ("created_at", "timestamp")
            ],
            "operations": [
                "create(): boolean",
                "read(): List",
                "getByTahun(tahun: int): List",
                "getLatest(): Object",
                "predict(data: Object): Object"
            ]
        },
        "ModelEvaluasi": {
            "attributes": [
                ("id", "int"), ("tanggal_training", "datetime"), ("accuracy", "decimal"),
                ("precision_score", "decimal"), ("recall_score", "decimal"), ("f1_score", "decimal"),
                ("mae", "decimal"), ("rmse", "decimal"), ("r2_score", "decimal"),
                ("n_estimators", "int"), ("max_depth", "int"), ("confusion_matrix", "text"),
                ("feature_importance", "text"), ("model_path", "string"), ("created_at", "timestamp")
            ],
            "operations": [
                "create(): boolean",
                "read(): List",
                "getLatest(): Object",
                "getMetrics(): Object"
            ]
        },
        "LogAktivitas": {
            "attributes": [
                ("id", "int"), ("user_id", "int"), ("aksi", "string"),
                ("deskripsi", "text"), ("ip_address", "string"), ("created_at", "timestamp")
            ],
            "operations": [
                "create(): boolean",
                "read(): List",
                "getByUser(user_id: int): List",
                "filter(filters: Object): List"
            ]
        }
    }
    
    xml = '''<?xml version="1.0" encoding="UTF-8"?>
<xmi:XMI xmi:version="2.1" xmlns:xmi="http://schema.omg.org/spec/XMI/2.1" xmlns:uml="http://schema.omg.org/spec/UML/2.1">
  <uml:Model xmi:type="uml:Model" name="Sistem Prediksi DBD Class Model" xmi:id="classModel1">
'''
    
    # Classes
    for name, cid in class_ids.items():
        xml += f'    <packagedElement xmi:type="uml:Class" xmi:id="{cid}" name="{name}">\n'
        
        # Attributes
        for attr_name, attr_type in classes_data[name]["attributes"]:
            attr_id = jude_id()
            xml += f'      <ownedAttribute xmi:type="uml:Property" xmi:id="{attr_id}" name="{attr_name}" visibility="private">\n'
            xml += f'        <type xmi:type="uml:PrimitiveType" name="{attr_type}"/>\n'
            xml += f'      </ownedAttribute>\n'
            
        # Operations
        for op in classes_data[name]["operations"]:
            op_id = jude_id()
            xml += f'      <ownedOperation xmi:type="uml:Operation" xmi:id="{op_id}" name="{op}" visibility="public"/>\n'
            
        xml += '    </packagedElement>\n'
    
    # Associations
    # User 1 -> 0..* HasilPrediksi (creates)
    aid1 = jude_id()
    xml += f'''    <packagedElement xmi:type="uml:Association" xmi:id="{aid1}" name="creates">
      <memberEnd xmi:idref="{jude_id()}" type="{class_ids["User"]}"/>
      <memberEnd xmi:idref="{jude_id()}" type="{class_ids["HasilPrediksi"]}"/>
    </packagedElement>
'''
    
    # User 1 -> 0..* LogAktivitas (logs)
    aid2 = jude_id()
    xml += f'''    <packagedElement xmi:type="uml:Association" xmi:id="{aid2}" name="logs">
      <memberEnd xmi:idref="{jude_id()}" type="{class_ids["User"]}"/>
      <memberEnd xmi:idref="{jude_id()}" type="{class_ids["LogAktivitas"]}"/>
    </packagedElement>
'''
    
    # Wilayah 1 -> 0..* PasienDBD (memiliki)
    aid3 = jude_id()
    xml += f'''    <packagedElement xmi:type="uml:Association" xmi:id="{aid3}" name="memiliki">
      <memberEnd xmi:idref="{jude_id()}" type="{class_ids["Wilayah"]}"/>
      <memberEnd xmi:idref="{jude_id()}" type="{class_ids["PasienDBD"]}"/>
    </packagedElement>
'''
    
    xml += '''  </uml:Model>
</xmi:XMI>
'''
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml)
    print(f"✅ Standard Class Diagram XMI 2.1 file saved: {output_path}")


if __name__ == "__main__":
    create_asta_file()
    create_class_diagram_xmi()
    
    print()
    print("=" * 65)
    print("CARA IMPORT KE ASTAH UML / ASTAH PROFESSIONAL:")
    print("=" * 65)
    print()
    print("OPSI A - Import XMI (DIREKOMENDASIKAN):")
    print("  1. Buka Astah")
    print("  2. File → Import XMI...")
    print("  3. Pilih file:")
    print("     - UseCase_DBD_standard.xmi (untuk Use Case)")
    print("     - Class_Diagram_DBD_standard.xmi (untuk Class Diagram)")
    print("  4. Buat diagram baru di Astah")
    print("  5. Drag & Drop elemen dari panel kiri (Project Tree)")
    print("  6. Atur posisi sesuai kebutuhan")
    print()
