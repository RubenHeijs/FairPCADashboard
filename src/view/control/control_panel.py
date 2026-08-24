from PySide6.QtWidgets import *
from src.view.scatter.scatter_2d import *
from PySide6.QtCore import Signal



class ControlPanel(QScrollArea):
    request_new_control_widget = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True) 
        self.setMinimumWidth(250)
        self.container = QWidget()
        self.control_container = QVBoxLayout(self.container)
        self.control_container.addStretch(1)  
        
        self.setWidget(self.container)
        plus_button = QPushButton('+')
        plus_button.clicked.connect(lambda: self.request_new_control_widget.emit())
        
        self.control_container.insertWidget(0,plus_button)

    def delete_widget(self,widget):
        self.control_container.removeWidget(widget)
        widget.close()

    def add_control(self, control_widget):
        control_widget.delete_requested.connect(lambda: self.delete_widget(control_widget))
        self.control_container.insertWidget(self.control_container.count() - 2, control_widget)
