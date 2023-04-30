import tkinter as tk

class Scale:
    def __init__(self, root, length, slider_size, slider_border_color, slider_border_width, trough_color, slider_color, active_slider_color):
        self.slider_frame = tk.Frame(root)
        
        self.slider_border_width = slider_border_width
        self.length = length
        self.slider_size = slider_size
        self.slider_size_no_border = self.slider_size - 2*self.slider_border_width
        self.slider_border_color = slider_border_color
        
        self.trough_color = trough_color
        self.slider_color = slider_color
        self.active_slider_color = active_slider_color

        self.canvas = tk.Canvas(self.slider_frame, width=self.length, height=self.slider_size, borderwidth= 0, highlightthickness=0)
        self.canvas.pack()

        # Dessiner le creux
        trough_height = 8
        trough_width = self.length
        self.trough_x1 = self.slider_size / 2
        self.trough_x2 = self.length - self.slider_size / 2
        trough_y = (self.slider_size - trough_height) / 2
        self.canvas.create_rectangle(self.trough_x1, trough_y, self.trough_x2, trough_y + trough_height, fill=self.trough_color)

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
 
    def on_slider_release(self, event):
        self.canvas.itemconfig(self.slider, fill=self.slider_color)

    def get_value_slider(self):
        self.value = (self.centre_slider - self.trough_x1) / (self.trough_x2 - self.trough_x1)
        if self.value < 0: self.value = 0
        if self.value > 1: self.value = 1