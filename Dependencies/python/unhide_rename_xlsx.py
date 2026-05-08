import os
import sys
import win32com.client as win32  # Alias for COM automation

def sanitize_file_name(file_path):
    """
    Removes unwanted markers like '_UNHIDE', '(hidden)', etc. from the filename,
    renames the file if necessary, and returns the new (or original) path.
    """
    directory, file_name = os.path.split(file_path)
    markers = ["_UNHIDE", "_unhide", "_hidden", "_HIDDEN",
               "(unhide)", "(UNHIDE)", "(hidden)", "(HIDDEN)"]
    sanitized_name = file_name
    for marker in markers:
        sanitized_name = sanitized_name.replace(marker, "")
    sanitized_name = sanitized_name.strip()
    new_path = os.path.join(directory, sanitized_name)
    if new_path != file_path:
        try:
            os.rename(file_path, new_path)
            print(f"[OK] Renamed '{file_path}' -> '{new_path}'")
            return new_path
        except OSError as e:
            print(f"[ERROR] Could not rename '{file_path}' -> '{new_path}': {e}")
            return file_path
    else:
        return file_path

def col_letter(col_index):
    """
    Converts a 1-based column index to an Excel column letter (e.g., 1 -> 'A').
    """
    letters = ""
    while col_index > 0:
        remainder = (col_index - 1) % 26
        letters = chr(65 + remainder) + letters
        col_index = (col_index - 1) // 26
    return letters

def unhide_excel(file_path):
    """
    Uses Excel COM automation to open an .xls or .xlsx file,
    unhide all rows and columns in the used range, then save and close the workbook.
    """
    excel_app = win32.Dispatch("Excel.Application")
    excel_app.Visible = False
    try:
        wb = excel_app.Workbooks.Open(file_path, ReadOnly=False)
    except Exception as e:
        print(f"[ERROR] Could not open '{file_path}' in Excel: {e}")
        excel_app.Quit()
        return

    try:
        for sheet in wb.Worksheets:
            used_range = sheet.UsedRange
            used_row_count = used_range.Rows.Count
            used_col_count = used_range.Columns.Count

            row_range_str = f"1:{used_row_count}"
            col_range_str = f"A:{col_letter(used_col_count)}"

            try:
                sheet.Range(row_range_str).EntireRow.Hidden = False
            except Exception as e:
                print(f"[WARN] Could not unhide rows in '{sheet.Name}': {e}")

            try:
                sheet.Range(col_range_str).EntireColumn.Hidden = False
            except Exception as e:
                print(f"[WARN] Could not unhide columns in '{sheet.Name}': {e}")

        wb.Save()
        print(f"[OK] Unhidden rows/columns in '{file_path}'")
    except Exception as e:
        print(f"[ERROR] Could not unhide rows/columns in '{file_path}': {e}")
    finally:
        wb.Close(False)
        excel_app.Quit()

def main():
    """
    Recursively processes all .xls and .xlsx files in the current directory:
      1) Renames files to remove unwanted markers.
      2) Unhides rows and columns using Excel COM automation.
    """
    current_dir = os.getcwd()
    valid_exts = {".xls", ".xlsx"}
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            base, ext = os.path.splitext(file)
            if ext.lower() in valid_exts:
                original_path = os.path.join(root, file)
                sanitized_path = sanitize_file_name(original_path)
                unhide_excel(sanitized_path)

if __name__ == "__main__":
    main()
