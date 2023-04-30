# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 07:14:58 2023

@author: ptngu
"""

import tkinter as tk
from tkinter import messagebox
from game_play import open_level
import csv

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


MIN_VOLUME = 0
MAX_VOLUME = 100

WINDOWHEIGHT = 600
WINDOWWIDTH = 1000

GAME_NAME = "ROUTE RUSH"
TITRE_FONT = (FONT, 80,"bold")

class Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("1000x600")
        
        window_frame = tk.Frame(self)
        window_frame.pack() 
        self.maze_playing_window = None
        
        self.frames = {}
        for F in (HomePage, PlayGame, SettingPopUp, LevelSelect):
            frame = F(self,window_frame) #self est Window
            if F != SettingPopUp:
                frame.config(width=1000, height=600)
                frame.config(bg= COLOR["lighter yellow"])
            frame.grid(row = 0, column =0)
                       #sticky = "nsew")
            self.frames[F] =frame
            
        self.show_frame(HomePage) 
    
    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()
        
class HomePage(tk.Frame):
    def __init__(self,controller,frame): 
        tk.Frame.__init__(self, frame)
        self.pack_propagate(0)
        self.controller = controller 
        
        self.dis_button = 20
        self.buttons_width = 320
        self.buttons_height = 80
        self.buttons_font_style = (FONT, 30, "bold")
        
        self.draw_widgets()
        
    def draw_widgets(self):       
        self.lb1=tk.Label(self,  text = GAME_NAME, font=(FONT, 90, 'bold'),
                          fg = COLOR["dark blue"],bg= COLOR["lighter yellow"] )
        self.lb1.pack(pady=(50,0))
        
        self.frame_button = tk.Frame(self, bg = COLOR["lighter yellow"])
        self.frame_button.pack(side = tk.BOTTOM, pady = (0, 40))
        
        list_buttons = ["play", "record", "setting"]
        frames_buttons = {}    
        for i in range(len(list_buttons)):
            frames_buttons[ list_buttons[i] ] = tk.Frame(self.frame_button,
                                                         highlightbackground = COLOR["dark blue"], highlightthickness = 5,
                                                         width = self.buttons_width, height = self.buttons_height)
            frames_buttons[ list_buttons[i] ].pack(pady= (self.dis_button, 0))
            frames_buttons[ list_buttons[i] ].pack_propagate(0)
        
        self.bouton_play_game = tk.Button( frames_buttons["play"], width = 30, height= 2,
                                           text = "PLAY",  font = self.buttons_font_style, 
                                      foreground = COLOR['white'], activeforeground= COLOR["light yellow"], 
                                      bg = COLOR['dark green'],  activebackground = COLOR['dark blue'],
                                      relief = 'flat')
        self.bouton_play_game.pack()     
        self.bouton_play_game.bind("<Button-1>",self.button1Click)
        
        self.bouton_record = tk.Button( frames_buttons["record"], width = 30, height= 2,
                                        text = "RECORD", font = self.buttons_font_style, 
                                        foreground = COLOR['dark blue'], activeforeground= COLOR["light yellow"], 
                                        bg = COLOR['light yellow'], activebackground = COLOR['dark blue'],
                                        relief = 'flat')
        self.bouton_record.pack()
        
        self.bouton_setting = tk.Button( frames_buttons["setting"], width = 30, height= 2,
                                         text = "SETTING", font = self.buttons_font_style, 
                                         foreground = COLOR['dark blue'], activeforeground= COLOR["light yellow"], 
                                         bg = COLOR['light yellow'], activebackground = COLOR['dark blue'],
                                         relief = 'flat')
        self.bouton_setting.pack()
        self.bouton_setting.bind("<Button-1>",self.boutonsettingClick)
            
        self.quitter_image = tk.PhotoImage(file = "./Image/quit_button.png")
        self.quitter_button = tk.Button(self, image = self.quitter_image,
                                        height = 65, width = 65, relief = 'flat',
                                        bg = COLOR["dark green"], 
                                        activebackground = COLOR["dark blue"])
        self.quitter_button.place(x = 30, y = 500)
        self.quitter_button.bind('<Button-1>', self.quitClick)        
               
    def button1Click(self,event):
        self.controller.show_frame(PlayGame)

    def boutonsettingClick(self,event):
        self.controller.show_frame(SettingPopUp)
        
    def quitClick(self,event):
        self.msg_box = messagebox.askquestion("Attention!", "Do you want to quit?", icon = "warning")
        if self.msg_box == "yes":
            self.controller.destroy()
            
class PlayGame(tk.Frame):
    def __init__(self,controller,frame):
        tk.Frame.__init__(self, frame)   
        self.controller = controller      
        self.pack_propagate(0)
        
        self.dis_button = 20
        self.buttons_width = 320
        self.buttons_height = 80
        self.buttons_font_style = (FONT, 30, "bold")
        
        self.draw_widgets()  
        
    def draw_widgets(self):
        self.lb1=tk.Label(self,  text = GAME_NAME, font=TITRE_FONT,
                          fg = COLOR["dark blue"],bg= COLOR["lighter yellow"] )
        self.lb1.pack(pady=(30,0))
        
        self.lb2=tk.Label(self, text = "Select Difficulty", font=(FONT, 40),
                          fg = COLOR["dark blue"], bg= COLOR["lighter yellow"] )
        self.lb2.pack()
        
        self.frame_button = tk.Frame(self, bg = COLOR["lighter yellow"])
        self.frame_button.pack(side = tk.BOTTOM, pady = (0, 40))
        
        self.list_buttons = ["EASY", "MEDIUM", "HARD"]
        self.frames_buttons = {}   
        self.buttons = {} 
        for i in range(len(self.list_buttons)):
            button = self.list_buttons[i]
            self.frames_buttons[ button ] = tk.Frame(self.frame_button,
                                                         highlightbackground = COLOR["dark blue"], highlightthickness = 5,
                                                         width = self.buttons_width, height = self.buttons_height)
            self.frames_buttons[ button ].pack(pady= (self.dis_button, 0))
            self.frames_buttons[ button ].pack_propagate(0)
            
            self.buttons[button] = tk.Button( self.frames_buttons[button], width = 30, height= 2,
                                              text = button, font = self.buttons_font_style, 
                                              foreground = COLOR['dark blue'], activeforeground= COLOR["light yellow"], 
                                              bg = COLOR['light yellow'], activebackground = COLOR['dark blue'],
                                              relief = 'flat')
            self.buttons[button].bind("<Button-1>", self.get_button_click)
            self.buttons[button].pack()
        
        self.return_image = tk.PhotoImage(file = "./Image/quit_button.png")
        self.return_button = tk.Button(self, image = self.return_image,
                                        height = 65, width = 65, relief = 'flat',
                                        bg = COLOR["dark green"], 
                                        activebackground = COLOR["dark blue"])
        self.return_button.place(x = 30, y = 500)
        self.return_button.bind('<Button-1>', self.button_return)        

    def get_button_click(self, event):
        self.open_level_selection( event.widget['text'] )

    def open_level_selection(self, difficulty):
        self.controller.show_frame(LevelSelect)
        self.controller.frames[LevelSelect].change_difficulty(difficulty)
        
    def button_return(self,event):
        self.controller.show_frame(HomePage)
 
class Scale:
    def __init__(self, root, bg, length, slider_size, slider_border_color, slider_border_width, trough_color, slider_color, active_slider_color, command):
        self.slider_frame = tk.Frame(root)
        self.command = command
        
        self.slider_border_width = slider_border_width
        self.length = length
        self.slider_size = slider_size
        self.slider_size_no_border = self.slider_size - 2*self.slider_border_width
        self.slider_border_color = slider_border_color
        
        self.trough_color = trough_color
        self.slider_color = slider_color
        self.active_slider_color = active_slider_color

        self.canvas = tk.Canvas(self.slider_frame, width=self.length, height=self.slider_size, 
                                background = bg, 
                                borderwidth= 0, highlightthickness=0)
        self.canvas.pack()

        # Dessiner le creux
        trough_height = 6
        trough_width = self.length
        self.trough_x1 = self.slider_size / 2
        self.trough_x2 = self.length - self.slider_size / 2
        trough_y = (self.slider_size - trough_height) / 2
        self.canvas.create_rectangle(self.trough_x1, trough_y, self.trough_x2, trough_y + trough_height, fill=self.trough_color, width=0)

        # Dessiner le glissière
        slider_x = self.length / 2
        self.slider = self.canvas.create_oval(slider_x, self.slider_border_width, slider_x + self.slider_size_no_border, -1 + self.slider_size_no_border+self.slider_border_width, 
                                              fill=self.slider_color, outline=slider_border_color, width = self.slider_border_width)
        
        #Ajouter des evenements
        self.last_x = 0
        self.canvas.tag_bind(self.slider, '<Button-1>', self.on_slider_press)
        self.canvas.tag_bind(self.slider, '<B1-Motion>', self.on_slider_move)
        self.canvas.tag_bind(self.slider, '<ButtonRelease-1>', self.on_slider_release)

    def on_slider_press(self,event):
        self.last_x = event.x
        self.canvas.itemconfig(self.slider, fill=self.active_slider_color)

    def on_slider_move(self,event):
        #Obtenir la position du glissiere
        pos_slider = self.canvas.coords(self.slider)
        self.centre_slider = (pos_slider[0]+pos_slider[2]) / 2
        
        #Mise à jour la position du glissiere
        new_x = event.x
        if (self.centre_slider > self.trough_x1) and (self.centre_slider < self.trough_x2):
            slider_delta_x = new_x - self.last_x
        elif (self.centre_slider <= self.trough_x1): slider_delta_x = 1
        else: slider_delta_x = -1
        self.canvas.move(self.slider, slider_delta_x, 0)
        self.last_x = new_x
        
        self.get_value_slider()
        self.command(self.value)
 
    def on_slider_release(self, event):
        self.canvas.itemconfig(self.slider, fill=self.slider_color)

    def get_value_slider(self):
        self.value = (self.centre_slider - self.trough_x1) / (self.trough_x2 - self.trough_x1)
        if self.value < 0: self.value = 0
        if self.value > 1: self.value = 1
class SettingPopUp(tk.Frame):
    def __init__(self, controller, frame):
        self.controller = controller
        
        self.bg_color = COLOR['light yellow']
        self.height = 325
        self.width = 600
        print("running")
        
        tk.Frame.__init__(self, frame)
        self.config(height = self.height, width = self.width, background= self.bg_color,
                    highlightbackground = COLOR["dark blue"], highlightthickness = 5)
        self.pack_propagate(0)
        
        self.scale_length = 320
        self.slider_size = 46
        self.draw()
    
    def draw_sound_scale(self):
        self.frame_volumn = tk.Frame(self, bg=self.bg_color, width = 600)
        self.frame_volumn.pack(side = tk.LEFT)
        
        self.label_font = (FONT, 30)
        self.label = tk.Label(self.frame_volumn, text="Volume:", bg=self.bg_color,
                              font = self.label_font, foreground = COLOR['dark green'])
        self.label.pack(side=tk.LEFT, padx= (30,20))

        self.scale = Scale(self.frame_volumn, length = self.scale_length, 
                           trough_color = COLOR['dark blue'], bg = self.bg_color,
                           slider_size = self.slider_size, slider_border_width = 3, 
                           slider_border_color = COLOR["dark blue"],          
                           slider_color = COLOR['light green'], 
                           active_slider_color = COLOR['dark green'],
                           command = self.update_volume)
        
        self.scale.slider_frame.pack(side=tk.LEFT, padx= (0,36))

    def draw(self):    
        #dessiner le titre
        self.title = tk.Label(self, bg = self.bg_color,
                              font = (FONT, 45, 'bold'), text = 'SETTING' , 
                              foreground = COLOR['dark blue'])
        self.title.pack(side = tk.TOP, pady = (20,0))
        
        
        #dessiner bouton "reset"       
        self.frame_reset_button = tk.Frame(self, bg=self.bg_color, height = 62, width = self.width)
        self.reset_button = tk.Button(self.frame_reset_button, width = 10, height= 1,
                                      text = "RESET DATA", font = (FONT, 30), 
                                      foreground = COLOR['lighter yellow'],
                                      activeforeground= COLOR["lighter yellow"], 
                                      bg = COLOR['dark green'],
                                      activebackground = COLOR['dark blue'],
                                      relief = 'flat')
        self.reset_button.pack()
        self.reset_button.bind('<Button-1>', self.reset_data_player)
        self.frame_reset_button.pack( side = tk.BOTTOM, pady=(10,25) )
        
        self.draw_sound_scale()
        
        #dessiner bouton "close"
        self.close_image = tk.PhotoImage(file = "./Image/close_button_yellow.png")
        self.close_button = tk.Button(self, image = self.close_image,
                                      height = 50, width = 50, relief = 'flat',
                                      bg = COLOR["dark green"], activebackground = COLOR["dark blue"])
        self.close_button.place(x = 520, y = 12)
        self.close_button.bind('<Button-1>', self.close_setting)
        
    def update_volume(self, value):
        #Code pour modifier l'intensite
        self.volumn_intensite = MIN_VOLUME + value * (MAX_VOLUME - MIN_VOLUME)
        print(self.volumn_intensite)  
        
    def reset_data_player(self, events):
        self.msg_box = messagebox.askquestion("Attention!", "Reset all data and start over?", icon = "info")
        if self.msg_box == "yes":
            print("reset")

    def close_setting(self, events):
        self.controller.show_frame(HomePage)
            
class LevelSelect(tk.Frame):
    def __init__(self,controller,frame):
        tk.Frame.__init__(self, frame)   
        self.controller = controller      
        self.pack_propagate(0)
        
        self.ver_dis_button = 30
        self.hoz_dis_button = 30
        self.buttons_width = 320
        self.buttons_height = 80
        self.buttons_font_style = (FONT, 30)
        
        self.get_player_data()
        self.difficulty = "EASY"
        self.nb_levels = 5 #Inclure également labyrinthe aléatoire
        self.draw_widgets()  
        
    def draw_grid_buttons_level(self):
        self.frame_button = tk.Frame(self, bg = COLOR["lighter yellow"])
        self.frame_button.pack(side = tk.TOP, pady = (0,0))
        
        self.list_buttons = []
        self.frames_buttons = {}   
        self.buttons = {} 
        
        for i in range(self.nb_levels - 1):
            self.list_buttons.append(f"{i+1}")
        self.list_buttons.append(f"random")
        
        for i in range(self.nb_levels):
            button = self.list_buttons[i]
            self.frames_buttons[ button ] = tk.Frame(self.frame_button,
                                                    highlightbackground = COLOR["dark blue"], highlightthickness = 5,
                                                    width = self.buttons_width, height = self.buttons_height)
            
            if i != self.nb_levels-1:
                self.frames_buttons[ button ].grid(column = i%2, row = i//2, 
                                                                pady= (self.ver_dis_button, 0), padx = self.hoz_dis_button//2)
            else:
                self.frames_buttons[ button ].grid(row = i//2, columnspan = 2, pady= (self.ver_dis_button, 0), padx = self.hoz_dis_button//2)
            self.frames_buttons[ button ].pack_propagate(0)
            
            self.buttons[button] = tk.Button( self.frames_buttons[button], width = 30, height= 2,
                                              text = "Maze "+ button, font = self.buttons_font_style, 
                                              foreground = COLOR['dark blue'], activeforeground = COLOR["light yellow"], 
                                              bg = COLOR['light yellow'], activebackground = COLOR['dark blue'],
                                              relief = 'flat')
            self.buttons[button].pack()
            self.buttons[button].bind("<Button-1>",self.open_maze_selection)
            
        for i in range(1, self.nb_levels):
            button = self.list_buttons[i]
            previous_level = self.difficulty + ' - ' + self.list_buttons[i-1]
            played_times, high_score = self.player_data[previous_level]
            if (played_times < 3) and (high_score < 90):
                self.buttons[button].config( state='disabled', bg = COLOR['light green'])
                self.frames_buttons[ button ].config( highlightbackground = COLOR["dark green"] )
        
    def draw_widgets(self):
        self.lb1=tk.Label(self,  text = GAME_NAME, font=TITRE_FONT,
                          fg = COLOR["dark blue"],bg= COLOR["lighter yellow"] )
        self.lb1.pack(pady=(30,0))
        
        self.difficulty_titre = self.difficulty[0] + self.difficulty[1:].lower() + " Maze"
        self.lb2=tk.Label(self, text = self.difficulty_titre, font=(FONT, 40),
                          fg = COLOR["dark blue"], bg= COLOR["lighter yellow"] )
        self.lb2.pack()
        
        self.draw_grid_buttons_level()
        
        self.return_image = tk.PhotoImage(file = "./Image/quit_button.png")
        self.return_button = tk.Button(self, image = self.return_image,
                                        height = 65, width = 65, relief = 'flat',
                                        bg = COLOR["dark green"], 
                                        activebackground = COLOR["dark blue"])
        self.return_button.place(x = 30, y = 500)
        self.return_button.bind('<Button-1>', self.button_return)        

    def open_maze_selection(self, event):
        button_clicked = event.widget
        print(button_clicked['state'])
        if button_clicked['state'] != 'disabled':
            level_select = self.difficulty + " - " + button_clicked['text'][-1]
            print(level_select)
            
            if self.controller.maze_playing_window != None:
                self.controller.maze_playing_window.destroy()
            self.fen_level = open_level(level_select, self.controller)
        
    def get_player_data(self):
        self.player_data = {}
        with open(file = PLAYER_DATA, mode = 'r', encoding= "utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            reader.__next__()
            for ligne in reader:
                level, played_times, high_score = ligne
                self.player_data[level] = [int(played_times), float(high_score)]
        print(self.player_data)
        
    def change_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.difficulty_titre = self.difficulty[0] + self.difficulty[1:].lower() + " Maze"
        
        self.lb2.config(text = self.difficulty_titre)
        self.frame_button.destroy()
        self.draw_grid_buttons_level()
        
    def button_return(self,event):
        self.controller.show_frame(PlayGame)
               
app = Window()
app.mainloop()
        
            