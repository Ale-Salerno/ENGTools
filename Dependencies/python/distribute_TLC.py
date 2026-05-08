import os
import re
import shutil

def main():
    """
    This script organizes files in the current directory into subfolders based on a
    language code detected in the filename.

    Two filename patterns are recognized:
        1) (LangCode)      e.g. "Document(en).docx"
        2) _LangCode.      e.g. "Document_en.docx"

    For each file:
      - If a language code is found, the script moves the file into a subfolder named
        after that language code (creating the folder if needed).
      - If no language code is found, the file remains in the current directory.

    Excludes files ending with .ps1, .exe, .bat, .py to avoid processing script/executable
    files. Run this script in the directory where your files are located.
    """

    source_directory = os.getcwd()

    # Collect all files excluding scripts/executables.
    files = [
        f for f in os.listdir(source_directory)
        if os.path.isfile(os.path.join(source_directory, f))
        and not f.lower().endswith(('.ps1', '.exe', '.bat', '.py'))
    ]

    # Define regex patterns for potential language codes in filenames.
    language_patterns = [
        re.compile(r'\(([A-Za-z-]+)\)'),  # e.g. "MyFile(en).doc"
        re.compile(r'_([A-Za-z-]+)\.')    # e.g. "MyFile_en.doc"
    ]

    moved_count = 0  # Track how many files are moved

    for file_name in files:
        language_code = None

        # Attempt matching with any pattern to find a language code.
        for pattern in language_patterns:
            match = pattern.search(file_name)
            if match:
                language_code = match.group(1)
                break

        if language_code:
            folder_path = os.path.join(source_directory, language_code)
            if not os.path.exists(folder_path):
                # Create folder if it doesn't exist
                try:
                    os.makedirs(folder_path)
                except OSError as e:
                    print(f"[ERROR] Could not create folder '{folder_path}': {e}")
                    continue

            # Attempt to move the file
            src_file = os.path.join(source_directory, file_name)
            dst_file = os.path.join(folder_path, file_name)
            try:
                shutil.move(src_file, dst_file)
                print(f"[OK] Moved '{file_name}' to '{language_code}' folder.")
                moved_count += 1
            except shutil.Error as e:
                print(f"[ERROR] Could not move '{file_name}' to '{language_code}' folder: {e}")
        else:
            print(f"[SKIP] No language code found in '{file_name}'. File remains in place.")

    print(f"\nDone. Moved {moved_count} file(s) to language folders.")

if __name__ == "__main__":
    main()
