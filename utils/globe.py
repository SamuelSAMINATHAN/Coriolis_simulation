import pyvista as pv

class GlobeApp:
    def __init__(self):
        self.plotter = pv.Plotter(shape=(1, 2), title="Coriolis Simulation - Multi-view")
        self.plotter.set_background("black")

    def setup_globe(self, texture_path="assets/earth_texture.jpg"):
            self.plotter.subplot(0, 0) # On se met sur la vue de gauche
            try:
                tex = pv.read_texture(texture_path)
                globe_mesh = pv.Sphere(radius=1.0).texture_map_to_sphere()
                # AJOUT : pickable=True pour garantir que le clic est détecté
                self.globe_actor = self.plotter.add_mesh(globe_mesh, texture=tex, pickable=True, name="terre")
            except:
                self.globe_actor = self.plotter.add_mesh(pv.Sphere(radius=1.0), color="blue", pickable=True)

    def setup_zoom_view(self):
        self.plotter.subplot(0, 1)
        self.plotter.add_mesh(pv.Sphere(radius=1.0), color="grey", opacity=0.3, name="sol")
        
        # Création des acteurs pour les billes
        self.b_jaune = self.plotter.add_mesh(pv.Sphere(radius=0.015), color="yellow", name="bj")
        self.b_rouge = self.plotter.add_mesh(pv.Sphere(radius=0.015), color="red", name="br")
        self.plotter.add_text("2. Observation de la déviation", font_size=10)