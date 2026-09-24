from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Slot, QTimer
from PySide6.QtGui import QColor
from PySide6.QtCore import Signal
from src.util.helpers_3d import get_basis_from_angles
from src.view.control_components.color_button import ColorButton
from src.view.control_components.control_slider import ControlSlider
from src.model.function.projected_variance import ProjectedVariance
from src.model.function.projected_variance_loss import ProjectedVarianceLoss
from src.model.algorithms.sdp import SDP
from src.model.function.proportional_projected_variance_loss import ProportionalProjectedVarianceLoss
import numpy as np
from src.view.control_components.group_combobox import GroupComboBox
from src.view.control_components.group_combobox_item import GroupComboboxItem
from src.util.helpers_3d import *

class SolutionControl(QFrame):
    color_changed = Signal(QColor)
    solution_changed = Signal(object)
    delete_requested = Signal()

    alpha_hovered = Signal(bool)
    beta_hovered = Signal(bool)
    p_hovered = Signal(bool)
    q_hovered = Signal(bool)

    class SolutionData:
        #A projection result for our purposes is equivalent when the projection is inversed
        def __init__(self, euclidean):
            self.euclidean = euclidean
            self.euclidean_opp = -euclidean

            self.polar = euclidean_to_polar(self.euclidean)
            self.polar_opp = euclidean_to_polar(self.euclidean_opp)

            self.stereographic = euclidean_to_stereographic(self.euclidean)
            self.stereographic_opp = euclidean_to_stereographic(self.euclidean_opp)

    def __init__(self, init_color, parent = None, slider_resolution = 100):
        super(SolutionControl, self).__init__(parent)
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
        self.algorithms_picker.addItems(['Manual', 'SDP', 'Something else'])
        self.algorithms_picker.currentIndexChanged.connect(self.on_algorithm_selection_changed)
        self.grid.addWidget(self.algorithms_picker,0,0,1,1)

        self.functions = [ProjectedVariance(), 
                          ProjectedVarianceLoss(), 
                          ProportionalProjectedVarianceLoss()]
        self.oo_picker = QComboBox()
        self.oo_picker.setFixedHeight(20)
        self.oo_picker.addItems([f.to_oo_string() for f in self.functions])
        self.oo_picker.currentIndexChanged.connect(self.on_oo_selection_changed)


        self.manual_type_picker = QComboBox()
        self.manual_type_picker.setFixedHeight(20)
        self.manual_type_picker.addItems(['Polar', 'Stereographic'])
        self.manual_type_picker.currentIndexChanged.connect(self.on_manual_type_changed)

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

        self.beta_slider = ControlSlider('β',0.0, 2.0, unit = 'π', init_val = 0, resolution = self.slider_resolution)
        self.beta_slider.value_changed.connect(self.on_beta_change)
        self.beta_slider.hover.connect(self.beta_hovered.emit)

        self.stereographic_max = 1
        self.stereographic_min = -1 
        self.p_slider = ControlSlider('p',self.stereographic_min, self.stereographic_max,init_val = 0, resolution = self.slider_resolution)
        self.p_slider.value_changed.connect(self.on_p_change)
        self.p_slider.hover.connect(self.p_hovered.emit)
        self.q_slider = ControlSlider('q',self.stereographic_min, self.stereographic_max, init_val = 0, resolution = self.slider_resolution)
        self.q_slider.value_changed.connect(self.on_q_change)
        self.q_slider.hover.connect(self.q_hovered.emit)

        #self.group_filter = CheckableComboBox()
        #self.group_filter.addCheckableItem('group 1', checked = True)
        #self.group_filter.addCheckableItem('group 2', checked = True)
        self.group_filter = GroupComboBox()
        self.group_filter.groups_changed.connect(self.on_groups_changed)
        self.manual_type = 0
        self.set_manual_view()
        #self.add_sliders()
        self.on_change_color(init_color)
        self.current_group_data_selection = []
        self.current_solution = self.SolutionData(np.array([1,0,0]))
        self.update_stereographic_sliders()
        self.update_polar_sliders()

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
                solution = SDP().solve(groups= self.current_group_data_selection,
                                    function = function,
                                    in_dim = 3,
                                    out_dim = 1)
                self.current_solution = self.SolutionData(solution[0])
                self.queue_update()
    @Slot(int)
    def on_manual_type_changed(self, index):
        self.manual_type = index
        self.set_manual_view()

    def set_manual_view(self):
        self.oo_picker.setParent(None)
        self.group_filter.setParent(None)
        self.grid.addWidget(self.manual_type_picker,1,0,1,2)
        if self.manual_type == 0 : #polar
            self.p_slider.setParent(None)
            self.q_slider.setParent(None)
            self.grid.addWidget(self.alpha_slider,2,0,1,2)
            self.grid.addWidget(self.beta_slider,3,0,1,2)
        elif self.manual_type == 1: #stereographic
            self.alpha_slider.setParent(None)
            self.beta_slider.setParent(None)
            self.grid.addWidget(self.p_slider,2,0,1,2)
            self.grid.addWidget(self.q_slider,3,0,1,2)    

    def set_algo_view(self):
        self.manual_type_picker.setParent(None)
        self.p_slider.setParent(None)
        self.q_slider.setParent(None)
        self.alpha_slider.setParent(None)
        self.beta_slider.setParent(None)
        self.grid.addWidget(self.oo_picker,1,0,1,2)
        self.grid.addWidget(self.group_filter,2,0,1,2)
    
        #self.grid.addWidget(self.beta_slider,3,0,1,2)            
    @Slot()
    def on_groups_changed(self, group_data):
        self.current_group_data_selection = group_data
        self.evaluate()

    @Slot(float)
    def on_alpha_change(self,val):
        self.current_solution.polar[0] = val*np.pi
        self.current_solution = self.SolutionData(polar_to_euclidean(self.current_solution.polar))   
        self.update_stereographic_sliders()
        self.queue_update()

    @Slot(float)
    def on_beta_change(self,val):
        self.current_solution.polar[1] = val*np.pi
        self.current_solution = self.SolutionData(polar_to_euclidean(self.current_solution.polar))   
        self.update_stereographic_sliders()
        self.queue_update()
    
    def update_stereographic_sliders(self):
        #Either the stereographic representation of the projection or of its inverse lies in the unit circle. 
        #To avoid infite sliders we use the representation that lies in this circle
        coord = self.current_solution.stereographic
        if (coord[0] >= self.stereographic_min and coord[0] <= self.stereographic_max and
            coord[1] >= self.stereographic_min and coord[1] <= self.stereographic_max):
            self.p_slider.set_value(self.current_solution.stereographic[0])
            self.q_slider.set_value(self.current_solution.stereographic[1])
            self.editing_stereographic_opp = False
        else:
            self.p_slider.set_value(self.current_solution.stereographic_opp[0])
            self.q_slider.set_value(self.current_solution.stereographic_opp[1])
            self.editing_stereographic_opp = True

    def update_polar_sliders(self):
        self.alpha_slider.set_value(self.current_solution.polar[0])
        self.beta_slider.set_value(self.current_solution.polar[1])
    @Slot(float)

    def on_p_change(self,val):
        if(self.editing_stereographic_opp):
            self.current_solution.stereographic_opp[0] = val
            self.current_solution = self.SolutionData(-stereographic_to_euclidean(self.current_solution.stereographic_opp))
        else:
            self.current_solution.stereographic[0] = val
            self.current_solution = self.SolutionData(stereographic_to_euclidean(self.current_solution.stereographic))
        self.update_polar_sliders()
        self.queue_update()

    @Slot(float)
    def on_q_change(self,val):
        if(self.editing_stereographic_opp):
            self.current_solution.stereographic_opp[1] = val
            self.current_solution = self.SolutionData(-stereographic_to_euclidean(self.current_solution.stereographic_opp))
        else:
            self.current_solution.stereographic[1] = val
            self.current_solution = self.SolutionData(stereographic_to_euclidean(self.current_solution.stereographic))
        self.update_polar_sliders()
        self.queue_update()

    @Slot(QColor)
    def on_change_color(self,col):
        self.alpha_slider.set_color(col)
        self.beta_slider.set_color(col)
        self.p_slider.set_color(col)
        self.q_slider.set_color(col)

        self.color_changed.emit(col)

    def queue_update(self):
        self.pending_update = self.current_solution
        if not self.update_timer.isActive():
            self.update_timer.start()

    def trigger_pending_update(self):            
        self.solution_changed.emit(self.pending_update)

    def get_solution_data(self):
        return self.current_solution