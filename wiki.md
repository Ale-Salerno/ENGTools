**CURRENT VERSION:(% style="color:#c0392b" %) ENGTools 0.2(%%)**


**Prerequisites:**

* **VPN **if you're out of the office
* Java 21+
* A copy of Okapi stored in **C:\Software\Okapi**
* Python 3.x
* Python modules (to install python modules:** pip install [name of module]** in cmd):
** pandas
** openpyxl
** xlrd
** xlwt
** pywin32
** python-docx
** langdetect
** regex
* C:\Software\Okapi added to your Environment Variables **PATH**
* A copy of **eng.bat** in C:\Software\Okapi
* GLAP installed in its default folder (**C:\Program Files\Analysis Package**)

**Downloads:**

* [[Okapi latest>>https://okapiframework.org/binaries/main/1.47.0/]]
* ~\~\languagewire.cph\Global\Engineering\LW\Engineers\Tools\ENGTools\Dependencies\bats\**eng.bat**
* ~\~\languagewire.cph\Global\Engineering\LW\Engineers\Tools\**GLALP.zip**

**Changelog:**

* (((
(% style="color:#c0392b" %)**ENGTools v0.2 - Enhanced Stability, Maintainability, and Functionality**

**Core Improvements:**
)))
* **Version Control & Project Structure:**
** Implemented Git and GitHub for robust version control and reversibility [[vicparramain/ENGTools>>url:https://github.com/vicparramain/ENGTools]]
** Established a structured Visual Studio project for improved traceability.
* **Comprehensive Code Refactoring:**
** Simplified code, enhanced menus, and added extensive comments for improved readability and maintainability.
** Standardized terminal logs with clear tags (e.g., [WARN], [ERROR]).
** Established a consistent folder structure.
* **Enhanced Error Handling:**
** Implemented comprehensive error handling throughout, including error-level checks in batch files and post-execution checks for critical operations.
* **Improved User Feedback:**
** Enhanced console output with clear, user-friendly messages for progress and status updates.
* **Documentation:**
** Created/updated README.md, CHANGELOG.md, and requirements.txt for comprehensive project documentation.
** Improved in code documentation.
* (((
**Feature Updates:**
)))
* **Translation 2.0:**
** Automated language detection and file renaming based on language tags (e.g., de-DE, it-IT, es-ES).
** Implemented a script to automatically exclude 100% matches from target translation files.
* **TFC Script Enhancements:**
** Added a script to automatically remove platform locales from target .xlf files.
* (((
**New Features:**
)))
* **Tool: Remove Platform Locales:**
** Automates the removal of platform locales from target .xlf files.
* **MS Office Tools: Hide by Colors in Word Files:**
** Enables selective hiding of text in .docx files based on font and highlight colors.
** Generates an HTML report with color indices for easy selection.
** Provides filtering options to hide selected or non-selected colors.
* (((
**MS Office Tools: Split/Merge multilingual .xlsx files:**

* Enables selective hiding of text in .docx files based on font and highlight colors.
* Generates an HTML report with color indices for easy selection.
* Provides filtering options to hide selected or non-selected colors.
)))

* (% style="color:#c0392b" %)**ENGTools v0.1**
* Initial release.

**Tasks included:**

* (((
**Source File Preparation**

* **Okapi – Standard SFP**
//Prepares source files using Okapi’s default filter and segmentation rules. It creates the necessary folder structure, copies base files, and generates XLF files, then applies pseudotranslation and packaging.//
* **Okapi – Custom SFP**
*Similar to the standard process but uses a custom parser (prompting you to supply a //.fprm file) for more specialized source file preparation. It generates XLF files with custom rules and then performs pseudotranslation.//
* **Okapi – SFP for Proofreading**
//Prepares files specifically for the proofreading process by generating XLF files and setting a “translated” state so that proofreaders can work on them directly.//
* **Okapi – Pretranslation**
//Uses Okapi’s tools to pretranslate files. It processes files (except batch and TMX files) by applying existing translations from TMX, easing the translator’s workload.//
* **Epiroc TXT**
//Handles Epiroc TXT files by extracting and flattening a ZIP package, restructuring the folders, and then creating XLF files using a dedicated Epiroc parser.//
)))
* (((
**TM Management**

* **XLF and Flavours to TMX**
//Converts XLF files (with flavour adjustments) into TMX format. It uses a custom filter and then cleans up properties with a Python script.//
* **XLF and Flavours to Bilingual Table**
//Converts XLF files into a bilingual table format, which can be useful for review or further processing.//
* **Clean Up TMX**
//Runs a cleanup script to remove unnecessary properties and ensure the TMX file is formatted correctly.//
* **Excel to TMX (Bilingual/Multilingual)**
//Converts Excel files containing translation memories into TMX format, supporting both bilingual and multilingual setups.//
* **Resegment Paragraph-Based TMX**
//Reprocesses paragraph-based TMX files by applying sentence segmentation and then regenerating the TMX file, making it more granular for translation memory use.//
)))
* (((
**Translation 2.0**

* //Renames and transfers translations between XLF files, applies exact-match filters to keep 100% matches, and escapes special characters to ensure consistency in the translated output.//
)))
* (((
**Alignment**

* **ID-Based Alignment**
//Aligns source and target files based on unique IDs. The process allows for optional segmentation by sentence and handles file preparation by moving source/target files to specific folders and applying the alignment tool.//
)))
* (((
**Microsoft Office Tools**

* **MS Word**
** **Batch Update TOCs**
//Updates Table of Contents in .doc or .docx files automatically.//
** **Batch Unhide and Rename .doc/.docx**
//Unhides content in Word files and renames them as needed.//
** **Batch Hide Based on Color Text**
//Hides text in Word files based on its color, which can be useful for managing visible content.//
* **MS Excel**
** **Batch Unhide and Rename .xls/.xlsx**
//Processes Excel files to unhide hidden cells and rename the files accordingly.//
** (((
**MS Office Tools: Split/Merge multilingual .xlsx files:**
//Enables selective hiding of text in .docx files based on font and highlight colors. Generates an HTML report with color indices for easy selection. Provides filtering options to hide selected or non-selected colors.//
)))
)))
* (((
**Additional Tools**

* **Flatten/Unflatten Folder Structure**
** **Flatten Folder Structure**
//Converts a nested folder structure into a single-level structure, simplifying file management.//
** **Unflatten Folder Structure**
//Restores the original folder hierarchy from a flattened structure.//
* **Distribute Files by Target Language Code**
//Organizes files into separate folders based on their target language code for easier management and processing.//
* **Extract JSON Paths**
//Extracts paths from JSON files using a dedicated command-line tool.//
* **XPath Generator**
//Generates XPath paths from XML files, assisting in data extraction and analysis.//
* **Remove platform locales**
//Removes platform locales.//
* **Regin .en Files**
** **.en Files to Multilingual Excel**
//Converts multiple .en files into a single multilingual Excel sheet for consolidated review and editing.//
** **Multilingual Excel to Individual .en Files**
//Splits a multilingual Excel file back into separate .en files, restoring the individual file format for further processing.//
