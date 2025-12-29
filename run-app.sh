#!/bin/bash

echo "=================================================="
echo "  🌍 Coriolis Simulation - Launcher macOS 🌍"
echo "=================================================="
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Vérifier si UV est installé
echo "[1/4] Vérification de UV..."
if ! command -v uv &> /dev/null; then
    echo "❌ ERREUR: UV n'est pas installé."
    echo ""
    echo "Installation rapide:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo ""
    exit 1
fi
echo "✓ UV détecté"

# Installer les dépendances
echo "[2/4] Installation des dépendances..."
uv sync --all-extras 2>/dev/null || uv pip install -r requirements.txt
echo "✓ Dépendances installées"

# Demander à l'utilisateur ce qu'il veut faire
echo ""
echo "[3/4] Que souhaitez-vous faire ?"
echo "  1) Générer le fichier .app (recommandé)"
echo "  2) Lancer directement l'application"
echo ""
read -p "Choisissez (1 ou 2): " choice

case $choice in
    1)
        echo ""
        echo "[4/4] Génération du fichier .app..."
        echo ""
        
        if [ -f "build_app.sh" ]; then
            chmod +x build_app.sh
            ./build_app.sh
            
            echo ""
            echo "=================================================="
            echo "  ✅ Application générée avec succès!"
            echo "=================================================="
            echo ""
            echo "📍 Localisation: dist/Coriolis_Simulation.app"
            echo ""
            echo "Pour lancer l'application:"
            echo "  • Double-clic sur dist/Coriolis_Simulation.app"
            echo "  • Ou: open dist/Coriolis_Simulation.app"
            echo "  • Ou: ./dist/Coriolis_Simulation.app/Contents/MacOS/Coriolis_Simulation"
            echo ""
        else
            echo "❌ ERREUR: build_app.sh non trouvé"
            exit 1
        fi
        ;;
    2)
        echo ""
        echo "[4/4] Lancement de Coriolis..."
        echo ""
        uv run main.py
        ;;
    *)
        echo "❌ Choix invalide. Abandon."
        exit 1
        ;;
esac