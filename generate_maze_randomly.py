# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 16:23:55 2023

@author: PC
"""
from random import randrange
import csv
import math 
from algo_plus_court_chemin import plus_court_chemin 

TAILLE_MATRICE = { "EASY"     : (10, 20),
                   "MEDIUM"   : (15, 30),
                   "HARD"     : (20, 40) } 

CARACTERE_CELL = { "trou"     : 0, #Ne pas passer
                   "sol plat" : 1, #Vitesse normal
                   "pente"    : 2, #Vitesse / 2
                   }

POURCENT_TROU_INTERVALLE = (50, 70) #20 à 50 %

class Matrice_random():
    def __init__(self, niveau):
        #Initiliser le matrice
        self.niveau = niveau
        (self.width, self.height) = TAILLE_MATRICE[ self.niveau ] 
        self.créer_matrice_brut()
        
        self.posit_début_fin()
        self.superficie = self.width * self.height
        self.pourcent_de_trou = randrange(POURCENT_TROU_INTERVALLE[0], POURCENT_TROU_INTERVALLE[1])
        self.nb_trous = self.pourcent_de_trou * self.superficie // 100
        
        self.algo = plus_court_chemin(self.matrice)
        self.creer_des_trous()
        print(self.way)
        
    def créer_matrice_brut(self):
        self.matrice = []
        for i in range(self.width):
            row = []
            for j in range(self.height):
                row.append(1)
            self.matrice.append(row.copy())             
        
    def posit_début_fin(self):
        self.debut = (randrange(0, self.width), randrange(0, self.height))
        self.fin = (randrange(0, self.width), randrange(0, self.height))
        while self.fin == self.debut:  
            self.fin = (randrange(0, self.width), randrange(0, self.height))
        
        self.matrice[ self.debut[0] ][ self.debut[1] ] = -1
        self.matrice[ self.fin[0] ][ self.fin[1] ] = -2   

    def creer_des_trous(self):
        self.way = self.algo.way
        while self.nb_trous > 0:  
            
            x_trou, y_trou = randrange(0, self.width), randrange(0, self.height)
            while self.matrice[x_trou][y_trou] != 1:
                x_trou, y_trou = randrange(0, self.width), randrange(0, self.height)
            self.matrice[x_trou][y_trou] = 0
            
            if (x_trou, y_trou) not in self.way:
                self.nb_trous -= 1
            else:
                
                self.algo.plan = self.matrice
                self.algo.reset_distance_map()
                self.algo.algo_main()
                algo_way = self.algo.way
                
                if len(algo_way) > 1: 
                    self.nb_trous -= 1
                    self.way = algo_way
                else: 
                    self.matrice[x_trou][y_trou] = 1
         
if __name__ == "__main__":
    mat = Matrice_random("facile")
            
                

