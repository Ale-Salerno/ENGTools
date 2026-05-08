import os
import zipfile
import shutil
from lxml import etree as ET
from tempfile import mkdtemp

def list_docx_files(folder):
    return [f for f in os.listdir(folder) if f.lower().endswith(".docx") and not f.lower().endswith("_out.docx")]

def extract_authors_from_xml(xml_data):
    authors = set()
    root = ET.fromstring(xml_data)
    for elem in root.iter():
        author = elem.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}author')
        if author:
            authors.add(author)
    return authors

def extract_all_authors(docx_path):
    authors = set()
    with zipfile.ZipFile(docx_path, 'r') as zipf:
        for xml_file in ['word/document.xml', 'word/comments.xml']:
            if xml_file in zipf.namelist():
                xml_data = zipf.read(xml_file)
                authors.update(extract_authors_from_xml(xml_data))
    return authors

def replace_authors_in_file(docx_path, author_map, output_path):
    temp_dir = mkdtemp()
    unzip_path = os.path.join(temp_dir, "unzipped")
    os.makedirs(unzip_path, exist_ok=True)

    with zipfile.ZipFile(docx_path, 'r') as zipf:
        zipf.extractall(unzip_path)

    changed_count = 0
    for xml_rel_path in ['word/document.xml', 'word/comments.xml']:
        xml_file = os.path.join(unzip_path, xml_rel_path)
        if os.path.exists(xml_file):
            parser = ET.XMLParser(remove_blank_text=True)
            tree = ET.parse(xml_file, parser)
            root = tree.getroot()
            for elem in root.iter():
                for attr_name in elem.attrib:
                    if 'author' in attr_name:
                        current = elem.attrib[attr_name]
                        if current in author_map and author_map[current] != current:
                            elem.attrib[attr_name] = author_map[current]
                            changed_count += 1
            tree.write(xml_file, encoding="utf-8", xml_declaration=True, pretty_print=True)

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as new_docx:
        for folder, _, files in os.walk(unzip_path):
            for file in files:
                file_path = os.path.join(folder, file)
                archive_name = os.path.relpath(file_path, unzip_path)
                new_docx.write(file_path, archive_name)

    shutil.rmtree(temp_dir)
    return changed_count

def main():
    current_dir = os.getcwd()
    docx_files = list_docx_files(current_dir)
    
    if not docx_files:
        print(f"No .docx files found in current directory: {current_dir}")
        input("\nPress Enter to exit...")
        return

    all_authors = set()
    for file in docx_files:
        all_authors.update(extract_all_authors(os.path.join(current_dir, file)))

    if not all_authors:
        print("❌ No `w:author` attributes found in any document.")
        input("\nPress Enter to exit...")
        return

    print("\n👥 Authors found:")
    for author in sorted(all_authors):
        print(f"- {author}")

    print("\nEnter new names (press Enter to skip/keep as-is):")
    author_map = {}
    for author in sorted(all_authors):
        new_name = input(f"Replace \"{author}\" with: ").strip()
        author_map[author] = new_name if new_name else author

    total_files = 0
    total_changes = 0

    for file in docx_files:
        input_path = os.path.join(current_dir, file)
        filename, ext = os.path.splitext(file)
        output_path = os.path.join(current_dir, f"{filename}_out{ext}")
        changed = replace_authors_in_file(input_path, author_map, output_path)
        if changed:
            total_files += 1
            total_changes += changed
            print(f"✔ Modified {file} -> {filename}_out{ext} ({changed} changes)")
        else:
            print(f"— No changes in {file} (output not created)")

    print(f"\n✅ Done. Updated {total_changes} author entries across {total_files} file(s).")
    

if __name__ == "__main__":
    main()