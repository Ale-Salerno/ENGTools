@echo off
REM ============================================================================
REM ENGTools.bat - Central menu for ENGTools
REM Version: 0.2 - Refactored
REM ----------------------------------------------------------------------------
REM This script provides a full menu with options for:
REM   - Source File Preparation (Standard & Custom)
REM   - Proofreading
REM   - Pretranslation
REM   - Epiroc TXT processing
REM   - TM Management
REM   - Translation 2.0
REM   - Alignment (ID-based, segmentation options)
REM   - Microsoft Office Tools
REM   - Various additional Tools (folder flattening, distribution, JSON/XPath
REM     extraction, Regin .en file tasks)
REM ----------------------------------------------------------------------------
REM REQUIREMENTS:
REM  - Java 17
REM  - Python 3.x
REM  - Okapi Framework
REM  - 7-Zip (for zip packaging)
REM  - Access to W:\Tools\ENGTools folder structure (or modify paths as needed)
REM ----------------------------------------------------------------------------
REM NOTE: This file self-deletes on normal exit to avoid accidental reuse.
REM ============================================================================
call chcp 65001 >nul
title ENGTools 0.2

REM ----------------------------------------------------------------------------
REM Set environment variables for general usage
REM ----------------------------------------------------------------------------
set "original_path=%cd%"
set "okapiPath=C:\Software\Okapi"

:WELCOME
cls
color 0F
echo ================================================================================
echo =                             ENGTools 0.2                                    =
echo ================================================================================
echo LanguageWire LE ^| Last update 2025-07-25
echo.
echo Java 21 ^| The Okapi Framework ^| Python 3.x ^| GLAP ^| 7-Zip
echo -------------------------------------------------------------------------------
echo   Welcome to ENGTools!
echo   Please select a task:
echo.
echo    1. Source File Preparation
echo    2. TM Management
echo    3. Translation
echo    4. Alignment
echo    5. Microsoft Office Tools
echo    6. Tools
echo    7. File Format Conversions
echo    8. Help
echo    0. Exit
echo.
set /p TASK="Enter your choice [0-8]: "

if "%TASK%"=="" (
    echo [ERROR] No input provided. Please enter a valid number.
    pause
    goto WELCOME
)

if "%TASK%"=="1" goto SFP
if "%TASK%"=="2" goto TMMANAGEMENT
if "%TASK%"=="3" goto TRANSLATION
if "%TASK%"=="4" goto ALIGNMENT
if "%TASK%"=="5" goto OFFICE
if "%TASK%"=="6" goto TOOLS
if "%TASK%"=="7" goto FILEFORMATCONVERSION
if "%TASK%"=="8" (
    start https://languagewire.cloud.xwiki.com/xwiki/bin/view/Delivery/Engineering/ENGTools/
    goto WELCOME
)
if "%TASK%"=="0" goto CLOSE

echo [ERROR] Invalid option. Please try again.
pause
goto WELCOME

REM ============================================================================
REM SOURCE FILE PREPARATION SECTION
REM ============================================================================
:SFP
cls
color 0A
echo ================================================================================
echo =                      Source File Preparation (SFP)                          =
echo ================================================================================
echo   1. Okapi - Standard SFP (No custom parser, default filter)
echo   2. Okapi - Custom SFP (Custom parser; you will be prompted)
echo   3. Okapi - XLIFF SFP
echo   4. Okapi - Source File Preparation for Proofreading
echo   5. Okapi - Pretranslation
echo   -------------------------------------------------------------------------------
echo   6. Daimler Multilingual Proofreading
echo   7. Epiroc TXT
echo   8. AXIS Type 4
echo   9. Beurer
echo   10. Edwards
echo   -------------------------------------------------------------------------------
echo   11. Confirm Segments SDLXLIFF
echo   0. Back
echo.
set /p TASK="Enter your choice [0-10]: "

if "%TASK%"=="" (
    echo [ERROR] No input provided. Please enter a valid number.
    pause
    goto SFP
)

if "%TASK%"=="1" goto OKAPISTANDARDSPF
if "%TASK%"=="2" goto OKAPICUSTOMSPF
if "%TASK%"=="3" goto XLIFFPREP
if "%TASK%"=="4" goto PROOFREADING
if "%TASK%"=="5" goto PRETRANSLATE
if "%TASK%"=="6" goto DAIMLERMULTILINGUAL
if "%TASK%"=="7" goto EPIROCTXT
if "%TASK%"=="8" goto AXISTYPE4
if "%TASK%"=="9" goto BEURER
if "%TASK%"=="10" goto EDWARDSBRANDS
if "%TASK%"=="11" goto CONFIRMSDLXLIFF
if "%TASK%"=="0" goto WELCOME

echo [ERROR] Invalid option. Please try again.
pause
goto SFP

REM ----------------------------------------------------------------------------
REM SFP - Standard
REM ----------------------------------------------------------------------------
:OKAPISTANDARDSPF
cls
color 0A
echo ================================================================================
echo =                  Okapi - Standard Source File Preparation                   =
echo ================================================================================
echo.

REM Prompt for source and target languages
set /p SLC="Enter source language code (e.g., en): "
set /p TLC="Enter target language code (e.g., de): "

REM Create necessary folders
echo.
echo Creating folder structure...
mkdir Prep\01_source 2>nul
mkdir Prep\02_transl 2>nul
mkdir Prep\03_pseudo 2>nul
mkdir Prep\04_configs 2>nul
mkdir Prep\05_translated 2>nul

REM Copy files and filter definitions
echo.
echo Copying required files...
robocopy . Prep\01_source *.* /XF *.bat /NDL /NFL /NJH /NJS /NP >nul
robocopy W:\Tools\ENGTools\Segmentation\okapi Prep\04_configs defaultSegmentation.srx /NDL /NFL /NJH /NJS /NP >nul
robocopy W:\Tools\ENGTools\Pipelines Prep\04_configs pseudo.pln /NDL /NFL /NJH /NJS /NP >nul
robocopy W:\Tools\ENGTools\Dependencies\bats Prep TFC.bat /NDL /NFL /NJH /NJS /NP >nul

REM Create XLF files via Okapi
echo.
echo Creating XLF files...
call "%okapiPath%\tikal.bat" -x Prep\01_source\*.* -seg Prep\04_configs\*.srx -sl %SLC% -tl %TLC% -nocopy -od Prep\02_transl -ie utf-8

REM Run Python script escape_more_than.py
robocopy W:\Tools\ENGTools\Dependencies\python Prep\02_transl escape_more_than.py /NDL /NFL /NJH /NJS /NP >nul
call python Prep\02_transl\escape_more_than.py
del Prep\02_transl\*.py

REM Pseudotranslating prepped files
echo.
echo Pseudotranslating files...

robocopy Prep\02_transl Prep\03_pseudo *.xlf /NDL /NFL /NJH /NJS /NP >nul


cd /d Prep\03_pseudo

robocopy W:\Tools\ENGTools\Dependencies\python . pseudo.py /NDL /NFL /NJH /NJS /NP >nul
call python pseudo.py
del *.py

cd /d %original_path%

robocopy W:\Tools\ENGTools\Dependencies\python Prep\03_pseudo escape_more_than.py /NDL /NFL /NJH /NJS /NP >nul
call python Prep\03_pseudo\escape_more_than.py
del Prep\03_pseudo\*.py

call "%okapiPath%\tikal.bat" -m Prep\03_pseudo\*.xlf -sd Prep\01_source -od Prep\03_pseudo -ie utf-8

REM Create zip package
echo.
echo Creating zip package (Prep.zip)...
call "c:\Program Files\7-Zip\7z.exe" a "Prep.zip" .\Prep\*
goto ENDBAT

