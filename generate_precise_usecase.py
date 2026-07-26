#!/usr/bin/env python3
"""
Generate a flat-hierarchy Draw.io (.drawio) file for the
DBD Prediction System Use Case Diagram (Gambar 4.26 in BABIV.pdf)
with absolute coordinates to ensure clean alignment and no relative warping.
"""
import os

def create_drawio_file():
    output_path = "/home/vue/Documents/frelence/joki/Dokumen/UML/UseCase_DBD.drawio"
    
    # Boundary coordinates (absolute)
    bx, by, bw, bh = 100, 20, 700, 880
    
    # Actor coordinates (absolute)
    admin_id = "actor_admin"
    petugas_id = "actor_petugas"
    boundary_id = "boundary"
    
    # Use Case raw relative coordinates and dimensions
    raw_usecases = {
        # Core
        "Login":                 ("Login", 340, 360, 100, 40),
        "Logout":                ("Logout", 560, 810, 100, 40),
        "Dashboard":             ("Dashboard", 220, 50, 120, 40),
        # CRUD Modules
        "KDP":                   ("Kelola Data Pasien", 220, 180, 130, 40),
        "MT":                    ("Manajemen Training", 220, 310, 130, 40),
        "KP":                    ("Kelola Prediksi", 220, 440, 130, 40),
        "MM":                    ("Manajemen Model", 220, 570, 130, 40),
        "KL":                    ("Kelola Laporan", 220, 700, 130, 40),
        # Petugas modules
        "LPR":                   ("Lihat Prediksi\nResiko", 460, 290, 130, 40),
        "LEM":                   ("Lihat Evaluasi\nModel", 460, 380, 130, 40),
        "LL":                    ("Lihat Laporan", 460, 470, 120, 40),
        "CL":                    ("Cetak Laporan", 400, 530, 100, 35),
    }
    
    # Calculate absolute coordinates for usecases
    usecases = {}
    for key, (label, rx, ry, w, h) in raw_usecases.items():
        # absolute_x = boundary_x + relative_x
        # absolute_y = boundary_y + relative_y
        usecases[key] = (label, bx + rx, by + ry, w, h)
        
    # CRUD offset list relative to parent module
    crud_offsets = {
        "Create": (-100, -50),
        "Read":   (-30, -70),
        "Update": (60, -70),
        "Delete": (130, -50),
    }
    
    crud_modules = ["KDP", "MT", "KP", "MM", "KL"]
    
    uc_ids = {k: f"uc_{k}" for k in usecases.keys()}
    crud_ids = {}
    for mod in crud_modules:
        crud_ids[mod] = {
            action: f"crud_{mod}_{action.lower()}" for action in crud_offsets.keys()
        }

    # Start writing XML
    xml = []
    xml.append('<mxfile host="Electron" modified="2026-07-24T00:00:00.000Z" agent="5.0" version="20.0.0">')
    xml.append('  <diagram id="diagram_dbd" name="UseCase Diagram">')
    xml.append('    <mxGraphModel dx="1200" dy="1200" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">')
    xml.append('      <root>')
    xml.append('        <mxCell id="0" />')
    xml.append('        <mxCell id="1" parent="0" />')
    
    # 1. System Boundary (Send to back, placed in parent="1" flat)
    xml.append(f'        <mxCell id="{boundary_id}" value="uo UseCase Diagram0" style="swimlane;whiteSpace=wrap;html=1;startSize=25;fillColor=none;strokeColor=#333333;childLayout=nil;collapsible=0;points=[];" vertex="1" parent="1">')
    xml.append(f'          <mxGeometry x="{bx}" y="{by}" width="{bw}" height="{bh}" as="geometry" />')
    xml.append('        </mxCell>')
    
    # 2. Actors (Outside boundary)
    xml.append(f'        <mxCell id="{admin_id}" value="Admin" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fillColor=#ffffff;strokeColor=#000000;" vertex="1" parent="1">')
    xml.append(f'          <mxGeometry x="30" y="380" width="30" height="60" as="geometry" />')
    xml.append('        </mxCell>')
    
    xml.append(f'        <mxCell id="{petugas_id}" value="Petugas" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fillColor=#ffffff;strokeColor=#000000;" vertex="1" parent="1">')
    xml.append(f'          <mxGeometry x="830" y="380" width="30" height="60" as="geometry" />')
    xml.append('        </mxCell>')
    
    # 3. Main Use Cases (Flat structure: parent="1")
    for key, (label, ax, ay, w, h) in usecases.items():
        xml_label = label.replace('\n', '&lt;br/&gt;')
        xml.append(f'        <mxCell id="{uc_ids[key]}" value="{xml_label}" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=11;" vertex="1" parent="1">')
        xml.append(f'          <mxGeometry x="{ax}" y="{ay}" width="{w}" height="{h}" as="geometry" />')
        xml.append('        </mxCell>')
        
    # 4. CRUD Sub-Use Cases (Flat structure: parent="1")
    for mod in crud_modules:
        mx, my = usecases[mod][1], usecases[mod][2]
        for action, offset in crud_offsets.items():
            cx = mx + offset[0]
            cy = my + offset[1]
            cid = crud_ids[mod][action]
            xml.append(f'        <mxCell id="{cid}" value="{action}" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFACD;strokeColor=#8B8000;fontSize=10;" vertex="1" parent="1">')
            xml.append(f'          <mxGeometry x="{cx}" y="{cy}" width="65" height="28" as="geometry" />')
            xml.append('        </mxCell>')
            
    # --- Edges (Relationships) ---
    edge_idx = 100
    
    # Helper to write association
    def write_assoc(source, target, style=""):
        nonlocal edge_idx
        edge_idx += 1
        default_style = "endArrow=none;html=1;rounded=0;strokeColor=#000000;jumpStyle=arc;"
        if style:
            default_style += style
        xml.append(f'        <mxCell id="edge_{edge_idx}" style="{default_style}" edge="1" parent="1" source="{source}" target="{target}">')
        xml.append('          <mxGeometry width="50" height="50" relative="1" as="geometry" />')
        xml.append('        </mxCell>')

    # Helper to write dependency (Include / Extend)
    def write_dep(source, target, label):
        nonlocal edge_idx
        edge_idx += 1
        style = "endArrow=open;endSize=12;dashed=1;html=1;rounded=0;strokeColor=#333333;fontSize=9;jumpStyle=arc;"
        xml.append(f'        <mxCell id="edge_{edge_idx}" value="{label}" style="{style}" edge="1" parent="1" source="{source}" target="{target}">')
        xml.append('          <mxGeometry width="50" height="50" relative="1" as="geometry" />')
        xml.append('        </mxCell>')

    # Connections: Admin to Core Modules (Oblique straight lines)
    admin_targets = ["Dashboard", "KDP", "MT", "KP", "MM", "KL", "Login"]
    for t in admin_targets:
        write_assoc(admin_id, uc_ids[t])
        
    # Admin to Logout (Orthogonal path under the boundary to keep it extremely clean)
    write_assoc(admin_id, uc_ids["Logout"], "edgeStyle=orthogonalEdgeStyle;exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    
    # Petugas connections
    petugas_targets = ["Login", "LPR", "LEM", "LL"]
    for t in petugas_targets:
        write_assoc(petugas_id, uc_ids[t])
        
    # Petugas to Dashboard (orthogonal path around top)
    write_assoc(petugas_id, uc_ids["Dashboard"], "edgeStyle=orthogonalEdgeStyle;exitX=0.5;exitY=0;entryX=1;entryY=0.5;")
    
    # Petugas to Logout (orthogonal path around bottom)
    write_assoc(petugas_id, uc_ids["Logout"], "edgeStyle=orthogonalEdgeStyle;exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    
    # Includes to Login (arrow points TO Login)
    include_modules = ["Dashboard", "KDP", "MT", "KP", "MM", "KL", "LPR", "LEM", "LL"]
    for m in include_modules:
        write_dep(uc_ids[m], uc_ids["Login"], "&lt;&lt;include&gt;&gt;")
        
    # Logout includes Login
    write_dep(uc_ids["Logout"], uc_ids["Login"], "&lt;&lt;include&gt;&gt;")
    
    # Extends (arrow points TO parent)
    for mod in crud_modules:
        for action in crud_offsets.keys():
            write_dep(crud_ids[mod][action], uc_ids[mod], "&lt;&lt;extend&gt;&gt;")
            
    # Cetak Laporan extends Lihat Laporan
    write_dep(uc_ids["CL"], uc_ids["LL"], "&lt;&lt;extend&gt;&gt;")
    
    # Finish Draw.io XML
    xml.append('      </root>')
    xml.append('    </mxGraphModel>')
    xml.append('  </diagram>')
    xml.append('</mxfile>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(xml))
    print(f"✅ Flat Draw.io file generated successfully: {output_path}")

if __name__ == "__main__":
    create_drawio_file()
