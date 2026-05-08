# -*- coding: utf-8 -*-
import os
import zipfile
import shutil

def main():
    """
    This script automates Epiroc TXT file processing by:
      1) Creating/ensuring three folders: "source", "raw", and "fixed".
      2) Extracting all .zip files in the current directory into "source".
      3) Copying all .txt files from the current directory to "raw".
      4) For each .txt in "raw", aligns it with a file of the same name in "source".
         - Lines in "raw" that match "source" lines containing the marker "//TRANSLATE"
           are either preserved with "//PRESERVE" or cleaned of the marker, depending on
           whether they differ from the source line.
         - Lines in "source" without "//TRANSLATE" remain unchanged in the final output.
      5) Writes results to the "fixed" folder. 
      6) Removes "source" and "raw" folders upon completion.

    Usage:
      - Place this script alongside any .zip or .txt files.
      - Run the script. The processed and cleaned files will appear in "fixed".
      - Original "source" and "raw" folders are then removed.
    """

    base_path = os.getcwd()
    source_folder = os.path.join(base_path, 'source')
    raw_folder = os.path.join(base_path, 'raw')
    fixed_folder = os.path.join(base_path, 'fixed')

    # Marker used to decide if a line should be replaced or preserved.
    translate_marker = '//TRANSLATE'

    print(f"Working folder: {base_path}")

    # Ensure the three main folders exist or create them.
    for folder in (source_folder, raw_folder, fixed_folder):
        if not os.path.exists(folder):
            try:
                os.mkdir(folder)
            except OSError as e:
                print(f"[ERROR] Could not create folder '{folder}': {e}")
                return  # If critical folder creation fails, exit.

    # Gather a list of all files in the base directory.
    all_base_files = os.listdir(base_path)

    # 1) Extract all .zip files into "source".
    zip_files = [f for f in all_base_files if f.lower().endswith('.zip')]
    print("Zip files found:", zip_files)
    for zip_name in zip_files:
        zip_path = os.path.join(base_path, zip_name)
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(source_folder)
            print(f"[OK] Extracted '{zip_name}' into 'source' folder.")
        except (zipfile.BadZipFile, OSError) as e:
            print(f"[ERROR] Could not extract '{zip_name}': {e}")

    # 2) Copy all .txt files from base directory to "raw".
    txt_files = [f for f in all_base_files if f.lower().endswith('.txt')]
    for txt_name in txt_files:
        src_file = os.path.join(base_path, txt_name)
        dst_file = os.path.join(raw_folder, txt_name)
        try:
            shutil.copy(src_file, dst_file)
            print(f"[OK] Copied '{txt_name}' to 'raw' folder.")
        except shutil.Error as e:
            print(f"[ERROR] Could not copy '{txt_name}': {e}")

    # 3) List all files in "raw", then process them one by one.
    translated_files = os.listdir(raw_folder)
    print("List of translated files:", translated_files)

    for filename in translated_files:
        print("=" * 30)
        source_file_path = os.path.join(source_folder, filename)
        raw_file_path = os.path.join(raw_folder, filename)

        # If the corresponding source file doesn't exist, skip processing.
        if not os.path.exists(source_file_path):
            print(f"[SKIP] Source file for '{filename}' not found in 'source'.")
            continue

        # Track line counts for different categories:
        # j[0] = lines unchanged, j[1] = lines replaced with //PRESERVE,
        # j[2] = lines cleaned of //TRANSLATE
        j = [0, 0, 0]
        output_bytes = b''

        # Read both files in binary mode for exact line comparison.
        try:
            with open(source_file_path, "rb") as sf:
                source_lines = sf.readlines()
            with open(raw_file_path, "rb") as rf:
                raw_lines = rf.readlines()
        except (OSError, IOError) as e:
            print(f"[ERROR] Could not read file '{filename}': {e}")
            continue

        # Check for line count mismatch.
        if len(source_lines) != len(raw_lines):
            print(f"[WARNING] Different line counts in source vs. raw for '{filename}'. Skipping.")
            continue

        # Process line by line.
        for i in range(len(raw_lines)):
            line_source = source_lines[i]
            line_raw = raw_lines[i]
            decoded_source = line_source.decode("utf-8", errors="replace")
            decoded_raw = line_raw.decode("utf-8", errors="replace")

            # If the marker isn't in the source, leave the raw line untouched.
            if translate_marker not in decoded_source:
                output_bytes += line_raw
                j[0] += 1
                continue

            # If lines are identical and contain the marker -> replace with //PRESERVE
            if line_source == line_raw:
                temp = decoded_raw.replace(translate_marker, "//PRESERVE")
                j[1] += 1
            else:
                # Otherwise, remove the //TRANSLATE marker from the raw line.
                temp = decoded_raw.replace(translate_marker, "")
                j[2] += 1

            output_bytes += temp.encode("utf-8")

        # Write the processed file to the "fixed" folder.
        fixed_file_path = os.path.join(fixed_folder, filename)
        try:
            with open(fixed_file_path, "wb") as out_file:
                out_file.write(output_bytes)
        except (OSError, IOError) as e:
            print(f"[ERROR] Could not write fixed file '{filename}': {e}")
            continue

        print(f"[OK] Processed '{filename}'. Total lines: {len(raw_lines)}")
        print(f"      Unchanged lines: {j[0]} | Replaced lines: {j[1]} | Cleaned lines: {j[2]}")

    # 4) Remove temporary folders.
    for temp_folder in (source_folder, raw_folder):
        try:
            shutil.rmtree(temp_folder, ignore_errors=True)
            print(f"[OK] Removed '{temp_folder}' folder.")
        except OSError as e:
            print(f"[ERROR] Could not remove '{temp_folder}' folder: {e}")

    print("Done. Processed all Epiroc TXT files and placed results into 'fixed'.")

if __name__ == "__main__":
    main()