REM ----------------------------------------------------------------------------
REM SFP - Custom
REM ----------------------------------------------------------------------------
:OKAPICUSTOMSPF
cls
color 0A
echo ================================================================================
echo =                    Okapi - Custom Source File Preparation                    =
echo ================================================================================
echo.

REM Prompt user for source/target languages
set /p SLC="Enter source language code (e.g., en): "
set /p TLC="Enter target language code (e.g., de): "

REM Create necessary folders
echo.
echo Creating folder structure...
mkdir Prep\01_source 2>nul
mkdir Prep\02_transl 2>nul
mkdir Prep\03_pseudo 2>nul
mkdir Prep\04_configs 2>nul
mkdir Prep\05_translated 2>nul

echo.
echo Please copy your custom parser (*.fprm) into Prep\04_configs, then press any key.
start Prep\04_configs
pause >nul

REM Copy base files
echo.
echo Copying required files...
robocopy . Prep\01_source *.* /XF *.bat *.fprm /NDL /NFL /NJH /NJS /NP >nul
robocopy W:\Tools\ENGTools\Segmentation\okapi Prep\04_configs defaultSegmentation.srx /NDL /NFL /NJH /NJS /NP >nul
robocopy W:\Tools\ENGTools\Pipelines Prep\04_configs pseudo.pln /NDL /NFL /NJH /NJS /NP >nul
robocopy W:\Tools\ENGTools\Dependencies\bats Prep TFC_custom.bat /NDL /NFL /NJH /NJS /NP >nul

REM Create XLF files via Okapi with custom parser
echo.
echo Creating XLF files...
call "%okapiPath%\tikal.bat" -x Prep\01_source\*.* -seg Prep\04_configs\*.srx -fc Prep\04_configs\*.fprm -sl %SLC% -tl %TLC% -nocopy -od Prep\02_transl -ie utf-8

REM Escape special characters
robocopy W:\Tools\ENGTools\Dependencies\python Prep\02_transl escape_more_than.py /NDL /NFL /NJH /NJS /NP >nul
call python Prep\02_transl\escape_more_than.py
del Prep\02_transl\*.py

REM Pseudotranslation
echo.
echo Pseudotranslating files...


robocopy Prep\02_transl Prep\03_pseudo *.xlf /NDL /NFL /NJH /NJS /NP >nul


cd /d Prep\03_pseudo

robocopy W:\Tools\ENGTools\Dependencies\python . pseudo.py /NDL /NFL /NJH /NJS /NP >nul
call python pseudo.py
del *.py

cd /d %original_path%

robocopy W:\Tools\ENGTools\Dependencies\python "%original_path%\Prep\03_pseudo" escape_more_than.py /NDL /NFL /NJH /NJS /NP >nul
call python "%original_path%\Prep\03_pseudo\escape_more_than.py"
del "%original_path%\Prep\03_pseudo\*.py"

cd /d "%original_path%"
call "%okapiPath%\tikal.bat" -m Prep\03_pseudo\*.xlf -sd Prep\01_source -od Prep\03_pseudo -fc Prep\04_configs\*.fprm -ie utf-8

REM Create zip package
echo.
echo Creating zip package (Prep.zip)...
call "c:\Program Files\7-Zip\7z.exe" a "Prep.zip" .\Prep\*
goto ENDBAT

REM ----------------------------------------------------------------------------
REM SFP - Custom
REM ----------------------------------------------------------------------------
:XLIFFPREP
cls
color 0A
echo ================================================================================
echo =                    Okapi - XLIFF SPF                                         =
echo ================================================================================
echo.

REM Prompt user for source/target languages
set /p SLC="Enter source language code (e.g., en): "
set /p TLC="Enter target language code (e.g., de): "

REM Create necessary folders
echo.
echo Creating folder structure...
mkdir Prep\01_source 2>nul
mkdir Prep\02_transl 2>nul
mkdir Prep\03_pseudo 2>nul
mkdir Prep\04_configs 2>nul
mkdir Prep\05_translated 2>nul

REM Copy base files
echo.
echo Copying required files...
robocopy . Prep\01_source *.* /XF *.bat *.fprm /NDL /NFL /NJH /NJS /NP >nul
robocopy W:\Tools\ENGTools\Parsers\okapi Prep\04_configs okf_xliff@XLIFF-with-placeholder.fprm /NDL /NFL /NJH /NJS /NP >nul
robocopy W:\Tools\ENGTools\Segmentation\okapi Prep\04_configs defaultSegmentation.srx /NDL /NFL /NJH /NJS /NP >nul
robocopy W:\Tools\ENGTools\Dependencies\bats Prep TFC_xlf.bat /NDL /NFL /NJH /NJS /NP >nul

echo.
echo Please check your custom parser before proceeding, then press any key.
call tikal.bat -e -fc Prep\04_configs\*.fprm
pause >nul

REM Create XLF files via Okapi with custom parser
echo.
echo Creating XLF files...
call "%okapiPath%\tikal.bat" -x Prep\01_source\*.* -seg Prep\04_configs\*.srx -fc Prep\04_configs\*.fprm -sl %SLC% -tl %TLC% -nocopy -od Prep\02_transl -ie utf-8


REM Pseudotranslation
echo.
echo Pseudotranslating files...


robocopy Prep\02_transl Prep\03_pseudo *.xlf /NDL /NFL /NJH /NJS /NP >nul


cd /d Prep\03_pseudo

robocopy W:\Tools\ENGTools\Dependencies\python . pseudo.py /NDL /NFL /NJH /NJS /NP >nul
call python pseudo.py
del *.py


cd /d "%original_path%"
call "%okapiPath%\tikal.bat" -m Prep\03_pseudo\*.xlf -sd Prep\01_source -od Prep\03_pseudo -fc Prep\04_configs\*.fprm -ie utf-8

REM Create zip package
echo.
echo Creating zip package (Prep.zip)...
call "c:\Program Files\7-Zip\7z.exe" a "Prep.zip" .\Prep\*
goto ENDBAT

REM ----------------------------------------------------------------------------
REM SFP - Proofreading
REM ----------------------------------------------------------------------------
:PROOFREADING
cls
color 0A
echo ================================================================================
echo =               Okapi - SFP for Proofreading Preparation                     =
echo ================================================================================
echo.

REM Prompt user for source/target languages
set /p SLC="Enter source language code (e.g., en): "
set /p TLC="Enter target language code (e.g., de): "

REM Create necessary folders
echo.
echo Creating folder structure...
mkdir Prep\01_source 2>nul
mkdir Prep\02_transl 2>nul
mkdir Prep\03_proofread 2>nul

REM Copy essential files
echo.
echo Copying required files...
robocopy . Prep\01_source *.* /XF *.bat /NDL /NFL /NJH /NJS /NP >nul
robocopy W:\Tools\ENGTools\Dependencies\bats Prep TFC_proof.bat /NDL /NFL /NJH /NJS /NP >nul

REM Create XLF files
echo.
echo Creating XLF files...
call "%okapiPath%\tikal.bat" -x Prep\01_source\*.* -sl %SLC% -tl %TLC% -nocopy -od Prep\02_transl -ie utf-8

robocopy W:\Tools\ENGTools\Dependencies\python Prep\02_transl escape_more_than.py /NDL /NFL /NJH /NJS /NP >nul
call python Prep\02_transl\escape_more_than.py
del Prep\02_transl\*.py

REM Run proofread_state.py to set translation state
echo.
echo Setting state to "translated"...
robocopy W:\Tools\ENGTools\Dependencies\python Prep\02_transl proofread_state.py /NDL /NFL /NJH /NJS /NP >nul
call python Prep\02_transl\proofread_state.py Prep\02_transl
del Prep\02_transl\*.py

