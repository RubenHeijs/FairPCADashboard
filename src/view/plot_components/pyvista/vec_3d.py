import pyvista as pv
from pyvistaqt import QtInteractor
from src.util.helpers_general import *

class Vec3D:
    def __init__(self,plotter:pv.Plotter,color):
        self.is_two_sides = False
        self.is_highlighted = False
        self.is_visible = True
        self.color = qcolor_to_pv_color(color)
        self.vec = pv.Line([0,0,0], [0,0,0])
        self.actor = plotter.add_mesh(self.vec, color = self.color, line_width = 5, render_lines_as_tubes = True, reset_camera=False)
        self.silhouette_actor = plotter.add_silhouette(self.vec,color = self.color,line_width = 10)
        self.silhouette_actor.SetVisibility(False)

    def update(self, vec, center = np.array([0,0,0])):
        point_a = center-vec
        point_b = center+vec
        if(not self.is_two_sides):
            point_a = center
        self.vec.points[:] = [point_a, point_b]

    def set_color(self, color):
        self.color = qcolor_to_pv_color(color)
        self.actor.prop.color = self.color
        self.silhouette_actor.prop.color = self.color

    def highlight(self, highlight_on):
        if(highlight_on and self.is_visible):
            self.actor.prop.color = (255,255,255)
            self.silhouette_actor.SetVisibility(True)
        else:
            self.actor.prop.color = self.color
            self.silhouette_actor.SetVisibility(False)

    def set_visible(self, is_visible):
        self.is_visible = is_visible
        self.actor.SetVisibility(self.is_visible)
        self.silhouette_actor.SetVisibility(self.is_visible)

    def set_two_sides(self, is_two_sides):
        self.is_two_sides = is_two_sides

    def set_show_whole_plane(self, is_infinite):
        return #Could be nice to have?

    def decouple(self, plotter):
        plotter.remove_actor(self.actor)
        plotter.remove_actor(self.silhouette_actor)