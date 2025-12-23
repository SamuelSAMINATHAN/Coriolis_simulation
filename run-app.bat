@echo off
title Simulations Coriolis
echo [1/3] Verification de Python...
python --version >nul 2>nul
if %errorlevel% neq 0 (
    echo ERREUR: Python n'est pas installe.
    pause && exit /b
)

if not exist "venv" (
    echo [2/3] Creation de l'environnement virtuel et installation...
    python -m venv venv
    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip >nul
    pip install -r requirements.txt
) else (
    echo [2/3] Environnement virtuel pret.
    call venv\Scripts\activate.bat
)

echo [3/3] Lancement de la simulation...
python main.py
if %errorlevel% neq 0 pause