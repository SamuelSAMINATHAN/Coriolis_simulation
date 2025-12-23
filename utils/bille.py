import numpy as np

class SimulateurBille:
    def __init__(self, flip_latitude=False):
        # Constantes physiques
        self.g = 9.81                  # Accélération de la pesanteur (m/s²)
        self.omega = 7.2921e-5         # Vitesse angulaire de la Terre (rad/s)
        self.R_terre = 6371000         # Rayon moyen de la Terre (m)
        
        # Paramètres de simulation
        self.amplification = 100       # Facteur pour rendre la déviation visible à l'œil
        # Si True, on inverse le signe de la latitude (utile si le maillage du globe
        # a l'axe Z inversé par rapport à la convention géographique)
        self.flip_latitude = flip_latitude

    def _equations_mouvement(self, state, latitude_rad):
        """
        Définit les équations différentielles du système.
        state = [x, vx, z, vz] : position et vitesse en (x, z)
        
        Équations:
        dx/dt = vx
        dvx/dt = -2*omega*cos(lat)*vz  (accélération due à Coriolis, positive vers l'Est)
        dz/dt = vz
        dvz/dt = -g  (accélération gravitationnelle)
        """
        x, vx, z, vz = state
        
        dxdt = vx
        dvxdt = -2 * self.omega * np.cos(latitude_rad) * vz
        dzdt = vz
        dvzdt = -self.g
        
        return np.array([dxdt, dvxdt, dzdt, dvzdt])
    
    def _rk4_step(self, state, latitude_rad, dt):
        """
        Exécute une étape de Runge-Kutta d'ordre 4.
        Retourne l'état au temps t + dt.
        """
        k1 = self._equations_mouvement(state, latitude_rad)
        k2 = self._equations_mouvement(state + 0.5 * dt * k1, latitude_rad)
        k3 = self._equations_mouvement(state + 0.5 * dt * k2, latitude_rad)
        k4 = self._equations_mouvement(state + dt * k3, latitude_rad)
        
        return state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
    
    def _integrer_trajectoire(self, h_saisie, latitude_rad, nb_points=200):
        """
        Intègre la trajectoire avec Coriolis par RK4.
        Retourne les tableaux t, x, z, vz (vitesse verticale pour le calcul de force).
        """
        # Temps de vol estimé
        t_vol = np.sqrt(2 * h_saisie / self.g)
        dt = t_vol / (nb_points - 1)
        
        # État initial : [x=0, vx=0, z=h, vz=0]
        state = np.array([0.0, 0.0, h_saisie, 0.0])
        
        # Listes pour stocker la trajectoire
        t_array = [0.0]
        x_array = [state[0]]
        z_array = [state[2]]
        vz_array = [state[3]]
        
        # Intégration RK4
        for i in range(1, nb_points):
            state = self._rk4_step(state, latitude_rad, dt)
            t_array.append(i * dt)
            x_array.append(state[0])
            z_array.append(state[2])
            vz_array.append(state[3])
            
            # Arrêt si la bille a atteint le sol
            if state[2] <= 0:
                t_array.append(t_vol)
                x_array.append(state[0])
                z_array.append(0.0)
                vz_array.append(state[3])
                break
        
        return np.array(t_array), np.array(x_array), np.array(z_array), np.array(vz_array)

    def calculer_donnees(self, point_globe, h_saisie):
        """
        Calcule les trajectoires et les vecteurs forces en fonction 
        de la position sur le globe et de l'altitude choisie.
        Utilise l'intégrateur RK4 pour la trajectoire avec Coriolis.
        """
        # 1. Extraction de la latitude à partir des coordonnées cartésiennes du globe
        x, y, z = point_globe
        # Calcul robuste de la latitude : atan2(z, sqrt(x^2+y^2)).
        base_lat = np.arctan2(z, np.sqrt(x**2 + y**2))
        latitude_rad = -base_lat if self.flip_latitude else base_lat
        
        # 2. Calcul du temps de vol théorique : t = sqrt(2h/g)
        t_vol = np.sqrt(2 * h_saisie / self.g)
        t = np.linspace(0, t_vol, 200)

        # 3. Trajectoire Idéale (Chute parfaitement verticale - analytique)
        # Équation : z(t) = h - 1/2 * g * t²
        z_id = h_saisie - 0.5 * self.g * t**2
        x_id = np.zeros_like(t)
        
        # 4. Trajectoire Coriolis (Déviation vers l'Est) - Intégration RK4
        t_rk4, x_co_real, z_co_real, vz_co = self._integrer_trajectoire(h_saisie, latitude_rad, 200)
        
        # Interpolation pour avoir les mêmes points temporels que t
        x_co = np.interp(t, t_rk4, x_co_real)
        z_co = np.interp(t, t_rk4, z_co_real)
        vz_interp = np.interp(t, t_rk4, vz_co)
        
        # Application du facteur d'amplification pour la visualisation
        x_co_visual = x_co * self.amplification
        
        # 5. Calcul de l'intensité de la force de Coriolis pour l'affichage du vecteur
        # La force de Coriolis est Fc = -2m(Omega x v). 
        # Sa composante Est est proportionnelle à cos(lat) * v_verticale
        force_mag = 2 * self.omega * np.cos(latitude_rad) * np.abs(vz_interp) * (self.amplification * 10)
        
        return t, x_id, z_id, x_co_visual, z_co, force_mag

    def obtenir_details_numeriques(self, point_globe, h_saisie):
        """Calcule les résultats réels (non amplifiés) pour l'affichage texte."""
        x, y, z = point_globe
        base_lat_deg = np.degrees(np.arctan2(z, np.sqrt(x**2 + y**2)))
        lat_deg = -base_lat_deg if self.flip_latitude else base_lat_deg
        latitude_rad = np.radians(lat_deg)
        
        # Intégration RK4 pour obtenir la déviation réelle
        t_rk4, x_co_real, z_co_real, vz_co = self._integrer_trajectoire(h_saisie, latitude_rad, 200)
        
        # La déviation finale est la dernière valeur non amplifiée
        dev_finale_reelle = x_co_real[-1]
        
        # Temps de vol réel (quand la bille atteint z=0)
        t_vol = t_rk4[-1]
        
        return {
            "latitude": lat_deg,
            "temps_vol": t_vol,
            "deviation_mm": dev_finale_reelle * 1000  # Conversion en millimètres
        }