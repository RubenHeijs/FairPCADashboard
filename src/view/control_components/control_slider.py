from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import  QPalette
from PySide6.QtCore import Signal
import numpy as np
from src.util.helpers_general import interpolate
class ControlSlider(QWidget):
    value_changed = Signal(float)
    hover = Signal(bool)
    def __init__(self,title,min, max, unit = "", parent = None, display_slider = True, resolution = 1000, init_val = 0):
        super(ControlSlider, self).__init__(parent)
        self.resolution = resolution
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
        self.slider.setRange(0,resolution)
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
        self.set_value(init_val)

    def on_slider_change(self,slider_val):
        val = interpolate(slider_val,0,self.resolution,self.min,self.max)
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
        slider_val = interpolate(val,self.min, self.max, 0, self.resolution)
        self.value_label.setText(str(np.round(val,2))+self.unit)
        self.slider.valueChanged.disconnect(self.on_slider_change) #Maybe theres a more elegant way to not trigger valueChanged
        self.slider.setValue(np.round(slider_val))
        self.slider.valueChanged.connect(self.on_slider_change)

    def get_value(self):
        return interpolate(self.slider.value(),0,self.resolution,self.min,self.max)

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
    

