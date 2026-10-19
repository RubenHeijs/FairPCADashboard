import numpy as np
import matplotlib as mpl
from src.util.helpers_general import qcolor_to_pv_color
class Vec2D:
    def __init__(self,ax,color):
        self.color = qcolor_to_pv_color(color)
        vec = np.array([0,0])
        self.vec, = ax.plot([-vec[0],vec[0]],[-vec[1],vec[1]],color=qcolor_to_pv_color(color))
    
    def update(self, vec):
        self.vec.set_data([-vec[0],vec[0]],[-vec[1],vec[1]])
    
    def set_color(self, color):
        self.color = qcolor_to_pv_color(color)
        self.vec.set_color(self.color)

    def highlight(self, highlight_on):
        if highlight_on:
            self.vec.set_color('black')
        else:
            self.vec.set_color(self.color)

    def set_visible(self, visible_on):
        self.vec.set_visible(visible_on)

    def remove(self):
        self.vec.remove()