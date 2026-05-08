import os
import shutil
import sys

def main():
    """
    This script walks through the current directory (recursively) and copies
    all files (except .bat files and the script itself) into a single 'FLATTEN'
    folder, renaming them with a separator to preserve subfolder path information.

    Example:
      If you have a file at:
        ./Subfolder/Subsubfolder/example.txt
      It gets copied to:
        ./FLATTEN/Subfolder$Subsubfolder$example.txt

    Steps:
      1) Create or reuse a folder named 'FLATTEN' in the current directory.
      2) Recursively visit all subdirectories.
      3) Skip:
         - The 'FLATTEN' folder itself
         - This Python script
         - Any .bat files
      4) Copy each file into the 'FLATTEN' folder. The path's subfolders are
         joined using a dollar sign ($).
    """

    separator = '$'
    working_directory = os.getcwd()

    # Create (or reuse) the 'FLATTEN' folder in the current directory.
    flatten_folder = os.path.join(working_directory, "FLATTEN")
    try:
        os.makedirs(flatten_folder, exist_ok=True)
    except OSError as e:
        print(f"[ERROR] Could not create 'FLATTEN' folder: {e}")
        sys.exit(1)

    script_path = os.path.abspath(__file__)
    file_count = 0

    for dirpath, dirnames, filenames in os.walk(working_directory):
        # Skip the 'FLATTEN' folder to avoid reprocessing copied files.
        if os.path.abspath(dirpath) == os.path.abspath(flatten_folder):
            continue

        for filename in filenames:
            source_path = os.path.join(dirpath, filename)

            # Skip this Python script itself.
            if os.path.abspath(source_path) == script_path:
                continue

            # Skip .bat files.
            if filename.lower().endswith('.bat'):
                continue

            # Construct the relative path from working_directory to dirpath.
            relative_path = os.path.relpath(dirpath, working_directory)

            # Build the new filename by concatenating all subfolder names plus the original filename.
            new_filename = separator.join(relative_path.split(os.path.sep)) + separator + filename

            # If relative_path is '.', this means the file is in the root
            # directory, so avoid adding an extra separator.
            if relative_path == '.':
                new_filename = filename

            # Build the destination path in the 'FLATTEN' folder.
            destination_path = os.path.join(flatten_folder, new_filename)

            # Ensure the destination subfolders exist if the user used
            # the separator in folder names (rare but possible).
            try:
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            except OSError as e:
                print(f"[ERROR] Could not create directory for '{destination_path}': {e}")
                continue

            # Copy the file, preserving metadata (timestamps, etc.).
            try:
                shutil.copy2(source_path, destination_path)
                file_count += 1
            except (shutil.Error, OSError) as e:
                print(f"[ERROR] Could not copy '{source_path}' to '{destination_path}': {e}")

    print(f"\nCopied and renamed {file_count} file(s) to the 'FLATTEN' folder.")

if __name__ == "__main__":
    main()
