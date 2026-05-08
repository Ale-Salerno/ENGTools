@echo off
REM ================================================================================
REM TFC_proof.bat - Okapi Target File Creation for Proofreading
REM --------------------------------------------------------------------------------
REM This script handles finalization for proofread-oriented translations by:
REM   1) Generating final target files from 03_proofread
REM   2) Escaping special characters
REM ================================================================================
title Okapi Target File Creation
setlocal
color a
cls

set "original_path=%cd%"
set "okapiPath=C:\Software\Okapi"

mkdir o

echo ================================================================================
echo =                       Creating Final Proofread Files                         =
echo ================================================================================
echo.

REM Step 1: Create final target files
call tikal.bat -m %original_path%\03_proofread\*.xlf -sd 01_source -od o -ie utf-8

REM Step 2: Escape special characters
robocopy W:\Tools\ENGTools\Dependencies\python %original_path%\o escape_more_than.py /NDL /NFL /NJH /NJS /NP >nul
call python %original_path%\o\escape_more_than.py
del %original_path%\o\*.py

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
