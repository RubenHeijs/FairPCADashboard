from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtGui import QColor
from src.view.function.group_function_view_3d import GroupFunctionView3D

'''
Each group has one of these. It can make new group specific function views that listen to group changes. Forwards relevant signals. 
'''
class GroupFunctionViewConnector(QObject):
    color_changed = Signal(QColor)
    delete_requested = Signal()
    var_hovered = Signal(bool)
    vec_1_hovered = Signal(bool)
    vec_2_hovered = Signal(bool)
    vec_3_hovered = Signal(bool)
    resolution_changed = Signal(object)
    group_changed = Signal(object)

    def __init__(self, color, init_vis_data, init_surface_data):
        super().__init__()
        self.color = color        
        self.surface_data = init_surface_data
        self.vis_data = init_vis_data
        
    def make_group_function_view(self):
        group_function_view = GroupFunctionView3D(self.color, self.vis_data, self.surface_data)
        #connect
        self.color_changed.connect(group_function_view.on_color_changed)
        self.var_hovered.connect(group_function_view.on_var_hovered)
        self.vec_1_hovered.connect(group_function_view.on_vec_1_hovered)
        self.vec_2_hovered.connect(group_function_view.on_vec_2_hovered)
        self.vec_3_hovered.connect(group_function_view.on_vec_3_hovered)
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
        self.color_changed.emit(color)

    @Slot(bool)
    def on_var_hovered(self, is_hovering):
        self.var_hovered.emit(is_hovering)


    @Slot(bool)
    def on_vec_1_hovered(self, is_hovering):
        self.vec_1_hovered.emit(is_hovering)


    @Slot(bool)
    def on_vec_2_hovered(self, is_hovering):
        self.vec_2_hovered.emit(is_hovering)


    @Slot(bool)
    def on_vec_3_hovered(self, is_hovering):
        self.vec_3_hovered.emit(is_hovering)


    @Slot(object)
    def on_group_changed(self, vis_data ):
        self.vis_data = vis_data
        self.group_changed.emit(self.vis_data)
    @Slot(object)
    def on_resolution_changed(self, surface_info):
        self.surface_info = surface_info
        self.resolution_changed.emit(self.surface_info)