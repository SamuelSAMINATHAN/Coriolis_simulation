import numpy as np

class SimulateurCoriolis:
    def __init__(self, omega_val=5.0, g_scale=0.005, radius_earth=1.0):
        # Vecteur rotation de la Terre (autour de l'axe Z par défaut dans PyVista)
        self.omega = np.array([0, 0, omega_val]) # Exagéré pour la visibilité
        self.g_scale = g_scale # Gravité à l'échelle de notre globe
        self.radius_earth = radius_earth # Rayon de notre modèle de Terre

    def calculer_trajectoire_animee(self, depart, dt=0.005, duree_chute_max=2.0, coriolis=True):
        """Calcule chaque point de la trajectoire pour une animation."""
        pos = np.array(depart, dtype=float)
        v = np.array([0.0, 0.0, 0.0], dtype=float)
        
        # Simuler une chute sur une "hauteur" plus significative pour voir l'effet
        # On fait partir la bille d'un peu au-dessus de la surface
        pos_initial_offset = pos * (self.radius_earth + 0.05) # Commence un peu au-dessus
        pos = pos_initial_offset

        trajectoire_points = [pos.copy()]
        
        temps_ecoule = 0.0
        
        while np.linalg.norm(pos) > self.radius_earth * 0.95 and temps_ecoule < duree_chute_max:
            # Vecteur directionnel vers le centre du globe
            direction_vers_centre = -pos / np.linalg.norm(pos)
            accel_gravite = direction_vers_centre * self.g_scale
            
            accel_totale = accel_gravite
            
            if coriolis:
                # Force de Coriolis : -2 * omega x v
                accel_coriolis = -2 * np.cross(self.omega, v)
                accel_totale += accel_coriolis
            
            v += accel_totale * dt
            pos += v * dt
            trajectoire_points.append(pos.copy())
            temps_ecoule += dt
            
        return trajectoire_points