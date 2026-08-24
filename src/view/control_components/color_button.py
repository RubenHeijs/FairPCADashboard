from PySide6.QtWidgets import *
from PySide6.QtCore import Slot
from PySide6.QtGui import QColor
from PySide6.QtCore import Signal
from src.util.helpers_3d import get_basis_from_angles
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