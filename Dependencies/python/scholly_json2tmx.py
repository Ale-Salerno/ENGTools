import json
import os
import glob
import re
import xml.etree.ElementTree as ET
from datetime import datetime

# Regex to find placeholders like {variable}
PLACEHOLDER_REGEX = r'(\{.*?\})'

def flatten_json(y, path_separator='.'):
    """
    Flattens a nested json object into a dictionary with dot-notation keys.
    """
    out = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + path_separator)
        elif type(x) is list:
            for i, a in enumerate(x):
                flatten(a, name + str(i) + path_separator)
        else:
            out[name[:-1]] = x
    flatten(y)
    return out

def get_language_code(json_content, filename):
    try:
        return json_content.get('meta', {}).get('language', os.path.splitext(filename)[0])
    except Exception:
        return os.path.splitext(filename)[0]

def set_seg_content(seg_element, text):
    """
    Parses the text for regex matches and creates <ph> elements
    inside the <seg> element.
    """
    if not text:
        return

    # Split text by the regex (keeping delimiters)
    parts = re.split(PLACEHOLDER_REGEX, str(text))
    
    # Text before the first placeholder
    seg_element.text = parts[0]
    
    # Iterate over matches. parts[1::2] are the placeholders
    for i in range(1, len(parts), 2):
        placeholder_text = parts[i]
        following_text = parts[i+1] if i + 1 < len(parts) else ""
        
        ph = ET.SubElement(seg_element, 'ph')
        ph.text = placeholder_text
        ph.tail = following_text

def indent_safe(elem, level=0, blocklist=None):
    """
    Custom indentation that skips specific tags (like 'seg') to avoid 
    inserting newlines into mixed content.
    """
    if blocklist is None:
        blocklist = ['seg']

    i = "\n" + level * "  "

    # If this element is blocked, we do NOT touch its text/children
    # We only fix its tail so the NEXT tag lines up correctly.
    if elem.tag in blocklist:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
        return

    # Standard indentation for structural elements
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
            
        for subelem in elem:
            indent_safe(subelem, level + 1, blocklist)
            
        # Fix the tail of the LAST child to ensure the closing tag 
        # starts on a new line
        if not elem[-1].tail or not elem[-1].tail.strip():
            elem[-1].tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def create_single_tmx(aligned_data, source_lang, target_lang):
    filename = f"{source_lang}_to_{target_lang}.tmx"
    
    tmx = ET.Element('tmx', {'version': '1.4'})
    
    # Header
    ET.SubElement(tmx, 'header', {
        'creationtool': 'PythonJsonToTmx',
        'creationtoolversion': '2.1',
        'segtype': 'sentence',
        'o-tmf': 'JSON',
        'adminlang': 'en-US',
        'srclang': source_lang,
        'datatype': 'PlainText',
        'creationdate': datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    })

    body = ET.SubElement(tmx, 'body')

    all_keys = sorted(aligned_data.keys())
    count = 0

    for key in all_keys:
        if key.startswith("meta."):
            continue

        if source_lang not in aligned_data[key]:
            continue
            
        target_text = aligned_data[key].get(target_lang, None)

        tu = ET.SubElement(body, 'tu', {'tuid': key})

        # Source
        tuv_source = ET.SubElement(tu, 'tuv', {'xml:lang': source_lang})
        seg_source = ET.SubElement(tuv_source, 'seg')
        set_seg_content(seg_source, aligned_data[key][source_lang])

        # Target
        if target_text is not None:
            tuv_target = ET.SubElement(tu, 'tuv', {'xml:lang': target_lang})
            seg_target = ET.SubElement(tuv_target, 'seg')
            set_seg_content(seg_target, target_text)
        
        count += 1

    # Apply Safe Indentation
    indent_safe(tmx, blocklist=['seg'])

    # Write using ElementTree (avoids minidom's aggressive formatting)
    tree = ET.ElementTree(tmx)
    tree.write(filename, encoding="utf-8", xml_declaration=True)

    print(f"Generated {filename} ({count} segments)")

def main():
    json_files = glob.glob("*.json")
    if not json_files:
        print("No JSON files found.")
        return

    alignment_map = {}
    detected_languages = set()

    print(f"Reading {len(json_files)} files...")

    for file in json_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = json.load(f)
            
            lang_code = get_language_code(content, file)
            detected_languages.add(lang_code)
            
            flat_content = flatten_json(content)
            
            for path, value in flat_content.items():
                if path not in alignment_map:
                    alignment_map[path] = {}
                alignment_map[path][lang_code] = value
                
        except Exception as e:
            print(f"Error reading {file}: {e}")

    if not detected_languages:
        print("No languages detected.")
        return

    sorted_langs = sorted(list(detected_languages))
    print("\nDetected languages:", ", ".join(sorted_langs))
    
    while True:
        source_lang = input(f"Enter Source Language code (e.g., {sorted_langs[0]}): ").strip()
        if source_lang in detected_languages:
            break
        print("Invalid language code.")

    target_langs = [l for l in sorted_langs if l != source_lang]
    
    print("\nProcessing...")
    for target in target_langs:
        create_single_tmx(alignment_map, source_lang, target)

    print("\nDone.")

if __name__ == "__main__":
    main()