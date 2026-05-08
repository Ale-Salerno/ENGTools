import os
import sys
import xml.etree.ElementTree as ET

def main():
    """
    This script processes all .xlf files in the current directory.

    For each file:
      1. Parse the file to extract the <file> element's target-language attribute.
      2. If the target-language is one of: 'es-es', 'fr-fr', 'de-de', 'it-it', rename the file to '[locale]_source.xlf'.
      3. Otherwise, rename the file to '[locale]_target.xlf', where [locale] is the target-language attribute in lowercase.

    If a file lacks a target-language attribute or the <file> element, a warning is printed.
    Renaming is skipped if the file is already correctly named or if a naming collision occurs.
    """
    # Collect all .xlf files in the current directory.
    all_xlf = [f for f in os.listdir('.') if f.lower().endswith('.xlf')]
    file_count = len(all_xlf)
    print(f"Found {file_count} XLF file(s). Processing all files.")

    # Languages that should be renamed as "source" variant.
    allowed_langs = {'es-es', 'fr-fr', 'de-de', 'it-it', 'nl-nl','pt-br','en-gb'}
    ns = {'xliff': 'urn:oasis:names:tc:xliff:document:1.2'}

    def get_target_language(filepath):
        """
        Parse the XLF file to extract the target-language attribute.
        Returns the attribute value, or None if not found or on parse error.
        """
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
        except Exception as e:
            print(f"[ERROR] Could not parse '{filepath}': {e}")
            return None

        file_elem = root.find('.//xliff:file', ns)
        if file_elem is None:
            print(f"[ERROR] No <file> element found in '{filepath}'.")
            return None

        target_lang = file_elem.get("target-language")
        if target_lang is None:
            print(f"[WARN] No target-language attribute found in '{filepath}'. Defaulting to 'target'.")
        return target_lang

    # Process each XLF file.
    for filename in all_xlf:
        target_lang = get_target_language(filename)
        if target_lang is None:
            # Default to target if target language is not found.
            target_lang = "target"
        tl_lower = target_lang.lower()

        if tl_lower in allowed_langs:
            new_name = f"{tl_lower}_source.xlf"
        else:
            new_name = f"{tl_lower}_target.xlf"
        
        # Skip renaming if the file already has the correct name.
        if filename.lower() == new_name.lower():
            print(f"[SKIP] '{filename}' is already correctly named '{new_name}'.")
            continue

        # Check for collision.
        if os.path.exists(new_name):
            print(f"[WARN] Cannot rename '{filename}' to '{new_name}' because '{new_name}' already exists.")
            continue

        try:
            os.rename(filename, new_name)
            print(f"[OK] Renamed '{filename}' -> '{new_name}'.")
        except Exception as e:
            print(f"[ERROR] Could not rename '{filename}' to '{new_name}': {e}")

if __name__ == "__main__":
    main()
