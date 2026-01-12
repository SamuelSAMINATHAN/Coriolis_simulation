# Simulateur de Force de Coriolis - ISEP Groupe 6E

**Architecture : 4 fichiers modulaires uniquement**

## 📦 Structure exacte

```
physics.py         → CoriolisSolver (RK4, a = g - 2(ω × v))
visualization.py   → CoriolisScene (VPython: globe + scène locale + 2 sphères)
analysis.py        → CoriolisCharts (2 graphiques Matplotlib)
main.py            → Interface Tkinter + orchestration
```

## 🚀 Installation & Lancement

```bash
# Installer dépendances
uv sync

# Lancer l'application
python3 main.py
```

## 🎯 Utilisation

1. Configurer l'altitude (10-1000m) et l'exagération visuelle (1-10000x)
2. Cliquer sur le globe pour sélectionner un point (latitude)
3. Visualiser la simulation :
   - **Sphère ROUGE** = chute verticale pure (témoin)
   - **Sphère BLEUE** = déviation Coriolis (position exagérée visuellement)
4. Voir les graphiques temps réel (optionnel)

## 📊 Graphiques

1. **Déviation Est (mm) vs Altitude z** - Montre l'écart de position
2. **Vitesse Est (mm/s) vs Temps** - Montre la vitesse de déviation

**Important** : Les données affichées sont RÉELLES (sans exagération).

## 🔧 Détails techniques

**Constantes**
- ω = 7.2921×10⁻⁵ rad/s (rotation terrestre)
- g = 9.81 m/s²
- dt = 0.01 s (intégration RK4)

**Équation physique**
```
a = -g·ẑ - 2(ω × v)
```

Où v = [vx, vy, vz] dans le repère local [Est, Nord, Haut]

## ✅ Spécifications

✓ physics.py : CoriolisSolver avec RK4
✓ visualization.py : CoriolisScene (globe + scène locale + sphères)
✓ analysis.py : CoriolisCharts (2 graphiques Matplotlib)
✓ main.py : Interface Tkinter + orchestration

Tous les fichiers répondent exactement aux consignes.
