import tkinter as tk
from tkinter import messagebox
from math import sqrt
from algo_plus_court_chemin import plus_court_chemin
from generate_maze_randomly import Matrice_random

import csv
import pandas as pd

#Constantes
COMPLETION_RATE = 80 #le pourcentage qu'il faut passer pour compter compté comme réussi

SQUARE_START_VALUE = -1 #value de position "start" dans le fiche csv du labyrinthe
SQUARE_END_VALUE = -2 #value de position "end" dans le fiche csv du labyrinthe

PLAYER_DATA = './data/player_data.csv' #lien de fichier csv contenant data de joueur

FONT = "Century Gothic" #font principal de GUI
BG_COLOR = "white"
COLOR = { "white"        :  "#FFFFFF",
          "yellow"       :  "#FFD966",       "light yellow" :   "#F3DEBA",       "lighter yellow" : "#F0E9D2",
          "light green"  :  "#ABC4AA",       "dark green"   :   "#678983",
          "red"          :  "#EA5455",       "light red"    :   "#F0997D",       "dark red"       : "#A9907E",
          "dark blue"    :  "#114C5E", 
          "brown"        :  "#675D50"
        }

HEIGHT_WINDOW = 600
PROC_BAR_HEIGHT = 390
PROC_BAR_WIDTH = 180
SIZE_MOVING_BUTTON = 45

MOVING_KEY = {  'Q' : (-1, -1) ,    'q' : (-1, -1) ,
                'W' : (-1,  0) ,    'w' : (-1,  0) ,
                'E' : (-1,  1) ,    'e' : (-1,  1) ,
                'A' : ( 0, -1) ,    'a' : ( 0, -1) ,
                'D' : ( 0,  1) ,    'd' : ( 0,  1) ,
                'Z' : ( 1, -1) ,    'z' : ( 1, -1) ,
                'S' : ( 1,  0) ,    's' : ( 1,  0) ,
                'C' : ( 1,  1) ,    'c' : ( 1,  1) ,
                }

BACKGROUND_MUSIC = "./Sound/background_music.mp3"
SOUND_EFFECT = { "button click" : "./Sound/button_click_sound.mp3",
                 "move"         : "./Sound/moving_sound.mp3",
                 "success"      : "./Sound/success_sound.mp3",
                 "fail"         : "./Sound/fail_sound.mp3",}

#Global variables

g_sound_id = {}
g_time_playing = 0 #Pour faire un Timer
g_level_difficulty = "EASY" #Le difficulté du labyrinthe
g_level = "1" #Le niveau dans ce difficulté
g_level_window = None #Pour enregistrer l'objet LevelWindow
g_level_map = [[]] #2D liste contenant info de ce labyrinthe
g_root = None

