import numpy as np
import matplotlib as mpl
from src.util.helpers_general import qcolor_to_pv_color

class DotPlot2D:
    def __init__(self,ax,color):
        self.color = qcolor_to_pv_color(color)

        self.scatter = ax.scatter([0],[0], color = self.color)
        return
    def update(self, data):
        self.scatter.set_offsets(np.c_[data[0],data[1]])
        return
    def set_color(self, color):
        self.color = qcolor_to_pv_color(color)
        
        self.scatter.set_color(self.color)
        return

    def highlight(self, highlight_on):
        return

    def set_visible(self, visible_on):
        self.scatter.set_visible(visible_on)
    def remove(self):
        self.scatter.remove()