from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from src.view.scatter.scatter_2d import *
from PySide6.QtCore import Slot
import pandas as pd
import numpy as np
from src.view.control.polar_control import *
from src.view.control.control_panel import *
from src.model.group import *
from src.view.scatter.group_scatter_3d import *
from src.view.modes.group_initializer import GroupInitializer
from src.view.scatter.scatter_panel import ScatterPanel

class Manual2D(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        control_view_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        scatter_function_splitter =  QSplitter(Qt.Orientation.Vertical)
        self.scatter_panel = ScatterPanel(scatter_function_splitter)
        self.function_panel = MatplotlibWidget(scatter_function_splitter)

        self.control_panel = ControlPanel()
        #self.control_panel.request_new_control_widget.connect(self.add_group)
        control_view_splitter.addWidget(self.control_panel)
        control_view_splitter.addWidget(scatter_function_splitter)
        
        layout = QVBoxLayout(self)
        
        layout.addWidget(control_view_splitter)
        layout.setContentsMargins(0, 0, 0, 0) 
    