REM Create zip package
echo.
echo Creating zip package (Prep.zip)...
call "c:\Program Files\7-Zip\7z.exe" a "Prep.zip" .\Prep\*
goto ENDBAT

REM ----------------------------------------------------------------------------
REM SFP - Pretranslate
REM ----------------------------------------------------------------------------
:PRETRANSLATE
cls
color 0A
echo ================================================================================
echo =                          Okapi - Pretranslation                              =
echo ================================================================================
echo.

REM Prompt user for source/target languages
set /p SLC="Enter source language code (e.g., en): "
set /p TLC="Enter target language code (e.g., de): "

echo.
echo Pretranslating files...
FOR %%F IN (*.*) DO (
  IF /I NOT "%%~xF"==".bat" (
    IF /I NOT "%%~xF"==".tmx" (
      call "%okapiPath%\tikal.bat" -t "%%F" -sl %SLC% -tl %TLC% -bi *.tmx -ie utf-8
    )
  )
)
goto ENDBAT

REM ----------------------------------------------------------------------------
REM SFP - Daimler Multilingual Proofreading
REM ----------------------------------------------------------------------------
:DAIMLERMULTILINGUAL
cls
color 0A
echo ================================================================================
echo =                    Daimler Multilingual Proofreading                         =
echo ================================================================================
echo.


REM Create necessary folders
echo.
echo Splitting xlsx files into bilingual files...
robocopy W:\Tools\ENGTools\Dependencies\python . daimler_split.py /NDL /NFL /NJH /NJS /NP >nul
call python daimler_split.py
del *.py

REM Create necessary folders
echo.
echo Creating folder structure...
mkdir Prep\01_source 2>nul
mkdir Prep\02_transl 2>nul
mkdir Prep\03_configs 2>nul
mkdir Prep\04_translated 2>nul

move "split_files\*.*" "Prep\01_source\"
move "original_metadata" "Prep\"


REM Copy base files
echo.
echo Copying required files...
robocopy W:\Tools\ENGTools\Parsers\okapi Prep\03_configs okf_openxml@daimler_multilingual.fprm /NDL /NFL /NJH /NJS /NP >nul
robocopy W:\Tools\ENGTools\Dependencies\bats Prep TFC_daimler.bat /NDL /NFL /NJH /NJS /NP >nul

REM Create XLF files via Okapi with custom parser
echo.
echo Creating XLF files...
call "%okapiPath%\tikal.bat" -x Prep\01_source\*.* -fc Prep\03_configs\*.fprm -sl en -tl de -nocopy -od Prep\02_transl -ie utf-8

REM Escape special characters
robocopy W:\Tools\ENGTools\Dependencies\python Prep\02_transl escape_more_than.py /NDL /NFL /NJH /NJS /NP >nul
call python Prep\02_transl\escape_more_than.py
del Prep\02_transl\*.py

REM Run proofread_state.py to set translation state
echo.
echo Setting state to "translated"...
robocopy W:\Tools\ENGTools\Dependencies\python Prep\02_transl proofread_state.py /NDL /NFL /NJH /NJS /NP >nul
call python Prep\02_transl\proofread_state.py Prep\02_transl
del Prep\02_transl\*.py

REM Distribute by TLC
cd /d Prep\02_transl
robocopy W:\Tools\ENGTools\Dependencies\python .  distribute_TLC.py /NDL /NFL /NJH /NJS /NP >nul
call python distribute_TLC.py
del *.py

cd /d %original_path%

rmdir split_files /s /q

call "c:\Program Files\7-Zip\7z.exe" a -tzip "del.zip" .\Prep\02_transl\* -r

REM Create zip package
echo.
echo Creating zip package (Prep.zip)...
call "c:\Program Files\7-Zip\7z.exe" a "Prep.zip" .\Prep\*
goto ENDBAT

REM ----------------------------------------------------------------------------
REM SFP - Epiroc TXT
REM ----------------------------------------------------------------------------
:EPIROCTXT
cls
color 0A
echo ================================================================================
echo =                             Epiroc TXT                                      =
echo ================================================================================
echo.

mkdir backup 2>nul
mkdir Prep 2>nul

REM Extract from ZIP to Prep folder
call "c:\Program Files\7-Zip\7z.exe" x *.zip -o.\Prep\* -y
MOVE *.zip backup

REM Flatten folder
robocopy W:\Tools\ENGTools\Dependencies\python .\Prep flatten_folder_structure.py /NDL /NFL /NJH /NJS /NP >nul
cd /d Prep
call python flatten_folder_structure.py
del *.py

REM Cleanup
cd /d .
for /d %%D in (*) do (
    if /i not "%%~nxD"=="FLATTEN" (
        echo Deleting folder: %%D
        rmdir /s /q "%%D"
    )
)

cd /d %original_path%

REM Create standard folder structure for Epiroc
echo.
echo Creating folder structure...
mkdir Prep\01_source 2>nul
mkdir Prep\02_transl 2>nul
mkdir Prep\03_configs 2>nul
mkdir Prep\04_translated 2>nul

echo.
echo Copying required files...
MOVE "%original_path%\Prep\FLATTEN\*.*" "%original_path%\Prep\01_source"
robocopy . Prep\01_source *.* /XF *.bat /NDL /NFL /NJH /NJS /NP >nul
robocopy W:\Tools\ENGTools\Segmentation\okapi Prep\03_configs defaultSegmentation.srx /NDL /NFL /NJH /NJS /NP >nul
robocopy W:\Tools\ENGTools\Dependencies\bats Prep TFC_epiroc.bat /NDL /NFL /NJH /NJS /NP >nul
robocopy W:\Tools\ENGTools\Parsers\okapi Prep\03_configs okf_regex@epiroc_txt.fprm /NDL /NFL /NJH /NJS /NP >nul

REM Create XLF with Epiroc parser
echo.
echo Creating XLF files...
call "%okapiPath%\tikal.bat" -x Prep\01_source\*.* -seg Prep\03_configs\*.srx -sl en -tl de -nocopy -fc Prep\03_configs\okf_regex@epiroc_txt.fprm -od Prep\02_transl -ie utf-8

cd /d Prep\02_transl
robocopy W:\Tools\ENGTools\Dependencies\python . remove_empty_xlf.py /NDL /NFL /NJH /NJS /NP >nul
call python remove_empty_xlf.py
del *.py

robocopy W:\Tools\ENGTools\Dependencies\python . escape_more_than.py /NDL /NFL /NJH /NJS /NP >nul
call python escape_more_than.py
del escape_more_than.py

cd /d "%original_path%"
rmdir /s /q Prep\FLATTEN

echo.
echo Creating zip package (Prep.zip)...
call "c:\Program Files\7-Zip\7z.exe" a "Prep.zip" .\Prep\*
goto ENDBAT

REM ----------------------------------------------------------------------------
REM SFP - AXIS Type 4
REM ----------------------------------------------------------------------------
:AXISTYPE4
cls
color 0A
echo ================================================================================
echo =                             AXIS                                      =
echo ================================================================================
echo.

mkdir backup 2>nul
mkdir Prep 2>nul

REM Extract from ZIP to Prep folder
call "c:\Program Files\7-Zip\7z.exe" x *.zip -o.\Prep\* -y
MOVE *.zip backup

REM Flatten folder
robocopy W:\Tools\ENGTools\Dependencies\python .\Prep flatten_folder_structure.py /NDL /NFL /NJH /NJS /NP >nul
cd /d Prep
call python flatten_folder_structure.py
del *.py

