import os
import glob
import xml.etree.ElementTree as ET

def has_source_segment(filepath):
    """
    Checks whether the .xlf XML file at 'filepath' has at least one <source> element.
    Returns True if a <source> is found, False otherwise.

    - Uses a simple tag comparison that ends with 'source', which is robust
      for both namespaced and non-namespaced XML.
    - If the file fails to parse, it's treated as having no source segments.
    """
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        # Look through all elements to find any whose tag ends with 'source'.
        for elem in root.iter():
            if elem.tag.endswith("source"):
                return True
        return False
    except ET.ParseError as e:
        print(f"[ERROR] Could not parse '{filepath}': {e}")
        # If it can't be parsed, treat it as "empty".
        return False

def main():
    """
    Searches the current directory for all .xlf files and removes
    those that contain no <source> elements.
    """
    xlf_files = glob.glob("*.xlf")
    if not xlf_files:
        print("No .xlf files found in the current directory.")
        return

    for filepath in xlf_files:
        if has_source_segment(filepath):
            print(f"[KEEP] File '{filepath}' contains source segments.")
        else:
            print(f"[DELETE] Removing empty file: '{filepath}'")
            os.remove(filepath)

if __name__ == "__main__":
    main()
