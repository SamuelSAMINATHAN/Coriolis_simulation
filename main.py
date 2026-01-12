#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simulations Coriolis - Interface principale
Copyright © Groupe G6E Samuel SAMINATHAN
"""

import tkinter as tk
from tkinter import font
import threading


class SimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulations Coriolis")
        self.root.geometry("700x400")
        self.root.resizable(False, False)
        
        # Configuration du style
        self.root.configure(bg="#f0f0f0")
        
        # Titre principal
        title_font = font.Font(family="Helvetica", size=18, weight="bold")
        title_label = tk.Label(
            self.root,
            text="Choisissez une simulation",
            font=title_font,
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=20)
        
        # Cadre pour les boutons
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Style pour les boutons
        button_font = font.Font(family="Helvetica", size=11)
        button_style = {
            "font": button_font,
            "bg": "#4CAF50",
            "fg": "white",
            "activebackground": "#45a049",
            "activeforeground": "white",
            "padx": 20,
            "pady": 20,
            "relief": tk.RAISED,
            "cursor": "hand2",
            "wraplength": 300
        }
        
        # Bouton 1 - Simulation déviation vers l'est
        btn1 = tk.Button(
            button_frame,
            text="Simulation de la déviation vers l'est\nd'un corps en chute libre\nen fonction de la latitude\net de l'altitude de départ",
            command=self.launch_sim1,
            **button_style
        )
        btn1.pack(side=tk.LEFT, padx=15, expand=True, fill=tk.BOTH)
        
        # Bouton 2 - Expérience Flammarion
        btn2 = tk.Button(
            button_frame,
            text="Expérience de Camille Flammarion\ndepuis le sommet du Panthéon",
            command=self.launch_sim2,
            **button_style
        )
        btn2.pack(side=tk.RIGHT, padx=15, expand=True, fill=tk.BOTH)
        
        # Pied de page avec copyright
        footer_font = font.Font(family="Helvetica", size=9)
        copyright_label = tk.Label(
            self.root,
            text="Copyright © Groupe G6E Samuel SAMINATHAN",
            font=footer_font,
            bg="#f0f0f0",
            fg="#666666"
        )
        copyright_label.pack(pady=10, side=tk.BOTTOM)
    
    def launch_sim1(self):
        """Lance la simulation 1: déviation vers l'est"""
        from utils.sim1 import main as sim1_main
        self.root.withdraw()  # Masquer la fenêtre principale
        sim1_main()
        # Après fermeture de la simulation, on réaffiche le menu
        self.root.deiconify()
    
    def launch_sim2(self):
        """Lance la simulation 2: expérience Flammarion"""
        from utils.sim2 import main as sim2_main
        self.root.withdraw()  # Masquer la fenêtre principale
        sim2_main()
        # Après fermeture de la simulation, on réaffiche le menu
        self.root.deiconify()


def main():
    root = tk.Tk()
    app = SimulationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
