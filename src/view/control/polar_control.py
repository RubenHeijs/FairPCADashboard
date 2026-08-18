from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Slot, QTimer
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Signal
from src.util.helpers_3d import get_basis_from_angles
import numpy as np
SLIDER_RESOLUTION = 1000
MIN_VARIANCE = 0.1
MAX_VARIANCE = 10

class PolarControl(QFrame):
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

    def __init__(self, name, init_color, parent = None):
        super(PolarControl, self).__init__(parent)
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
        self.beta = 0
        self.theta = 0

        self.l1 = 1/3  # >1/3
        self.l2 = (1 - self.l1)/2
        self.l3 = 1-(self.l1+self.l2)

        self.add_sliders()
        self.on_change_color(init_color)
        self.set_values(self.var, self.alpha, self.beta, self.theta, self.l1, self.l2, self.l3)

    def set_values(self, var, alpha, beta, theta, l1, l2, l3):
        self.var_slider.set_value(var)
        self.alpha_slider.set_value(alpha/np.pi)
        self.beta_slider.set_value(beta/np.pi)
        self.theta_slider.set_value(theta/np.pi)
        self.lambda_1_slider.set_value(l1)
        self.lambda_2_slider.set_value(l2)

    def add_sliders(self):
        self.var_slider = ControlSlider('σ<sup>2</sup>',MIN_VARIANCE, MAX_VARIANCE)
        self.var_slider.value_changed.connect(self.on_var_change)
        self.grid.addWidget(self.var_slider,1,0,1,2)
        self.var_slider.hover.connect(self.var_hovered.emit)

        self.alpha_slider = ControlSlider('α',0.0, 2.0, unit = 'π')
        self.alpha_slider.value_changed.connect(self.on_alpha_change)
        self.grid.addWidget(self.alpha_slider,2,0,1,2)
        self.alpha_slider.hover.connect(self.alpha_hovered.emit)

        self.beta_slider = ControlSlider('β',0.0, 2.0, unit = 'π')
        self.beta_slider.value_changed.connect(self.on_beta_change)
        self.grid.addWidget(self.beta_slider,3,0,1,2)
        self.beta_slider.hover.connect(self.beta_hovered.emit)

        self.theta_slider = ControlSlider('θ',0.0, 2.0, unit = 'π')
        self.theta_slider.value_changed.connect(self.on_theta_change)
        self.grid.addWidget(self.theta_slider,4,0,1,2)
        self.theta_slider.hover.connect(self.theta_hovered.emit)

        self.lambda_1_slider = ControlSlider('λ<sub>1</sub>', 1/3, 1.0 )
        self.lambda_1_slider.value_changed.connect(self.on_lambda_1_change)
        self.grid.addWidget(self.lambda_1_slider,5,0,1,2)
        self.lambda_1_slider.hover.connect(self.lambda_1_hovered.emit)

        self.lambda_2_slider = ControlSlider('λ<sub>2</sub>', 1/3, 1/3)
        self.lambda_2_slider.value_changed.connect(self.on_lambda_2_change)
        self.grid.addWidget(self.lambda_2_slider,6,0,1,2)
        self.lambda_2_slider.hover.connect(self.lambda_2_hovered.emit)

        self.lambda_3_slider = ControlSlider('λ<sub>3</sub>', 1/3, 1/3, display_slider=False)
        self.lambda_3_slider.value_changed.connect(self.on_lambda_3_change)
        self.grid.addWidget(self.lambda_3_slider,7,0,1,2)
        self.lambda_3_slider.hover.connect(self.lambda_3_hovered.emit)

    @Slot(float)
    def on_alpha_change(self,val):
        self.alpha = val*np.pi
        self.queue_update()
    @Slot(float)
    def on_beta_change(self,val):
        self.beta = val*np.pi
        self.queue_update()
    @Slot(float)
    def on_theta_change(self,val):
        self.theta = val*np.pi
        self.queue_update()
    @Slot(float)
    def on_var_change(self,val):
        self.var = val*np.pi
        self.queue_update()
    @Slot(float)
    def on_lambda_1_change(self,val):
        self.l1 = val
        self.lambda_2_slider.set_bounds_and_update_value((1-self.l1)*0.5, min(self.l1,1-self.l1))
    @Slot(float)
    def on_lambda_2_change(self,val):
        self.l2 = val
        self.lambda_3_slider.set_bounds_and_update_value(1.0-(self.l1+self.l2),1.0-(self.l1+self.l2))
    @Slot(float)
    def on_lambda_3_change(self,val):
        self.l3 = val
        self.queue_update()
    @Slot(QColor)
    def on_change_color(self,col):
        new_palette = self.name_label.palette()
        new_palette.setColor(QPalette.ColorRole.WindowText,col)
        self.name_label.setPalette(new_palette)

        self.var_slider.set_color(col)
        self.alpha_slider.set_color(col)
        self.beta_slider.set_color(col)
        self.theta_slider.set_color(col)
        self.lambda_1_slider.set_color(col)
        self.lambda_2_slider.set_color(col)
        self.lambda_3_slider.set_color(col)

        self.color_changed.emit(col)

    def queue_update(self):
        v1, v2, v3 = get_basis_from_angles(self.alpha, self.beta, self.theta)
        self.pending_e_vecs = [ v1, v2, v3 ]
        self.pending_e_vals = [self.l1, self.l2, self.l3]
        self.pending_var = self.var
        if not self.update_timer.isActive():
            self.update_timer.start()
    def trigger_pending_update(self):
        self.group_input_changed.emit(self.pending_e_vals, self.pending_e_vecs, self.pending_var)


