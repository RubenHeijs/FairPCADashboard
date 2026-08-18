from PySide6.QtCore import *
from PySide6.QtWidgets import *
import numpy as np
from src.util.helpers_3d import *
import pyvista as pv
from pyvistaqt import QtInteractor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QHBoxLayout
from PySide6.QtCore import Slot
from src.model.function.projected_variance import ProjectedVariance
from src.model.function.projected_variance_loss import ProjectedVarianceLoss
from src.model.function.proportional_projected_variance_loss import ProportionalProjectedVarianceLoss
class FunctionView(QWidget):
    new_function_view_requested = Signal()
    function_delete_requested = Signal(object)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vbox = QVBoxLayout(self)
        self.control_hbox = QHBoxLayout()
        self.vbox.addLayout(self.control_hbox)


        self.functions = [ProjectedVariance(), 
                          ProjectedVarianceLoss(), 
                          ProportionalProjectedVarianceLoss()]

        self.function_picker = QComboBox()
        self.function_picker.setFixedHeight(20)

        self.function_picker.addItems([f.to_string() for f in self.functions])
        self.function_picker.currentIndexChanged.connect(self.on_function_selection_changed)
        self.control_hbox.addWidget(self.function_picker)

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

        self.projection_picker = QComboBox()
        self.projection_picker.setFixedHeight(20)
        self.projection_picker.addItems(['Polar', 'Stereographic'])
        self.projection_picker.currentIndexChanged.connect(self.on_projection_selection_changed)
        self.control_hbox.addWidget(self.projection_picker)

        self.group_function_views = []

        self.plotter = QtInteractor(self)
        self.plotter.suppress_rendering = True
        
        self.vbox.addWidget(self.plotter.interactor)
        self.is_polar = True
        self.function = self.functions[self.function_picker.currentIndex()]
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
        if index == 0 :
            self.is_polar = True
        elif index == 1 :
            self.is_polar = False

        for group_function_view in self.group_function_views:
            group_function_view.set_is_polar(self.is_polar)  
                  
    @Slot()
    def on_group_requests_render(self):
        self.plotter.suppress_rendering = False
        self.plotter.render()
        self.plotter.suppress_rendering = True
        
    def on_group_scatter_delete_requested(self, group_function_view):
        self.group_function_views.remove(group_function_view)
        group_function_view.remove_from_plotter(self.plotter)

    def add_group(self, group_function_view):

        group_function_view.add_to_plotter(self.plotter, self.is_polar, self.function)

        group_function_view.delete_requested.connect(lambda : self.on_group_scatter_delete_requested(group_function_view))
        group_function_view.render_requested.connect(self.on_group_requests_render)
        self.group_function_views.append(group_function_view)