REM Cleanup
cd /d .
for /d %%D in (*) do (
    if /i not "%%~nxD"=="FLATTEN" (
        echo Deleting folder: %%D
        rmdir /s /q "%%D"
    )
)

cd /d %original_path%

REM Create standard folder structure for AXIS Type4
echo.
echo Creating folder structure...
mkdir Prep\01_source 2>nul
mkdir Prep\02_transl 2>nul
mkdir Prep\03_pseudo 2>nul
mkdir Prep\04_configs 2>nul
mkdir Prep\05_translated 2>nul

echo.
echo Copying required files...
MOVE "%original_path%\Prep\FLATTEN\*.*" "%original_path%\Prep\01_source"
robocopy . Prep\01_source *.* /XF *.bat /NDL /NFL /NJH /NJS /NP >nul
robocopy W:\Tools\ENGTools\Segmentation\okapi Prep\04_configs defaultSegmentation.srx /NDL /NFL /NJH /NJS /NP >nul
robocopy W:\Tools\ENGTools\Dependencies\bats Prep TFC_axistype4.bat /NDL /NFL /NJH /NJS /NP >nul
robocopy W:\Tools\ENGTools\Parsers\okapi Prep\04_configs okf_regex@AxisType42.fprm /NDL /NFL /NJH /NJS /NP >nul

cd /d Prep\01_source

robocopy W:\Tools\ENGTools\Dependencies\python . comillas_true.py /NDL /NFL /NJH /NJS /NP >nul
call python comillas_true.py
del *.py

cd /d %original_path%

REM Create XLF with Axis Type 4 parser
echo.
echo Creating XLF files...
call "%okapiPath%\tikal.bat" -x Prep\01_source\*.* -seg Prep\04_configs\*.srx -sl en -tl de -nocopy -fc Prep\04_configs\okf_regex@AxisType42.fprm -od Prep\02_transl -ie utf-8

robocopy W:\Tools\ENGTools\Dependencies\python . escape_more_than.py /NDL /NFL /NJH /NJS /NP >nul
call python escape_more_than.py
del escape_more_than.py

REM Pseudotranslation
echo.
echo Pseudotranslating files...


robocopy Prep\02_transl Prep\03_pseudo *.xlf /NDL /NFL /NJH /NJS /NP >nul


cd /d Prep\03_pseudo

robocopy W:\Tools\ENGTools\Dependencies\python . pseudo.py /NDL /NFL /NJH /NJS /NP >nul
call python pseudo.py
del *.py

cd /d "%original_path%"

call "%okapiPath%\tikal.bat" -m Prep\03_pseudo\*.xlf -sd Prep\01_source -od Prep\03_pseudo -ie utf-8 -fc Prep\04_configs\okf_regex@AxisType42.fprm

cd /d "%original_path%"
rmdir /s /q Prep\FLATTEN

echo.
echo Creating zip package (Prep.zip)...
call "c:\Program Files\7-Zip\7z.exe" a "Prep.zip" .\Prep\*
goto ENDBAT

REM ----------------------------------------------------------------------------
REM SFP - Beurer Multilingual
REM ----------------------------------------------------------------------------
:BEURER
cls
color 0A
echo ================================================================================
echo =                    BEURER                                                    =
echo ================================================================================
echo.


REM Create necessary folders
echo.
echo Splitting xlsx files into bilingual files...
robocopy W:\Tools\ENGTools\Dependencies\python . beurer_split.py /NDL /NFL /NJH /NJS /NP >nul
call python beurer_split.py
del *.py

REM Create necessary folders
echo.
echo Creating folder structure...
mkdir Prep\01_source 2>nul
mkdir Prep\02_transl 2>nul
mkdir Prep\04_configs 2>nul
mkdir Prep\03_pseudo 2>nul
mkdir Prep\05_translated 2>nul

move "split_files\*.*" "Prep\01_source\"
move "original_metadata" "Prep\"


REM Copy base files
echo.
echo Copying required files...
robocopy W:\Tools\ENGTools\Parsers\okapi Prep\04_configs okf_openxml@beurer.fprm /NDL /NFL /NJH /NJS /NP >nul
robocopy W:\Tools\ENGTools\Dependencies\bats Prep TFC_beurer.bat /NDL /NFL /NJH /NJS /NP >nul
robocopy W:\Tools\ENGTools\Segmentation\okapi Prep\04_configs defaultSegmentation.srx /NDL /NFL /NJH /NJS /NP >nul



REM Create XLF files via Okapi with custom parser
echo.
echo Creating XLF files...
call "%okapiPath%\tikal.bat" -x Prep\01_source\*.* -seg Prep\04_configs\*.srx -sl de -tl en -fc Prep\04_configs\okf_openxml@beurer.fprm -nocopy -seg -od Prep\02_transl -ie utf-8

REM Run Python script escape_more_than.py
robocopy W:\Tools\ENGTools\Dependencies\python Prep\02_transl escape_more_than.py /NDL /NFL /NJH /NJS /NP >nul
call python Prep\02_transl\escape_more_than.py
del Prep\02_transl\*.py

REM Pseudotranslating prepped files
echo.
echo Pseudotranslating files...

robocopy Prep\02_transl Prep\03_pseudo *.xlf /NDL /NFL /NJH /NJS /NP >nul


cd /d Prep\03_pseudo

robocopy W:\Tools\ENGTools\Dependencies\python . pseudo.py /NDL /NFL /NJH /NJS /NP >nul
call python pseudo.py
del *.py

cd /d %original_path%

robocopy W:\Tools\ENGTools\Dependencies\python Prep\03_pseudo escape_more_than.py /NDL /NFL /NJH /NJS /NP >nul
call python Prep\03_pseudo\escape_more_than.py
del Prep\03_pseudo\*.py

call "%okapiPath%\tikal.bat" -m Prep\03_pseudo\*.xlf -sd Prep\01_source -od Prep\03_pseudo -ie -ie utf-8 -fc Prep\04_configs\okf_openxml@beurer.fprm

rmdir split_files /s /q

REM Create zip package
echo.
echo Creating zip package (Prep.zip)...
call "c:\Program Files\7-Zip\7z.exe" a "Prep.zip" .\Prep\*
goto ENDBAT

REM ----------------------------------------------------------------------------
REM SFP - Edwards
REM ----------------------------------------------------------------------------
:EDWARDSBRANDS
cls
color 0A
echo ================================================================================
echo =                    EDWARDS BRANDS                                            =
echo ================================================================================
echo.


echo   Please select a brand:
echo.
echo    1. Edwards
echo    2. Leybold
echo    3. Atlas
echo   -----------------
echo    0. Exit
echo.
set /p BRAND="Enter your choice [0-3]: "

if "%BRAND%"=="" (
    echo [ERROR] No input provided. Please enter a valid number.
    pause
    goto EDWARDSBRANDS
)

if "%BRAND%"=="1" goto EDWARDS
if "%BRAND%"=="2" goto LEYBOLD
if "%BRAND%"=="3" goto ATLAS
if "%BRAND%"=="0" goto SFP

:EDWARDS
cls
color 0C
echo ================================================================================
echo =                           EDWARDS                                            =
echo ================================================================================

REM Copy base files
echo.
echo Copying required files...
robocopy W:\Tools\ENGTools\Dependencies\mappings . mapping_Edwards.xlsx /NDL /NFL /NJH /NJS /NP >nul
robocopy W:\Tools\ENGTools\Dependencies\python . Edwards.py /NDL /NFL /NJH /NJS /NP >nul

REM Running Python script
call python Edwards.py
del Edwards.py
del mapping_Edwards.xlsx
goto ENDBAT

