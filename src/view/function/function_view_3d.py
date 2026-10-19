from PySide6.QtCore import *
from PySide6.QtWidgets import *
import numpy as np
from src.util.helpers_3d import *
import pyvista as pv
from pyvistaqt import QtInteractor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QHBoxLayout
from PySide6.QtCore import Slot
from src.model.function.reconstruction_error import ReconstructionError
from src.model.function.projected_variance_loss import ProjectedVarianceLoss
from src.model.function.proportional_projected_variance_loss import ProportionalProjectedVarianceLoss
class FunctionView3D(QWidget):
    new_function_view_requested = Signal()
    function_delete_requested = Signal(object)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(100)
        self.vbox = QVBoxLayout(self)
        self.control_hbox = QHBoxLayout()
        self.vbox.addLayout(self.control_hbox)


        self.functions = [ReconstructionError(), 
                          ProjectedVarianceLoss(), 
                          ProportionalProjectedVarianceLoss()]

        self.function_picker = QComboBox()
        self.function_picker.setFixedHeight(20)

        self.function_picker.addItems([f.to_string() for f in self.functions])
        self.function_picker.currentIndexChanged.connect(self.on_function_selection_changed)
        self.control_hbox.addWidget(self.function_picker)

        self.projection_picker = QComboBox()
        self.projection_picker.setMaximumSize(120,20)
        self.projection_picker.addItems(['Polar', 'Stereographic'])
        self.projection_picker.currentIndexChanged.connect(self.on_projection_selection_changed)
        self.control_hbox.addWidget(self.projection_picker)

        self.save_btn = QPushButton('s')
        self.save_btn.setFixedSize(20,20)
        self.save_btn.clicked.connect(self.on_save_clicked)
        self.control_hbox.addWidget(self.save_btn)

        self.close_btn = QPushButton('x')
        self.close_btn.setFixedSize(20,20)
        self.close_btn.clicked.connect(lambda :self.function_delete_requested.emit(self))
        self.control_hbox.addWidget(self.close_btn)

        self.add_btn = QPushButton('+')
        self.add_btn.setFixedSize(20,20)
        self.add_btn.clicked.connect(self.new_function_view_requested.emit)
        self.control_hbox.addWidget(self.add_btn)



        self.group_function_views = []
        self.solution_views = []
        self.plotter = QtInteractor(self)
        self.plotter.suppress_rendering = True
        
        self.vbox.addWidget(self.plotter.interactor)
        self.is_polar = True
        self.function = self.functions[self.function_picker.currentIndex()]
        self.initialize_camera_settings()
        self.cam_up_sign = 1
    def enforce_up(self,caller, event):
        if np.abs(self.plotter.camera.up[2]) >=0.001:
            self.plotter.camera.up = (0, 0, np.sign(self.plotter.camera.up[2]))
        
    def initialize_camera_settings(self):
        self.plotter.iren.add_observer('InteractionEvent', self.enforce_up)
        self.stereo_cam = pv.Camera()
        self.stereo_cam.focal_point = (0,0,0)
        self.stereo_cam.up = (0,0,1)
        self.stereo_cam.position = (2,3,6)

        self.polar_cam = pv.Camera()
        self.polar_cam.focal_point = (np.pi/2, 0, 0)
        self.polar_cam.up = (0,0,1)
        self.polar_cam.position = (6,2,5)
        self.plotter.camera = self.polar_cam
    def set_can_add(self, can_add):
        self.add_btn.setDisabled(not can_add)
    def set_can_close(self, can_close):
        self.close_btn.setDisabled(not can_close)

    @Slot()
    def on_save_clicked(self):
        print('Save screenshot')

    @Slot(int)
    def on_function_selection_changed(self, index):
        self.function = self.functions[index]
        for group_function_view in self.group_function_views:
            group_function_view.set_function(self.function)
     
    @Slot(int)
    def on_projection_selection_changed(self, index):
        if index == 0 and self.is_polar == False:
            self.stereo_cam = self.plotter.camera
            self.plotter.camera = self.polar_cam
            self.is_polar = True
            for solution_view in self.solution_views:
                solution_view.set_polar_mode()
        elif index == 1 and self.is_polar == True:
            self.polar_cam = self.plotter.camera
            self.plotter.camera = self.stereo_cam
            self.is_polar = False
            for solution_view in self.solution_views:
                solution_view.set_stereographic_mode()
        else: 
            #Nothing changed
            return
        for group_function_view in self.group_function_views:
            group_function_view.set_is_polar(self.is_polar)  
                  
    @Slot()
    def on_render_requested(self):
        self.plotter.suppress_rendering = False
        self.plotter.render()
        self.plotter.suppress_rendering = True
        
    def on_group_scatter_delete_requested(self, group_function_view):
        self.group_function_views.remove(group_function_view)
        group_function_view.remove_from_plotter(self.plotter)

    def on_solution_view_delete_requested(self, solution_view):
        self.solution_views.remove(solution_view)
        solution_view.remove_from_plotter(self.plotter)

    def add_group(self, group_function_view):

        group_function_view.add_to_plotter(self.plotter, self.is_polar, self.function)
        group_function_view.delete_requested.connect(lambda : self.on_group_scatter_delete_requested(group_function_view))
        group_function_view.render_requested.connect(self.on_render_requested)
        self.group_function_views.append(group_function_view)

    def add_solution_view(self, solution_view):# Not sure if this is the way to go. Maybe I can store a copy and add to different plotters?
        solution_view.add_to_plotter(self.plotter)
        if self.is_polar:
            solution_view.set_polar_mode()
        else:
            solution_view.set_stereographic_mode()
        solution_view.delete_requested.connect(lambda : self.on_solution_view_delete_requested(solution_view))
        solution_view.render_requested.connect(self.on_render_requested)
        self.solution_views.append(solution_view) 