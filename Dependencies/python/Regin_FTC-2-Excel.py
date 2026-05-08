import os
import re
import openpyxl

# Dictionary mapping known language codes (in parentheses) to their descriptive names.
LANGUAGE_CODES = {
    "(chi-CN)": "Chinese (China)",
    "(chi-TW)": "Chinese (Taiwan)",
    "(chi-HK)": "Chinese (Hong-Kong)",
    "(cze)":    "Czech",
    "(dan)":    "Danish",
    "(dut-NL)": "Dutch (Netherlands)",
    "(dut-BE)": "Dutch (Belgium)",
    "(eng-GB)": "English",
    "(eng-US)": "English (United-States)",
    "(est)":    "Estonian",
    "(fin)":    "Finnish",
    "(fre-FR)": "French",
    "(fre-CA)": "French (Canada)",
    "(fre-CH)": "French (Switzerland)",
    "(fre-BE)": "French (Belgium)",
    "(ger-DE)": "German",
    "(ger-AT)": "German (Austria)",
    "(ger-CH)": "German (Switzerland)",
    "(hun)":    "Hungarian",
    "(ita-IT)": "Italian",
    "(jpn)":    "Japanese",
    "(kor)":    "Korean",
    "(lav)":    "Latvian",
    "(lit)":    "Lithuanian",
    "(nob)":    "Norwegian",
    "(pol)":    "Polish",
    "(por-BR)": "Portuguese (Brazil)",
    "(por-PT)": "Portuguese (Portugal)",
    "(rum)":    "Romanian",
    "(rus)":    "Russian",
    "(slo)":    "Slovak",
    "(slv)":    "Slovenian",
    "(spa-ES)": "Spanish",
    "(swe-SE)": "Swedish",
    "(tur)":    "Turkish",
}

def create_translation_excel(input_folder, output_folder):
    translation_data = {}
    languages = set()
    base_names = set()
    unrecognized_codes = set()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".en", ".enu")):
            match = re.search(r"^(.*?)(\(.*?\))\.(en|enu|Enu)$", filename)
            if not match:
                continue

            base_name = match.group(1)
            lang_code = match.group(2)
            base_names.add(base_name)

            if lang_code in LANGUAGE_CODES:
                lang_name = LANGUAGE_CODES[lang_code]
                languages.add(lang_name)
            else:
                unrecognized_codes.add(lang_code)
                lang_name = lang_code
                languages.add(lang_name)

            filepath = os.path.join(input_folder, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.readlines()
            except UnicodeDecodeError:
                with open(filepath, "r", encoding="cp1252") as f:
                    content = f.readlines()
            
            for line in content:
                line = line.strip()
                if line.startswith(";") or line.startswith("Name ="):
                    continue
                
                match = re.match(r"(\d+)\s*=\s*(?:\"(.*?)\"|\[(.*?)\]|(.+?)(?=\s*\d+\s*=|$))", line)
                if match:
                    key, single_value, multiline_value, other_value = match.groups()
                    key = key.strip()
                    value = (single_value or multiline_value or other_value or "").strip()
                    value = value.replace('[', '').replace(']', '').strip('"')

                    if key not in translation_data:
                        translation_data[key] = {}
                    translation_data[key][lang_name] = value

    if unrecognized_codes:
        print("[WARNING] The following language codes were not recognized and will be used as-is:")
        print(", ".join(unrecognized_codes))

    if not base_names:
        print("No valid .en or .enu files found. No Excel created.")
        return
    elif len(base_names) > 1:
        print("[WARNING] Multiple different base names found. Will use the first one:")
        print(", ".join(base_names))

    final_base_name = list(base_names)[0]

    workbook = openpyxl.Workbook()
    sheet = workbook.active

    languages_sorted = sorted(list(languages))
    header = ["Key"] + languages_sorted
    sheet.append(header)

    for key, translations in translation_data.items():
        row = [key] + [translations.get(lang, "") for lang in languages_sorted]
        sheet.append(row)

    excel_filename = os.path.join(output_folder, f"{final_base_name}.xlsx")
    try:
        workbook.save(excel_filename)
        print(f"[OK] Translations saved to '{excel_filename}'.")
    except Exception as e:
        print(f"[ERROR] Could not save Excel file '{excel_filename}': {e}")

def main():
    input_folder = "i"
    output_folder = "o"

    if not os.path.isdir(input_folder):
        print(f"[ERROR] Input folder '{input_folder}' not found. Please create it and put the .en or .enu files there.")
        return

    create_translation_excel(input_folder, output_folder)

if __name__ == "__main__":
    main()
