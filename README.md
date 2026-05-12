# ENGTools

**Current version:** ENGTools 0.2

## Prerequisites

### Core environment
- Windows workstation
- VPN access if you are outside the office
- Java 21+
- Okapi installed in `C:\Software\Okapi`
- `C:\Software\Okapi` added to `PATH`
- `eng.bat` available in `C:\Software\Okapi`
- GLAP installed in `C:\Program Files\Analysis Package`
- 7-Zip installed in `C:\Program Files\7-Zip`
- Access to the `W:` network drive used by `eng.bat`

### Python
Install the modules in `/home/runner/work/ENGTools/ENGTools/Dependencies/python/requirements.txt`, or at minimum:
- `pandas`
- `openpyxl`
- `xlrd`
- `xlwt`
- `pywin32`
- `python-docx`
- `langdetect`
- `regex`
- `lxml`
- `PyMuPDF`
- `requests`
- `beautifulsoup4`
- `PySide6`

### Office-dependent features
The Microsoft Office workflows, Beurer split/merge flow, and some rename/unhide scripts require Microsoft Word and/or Excel installed locally because they use COM automation.

## Downloads
- Okapi (latest)
- `eng.bat`: `\\languagewire.cph\Global\Engineering\LW\Engineers\Tools\ENGTools\Dependencies\bats\eng.bat`
- GLAP: `\\languagewire.cph\Global\Engineering\LW\Engineers\Tools\GLAP.zip`

## Menu Overview

### 1. Source File Preparation
- Okapi - Standard SFP
- Okapi - Custom SFP
- Okapi - XLIFF SFP
- Okapi - Source File Preparation for Proofreading
- Okapi - Pretranslation
- Daimler Multilingual Proofreading
- Epiroc TXT
- AXIS Type 4
- Beurer
- Edwards / Leybold / Atlas brand processors
- Confirm Segments SDLXLIFF

### 2. TM Management
- XLF and flavours to TMX
- XLF and flavours to bilingual table
- Clean up TMX
- Excel to TMX (bilingual/multilingual)
- Resegment paragraph-based TMX
- Split multilingual TMX

### 3. Translation
- Translation 2.0
- Translation

### 4. Alignment
- ID-based alignment

### 5. Microsoft Office Tools
- Batch update TOCs
- Batch unhide and rename `.doc/.docx`
- Batch hide based on color text in Word files
- Anonymize track changes
- Batch unhide and rename `.xls/.xlsx`
- Split/merge multilingual `.xlsx` files

### 6. Tools
- Flatten / unflatten folder structure
- Distribute files by target language code
- Extract JSON paths
- XPath generator
- Remove platform locales
- Regin `.en` files to/from multilingual Excel
- Static Maxlen Setter
- Batch Delete Column CSV
- Web-crawling
- Extract PDF comments to Excel and CSV
- Append folder name to files

### 7. File Format Conversions
- SRT to/from VTT

## Repository Layout
- `/home/runner/work/ENGTools/ENGTools/ENGTools.bat` - main menu entry point
- `/home/runner/work/ENGTools/ENGTools/Dependencies/bats` - helper batch launchers and target-file creation scripts
- `/home/runner/work/ENGTools/ENGTools/Dependencies/python` - feature scripts used by menu options
- `/home/runner/work/ENGTools/ENGTools/Dependencies/mappings` - Edwards/Leybold/Atlas mapping workbooks
- `/home/runner/work/ENGTools/ENGTools/Dependencies/macros` - Excel helper macros
- `/home/runner/work/ENGTools/ENGTools/Dependencies/fonts` - Scholly QA font assets
- `/home/runner/work/ENGTools/ENGTools/Parsers/okapi` - Okapi `.fprm` filters
- `/home/runner/work/ENGTools/ENGTools/Pipelines` - Okapi/Rainbow pipelines
- `/home/runner/work/ENGTools/ENGTools/Segmentation/okapi` - segmentation rules

## Notes and Known Constraints
- Daimler, Epiroc, AXIS Type 4, and Beurer are specialized workflows with hardcoded language assumptions in the batch launcher; verify those assumptions before using them on new content.
- ID-based alignment still depends on Rainbow/GLAP and writes intermediate output to `C:\TMX`; confirm that path is writable in your environment.
- The Scholly scripts and batch files exist in the repository but are not wired into the main menu yet. Treat them as manual/experimental utilities until a human review confirms the intended UX.
- A few utility scripts remain manual-only or legacy (`Atlas-OLD.py`, `prep_qa_merge_json.py`, `unhide_rename_word.py`).