class FinishPopUp: 
    '''
    creer un PopUp qui apparaît  après le joueur fini le labyrinthe pour montrer le score
        :parametre: - racine: la fenetre de jeu
                    - nombre: le distance que le joueur a gagné, 
                    - un liste de tuples: correspond à ce distance
    '''
    def __init__(self, root, distance_player, way_player):  #initialiser les variables
        #variables relatives au resultat de labyrinthe 
        algo = plus_court_chemin(g_level_map)
        self.result_distance = algo.shortest_distance
        self.result_way = algo.shortest_way
        self.fini_pos = (algo.x_end, algo.y_end)
        
        #variables relatives à la progression du joueur
        self.distance_player = distance_player 
        self.way_player = way_player
        self.comparison_distance = (2-self.distance_player / self.result_distance) * 100
        self.update_get_player_data() #Lire des informations relatives à la progression plus ancienne
        
        #variables de GUI
        self.fen_level = root
        self.bg_color = COLOR["lighter yellow"]
        self.bg_button = COLOR["light green"]
        self.active_bg_button = COLOR["dark green"]
        self.fini_fen = tk.Frame(root, bg = self.bg_color, 
                                 highlightbackground = COLOR["dark blue"],
                                 highlightthickness = 3)
       
    def update_get_player_data(self): #Enregistrer ce resultat dans le fichier csv
        df = pd.read_csv(PLAYER_DATA, sep = ';', index_col='level')
        playing_level = g_level_difficulty + " - " + g_level
        df['played_times'][playing_level] += 1
        self.played_times = df['played_times'][playing_level]
        
        self.highest_score = df['high_score'][playing_level]
        if (self.highest_score < self.comparison_distance) or (self.highest_score == 0):
            df['high_score'][playing_level] = self.comparison_distance
            self.highest_score = self.comparison_distance
            
        df.to_csv("./data/player_data.csv", sep= ';')
                       
    def draw_widgets(self): #dessiner les widgets
        #dessiner le titre
        if self.comparison_distance < COMPLETION_RATE: #Si le joueur satisfait la condition pour passer
            titre_text = "TRY SHORTER WAY!"
            g_root.play_sound("fail")
        else:
            titre_text = "YOU FOUND THE SHORTEST!"
            g_root.play_sound("success")
        self.title = tk.Label(self.fini_fen, font = (FONT, 30, 'bold'),
                                text = titre_text , bg = self.bg_color)
        
        #Écrire des textes pour informer la réalisations de joueur
        self.text_frame = tk.LabelFrame(self.fini_fen, bg = self.bg_color, bd = 0)
        
        font_text = (FONT, 15)
        self.text_player_score = tk.Label(self.text_frame, font = font_text, bg = self.bg_color,
                                          text = f"Your distance : {self.distance_player:.2f}")
        self.text_player_score.grid(column=0, row=0, sticky=tk.W)
        
        self.text_result_distance = tk.Label(self.text_frame, font = font_text, bg = self.bg_color,
                                          text = f"Expected distance : {self.result_distance:.2f}")
        self.text_result_distance.grid(column=0, row=1, sticky=tk.W)
        
        self.text_comparison = tk.Label(self.text_frame, font = font_text, bg = self.bg_color,
                                          text = "Completion rate: "  + str(round(self.comparison_distance)) + " % ")
        self.text_comparison.grid(column=0, row=2, sticky=tk.W)
        
        self.text_result_distance = tk.Label(self.text_frame, font = font_text, bg = self.bg_color,
                                          text = f"High score : {self.highest_score:.0f} %")
        self.text_result_distance.grid(column=0, row=3, sticky=tk.W)

        #Dessiner les 3 buttons: Quit / Rejouer / Afficher le résultat
        self.buttons_frame = tk.Frame(self.fini_fen, bg = self.bg_color)
        
        font_text = (FONT, 16)
        button_height = 1; button_width = 10
        self.button_quit = tk.Button(self.buttons_frame,
                                     height = button_height,  width = button_width,
                                     text = "Exit", font = font_text,
                                     bg = self.bg_button, activebackground = self.active_bg_button,  
                                     fg = COLOR["dark blue"], activeforeground= COLOR["dark blue"],
                                     command = self.fen_level.destroy)
        self.button_quit.grid( column = 0, row = 0, padx = 5)

        self.button_restart = tk.Button(self.buttons_frame,
                                     height = button_height,  width = button_width,
                                     text = "Restart" , font = font_text,
                                     bg = self.bg_button, activebackground = self.active_bg_button,  
                                     fg = COLOR["dark blue"], activeforeground= COLOR["dark blue"],
                                     command = self.restart_level)
        self.button_restart.grid( column = 1, row = 0, padx = 5)
        
        self.button_show_map = tk.Button(self.buttons_frame,
                                     height = button_height,  width = button_width,
                                     text = "Show result", font = font_text,
                                     bg = self.bg_button, activebackground = self.active_bg_button,  
                                     fg = COLOR["dark blue"], activeforeground= COLOR["dark blue"], disabledforeground = COLOR["brown"],
                                     command = self.show_result_map)
        
        if (self.comparison_distance < 80) and (self.played_times < 3): #la condition pour utiliser le bouton "Afficher le résultat"
            self.button_show_map.config(state = 'disabled', bg = COLOR["dark red"])
        self.button_show_map.grid( column = 2, row = 0, padx = 5)

        #Organiser tous widgets dans ce PopUp
        self.map_frame = tk.Frame(self.fini_fen, 
                                  highlightbackground = COLOR["dark blue"], highlightthickness = 2)
        self.result_map = GraphicPlayingMap(self.map_frame, self.way_player) 

        self.title.pack(side = tk.TOP, fill = 'x', anchor = 'center', pady = 20)         
        self.map_frame.pack(side = tk.RIGHT, padx = (0,15), pady = (0,10))
        self.buttons_frame.pack(side = tk.BOTTOM, padx= 10, pady = (5,10)) 
        self.text_frame.pack(side = tk.LEFT, padx= (30,0), pady = (0,20), anchor = tk.W)

    def place_fenetre(self): #Trouver la position centre de l'écran et dessiner le PopUp
        self.draw_widgets()
        
        #Trouver le centre de fenetre pour positioner le PopUp
        self.fini_fen.update()       
        self.width = self.fini_fen.winfo_reqwidth()
        self.heigth = self.fini_fen.winfo_reqheight()
        
        self.x_centre = self.fen_level.winfo_reqwidth() / 2
        self.y_centre = self.fen_level.winfo_reqheight() / 2
        
        self.fini_fen.place( x = (self.x_centre - self.width / 2) , y = (self.y_centre - self.heigth / 2) )
        
    def restart_level(self): #callback pour le bouton "Rejouer"
        g_root.play_sound("button click")
        g_level_window.restart()    
        
    def show_result_map(self): #callback pour le bouton "Afficher le résultat"
        g_root.play_sound("button click")
        self.result_map.draw_way(self.result_way, COLOR["red"])

