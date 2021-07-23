import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from cs1lib import *

class Piece:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        
    def move(self, deltaX, deltaY):
        self.x += deltaX
        self.y += deltaY
    
    
    def draw(self, width, height):
        r, g, b = mcolors.to_rgb(self.color)
        set_fill_color(r, g, b)
        disable_stroke()
        x = (self.x/8) * width + (width/16)
        y = (self.y/8) * height + (height/16)
        draw_circle(x , y, self.radius)

    def drawText(self, score, width, height):
        fontSize = 60
        set_font_size(fontSize)
        set_fill_color(0, 0.5, 0)
        set_stroke_color(0, 0, 0.5)
        set_font_bold()
        x = (self.x/8) * width + (width/16)
        y = (self.y/8) * height + (height/16)
        draw_text(str(score), x, y )