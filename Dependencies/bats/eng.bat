@echo off
REM ================================================================================
REM eng.bat - Maps drive W: if needed, then copies and calls ENGTools.bat
REM --------------------------------------------------------------------------------
REM This script checks whether W: is already mapped. If not, it attempts to map
REM the drive for the user. Once W: is confirmed, the script copies ENGTools.bat
REM from W: into the current directory and calls it.
REM ================================================================================
setlocal

dir W:\ >nul 2>&1
if %ERRORLEVEL%==0 (
    echo Drive W: is already mounted.
) else (
    echo Attempting to map drive W:...
    net use W: \\languagewire.cph\Global\Engineering\LW\Engineers /persistent:yes >nul 2>&1
    if %ERRORLEVEL%==0 (
        echo Drive W: mapped successfully.
    ) else (
        echo [ERROR] Failed to map drive W:. Please check the path or your credentials.
        exit /b 1
    )
)

set "current_path=%cd%"
set "source_path=W:\Tools\ENGTools\ENGTools.bat"

copy /Y "%source_path%" "%current_path%" >nul
if errorlevel 1 (
    echo [ERROR] Failed to copy "%source_path%" to "%current_path%".
    exit /b 1
)

call "%current_path%\ENGTools.bat"