class Character: 
    '''
    Un class du personnage qui est controlé par le joueur
        :parametre: - tuple: la position au début du personnage, 
                    - le racine (c'est la carte graphique), 
                    - number: le taille de chaque cellular de la carte (pour determine la taille du personnage)  
    '''

    def __init__(self, start_pos, map_graphic_root, map_square_size): #initialiser les variables    
        #le position au début du personnage est la position "start"     
        self.pos_x = start_pos[0]
        self.pos_y = start_pos[1] 
        
        #Obtenir la taille graphique de chaque carré de la carte dessinée pour déterminer la taille du personnage
        self.square_size = map_square_size     
        self.height = 0.7 * self.square_size
        self.width = self.height 

        self.root = map_graphic_root #le racine est la carte graphique
        
    def draw(self, pos): 
        '''
        Dessiner le personnage selon sa position pos_x et pos_y
            :parametre: - tuple: indique la position du personnage
        '''
        #position graphique (Oxy)
        graph_pos_x = (pos[0] + 1/2) * self.square_size
        graph_pos_y = (pos[1] + 1/2) * self.square_size        
        self.charac = self.root.create_oval((graph_pos_y - self.width / 2, graph_pos_x - self.height / 2),
                                            (graph_pos_y + self.width / 2, graph_pos_x + self.height / 2),
                                            fill = COLOR["yellow"], 
                                            width = 1, outline = COLOR["dark blue"])
        
    def update_pos(self, vari_pos): 
        '''
        Mise à jour la position après appuyer sur un bouton de déplacement
            :parametre: - tuple: indique la variation de la position selon le button appuyé
        '''
        g_root.play_sound("move")
        self.pos_x += vari_pos[0]
        self.pos_y += vari_pos[1]
        self.root.move(self.charac, vari_pos[1] * self.square_size, vari_pos[0] * self.square_size)

