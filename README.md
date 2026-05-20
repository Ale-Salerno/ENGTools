# ENGTools

![CI](https://github.com/Ale-Salerno/ENGTools/actions/workflows/ci.yml/badge.svg)

**Current version:** ENGTools 0.2

## Prerequisites

### Core environment
- Windows workstation
- VPN access if you are outside the office
- Java 21+
- `config.toml` in the repository root is provided with default values (paths for Okapi, ENG root and 7-Zip)
- Edit `config.toml` before first run so it matches your local machine/network mapping
- Okapi installed in the path configured in `config.toml` (`paths.okapi`)
- `eng.bat` available in the Okapi path configured in `config.toml`
- GLAP installed in `C:\Program Files\Analysis Package`
- 7-Zip installed in the path configured in `config.toml` (`paths.sevenzip`)
- Access to the ENG root path configured in `config.toml` (`paths.eng_root`)

### Python
Install the modules in `Dependencies/python/requirements.txt`, or at minimum:
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

## Python CLI

ENGTools includes a `click`-based CLI that mirrors the top-level menu of `ENGTools.bat`.

### Installation

```bash
pip install -e .
```

### Usage

```bash
engtools --help
engtools sfp --help
engtools sfp standard --sl en --tl de
engtools tm xlf-to-tmx --sl en --tl de
engtools translation translation-2
engtools alignment id-based
engtools office update-toc
engtools tools flatten
```

Available command groups:

| Group | Subcommands |
|---|---|
| `sfp` | `standard`, `custom`, `xliff`, `proofreading`, `pretranslate`, `daimler`, `epiroc`, `axis`, `beurer`, `edwards`, `confirm-sdlxliff` |
| `tm` | `xlf-to-tmx`, `xlf-to-table`, `cleanup`, `excel-to-tmx`, `resegment`, `split-multilingual` |
| `translation` | `standard`, `translation-2` |
| `alignment` | `id-based` |
| `office` | `update-toc`, `unhide-docx`, `hide-color`, `anonymize`, `unhide-xlsx`, `split-xlsx` |
| `tools` | `flatten`, `unflatten`, `distribute`, `json-paths`, `xpath`, `remove-locales`, `regin`, `maxlen`, `delete-column-csv`, `webcrawl`, `pdf-comments`, `append-folder`, `srt-vtt` |

> **Note:** All subcommands are currently stubs — they print a "not yet implemented" message and exit cleanly. Full implementations will replace `ENGTools.bat` workflows progressively.

## CI

GitHub Actions runs automatically on every push and pull request. The workflow (`.github/workflows/ci.yml`) includes three jobs:

- **lint** – checks the syntax of all Python scripts in `Dependencies/python/` using `python -m py_compile`
- **dependencies** – installs all packages from `Dependencies/python/requirements.txt` and verifies no install errors occur
- **tests** – runs `pytest --collect-only` so it succeeds even when no test files exist yet

## Repository Layout
- `.github/workflows/ci.yml` - GitHub Actions CI workflow
- `ENGTools.bat` - main menu entry point
- `Dependencies/bats` - helper batch launchers and target-file creation scripts
- `Dependencies/python` - feature scripts used by menu options
- `Dependencies/mappings` - Edwards/Leybold/Atlas mapping workbooks
- `Dependencies/macros` - Excel helper macros
- `Dependencies/fonts` - Scholly QA font assets
- `Parsers/okapi` - Okapi `.fprm` filters
- `Pipelines` - Okapi/Rainbow pipelines
- `Segmentation/okapi` - segmentation rules

## Notes and Known Constraints
- Daimler, Epiroc, AXIS Type 4, and Beurer are specialized workflows with hardcoded language assumptions in the batch launcher; verify those assumptions before using them on new content.
- ID-based alignment still depends on Rainbow/GLAP and writes intermediate output to `C:\TMX`; confirm that path is writable in your environment.
- The Scholly scripts and batch files exist in the repository but are not wired into the main menu yet. Treat them as manual/experimental utilities until a human review confirms the intended UX.
- A few utility scripts remain manual-only or legacy (`Atlas-OLD.py`, `prep_qa_merge_json.py`, `unhide_rename_word.py`).
