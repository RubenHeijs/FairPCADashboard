from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QObject, Slot
from src.view.control.control_panel import ControlPanel
from src.view.modes.group_initializer import GroupInitializer
from src.view.scatter.scatter_panel import ScatterPanel
from src.view.function.function_panel import FunctionPanel
from src.model.sample_coordinate_picker import SampleCoordinatePicker
class Manual2D(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.groups = []
        self.group_pv_samplers = []
        group_view_solution_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        scatter_function_splitter =  QSplitter(Qt.Orientation.Vertical)
        self.scatter_panel = ScatterPanel(scatter_function_splitter)
        self.function_panel = FunctionPanel(scatter_function_splitter)

        self.group_panel = ControlPanel(group_view_solution_splitter)
        self.group_panel.request_new_control_widget.connect(self.on_new_group_requested)
        group_view_solution_splitter.addWidget(scatter_function_splitter)
        self.solution_panel = ControlPanel(group_view_solution_splitter)
        self.solution_panel.request_new_control_widget.connect(self.on_new_solution_requested)

        layout = QVBoxLayout(self)
        layout.addWidget(group_view_solution_splitter)
        layout.setContentsMargins(0, 0, 0, 0) 

        self.group_initializer = GroupInitializer()
        self.sample_coordinate_picker = SampleCoordinatePicker(5000)

    @Slot(object)
    def on_group_delete_requested(self, group):
        index = self.groups.index(group)
        del self.groups[index]
        del self.group_pv_samplers[index]

    @Slot()
    def on_new_solution_requested(self):
        print('new solution requested')
    def on_new_group_requested(self):
        group, group_control_view, group_scatter_view, group_function_view_connector, group_pv_sampler = self.group_initializer.make_group_3d(self.sample_coordinate_picker.get_surface_data())
        group.delete_requested.connect(self.on_group_delete_requested)
        self.groups.append(group)
        self.sample_coordinate_picker.resolution_changed.connect(group_pv_sampler.on_resolution_changed)
        self.group_panel.add_control(group_control_view)
        self.scatter_panel.add_group(group_scatter_view)
        self.function_panel.add_group(group_function_view_connector)
        self.group_pv_samplers.append(group_pv_sampler)