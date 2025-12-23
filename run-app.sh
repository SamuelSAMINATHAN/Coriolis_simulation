#!/bin/bash
echo "[1/3] Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    echo "ERREUR: Python 3 n'est pas installé."
    exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

if [ ! -d "venv" ]; then
    echo "[2/3] Création de l'environnement et installation (patience)..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt
else
    echo "[2/3] Environnement prêt."
    source venv/bin/activate
fi

echo "[3/3] Lancement de Coriolis..."
python3 main.py