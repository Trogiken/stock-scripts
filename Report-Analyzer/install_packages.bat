@echo off
setlocal enabledelayedexpansion

REM Define the list of Python packages you want to install
set "packages=pandas pillow tkinter"

REM Loop through the list of packages and install each one
for %%p in (%packages%) do (
    echo Installing %%p...
    python -m pip install %%p
    if !errorlevel! neq 0 (
        echo Error installing %%p. Please check and try again.
        exit /b 1
    )
)

echo All packages have been installed successfully.

endlocal