:LEYBOLD
cls
color 0C
echo ================================================================================
echo =                           LEYBOLD                                            =
echo ================================================================================

REM Copy base files
echo.
echo Copying required files...
robocopy W:\Tools\ENGTools\Dependencies\mappings . mapping_Leybold.xlsx /NDL /NFL /NJH /NJS /NP >nul
robocopy W:\Tools\ENGTools\Dependencies\python . Leybold.py /NDL /NFL /NJH /NJS /NP >nul

REM Running Python script
call python Leybold.py
del Leybold.py
del mapping_Leybold.xlsx
goto ENDBAT

:ATLAS
cls
color 0C
echo ================================================================================
echo =                           ATLAS                                              =
echo ================================================================================

REM Copy base files
echo.
echo Copying required files...
robocopy W:\Tools\ENGTools\Dependencies\mappings . mapping_Atlas.xlsx /NDL /NFL /NJH /NJS /NP >nul
robocopy W:\Tools\ENGTools\Dependencies\python . Atlas.py /NDL /NFL /NJH /NJS /NP >nul

REM Running Python script
call python Atlas.py
del Atlas.py
del mapping_Atlas.xlsx
goto ENDBAT


REM ----------------------------------------------------------------------------
REM Confirm Segments SDLXLIFF
REM ----------------------------------------------------------------------------
:CONFIRMSDLXLIFF
cls
color 0A
echo ================================================================================
echo =                             Confirm Segments SDLXLIFF                        =
echo ================================================================================
echo.
robocopy W:\Tools\ENGTools\Dependencies\python . sdlxliff_translate_state.py /NDL /NFL /NJH /NJS /NP >nul
call python sdlxliff_translate_state.py
del *.py
goto ENDBAT
REM ============================================================================
REM TM MANAGEMENT SECTION
REM ============================================================================
:TMMANAGEMENT
cls
color 0B
echo ================================================================================
echo =                            TM Management                                   =
echo ================================================================================
echo   1. XLF and flavours to TMX
echo   2. XLF and flavours to bilingual table
echo   3. Clean up TMX
echo   4. Excel to TMX (bilingual/multilingual)
echo   5. Resegment paragraph-based TMX
echo   6. Split Multilingual TMX
echo   -------------------------------------------------------------------------------
echo   0. Back
echo.
set /p TASK="Enter your choice [0-6]: "

if "%TASK%"=="" (
    echo [ERROR] No input provided. Please enter a valid number.
    pause
    goto TMMANAGEMENT
)

if "%TASK%"=="1" goto XLFTOTMX
if "%TASK%"=="2" goto XLFTOBT
if "%TASK%"=="3" goto CLEANUPTMX
if "%TASK%"=="4" goto EXCELTOTMX
if "%TASK%"=="5" goto RESEGMENT
if "%TASK%"=="6" goto SPLITMULTITMX
if "%TASK%"=="0" goto WELCOME

echo [ERROR] Invalid option. Please try again.
pause
goto TMMANAGEMENT

REM ----------------------------------------------------------------------------
REM TM - XLF to TMX
REM ----------------------------------------------------------------------------
:XLFTOTMX
cls
color 0B
echo ================================================================================
echo =                         XLF and flavours to TMX                              =
echo ================================================================================
echo Converting files...
call "%okapiPath%\tikal.bat" -2tmx *.*xl* -fc W:\Tools\ENGTools\Parsers\okapi\okf_xliff@xlf2tmx.fprm -ie utf-8

echo Cleaning up TMX file(s)...
robocopy W:\Tools\ENGTools\Dependencies\python . cleanprops.py /NDL /NFL /NJH /NJS /NP >nul
call python cleanprops.py
del *.py
goto ENDBAT

REM ----------------------------------------------------------------------------
REM TM - XLF to bilingual table
REM ----------------------------------------------------------------------------
:XLFTOBT
cls
color 0B
echo ================================================================================
echo =                     XLF and flavours to bilingual table                      =
echo ================================================================================
echo Converting files...
call "%okapiPath%\tikal.bat" -2tbl *.*xl* -fc W:\Tools\ENGTools\Parsers\okapi\okf_xliff@xlf2tmx.fprm -csv -tmx -ie utf-8
goto ENDBAT

REM ----------------------------------------------------------------------------
REM TM - Clean up TMX
REM ----------------------------------------------------------------------------
:CLEANUPTMX
cls
color 0B
echo ================================================================================
echo =                            Clean up TMX                                     =
echo ================================================================================
echo Cleaning up TMX file(s)...
robocopy W:\Tools\ENGTools\Dependencies\python . cleanprops.py /NDL /NFL /NJH /NJS /NP >nul
call python cleanprops.py
del *.py
goto ENDBAT

REM ----------------------------------------------------------------------------
REM TM - Excel to TMX
REM ----------------------------------------------------------------------------
:EXCELTOTMX
cls
color 0B
echo ================================================================================
echo =                Excel to TMX (bilingual/multilingual)                        =
echo ================================================================================
echo Running excel2tmx_multilingual.py...
robocopy W:\Tools\ENGTools\Dependencies\python . excel2tmx_multilingual.py /NDL /NFL /NJH /NJS /NP >nul
call python excel2tmx_multilingual.py
del *.py
goto ENDBAT

REM ----------------------------------------------------------------------------
REM TM - Split Multilingual TMX
REM ----------------------------------------------------------------------------
:SPLITMULTITMX
cls
color 0B
echo ================================================================================
echo =                Split Multilingual TMX                                       =
echo ================================================================================
echo Splitting multilingual TMX...
call "C:\Program Files\Analysis Package\bin\TmxSplitAll.cmd" .
goto ENDBAT

REM ----------------------------------------------------------------------------
REM TM - Resegment paragraph-based TMX
REM ----------------------------------------------------------------------------
:RESEGMENT
cls
color 0B
echo ================================================================================
echo =                       Resegment paragraph-based TMX                         =
echo ================================================================================
echo Resegmenting TMX...
call %okapiPath%\tikal.bat -x *.tmx -seg W:\Tools\ENGTools\Segmentation\okapi\defaultSegmentation.srx -ie utf-8
call "%okapiPath%\tikal.bat" -2tmx *.tmx.xlf -ie utf-8
del "%original_path%\*.tmx.xlf"
cd /d "%original_path%"
rename *.tmx.xlf.tmx by-sentence.tmx
robocopy W:\Tools\ENGTools\Dependencies\python . cleanprops.py /NDL /NFL /NJH /NJS /NP >nul
call python cleanprops.py
del *.py
goto ENDBAT

REM ============================================================================
REM TRANSLATION SECTION
REM ============================================================================
:TRANSLATION
cls
color 0C
echo ================================================================================
echo =                           Translation                                        =
echo ================================================================================
echo   1. Translation 2.0
echo   2. Translation
echo   -------------------------------------------------------------------------------
echo   0. Back
echo.
set /p TASK="Enter your choice [0-2]: "

if "%TASK%"=="" (
    echo [ERROR] No input provided. Please enter a valid number.
    pause
    goto REGIN
)

if "%TASK%"=="1" goto TRANSLATIONTWO
if "%TASK%"=="2" goto TRANSLATIONMONO
if "%TASK%"=="0" goto WELCOME

echo [ERROR] Invalid option. Please try again.
pause
goto REGIN

:TRANSLATIONTWO
cls
color 0C
echo ================================================================================
echo =                        Translation 2.0                                       =
echo ================================================================================
echo Renaming files...
robocopy W:\Tools\ENGTools\Dependencies\python . rename_translation_2_0.py /NDL /NFL /NJH /NJS /NP >nul
call python rename_translation_2_0.py
del *.py

