import pyvista as pv
from PySide6.QtCore import Signal, QObject, Slot
from src.view.plot_components.pyvista.surface_vec_3d import SurfaceVec3D
from src.view.plot_components.pyvista.polar_projection import PolarProjection
from src.view.plot_components.pyvista.stereographic_projection import StereographicProjection
from src.util.helpers_3d import *
from PySide6.QtGui import QColor

class GroupFunctionView3D(QObject):
    render_requested = Signal()
    delete_requested = Signal()

    def __init__(self, color, init_vis_data, init_surface_data):
        super().__init__()

        self.color = color
        self.coupled = False
        self.surface_data = init_surface_data
        self.vis_data = init_vis_data

    def set_is_polar(self, is_polar):
        self.is_polar = is_polar
        if is_polar:
            self.vec_to_coord = euclidean_to_polar
        else:
            self.vec_to_coord = euclidean_to_stereographic
        if self.coupled:
            self.stereographic_view.set_visible(not self.is_polar)
            self.polar_view.set_visible(self.is_polar)   
            self.update()

    def set_function(self, function):
        self.function = function
        if (self.coupled):
            self.update()
    def add_to_plotter(self, plotter, initial_is_polar, initial_function):

        self.vec_1_view = SurfaceVec3D(plotter, self.color)
        self.vec_2_view = SurfaceVec3D(plotter, self.color)
        self.vec_3_view = SurfaceVec3D(plotter, self.color)
        self.stereographic_view = StereographicProjection(plotter, self.color, self.surface_data.stereographic[1], self.surface_data.stereographic[0], self.surface_data.stereographic_faces)
        self.polar_view = PolarProjection(plotter, self.color, self.surface_data.polar, self.surface_data.polar_faces)
        self.function = initial_function

        #self.intersection_view
        self.coupled = True 
        self.set_is_polar(initial_is_polar)

    def remove_from_plotter(self,plotter):
        self.vec_1_view.decouple(plotter)
        self.vec_2_view.decouple(plotter)
        self.vec_3_view.decouple(plotter)
        self.stereographic_view.decouple(plotter)
        self.polar_view.decouple(plotter)

        self.render_requested.emit()
        self.coupled = False 

    @Slot()
    def on_delete_requested(self):
        self.delete_requested.emit()

    @Slot(QColor)
    def on_color_changed(self,color):
        self.color = color
        if (self.coupled):
            self.vec_1_view.set_color(self.color)
            self.vec_2_view.set_color(self.color)
            self.vec_3_view.set_color(self.color)
            self.stereographic_view.set_color(self.color)
            self.polar_view.set_color(self.color)

            self.render_requested.emit()

    @Slot(bool)
    def on_var_hovered(self, is_hovering):
        if (self.coupled):
            self.vec_1_view.highlight(is_hovering)
            self.vec_2_view.highlight(is_hovering)
            self.vec_3_view.highlight(is_hovering)
            self.render_requested.emit()


    @Slot(bool)
    def on_vec_1_hovered(self, is_hovering):
        if (self.coupled):
            self.vec_1_view.highlight(is_hovering)
            self.render_requested.emit()

    @Slot(bool)
    def on_vec_2_hovered(self, is_hovering):
        if (self.coupled):
            self.vec_2_view.highlight(is_hovering)
            self.render_requested.emit()

    @Slot(bool)
    def on_vec_3_hovered(self, is_hovering):
        if (self.coupled):
            self.vec_3_view.highlight(is_hovering)
            self.render_requested.emit()

    def update(self):
        if (self.coupled):
            coords = self.vec_to_coord(self.vis_data.vecs)
            lambdas = self.vis_data.vals #/ np.sum(self.vis_data.vals)
            self.vec_1_view.update(coords[0], lambdas[0])
            self.vec_2_view.update(coords[1], lambdas[1])
            self.vec_3_view.update(coords[2], lambdas[2])
            if(self.is_polar):
                self.polar_view.update(self.function.get_value_from_pvs(self.vis_data.projected_variances,self.vis_data.vals))
            else:
                self.stereographic_view.update(self.function.get_value_from_pvs(self.vis_data.projected_variances,self.vis_data.vals))
            self.render_requested.emit()

    @Slot(object)
    def on_group_changed(self, vis_data):
        self.vis_data = vis_data
        self.update()
    @Slot(object)
    def on_resolution_changed(self, surface_data):
        self.surface_data = surface_data
        self.stereographic_view.set_coords(self.surface_data.stereographic[1], self.surface_data.stereographic[0], self.surface_data.stereographic_faces)
        self.polar_view.set_coords(self.surface_data.polar, self.surface_data.polar_faces)
        self.update()
