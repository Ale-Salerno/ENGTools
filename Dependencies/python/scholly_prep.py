#!/usr/bin/env python3
"""
Scholly Prep: Localization File Merger & Generator.

- Merges 'ui_texts_en.csv' and 'notifications_en-US.csv'.
- Cleans data and adds metadata.
- Creates a master 'en.csv' and placeholder copies for other languages.
"""

import pandas as pd
import shutil
import os

def main():
    # Configuration
    input_ui = 'ui_texts_en.csv'
    input_notif = 'notifications_en-US.csv'
    output_master = 'en.csv'

    print("--- Localization File Merger & Generator (Task: Prep) ---")

    # 1. User Input for Version
    version_input = input("Please enter the Version number (e.g., 0.1.0): ")
    if not version_input.strip():
         version_input = '0.1.0'

    try:
        # 2. Load Files
        if not os.path.exists(input_ui):
             raise FileNotFoundError(f"Input file not found: {input_ui}")
        if not os.path.exists(input_notif):
             raise FileNotFoundError(f"Input file not found: {input_notif}")

        # Both files use a semicolon delimiter
        df_ui = pd.read_csv(input_ui, sep=';')
        df_notif = pd.read_csv(input_notif, sep=';')
        
        print("Files loaded successfully.")

        # 3. Add Prefixes
        df_ui['Variable Name'] = 'ui:' + df_ui['Variable Name'].astype(str)
        df_notif['Variable Name'] = 'notifications:' + df_notif['Variable Name'].astype(str)

        # 4. Merge Files
        df_merged = pd.concat([df_ui, df_notif], ignore_index=True)

        # 5. Fix malformed variables
        print("Fixing malformed variables (replacing '{text]' with '{text}')...")
        df_merged['Translation'] = df_merged['Translation'].astype(str).str.replace(
            r'\{([^\{\}]+)\]', r'{\1}', regex=True
        )

        # 6. Add Metadata Columns
        df_merged['version'] = ''
        df_merged['dropdown_name'] = ''
        df_merged['language'] = ''

        if not df_merged.empty:
            df_merged.at[0, 'version'] = version_input
            df_merged.at[0, 'dropdown_name'] = 'English (US)'
            df_merged.at[0, 'language'] = 'en-US'

        # 7. Save Master en.csv
        df_merged.to_csv(output_master, index=False, sep=';')
        print(f"Successfully created master file: {output_master}")

        # 8. Multiply into other languages and update metadata
        print("Creating and updating language-specific files...")
        
        # Define the metadata for each language
        lang_metadata = {
            'en': {'dropdown': 'English (United Kingdom)', 'code': 'en-GB'},
            'fr': {'dropdown': 'French (France)', 'code': 'fr-FR'},
            'de': {'dropdown': 'German (Germany)', 'code': 'de-DE'},
            'es': {'dropdown': 'Spanish (Spain)', 'code': 'es-ES'},
            'it': {'dropdown': 'Italian (Italy)', 'code': 'it-IT'},
            'pt': {'dropdown': 'Portuguese (Portugal)', 'code': 'pt-PT'},
            'nl': {'dropdown': 'Dutch (Netherlands)', 'code': 'nl-NL'},
            'sv': {'dropdown': 'Swedish (Sweden)', 'code': 'sv-SE'},
            'da': {'dropdown': 'Danish (Denmark)', 'code': 'da-DK'},
            'no': {'dropdown': 'Norwegian (Norway)', 'code': 'nb-NO'},
            'fi': {'dropdown': 'Finnish (Finland)', 'code': 'fi-FI'},
            'pl': {'dropdown': 'Polish (Poland)', 'code': 'pl-PL'},
            'cs': {'dropdown': 'Czech (Czech Republic)', 'code': 'cs-CZ'},
            'sk': {'dropdown': 'Slovak (Slovakia)', 'code': 'sk-SK'},
            'hu': {'dropdown': 'Hungarian (Hungary)', 'code': 'hu-HU'},
            'ro': {'dropdown': 'Romanian (Romania)', 'code': 'ro-RO'},
            'bg': {'dropdown': 'Bulgarian (Bulgaria)', 'code': 'bg-BG'},
            'hr': {'dropdown': 'Croatian (Croatia)', 'code': 'hr-HR'},
            'sl': {'dropdown': 'Slovenian (Slovenia)', 'code': 'sl-SI'},
            'sr': {'dropdown': 'Serbian (Serbia)', 'code': 'sr-RS'},
            'et': {'dropdown': 'Estonian (Estonia)', 'code': 'et-EE'},
            'lv': {'dropdown': 'Latvian (Latvia)', 'code': 'lv-LV'},
            'lt': {'dropdown': 'Lithuanian (Lithuania)', 'code': 'lt-LT'},
            'el': {'dropdown': 'Greek (Greece)', 'code': 'el-GR'},
            'ru': {'dropdown': 'Russian (Russia)', 'code': 'ru-RU'},
            'zh': {'dropdown': 'Chinese (Simplified, China)', 'code': 'zh-CN'},
            'ja': {'dropdown': 'Japanese (Japan)', 'code': 'ja-JP'},
            'ko': {'dropdown': 'Korean (South Korea)', 'code': 'ko-KR'},
            'hi': {'dropdown': 'Hindi (India)', 'code': 'hi-IN'},
            'th': {'dropdown': 'Thai (Thailand)', 'code': 'th-TH'},
            'vi': {'dropdown': 'Vietnamese (Vietnam)', 'code': 'vi-VN'},
            'id': {'dropdown': 'Indonesian (Indonesia)', 'code': 'id-ID'},
            'ar': {'dropdown': 'Arabic (Saudi Arabia)', 'code': 'ar-SA'},
            'he': {'dropdown': 'Hebrew (Israel)', 'code': 'he-IL'}
        }

        # Generate ALL target language files except English
        languages_to_multiply = [
            lang for lang in lang_metadata.keys()
            if lang != 'en'
        ]

        for lang in languages_to_multiply:
            filename = f"{lang}.csv"
            
            # Get the metadata for the current language
            metadata = lang_metadata.get(lang)
            
            if metadata and not df_merged.empty:
                # Create a fresh copy of the master dataframe
                df_lang = df_merged.copy()
                
                # Update the metadata in the first row for this language
                df_lang.at[0, 'dropdown_name'] = metadata['dropdown']
                df_lang.at[0, 'language'] = metadata['code']
                
                # Save the new language-specific CSV
                df_lang.to_csv(filename, index=False, sep=';')
                print(f"Successfully created and updated: {filename}")
            else:
                # Fallback to just copying if metadata is not defined
                shutil.copyfile(output_master, filename)
                print(f"Created replica (metadata not updated): {filename}")

        print("\nProcess complete.")

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Please ensure 'ui_texts_en.csv' and 'notifications_en-US.csv' are in the same directory as this script.")
    except KeyError as e:
        print(f"\nAn error occurred: A required column {e} was not found.")
        print("This often happens if the input file's delimiter (separator) is wrong.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()