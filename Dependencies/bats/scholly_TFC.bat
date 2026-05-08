@echo off

set "original_path=%cd%"
set "okapiPath=C:\Software\Okapi"

mkdir o

robocopy %original_path%\04_translated %original_path%\06_from_QA *.csv /NDL /NFL /NJH /NJS /NP >nul
robocopy W:\Tools\ENGTools\Dependencies\python %original_path%\06_from_QA scholly_merge.py /NDL /NFL /NJH /NJS /NP >nul

cd /d %original_path%\06_from_QA

call python scholly_merge.py
del *.py

cd /d %original_path%

robocopy %original_path%\06_from_QA %original_path%\o *.csv /NDL /NFL /NJH /NJS /NP >nul

robocopy W:\Tools\ENGTools\Dependencies\python %original_path%\o scholly_csv2json.py /NDL /NFL /NJH /NJS /NP >nul

robocopy W:\Tools\ENGTools\Dependencies\python %original_path%\o scholly_json2tmx.py /NDL /NFL /NJH /NJS /NP >nul

cd /d %original_path%\o

call python scholly_csv2json.py
call python scholly_json2tmx.py

del *.py
del *.csv
cd /d %original_path%


echo Press any key to exit; mind that the bat file is removed from your working folder
pause >nul
exit
