@echo off
title Simulations Coriolis - Generation de l'executable
echo [1/3] Verification de uv...
uv --version >nul 2>nul
if %errorlevel% neq 0 (
    echo ERREUR: uv n'est pas installe. Veuillez installer uv depuis https://github.com/astral-sh/uv
    pause && exit /b
)

if not exist ".venv" (
    echo [2/3] Synchronisation de l'environnement virtuel...
    uv sync
) else (
    echo [2/3] Environnement virtuel pret.
)

echo [3/3] Generation de l'executable...
uv run pyinstaller --onefile --noconsole --add-data "assets;assets" main.py
if %errorlevel% neq 0 (
    echo ERREUR lors de la generation de l'executable.
    pause
) else (
    echo Executable genere avec succes dans le dossier dist\main.exe
    echo Vous pouvez maintenant lancer main.exe directement.
)
pause