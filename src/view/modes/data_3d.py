from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from src.view.scatter.scatter_2d import *
from PySide6.QtCore import Slot
import pandas as pd
import numpy as np

class Data3D(QWidget):

    def __init__(self,parent=None):
        super().__init__(parent)