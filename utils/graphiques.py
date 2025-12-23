import numpy as np

class GestionnaireGraphiques:
    def __init__(self, canvas1, canvas2):
        self.canvas1 = canvas1
        self.canvas2 = canvas2
        
        # On prépare les objets lignes pour le futur
        self.line_dev = None
        self.line_alt = None
        self.ax1 = None
        self.ax2 = None

    def preparer_axes(self, t_max, h_max, dev_max):
        """Vide les figures et prépare les axes proprement avant l'animation."""
        # --- Graphique 1 : Déviation ---
        self.canvas1.figure.clf() # On vide TOUT
        self.ax1 = self.canvas1.figure.add_subplot(111)
        self.line_dev, = self.ax1.plot([], [], color='red', lw=2)
        
        self.ax1.set_xlim(0, t_max)
        self.ax1.set_ylim(0, dev_max * 1.1)
        self.ax1.set_title("Déviation cumulée (mm)", pad=15)
        self.ax1.set_xlabel("Temps (s)")
        self.ax1.grid(True, linestyle='--', alpha=0.7)

        # --- Graphique 2 : Altitude ---
        self.canvas2.figure.clf() # On vide TOUT
        self.ax2 = self.canvas2.figure.add_subplot(111)
        self.line_alt, = self.ax2.plot([], [], color='green', lw=2)
        
        self.ax2.set_xlim(0, t_max)
        self.ax2.set_ylim(0, h_max * 1.1)
        self.ax2.set_title("Altitude z(t) (m)", pad=15)
        self.ax2.set_xlabel("Temps (s)")
        self.ax2.grid(True, linestyle='--', alpha=0.7)

        # Empêche les chevauchements de texte
        self.canvas1.figure.tight_layout()
        self.canvas2.figure.tight_layout()
        
        self.canvas1.draw()
        self.canvas2.draw()

    def mettre_a_jour_point(self, t_actuel, dev_actuelle, alt_actuelle):
        """Ajoute le point actuel aux lignes sans redessiner les axes."""
        if self.line_dev and self.line_alt:
            # Mise à jour Déviation
            xdata = np.append(self.line_dev.get_xdata(), t_actuel)
            ydata = np.append(self.line_dev.get_ydata(), dev_actuelle)
            self.line_dev.set_data(xdata, ydata)
            
            # Mise à jour Altitude
            xdata2 = np.append(self.line_alt.get_xdata(), t_actuel)
            ydata2 = np.append(self.line_alt.get_ydata(), alt_actuelle)
            self.line_alt.set_data(xdata2, ydata2)
            
            # On redessine uniquement le contenu (très rapide)
            self.canvas1.draw_idle()
            self.canvas2.draw_idle()