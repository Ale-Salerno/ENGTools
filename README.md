# ENGTools

**CURRENT VERSION:** ENGTools 0.2

## Prerequisites

* VPN (if you're out of the office)
* Java 21+
* Okapi (stored in `C:\Software\Okapi`)
* Python 3.x
* Python modules (install with `pip install [module_name]`):
    * `pandas`
    * `openpyxl`
    * `xlrd`
    * `xlwt`
    * `pywin32`
    * `python-docx`
    * `langdetect`
    * `regex`
* `C:\Software\Okapi` added to your Environment Variables PATH
* `eng.bat` (in `C:\Software\Okapi`)
* GLAP installed in its default folder (`C:\Program Files\Analysis Package`)

## Downloads

* Okapi (latest)
* `eng.bat`: `\\languagewire.cph\Global\Engineering\LW\Engineers\Tools\ENGTools\Dependencies\bats\eng.bat`
* GLALP: `\\languagewire.cph\Global\Engineering\LW\Engineers\Tools\GLALP.zip`

## Tasks Included

* **Source File Preparation:**
    * **Okapi – Standard SFP:** Prepares source files using Okapi's default filter and segmentation.
    * **Okapi – Custom SFP:** Uses a custom parser for specialized source file preparation.
    * **Okapi – SFP for Proofreading:** Prepares files for proofreading.
    * **Okapi – Pretranslation:** Uses Okapi to pretranslate files.
    * **Epiroc TXT:** Handles Epiroc TXT files.
* **TM Management:**
    * **XLF and Flavours to TMX:** Converts XLF files to TMX format.
    * **XLF and Flavours to Bilingual Table:** Converts XLF files to a bilingual table.
    * **Clean Up TMX:** Cleans up TMX files.
    * **Excel to TMX (Bilingual/Multilingual):** Converts Excel files to TMX.
    * **Resegment Paragraph-Based TMX:** Reprocesses paragraph-based TMX files.
* **Translation 2.0:** Renames and transfers translations between XLF files, applies exact-match filters, and escapes special characters.
* **Alignment:**
    * **ID-Based Alignment:** Aligns source and target files based on IDs.
* **Microsoft Office Tools:**
    * **MS Word:**
        * Batch Update TOCs
        * Batch Unhide and Rename `.doc/.docx`
        * Batch Hide Based on Color Text
    * **MS Excel:**
        * Batch Unhide and Rename `.xls/.xlsx`
        * MS Office Tools: Split/Merge multilingual .xlsx files
* **Additional Tools:**
    * **Flatten/Unflatten Folder Structure:**
        * Flatten Folder Structure
        * Unflatten Folder Structure
    * **Distribute Files by Target Language Code:** Organizes files by language code.
    * **Extract JSON Paths:** Extracts paths from JSON files.
    * **XPath Generator:** Generates XPath paths from XML files.
    * **Remove platform locales:** Removes platform locales.
    * **Regin .en Files:**
        * `.en` Files to Multilingual Excel
        * Multilingual Excel to Individual `.en` Files