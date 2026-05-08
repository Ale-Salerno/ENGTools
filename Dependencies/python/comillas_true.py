import os
import json
import shutil

# Set working directory to script's folder
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print(f"Working directory set to: {script_dir}")

# Backup folder path
backup_folder = os.path.join(script_dir, "Backup")

# Create Backup folder if it doesn't exist
os.makedirs(backup_folder, exist_ok=True)

def fix_file(filepath):
    actual_changes = 0
    try:
        # Change encoding to 'utf-8-sig' to handle files with BOM
        with open(filepath, "r", encoding="utf-8-sig") as f: 
            content = json.load(f)

        if "Entries" in content and isinstance(content["Entries"], list):
            for entry in content["Entries"]:
                # Ensure the entry is a dictionary and 'Translate' key exists and is true
                if isinstance(entry, dict) and entry.get("Translate") is True:
                    current_translation = entry.get("Translation")

                    # Case 1: If 'Translation' is null, change it to an empty string ""
                    if current_translation is None:
                        entry["Translation"] = ""
                        actual_changes += 1
                        # Continue to the next entry as "" is already a quoted string
                        continue 

                    # Case 2: If 'Translation' is a string but not quoted, wrap it in quotes
                    # This check only runs if Case 1 (null to "") didn't apply
                    if isinstance(current_translation, str) and \
                       not (current_translation.startswith('"') and current_translation.endswith('"')):
                        entry["Translation"] = f'"{current_translation}"'
                        actual_changes += 1
        
        if actual_changes > 0:
            # When writing, we can stick to 'utf-8' if no BOM is desired in output
            # Or use 'utf-8-sig' if you want to preserve/add BOM on write (less common for JSON)
            # Sticking to 'utf-8' for cleaner output by default
            with open(filepath, "w", encoding="utf-8") as f: 
                # Use indent=2 for pretty printing and ensure_ascii=False for proper handling of non-ASCII characters
                json.dump(content, f, indent=2, ensure_ascii=False)
            print(f"✅ {filepath}: fixed {actual_changes} entr{'y' if actual_changes == 1 else 'ies'}.")
        else:
            print(f"ℹ️ {filepath}: no changes needed.")

    except json.JSONDecodeError as e:
        print(f"❌ Error decoding JSON from {filepath}: {e}")
    except Exception as e:
        print(f"❌ An error occurred while processing {filepath}: {e}")

def main():
    json_files = [f for f in os.listdir(".") if f.endswith(".json")]
    if not json_files:
        print("⚠️ No JSON files found in current folder.")
        return

    # Backup all files first
    for file in json_files:
        shutil.copy(file, os.path.join(backup_folder, file))
    print(f"Backup complete: copied {len(json_files)} files to '{backup_folder}'.")

    # Process each file
    for file in json_files:
        fix_file(file)

if __name__ == "__main__":
    main()