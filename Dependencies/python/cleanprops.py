import os
import xml.etree.ElementTree as ET

def remove_prop_elements(element):
    """Recursively remove all <prop> elements from the XML tree."""
    for child in list(element):
        if child.tag == 'prop':
            element.remove(child)
        else:
            remove_prop_elements(child)

def main():
    cwd = os.getcwd()
    processed_count = 0

    for root_dir, dirs, files in os.walk(cwd):
        for filename in files:
            if filename.lower().endswith('.tmx'):
                file_path = os.path.join(root_dir, filename)
                
                # Attempt to parse the TMX file as XML
                try:
                    tree = ET.parse(file_path)
                    root = tree.getroot()
                except Exception as e:
                    print(f"[ERROR] Could not parse file: {file_path}\n{e}")
                    continue

                # Remove <prop> elements safely
                remove_prop_elements(root)

                # Write back the modified XML to the file
                try:
                    tree.write(file_path, encoding='utf-8', xml_declaration=True)
                except Exception as e:
                    print(f"[ERROR] Could not write file: {file_path}\n{e}")
                    continue

                # Optional: Replace &apos; with literal apostrophes if needed.
                # (Parsing already converts entities, but writing might re-escape them.)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        contents = f.read()
                    contents = contents.replace("&apos;", "'")
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(contents)
                except Exception as e:
                    print(f"[ERROR] Could not post-process file: {file_path}\n{e}")
                    continue

                print(f"[OK] Processed and updated: {file_path}")
                processed_count += 1

    print(f"\nDone. Processed {processed_count} .tmx file(s) in '{cwd}' and subdirectories.")

if __name__ == "__main__":
    main()
