import pyvista as pv
from PySide6.QtCore import Signal, QObject, Slot
from src.view.plot_components.matplotlib.function_point_2d import FunctionPoint2D
from src.view.plot_components.matplotlib.function_line_2d import FunctionLine2D
from src.util.helpers_2d import *
from PySide6.QtGui import QColor

class GroupFunctionView2D(QObject):
    render_requested = Signal()
    color_changed = Signal(QColor)
    delete_requested = Signal()
    var_hovered = Signal(bool)
    vec_1_hovered = Signal(bool)
    vec_2_hovered = Signal(bool)
    resolution_changed = Signal(object)
    group_changed = Signal(object)
    def __init__(self, color, init_group_summary_data, init_sample_data):
        super().__init__()
        
        self.color = color
        self.coupled = False
        self.sample_data = init_sample_data

        self.group_summary_data = init_group_summary_data

    
    def set_function(self, function):
        self.function = function
        if (self.coupled):
            self.update()
    def add_to_axes(self, axes, initial_function):

        self.vec_1_view = FunctionPoint2D(axes, self.color, False)
        self.vec_2_view = FunctionPoint2D(axes, self.color, False)
        self.function_line_view = FunctionLine2D(axes, self.color, self.sample_data.angles)
        self.function = initial_function

        #self.intersection_view
        self.coupled = True 

    def remove_from_axes(self,axes):
        self.vec_1_view.remove()
        self.vec_2_view.remove()
        self.function_line_view.remove()

        self.render_requested.emit()
        self.coupled = False

    def make_next_group_function_view(self):
        group_function_view = GroupFunctionView2D(self.color, self.group_summary_data, self.sample_data)
        #connect
        self.color_changed.connect(group_function_view.on_color_changed)
        self.var_hovered.connect(group_function_view.on_var_hovered)
        self.vec_1_hovered.connect(group_function_view.on_vec_1_hovered)
        self.vec_2_hovered.connect(group_function_view.on_vec_2_hovered)
        self.delete_requested.connect(group_function_view.on_delete_requested)
        self.group_changed.connect(group_function_view.on_group_changed)
        self.resolution_changed.connect(group_function_view.on_resolution_changed)
        return group_function_view
    
    @Slot()
    def on_delete_requested(self):
        self.delete_requested.emit()

    @Slot(QColor)
    def on_color_changed(self,color):
        self.color = color
        if (self.coupled):
            self.vec_1_view.set_color(self.color)
            self.vec_2_view.set_color(self.color)
            self.function_line_view.set_color(self.color)
            self.render_requested.emit()
        self.color_changed.emit(color)

    @Slot(bool)
    def on_var_hovered(self, is_hovering):
        if (self.coupled):
            self.vec_1_view.highlight(is_hovering)
            self.vec_2_view.highlight(is_hovering)

            self.render_requested.emit()
        self.var_hovered.emit(is_hovering)


    @Slot(bool)
    def on_vec_1_hovered(self, is_hovering):
        if (self.coupled):
            self.vec_1_view.highlight(is_hovering)
            self.render_requested.emit()
        self.vec_1_hovered.emit(is_hovering)

    @Slot(bool)
    def on_vec_2_hovered(self, is_hovering):
        if (self.coupled):
            self.vec_2_view.highlight(is_hovering)
            self.render_requested.emit()
        self.vec_2_hovered.emit(is_hovering)


    def update(self):
        if (self.coupled):
            pc1_alpha = euclidean_to_angle(self.group_summary_data.vecs[0])%np.pi
            pc2_alpha = euclidean_to_angle(self.group_summary_data.vecs[1])%np.pi
            lambdas = self.group_summary_data.vals #/ np.sum(self.vis_data.vals)
            self.vec_1_view.update([pc1_alpha, self.function.get_value_from_pvs(lambdas[0],self.group_summary_data.vals)])
            self.vec_2_view.update([pc2_alpha, self.function.get_value_from_pvs(lambdas[1],self.group_summary_data.vals)])
            
            self.function_line_view.update(self.function.get_value_from_pvs(self.group_summary_data.projected_variances,self.group_summary_data.vals))
            
            self.render_requested.emit()

    @Slot(object)
    def on_group_changed(self, summary_data):
        self.group_summary_data= summary_data
        self.group_changed.emit(self.group_summary_data)
        self.update()
    @Slot(object)
    def on_resolution_changed(self, sample_data):
        self.sample_data = sample_data
        self.function_line_view.set_new_x(self.surface_data.angles)
        self.resolution_changed.emit(self.sample_data)
        self.update()

    