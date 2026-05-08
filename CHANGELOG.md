# ENGTools Changelog

* **v0.2 - Enhanced Stability, Maintainability, and Functionality**
    * **Core Improvements:**
        * **Version Control & Project Structure:**
            * Implemented Git and GitHub for robust version control and reversibility.
            * Established a structured Visual Studio project for improved traceability.
        * **Comprehensive Code Refactoring:**
            * Simplified code, enhanced menus, and added extensive comments.
            * Standardized terminal logs with clear tags (e.g., `[WARN]`, `[ERROR]`).
            * Established a consistent folder structure.
        * **Enhanced Error Handling:**
            * Implemented comprehensive error handling, including:
                * Error-level checks in batch files.
                * Post-execution checks for critical operations.
        * **Improved User Feedback:**
            * Enhanced console output with clear, user-friendly messages.
        * **Documentation:**
            * Created/updated `README.md`, `CHANGELOG.md`, and `requirements.txt`.
            * Improved in-code documentation.
    * **Feature Updates:**
        * **Translation 2.0:**
            * Automated language detection and file renaming based on language tags.
            * Implemented a script to exclude 100% matches from target translation files.
        * **TFC Script Enhancements:**
            * Added a script to automatically remove platform locales from target `.xlf` files.
    * **New Features:**
        * **Tool: Remove Platform Locales:**
            * Automates the removal of platform locales from target `.xlf` files.
        * **MS Office Tools: Hide by Colors in Word Files:**
            * Enables selective hiding of text in `.docx` files based on font and highlight colors.
            * Generates an HTML report with color indices.
            * Provides filtering options (hide selected or hide non-selected colors).
          * **MS Office Tools: Split/Merge multilingual .xlsx files:**
            * Splits a multilingual Excel file into individual bilingual files based on source and target language columns.
            * Generates detailed metadata to enable seamless back merging of updated translations into the original file.
            * Preserves original formatting and structure, ensuring consistency across split and merged documents.
    * **Key Changes Summary:**
        * Strengthened version control and project organization.
        * Significantly improved code quality and maintainability.
        * Enhanced error handling and user feedback.
        * Streamlined translation workflows.
        * Added a powerful new color-based document filtering tool.

* **v0.1 - Initial Release**
