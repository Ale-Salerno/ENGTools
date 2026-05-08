import os
import sys
import win32com.client as win32

def update_toc_in_word_files(folder_path):
    """
    Updates all Tables of Contents in both .doc and .docx files within 'folder_path'.

    Performance optimizations:
      - Disables screen updating and display alerts
      - Disables real-time spell/grammar checks
      - Processes all files in a single Word session
    """

    # Launch Word as a background process
    word_app = win32.Dispatch("Word.Application")
    word_app.Visible = False

    # Speed optimizations
    word_app.ScreenUpdating = False
    word_app.DisplayAlerts = 0  # 0 = wdAlertsNone
    try:
        word_app.Options.CheckSpellingAsYouType = False
        word_app.Options.CheckGrammarAsYouType = False
        word_app.Options.CheckSpellingOnSave = False
        word_app.Options.CheckGrammarOnSave = False
    except Exception as e:
        print(f"[WARN] Could not disable certain Word options: {e}")

    file_count = 0
    processed_count = 0

    try:
        # Iterate over files in the folder
        for file_name in os.listdir(folder_path):
            lower_name = file_name.lower()
            # Check for .doc or .docx and ignore temp (~$) files
            if (lower_name.endswith(".doc") or lower_name.endswith(".docx")) and not file_name.startswith("~$"):
                file_count += 1
                file_path = os.path.join(folder_path, file_name)
                print(f"Processing: {file_path}")

                # Attempt to open the Word document
                try:
                    doc = word_app.Documents.Open(file_path, ReadOnly=False)
                except Exception as e:
                    print(f"[ERROR] Could not open '{file_path}': {e}")
                    continue

                try:
                    # Update all TOCs in the doc
                    for toc in doc.TablesOfContents:
                        toc.Update()
                    # Save changes
                    doc.Save()
                    processed_count += 1
                    print(f"[OK] Updated TOC in '{file_name}'")
                except Exception as e:
                    print(f"[ERROR] Updating TOC in '{file_name}': {e}")
                finally:
                    doc.Close(SaveChanges=False)

    except Exception as e:
        print(f"[ERROR] Error iterating folder '{folder_path}': {e}")
    finally:
        # Restore application settings and quit Word
        word_app.ScreenUpdating = True
        word_app.Quit()
        print(f"Word application closed.")
        print(f"Found {file_count} file(s) (.doc/.docx), updated {processed_count}.")

def main():
    """
    Runs the update of TOCs in the current working directory by default.
    """
    folder_path = os.getcwd()
    print(f"Running TOC update in folder: {folder_path}")

    if not os.path.isdir(folder_path):
        print("[ERROR] Invalid folder path. Exiting.")
        sys.exit(1)

    update_toc_in_word_files(folder_path)

if __name__ == "__main__":
    main()
