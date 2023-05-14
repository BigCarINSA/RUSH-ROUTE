# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 16:23:55 2023

@author: PC
"""
from random import randrange
from algo_plus_court_chemin import plus_court_chemin 

TAILLE_MATRICE = { "EASY"     : (10, 20),
                   "MEDIUM"   : (15, 30),
                   "HARD"     : (20, 40) } 

CARACTERE_CELL = { "trou"     : 0, #Ne pas passer
                   "sol plat" : 1, #Vitesse normal
                   "pente"    : 2, #Vitesse / 2
                   }

POURCENT_TROU_INTERVALLE = (50, 70) #20 à 50 %
POURCENT_PENTE = 50

class Matrice_random:
    '''
    Cette classe permet de générer une matrice aléatoire de taille niveau.
    Algorith utilité : au début, on choisit position de début et fin de la matrice par aleatoire, 
                       et ensuite par chaque fois, on ajoute un pente et verifie si il existe toujours de chemin entre les 2 positions
                       sinon, on le supprime. On arrete quand la matrice a assez de trou 
        :parametre : un String "niveau"
        :return : None, (utilise attribute .matrice pour acceder à la matrice)
    '''
    
    def __init__(self, niveau): #Initiliser le matrice
        self.niveau = niveau
        (self.width, self.height) = TAILLE_MATRICE[ self.niveau ] 
        
        #Enregistrer la superficie de la matrice pour determiner le nombre de trous avec la posibilité: POURCENT_TROU_INTERVALLE
        self.superficie = self.width * self.height
        self.pourcent_de_trou = randrange(POURCENT_TROU_INTERVALLE[0], POURCENT_TROU_INTERVALLE[1])
        self.nb_trous = self.pourcent_de_trou * self.superficie // 100
        
        self.creer_matrice()
        self.ajoute_des_pentes()
        
    def creer_matrice(self):
        '''
        Créer la matrice
        '''
        self.créer_matrice_brut()
        self.posit_début_fin()
        self.algo = plus_court_chemin(self.matrice)
        self.creer_des_trous()
        
    def créer_matrice_brut(self):
        '''
        Initialiser la matrice: on considere que chaque cellule de la matrice est 1 (càd tout le matrice est sol plat) au début
        '''
        self.matrice = []
        for i in range(self.width):
            row = []
            for j in range(self.height):
                row.append(1)
            self.matrice.append(row.copy())             
        
    def posit_début_fin(self):
        '''
        Determiner la position de début et fin de la matrice par aleatoire
        '''
        self.debut = (randrange(0, self.width), randrange(0, self.height))
        self.fin = (randrange(0, self.width), randrange(0, self.height))
        while self.fin == self.debut:  
            self.fin = (randrange(0, self.width), randrange(0, self.height))
        
        self.matrice[ self.debut[0] ][ self.debut[1] ] = -1
        self.matrice[ self.fin[0] ][ self.fin[1] ] = -2   

    def creer_des_trous(self):
        '''
        Ajouter des trous
        '''
        self.way = self.algo.shortest_way
        while self.nb_trous > 0:  #si le nombre de trous n'est pas 0
            
            #Determiner la position du trou par aleatoire
            x_trou, y_trou = randrange(0, self.width), randrange(0, self.height)
            while self.matrice[x_trou][y_trou] != 1: # si cette position est déjà un trou
                x_trou, y_trou = randrange(0, self.width), randrange(0, self.height)
            self.matrice[x_trou][y_trou] = CARACTERE_CELL["trou"]
            
            #Verifie si il existe toujours de chemin pour passer le labyrinth
            if (x_trou, y_trou) not in self.way: #Position du trou ne lie pas à la chemin qu'on a trouvé avant -> chemin existe toujours
                self.nb_trous -= 1
            else: #Sinon
                # on verifie si il existe toujours de chemin
                self.algo.plan = self.matrice
                self.algo.create_heuristice_map()
                self.algo.algo_main()
                algo_way = self.algo.shortest_way
                
                if len(algo_way) > 1: 
                    self.nb_trous -= 1
                    self.way = algo_way
                else: #sinon, on supprime le trou
                    self.matrice[x_trou][y_trou] = CARACTERE_CELL["sol plat"]
                    
    def ajoute_des_pentes(self):
        '''
            Changer quelques cellules de la matrice à un pente
        '''
        for i in range(len(self.matrice)):
            for j in range(len(self.matrice[i])):
                ecq_change_a_pente = randrange(0, 100) < POURCENT_PENTE
                if ecq_change_a_pente and self.matrice[i][j] == CARACTERE_CELL["sol plat"]:
                    self.matrice[i][j] = CARACTERE_CELL["pente"]
         
if __name__ == "__main__":
    mat = Matrice_random("facile")
            
                