echo.
echo Transferring German translations...
call "%okapiPath%\tikal.bat" -t de-at_target.xlf -bi de-de_source.xlf
call "%okapiPath%\tikal.bat" -t de-ch_target.xlf -bi de-de_source.xlf

echo.
echo Transferring Spanish translations...
call "%okapiPath%\tikal.bat" -t es-ar_target.xlf -bi es-es_source.xlf
call "%okapiPath%\tikal.bat" -t es-co_target.xlf -bi es-es_source.xlf
call "%okapiPath%\tikal.bat" -t es-cl_target.xlf -bi es-es_source.xlf
call "%okapiPath%\tikal.bat" -t es-mx_target.xlf -bi es-es_source.xlf
call "%okapiPath%\tikal.bat" -t es-us_target.xlf -bi es-es_source.xlf
call "%okapiPath%\tikal.bat" -t es-pe_target.xlf -bi es-es_source.xlf

echo.
echo Transferring French translations...
call "%okapiPath%\tikal.bat" -t fr-be_target.xlf -bi fr-fr_source.xlf
call "%okapiPath%\tikal.bat" -t fr-ca_target.xlf -bi fr-fr_source.xlf
call "%okapiPath%\tikal.bat" -t fr-ch_target.xlf -bi fr-fr_source.xlf

echo.
echo Transferring Italian translations...
call "%okapiPath%\tikal.bat" -t it-ch_target.xlf -bi it-it_source.xlf

echo.
echo Transferring Dutch translations...
call "%okapiPath%\tikal.bat" -t nl-be_target.xlf -bi nl-nl_source.xlf

echo.
echo Transferring Portuguese translations...
call "%okapiPath%\tikal.bat" -t pt-pt_target.xlf -bi pt-br_source.xlf
echo.

echo.
echo Transferring English translations...
call "%okapiPath%\tikal.bat" -t en-029_target.xlf -bi en-gb_source.xlf
call "%okapiPath%\tikal.bat" -t en-au_target.xlf -bi en-gb_source.xlf
call "%okapiPath%\tikal.bat" -t en-bz_target.xlf -bi en-gb_source.xlf
call "%okapiPath%\tikal.bat" -t en-ca_target.xlf -bi en-gb_source.xlf
call "%okapiPath%\tikal.bat" -t en-jm_target.xlf -bi en-gb_source.xlf
call "%okapiPath%\tikal.bat" -t en-in_target.xlf -bi en-gb_source.xlf

echo.
echo Escaping special characters...
robocopy W:\Tools\ENGTools\Dependencies\python . escape_more_than.py /NDL /NFL /NJH /NJS /NP >nul
call python escape_more_than.py
del *.py

REM echo Keeping 100%% matches and above...
REM robocopy W:\Tools\ENGTools\Dependencies\python . exact_match.py /NDL /NFL /NJH /NJS /NP >nul
REM call python exact_match.py
REM del *.py
goto ENDBAT

:TRANSLATIONMONO
cls
color 0C
echo ================================================================================
echo =                             Translation                                      =
echo ================================================================================
echo Renaming files and transferring translations...
robocopy W:\Tools\ENGTools\Dependencies\python . transfer.py /NDL /NFL /NJH /NJS /NP >nul
call python transfer.py
del *.py
goto ENDBAT

REM ============================================================================
REM ALIGNMENT SECTION
REM ============================================================================
:ALIGNMENT
cls
color 0E
echo ================================================================================
echo =                               Alignment                                     =
echo ================================================================================
echo   1. ID-based alignment
echo   -------------------------------------------------------------------------------
echo   0. Back
echo.
set /p TASK="Enter your choice [0-1]: "

if "%TASK%"=="" (
    echo [ERROR] No input provided. Please enter a valid number.
    pause
    goto ALIGNMENT
)

if "%TASK%"=="1" goto IDBASED
if "%TASK%"=="0" goto WELCOME

echo [ERROR] Invalid option. Please try again.
pause
goto ALIGNMENT

REM ----------------------------------------------------------------------------
REM Alignment - ID-based
REM ----------------------------------------------------------------------------
:IDBASED
set "sourcePath=%original_path%\src"
set "targetPath=%original_path%\tgt"

cls
color 0E
echo ================================================================================
echo =                         ID-based Alignment Setup                            =
echo ================================================================================
echo.

set /p SLC="Enter source language code (e.g., en): "
set /p TLC="Enter target language code (e.g., de): "

echo.
echo Do you want to segment the TMX by sentence?
echo   1. Yes
echo   2. No
echo.
set /p TASK="Enter your choice [1-2]: "

SET src_not_empty=0
SET tgt_not_empty=0

IF EXIST "src" (
    FOR /F %%i IN ('dir /A /B "src"') DO SET src_not_empty=1
)
IF EXIST "tgt" (
    FOR /F %%i IN ('dir /A /B "tgt"') DO SET tgt_not_empty=1
)

IF "%src_not_empty%"=="1" IF "%tgt_not_empty%"=="1" goto skip_to_okapi

IF NOT EXIST "src" mkdir src
IF NOT EXIST "tgt" mkdir tgt

echo.
echo Please place your source file into the 'src' folder and target file into 'tgt'.
echo.
pause

:skip_to_okapi
cd /d "%okapiPath%"
call "%okapiPath%\rainbow.exe" -pln W:\Tools\ENGTools\Pipelines\id_based_alignment.pln -sl %SLC% -tl %TLC% "%original_path%\src\*.*" "%original_path%\tgt\*.*" -np
timeout /t 4 /nobreak >nul

MOVE c:\TMX\* "%original_path%"
call "C:\Program Files\Analysis Package\bin\TmxSplitAll.cmd" "%original_path%\alignment.tmx" -f W:\Tools\ENGTools\Dependencies\ap\tmxtexttotag.properties
del "%original_path%\alignment.tmx"

if "%TASK%"=="1" goto SEGMENTTMX
if "%TASK%"=="2" goto NOSEGMENTTMX

echo [ERROR] Invalid choice. Proceeding without segmentation...
goto NOSEGMENTTMX

:SEGMENTTMX
call "%okapiPath%\tikal.bat" -x "%original_path%\alignment-fixed.tmx" -seg W:\Tools\ENGTools\Segmentation\okapi\defaultSegmentation.srx -ie utf-8
call "%okapiPath%\tikal.bat" -2tmx "%original_path%\alignment-fixed.tmx.xlf" -ie utf-8
del "%original_path%\alignment-fixed.tmx"
del "%original_path%\alignment-fixed.tmx.xlf"
cd /d "%original_path%"
rename alignment-fixed.tmx.xlf.tmx alignment-sentence.tmx
robocopy W:\Tools\ENGTools\Dependencies\python . cleanprops.py /NDL /NFL /NJH /NJS /NP >nul
call python cleanprops.py
del *.py
goto ENDBAT

:NOSEGMENTTMX
cd /d "%original_path%"
rename alignment-fixed.tmx alignment-paragraph.tmx
goto ENDBAT

REM ============================================================================
REM MICROSOFT OFFICE TOOLS
REM ============================================================================
:OFFICE
cls
color 06
echo ================================================================================
echo =                          Microsoft Office Tools                             =
echo ================================================================================
echo   *** MS Word ***
echo   1. Batch update TOCs
echo   2. Batch unhide and rename .doc(x)
echo   3. Batch hide based on color text in .doc(x) files
echo   4. Anonymize track changes
echo   -------------------------------------------------------------------------------
echo   *** MS Excel ***
echo   5. Batch unhide and rename .xls(x)
echo   6. Split/merge multilingual .xlsx files
echo   -------------------------------------------------------------------------------
echo   0. Back
echo.
set /p TASK="Enter your choice [0-6]: "