from src.util.helpers_general import interpolate
class ControlSlider(QWidget):
    value_changed = Signal(float)
    hover = Signal(bool)
    def __init__(self,title,min, max, unit = "", parent = None, display_slider = True):
        super(ControlSlider, self).__init__(parent)
        self.unit = unit
        self.min = min
        self.max = max

        self.grid = QHBoxLayout(self)
        self.grid.setContentsMargins(0,3,0,3)

        self.text_label = QLabel(title)
        self.text_label.setFixedWidth(15)
        self.grid.addWidget(self.text_label,alignment = Qt.AlignmentFlag.AlignLeft)

        self.slider = QSlider(orientation = Qt.Orientation.Horizontal)
        self.slider.valueChanged.connect(self.on_slider_change)
        self.slider.setRange(0,SLIDER_RESOLUTION)
        self.grid.addWidget(self.slider)

        policy = self.slider.sizePolicy()
        policy.setRetainSizeWhenHidden(True)
        self.slider.setSizePolicy(policy)
        self.slider.setVisible(display_slider)
    
        self.value_label = QLabel('0')
        self.value_label.setFixedWidth(30)
        self.grid.addWidget(self.value_label,alignment = Qt.AlignmentFlag.AlignRight)

        self.hover_palette = self.text_label.palette()
        self.default_palette = self.text_label.palette()
    def on_slider_change(self,slider_val):
        val = interpolate(slider_val,0,SLIDER_RESOLUTION,self.min,self.max)
        self.value_label.setText(str(np.round(val,2))+self.unit)
        self.value_changed.emit(val)

    def set_color(self, color):
        self.hover_palette.setColor(QPalette.ColorRole.WindowText,color)

    def set_bounds_and_update_value(self, min, max):
        self.min = min
        self.max = max
        self.on_slider_change(self.slider.value())

    def set_value(self,val):
        val = max(min(val,self.max),self.min)
        slider_val = interpolate(val,self.min, self.max, 0, SLIDER_RESOLUTION)
        self.value_label.setText(str(np.round(val,2))+self.unit)
        self.slider.setValue(np.round(slider_val))

    def get_value(self):
        return interpolate(self.slider.value(),0,SLIDER_RESOLUTION,self.min,self.max)

    def enterEvent(self, event):
        self.text_label.setPalette(self.hover_palette)
        self.value_label.setPalette(self.hover_palette)

        self.hover.emit(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.text_label.setPalette(self.default_palette)
        self.value_label.setPalette(self.default_palette)
        self.hover.emit(False)
        super().leaveEvent(event)
    

class ColorButton(QPushButton):
    colorChanged = Signal(QColor)

    def __init__(self, color=QColor("white"), parent=None):
        super().__init__(parent)
        self.color = QColor()
        self.setColor(color)
        self.clicked.connect(self.pick_color)
        self.setFixedSize(24,24)
    def setColor(self, color):
        self.color = QColor(color)
        self.setStyleSheet(f"background-color: {self.color.name()};")

    def color(self):
        return self.color
    @Slot()
    def pick_color(self):
        chosen = QColorDialog.getColor(self.color, self.parent(), "Select Color")
        if chosen.isValid():
            self.setColor(chosen)
            self.colorChanged.emit(chosen)