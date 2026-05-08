#!/usr/bin/env python3
import glob
import sys
import re
import xml.etree.ElementTree as ET

def register_namespaces_from_header(path):
    """
    Read the first few lines of the file to pick up the
    xmlns="…" and xmlns:sdl="…" declarations, and
    register them with ElementTree so they get the correct prefixes
    on write().
    """
    header = []
    with open(path, encoding='utf-8') as f:
        for _ in range(10):
            line = f.readline()
            if not line:
                break
            header.append(line)
    header = "".join(header)

    # default namespace (xliff)
    m = re.search(r'\sxmlns="([^"]+)"', header)
    if m:
        ET.register_namespace('', m.group(1))

    # sdl extension namespace
    m = re.search(r'\sxmlns:(sdl)="([^"]+)"', header)
    if m:
        ET.register_namespace(m.group(1), m.group(2))

    # (optional) xsi, if you happen to have it
    m = re.search(r'\sxmlns:(xsi)="([^"]+)"', header)
    if m:
        ET.register_namespace(m.group(1), m.group(2))


def process_file(path):
    # pick up & re-register your prefixes
    register_namespaces_from_header(path)

    tree = ET.parse(path)
    root = tree.getroot()
    changed = False

    # 1) Mark every <target> as translated
    for tgt in root.findall('.//{*}target'):
        if tgt.get('state') != 'translated':
            tgt.set('state', 'translated')
            changed = True

    # 2) Ensure each <sdl:seg> has the SDL metadata Trados expects
    for seg in root.findall('.//{*}seg-defs/{*}seg'):
        if seg.get('conf') != 'Translated':
            seg.set('conf', 'Translated')
            changed = True
        if seg.get('percent') != '100':
            seg.set('percent', '100')
            changed = True

    if changed:
        tree.write(path, 
                   encoding='utf-8', 
                   xml_declaration=True)
        print(f"✔ Updated: {path}")
    else:
        print(f"─ No changes needed: {path}")


def main():
    files = glob.glob('*.sdlxliff')
    if not files:
        print("No .sdlxliff files found.")
        sys.exit(1)

    for fn in files:
        try:
            process_file(fn)
        except Exception as e:
            print(f"✘ Failed to process {fn}: {e}")


if __name__ == '__main__':
    main()
