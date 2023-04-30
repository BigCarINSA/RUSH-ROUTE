# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 16:23:55 2023

@author: PC
"""
from random import randint
import csv
import math 

prob_niveau={"Facile":[50,30],
               "Moyen":[50,30],
               "Difficile":[50,30]}

class Matrice():
    def __init__(self, niveau, maze):
        #Initiliser le matrice
        self.matrice =[]
        self.niveau = niveau
        self.créer_matrice_brut()
        
        self.bloc = maze[0]
        self.carrée_plus_vite=maze[1]
        self.debut = (0,0)
        self.chemin = []
        self.distance = 0
        
        self.posit_début_fin()
        self.créer_matrice_net()
        self.créer_file_csv()
        
    def créer_matrice_brut(self):
        if self.niveau == "Facile":
            for y in range(3):
                ligne = []
                for x in range(3):
                    ligne.append(3)
                self.matrice.append(ligne)
                
        elif self.niveau == "Normal":
            for y in range(15):
                ligne = []
                for x in range(30):
                    ligne.append(3)
                self.matrice.append(ligne)
                
        else:
            for y in range(20):
                ligne = []
                for x in range(40):
                    ligne.append(3)
                self.matrice.append(ligne)
        
    def posit_début_fin(self):
        self.matrice[0][0] = -1
        self.matrice[len(self.matrice)-1][len(self.matrice[0])-1] = -2   

    def créer_matrice_net(self):
        prob_0 = prob_niveau[self.niveau][0]
        prob_1 = prob_niveau[self.niveau][1]
        for i in range(len(self.matrice)):
            for j in range(len(self.matrice[0])):
                if self.matrice[i][j] == 3:
                    if randint(0,100) < prob_0:
                        self.matrice[i][j] = 0
                    if randint(0,100) < prob_1:
                        self.matrice[i][j] = 1
                        
    def créer_file_csv(self):
        with open("maze.csv",'w',newline = '') as f:
            writer =csv.writer(f)
            writer.writerow(self.chemin)
            writer.writerows(self.matrice)
           # print(self.chemin)
         
    def update_matrice(self, i,j):
        if self.matrice[j][i] !=0:
            
            row = self.debut[0]
            col = self.debut[1]
            if abs(i-self.debut[0])==1 and abs(j-self.debut[1])==1:
                self.distance += math.sqrt(abs(self.matrice[col][row]))
            else:
                self.distance += abs(self.matrice[col][row])
            self.matrice[j][i] *= -1
            self.debut= (i,j)
            self.créer_file_csv()
            
    def chemin_passe(self, point):
        if point not in self.chemin:
            self.chemin += point
            self.créer_file_csv()
            
    def delete_item(self):
        self.chemin.pop()
        self.créer_file_csv()
        
    def restart(self):
        self.chemin = []
        self.créer_file_csv()
                

