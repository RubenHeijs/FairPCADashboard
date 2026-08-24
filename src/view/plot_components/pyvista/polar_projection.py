import pyvista as pv
from pyvistaqt import QtInteractor
from scipy.spatial import ConvexHull
import numpy as np
from src.util.helpers_general import *
class PolarProjection:
    def __init__(self,plotter:pv.Plotter,color, coords, faces):
        points = np.column_stack([coords, np.zeros(coords.shape[0])])

        self.surface = pv.PolyData(points, faces)
        self.actors = []
        coords = [[-1,-1], [-1,0], [-1,1],
                  [0,-1], [0,0],    [0,1],
                  [1,-1], [1,0],  [1,1]] 
        coords = [[0,0], [0,-1]]
        for coord in coords:
            self.add_copy(plotter, color, coord[0], coord[1])
    def add_copy(self,plotter,color, x, y ):
        edges = False
        scale = 1
        if np.abs(y)%2==1:
            x+=1
            edges = True
            scale = -1
        actor = plotter.add_mesh(self.surface, color=qcolor_to_pv_color(color), show_edges=False, reset_camera=False)
        actor.SetScale(scale,1,1)        
        actor.SetPosition(np.pi*x, np.pi*y,0)
        self.actors.append(actor)

    def set_coords(self, coords, faces):
        points = np.column_stack([coords, np.zeros(coords.shape[0])])
        self.surface.copy_from(pv.PolyData(points, faces))

    def update(self, Zs):
        self.surface.points[:,2] = Zs

    def set_color(self, color):
        for actor in self.actors:
            actor.prop.color = qcolor_to_pv_color(color)

    def highlight(self, highlight_on):
        return

    def set_visible(self, visible_on):
        for actor in self.actors:
            actor.SetVisibility(visible_on)

    def decouple(self, plotter):
        for actor in self.actors:
            plotter.remove_actor(actor)

