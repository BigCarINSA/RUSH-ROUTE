# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 16:23:55 2023

@author: PC
"""
from random import randint
import csv
import math 
import algo_plus_court_chemin

TAILLE_MATRICE = { "facile"    : (10, 20),
                   "moyen"      : (15, 30),
                   "difficile"  : (20, 40) } 

CARACTERE_CELL = { "trou"     : 0, #Ne pas passer
                   "sol plat" : 1, #Vitesse normal
                   "pente"    : 2, #Vitesse / 2
                   }

POURCENT_TROU_INTERVALLE = (20, 50) #20 à 50 %

class Matrice():
    def __init__(self, niveau):
        #Initiliser le matrice
        self.niveau = niveau
        (self.width, self.height) = TAILLE_MATRICE[ self.niveau ] 
        self.créer_matrice_brut()
        
        self.posit_début_fin()
        self.superficie = self.width * self.height
        self.pourcent_de_trou = randint(POURCENT_TROU_INTERVALLE[0], POURCENT_TROU_INTERVALLE[1])
        self.nb_trous = self.pourcent_de_trou * self.superficie // 100
        
        self.algo = algo_plus_court_chemin(self.matrice)
        self.creer_des_trous()
        self.algo.print_map(self.matrice)
        print(self.algo.way)
        
    def créer_matrice_brut(self):
        self.matrice = []
        for i in range(self.width):
            row = []
            for j in range(self.height):
                row.append(1)
            self.matrice.append(row.copy())                
        
    def posit_début_fin(self):
        self.debut = (randint(0, self.width), randint(0, self.width))
        self.fin = (randint(0, self.width), randint(0, self.width))
        while self.fin == self.debut:  
            self.fin = (randint(0, self.width), randint(0, self.width))
        
        self.matrice[ self.debut[0] ][ self.debut[1] ] = -1
        self.matrice[ self.fin[0] ][ self.fin[1] ] = -2   

    def creer_des_trous(self):
        while self.nb_trous > 0:  
            x_trou, y_trou = randint(0, self.width), randint(0, self.width)
            self.matrice[x_trou][y_trou] = 0
            
            self.algo.plan = self.matrice
            self.algo.reset_distance_map()
            self.algo.algo_main()
            
            if self.algo.way != []:
                self.nb_trous -= 1
            else:
                self.matrice[x_trou][y_trou] = 1
                        
    def créer_file_csv(self):
        with open("maze.csv",'w',newline = '') as f:
            writer =csv.writer(f)
            writer.writerow(self.chemin)
            writer.writerows(self.matrice)
           # print(self.chemin)
         
if __name__ == "__main__":
    mat = Matrice("facile")
            
                

