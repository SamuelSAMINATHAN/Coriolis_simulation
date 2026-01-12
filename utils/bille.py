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

    def calculer_donnees(self, point_globe, h_saisie):
        """
        Calcule les trajectoires et les vecteurs forces en fonction 
        de la position sur le globe et de l'altitude choisie.
        """
        # 1. Extraction de la latitude à partir des coordonnées cartésiennes du globe
        x, y, z = point_globe
        # Calcul robuste de la latitude : atan2(z, sqrt(x^2+y^2)).
        base_lat = np.arctan2(z, np.sqrt(x**2 + y**2))
        latitude_rad = -base_lat if self.flip_latitude else base_lat
        
        # 2. Calcul du temps de vol théorique : t = sqrt(2h/g)
        t_vol = np.sqrt(2 * h_saisie / self.g)
        t = np.linspace(0, t_vol, 200)

        # 3. Trajectoire Idéale (Chute parfaitement verticale)
        # Équation : z(t) = h - 1/2 * g * t²
        z_id = h_saisie - 0.5 * self.g * t**2
        x_id = np.zeros_like(t)
        
        # 4. Trajectoire Coriolis (Déviation vers l'Est)
        # Équation simplifiée de la déviation : d = 1/3 * omega * cos(lat) * g * t³
        x_co = (1/3) * self.omega * np.cos(latitude_rad) * self.g * (t**3) * self.amplification
        z_co = z_id.copy()
        
        # 5. Calcul de l'intensité de la force de Coriolis pour l'affichage du vecteur
        # La force de Coriolis est Fc = -2m(Omega x v). 
        # Sa composante Est est proportionnelle à cos(lat) * v_verticale
        # v_verticale = g * t
        force_mag = 2 * self.omega * np.cos(latitude_rad) * (self.g * t) * (self.amplification * 10)
        
        return t, x_id, z_id, x_co, z_co, force_mag

    def obtenir_details_numeriques(self, point_globe, h_saisie):
        """Calcule les résultats réels (non amplifiés) pour l'affichage texte."""
        x, y, z = point_globe
        base_lat_deg = np.degrees(np.arctan2(z, np.sqrt(x**2 + y**2)))
        lat_deg = -base_lat_deg if self.flip_latitude else base_lat_deg
        
        t_vol = np.sqrt(2 * h_saisie / self.g)
        
        # Calcul de la déviation réelle en mètres (sans amplification)
        # $d = \frac{1}{3} \omega \cos(\phi) g t^3$
        dev_finale_reelle = (1/3) * self.omega * np.cos(np.radians(lat_deg)) * self.g * (t_vol**3)
        
        return {
            "latitude": lat_deg,
            "temps_vol": t_vol,
            "deviation_mm": dev_finale_reelle * 1000  # Conversion en millimètres
        }