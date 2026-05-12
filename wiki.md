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
Install the packages from `/home/runner/work/ENGTools/ENGTools/Dependencies/python/requirements.txt`.

### Office automation
Word/Excel-based tools require Microsoft Office installed locally.

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
- The Split/Merge multilingual `.xlsx` workflow is an Excel split/merge utility, not a Word color-hiding tool.
- Daimler, Epiroc, AXIS Type 4, and Beurer remain specialized flows with hardcoded language assumptions that should be reviewed before wider reuse.
- Scholly assets are present in the repository but are still manual-only and should be reviewed by a human before being exposed in the main menu.
- Alignment still depends on `C:\TMX`, Rainbow, and GLAP behavior in the local Windows environment.
