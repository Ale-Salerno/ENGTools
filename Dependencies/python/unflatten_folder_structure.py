import os
import shutil
import sys

def main():
    """
    This script reverses the "flattening" process performed by flatten_folder_structure.py.
    It looks for a 'FLATTEN' folder in the current working directory, then:
      1) Iterates through each file in 'FLATTEN'.
      2) Splits the filename by the separator '$'. 
         - The parts before the last element represent subfolders.
         - The last element is the original filename.
      3) Recreates the subfolder structure in the original working directory.
      4) Moves each file from 'FLATTEN' back to its original location.

    Example:
      If flatten_folder_structure.py produced a file named 
        "Subfolder$Subsubfolder$example.txt"
      in 'FLATTEN', this script will reconstruct:
        ./Subfolder/Subsubfolder/example.txt
      relative to the current working directory.

    Usage:
      1) Ensure a folder named 'FLATTEN' is present in the current directory, 
         containing the flattened files with '$' in their names.
      2) Run this script. The script will move each file in 'FLATTEN' back 
         to its appropriate subdirectory path.
    """
    separator = '$'
    working_directory = os.getcwd()
    flatten_folder = os.path.join(working_directory, "FLATTEN")

    # Check if the 'FLATTEN' folder exists
    if not os.path.isdir(flatten_folder):
        print(f"[ERROR] No 'FLATTEN' folder found at: {flatten_folder}")
        sys.exit(1)

    # Traverse the 'FLATTEN' folder
    for dirpath, dirnames, filenames in os.walk(flatten_folder):
        for filename in filenames:
            # Split the flattened filename into path parts
            parts = filename.split(separator)

            # All parts except the last form the subfolders; last is the original filename
            target_dir = working_directory
            for part in parts[:-1]:
                target_dir = os.path.join(target_dir, part)

            original_filename = parts[-1]
            source_path = os.path.join(dirpath, filename)
            target_path = os.path.join(target_dir, original_filename)

            # Ensure the target folder structure exists
            try:
                os.makedirs(target_dir, exist_ok=True)
            except OSError as e:
                print(f"[ERROR] Could not create directory '{target_dir}': {e}")
                continue

            # Move the file to its reconstructed subfolder
            try:
                shutil.move(source_path, target_path)
                print(f"[OK] Restored '{filename}' to '{target_path}'")
            except (shutil.Error, OSError) as e:
                print(f"[ERROR] Could not move '{filename}' to '{target_path}': {e}")

    print("All files have been moved to their original locations based on the '$' separators.")

if __name__ == "__main__":
    main()
