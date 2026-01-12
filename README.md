# Simulations Coriolis

Modélisation interactive de la déviation vers l'Est d'un objet en chute libre selon la latitude et l'altitude, basée sur l'intégrateur RK4 avec la force de Coriolis.

## Installation

### 1. Installer UV

UV est un gestionnaire de paquets et d'environnements Python rapide. Il gère automatiquement Python et les dépendances.

**Windows (PowerShell en mode administrateur):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Vérifiez l'installation :
```bash
uv --version
```

### 2. Générer l'exécutable

**Windows:** Double-cliquez sur `run-app.bat`

**macOS/Linux:** Depuis un terminal
```bash
chmod +x run-app.sh
./run-app.sh
```

Ces scripts :
- Vérifient que UV est installé
- Synchronisent l'environnement virtuel avec les dépendances
- Génèrent l'exécutable `main.exe` (Windows) ou `main` (macOS/Linux) dans le dossier `dist/`

### 3. Lancer l'application

Une fois l'exécutable généré, lancez-le directement :
- **Windows:** Double-cliquez sur `dist\main.exe`
- **macOS/Linux:** `./dist/main`

### Installation manuelle (alternative)

Si vous préférez installer manuellement :
```bash
uv sync
uv run python main.py
```

## À propos

Ce projet simule la déviation vers l'Est d'un objet en chute libre due à l'effet Coriolis. L'application propose deux simulations:

1. **Simulation générale**: Sélectionnez une latitude sur le globe, ajustez l'altitude, visualisez la trajectoire et obtenez la déviation en mm
2. **Expérience Flammarion**: Simulation historique du Panthéon (Paris, 48.86°N, 84m)

Le calcul utilise l'intégrateur RK4 pour résoudre les équations différentielles du mouvement avec Coriolis.

## Utilisation

1. Lancez l'application
2. Sélectionnez une simulation (déviation Est ou Expérience Flammarion)
3. Cliquez sur le globe pour choisir une latitude
4. Ajustez l'altitude (m) via le champ de droite
5. Visualisez:
   - Trajectoires animées (rouge = Coriolis, bleu = chute verticale)
   - Graphiques Déviation(t) et Altitude(t)
   - Résultats: latitude, temps vol, déviation en mm

## Architecture

**Structure du projet:**
```
Coriolis_Simulation/
├── main.py                 # Menu principal (Tkinter)
├── run-app.bat            # Lanceur Windows
├── run-app.sh             # Lanceur macOS/Linux
├── requirements.txt       # Dépendances pip
├── README.md              # Documentation
└── utils/
    ├── __init__.py
    ├── interface.py       # UI PyQt5/PyVista (globe 3D, graphiques)
    ├── bille.py          # Intégrateur RK4 (équations du mouvement)
    ├── sim1.py           # Contrôleur simulation déviation Est
    ├── sim2.py           # Contrôleur expérience Flammarion
    ├── graphiques.py     # Gestion graphiques Matplotlib
    ├── globe.py          # Utilitaires visualisation globe
    └── physique.py       # Modèle physique simplifié
```

**Technologies:**
- NumPy: calculs numériques et intégrateur RK4
- PyQt5/PyVista: interface 3D interactive
- Matplotlib: graphiques scientifiques temps réel
- Tkinter: menu principal

## Physique

**Équations du mouvement (repère local en chute):**

d²x/dt² = -2Ω cos(λ) dz/dt

d²z/dt² = -g

Où Ω = 7.2921×10⁻⁵ rad/s, λ = latitude, g = 9.81 m/s²

**Résolution:** Intégrateur RK4 sur 4 états [x, vx, z, vz]

**Validation analytique:**

x(t) = (1/3) Ω cos(λ) g t³

## Validation

**Cas de test: Paris (Panthéon)**
- Latitude: 48.86°N
- Altitude: 84 m
- Temps vol: 4.14 s
- Déviation théorique: 6.23 mm
- Déviation RK4: 6.23 mm (erreur < 0.1%)

Remarque: La déviation est amplifiée ×100 pour la visualisation (sinon invisible)

## Développement

**Modifier les constantes (utils/bille.py):**
```python
self.g = 9.81              # gravité (m/s²)
self.omega = 7.2921e-5     # vitesse rotation Terre (rad/s)
self.amplification = 100   # facteur visuel
```

## Limitations

- Modèle 2D local (pas de 3D)
- Seule la déviation Est (composante horizontale)
- Pas de frottement atmosphérique
- Latitudes modérées (|λ| < 85°)
- Chutes courtes (< 10 secondes)

## Dépannage

**Erreur de dépendance graphique (Exit 139):**
```bash
pip install --force-reinstall pyvista
```

## Auteurs

Samuel SAMINATHAN - Groupe G6E (ISEP)

MIT License © 2025
# Coriolis_simulation
