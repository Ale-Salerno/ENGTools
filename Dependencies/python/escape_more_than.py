import os
import re

def main():
    """
    This script walks through the current directory (and all its subdirectories) 
    searching for .xlf files. In each file, it looks for patterns like:
       (&lt;something>)
    that have an unescaped '>' and replaces it with '&gt;'.

    Specifically:
       search_pattern:  '((&lt;[^<]*))>'
       replace_pattern: '\1&gt;'

    This helps ensure that angle brackets within XLF files are properly escaped
    when '>' might otherwise be interpreted incorrectly.

    Usage:
      - Place this script in (or run it from) the directory containing .xlf files.
      - It recursively processes all .xlf files in subfolders as well.
      - Upon completion, prints a summary message.
    """

    cwd = os.getcwd()
    print(f"Starting 'escape_more_than.py' in directory: {cwd}")

    # Regex to find unescaped '>' after an "&lt;" block.
    search_pattern = re.compile(r'((&lt;[^<]*))>')
    replace_pattern = r'\1&gt;'

    processed_count = 0

    # Walk through each file in the current directory (including subdirectories).
    for root, dirs, files in os.walk(cwd):
        for filename in files:
            if filename.lower().endswith('.xlf'):
                file_path = os.path.join(root, filename)
                print(f"Processing file: {file_path}")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f_in:
                        contents = f_in.read()
                except (OSError, IOError) as e:
                    print(f"[ERROR] Could not read file '{filename}': {e}")
                    continue

                # Perform the search and replace.
                new_contents = search_pattern.sub(replace_pattern, contents)

                # Only write back if there is a change.
                if new_contents != contents:
                    try:
                        with open(file_path, 'w', encoding='utf-8') as f_out:
                            f_out.write(new_contents)
                        print(f"[OK] Updated file: {file_path}")
                    except (OSError, IOError) as e:
                        print(f"[ERROR] Could not write file '{filename}': {e}")
                        continue
                else:
                    print(f"[SKIP] No change required: {file_path}")

                processed_count += 1

    print(f"\nReplacement process complete. Processed {processed_count} .xlf file(s).")

if __name__ == "__main__":
    main()
