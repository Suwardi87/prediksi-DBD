#!/usr/bin/env python3
"""
Sync the manually-fixed Use Case Diagram from 1_use_case_diagram.drawio
into the first page of Sistem_DBD_All_Diagrams.drawio.
"""
import xml.etree.ElementTree as ET

def sync_usecase_page():
    single_path = '/home/vue/Documents/frelence/joki/Dokumen/UML/1_use_case_diagram.drawio'
    multi_path = '/home/vue/Documents/frelence/joki/Dokumen/UML/Sistem_DBD_All_Diagrams.drawio'
    
    # Parse single page XML
    single_tree = ET.parse(single_path)
    single_diagram = single_tree.find('diagram')
    
    # Parse multi page XML
    multi_tree = ET.parse(multi_path)
    multi_root = multi_tree.getroot()
    
    # Replace the Use Case Diagram page
    replaced = False
    for i, diag in enumerate(multi_root.findall('diagram')):
        if diag.attrib.get('name') == 'Use Case Diagram':
            # Preserve multi-page id or use the single page diagram
            # To be safe, we just replace the whole node
            multi_root[i] = single_diagram
            replaced = True
            break
            
    if replaced:
        # Write back to Sistem_DBD_All_Diagrams.drawio
        # Ensure it starts with proper header
        with open(multi_path, 'wb') as f:
            multi_tree.write(f, encoding='utf-8', xml_declaration=False)
        print("✅ Sync Use Case page in multi-page drawio completed successfully!")
    else:
        print("❌ Error: Could not find Use Case Diagram page in multi-page file.")

if __name__ == '__main__':
    sync_usecase_page()
