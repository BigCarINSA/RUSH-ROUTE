import tkinter as tk
from tkinter import messagebox

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

class SettingPopUp:
    def __init__(self, root):
        self.bg_color = COLOR['light yellow']
        self.height = 325
        self.width = 600
        
        self.frame_setting = tk.Frame(root, height=self.height, width=self.width, bg = self.bg_color,
                                      highlightbackground = COLOR["dark blue"], highlightthickness = 5)
        self.frame_setting.pack_propagate(0)
        
        self.scale_length = 320
        self.slider_size = 46
        self.draw()
        
        self.frame_setting.pack()
    
    def draw_sound_scale(self):
        self.frame_volumn = tk.Frame(self.frame_setting, bg=self.bg_color, width = 600)
        self.frame_volumn.pack(side = tk.LEFT)
        
        self.label_font = (FONT, 30)
        self.label = tk.Label(self.frame_volumn, text="Volume:", bg=self.bg_color,
                              font = self.label_font, foreground = COLOR['dark green'])
        self.label.pack(side=tk.LEFT, padx= (30,20))

        self.scale = Scale(self.frame_volumn, length = self.scale_length, trough_color = COLOR['dark blue'], bg = self.bg_color,
                           slider_size = self.slider_size, slider_border_width = 3, slider_border_color = COLOR["dark blue"],          
                           slider_color = COLOR['light green'], active_slider_color = COLOR['dark green'],
                           command = self.update_volume)
        
        self.scale.slider_frame.pack(side=tk.LEFT, padx= (0,36))

    def draw(self):    
        #dessiner le titre
        self.title = tk.Label(self.frame_setting, bg = self.bg_color,
                              font = (FONT, 45, 'bold'), text = 'SETTING' , 
                              foreground = COLOR['dark blue'])
        self.title.pack(side = tk.TOP, pady = (20,0))
        
        
        #dessiner bouton "reset"
        self.frame_reset_button = tk.Frame(self.frame_setting, bg=self.bg_color, height = 62, width = self.width)
        self.frame_reset_button.pack_propagate(0)
        self.reset_button = tk.Button(self.frame_reset_button, width = 10, height= 2,
                                      text = "RESET DATA", font = (FONT, 30), 
                                      foreground = COLOR['lighter yellow'], activeforeground= COLOR["light yellow"], 
                                      bg = COLOR['dark green'], activebackground = COLOR['dark blue'],
                                      relief = 'flat')
        self.reset_button.pack()
        self.reset_button.bind('<Button-1>', self.reset_data_player)
        self.frame_reset_button.pack( side = tk.BOTTOM, pady=(10,25) )
        
        self.draw_sound_scale()
        
        #dessiner bouton "close"
        self.close_image = tk.PhotoImage(file = "close_button.png")
        self.close_button = tk.Button(self.frame_setting, image = self.close_image,
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
        self.frame_setting.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry(f"{WINDOWWIDTH}x{WINDOWHEIGHT}")
    sound_scale = SettingPopUp(root)
    root.mainloop()
