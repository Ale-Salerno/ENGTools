import os
import re

def rename_files():
    """
    Searches the current directory for files whose names match the pattern:
        * (XYZ) . <allowed extension>
    and removes the parenthetical locale code.
    
    By default, allowed extensions are: xlf, tsxlf, sdlxliff
    Example:
      MyFile(eng-GB).xlf  ->  MyFile.xlf
      AnotherFile(ger-DE).sdlxliff  ->  AnotherFile.sdlxliff
    """
    allowed_exts = {'xlf', 'tsxlf', 'sdlxliff'}

    # This pattern looks for:
    #   '('
    #   one or more letters (A-Z), optional digits 0-9, or dash/underscore
    #   ')'
    # only if immediately followed by a dot + one of the allowed extensions at the end of the filename.
    # e.g.:  "Data(eng-US).xlf" -> remove "(eng-US)" if preceded by .xlf at the end.
    pattern = re.compile(
        r'\([A-Za-z0-9_-]+\)(?=\.(?:' + '|'.join(allowed_exts) + r')$)',
        flags=re.IGNORECASE
    )

    for filename in os.listdir('.'):
        # Check if it ends with an allowed extension (case-insensitive)
        lower_filename = filename.lower()
        if any(lower_filename.endswith(f".{ext}") for ext in allowed_exts):
            # Perform the regex substitution
            new_filename = pattern.sub('', filename)
            if new_filename != filename:
                try:
                    print(f"Renaming: {filename} -> {new_filename}")
                    os.rename(filename, new_filename)
                except Exception as e:
                    print(f"[ERROR] Could not rename '{filename}': {e}")

if __name__ == '__main__':
    rename_files()
