@echo off

set "original_path=%cd%"
set "okapiPath=C:\Software\Okapi"

mkdir 05_to_QA
mkdir 06_from_QA

REM 1) Proofreading state
robocopy W:\Tools\ENGTools\Dependencies\python %original_path%\04_translated proofread_state.py /NDL /NFL /NJH /NJS /NP >nul
call python %original_path%\04_translated\proofread_state.py %original_path%\04_translated
del %original_path%\04_translated\*.py

REM 2) Rename platform locales
cd /d %original_path%\04_translated

robocopy W:\Tools\ENGTools\Dependencies\python . rename_platform_locales.py /NDL /NFL /NJH /NJS /NP >nul
call python rename_platform_locales.py
del *.py

cd /d %original_path%

echo.
echo Creating final file(s)...
echo.

REM 3) Use tikal.bat to create final files
call tikal.bat -m %original_path%\04_translated\*.xlf -fc %original_path%\03_configs\*.fprm -sd 01_source -od 05_to_QA -ie utf-8

REM Escape special characters
robocopy W:\Tools\ENGTools\Dependencies\python %original_path%\05_to_QA escape_more_than.py /NDL /NFL /NJH /NJS /NP >nul
call python %original_path%\05_to_QA\escape_more_than.py
del %original_path%\05_to_QA\*.py

robocopy W:\Tools\ENGTools\Dependencies\fonts %original_path%\05_to_QA *.* /NDL /NFL /NJH /NJS /NP >nul
robocopy W:\Tools\ENGTools\Dependencies\python %original_path%\05_to_QA scholly_qa.py /NDL /NFL /NJH /NJS /NP >nul

cd /d 05_to_QA

call python scholly_qa.py 
del *.py
del *.otf
del *.ttf

cd /d %original_path%

robocopy "05_to_QA" "04_translated" "*.csv" /MOV /XF *.bat /NDL /NFL /NJH /NJS /NP >nul

:CLOSE

echo Press any key to exit; mind that the bat file is removed from your working folder
pause >nul
exit
