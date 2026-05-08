#!/usr/bin/env python3
"""
Revert split-out Excel columns back into copies of the originals,
using metadata_conversion.json to know where each slice belongs,
and align data rows to start at row 4 (headers at row 1).

Prerequisites:
    pip install pywin32

Usage:
    Place this script in the folder containing:
      • metadata_conversion.json
      • the original workbooks (e.g. Foo.xlsx or Foo.xlsm)
      • all the individual “basename_header.xlsx” slices
    Then:
      python revert_columns.py
"""

import os
import json
import shutil
import win32com.client as win32

def revert_columns():
    folder = os.getcwd()
    meta_path = os.path.join(folder, "metadata_conversion.json")
    if not os.path.exists(meta_path):
        print("ERROR: metadata_conversion.json not found in", folder)
        return

    # Load the metadata JSON
    with open(meta_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # Launch Excel silently
    excel = win32.Dispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False

    # Process each original workbook entry
    for baseName, info in metadata.items():
        # --- find the original file (any .xls/.xlsx/.xlsm matching baseName) ---
        candidates = [
            f for f in os.listdir(folder)
            if os.path.splitext(f)[0] == baseName
            and f.lower().endswith((".xls", ".xlsx", ".xlsm"))
        ]
        if not candidates:
            print(f"  • Skipping '{baseName}': no original workbook found.")
            continue

        orig_file = candidates[0]
        orig_path = os.path.join(folder, orig_file)
        ext = os.path.splitext(orig_file)[1]
        compiled_file = f"{baseName}_compiled{ext}"
        compiled_path = os.path.join(folder, compiled_file)

        # --- copy original → compiled ---
        try:
            shutil.copy2(orig_path, compiled_path)
        except Exception as e:
            print(f"  • Failed to copy '{orig_file}' → '{compiled_file}': {e}")
            continue

        print(f"Reverting columns into '{compiled_file}'...")
        wb_orig = excel.Workbooks.Open(compiled_path)
        ws_orig = wb_orig.Worksheets(1)

        # for each slice of this workbook...
        for col_meta in info.get("columns", []):
            slice_file = col_meta["file"]
            slice_path = os.path.join(folder, slice_file)
            if not os.path.exists(slice_path):
                print(f"    – Missing slice file: {slice_file}  (skipping)")
                continue

            wb_slice = excel.Workbooks.Open(slice_path)
            ws_slice = wb_slice.Worksheets(1)

            # find last used row in column A of the slice
            last_row = ws_slice.Cells(ws_slice.Rows.Count, 1) \
                                  .End(win32.constants.xlUp).Row

            # 1) copy header (row 1 of slice) → row 1 of compiled
            ws_slice.Cells(1, 1).Copy(
                Destination=ws_orig.Cells(1, col_meta["colIndex"])
            )

            # 2) copy data (rows 2..last_row in slice) → rows 4.. in compiled
            src = ws_slice.Range(
                ws_slice.Cells(2, 1),
                ws_slice.Cells(last_row, 1)
            )
            dest = ws_orig.Cells(4, col_meta["colIndex"])
            src.Copy(Destination=dest)

            wb_slice.Close(SaveChanges=False)

        # save & close the compiled workbook
        wb_orig.Save()
        wb_orig.Close(SaveChanges=False)
        print(f"  ✓ Done '{compiled_file}'")

    excel.Quit()
    print("All done! 🎉")


if __name__ == "__main__":
    revert_columns()
