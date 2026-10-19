from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Slot, QTimer
from PySide6.QtGui import QColor
from PySide6.QtCore import Signal
from src.util.helpers_3d import get_basis_from_angles
from src.view.control_components.color_button import ColorButton
from src.view.control_components.control_slider import ControlSlider
from src.model.function.reconstruction_error import ReconstructionError
from src.model.function.projected_variance_loss import ProjectedVarianceLoss
from src.model.algorithms.sdp import SDP
from src.model.algorithms.sweep import Sweep
from src.model.function.proportional_projected_variance_loss import ProportionalProjectedVarianceLoss
import numpy as np
from src.view.control_components.group_combobox import GroupComboBox
from src.view.control_components.group_combobox_item import GroupComboboxItem
from src.util.helpers_2d import *

class SolutionControl2D(QFrame):
    color_changed = Signal(QColor)
    solution_changed = Signal(object)
    delete_requested = Signal()

    alpha_hovered = Signal(bool)


    class SolutionData:
        #A projection result for our purposes is equivalent when the projection is inversed
        def __init__(self, euclidean, score):
            self.euclidean = euclidean

            self.angle = [euclidean_to_angle(self.euclidean)%np.pi, score]


    def __init__(self, init_color, parent = None, slider_resolution = 100):
        super(SolutionControl2D, self).__init__(parent)
        self.slider_resolution = slider_resolution
        self.setFrameShape(QFrame.Shape.StyledPanel)
        
        self.update_timer = QTimer(self)
        self.update_timer.setSingleShot(True)
        self.update_timer.setInterval(16)
        self.update_timer.timeout.connect(self.trigger_pending_update)

        self.grid = QGridLayout(self)
        self.grid.setVerticalSpacing(2)
        self.grid.setContentsMargins(5,0,5,0)

#        self.algorithms = [ProjectedVariance(), 
#                          ProjectedVarianceLoss(), 
#                          ProportionalProjectedVarianceLoss()]
        self.algorithms_picker = QComboBox()
        self.algorithms_picker.setFixedHeight(20)
        self.algorithms_picker.addItems(['Manual', 'SDP', 'k-group 2d -> 1d'])
        self.algorithms_picker.currentIndexChanged.connect(self.on_algorithm_selection_changed)
        self.grid.addWidget(self.algorithms_picker,0,0,1,1)

        self.functions = [ReconstructionError(), 
                          ProjectedVarianceLoss(), 
                          ProportionalProjectedVarianceLoss()]
        self.oo_picker = QComboBox()
        self.oo_picker.setFixedHeight(20)
        self.oo_picker.addItems([f.to_oo_string() for f in self.functions])
        self.oo_picker.currentIndexChanged.connect(self.on_oo_selection_changed)


        self.color_picker = ColorButton(init_color)
        self.color_picker.colorChanged.connect(self.on_change_color)
        self.grid.addWidget(self.color_picker, 8,1)
        self.grid.addWidget(QLabel('Select color'),8,0,alignment = Qt.AlignmentFlag.AlignRight)

        delete_button = QPushButton(icon = self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarCloseButton),text = '')
        delete_button.setFixedSize(24,24)
        delete_button.setToolTip("Close")
        delete_button.clicked.connect(self.delete_requested.emit)
        self.grid.addWidget(delete_button, 0,1)

        self.alpha_slider = ControlSlider('α',0.0, 2.0, unit = 'π' , init_val = 0, resolution = self.slider_resolution)
        self.alpha_slider.value_changed.connect(self.on_alpha_change)
        self.alpha_slider.hover.connect(self.alpha_hovered.emit)





        self.group_filter = GroupComboBox()
        self.group_filter.groups_changed.connect(self.on_groups_changed)
        self.manual_type = 0
        self.set_manual_view()
        #self.add_sliders()
        self.on_change_color(init_color)
        self.current_group_data_selection = []
        self.current_solution = self.SolutionData(np.array([1,0]),1)

    def add_group(self, group):
        self.group_filter.add_group_widget(GroupComboboxItem(group))

    @Slot(int)
    def on_algorithm_selection_changed(self, index):
        if index == 0:
            self.set_manual_view()
        else:
            self.set_algo_view()
            self.evaluate()

    @Slot(int)
    def on_oo_selection_changed(self, index):
        self.evaluate()

    def evaluate(self):
        if len(self.current_group_data_selection) >= 2:
            function = self.functions[self.oo_picker.currentIndex()]
            if self.algorithms_picker.currentIndex() == 1:
                solution, score = SDP().solve(groups= self.current_group_data_selection,
                                    function = function,
                                    in_dim = 2,
                                    out_dim = 1)
            elif self.algorithms_picker.currentIndex() == 2:
                solution, score = Sweep().solve(groups= self.current_group_data_selection,
                                    function = function,
                                    in_dim = 2,
                                    out_dim = 1)
            self.current_solution = self.SolutionData(solution[0],score)
            self.queue_update()
    @Slot(int)
    def on_manual_type_changed(self, index):
        self.manual_type = index
        self.set_manual_view()

    def set_manual_view(self):
        self.oo_picker.setParent(None)
        self.group_filter.setParent(None)
        self.grid.addWidget(self.alpha_slider,1,0,1,2)

 

    def set_algo_view(self):

        self.alpha_slider.setParent(None)
        self.grid.addWidget(self.oo_picker,1,0,1,2)
        self.grid.addWidget(self.group_filter,2,0,1,2)
    
        #self.grid.addWidget(self.beta_slider,3,0,1,2)            
    @Slot()
    def on_groups_changed(self, group_data):
        self.current_group_data_selection = group_data
        self.evaluate()

    @Slot(float)
    def on_alpha_change(self,val):
        self.current_solution = self.SolutionData(angle_to_euclidean(val*np.pi),1)   
        self.queue_update()

    
    @Slot(QColor)
    def on_change_color(self,col):
        self.alpha_slider.set_color(col)
        self.color_changed.emit(col)

    def queue_update(self):
        self.pending_update = self.current_solution
        if not self.update_timer.isActive():
            self.update_timer.start()

    def trigger_pending_update(self):            
        self.solution_changed.emit(self.pending_update)

    def get_solution_data(self):
        return self.current_solution