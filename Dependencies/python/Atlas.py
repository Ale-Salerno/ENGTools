import os
import re
import zipfile
import pandas as pd
import sys
import tempfile
from pathlib import Path

# Configuration
XML_TAG = 'PrintByLine'
DEBUG_MODE = True  # Set to False to reduce output
EXCEL_FILE = 'mapping_Atlas.xlsx'

def debug_print(message):
    if DEBUG_MODE:
        print(message)

def setup_environment():
    """Set up paths and validate environment"""
    script_dir = Path(__file__).parent.resolve()
    os.chdir(script_dir)
    
    excel_path = script_dir / EXCEL_FILE
    if not excel_path.exists():
        print(f"ERROR: {EXCEL_FILE} not found in script directory: {script_dir}")
        input("Press Enter to exit...")
        sys.exit(1)
    
    return script_dir, excel_path

def load_mappings(excel_path):
    """Load Atlas language mappings from Excel"""
    try:
        df = pd.read_excel(excel_path)
        required_cols = ['Language_Code', 'Suffix']
        
        if not all(col in df.columns for col in required_cols):
            print(f"ERROR: Excel missing required columns: {required_cols}")
            return None
        
        lang_map = {}
        for _, row in df.iterrows():
            lang_code = str(row['Language_Code']).strip().lower()
            suffix = str(row['Suffix']) if pd.notna(row['Suffix']) else ''
            lang_map[lang_code] = suffix
        
        debug_print(f"Loaded {len(lang_map)} Atlas language mappings")
        return lang_map
    
    except Exception as e:
        print(f"ERROR reading Excel file: {str(e)}")
        return None

def extract_language_code(file_name):
    """Extract language code from zip file name"""
    match = re.search(r'\b([a-z]{2}_[a-z]{2})\b', file_name, re.IGNORECASE)
    return match.group(1).lower() if match else None

def process_zip_file(zip_path, lang_map):
    """Process a single zip file - extract, update XMLs, re-zip with same name"""
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Extract zip to temp directory
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_path)
                debug_print(f"  Extracted to: {temp_path}")
            
            # Process all XML files
            xml_files = list(temp_path.rglob('*.xml'))
            updated_count = 0
            
            for xml_file in xml_files:
                if update_xml_file(xml_file, lang_map):
                    updated_count += 1
            
            # Create new zip with original name
            temp_zip_path = zip_path.with_suffix('.temp.zip')
            with zipfile.ZipFile(temp_zip_path, 'w', zipfile.ZIP_DEFLATED) as new_zip:
                for file in temp_path.rglob('*'):
                    if file.is_file():
                        rel_path = file.relative_to(temp_path)
                        new_zip.write(file, rel_path)
            
            # Replace original zip with the updated one
            zip_path.unlink()
            temp_zip_path.rename(zip_path)
            
            return updated_count, zip_path
    
    except Exception as e:
        debug_print(f"  ERROR processing zip: {str(e)}")
        return 0, None

def update_xml_file(xml_path, lang_map):
    """Update PrintByLine tags in XML file - fixed for multiple occurrences"""
    try:
        debug_print(f"\nProcessing: {xml_path.name}")
        
        # Extract language code from XML path
        lang_code = None
        for part in xml_path.parts:
            match = re.search(r'\b([a-z]{2}_[a-z]{2})\b', part, re.IGNORECASE)
            if match:
                lang_code = match.group(1).lower()
                break
        
        if not lang_code:
            debug_print("  ⚠️ Could not determine language from file path")
            return False
        
        suffix = lang_map.get(lang_code, '')
        debug_print(f"  Detected language: {lang_code}, Suffix: '{suffix}'")
        
        with open(xml_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if target tag exists
        if f'<{XML_TAG}>' not in content:
            debug_print(f"  Skipping: No '{XML_TAG}' tag found")
            return False
        
        # Count occurrences before modification
        initial_count = content.count(f'<{XML_TAG}>')
        debug_print(f"  Found {initial_count} '{XML_TAG}' tags")
        
        # Create a regex pattern to match PrintByLine tags with their content
        # This pattern captures the entire tag so we can replace it in one go
        def replace_tag(match):
            full_tag = match.group(0)  # The entire matched tag
            # Extract content between the tags
            content_start = match.group(0).find('>') + 1
            content_end = match.group(0).rfind('<')
            original_content = match.group(0)[content_start:content_end].strip()
            
            if not original_content:
                return full_tag  # Return unchanged if empty
            
            # Remove any existing suffix (underscore + 2 letters)
            base_value = re.sub(r'_[A-Za-z]{2}$', '', original_content)
            
            # Add new suffix if needed
            new_value = base_value + (f"_{suffix}" if suffix else "")
            
            # Reconstruct the tag with new value
            return f'<{XML_TAG}>{new_value}</{XML_TAG}>'
        
        # Use a non-greedy pattern to match each tag individually
        # The pattern: <PrintByLine>any content except <</PrintByLine>
        pattern = re.compile(rf'<{XML_TAG}>[^<]*</{XML_TAG}>')
        
        # Replace all occurrences in one pass
        new_content = pattern.sub(replace_tag, content)
        
        # Check if anything changed
        if new_content != content:
            with open(xml_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # Count how many were actually updated
            updated_count = 0
            # Simple check: count tags with suffix in new content
            for match in pattern.finditer(new_content):
                tag_content = match.group(0)
                content_start = tag_content.find('>') + 1
                content_end = tag_content.rfind('<')
                tag_value = tag_content[content_start:content_end].strip()
                if suffix and tag_value.endswith(f'_{suffix}'):
                    updated_count += 1
                elif not suffix and not re.search(r'_[A-Za-z]{2}$', tag_value):
                    updated_count += 1
            
            debug_print(f"  Updated {updated_count} tags")
            debug_print("  File updated successfully")
            return True
        else:
            debug_print("  No changes needed")
            return False
    
    except Exception as e:
        debug_print(f"  ERROR processing file: {str(e)}")
        return False

def main():
    script_dir, excel_path = setup_environment()
    debug_print(f"Script directory: {script_dir}")
    
    lang_map = load_mappings(excel_path)
    if lang_map is None:
        input("Press Enter to exit...")
        sys.exit(1)
    
    processed_zips = 0
    processed_files = 0
    
    debug_print("\nStarting zip file processing...")
    for zip_file in script_dir.glob('*.zip'):
        lang_code = extract_language_code(zip_file.name)
        if not lang_code:
            debug_print(f"\nSkipping non-language zip: {zip_file.name}")
            continue
        
        print(f"\nProcessing: {zip_file.name} [{lang_code}]")
        
        updated_count, output_path = process_zip_file(zip_file, lang_map)
        
        if updated_count:
            print(f"  Updated {updated_count} files in: {output_path.name}")
            processed_files += updated_count
            processed_zips += 1
        else:
            print("  No files required updates")
    
    print(f"\nProcessing complete. Updated {processed_files} files across {processed_zips} zip archives.")

if __name__ == "__main__":
    main()