import pyvista as pv
import numpy as np


def main():
    """Lance la simulation 2: Expérience de Flammarion"""
    # ==================== PARAMÈTRES PHYSIQUES ====================
    g = 9.81  # Accélération gravitationnelle (m/s²)
    h = 68.0  # Hauteur du Panthéon (m)
    latitude = 48.8462  # Latitude de Paris (degrés)
    omega = 7.2921e-5  # Vitesse de rotation de la Terre (rad/s)

    # ==================== CALCUL DE LA DÉVIATION ====================
    lat_rad = np.radians(latitude)
    deviation_theorique = (2/3) * omega * np.cos(lat_rad) * np.sqrt(2 * h**3 / g)
    deviation_mm = deviation_theorique * 1000 
    amplification = 400

    # ==================== CONFIGURATION PYVISTA ====================
    plotter = pv.Plotter(title="Expérience de Flammarion - Panthéon 1903")
    plotter.set_background('black')

    # === CYLINDRE ===
    cylinder = pv.Cylinder(center=(0, h/2, 0), direction=(0, 1, 0), radius=3, height=h)
    plotter.add_mesh(cylinder, color='lightgray', opacity=0.2, style='wireframe')

    # === SOL ===
    floor = pv.Plane(center=(0, 0, 0), direction=(0, 1, 0), i_size=20, j_size=20)
    plotter.add_mesh(floor, color='green', opacity=0.3)

    # === TRAJECTOIRE ===
    t_chute = np.sqrt(2 * h / g)
    n_points = 200
    t = np.linspace(0, t_chute, n_points)
    y = h - 0.5 * g * t**2
    x = (1/3) * omega * np.cos(lat_rad) * g * t**3
    x_visu = x * amplification
    z = np.zeros_like(t)

    # === TEXTE DES DONNÉES ===
    texte_donnees = f"""EXPÉRIENCE DE FLAMMARION - PANTHÉON (1903)
CALCUL THÉORIQUE :
  Déviation : {deviation_mm:.2f} mm
  Incertitude : ± 0.2 mm
MESURE HISTORIQUE :
  Déviation (Moyenne 169 lancers) : 8.22 mm
  Incertitude : ± 2.5 mm
PARAMÈTRES :
  Hauteur : {h} m
  Latitude : {latitude}°N
(Trajectoire amplifiée ×{amplification} pour visibilité)

COMMANDES :
  [R] Recommencer la simulation
  [Q] Quitter"""
    plotter.add_text(texte_donnees, position='upper_left', font_size=10, color='cyan', font='courier')

    # === VARIABLES D'ÉTAT ===
    bille = pv.Sphere(radius=0.4, center=(0, h, 0))
    bille_actor = plotter.add_mesh(bille, color='yellow')
    trajectoire_points = []
    frame_counter = [0]
    timer_id = [None]
    line_actor = [None]

    # === ANIMATION ===
    def update_animation(step):
        f = frame_counter[0]
        
        if f < n_points:
            # Mise à jour position bille
            current_pos = [x_visu[f], y[f], z[f]]
            bille.points[:] = pv.Sphere(radius=0.4, center=current_pos).points
            
            # Ajout point à la trajectoire
            trajectoire_points.append(current_pos)
            
            # Dessin de la ligne
            if len(trajectoire_points) > 1:
                points = np.array(trajectoire_points)
                line = pv.MultipleLines(points=points)
                
                # Suppression ancienne ligne
                if line_actor[0] is not None:
                    plotter.remove_actor(line_actor[0])
                
                line_actor[0] = plotter.add_mesh(line, color='orange', line_width=4)
            
            frame_counter[0] += 1
        else:
            # Animation terminée, on arrête le timer
            if timer_id[0] is not None:
                plotter.remove_timer_event(timer_id[0])
                timer_id[0] = None
        
        plotter.render()

    def reset_simulation():
        """Réinitialise et relance la simulation"""
        # 1. Arrêter le timer actuel s'il existe
        if timer_id[0] is not None:
            plotter.remove_timer_event(timer_id[0])
            timer_id[0] = None
        
        # 2. Nettoyage des données
        trajectoire_points.clear()
        frame_counter[0] = 0
        
        # 3. Suppression de la ligne
        if line_actor[0] is not None:
            plotter.remove_actor(line_actor[0])
            line_actor[0] = None
        
        # 4. Remise à zéro de la bille
        bille.points[:] = pv.Sphere(radius=0.4, center=(0, h, 0)).points
        
        # 5. Relance du timer
        timer_id[0] = plotter.add_timer_event(max_steps=n_points, duration=30, callback=update_animation)
        
        plotter.render()

    def on_key_press(obj, event):
        key = obj.GetKeySym()
        if key == 'r' or key == 'R':
            reset_simulation()

    # Configuration
    plotter.camera_position = [(40, h/2, 40), (0, h/2, 0), (0, 1, 0)]
    plotter.iren.add_observer('KeyPressEvent', on_key_press)

    # Lancement initial
    timer_id[0] = plotter.add_timer_event(max_steps=n_points, duration=30, callback=update_animation)
    plotter.show()


if __name__ == "__main__":
    main()