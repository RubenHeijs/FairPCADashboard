import pyvista as pv
import numpy as np
from src.util.helpers_general import qcolor_to_pv_color

class StereographicProjection:
    def __init__(self,plotter:pv.Plotter,color, coords_inner, coords_outer, faces):
        points_inner = np.column_stack([coords_inner, np.zeros(coords_inner.shape[0])])
        points_outer = np.column_stack([coords_outer, np.zeros(coords_outer.shape[0])])

        self.inner_surface = pv.PolyData(points_inner, faces)
        self.outer_surface = pv.PolyData(points_outer, faces)

        self.actor_inner = plotter.add_mesh(self.inner_surface, color=qcolor_to_pv_color(color), show_edges=False)
        self.actor_outer = plotter.add_mesh(self.outer_surface, color=qcolor_to_pv_color(color), show_edges=False)


    def set_coords(self, coords_inner, coords_outer, faces):
        points_inner = np.column_stack([coords_inner, np.zeros(coords_inner.shape[0])])
        points_outer = np.column_stack([coords_outer, np.zeros(coords_outer.shape[0])])

        self.inner_surface.copy_from(pv.PolyData(points_inner, faces))
        self.outer_surface.copy_from(pv.PolyData(points_outer, faces))


    def update(self, Zs):
        self.inner_surface.points[:,2] = Zs
        self.outer_surface.points[:,2] = Zs

    def set_color(self, color):
        self.actor_inner.prop.color = qcolor_to_pv_color(color)
        self.actor_outer.prop.color = qcolor_to_pv_color(color)

    def highlight(self, highlight_on):
        return

    def set_visible(self, visible_on):
        self.actor_inner.SetVisibility(visible_on)
        self.actor_outer.SetVisibility(visible_on)

    def decouple(self, plotter):
        plotter.remove_actor(self.actor_inner)
        plotter.remove_actor(self.actor_outer)

