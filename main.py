import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

from game_play import open_level

import csv
import random
import math

class fenetre():
    def __init__(self):        
        self.racine = tk.Tk()
        
        self.racine.title("Labyrinthe")
        self.icon = tk.PhotoImage(file = "./Image/logo_maze.png")
        self.racine.wm_iconphoto(True, self.icon)

        self.width = 200
        self.height = 300
        self.racine.geometry(f"{self.width}x{self.height}")         
              
        self.fen_level = None
        self.creer_widgets(self.racine)

    def creer_widgets(self,root):      
        #Fenetre secondaire
        self.boutonDessin = tk.Button(root, 
                                      text = "Fenetre graphique", 
                                      height = 3, width = 15)
        self.boutonDessin.bind('<Button-1>', self.ouvrir_level)
        self.boutonDessin.pack(side = tk.TOP)
        
    def ouvrir_level(self, event):
        if (self.fen_level != None) : #cai nay nham ngan can viec nhieu cua so mo len
            self.fen_level.racine.destroy()
        self.fen_level = open_level('Easy - 1', self.racine)
        
if __name__ == "__main__":
    app = fenetre()
    app.racine.mainloop()
