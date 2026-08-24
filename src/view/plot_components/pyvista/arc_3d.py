import pyvista as pv
from pyvistaqt import QtInteractor
import numpy as np
from src.util.helpers_general import *
class Arc3D:
    def __init__(self,plotter:pv.Plotter,color):
        self.arc = pv.CircularArc(pointa=[0, 0, 0], pointb=[0, 0, 0], center=[0, 0, 0])
        self.actor = plotter.add_mesh(self.arc, color = qcolor_to_pv_color(color), reset_camera=False)
        self.radius=0.5
        self.is_visible = True
        self.is_highlighted = False
    def update(self, vec1, vec2, center = np.array([0,0,0])):
        self.arc.copy_from(pv.CircularArc(
            pointa = vec1,
            pointb = vec2,
            center = center, 
            negative= np.dot(vec1,vec2)<0
        ))
        
    def set_color(self, color):
        self.actor.prop.color = qcolor_to_pv_color(color)

    def highlight(self, is_highlighted):
        self.is_highlighted = is_highlighted
        self.actor.SetVisibility(self.is_highlighted and self.is_visible )

    def set_visible(self, is_visible):
        self.is_visible = is_visible
        self.actor.SetVisibility(self.is_highlighted and self.is_visible )

    def decouple(self, plotter):
        plotter.remove_actor(self.actor)
