from PySide6.QtWidgets import QMainWindow, QSplitter, QScrollArea, QWidget, QVBoxLayout, QPushButton, QTabBar, QTabWidget
from PySide6.QtCore import Qt
from src.view.scatter.scatter_2d import *
from src.view.modes.init_dialogue import *
from PySide6.QtCore import Slot
from src.view.modes.data_2d import *
from src.view.modes.data_3d import *
from src.view.modes.manual_2d import *
from src.view.modes.manual_3d import *

class MainWindow(QMainWindow):
    def __init__(self):
        self.manual_2d_counter = 1
        self.manual_3d_counter = 1
        super().__init__()
        self.setWindowTitle("Fair PCA Dashboard")
        self.resize(800, 600)



        self.tab_widget = QTabWidget()
        #tab_widget.addTab(control_view_splitter,'Free11')
        add_button = QPushButton('+')
        add_button.pressed.connect(self.add_new_tab)
        self.tab_widget.setCornerWidget(add_button,Qt.Corner.TopRightCorner)
        #Quicker for debugging
        self.tab_widget.addTab(Manual2D(), 'man2d')

        self.setCentralWidget(self.tab_widget)

    @Slot()
    def add_new_tab(self):
        self.tab_widget.addTab(InitDialogue(self.apply_selection), 'New tab')
        self.tab_widget.setCurrentIndex(self.tab_widget.count()-1)
    @Slot(QWidget,int,object,object,object)
    def apply_selection(self, widget_to_replace, mode, df=None, sensitive_feature=None, features=None ):
        tab_i = self.tab_widget.indexOf(widget_to_replace)
        if (mode == 0 ): # manual 2d
            tab = Manual2D()
            title = 'Manual 2D (' + str(self.manual_2d_counter) + ')'
            self.manual_2d_counter+=1
        elif (mode == 1 ): #manual 3d
            tab = Manual3D()
            title = 'Manual 3D (' + str(self.manual_3d_counter)  + ')'
            self.manual_3d_counter+=1
        elif (mode == 2 ): #input data 2d
            tab = Data2D(df,sensitive_feature,features)
            title = sensitive_feature + ' 2D'
        elif (mode == 3 ): #input data 3d
            tab = Data3D(df,sensitive_feature,features)
            title = sensitive_feature = ' 3D'

        self.tab_widget.removeTab(tab_i)
        self.tab_widget.insertTab(tab_i, tab,title)
        self.tab_widget.setCurrentIndex(tab_i)
        