class GraphicPlayingMap: 
    '''
    Un class de la carte graphique qui est contenue dans la fenêtre de jeu
        :parametre: - racine: la fenêtre de jeu
                    - way = un list: indique le chemin que le joueur a joué 
                    (si on dessine la carte graphique pour le joueur de jouer, way = [],
                     si on dessine la carte graphique pour afficher le resultat dans le FinishPopUp, way = le chemin correspondant pour montrer)
    '''
    def __init__(self, racine, way): #initialiser les variables
        #Variables relatives au labyrinthe à jouer
        self.map_height = len(g_level_map)
        self.map_width = len(g_level_map[0])
        self.get_start_end()
        
        #On veut dessiner le carte 2 fois, l'un pour le joueur de jouer (donc au debut, way = [])
        #Et l'autre pour afficher le résultat à la fin (way est le chemin que le joueur a joué, donc, way != []) 
        self.way = way 
        if self.way == []:
            self.way = [self.start_pos] #Au début, le personnage est à la position "start"
        self.distance = 0.0
           
        self.calcul_square_size() #la taille du labyrinthe de chaque niveau est différent mais HEIGHT_WINDOW est constante, donc la taile de chaque carré du carte est différent 

        self.color_square = [COLOR["dark red"], COLOR["light yellow"], COLOR["light green"], COLOR["light red"], COLOR["light red"]]        
        
        #Variables de GUI
        self.fen_level = racine
        self.graph = tk.Canvas( self.fen_level, 
                                height = self.square_size * self.map_height+self.border_cell,  #plus 1 pour le "border"
                                width = self.square_size * self.map_width+self.border_cell,
                                highlightthickness=0)
        self.way_graph = [] #Enregistrer les "id" des droits du chemin déssinés dans le canevas pour controler après, comme "delete"
        self.player_charac = Character(self.start_pos, self.graph, self.square_size)           
        self.draw(self.start_pos)
    
    def get_start_end(self): #Obternir la position "start" et "end"
        for row in range(self.map_height):
            for col in range(self.map_width):
                if g_level_map[row][col] == SQUARE_START_VALUE: self.start_pos = (row, col)
                if g_level_map[row][col] == SQUARE_END_VALUE: self.end_pos = (row, col)  
     
    def calcul_square_size(self): #Calculer la taille de chaque cellule de la carte qu'on veut dessiner
        self.square_size = (HEIGHT_WINDOW - 10) // self.map_height #20 vient du "padding" du carte
        
        if self.way[-1] == self.end_pos: #si cette carte est utilisé pour le PopUp à la fin, donc, elle est plus petite
            self.square_size *= 0.3
            
        self.padding_from_border = self.square_size // 3
        if self.padding_from_border > 8: self.padding_from_border = 8
        
        self.border_cell = 1
        if self.square_size < 8: #si la taille de la carte est trop petite, on ne veux pas dessiner le "border" de chaque carré
            self.border_cell = 0
    
    def get_pos_graphic(self, pos_x, pos_y): 
        '''
        Determiner la position correspondant dans le canevas
            :parametre: - les nombres pos_x, pos_y: position
            :return: - tuple: la position correspondant dans le canevas
        '''
        return( pos_x * self.calcul_square_size, pos_y * self.calcul_square_size )     
        
    def draw_map(self): #dessiner la carte
        for pos_x in range(self.map_height):
            for pos_y in range(self.map_width):
                cell_color = self.color_square[ g_level_map[pos_x][pos_y] ]
                
                self.graph.create_rectangle(( pos_y * self.square_size, pos_x * self.square_size), 
                                            ( (pos_y+1) * self.square_size, (pos_x+1) * self.square_size),
                                            fill = cell_color,
                                            width = self.border_cell, outline = COLOR["brown"])   
             
    def draw_way_index(self, ind, way, color): 
        '''
        Dessiner un droite connectant 2 carré qui représente le chemin que le joueur a passé 
            :parametre: - ind: index de la deplacement que on veut dessiner dans le liste de chemin: way
                        - way: le chemin que le joueur a joué
                        - color (#XXXXXX): la couleur du droite
        '''
        
        #Obtenir la position des 2 carrés consécutives dans le variales "way" du joueur
        pos_x, pos_y = way[ind]
        pre_pos_x, pre_pos_y = way[ind-1]
        id_line = self.graph.create_line( (pos_y+1/2)*self.square_size, (pos_x+1/2)*self.square_size ,
                                            (pre_pos_y+1/2)*self.square_size, (pre_pos_x+1/2)*self.square_size ,
                                            width = 2, fill = color)
        self.way_graph.append(id_line) 

    def draw_way(self, way, color): #draw le chemin du joueur
        for i in range(1, len(way)):
            self.draw_way_index(i, way, color)

    def draw(self, pos_char): #dessiner tout ce qui concerne à la carte graphique: la carte, le personnage, le chemin
        self.draw_map()
        if self.way[-1] != self.end_pos:
            self.player_charac.draw(pos_char)
        self.draw_way(self.way, COLOR["dark green"])
        self.graph.pack(padx= self.padding_from_border, pady= self.padding_from_border)

    def check_pos(self, pos_x, pos_y): #Vérifier si une position est dehors de la carte pour blocker la déplacement de joueur
        if (( pos_x > -1 ) and ( pos_x < self.map_height )) and ( 
            ( pos_y > -1 ) and ( pos_y < self.map_width )) and (
            g_level_map[pos_x][pos_y] != 0):    
                return True
        return False

    def distance_needed(self, value_square_start, value_square_get, vari_pos): #calculer de la distance nécessaire pour passer un carré à d'autre
        #Car la position "start" et "end" sont enregistrées dans le liste avec les values -1 et -2, donc il faut changer pour avoir un l'algo précis
        if value_square_start in (SQUARE_START_VALUE, SQUARE_END_VALUE): value_square_start = 1
        if value_square_get in (SQUARE_START_VALUE, SQUARE_END_VALUE): value_square_get = 1
        
        #Basé sur pythagores
        coef = sqrt( vari_pos[0] ** 2 + vari_pos[1] ** 2 )
        return 0.5 * coef * (value_square_start + value_square_get)  

    def update_deplacement(self, vari_pos, is_back_1_step): #Mise à jour les variables et GUI après appuyer sur un bouton de déplacement
                                                            #On veut utiliser ce fonction pour le bouton "1 pas en arrière" comme Ctrl+Z, donc il y a un variable boolean: is_back_1_step
        if self.check_pos( self.player_charac.pos_x + vari_pos[0], self.player_charac.pos_y + vari_pos[1] ): #si cette position est dedans de la carte
            #Obtenir la caractérisque du "soil" que le personnage doit passer
            land_from = g_level_map[self.player_charac.pos_x][self.player_charac.pos_y] 
            land_to = g_level_map[self.player_charac.pos_x + vari_pos[0]][self.player_charac.pos_y + vari_pos[1] ]             
            
            self.player_charac.update_pos(vari_pos) #mise à jour le personnage
            if not is_back_1_step: #mise à jour après appuye sur un bouton de déplacement
                self.distance += self.distance_needed(land_from, land_to, vari_pos)
                self.way.append( (self.player_charac.pos_x, self.player_charac.pos_y) )           
                self.draw_way_index(-1, self.way, COLOR["dark green"])
            else: #si cette fonction est utilisée pour le bouton "1 pas en arrière"
                self.distance -= self.distance_needed(land_from, land_to, vari_pos)
                self.graph.delete(self.way_graph[-1]) 
                self.way_graph.pop(-1)
            
            g_level_window.proc_bar.update_distace(self.distance)
                        
            #finish actions
            if g_level_map[ self.player_charac.pos_x ][ self.player_charac.pos_y ] == -2: #si le personnage est à la position "end"
                self.finish_action()
                
    def finish_action(self): 
        '''
        Les actions à faire quand le personnage est à la position "end"
            - Creer et dessiner le FinishPopUp
            - Bloquer les boutons de déplacement si il y a le PopUp
            - Mise à jour le data de joueur (fichier csv)
        '''  
        #Creer le PopUp
        self.result_fen = FinishPopUp(g_level_window.racine, self.distance, self.way)
        self.result_fen.place_fenetre()
        
        #Déactiver les boutons de déplacement si il y a le PopUp
        for button in g_level_window.buttons:
            button.bttn.config(state = 'disabled')
        g_level_window.isFinish = True
        
        #Mise à jour le data de joueur (fichier csv) (la fonction est dans le fichier: main.py)
        g_level_window.menu_root.reset_select_level()
           
    def back_1_step(self): #Pour le bouton "1 pas en arrière" comme Ctrl+Z
        pos_delete = self.way.pop(-1)
        pos_get_to = self.way[-1]
        
        vari_pos = (pos_get_to[0] - pos_delete[0], pos_get_to[1] - pos_delete[1])
        self.update_deplacement(vari_pos, True)
                             
