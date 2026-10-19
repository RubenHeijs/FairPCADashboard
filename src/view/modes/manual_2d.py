from src.view.scatter.scatter_2d import *
from PySide6.QtWidgets import *
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QObject, Slot
from src.view.control.control_panel import ControlPanel
from src.view.modes.group_initializer import GroupInitializer
from src.view.scatter.scatter_view_2d import ScatterView2D
from src.view.function.function_panel import FunctionPanel
from src.model.sample_coordinate_picker import SampleCoordinatePicker
from src.view.control.solution_control_2d import SolutionControl2D
from src.view.solution.solution_view_2d import SolutionView2D
from src.view.modes.group_collection import GroupCollection

class Manual2D(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.groups = GroupCollection()

        group_view_solution_splitter = QSplitter(Qt.Orientation.Horizontal)
        

        self.function_resolution = 100
        self.group_panel = ControlPanel(group_view_solution_splitter)
        self.group_panel.request_new_control_widget.connect(self.on_new_group_requested)

        scatter_function_splitter =  QSplitter(Qt.Orientation.Vertical)
        self.scatter_panel = ScatterView2D(scatter_function_splitter)
        self.function_panel = FunctionPanel(scatter_function_splitter,False)
        group_view_solution_splitter.addWidget(scatter_function_splitter)

        self.solution_panel = ControlPanel(group_view_solution_splitter)
        self.solution_panel.request_new_control_widget.connect(self.on_new_solution_requested)

        layout = QVBoxLayout(self)
        layout.addWidget(group_view_solution_splitter)
        layout.setContentsMargins(0, 0, 0, 0) 

        self.group_initializer = GroupInitializer()
        self.sample_coordinate_picker = SampleCoordinatePicker(1000, True)

    @Slot()
    def on_new_solution_requested(self):
        print('new solution requested')
        #add vecs to functions. Can I give two vectors to the group of functions because I just have two unique vectors per solution
        #I need a solver, probably per solution but feels redundant. And does every solution have an SDP solver/my solver or should I make one oracle that you can ask
        #I will make an oracle, but then the solution control needs to send it to solution object which asks the oracle to get the solution. so control updates the solution object and vice versa? And then control updates 
        color = QColor.fromHsv((0*99)%255,255,255)
        solution_control = SolutionControl2D(color)
        self.groups.group_added.connect(solution_control.add_group)

        
        solution_view = SolutionView2D(color,solution_control.get_solution_data())
        solution_control.solution_changed.connect(solution_view.on_solution_changed)
        solution_control.delete_requested.connect(solution_view.on_delete_requested)
        solution_control.color_changed.connect(solution_view.on_color_changed)
        for group in self.groups.get_groups():
            solution_control.add_group(group)
        self.solution_panel.add_control(solution_control)

        self.scatter_panel.add_solution_view(solution_view.make_next_solution_view())
        self.function_panel.add_solution_view(solution_view)

    @Slot()    
    def on_new_group_requested(self):
        group, group_control_view, group_scatter_view, group_function_view, group_pv_sampler= self.group_initializer.make_group_2d(self.sample_coordinate_picker.get_surface_data())
        self.groups.add_group(group, group_pv_sampler)
        self.sample_coordinate_picker.resolution_changed.connect(group_pv_sampler.on_resolution_changed)
        self.group_panel.add_control(group_control_view)
        self.scatter_panel.add_group(group_scatter_view)
        self.function_panel.add_group(group_function_view)
