import os
import re
import subprocess

# Paths
md_file_path = "/home/vue/Documents/frelence/joki/UML_Bab4.md"
target_dir = "/home/vue/Documents/frelence/joki/Dokumen/UML/images"

# Make sure target dir exists
os.makedirs(target_dir, exist_ok=True)

# Mapping of headings to target filenames
mapping = {
    r"2\.\s+Class\s+Diagram": "class_diagram.png",
    r"Activity\s+Diagram\s+Admin": "activity_diagram_admin.png",
    r"Activity\s+Diagram\s+Petugas": "activity_diagram_petugas.png",
    r"Sequence\s+Diagram\s+Login": "sequence_diagram_login.png",
    r"Sequence\s+Diagram\s+Kelola\s+Data\s+Pasien": "sequence_diagram_kelola_pasien.png",
    r"Sequence\s+Diagram\s+Import\s+Data\s+Excel": "sequence_diagram_import.png",
    r"Sequence\s+Diagram\s+Training\s+Model": "sequence_diagram_training.png",
    r"Sequence\s+Diagram\s+Prediksi\s+Risiko": "sequence_diagram_prediksi.png",
    r"Sequence\s+Diagram\s+Lihat\s+Laporan": "sequence_diagram_laporan.png",
    r"Sequence\s+Diagram\s+Kelola\s+Pengguna": "sequence_diagram_kelola_pengguna.png",
    r"State\s+Chart\s+Diagram": "state_chart_diagram.png",
    r"Deployment\s+Diagram": "deployment_diagram.png"
}

with open(md_file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Split the content by headers to find the code blocks associated with each section
# We will iterate through sections
sections = re.split(r"^(#+\s+.*)$", content, flags=re.MULTILINE)

current_header = ""
for section in sections:
    section_stripped = section.strip()
    if not section_stripped:
        continue
    
    if section.startswith("#"):
        current_header = section_stripped
        continue
    
    # We are in a content block, check if current_header matches any of our patterns
    matched_filename = None
    for pattern, filename in mapping.items():
        if re.search(pattern, current_header, re.IGNORECASE):
            matched_filename = filename
            break
            
    if matched_filename:
        # Find the mermaid block inside this section
        match = re.search(r"```mermaid\s+(.*?)\s+```", section, re.DOTALL)
        if match:
            mermaid_code = match.group(1).strip()
            
            # Write to temp mmd file
            temp_mmd = f"/tmp/{matched_filename.replace('.png', '.mmd')}"
            with open(temp_mmd, "w", encoding="utf-8") as temp_f:
                temp_f.write(mermaid_code)
                
            print(f"Rendering: {matched_filename} from header '{current_header}'...")
            
            # Execute mermaid-cli
            output_file = os.path.join(target_dir, matched_filename)
            cmd = ["npx", "-y", "@mermaid-js/mermaid-cli", "-i", temp_mmd, "-o", output_file, "-b", "white"]
            
            try:
                res = subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(f"Success rendering {matched_filename}")
            except subprocess.CalledProcessError as e:
                print(f"Error rendering {matched_filename}:")
                print(e.stderr)
            finally:
                if os.path.exists(temp_mmd):
                    os.remove(temp_mmd)
        else:
            print(f"No mermaid code block found for matched header: {current_header}")
