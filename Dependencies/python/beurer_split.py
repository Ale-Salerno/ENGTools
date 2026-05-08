#!/usr/bin/env python3
"""
Split Excel columns into individual workbooks, skipping empty ones,
outputting slices in `split_files/` and the originals + metadata in `original_metadata/`.

Prerequisites:
    pip install pywin32

Usage:
    Place this script in the folder containing your .xls/.xlsx/.xlsm files.
    Then:
      python split.py
"""

import os
import json
import sys
import shutil
from win32com.client import Dispatch, constants

def batch_process(folder_path):
    # prepare output folders
    split_dir = os.path.join(folder_path, "split_files")
    meta_dir  = os.path.join(folder_path, "original_metadata")
    os.makedirs(split_dir, exist_ok=True)
    os.makedirs(meta_dir,  exist_ok=True)

    # launch Excel
    excel = Dispatch("Excel.Application")
    excel.ScreenUpdating = False
    excel.EnableEvents = False
    try:
        excel.Calculation = constants.xlCalculationManual
    except Exception:
        try:
            excel.Calculation = -4135
        except:
            pass
    excel.DisplayAlerts = False

    meta = {}

    for fname in os.listdir(folder_path):
        if not fname.lower().endswith((".xls", ".xlsx", ".xlsm")):
            continue
        if fname == os.path.basename(sys.argv[0]):
            continue

        full_path = os.path.join(folder_path, fname)
        base_name = os.path.splitext(fname)[0]

        # copy original into metadata folder
        shutil.copy2(full_path, os.path.join(meta_dir, fname))

        # open workbook
        wb = excel.Workbooks.Open(full_path)
        ws = wb.ActiveSheet

        # 1) fill blanks from column C into D:…
        last_row = ws.Cells(ws.Rows.Count, 3).End(constants.xlUp).Row
        last_col = ws.Cells(1, ws.Columns.Count).End(constants.xlToLeft).Column

        for r in range(4, last_row + 1):
            if ws.Cells(r, 3).Value not in (None, ""):
                try:
                    blanks = ws.Range(ws.Cells(r, 4), ws.Cells(r, last_col)) \
                               .SpecialCells(constants.xlCellTypeBlanks)
                    ws.Range(ws.Cells(r, 3), ws.Cells(r, 3)).Copy(Destination=blanks)
                except:
                    pass

        meta[base_name] = {"columns": []}

        # 2) split each column D→last_col
        for c in range(4, last_col + 1):
            header = ws.Cells(1, c).Value
            if header is None or str(header).strip() == "":
                break

            new_wb = excel.Workbooks.Add(constants.xlWBATWorksheet)
            new_ws = new_wb.Sheets(1)

            # copy header and data
            ws.Cells(1, c).Copy(new_ws.Cells(1, 1))
            ws.Range(ws.Cells(4, c), ws.Cells(last_row, c)) \
              .Copy(new_ws.Cells(2, 1))
            new_ws.Columns(1).ColumnWidth = ws.Columns(c).ColumnWidth

            # hide header row (row 1)
            new_ws.Rows(1).Hidden = True

            # hide "no" rows
            dest_last = new_ws.Cells(new_ws.Rows.Count, 1).End(constants.xlUp).Row
            for r in range(2, dest_last + 1):
                if str(new_ws.Cells(r, 1).Value).lower() == "no":
                    new_ws.Rows(r).Hidden = True

            # only save if data remains (rows 2..dest_last)
            has_data = any(not new_ws.Rows(r).Hidden for r in range(2, dest_last + 1))
            if has_data:
                # prepend locale/header to filename
                slice_name = f"{header}_{base_name}.xlsx"
                new_path = os.path.join(split_dir, slice_name)
                new_wb.SaveAs(new_path, FileFormat=constants.xlOpenXMLWorkbook)
                meta[base_name]["columns"].append({
                    "header": str(header).replace('"', '\\"'),
                    "file": slice_name,
                    "colIndex": c
                })
            new_wb.Close(False)

        wb.Close(False)

    # write metadata JSON into metadata folder
    meta_path = os.path.join(meta_dir, "metadata_conversion.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    # restore Excel
    excel.DisplayAlerts = True
    try:
        excel.Calculation = constants.xlCalculationAutomatic
    except Exception:
        try:
            excel.Calculation = -4105
        except:
            pass
    excel.EnableEvents = True
    excel.ScreenUpdating = True
    excel.Quit()

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    batch_process(here)
