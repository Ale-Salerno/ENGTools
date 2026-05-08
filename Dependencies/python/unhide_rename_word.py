import os
import sys
import win32com.client as win32

def unhide_text_in_word(file_path):
   
    try:
        word_app = win32.Dispatch("Word.Application")
        word_app.Visible = False
       
        doc = word_app.Documents.Open(file_path, ReadOnly=False)
       
        for story in doc.StoryRanges:
            current_range = story
            while current_range is not None:
                try:
                   
                    current_range.Font.Hidden = False
                except Exception as inner_e:
                    print(f"[WARN] Could not unhide a story range in '{file_path}': {inner_e}")
                current_range = current_range.NextStoryRange
        
        doc.Save()
        doc.Close()
        word_app.Quit()
        print(f"[OK] Unhidden text in '{file_path}'")
    except Exception as e:
        print(f"[ERROR] Could not unhide text in '{file_path}': {e}")

def sanitize_file_name(file_path):
  
    directory, file_name = os.path.split(file_path)
    markers = ["_UNHIDE", "_unhide", "_hidden", "_HIDDEN",
               "(unhide)", "(UNHIDE)", "(hidden)", "(HIDDEN)"]
    sanitized_name = file_name
    for marker in markers:
        sanitized_name = sanitized_name.replace(marker, "")
    sanitized_name = sanitized_name.strip()
    sanitized_path = os.path.join(directory, sanitized_name)
    if sanitized_path != file_path:
        try:
            os.rename(file_path, sanitized_path)
            print(f"[OK] Renamed '{file_path}' -> '{sanitized_path}'")
        except OSError as e:
            print(f"[ERROR] Could not rename '{file_path}' -> '{sanitized_path}': {e}")
            return file_path
    return sanitized_path

def main():
   
    current_dir = os.getcwd()
    doc_extensions = {".doc", ".docx"}
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext.lower() in doc_extensions:
                original_path = os.path.join(root, file)
                sanitized_path = sanitize_file_name(original_path)
                unhide_text_in_word(sanitized_path)

if __name__ == "__main__":
    main()