if "%TASK%"=="" (
    echo [ERROR] No input provided. Please enter a valid number.
    pause
    goto OFFICE
)

if "%TASK%"=="1" goto TOC
if "%TASK%"=="2" goto UNHIDEDOC
if "%TASK%"=="3" goto REDTEXT
if "%TASK%"=="4" goto ANONYMIZER
if "%TASK%"=="5" goto UNHIDEXLS
if "%TASK%"=="6" goto MULTIEXCEL
if "%TASK%"=="0" goto WELCOME

echo [ERROR] Invalid option. Please try again.
pause
goto OFFICE

REM ----------------------------------------------------------------------------
REM Office - Word
REM ----------------------------------------------------------------------------
:TOC
cls
color 06
echo ================================================================================
echo =               Batch update TOCs in .doc(x) files (Word)                    =
echo ================================================================================
robocopy W:\Tools\ENGTools\Dependencies\python . updateTOC.py /NDL /NFL /NJH /NJS /NP >nul
call python updateTOC.py
del *.py
goto ENDBAT

:UNHIDEDOC
cls
color 06
echo ================================================================================
echo =          Batch unhide and rename .doc(x) files (Word)                      =
echo ================================================================================
robocopy W:\Tools\ENGTools\Dependencies\python . unhide_rename_docx.py /NDL /NFL /NJH /NJS /NP >nul
call python unhide_rename_docx.py
del *.py
goto ENDBAT

:REDTEXT
cls
color 06
echo ================================================================================
echo =   Batch hide based on color text in .doc(x) files (Word)            =
echo ================================================================================
robocopy W:\Tools\ENGTools\Dependencies\python . hide_no_colour.py /NDL /NFL /NJH /NJS /NP >nul
call python hide_no_colour.py
del *.py
goto ENDBAT

:ANONYMIZER
cls
color 06
echo ================================================================================
echo =                           ANONYMIZER                                         =
echo ================================================================================

REM Copy base files
echo.
echo Copying required files...
robocopy W:\Tools\ENGTools\Dependencies\python . Anonymizer.py /NDL /NFL /NJH /NJS /NP >nul

REM Running script
call python Anonymizer.py
del Anonymizer.py
goto ENDBAT

REM ----------------------------------------------------------------------------
REM Office - Excel
REM ----------------------------------------------------------------------------
:UNHIDEXLS
cls
color 06
echo ================================================================================
echo =          Batch unhide and rename .xls(x) files (Excel)                     =
echo ================================================================================
robocopy W:\Tools\ENGTools\Dependencies\python . unhide_rename_xlsx.py /NDL /NFL /NJH /NJS /NP >nul
call python unhide_rename_xlsx.py
del *.py
goto ENDBAT

:MULTIEXCEL
cls
color 06
echo ================================================================================
echo =                     Split/Merge multilingual .xlsx files                    =
echo ================================================================================
echo   1. Split multilingual .xlsx files
echo   2. Merge multilingual .xlsx files
echo   -------------------------------------------------------------------------------
echo   0. Back
echo.
set /p TASK="Enter your choice [0-2]: "

if "%TASK%"=="" (
    echo [ERROR] No input provided. Please enter a valid number.
    pause
    goto MULTIEXCEL
)

if "%TASK%"=="1" goto SPLITMULTI
if "%TASK%"=="2" goto MERGEMULTI
if "%TASK%"=="0" goto WELCOME

echo [ERROR] Invalid option. Please try again.
pause
goto MULTIEXCEL

:SPLITMULTI
cls
color 06
echo ================================================================================
echo =                           Split multilingual .xlsx files                     =
echo ================================================================================
robocopy W:\Tools\ENGTools\Dependencies\python . split2.py /NDL /NFL /NJH /NJS /NP >nul
call python split2.py
del *.py
goto ENDBAT

:MERGEMULTI
cls
color 06
echo ================================================================================
echo =                         Merge multilingual .xlsx files                     =
echo ================================================================================
robocopy W:\Tools\ENGTools\Dependencies\python . merge2.py /NDL /NFL /NJH /NJS /NP >nul
call python merge2.py
del *.py
goto ENDBAT

REM ============================================================================
REM TOOLS SECTION
REM ============================================================================
:TOOLS
cls
color 0D
echo ================================================================================
echo =                                  Tools                                      =
echo ================================================================================
echo   1.  Flatten/unflatten folder structure
echo   2.  Distribute files by target language code
echo   3.  Extract JSON paths
echo   4.  XPath generator
echo   5.  Remove platform locales
echo   6.  Regin .en files
echo   7.  Static Maxlen Setter
echo   8.  Batch Delete Column CSV
echo   9.  Web-crawling
echo   10. Extract PDF Comments to Excel and CSV
echo   11. Append folder name to files
echo   -------------------------------------------------------------------------------
echo   0. Back
echo.
set /p TASK="Enter your choice [0-10]: "

if "%TASK%"=="" (
    echo [ERROR] No input provided. Please enter a valid number.
    pause
    goto TOOLS
)

if "%TASK%"=="1" goto FLATUNFLAT
if "%TASK%"=="2" goto DISTRIBUTE
if "%TASK%"=="3" goto JSONSTRUCTURE
if "%TASK%"=="4" goto XPATH
if "%TASK%"=="5" goto PLATFORMLOCALES
if "%TASK%"=="6" goto REGIN
if "%TASK%"=="7" goto STATIC
if "%TASK%"=="8" goto CSVCOLUMN
if "%TASK%"=="9" goto WEBCRAWLING
if "%TASK%"=="10" goto EXTRACTPDF
if "%TASK%"=="11" goto FOLDERNAMETOFILES
if "%TASK%"=="0" goto WELCOME

echo [ERROR] Invalid option. Please try again.
pause
goto TOOLS

REM ----------------------------------------------------------------------------
REM Tools - Flatten / Unflatten
REM ----------------------------------------------------------------------------
:FLATUNFLAT
cls
color 0D
echo ================================================================================
echo =                     Flatten / Unflatten Folder Structure                    =
echo ================================================================================
echo   1. Flatten folder structure
echo   2. Unflatten folder structure
echo   -------------------------------------------------------------------------------
echo   0. Back
echo.
set /p TASK="Enter your choice [0-2]: "

if "%TASK%"=="" (
    echo [ERROR] No input provided. Please enter a valid number.
    pause
    goto FLATUNFLAT
)

if "%TASK%"=="1" goto FLAT
if "%TASK%"=="2" goto UNFLAT
if "%TASK%"=="0" goto WELCOME

echo [ERROR] Invalid option. Please try again.
pause
goto FLATUNFLAT

:FLAT
cls
color 0D
echo ================================================================================
echo =                           Flatten folder structure                          =
echo ================================================================================
robocopy W:\Tools\ENGTools\Dependencies\python . flatten_folder_structure.py /NDL /NFL /NJH /NJS /NP >nul
call python flatten_folder_structure.py
del *.py
goto ENDBAT

:UNFLAT
cls
color 0D
echo ================================================================================
echo =                         Unflatten folder structure                          =
echo ================================================================================
robocopy W:\Tools\ENGTools\Dependencies\python . unflatten_folder_structure.py /NDL /NFL /NJH /NJS /NP >nul
call python unflatten_folder_structure.py
del *.py
goto ENDBAT

REM ----------------------------------------------------------------------------
REM Tools - Distribute by TLC
REM ----------------------------------------------------------------------------
:DISTRIBUTE
cls
color 0D
echo ================================================================================
echo =             Distribute files by target language code                        =
echo ================================================================================
robocopy W:\Tools\ENGTools\Dependencies\python . distribute_TLC.py /NDL /NFL /NJH /NJS /NP >nul
call python distribute_TLC.py
del *.py
goto ENDBAT

