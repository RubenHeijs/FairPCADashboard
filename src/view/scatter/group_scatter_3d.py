import pyvista as pv
from PySide6.QtCore import Signal, QObject, Slot
from src.view.plot_components.pyvista.vec_3d import*
from src.view.plot_components.pyvista.arc_3d import*
from src.view.plot_components.pyvista.dot_plot_3d import*
from src.util.helpers_3d import *
from src.view.plot_components.pyvista.parametric_sphere_3d import*
from PySide6.QtGui import QColor

class GroupScatter3D(QObject):
    render_requested = Signal()
    delete_requested = Signal()
    def __init__(self, color, init_vis_data, init_surface_data):
        super().__init__()
        self.color = color
        self.coupled = False
        self.surface_data = init_surface_data
        self.vis_data = init_vis_data
        
    def add_to_plotter(self, plotter):
        self.vec_1_view = Vec3D(plotter, self.color)
        self.vec_2_view = Vec3D(plotter, self.color)
        self.vec_3_view = Vec3D(plotter, self.color)
        self.data_view = DotPlot3D(plotter, self.color)
        self.alpha_view = Arc3D(plotter,self.color)
        self.beta_view = Arc3D(plotter,self.color)
        self.beta_ghost_vec_view = Vec3D(plotter, self.color)
        self.theta_view = Arc3D(plotter,self.color)
        self.theta_ghost_vec_view = Vec3D(plotter, self.color)
        self.parametric_surface_view = ParametricSphere3D(plotter, self.color, self.surface_data.vecs, self.surface_data.vec_faces)
        self.update()
        self.coupled = True 

    def remove_from_plotter(self,plotter):
        self.vec_1_view.decouple(plotter)
        self.vec_2_view.decouple(plotter)
        self.vec_3_view.decouple(plotter)
        self.data_view.decouple(plotter)
        self.alpha_view.decouple(plotter)
        self.beta_view.decouple(plotter)
        self.beta_ghost_vec_view.decouple(plotter)
        self.theta_view.decouple(plotter)
        self.theta_ghost_vec_view.decouple(plotter)
        self.parametric_surface_view.decouple(plotter)

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
            self.data_view.set_color(self.color)
            self.alpha_view.set_color(self.color)
            self.beta_view.set_color(self.color)
            self.theta_view.set_color(self.color)
            self.parametric_surface_view.set_color(self.color)
            self.render_requested.emit()

    @Slot(bool)
    def on_var_hovered(self, is_hovering):
        if (self.coupled):
            self.vec_1_view.highlight(is_hovering)
            self.vec_2_view.highlight(is_hovering)
            self.vec_3_view.highlight(is_hovering)
            self.render_requested.emit()

    @Slot(bool)
    def on_alpha_hovered(self, is_hovering):
        if (self.coupled):
            self.alpha_view.highlight(is_hovering)
            self.vec_1_view.highlight(is_hovering)
            self.render_requested.emit()

    @Slot(bool)
    def on_beta_hovered(self, is_hovering):
        if (self.coupled):
            self.beta_view.highlight(is_hovering)
            self.beta_ghost_vec_view.set_visible(is_hovering)

            self.vec_1_view.highlight(is_hovering)
            self.render_requested.emit()

    @Slot(bool)
    def on_theta_hovered(self, is_hovering):
        if (self.coupled):
            self.theta_view.highlight(is_hovering)
            self.theta_ghost_vec_view.set_visible(is_hovering)
            self.vec_2_view.highlight(is_hovering)
            self.vec_3_view.highlight(is_hovering)
            self.render_requested.emit()

    @Slot(bool)
    def on_lambda_1_hovered(self, is_hovering):
        if (self.coupled):
            self.vec_1_view.highlight(is_hovering)
            self.render_requested.emit()

    @Slot(bool)
    def on_lambda_2_hovered(self, is_hovering):
        if (self.coupled):
            self.vec_2_view.highlight(is_hovering)
            self.render_requested.emit()

    @Slot(bool)
    def on_lambda_3_hovered(self, is_hovering):
        if (self.coupled):
            self.vec_3_view.highlight(is_hovering)
            self.render_requested.emit()

    @Slot(QObject)
    def on_data_changed(self, data):
        if (self.coupled):
            self.data_view.update(data)
            self.render_requested.emit()


    @Slot(object)
    def on_group_changed(self, vis_data):
        self.vis_data = vis_data
        self.update()
    def update(self):
        if (self.coupled):
            vecs = self.vis_data.vecs.T@np.diag(self.vis_data.vals)
            self.vec_1_view.update(vecs.T[0])
            self.vec_2_view.update(vecs.T[1])
            self.vec_3_view.update(vecs.T[2])

            pc1 = self.vis_data.vecs[0]
            x_vec = np.array([1,0,0])
            y_vec = np.array([0,1,0])
            self.alpha_view.update(x_vec,pc1)

            beta_center = np.dot(x_vec,pc1)*x_vec 
            beta_b = beta_center + np.linalg.norm(beta_center-pc1)*y_vec
            self.beta_view.update(pc1, beta_b, beta_center)
            self.beta_ghost_vec_view.update(beta_b)

            pc2 = self.vis_data.vecs[1]
            theta_a = get_up_orth(pc1)
            self.theta_view.update(theta_a, pc2)
            self.theta_ghost_vec_view.update(theta_a)

            self.parametric_surface_view.update(self.vis_data.projected_variances)

            self.render_requested.emit()
        

    @Slot(object)
    def on_resolution_changed(self, surface_data):
        self.surface_data = surface_data
        if (self.coupled):
            self.parametric_surface_view.set_sphere_points(self.surface_data.vecs, self.surface_data.vec_faces)
        