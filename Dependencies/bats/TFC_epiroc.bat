@echo off
REM ================================================================================
REM TFC_epiroc.bat - Okapi Target File Creation for Epiroc
REM --------------------------------------------------------------------------------
REM This script finalizes Epiroc-based translations by:
REM   1) Applying proofreading state, renaming locales
REM   2) Creating final target files with custom Epiroc FPRM
REM   3) Flatten/Unflatten operations to restore original folder structure
REM ================================================================================
title Okapi Target File Creation
setlocal
color a
cls

echo ================================================================================
echo =                           Target File Creation                              =
echo ================================================================================
echo.

set "original_path=%cd%"
set "okapiPath=C:\Software\Okapi"

REM Step 1: Proofreading and rename scripts
robocopy W:\Tools\ENGTools\Dependencies\python %original_path%\04_translated proofread_state.py /NDL /NFL /NJH /NJS /NP >nul
call python %original_path%\04_translated\proofread_state.py %original_path%\04_translated
del %original_path%\04_translated\*.py

cd /d %original_path%\04_translated

robocopy W:\Tools\ENGTools\Dependencies\python . rename_platform_locales.py /NDL /NFL /NJH /NJS /NP >nul
call python rename_platform_locales.py
del *.py

cd /d %original_path%

echo.
echo Creating Final file(s)...
echo.

REM Step 2: Use Epiroc parser from 03_configs\*.fprm
mkdir raw source
call tikal.bat -m %original_path%\04_translated\*.xlf -sd 01_source -od raw -fc 03_configs\*.fprm -ie utf-8

robocopy 01_source source *.* /NDL /NFL /NJH /NJS /NP >nul

REM Step 3: Run custom Epiroc script(s) for .txt
robocopy W:\Tools\ENGTools\Dependencies\python . epiroc_txt.py /NDL /NFL /NJH /NJS /NP >nul
call python epiroc_txt.py
del *.py

mkdir o
mkdir o\FLATTEN
MOVE fixed\*.* o\FLATTEN
rmdir /s /q fixed

cd o
robocopy W:\Tools\ENGTools\Dependencies\python . unflatten_folder_structure.py /NDL /NFL /NJH /NJS /NP >nul
call python unflatten_folder_structure.py
del unflatten_folder_structure.py
rmdir /s /q FLATTEN

REM --------------------- New Section: Zip Each Root Folder in "o" ---------------------
for /d %%D in (*) do (
    echo Zipping folder: %%D
    "C:\Program Files\7-Zip\7z.exe" a "%%D.zip" "%%D\*"
)
REM Delete the now unzipped subfolders, leaving only the zip archives.
for /d %%D in (*) do (
    echo Deleting folder: %%D
    rmdir /s /q "%%D"
)
REM ------------------------------------------------------------------------------------

:CLOSE
echo.
echo ================================================================================
echo =                     Thanks for using ENGTools 0.2                           =
echo ================================================================================
echo For further information, please visit:
echo   https://languagewire.cloud.xwiki.com/xwiki/bin/view/Delivery/Engineering/ENGTools/
echo.
echo In case of bug, feature request or update, please contact:
echo   vipa@languagewire.com
echo.
echo Press any key to exit; mind that the bat file is removed from your working folder
pause >nul
exit
