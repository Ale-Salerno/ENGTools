#!/usr/bin/env python3
"""
Scholly Merge: QA Update Tool.

- Finds all *.json files (from QA report exports).
- Merges changes directly back into the original CSV files.
"""

import pandas as pd
import os
import json
import glob

def merge_csv_changes(json_filepath):
    """
    Parses a JSON file and merges changes into the specified source CSV.
    """
    
    print(f"--- Processing '{json_filepath}' ---")
    try:
        with open(json_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"  ERROR: Could not read JSON file. {e}")
        return

    # Key is 'source_xlf' as defined in the JS export function
    source_csv = data.get('source_xlf') 
    modified_units = data.get('modified_units')

    if not source_csv or not modified_units:
        print("  ERROR: JSON is invalid. Missing 'source_xlf' or 'modified_units' key. Skipping.")
        return

    if not os.path.exists(source_csv):
        print(f"  ERROR: Source CSV file '{source_csv}' not found in this directory. Skipping.")
        return
        
    # Load the source CSV
    try:
        df = pd.read_csv(source_csv, sep=';')
        # Check for the expected Variable Name column
        if 'Variable Name' not in df.columns:
            print(f"  ERROR: Source CSV '{source_csv}' is missing the 'Variable Name' column. Skipping.")
            return
            
        # Get original column order before we set the index
        original_cols = df.columns.tolist()
            
        df.set_index('Variable Name', inplace=True)
    except Exception as e:
        print(f"  ERROR: Could not read or process source CSV '{source_csv}'. {e}")
        return
        
    print(f"  Updating '{source_csv}' with {len(modified_units)} changes...")
    changes_applied = 0
    
    for resname, new_text in modified_units.items():
        if resname in df.index:
            # Update the 'Translation' column for the matching resname
            df.loc[resname, 'Translation'] = new_text
            changes_applied += 1
        else:
            print(f"    WARNING: resname '{resname}' from JSON not found in CSV.")

    # Save the updated CSV (Overwriting original)
    try:
        # Reset index to get 'Variable Name' back as a column
        df.reset_index(inplace=True)
        
        # Set output to the original filename to overwrite it
        output_csv = source_csv 
        
        # Re-apply original column order
        df = df[original_cols] 
        
        df.to_csv(output_csv, sep=';', index=False, encoding='utf-8')
        print(f"  Success! Overwrote {output_csv} with {changes_applied} changes.")
    except Exception as e:
        print(f"  ERROR: Could not write updated CSV '{output_csv}'. {e}")

def main():
    print("--- Batch CSV Merge (Task: Merge CSV) ---")
    json_files = glob.glob('*.json')
    
    if not json_files:
        print("  No .json files found to merge.")
        return

    print(f"Found {len(json_files)} JSON file(s) to process.")
    total_merged = 0
    
    for json_file in json_files:
        # Simple check to avoid processing a file that might be a config
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                preview = f.read(200)
            if "modified_units" in preview and "source_xlf" in preview:
                merge_csv_changes(json_file)
                total_merged += 1
            else:
                print(f"  Skipping '{json_file}' (does not appear to be a report export).")
        except Exception as e:
            print(f"  Could not read '{json_file}'. Skipping. Error: {e}")
    
    print(f"\nBatch merge complete. Processed {total_merged} JSON file(s).")

if __name__ == "__main__":
    main()