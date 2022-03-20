@echo off

net session >nul 2>&1

if %errorLevel% == 0 (
    echo Pip, setuptools and pyinstaller upgrading
    pip install --upgrade pip
    pip install --upgrade setuptools
    pip uninstall pyinstaller
    pip install https://github.com/pyinstaller/pyinstaller/archive/develop.tar.gz
    echo Now you can run pyinstaller
) else (
    echo You need to run this script as admin
)

pause