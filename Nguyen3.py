# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 07:14:58 2023

@author: ptngu
"""

import tkinter as tk
from PIL import Image, ImageTk

FONT = "Century Gothic" #font principal de GUI
BG_COLOR = "white"
COLOR = { "white"        :  "#FFFFFF",
          "yellow"       :  "#FFD966",       "light yellow" :   "#F3DEBA",       "lighter yellow" : "#F0E9D2",
          "light green"  :  "#ABC4AA",       "dark green"   :   "#678983",
          "red"          :  "#EA5455",       "light red"    :   "#F0997D",       "dark red"       : "#A9907E",
          "dark blue"    :  "#114C5E", 
          "brown"        :  "#675D50"
        }
class Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("1000x600")
        
        window_frame = tk.Frame(self)
        window_frame.pack() 
        
        self.frames = {}
        for F in (HomePage, PlayGame):
            frame = F(self,window_frame) #self est Window
            frame.config(width=1000, height=600)
            frame.config(bg= COLOR["lighter yellow"])
            frame.grid(row = 0, column =0,
                       sticky = "nsew")
            self.frames[F] =frame
        
        self.show_frame(HomePage)
        
    
    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()
        
class HomePage(tk.Frame):
    def __init__(self,controller,frame): 
        tk.Frame.__init__(self, frame)
        self.controller = controller        
        self.lb1=tk.Label(self, 
                          text = "ROUTE RUSH",
                          font=(FONT, 90, "bold"),
                          fg = COLOR["dark blue"],bg= COLOR["lighter yellow"]
                          )
        self.lb1.place(x=160 ,y =00)
        
        
        self.frame_button_play = tk.Frame(self,highlightbackground = COLOR["dark blue"], highlightthickness = 5)
        self.frame_button_play.place(x=380 ,y =200)
        self.bouton_play_game = tk.Button( self.frame_button_play, width = 10, height= 0,
                                      text = "PLAY", 
                                      font = (FONT, 25,"bold"), 
                                      foreground = COLOR['white'],
                                      activeforeground= COLOR["light yellow"], 
                                      bg = COLOR['dark green'], 
                                      activebackground = COLOR['dark blue'],
                                      relief = 'flat')
        self.bouton_play_game.pack()     
        self.bouton_play_game.bind("<Button-1>",self.button1Click)
        
        self.frame_button_record = tk.Frame(self,highlightbackground = COLOR["dark blue"], highlightthickness = 5)
        self.frame_button_record.place(x=380 ,y =300)  
        self.bouton_record = tk.Button( self.frame_button_record, width = 10, height= 0,
                                      text = "RECORD", font = (FONT, 25,"bold"), 
                                      foreground = COLOR['dark blue'],
                                      activeforeground= COLOR["light yellow"], 
                                      bg = COLOR['light yellow'], activebackground = COLOR['dark blue'],
                                      relief = 'flat')
        self.bouton_record.pack()
        
        self.frame_button_setting = tk.Frame(self,highlightbackground = COLOR["dark blue"], highlightthickness = 5)
        self.frame_button_setting.place(x=380 ,y =400) 
        self.bouton_setting = tk.Button( self.frame_button_setting, width = 10, height= 0,
                                      text = "SETTING", font = (FONT, 25,"bold"), 
                                      foreground = COLOR['dark blue'],
                                      activeforeground= COLOR["light yellow"], 
                                      bg = COLOR['light yellow'],
                                      activebackground = COLOR['dark blue'],
                                      relief = 'flat')
        self.bouton_setting.pack()
        
        
        #self.quitter_image = tk.PhotoImage()
        self.quitter_button = tk.Button(self, text = "q",
                                      height = 1, width = 1, relief = 'flat',
                                      bg = COLOR["dark green"], 
                                      activebackground = COLOR["dark blue"])
        self.quitter_button.place(x = 12, y = 800)
        #self.quitter_button.bind('<Button-1>', self.close_setting)
    
        
        
        
    def button1Click(self,event):
        self.controller.show_frame(PlayGame)
    
   
        
class PlayGame(tk.Frame):
    def __init__(self,controller,frame):
        tk.Frame.__init__(self, frame)
    
        self.controller = controller        
        

        self.lb1=tk.Label(self, 
                          text = "SELECT DIFFICULTY",
                          font=(FONT,70, "bold"),
                          fg = COLOR["dark blue"],
                          bg= COLOR["lighter yellow"]
                          )
        self.lb1.place(x=140 ,y =30)
        
        self.frame_button_easy = tk.Frame(self,highlightbackground = COLOR["dark blue"], highlightthickness = 5)
        self.frame_button_easy.place(x=380 ,y =200) 
        self.bouton_easy= tk.Button( self.frame_button_easy, width = 10, height= 0,
                                      text = "EASY", font = (FONT, 25,"bold"), 
                                      foreground = COLOR['dark blue'],
                                      activeforeground= COLOR["light yellow"], 
                                      bg = COLOR['light yellow'],
                                      activebackground = COLOR['dark blue'],
                                      relief = 'flat')
        self.bouton_easy.pack()
        
        self.frame_button_medium = tk.Frame(self,highlightbackground = COLOR["dark blue"], highlightthickness = 5)
        self.frame_button_medium.place(x=380 ,y =300) 
        self.bouton_medium= tk.Button( self.frame_button_medium, width = 10, height= 0,
                                      text = "MEDIUM", font = (FONT, 25,"bold"), 
                                      foreground = COLOR['dark blue'],
                                      activeforeground= COLOR["light yellow"], 
                                      bg = COLOR['light yellow'],
                                      activebackground = COLOR['dark blue'],
                                      relief = 'flat')
        self.bouton_medium.pack()
        
        self.frame_button_hard = tk.Frame(self,highlightbackground = COLOR["dark blue"], highlightthickness = 5)
        self.frame_button_hard .place(x=380 ,y =400) 
        self.bouton_hard = tk.Button( self.frame_button_hard , width = 10, height= 0,
                                      text = "SETTING", font = (FONT, 25,"bold"), 
                                      foreground = COLOR['dark blue'],
                                      activeforeground= COLOR["light yellow"], 
                                      bg = COLOR['light yellow'],
                                      activebackground = COLOR['dark blue'],
                                      relief = 'flat')
        self.bouton_hard .pack()
        self.controller = controller        
        #cần self để gọi lên self.window.showframe
        
        
        #thay ảnh vô giúp t vs nhá
        
        
        self.frame_button_return = tk.Frame(self,highlightbackground = COLOR["dark blue"],
                                            highlightthickness = 5)
        self.frame_button_return.place(x=0 , y =500) 
        self.bouton_return = tk.Button( self.frame_button_return, width = 10, height= 0,
                                      text = "quit", font = (FONT, 25,"bold"), 
                                      foreground = COLOR['dark blue'],
                                      activeforeground= COLOR["light yellow"], 
                                      bg = COLOR['light yellow'],
                                      activebackground = COLOR['dark blue'],
                                      relief = 'flat')
        self.bouton_return.bind("<Button-1>",self.button_return)
        self.bouton_return.pack()     
           
    def button_return(self,event):
        self.controller.show_frame(HomePage)


        
app = Window()
app.mainloop()
        
            