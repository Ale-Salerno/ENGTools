import os
import sys
import re

def main():
    """
    This script scans all .xlf files in a specified directory (and subdirectories),
    ensuring that each <target> tag includes state="translated". Specifically:
      1) Any existing state="..." attributes get removed.
      2) A new state="translated" attribute is injected.
    
    Usage:
      python proofread_state.py [path_to_folder]
    
    If no path is provided, the current directory is used by default.
    """

    # Determine the directory to process (either the first sys.argv or current dir).
    if len(sys.argv) > 1:
        cwd = sys.argv[1]
    else:
        cwd = os.getcwd()

    # Regex pattern matching <target...> tags, capturing everything after <target until the closing '>'.
    target_pattern = re.compile(r'<target([^>]*)>')

    # Replacement function: remove any existing state attribute, then add state="translated".
    def fix_target(match):
        attrs = match.group(1)
        # Remove any existing state="..." attribute (and preceding whitespace).
        attrs = re.sub(r'\s*state="[^"]*"', '', attrs)
        # Insert state="translated" immediately after <target
        return f'<target state="translated"{attrs}>'

    file_count = 0
    updated_tags_total = 0

    # Walk through the directory (recursively).
    for root, dirs, files in os.walk(cwd):
        for filename in files:
            if filename.lower().endswith('.xlf'):
                file_path = os.path.join(root, filename)
                file_count += 1
                print(f"Processing file: {file_path}")

                # Read file contents (assuming UTF-8).
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        contents = f.read()
                except (OSError, IOError) as e:
                    print(f"[ERROR] Could not read '{file_path}': {e}")
                    continue

                # Apply regex substitution.
                # Count how many <target> tags get replaced.
                new_contents, num_subs = target_pattern.subn(fix_target, contents)
                updated_tags_total += num_subs

                # Write back if changes occurred.
                if new_contents != contents:
                    try:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_contents)
                        print(f"[OK] Updated {num_subs} <target> tag(s).")
                    except (OSError, IOError) as e:
                        print(f"[ERROR] Could not write '{file_path}': {e}")
                else:
                    print("[SKIP] No <target> tags modified.")

    print(f"\nProcessed {file_count} .xlf file(s).")
    print(f"Updated a total of {updated_tags_total} <target> tag(s) with state=\"translated\".")

if __name__ == "__main__":
    main()
