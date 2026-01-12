import sys
import numpy as np
import time
import pyvista as pv
from PyQt5 import QtWidgets

from utils.interface import CoriolisInterface
from utils.bille import SimulateurBille
from utils.graphiques import GestionnaireGraphiques

class ControlleurPrincipal:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.view = CoriolisInterface()
        # Le globe affiché dans l'interface est pivoté (voir interface._populate_views),
        # donc on indique au moteur d'inverser le signe de la latitude pour rester cohérent.
        self.moteur = SimulateurBille(flip_latitude=True)
        self.graph = GestionnaireGraphiques(self.view.matplot1, self.view.matplot2)
        
        # Activation de la sélection par clic sur le globe
        self.view.globe_widget.enable_surface_point_picking(
            callback=self.gerer_clic, 
            left_clicking=True, 
            show_point=True
        )
        
        self.setup_ball_view()

    def setup_ball_view(self):
        """Configuration initiale de la vue de simulation (profil XZ)."""
        bw = self.view.ball_widget
        bw.set_background("black")
        
        # 1. Création du sol (Cube pour l'épaisseur visuelle)
        sol_visible = pv.Cube(center=(50, 0, -2), x_length=200, y_length=10, z_length=4)
        bw.add_mesh(sol_visible, color="seagreen", opacity=0.8, label="Surface (Z=0)")
        
        # 2. Création des acteurs billes (sphères)
        self.b_id = bw.add_mesh(pv.Sphere(radius=1.5), color="orange", label="Chute Verticale")
        self.b_co = bw.add_mesh(pv.Sphere(radius=1.5), color="red", label="Chute Coriolis (Amplifiée)")
        
        self.force_arrow = None
        
        # 3. Légende avec correction du texte noir sur fond blanc
        legend = bw.add_legend(bcolor='white', border=True, size=(0.20, 0.25))
        legend.GetEntryTextProperty().SetColor(0, 0, 0)
        
        # 4. Configuration de la caméra 2D
        bw.view_xz() 
        bw.enable_parallel_projection()
        
        # Cadrage par défaut (pour une hauteur de ~84m)
        bw.camera.focal_point = (50, 0, 45)
        bw.camera.position = (50, -150, 45)
        bw.camera.parallel_scale = 60

    def gerer_clic(self, point):
        # 1. Récupération de l'altitude saisie dans l'interface
        h_utilisateur = self.view.input_alt.value()
        
        # 2. Calcul des trajectoires et détails physiques
        t, x_id, z_id, x_co, z_co, force_mag = self.moteur.calculer_donnees(point, h_utilisateur)
        details = self.moteur.obtenir_details_numeriques(point, h_utilisateur)
        
        # 3. Mise à jour dynamique des axes et de la caméra selon l'altitude
        self.graph.preparer_axes(t[-1], h_utilisateur, x_co[-1])
        
        # Ajustement automatique de la vue pour que le sol reste en bas
        bw = self.view.ball_widget
        bw.camera.focal_point = (x_co[-1] / 2, 0, h_utilisateur / 2)
        bw.camera.position = (x_co[-1] / 2, -h_utilisateur * 2, h_utilisateur / 2)
        bw.camera.parallel_scale = h_utilisateur * 0.7
        
        # Affichage des résultats dans le panneau de droite
        self.view.details.setPlainText(
            f"--- CONFIGURATION ---\n"
            f"LATITUDE  : {details['latitude']:.2f}°\n"
            f"HAUTEUR   : {h_utilisateur:.1f} m\n\n"
            f"--- RÉSULTATS RÉELS ---\n"
            f"TEMPS VOL : {details['temps_vol']:.3f} s\n"
            f"DÉVIATION : {details['deviation_mm']:.2f} mm\n\n"
            f"--- VISUEL (x{self.moteur.amplification}) ---\n"
            f"DÉV. SIMU : {x_co[-1]:.2f} m"
        )

        # Nettoyage des tracés précédents
        bw.remove_actor("t_id")
        bw.remove_actor("t_co")

        # 4. Boucle d'animation synchronisée (PyVista + Matplotlib)
        for i in range(len(t)):
            # Mise à jour positions billes
            self.b_id.position = [x_id[i], 0, z_id[i]]
            self.b_co.position = [x_co[i], 0, z_co[i]]
            
            # Mise à jour du vecteur Force (Flèche orange)
            if self.force_arrow: 
                bw.remove_actor(self.force_arrow)
            arrow = pv.Arrow(start=[x_co[i], 0, z_co[i]], direction=[1, 0, 0], scale=force_mag[i])
            self.force_arrow = bw.add_mesh(arrow, color="orange")
            
            # Mise à jour des lignes de trajectoire
            if i > 1:
                pts_id = np.column_stack((x_id[:i], np.zeros(i), z_id[:i]))
                pts_co = np.column_stack((x_co[:i], np.zeros(i), z_co[:i]))
                bw.add_mesh(pv.MultipleLines(points=pts_id), color="yellow", name="t_id", line_width=2)
                bw.add_mesh(pv.MultipleLines(points=pts_co), color="red", name="t_co", line_width=2)

            # Mise à jour point par point des graphiques Matplotlib
            self.graph.mettre_a_jour_point(t[i], x_co[i], z_co[i])

            bw.render()
            self.app.processEvents() # Maintient l'interface fluide
            time.sleep(0.005)

    def executer(self):
        self.view.show()
        self.app.exec_()


def main():
    """Lance la simulation 1"""
    ctrl = ControlleurPrincipal()
    ctrl.executer()


if __name__ == "__main__":
    main()