class button_deplacement: 
    '''
    Un class d'u bouton de déplacement
        :parametres: - root: la fenêtre du jeu
                     - name (String): le nom du bouton (pour determiner l'image du bouton)
                     - grid_pos (tuple): la position du bouton dans le grid de frame des boutons (pour utiliser .grid())
                     - pos_char_varie (tuple): la variation du personnage corrrespondant au bouton
    '''
    def __init__(self, root, name, grid_pos, pos_char_varie): #initialiser les variables       
        self.icon_link = './image/moving_buttons/' + name + '.png'
        self.icon = tk.PhotoImage(file = self.icon_link)
        
        self.button_with_border = tk.Frame(root, highlightbackground = COLOR["dark green"], highlightthickness = 3, bd =0)    
        self.bttn = tk.Button(self.button_with_border,
                                height = SIZE_MOVING_BUTTON, width = SIZE_MOVING_BUTTON,  
                                image = self.icon, relief= "flat",
                                bg = COLOR["lighter yellow"], activebackground = "#e3d8b6")#COLOR["lighter yellow"])
        self.bttn.pack()
        self.bttn.bind('<Button-1>', self.change_pos_charac)
        
        #on veut utiliser .grid() pour positioner ces boutons
        self.grid_row = grid_pos[0]
        self.grid_col = grid_pos[1]
        self.button_with_border.grid( column = self.grid_col, row = self.grid_row, padx = 2, pady = 2 )
        
        self.pos_char_varie = pos_char_varie       
        
    def change_pos_charac(self, event): #Callback pour le bouton -> mise à jour la position du personnage
        g_level_window.map_player.update_deplacement(self.pos_char_varie, False)

