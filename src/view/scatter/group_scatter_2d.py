import pyvista as pv
from PySide6.QtCore import Signal, QObject, Slot
from src.view.plot_components.matplotlib.vec_2d import *
from src.view.plot_components.matplotlib.arc_2d import *
from src.view.plot_components.matplotlib.dot_plot_2d import*
from src.util.helpers_3d import *
from src.view.plot_components.matplotlib.parametric_arc_2d import*
from PySide6.QtGui import QColor

class GroupScatter2D(QObject):
    render_requested = Signal()
    delete_requested = Signal()
    def __init__(self, color, init_group_summary_data, init_sample_data):
        super().__init__()
        self.color = color
        self.coupled = False
        self.sample_data = init_sample_data
        self.group_summary_data = init_group_summary_data
        self.pcs_visible = True
        self.param_arc_visible = True
    def add_to_axes(self, axes):
        self.vec_1_view = Vec2D(axes, self.color)
        self.vec_2_view = Vec2D(axes, self.color)
        self.data_view = DotPlot2D(axes, self.color)
        self.alpha_view = Arc2D(axes,self.color)
        self.parametric_arc_view = ParametricArc2D(axes, self.color, self.sample_data.vecs.T)
        self.coupled = True 
        self.update()
        self.set_pcs_visible(False)
        self.set_param_arc_visible(False)

    def remove_from_axes(self,axes):
        self.vec_1_view.remove()
        self.vec_2_view.remove()
        self.data_view.remove()
        self.alpha_view.remove()
        self.parametric_arc_view.remove()

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
            self.data_view.set_color(self.color)
            self.alpha_view.set_color(self.color)
            self.parametric_arc_view.set_color(self.color)
            self.render_requested.emit()

    @Slot(bool)
    def on_var_hovered(self, is_hovering):
        if (self.coupled):
            self.vec_1_view.highlight(is_hovering)
            self.vec_2_view.highlight(is_hovering)
            self.render_requested.emit()

    @Slot(bool)
    def on_alpha_hovered(self, is_hovering):
        if (self.coupled):
            self.alpha_view.highlight(is_hovering)
            self.vec_1_view.highlight(is_hovering)
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

    @Slot(QObject)
    def on_data_changed(self, data):
        if (self.coupled):
            self.data_view.update(data.T)
            self.render_requested.emit()

    def set_pcs_visible(self, visible):
        self.vec_1_view.set_visible(visible)
        self.vec_2_view.set_visible(visible)
        self.pcs_visible = visible
        self.update()

    def set_param_arc_visible(self, visible):
        self.parametric_arc_view.set_visible(visible)
        self.param_arc_visible = visible
        self.update()
    @Slot(object)
    def on_group_changed(self, summary_data):
        self.group_summary_data = summary_data
        self.update()

    def update(self):
        if (self.coupled):
            vecs = self.group_summary_data.vecs.T@np.diag(self.group_summary_data.vals)
            self.vec_1_view.update(vecs.T[0]*self.pcs_visible)
            self.vec_2_view.update(vecs.T[1]*self.pcs_visible)
            #pc1 = self.vis_data.vecs[0]
            #x_vec = np.array([1,0,0])
            #self.alpha_view.update(x_vec,pc1)
            self.parametric_arc_view.update(self.group_summary_data.projected_variances*self.param_arc_visible)
#TODO add surface
            #self.parametric_surface_view.update(self.vis_data.projected_variances)

            self.render_requested.emit()
        
    @Slot(object)
    def on_resolution_changed(self, sample_data):
        self.sample_data = sample_data
        if (self.coupled):
            self.parametric_surface_view.set_base_vecs(self.sample_data.vecs)
        