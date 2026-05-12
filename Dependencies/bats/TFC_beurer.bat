@echo off
REM ================================================================================
REM TFC_beurer.bat - Okapi Target File Creation Beurer Multilingual
REM --------------------------------------------------------------------------------
REM This script finalizes translated files by:
REM   1) Setting the translation state with proofread_state.py
REM   2) Renaming locales with rename_platform_locales.py
REM   3) Creating final target files using a custom Okapi filter (FPRM)
REM ================================================================================
title Okapi Target File Creation Beurer Multilingual
setlocal
color a
cls

echo ================================================================================
echo =                           Target File Creation                              =
echo ================================================================================
echo.

set "original_path=%cd%"
set "okapiPath=C:\Software\Okapi"

REM Create output folder
mkdir o

REM 2) Rename platform locales
cd /d %original_path%\05_translated

robocopy W:\Tools\ENGTools\Dependencies\python . rename_platform_locales.py /NDL /NFL /NJH /NJS /NP >nul
call python rename_platform_locales.py
del *.py

cd /d %original_path%

echo.
echo Creating final file(s)...
echo.

REM 3) Use a custom filter from 04_configs\*.fprm
call tikal.bat -m %original_path%\05_translated\*.xlf -sd 01_source -od o -ie utf-8 -fc %original_path%\04_configs\*.fprm

robocopy "original_metadata" "o" *.* /NDL /NFL /NJH /NJS /NP >nul

cd /d o

robocopy W:\Tools\ENGTools\Dependencies\python . beurer_merge.py /NDL /NFL /NJH /NJS /NP >nul
call python beurer_merge.py
del *.py

for %%f in (*) do (
    echo %%f | findstr /I /C:"_compiled.xlsx" >nul
    if errorlevel 1 (
       del "%%f"
    )
)


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
