import pyvista as pv
from pyvistaqt import QtInteractor
import numpy as np
from src.util.helpers_general import *
class DotPlot3D:
    def __init__(self,plotter:pv.Plotter,color):
        self.n = 2
        self.scatter = pv.PolyData(np.array([[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]))
        self.actor = plotter.add_points(self.scatter, render_points_as_spheres = True, color =  qcolor_to_pv_color(color), point_size = 10)
    def update(self, data):

        if(data.shape[1]!=self.n):
            self.n = data.shape[1]
            self.scatter.copy_from(pv.PolyData(data))
        else:
            self.scatter.points[:]= data

    def set_color(self, color):
        self.actor.prop.color = qcolor_to_pv_color(color)

    def highlight(self, highlight_on):
        return

    def set_visible(self, visible_on):
        self.actor.SetVisibility(visible_on)

    def decouple(self, plotter):
        plotter.remove_actor(self.actor)

