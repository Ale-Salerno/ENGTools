# ENGTools Wiki Snapshot

## Version
**ENGTools 0.2**

## Prerequisites
### Core
- Windows workstation
- VPN if you are out of the office
- Java 21+
- Okapi in `C:\Software\Okapi`
- `C:\Software\Okapi` on `PATH`
- `eng.bat` copied to `C:\Software\Okapi`
- GLAP in `C:\Program Files\Analysis Package`
- 7-Zip in `C:\Program Files\7-Zip`
- Access to the `W:` drive used by `eng.bat`

### Python modules
Install the packages from `Dependencies/python/requirements.txt`.

### Office automation
Word/Excel-based tools require Microsoft Office installed locally (COM automation via `pywin32`). This includes:
- Batch update TOCs, Batch unhide/rename Word files, Anonymize track changes (require Word)
- Batch unhide/rename Excel files, Split/Merge multilingual `.xlsx` (require Excel)
- **Beurer SFP and TFC** — split and merge steps both require Excel COM automation

## Downloads
- Okapi latest build
- `\\languagewire.cph\Global\Engineering\LW\Engineers\Tools\ENGTools\Dependencies\bats\eng.bat`
- `\\languagewire.cph\Global\Engineering\LW\Engineers\Tools\GLAP.zip`

## Tasks Included
### Source File Preparation
- Okapi - Standard SFP
- Okapi - Custom SFP
- Okapi - XLIFF SFP
- Okapi - Source File Preparation for Proofreading
- Okapi - Pretranslation
- Daimler Multilingual Proofreading
- Epiroc TXT
- AXIS Type 4
- Beurer
- Edwards / Leybold / Atlas
- Confirm Segments SDLXLIFF

### TM Management
- XLF and flavours to TMX
- XLF and flavours to bilingual table
- Clean up TMX
- Excel to TMX (bilingual/multilingual)
- Resegment paragraph-based TMX
- Split multilingual TMX

### Translation
- Translation 2.0
- Translation

### Alignment
- ID-based alignment

### Microsoft Office Tools
- Batch update TOCs
- Batch unhide and rename `.doc/.docx`
- Batch hide based on color text in Word files
- Anonymize track changes
- Batch unhide and rename `.xls/.xlsx`
- Split multilingual `.xlsx` files

### Additional Tools
- Flatten / unflatten folder structure
- Distribute files by target language code
- Extract JSON paths
- XPath generator
- Remove platform locales
- Regin `.en` file conversion
- Static Maxlen Setter
- Batch Delete Column CSV
- Web-crawling
- Extract PDF comments to Excel and CSV
- Append folder name to files
- SRT to/from VTT

## Operational Notes
- Translation 2.0 now runs the exact-match preservation step again.
- The Split/Merge multilingual `.xlsx` workflow is an Excel split/merge utility (splits a multilingual Excel into per-language bilingual files and merges them back), not a Word color-hiding tool.
- Daimler, Epiroc, AXIS Type 4, and Beurer remain specialized flows with hardcoded language assumptions that should be reviewed before wider reuse.
- Scholly assets are present in the repository but are still manual-only and should be reviewed by a human before being exposed in the main menu.
- Alignment still depends on `C:\TMX`, Rainbow, and GLAP behavior in the local Windows environment. The `engRootPath` variable in `ENGTools.bat` controls where the pipeline file is read from; update it if running from a local checkout instead of the W: drive deployment.

## Scripts Not Exposed in the Main Menu
The following Python scripts exist in `Dependencies/python/` but are not directly accessible via the ENGTools main menu:

| Script | Status |
|---|---|
| `beurer_merge.py` | Called by `TFC_beurer.bat` during the Beurer target file creation step |
| `daimler_merge_multilingual_excel.py` | Called by `TFC_daimler.bat` during the Daimler target file creation step |
| `prep_qa_merge_json.py` | Orphaned — no menu entry or bat references it |
| `Atlas-OLD.py` | Superseded by `Atlas.py`; kept for reference only |
| `unhide_rename_word.py` | Orphaned — functionality covered by `unhide_rename_docx.py` |
| `scholly_csv2json.py` | Scholly suite — manual-only, not yet wired into the menu |
| `scholly_json2tmx.py` | Scholly suite — manual-only |
| `scholly_merge.py` | Scholly suite — manual-only |
| `scholly_prep.py` | Scholly suite — manual-only |
| `scholly_qa.py` | Scholly suite — manual-only |
