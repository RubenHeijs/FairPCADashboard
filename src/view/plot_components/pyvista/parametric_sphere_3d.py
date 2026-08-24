import pyvista as pv
from pyvistaqt import QtInteractor
from scipy.spatial import ConvexHull
import numpy as np
from src.util.helpers_general import *
class ParametricSphere3D:
    def __init__(self,plotter:pv.Plotter,color, base_points, faces):
        self.base_points = base_points
        self.sphere = pv.PolyData(self.base_points, faces)
        self.actor = plotter.add_mesh(self.sphere, color=qcolor_to_pv_color(color), opacity=0.6, reset_camera=False)
        self.actor_mirror = plotter.add_mesh(self.sphere, color=qcolor_to_pv_color(color), opacity=0.6, reset_camera=False)
        self.actor_mirror.SetScale(-1,-1,-1)
    def set_sphere_points(self, points, faces):
        self.base_points = points
        self.sphere.copy_from(pv.PolyData(self.base_points, faces))

    def update(self, vals):
        self.sphere.points = self.base_points * vals[:, None]

    def set_color(self, color):
        self.actor.prop.color = qcolor_to_pv_color(color)
        self.actor_mirror.prop.color = qcolor_to_pv_color(color)

    def highlight(self, highlight_on):
        return

    def set_visible(self, visible_on):
        self.actor.SetVisibility(visible_on)
        self.actor_mirror.SetVisibility(visible_on)

    def decouple(self, plotter):
        plotter.remove_actor(self.actor)
        plotter.remove_actor(self.actor_mirror)