class ProgressBar: #
    '''
    Le tableau de la progression de joueur pendant le jeu.
    Il va monter la distance et le temps que le jeu est en cours, il contient aussi des boutons: quitter, retour, vol_on_off
        :parametres: - root: la fenêtre du jeu
                     - height (int): la hauteur du tableau
                     - width (int): la largeur du tableau
    '''
    def __init__(self, root, height, width): #initialiser les variables
        self.fen_level = root
        self.bar_height = height
        self.bar_width = width
        self.is_vol_up = True
        
        #Les couleurs
        self.bg_bar_color = COLOR["dark green"]
        self.font_titre = (FONT, 18)
        self.font_level = (FONT, 20, "bold") 
        self.font_in_square = (FONT, 18)
        self.font_color = COLOR["light yellow"]
        self.square_color = COLOR["lighter yellow"]
        
        #variables pour GUI
        self.height_separated_line = 2
        
        self.button_size = 40
        self.label_height = 50
        self.img_back_button = tk.PhotoImage(file = "./image/return_button.png")
        self.img_exit_button = tk.PhotoImage(file = "./image/close_button_green.png")
        self.img_vol_up_button = tk.PhotoImage(file = "./image/volume_up_button.png")
        self.img_vol_down_button = tk.PhotoImage(file = "./image/volume_down_button.png")
        
        self.bar_frame = tk.Frame(root, bg = self.bg_bar_color, 
                                  height = self.bar_height, width = self.bar_width)
        self.bar_frame.grid_propagate(False)
        
        percent_head = 36
        self.frame_head = tk.Frame(self.bar_frame, bg = self.bg_bar_color,
                                   height= self.bar_height*percent_head/100, width= self.bar_width) #2 boutons et une text indicant niveau de jouer
        self.frame_time = tk.Frame(self.bar_frame, bg = self.bg_bar_color,
                                   height= self.bar_height*(100 - percent_head)//200, width= self.bar_width) #Indication du temps
        self.frame_distance = tk.Frame(self.bar_frame, bg = self.bg_bar_color,
                                       height= self.bar_height*(100-percent_head)//200, width= self.bar_width) #Indication de la distance
          
        self.draw_widgets()
    
    def number_2_chiffres(self, number):
        '''
        Fonction permet de convertir un nombre vers un String de length = 2 pour montrer le temps de jouer (par ex: "01 : 30")
            :parametres: - number (int): le nombre à convertir
            :return:     - un String de length = 2
        '''
        if number < 10: return  ("0" + str(number))
        return str(number)
  
    def update_time(self): #Mise à jour le dessine chaque second
        txt_minute = self.number_2_chiffres(g_time_playing // 60)
        txt_second = self.number_2_chiffres(g_time_playing % 60)
        self.rectange_minute.config(text = txt_minute)
        self.rectange_second.config(text = txt_second)
        
    def update_distace(self, distance): #Mise à jour la distance montrée après chaque action
        self.rectange_distance.config(text = f"{distance:.2f}")  
    
    def draw_head(self): #dessiner la 1er partie du tableau: les boutons avec le nom indiquant labyrinth en cours de jouer
        separated_line = tk.Frame(self.frame_head, height = self.height_separated_line, width = 0.7 * self.bar_width,
                                       bg = self.font_color)
        separated_line.pack(side = tk.BOTTOM, pady = (2,0))
        
        #Dessiner le nom du labyrinth en cours de jouer
        titre_text = f"{g_level_difficulty} - {g_level}"
        if type(g_level) is not int: titre_text = f"{g_level_difficulty}\n{g_level}"
        self.titre_level = tk.Label(self.frame_head, text = titre_text, bg = self.bg_bar_color,
                                   fg = self.font_color, font = self.font_level)
        self.titre_level.pack(side = tk.BOTTOM, pady = (0, 5))
        
        #Dessiner les boutons: quitter, retour et vol_on_off
        self.frame_head_buttons = tk.Frame(self.frame_head, width = self.bar_width, bg = self.bg_bar_color, height= self.button_size +5)
        self.frame_head_buttons.grid_propagate(False)
        self.frame_head_buttons.pack(side = tk.TOP, pady=(12,2), padx= 7)
        self.frame_head_buttons.columnconfigure(0, weight=1)
        self.frame_head_buttons.columnconfigure(1, weight=1)
        self.frame_head_buttons.columnconfigure(2, weight=1)
        
        self.back_button = tk.Button(self.frame_head_buttons,
                              height = self.button_size, width = self.button_size,  
                              image = self.img_back_button, 
                              bg = COLOR["lighter yellow"], activebackground = COLOR["light yellow"])
        self.back_button.grid(column = 0, row = 0, sticky='n')
        self.back_button.bind('<Button-1>', self.back_one_step)
        
        self.vol_button = tk.Button(self.frame_head_buttons,
                              height = self.button_size, width = self.button_size,  
                              image = self.img_vol_up_button, 
                              bg = COLOR["lighter yellow"], activebackground = COLOR["light yellow"])
        self.vol_button.grid(column = 1, row = 0, sticky='n')
        self.vol_button.bind('<Button-1>', self.on_off_vol)
        
        self.exit_button = tk.Button(self.frame_head_buttons,
                              height = self.button_size, width = self.button_size,  
                              image = self.img_exit_button, 
                              bg = COLOR["lighter yellow"], activebackground = COLOR["light yellow"])
        self.exit_button.grid(column = 2, row = 0, sticky='n')
        self.exit_button.bind("<Button-1>", self.ask_to_exit)
    
    def draw_time(self): #dessiner la partie qui montre le temps
        self.titre_time = tk.Label(self.frame_time, text = "Time", bg = self.bg_bar_color,
                                   fg = self.font_color, font = self.font_titre)
        self.titre_time.pack(side = tk.TOP, pady = (8, 4))

        separated_line = tk.Frame(self.frame_time, height = self.height_separated_line, width = 0.7 * self.bar_width,
                                       bg = self.font_color)
        separated_line.pack(side = tk.BOTTOM, pady = (4,0))
        
        frame_block_height = tk.Frame(self.frame_time, height = self.label_height, width = self.bar_width,
                                      bg = self.bg_bar_color)
        frame_block_height.pack_propagate(0)
        
        self.rectange_minute = tk.Label(frame_block_height, bg = self.square_color,
                                        height = 2, width = 4, 
                                        fg = self.bg_bar_color, font = self.font_in_square)
        self.rectange_minute.pack(side = tk.LEFT, padx = (20,4))
    
        self.rectange_second = tk.Label(frame_block_height, bg = self.square_color, 
                                        height = 2, width = 4,   
                                        fg = self.bg_bar_color, font = self.font_in_square)
        self.rectange_second.pack(side = tk.RIGHT, padx = (4,20))
        
        frame_block_height.pack(side = tk.TOP, pady = (5,14))
        self.update_time()
    
    def draw_distance(self): #dessiner la partie qui montre la distance
        self.titre_distance = tk.Label(self.frame_distance, text = "Distance", bg = self.bg_bar_color,
                                      fg = self.font_color, font = self.font_titre)
        self.titre_distance.pack(side = tk.TOP, pady = (6, 2))
        
        text_distance = str(0.0)
        
        frame_block_height = tk.Frame(self.frame_distance, height = self.label_height, width = self.bar_width,
                                      bg = self.bg_bar_color)
        frame_block_height.pack_propagate(0)
        
        self.rectange_distance = tk.Label(frame_block_height, text = text_distance, bg = self.square_color, 
                                        height = 2, width = 7, 
                                        fg = self.bg_bar_color, font = self.font_in_square)
        self.rectange_distance.pack(side = tk.TOP)
        
        frame_block_height.pack(side = tk.TOP, pady = (8, 15))
            
    def draw_widgets(self): #draw tous les 3 parties
        #Éviter les 3 frames de être influencés par .pack() des widgets dedans
        self.frame_head.pack_propagate(False)
        self.frame_time.pack_propagate(False)
        self.frame_distance.pack_propagate(False)
        
        self.draw_time()
        self.draw_distance()
        self.draw_head()
        
        self.frame_head.grid(column=0, row=0)
        self.frame_time.grid(column=0, row=1)
        self.frame_distance.grid(column=0, row=2)
        
    def back_one_step(self, events): #Callback pour le bouton retour ("back_one_step")
        g_root.play_sound("button click")
        if g_level_window.map_player.distance > 0:
            g_level_window.map_player.back_1_step()
        
    def on_off_vol(self, event): #Callback pour le bouton vol_on_off
        g_root.play_sound("button click")
        if self.is_vol_up:
            self.is_vol_up = False
            self.vol_button['image'] = self.img_vol_down_button
        else:
            self.is_vol_up = True
            self.vol_button['image'] = self.img_vol_up_button
        g_root.on_off_music(self.is_vol_up)
        
    def ask_to_exit(self, events): #Callback pour le bouton quitter -> demander si le joueur veut quitter
        g_root.play_sound("button click")
        g_level_window.ask_to_quit()

class LevelWindow: 
    '''
    Class du fenetre du jeu
        :parametres: - root: le Toplevel du fenetre
                     - restart_random: liste des coordonnées de la matrice de réinitialisation
                     (ce paramatre est utilisé pour éviter la réinitialisation du labyrinthe quand le joueur rejoue un matrice aleatoire,
                     donc si le labyrinthe en cours de jouer n'est pas Matrice_random, donc, restart_random = [])
    '''
    
    def __init__(self, root, restart_random): #initialiser les variables
        self.menu_root = root
        
        #Verifier si le joeur rejoue un matrice aleatoire
        if restart_random == []: self.get_map() #Si non, on réinitialise le labyrinthe
        else:                                   #Si oui, on garde l'ancien matrice
            global g_level_map
            g_level_map = restart_random
        
        self.racine = tk.Toplevel(root,
                                  bg = BG_COLOR)
        self.racine.bind('<Key>',self.key_press_event)
        self.racine.resizable(width = False, height = False)
        self.draw()
        
        self.isFinish = False
        
        #initialiser la fonction compte le temps de jouer
        global g_time_playing
        g_time_playing = 0
        self.update_playing_time() 
       
    def get_map_csv(self): #lire le fichier csv du labyrinthe   
        fichier = "./level/" + g_level_difficulty + " - " + g_level + ".csv"
        with open(fichier, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            
            level_map = []
            for ligne in reader:
                level_ligne = []
                for cell in ligne:
                    level_ligne.append( int(cell) )
                        
                level_map.append( level_ligne.copy() )  
        print(level_map)
        return level_map 
                
    def get_map(self): #obtenir le labyrinthe de jouer: lire le fichier csv pour un labyrinthe normal, creer aleatoire pour un labyrinthe random
        global g_level_map
        if g_level.isnumeric(): 
            g_level_map = self.get_map_csv()
        else:
            mat_ran = Matrice_random(g_level_difficulty)
            g_level_map = mat_ran.matrice  
                
    def draw(self): #dessiner le fenetre
        self.frame_map = tk.Frame(self.racine,
                                  bg = BG_COLOR,
                                  highlightbackground = COLOR["dark green"],
                                  highlightthickness = 3)
        self.map_player = GraphicPlayingMap(self.frame_map, [])
        self.frame_map.pack(side = tk.LEFT, padx = (8,4), pady = 8 )
           
        self.draw_moving_button() 
        
        self.proc_bar = ProgressBar(self.racine, height = PROC_BAR_HEIGHT, width = PROC_BAR_WIDTH)
        self.proc_bar.bar_frame.pack(side = tk.TOP, padx= (6,12), pady = (0,0))

    def draw_moving_button(self): #dessiner les boutons de déplacement
        self.frame_buttons = tk.Frame(self.racine,
                                      bg = BG_COLOR)  
        
        self.buttons = [ #root; sa fonction; position pour .grid(); le changement du personnage quand le bouton est appuyé
            button_deplacement( self.frame_buttons,  'up-left',     (0,0) , (-1, -1) ) , 
            button_deplacement( self.frame_buttons,  'up' ,         (0,1) , (-1, 0)  ) ,
            button_deplacement( self.frame_buttons,  'up-right' ,   (0,2) , (-1, 1)  ) ,
            button_deplacement( self.frame_buttons,  'left' ,       (1,0) , (0, -1)  ) ,
            button_deplacement( self.frame_buttons,  'right' ,      (1,2) , (0, 1)   ) ,
            button_deplacement( self.frame_buttons,  'down-left' ,  (2,0) , (1, -1)  ) ,
            button_deplacement( self.frame_buttons,  'down' ,       (2,1) , (1, 0)   ) ,
            button_deplacement( self.frame_buttons,  'down-right' , (2,2) , (1, 1)   ) ,
        ]
        
        self.frame_buttons.pack(side = tk.BOTTOM, pady = (4,8), padx = (6,10))
    
    def key_press_event(self, event): #callback permet le joeur d'utiliser le keyboard pour jouer
        if event.keysym in MOVING_KEY.keys():
            g_level_window.map_player.update_deplacement( MOVING_KEY[event.keysym] , False)
              
    def ask_to_quit(self): #creer un "message box" pour demander si le joueur veut quitter
        self.msg_box = messagebox.askquestion("Attention!", "Do you want to quit?", icon = "info")
        if self.msg_box == "yes":
            self.racine.destroy()
        
    def update_playing_time(self): #une fonction pour compter le temps de jouer
        global g_time_playing
        g_time_playing += 1
        self.proc_bar.update_time()
        if not self.isFinish:
            self.racine.after(1000, self.update_playing_time)
        
    def restart(self): #pour le bouton "rejouer", "restart_random" pour enregistrer le matrice random si le joeur veux rejouer le labyrinthe random avant    
        self.racine.destroy()
        if g_level == "RANDOM": restart_random = g_level_map
        else: restart_random = []
        self.__init__(self.menu_root, restart_random)
        
def open_level(difficulty, level, root): #fonction pour le fichier python principal, quand le joueur choisit un labyrinthe pour jouer
    global g_level_difficulty
    global g_level
    g_level_difficulty = difficulty
    g_level = level
    
    global g_root
    g_root = root
    
    global g_level_window
    g_level_window = LevelWindow(root, []) 
    return g_level_window     
    
if __name__ == "__main__":
    g_root = tk.Tk()
    #g_root.geometry(f"{1000}x{700}")
    open_level("EASY", "RANDOM" , g_root)
    g_root.mainloop()
