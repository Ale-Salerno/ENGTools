import os
import re

def process_pair(source_file, out_file):
    print(f"\nProcessing pair: '{source_file}' -> '{out_file}'")
    
    # Regex to match each entire <trans-unit> block
    tu_pattern = re.compile(r'(<trans-unit\b.*?>.*?</trans-unit>)', re.DOTALL)
    # Regex to find the <target> ... </target> portion inside a trans-unit
    target_pattern = re.compile(r'(<target\b[^>]*>.*?</target>)', re.DOTALL)
    # Regex to match se:pre-rate="XYZ"
    pr_rate_pattern = re.compile(r'\bse:pre-rate="(\d+)"')
    
    # 1) Read all <trans-unit> blocks from the source file ([locale]_target.xlf)
    with open(source_file, "r", encoding="utf-8") as f:
        source_text = f.read()
    source_units = tu_pattern.findall(source_text)
    
    # 2) Determine which trans-units have a <target> element with se:pre-rate >= 100
    updates = {}  # index -> new <target> element text
    for idx, block in enumerate(source_units):
        match = target_pattern.search(block)
        if not match:
            continue
        target_full = match.group(1)
        pr_match = pr_rate_pattern.search(target_full)
        if pr_match:
            try:
                rate_val = int(pr_match.group(1))
                if rate_val >= 100:
                    updates[idx] = target_full
            except ValueError:
                pass
    
    # 3) Read all <trans-unit> blocks from the target output file ([locale]_target.out.xlf)
    with open(out_file, "r", encoding="utf-8") as f:
        out_text = f.read()
    out_units = tu_pattern.findall(out_text)
    
    if not out_units:
        print(f"[ERROR] No <trans-unit> blocks found in '{out_file}'. Skipping.")
        return
    
    if len(source_units) != len(out_units):
        print(f"[WARNING] The files '{source_file}' and '{out_file}' have different counts of <trans-unit>: "
              f"{len(source_units)} vs. {len(out_units)}. Matching by position anyway.")
    
    updated_count = 0
    new_out_units = []
    for i, block in enumerate(out_units):
        if i in updates:
            new_target = updates[i]
            # Replace only the first <target> in that block with the updated version
            replaced_block, replacements = target_pattern.subn(new_target, block, count=1)
            if replacements > 0:
                updated_count += 1
                new_out_units.append(replaced_block)
            else:
                new_out_units.append(block)
        else:
            new_out_units.append(block)
    
    # 4) Reconstruct the out_file content while preserving text outside <trans-unit> blocks.
    container_pattern = re.compile(r'(<trans-unit\b.*?>.*?</trans-unit>)', re.DOTALL)
    def generator_func(_):
        return new_out_units.pop(0)
    
    new_out_text, n_subs = container_pattern.subn(generator_func, out_text)
    
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(new_out_text)
    
    print(f"Done. Updated {updated_count} <trans-unit> block(s) in '{out_file}'.")

def main():
    """
    This script processes all matching translation files in the current directory.
    
    It searches for source files matching the pattern:
        [locale]_target.xlf
    and then, for each, expects a corresponding output file:
        [locale]_target.out.xlf
    
    For each pair:
      1. Reads all <trans-unit> blocks from the source file.
      2. For each block, if the contained <target> element has a se:pre-rate attribute >= 100,
         that <target> element is captured.
      3. The captured <target> element is then used to replace the first <target> element
         in the corresponding <trans-unit> block (matched by position) in the output file.
      4. The updated content is then written back to the output file.
    
    If se:pre-rate is less than 100 for a block, that trans-unit remains unchanged.
    """
    # Find all source files matching the pattern [locale]_target.xlf
    source_pattern = re.compile(r'^(?P<locale>.+)_target\.xlf$', re.IGNORECASE)
    files = os.listdir('.')
    source_files = [f for f in files if source_pattern.match(f)]
    
    if not source_files:
        print("No matching source files found (e.g., [locale]_target.xlf). Aborting.")
        return
    
    for source_file in source_files:
        m = source_pattern.match(source_file)
        if not m:
            continue
        locale = m.group("locale")
        out_file = f"{locale}_target.out.xlf"
        if not os.path.isfile(out_file):
            print(f"[ERROR] Corresponding output file '{out_file}' not found for locale '{locale}'. Skipping this pair.")
            continue
        
        process_pair(source_file, out_file)

if __name__ == "__main__":
    main()
