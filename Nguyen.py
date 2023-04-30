# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 07:14:58 2023

@author: ptngu
"""

import tkinter as tk

class Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        window_frame = tk.Frame(self)
        window_frame.pack() 
        
        self.frames = {}
        for F in (HomePage, SettingPage):
            frame = F(self,window_frame) #self là Window
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
        
        self.lb1=tk.Label(self, text = "Home Page")
        self.lb1.pack()
        
        self.lb2 = tk.Label(self, text="          GAME TITRE:          ", font=("Times New Roman", 35))
        self.lb2.pack()
        x=2
        for i in range(x):
            self.lb =tk.Label(self, text = "")
            self.lb.pack()
        self.bouton_play_game = tk.Button(self, text="PLAY GAME ", borderwidth=2, relief="solid", highlightbackground="green", font=("Times New Roman", 13))
        self.bouton_play_game.pack()     
        
        self.bouton_setting = tk.Button(self, text="SETTING        ", borderwidth=2, relief="solid", highlightbackground="green", font=("Times New Roman", 13))
        self.bouton_setting.bind("<Button-1>",self.button1Click)
        self.bouton_setting.pack()
        
        self.bouton_quit = tk.Button(self, text="QUIT               ", borderwidth=2, relief="solid", highlightbackground="green", font=("Times New Roman", 13))
        self.bouton_quit.pack()
        n=5
        for i in range(n):
            self.lb =tk.Label(self, text = "")
            self.lb.pack()
        
        
        
    def button1Click(self,event):
        self.controller.show_frame(SettingPage)
    
   
        
class SettingPage(tk.Frame):
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
        
            