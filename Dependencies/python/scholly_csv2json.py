import pandas as pd
import json
import glob
import os

def batch_convert_csv_to_json():
    # Find all CSV files matching the pattern "updated_*.csv"
    csv_files = glob.glob('*.csv')
    
    if not csv_files:
        print("No files found matching 'updated_*.csv' in the current directory.")
        return

    print(f"Found {len(csv_files)} file(s) to process: {csv_files}")

    for csv_file in csv_files:
        try:
            # Extract language code from filename (e.g., 'updated_de-DE.csv' -> 'de-DE')
            base_name = os.path.basename(csv_file)
            lang_code = base_name.replace('', '').replace('.csv', '')
            
            # Define output filename
            output_filename = f"{lang_code}.json"
            
            # --- Conversion Logic Starts Here ---
            
            # Load CSV
            df = pd.read_csv(csv_file, sep=';')
            
            # Filter clean data
            df = df[df['Variable Name'].notna()]
            df = df[df['Translation'].notna()]
            df = df.sort_values('Variable Name')

            result_json = {}

            # 1. Extract Meta Data
            # We read the raw file again to get the header row safely
            meta_row = pd.read_csv(csv_file, sep=';').iloc[0]
            result_json['meta'] = {
                "version": meta_row['version'],
                "language": meta_row['language'],
                "dropdown_name": meta_row['dropdown_name'],
                "date": meta_row['Export Date']
            }

            # 2. Process Content
            for index, row in df.iterrows():
                path_str = row['Variable Name']
                translation = row['Translation']
                
                # Normalize separators
                normalized_path = path_str.replace('/', ':')
                parts = normalized_path.split(':')
                
                current = result_json
                
                for i, part in enumerate(parts):
                    is_last = (i == len(parts) - 1)
                    
                    if is_last:
                        # Assign translation
                        if part in current and isinstance(current[part], dict):
                            print(f"Warning in {csv_file}: Key '{part}' in path '{path_str}' is already a container.")
                        else:
                            current[part] = translation
                    else:
                        # Build/Traverse hierarchy
                        if part not in current:
                            current[part] = {}
                            current = current[part]
                        else:
                            # Handle Conflict: Path vs Leaf
                            if isinstance(current[part], str):
                                remaining_key = ":".join(parts[i:])
                                current[remaining_key] = translation
                                break 
                            else:
                                current = current[part]

            # 3. Save to JSON
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(result_json, f, indent=2, ensure_ascii=False)
            
            print(f"Successfully converted '{csv_file}' to '{output_filename}'")
            
        except Exception as e:
            print(f"Error processing {csv_file}: {e}")

# Run the batch process
if __name__ == "__main__":
    batch_convert_csv_to_json()