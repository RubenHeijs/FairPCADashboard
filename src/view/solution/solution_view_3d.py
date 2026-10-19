import pyvista as pv
from PySide6.QtCore import Signal, QObject, Slot
from src.view.plot_components.pyvista.vec_3d import*
from src.view.plot_components.pyvista.arc_3d import*
from src.view.plot_components.pyvista.dot_plot_3d import*
from src.util.helpers_3d import *
from src.view.plot_components.pyvista.parametric_sphere_3d import*
from PySide6.QtGui import QColor
from src.view.plot_components.pyvista.surface_vec_3d import *
class SolutionView3D(QObject):
    render_requested = Signal()
    delete_requested = Signal()
    color_changed = Signal(QColor)
    solution_changed = Signal(object)
    
    def __init__(self, color, init_solution_data):
        super().__init__()
        self.color = color
        self.coupled = False
        self.solution_data = init_solution_data
        self.mode = 0

    def set_euclidean_mode(self):
        self.mode = 0
        self.update_mode()

    def set_stereographic_mode(self):
        self.mode = 1
        self.update_mode()

    def set_polar_mode(self):
        self.mode = 2
        self.update_mode()

    def update_mode(self):
        if (self.coupled):
            self.euclidean_vec.set_visible(self.mode == 0)
            self.euclidean_vec_opp.set_visible(self.mode == 0)

            self.stereographic_vec.set_visible(self.mode == 1)
            self.stereographic_vec_opp.set_visible(self.mode == 1)

            self.polar_vec.set_visible(self.mode == 2)
            self.polar_vec_opp.set_visible(self.mode == 2)

            self.render_requested.emit()
    def add_to_plotter(self, plotter):
        self.euclidean_vec = Vec3D(plotter, self.color)
        self.euclidean_vec_opp = Vec3D(plotter, self.color)

        self.stereographic_vec = SurfaceVec3D(plotter, self.color)
        self.stereographic_vec_opp = SurfaceVec3D(plotter, self.color)

        self.polar_vec = SurfaceVec3D(plotter, self.color)
        self.polar_vec_opp = SurfaceVec3D(plotter, self.color)

        self.coupled = True
        self.update_mode()

    def remove_from_plotter(self,plotter):
        self.euclidean_vec.decouple(plotter)
        self.euclidean_vec_opp.decouple(plotter)

        self.stereographic_vec.decouple(plotter)
        self.stereographic_vec_opp.decouple(plotter)

        self.polar_vec.decouple(plotter)
        self.polar_vec_opp.decouple(plotter)
        self.render_requested.emit()
        self.coupled = False 

    @Slot()
    def on_delete_requested(self):
        self.delete_requested.emit()

    @Slot(QColor)
    def on_color_changed(self,color):
        self.color = color
        if (self.coupled):

            self.euclidean_vec.set_color(self.color)
            self.euclidean_vec_opp.set_color(self.color)

            self.stereographic_vec.set_color(self.color)
            self.stereographic_vec_opp.set_color(self.color)

            self.polar_vec.set_color(self.color)
            self.polar_vec_opp.set_color(self.color)

            self.render_requested.emit()

        self.color_changed.emit(color)

    @Slot(object)
    def on_solution_changed(self, solution_data):
        self.solution_data = solution_data
        self.update()
        self.solution_changed.emit(solution_data)

    def update(self):
        if (self.coupled):
            self.euclidean_vec.update(self.solution_data.euclidean)
            self.euclidean_vec_opp.update(self.solution_data.euclidean_opp)

            self.stereographic_vec.update(self.solution_data.stereographic, 3)
            self.stereographic_vec_opp.update(self.solution_data.stereographic_opp,3)

            self.polar_vec.update(self.solution_data.polar, 3)
            self.polar_vec_opp.update(self.solution_data.polar_opp, 3)

            self.render_requested.emit()

    def make_next_solution_view(self):
        new_solution_view = SolutionView3D(self.color,self.solution_data)
        self.delete_requested.connect(new_solution_view.on_delete_requested) 
        self.color_changed.connect(new_solution_view.on_color_changed) 
        self.solution_changed.connect(new_solution_view.on_solution_changed)
        return new_solution_view 