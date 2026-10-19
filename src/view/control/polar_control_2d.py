from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Slot, QTimer
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Signal
from src.util.helpers_2d import angle_to_euclidean
from src.view.control_components.color_button import ColorButton
from src.view.control_components.control_slider import ControlSlider
import numpy as np


class PolarControl2D(QFrame):
    color_changed = Signal(QColor)
    group_input_changed = Signal(object,object,float)
    delete_requested = Signal()

    var_hovered = Signal(bool)
    alpha_hovered = Signal(bool)
    beta_hovered = Signal(bool)
    theta_hovered = Signal(bool)
    lambda_1_hovered = Signal(bool)
    lambda_2_hovered = Signal(bool)
    lambda_3_hovered = Signal(bool)

    def __init__(self, name, init_color, parent = None, slider_resolution = 1000, min_var=0.1, max_var=20):
        self.min_var = min_var
        self.max_var = max_var
        self.slider_resolution = slider_resolution
        super(PolarControl2D, self).__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        
        self.update_timer = QTimer(self)
        self.update_timer.setSingleShot(True)
        self.update_timer.setInterval(16)
        self.update_timer.timeout.connect(self.trigger_pending_update)

        self.grid = QGridLayout(self)
        self.grid.setVerticalSpacing(2)
        self.grid.setContentsMargins(5,0,5,0)
        self.name_label = QLabel(name)
        self.grid.addWidget(self.name_label,0,0,1,1)

        self.color_picker = ColorButton(init_color)
        self.color_picker.colorChanged.connect(self.on_change_color)
        self.grid.addWidget(self.color_picker, 8,1)
        self.grid.addWidget(QLabel('Select color'),8,0,alignment = Qt.AlignmentFlag.AlignRight)

        delete_button = QPushButton(icon = self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarCloseButton),text = '')
        delete_button.setFixedSize(24,24)
        delete_button.setToolTip("Close")
        delete_button.clicked.connect(self.delete_requested.emit)
        self.grid.addWidget(delete_button, 0,1)


        self.var = 1
        self.alpha = 0
        self.beta = np.pi/2

        self.l1 = 1/2  # >1/3
        self.l2 = 1/2

        self.add_sliders()
        self.on_change_color(init_color)
        self.set_values(self.var, self.alpha, self.l1, self.l2)

    def set_values(self, var, alpha, l1, l2,):
        self.var = var
        self.alpha = alpha
        self.var_slider.set_value(var)
        self.alpha_slider.set_value(alpha/np.pi)
        beta = (alpha+(np.pi/2))%np.pi
        self.beta_slider.set_value(beta/np.pi)
        self.lambda_1_slider.set_value(l1)

    def add_sliders(self):
        self.var_slider = ControlSlider('σ<sup>2</sup>',self.min_var, self.max_var, resolution = self.slider_resolution)
        self.var_slider.value_changed.connect(self.on_var_change)
        self.grid.addWidget(self.var_slider,1,0,1,2)
        self.var_slider.hover.connect(self.var_hovered.emit)

        self.alpha_slider = ControlSlider('α',0.0, 2.0, unit = 'π' , resolution = self.slider_resolution)
        self.alpha_slider.value_changed.connect(self.on_alpha_change)
        self.grid.addWidget(self.alpha_slider,2,0,1,2)
        self.alpha_slider.hover.connect(self.alpha_hovered.emit)

        self.beta_slider = ControlSlider('β',0.0, 2.0, unit = 'π', resolution = self.slider_resolution, display_slider=False)
        self.grid.addWidget(self.beta_slider,3,0,1,2)
        self.beta_slider.hover.connect(self.beta_hovered.emit)


        self.lambda_1_slider = ControlSlider('λ<sub>1</sub>', 0.5, 1.0, resolution = self.slider_resolution )
        self.lambda_1_slider.value_changed.connect(self.on_lambda_1_change)
        self.grid.addWidget(self.lambda_1_slider,4,0,1,2)
        self.lambda_1_slider.hover.connect(self.lambda_1_hovered.emit)

        self.lambda_2_slider = ControlSlider('λ<sub>2</sub>', 0, 0.5, resolution = self.slider_resolution,display_slider=False)
        self.grid.addWidget(self.lambda_2_slider,5,0,1,2)
        self.lambda_2_slider.hover.connect(self.lambda_2_hovered.emit)



    @Slot(float)
    def on_alpha_change(self,val):
        self.alpha = val*np.pi
        self.beta = (self.alpha+(np.pi/2))%(2*np.pi)
        self.beta_slider.set_value(self.beta/np.pi)
        self.queue_update()

    @Slot(float)
    def on_var_change(self,val):
        self.var = val
        self.queue_update()

    @Slot(float)
    def on_lambda_1_change(self,val):
        self.l1 = val
        self.l2 = 1-val
        self.lambda_2_slider.set_value(self.l2)
        self.queue_update()

        #self.lambda_2_slider.set_bounds_and_update_value((1-self.l1), min(self.l1,1-self.l1))
    

    @Slot(QColor)
    def on_change_color(self,col):
        new_palette = self.name_label.palette()
        new_palette.setColor(QPalette.ColorRole.WindowText,col)
        self.name_label.setPalette(new_palette)

        self.var_slider.set_color(col)
        self.alpha_slider.set_color(col)
        self.beta_slider.set_color(col)
        self.lambda_1_slider.set_color(col)
        self.lambda_2_slider.set_color(col)

        self.color_changed.emit(col)

    def queue_update(self):
        v1 = angle_to_euclidean(self.alpha)
        v2 = angle_to_euclidean(self.beta)
        self.pending_e_vecs = [ v1, v2 ]
        self.pending_e_vals = [self.l1, self.l2]
        self.pending_var = self.var
        if not self.update_timer.isActive():
            self.update_timer.start()
    def trigger_pending_update(self):
        self.group_input_changed.emit(self.pending_e_vals, self.pending_e_vecs, self.pending_var)