REM ----------------------------------------------------------------------------
REM Tools - JSON Structure
REM ----------------------------------------------------------------------------
:JSONSTRUCTURE
cls
color 0D
echo ================================================================================
echo =                         Extract JSON paths                                  =
echo ================================================================================
call "C:\Program Files\Analysis Package\bin\extractJSONPaths.cmd" . >JSON_paths.txt
goto ENDBAT

REM ----------------------------------------------------------------------------
REM Tools - XPath generator
REM ----------------------------------------------------------------------------
:XPATH
cls
color 0D
echo ================================================================================
echo =                           XPath generator                                   =
echo ================================================================================
call "C:\Program Files\Analysis Package\bin\XPathGenerator.cmd" . >XPATH_paths.txt
goto ENDBAT

REM ----------------------------------------------------------------------------
REM Tools - Platform locales
REM ----------------------------------------------------------------------------
:PLATFORMLOCALES
cls
color 0D
echo ================================================================================
echo =                           Remove platform locales                                   =
echo ================================================================================
robocopy W:\Tools\ENGTools\Dependencies\python . rename_platform_locales.py /NDL /NFL /NJH /NJS /NP >nul
call python rename_platform_locales.py
del *.py
goto ENDBAT

REM ----------------------------------------------------------------------------
REM Tools - Regin .en files
REM ----------------------------------------------------------------------------
:REGIN
cls
color 0D
echo ================================================================================
echo =                            Regin .en files                                  =
echo ================================================================================
echo   1. .en files to multilingual Excel
echo   2. Multilingual Excel to individual .en files
echo   -------------------------------------------------------------------------------
echo   0. Back
echo.
set /p TASK="Enter your choice [0-2]: "

if "%TASK%"=="" (
    echo [ERROR] No input provided. Please enter a valid number.
    pause
    goto REGIN
)

if "%TASK%"=="1" goto REGINEN
if "%TASK%"=="2" goto REGINEXCEL
if "%TASK%"=="0" goto WELCOME

echo [ERROR] Invalid option. Please try again.
pause
goto REGIN

:REGINEN
cls
color 0D
echo ================================================================================
echo =               .en files to multilingual Excel (Regin)                      =
echo ================================================================================
robocopy W:\Tools\ENGTools\Dependencies\python . Regin_FTC-2-Excel.py /NDL /NFL /NJH /NJS /NP >nul
call python Regin_FTC-2-Excel.py
del *.py
goto ENDBAT

:REGINEXCEL
cls
color 0D
echo ================================================================================
echo =           Multilingual Excel to individual .en files (Regin)              =
echo ================================================================================
robocopy W:\Tools\ENGTools\Dependencies\python . Regin_reverse.py /NDL /NFL /NJH /NJS /NP >nul
call python Regin_reverse.py
del *.py
goto ENDBAT

REM ----------------------------------------------------------------------------
REM Tools - Static Maxlen Setter
REM ----------------------------------------------------------------------------
:STATIC
cls
color 0D
echo ================================================================================
echo =                           Static Maxlen Setter                                   =
echo ================================================================================
robocopy W:\Tools\ENGTools\Dependencies\python . maxlen.py /NDL /NFL /NJH /NJS /NP >nul
call python maxlen.py
del *.py
goto ENDBAT

REM ----------------------------------------------------------------------------
REM Batch Delete Column CSV
REM ----------------------------------------------------------------------------
:CSVCOLUMN
cls
color 0D
echo ================================================================================
echo =                           Batch Delete Column CSV                            =
echo ================================================================================
robocopy W:\Tools\ENGTools\Dependencies\python . csv-delete_column.py /NDL /NFL /NJH /NJS /NP >nul
call python csv-delete_column.py
del *.py
goto ENDBAT

REM ----------------------------------------------------------------------------
REM Web-crawling
REM ----------------------------------------------------------------------------
:WEBCRAWLING
cls
color 0D
echo ================================================================================
echo =                           Web-crawling                                       =
echo ================================================================================
robocopy W:\Tools\ENGTools\Dependencies\python . web-crawler.py /NDL /NFL /NJH /NJS /NP >nul
call python web-crawler.py
del *.py
goto ENDBAT

REM ----------------------------------------------------------------------------
REM Extract PDF Comments to Excel and CSV
REM ----------------------------------------------------------------------------
:EXTRACTPDF
cls
color 0D
echo ================================================================================
echo =               Extract PDF Comments to Excel and CSV                           =
echo ================================================================================
robocopy W:\Tools\ENGTools\Dependencies\python . export_pdf_comments.py /NDL /NFL /NJH /NJS /NP >nul
call python export_pdf_comments.py
del *.py
goto ENDBAT

:FOLDERNAMETOFILES
cls
color 0D
echo ================================================================================
echo =                           Append folder name to files                        =
echo ================================================================================
robocopy W:\Tools\ENGTools\Dependencies\python . RenameFolder2FilesExceptSdlxliff.py /NDL /NFL /NJH /NJS /NP >nul
call python RenameFolder2FilesExceptSdlxliff.py
del RenameFolder2FilesExceptSdlxliff.py
goto ENDBAT

REM ============================================================================
REM File Format Conversions Section
REM ============================================================================
:FILEFORMATCONVERSION
cls
color 0E
echo ================================================================================
echo =                               File Format Conversions                        =
echo ================================================================================
echo   1. SRT to/from VTT
echo   -------------------------------------------------------------------------------
echo   0. Back
echo.
set /p TASK="Enter your choice [0-1]: "

if "%TASK%"=="" (
    echo [ERROR] No input provided. Please enter a valid number.
    pause
    goto FILEFORMATCONVERSION
)

if "%TASK%"=="1" goto SRTVTT
if "%TASK%"=="0" goto WELCOME

echo [ERROR] Invalid option. Please try again.
pause
goto FILEFORMATCONVERSION

REM ----------------------------------------------------------------------------
REM SRT to/from VTT
REM ----------------------------------------------------------------------------
:SRTVTT
cls
color 0E
echo ================================================================================
echo =                         SRT to/from VTT                                         =
echo ================================================================================
echo.
robocopy W:\Tools\ENGTools\Dependencies\python . vtt_srt.py /NDL /NFL /NJH /NJS /NP >nul
call python vtt_srt.py
del *.py
goto ENDBAT


REM ============================================================================
REM COMMON EXIT POINT - ENDBAT
REM ============================================================================
:ENDBAT
echo.
echo ================================================================================
echo =                   Thanks for using ENGTools 0.2                            =
echo ================================================================================
echo   For further information, please visit:
echo     https://languagewire.cloud.xwiki.com/xwiki/bin/view/Delivery/Engineering/ENGTools/
echo.
echo   In case of bug, feature request or update, please contact:
echo     vipa@languagewire.com
echo.
echo Press any key to exit. This batch file will self-delete.
pause >nul
del "%~f0" & exit

REM ----------------------------------------------------------------------------
REM CLOSE
REM ----------------------------------------------------------------------------
:CLOSE
echo.
echo ================================================================================
echo =                   Thanks for using ENGTools 0.2                            =
echo ================================================================================
echo   For further information, please visit:
echo     https://languagewire.cloud.xwiki.com/xwiki/bin/view/Delivery/Engineering/ENGTools/
echo.
echo   In case of bug, feature request or update, please contact:
echo     vipa@languagewire.com
echo.
echo Press any key to exit. This batch file will self-delete.
pause >nul
exit
