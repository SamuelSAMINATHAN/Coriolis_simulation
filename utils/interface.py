import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from pyvista import examples
import pyvista as pv
try:
    from pyvistaqt import QtInteractor
except Exception as e:
    QtInteractor = None
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class CoriolisInterface(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Analyse Coriolis - ISEP")
        self._build_ui()
        self._populate_views()

    def _create_titled_widget(self, title, widget):
        """Encapsule un widget avec un titre au-dessus."""
        container = QtWidgets.QWidget()
        v_layout = QtWidgets.QVBoxLayout(container)
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.setSpacing(5)
        
        label = QtWidgets.QLabel(title)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setStyleSheet("""
            font-weight: bold; 
            font-size: 14px; 
            color: #2c3e50; 
            background-color: #ecf0f1; 
            padding: 4px; 
            border-radius: 4px;
        """)
        
        v_layout.addWidget(label)
        v_layout.addWidget(widget)
        return container

    def _build_ui(self):
        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # 1. Globe (Gauche)
        if QtInteractor:
            self.globe_widget = QtInteractor(self)
        else:
            self.globe_widget = QtWidgets.QLabel("Globe manquant")
        
        globe_container = self._create_titled_widget("SÉLECTION DE LA LATITUDE", self.globe_widget)
        layout.addWidget(globe_container, 0, 0, 2, 1)

        # 2. Bille (Centre Haut)
        if QtInteractor:
            self.ball_widget = QtInteractor(self)
        else:
            self.ball_widget = QtWidgets.QLabel("Bille manquante")
            
        ball_container = self._create_titled_widget("SIMULATION LOCALE (ZOOM)", self.ball_widget)
        layout.addWidget(ball_container, 0, 1)

        # 3. Matplotlib Plots (Centre Bas)
        self.matplot1 = FigureCanvas(Figure(figsize=(6, 4.5)))
        self.matplot2 = FigureCanvas(Figure(figsize=(6, 4.5)))
        
        mat_layout = QtWidgets.QHBoxLayout()
        mat_layout.addWidget(self.matplot1)
        mat_layout.addWidget(self.matplot2)
        mat_sub_container = QtWidgets.QWidget()
        mat_sub_container.setLayout(mat_layout)
        
        charts_container = self._create_titled_widget("ANALYSE GRAPHIQUE", mat_sub_container)
        charts_container.setMinimumWidth(int(1825 * 0.5))
        charts_container.setMinimumHeight(int(1050 * 0.2))
        layout.addWidget(charts_container, 1, 1)

        # 4. Paramètres & Détails (Droite)
        # --- AJOUT DU CHAMP ALTITUDE ---
        self.input_alt = QtWidgets.QDoubleSpinBox()
        self.input_alt.setRange(1.0, 10000.0)
        self.input_alt.setValue(84.0)
        self.input_alt.setSuffix(" m")
        self.input_alt.setStyleSheet("font-size: 16px; font-weight: bold; height: 30px;")
        
        self.details = QtWidgets.QTextEdit()
        self.details.setReadOnly(True)
        self.details.setStyleSheet("background-color: #f9f9f9; font-family: 'Courier New'; font-size: 12px;")
        
        # Montage de la colonne de droite
        right_panel = QtWidgets.QWidget()
        right_vbox = QtWidgets.QVBoxLayout(right_panel)
        right_vbox.addWidget(QtWidgets.QLabel("Altitude de départ (h) :"))
        right_vbox.addWidget(self.input_alt)
        right_vbox.addSpacing(10)
        right_vbox.addWidget(QtWidgets.QLabel("Résultats :"))
        right_vbox.addWidget(self.details)
        
        details_container = self._create_titled_widget("PARAMÈTRES & RÉSULTATS", right_panel)
        details_container.setFixedWidth(300)
        layout.addWidget(details_container, 0, 2, 2, 1)

        # Configuration des proportions
        layout.setColumnStretch(0, 6)
        layout.setColumnStretch(1, 8)
        layout.setColumnStretch(2, 0)

        self.setLayout(layout)
        self.resize(1825, 1050)

        globe_container.setMinimumWidth(525)
        globe_container.setMinimumHeight(800)
        ball_container.setMinimumWidth(375)
        ball_container.setMinimumHeight(375)

    def _populate_views(self):
        # Configuration du Globe
        if QtInteractor:
            globe_plotter = self.globe_widget
            globe_plotter.clear()
            
            # 1. Création de la sphère de base
            # On augmente la résolution pour un rendu plus joli
            earth_mesh = pv.Sphere(radius=1.0, theta_resolution=100, phi_resolution=100)
            
            # 2. Préparation des coordonnées de texture
            # inplace=True modifie directement le maillage
            earth_mesh.texture_map_to_sphere(inplace=True)
            
            # --- LA CORRECTION EST ICI ---
            # On fait pivoter la sphère de 180° autour de l'axe X pour remettre le Nord en haut.
            earth_mesh.rotate_x(180)
            # -----------------------------
            
            try:
                # Chargement de la texture
                tex = pv.read_texture(examples.mapfile) if hasattr(examples, "mapfile") else None
                # Ajout du maillage texturé au traceur
                # smooth_shading=True adoucit les facettes
                globe_plotter.add_mesh(earth_mesh, texture=tex, smooth_shading=True)
            except:
                # Fallback si la texture échoue
                globe_plotter.add_mesh(earth_mesh, color='blue')
            
            # 4. Configuration de la caméra
            # On force la caméra à considérer que l'axe Z positif est le "haut"
            globe_plotter.camera.up = (0, 0, 1)
            # Position initiale : un peu décalée pour voir l'Europe/Afrique
            globe_plotter.camera_position = [(3, 1, 1), (0, 0, 0), (0, 0, 1)]
            globe_plotter.reset_camera()

        # Configuration Ball View (vide au départ)
        if QtInteractor:
            self.ball_widget.clear()
            self.ball_widget.reset_camera()
    

    def run(self):
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = CoriolisInterface()
    win.run()
    sys.exit(app.exec_())