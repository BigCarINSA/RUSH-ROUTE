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
        for F in (HomePage, PlayGame, Setting):
            frame = F(self,window_frame) #self là Window
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
       
        self.lb1=tk.Label(self, text = "ROUTE RUSH",
                          font=(FONT, 90, "bold"),
                          fg = COLOR["dark blue"],bg= COLOR["lighter yellow"])
        self.lb1.place(x=160 ,y =00)
        
        
        # self.frame_button = tk.Frame(self, width, heigth)
        # self.frame_button.pack_propagate(0)
                                    
        # self.bouton_play_game = tk.Button(self, text="PLAY  ",  
        #                                   width = 7, 
        #                                   foreground = COLOR['white'],
        #                                   activeforeground= COLOR["dark green"], 
        #                                   bg = COLOR["light green"], 
        #                                   activebackground = COLOR['dark green'],
        #                                   font=("Century Gothic", 40,"bold"),
    
        #                                   relief='flat')
        self.bouton_play_game = tk.Button(self, width = 10, height= 0,
                                      text = "PLAY", font = (FONT, 30,"bold"), 
                                      foreground = COLOR['white'],
                                      activeforeground= COLOR["light yellow"], 
                                      bg = COLOR['dark green'], activebackground = COLOR['dark blue'],
                                      relief = 'flat')
        self.bouton_play_game.place(x=380 ,y =200)     
        self.bouton_play_game.bind("<Button-1>",self.button1Click)
        
        self.bouton_record = tk.Button(self, width = 10, height= 0,
                                      text = "RECORD", font = (FONT, 30,"bold"), 
                                      foreground = COLOR['dark blue'],
                                      activeforeground= COLOR["light yellow"], 
                                      bg = COLOR['light yellow'], activebackground = COLOR['dark blue'],
                                      relief = 'flat')
        
        self.bouton_record.place(x=380 ,y =300)
        
        self.bouton_setting = tk.Button(self, width = 10, height= 0,
                                      text = "SETTING", font = (FONT, 30,"bold"), 
                                      foreground = COLOR['dark blue'],
                                      anchor="nw",
                                      activeforeground= COLOR["light yellow"], 
                                      bg = COLOR['light yellow'], activebackground = COLOR['dark blue'],
                                      relief = 'flat')
        self.bouton_setting.place(x=380 ,y =400)
        
        self.quitter_image = tk.PhotoImage(file = "./Image/quit_button.png")
        self.quitter_button = tk.Button(self, image = self.quitter_image,
                                      height = 50, width = 50, relief = 'flat',
                                      bg = COLOR["dark green"], 
                                      activebackground = COLOR["dark blue"])
        self.quitter_button.place(x = 800, y = 12)
        #self.quitter_button.bind('<Button-1>', self.close_setting)
               
        
        
    def button1Click(self,event):
        self.controller.show_frame(PlayGame)
    
   
        
class PlayGame(tk.Frame):
    def __init__(self,controller,frame):
        tk.Frame.__init__(self, frame)
    
        self.controller = controller        
        #cần self để gọi lên self.window.showframe
        
        self.lbl =tk.Label(self, text = "Setting Page")
        self.lbl.pack() #khởi tạo frame thuộc tk nào : window  
        
        self.lb2 = tk.Label(self, text="          Select difficulty          ", font=("Times New Roman", 35))
        self.lb2.pack()
        self.bouton_easy = tk.Button(self, text="EASY", borderwidth=2, relief="solid", highlightbackground="green", font=("Times New Roman", 13))
        self.bouton_easy.pack()
        self.medium = tk.Button(self, text="MEDIUM", borderwidth=2, relief="solid", highlightbackground="green", font=("Times New Roman", 13))
        self.medium.pack()
        self.hard = tk.Button(self, text="HARD", borderwidth=2, relief="solid", highlightbackground="green", font=("Times New Roman", 13))
        self.hard.pack()
        
        n=3
        for i in range(n):
            self.lb =tk.Label(self, text = "")
            self.lb.pack()
        self.controller = controller        
        #cần self để gọi lên self.window.showframe
        
        self.button1 = tk.Button(self,text = "Return to HomePage")
        self.button1.bind("<Button-1>",self.button1Click)
        self.button1.pack()
        
        m=2
        for i in range(m):
            self.lb =tk.Label(self, text = "")
            self.lb.pack()
        self.controller = controller        
        
    def button1Click(self,event):
        self.controller.show_frame(HomePage)
        
class PlayGame(tk.Frame):
    def __init__(self,controller,frame):
        tk.Frame.__init__(self, frame)
    
        self.controller = controller        
        #cần self để gọi lên self.window.showframe
        
        self.lbl =tk.Label(self, text = "Setting Page")
        self.lbl.pack() #khởi tạo frame thuộc tk nào : window  
        
        self.lb2 = tk.Label(self, text="          Select difficulty          ", font=("Times New Roman", 35))
        self.lb2.pack()
        self.bouton_easy = tk.Button(self, text="EASY", borderwidth=2, relief="solid", highlightbackground="green", font=("Times New Roman", 13))
        self.bouton_easy.pack()
        self.medium = tk.Button(self, text="MEDIUM", borderwidth=2, relief="solid", highlightbackground="green", font=("Times New Roman", 13))
        self.medium.pack()
        self.hard = tk.Button(self, text="HARD", borderwidth=2, relief="solid", highlightbackground="green", font=("Times New Roman", 13))
        self.hard.pack()
        
        n=3
        for i in range(n):
            self.lb =tk.Label(self, text = "")
            self.lb.pack()
        self.controller = controller        
        #cần self để gọi lên self.window.showframe
        
        self.button1 = tk.Button(self,text = "Return to HomePage")
        self.button1.bind("<Button-1>",self.button1Click)
        self.button1.pack()
        
        m=2
        for i in range(m):
            self.lb =tk.Label(self, text = "")
            self.lb.pack()
        self.controller = controller        
        
    def button1Click(self,event):
        self.controller.show_frame(HomePage)
        
class Setting(tk.Frame):
    def __init__(self,controller,frame):
        tk.Frame.__init__(self, frame)
    
        self.controller = controller        
        #cần self để gọi lên self.window.showframe
        
        self.lbl =tk.Label(self, text = "Setting Page")
        self.lbl.pack() #khởi tạo frame thuộc tk nào : window  
        
        self.lb2 = tk.Label(self, text="          Select difficulty          ", font=("Times New Roman", 35))
        self.lb2.pack()
        self.bouton_easy = tk.Button(self, text="EASY", borderwidth=2, relief="solid", highlightbackground="green", font=("Times New Roman", 13))
        self.bouton_easy.pack()
        self.medium = tk.Button(self, text="MEDIUM", borderwidth=2, relief="solid", highlightbackground="green", font=("Times New Roman", 13))
        self.medium.pack()
        self.hard = tk.Button(self, text="HARD", borderwidth=2, relief="solid", highlightbackground="green", font=("Times New Roman", 13))
        self.hard.pack()
        
        n=3
        for i in range(n):
            self.lb =tk.Label(self, text = "")
            self.lb.pack()
        self.controller = controller        
        #cần self để gọi lên self.window.showframe
        
        self.button1 = tk.Button(self,text = "Return to HomePage")
        self.button1.bind("<Button-1>",self.button1Click)
        self.button1.pack()
        
        m=2
        for i in range(m):
            self.lb =tk.Label(self, text = "")
            self.lb.pack()
        self.controller = controller        
        
    def button1Click(self,event):
        self.controller.show_frame(HomePage)
        

        
app = Window()
app.mainloop()
        
            