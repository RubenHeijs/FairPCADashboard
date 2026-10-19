import pyvista as pv
from pyvistaqt import QtInteractor
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Slot
from src.view.function.function_view_3d import FunctionView3D
from src.view.function.function_view_2d import FunctionView2D

class FunctionPanel(QWidget):
    def __init__(self, parent=None, is_3d = False):
        super().__init__(parent)
        self.is_3d = is_3d

        self.group_function_views = []
        self.function_views = []
        self.solution_views = []
        self.hbox = QVBoxLayout(self)

        self.f12_34_splitter = QSplitter(Qt.Orientation.Vertical)
        self.hbox.addWidget(self.f12_34_splitter)
        self.f1_2_splitter = QSplitter(Qt.Orientation.Horizontal, self.f12_34_splitter)
        self.f3_4_splitter = QSplitter(Qt.Orientation.Horizontal, self.f12_34_splitter)

        self.max_n_views = 6

        self.on_new_function_view_requested()



    def on_group_function_view_delete_requested(self, group_function_view):
        self.group_function_views.remove(group_function_view)
        #add cleanup (done?)

    def add_group(self, group_function_view):
        group_function_view.delete_requested.connect(lambda : self.on_group_function_view_delete_requested(group_function_view))
        self.group_function_views.append(group_function_view)
        for function_view in self.function_views:
            function_view.add_group(group_function_view.make_next_group_function_view())

    def on_solution_view_delete_requested(self, solution_view):
        self.solution_views.remove(solution_view)
        #add cleanup (done?)
    def add_solution_view(self, solution_view):
        solution_view.delete_requested.connect(lambda : self.on_solution_view_delete_requested(solution_view))
        self.solution_views.append(solution_view)
        for function_view in self.function_views:
            function_view.add_solution_view(solution_view.make_next_solution_view())
    
    @Slot(object)
    def on_function_delete_requested(self, function):
        self.function_views.remove(function)
        function.setParent(None)
        function.deleteLater()
        self.update_arrangement()

    @Slot()
    def on_new_function_view_requested(self):
        if self.is_3d:
            function_view = FunctionView3D()
        else :
            function_view = FunctionView2D()
        function_view.function_delete_requested.connect(self.on_function_delete_requested)
        function_view.new_function_view_requested.connect(self.on_new_function_view_requested)
        for solution_view in self.solution_views:
            function_view.add_solution_view(solution_view.make_next_solution_view())
        for group_function_view in self.group_function_views:
            function_view.add_group(group_function_view.make_next_group_function_view())
        self.function_views.append(function_view)
        self.f3_4_splitter.addWidget(function_view)
        self.update_arrangement()

    def update_arrangement(self):
        for view in self.function_views:
            view.set_can_add(len(self.function_views) < self.max_n_views)
            view.set_can_close(len(self.function_views) > 1)           
        while(self.f3_4_splitter.count()>self.f1_2_splitter.count()
              or self.f1_2_splitter.count()<2 and self.f3_4_splitter.count()>0):
            function = self.f3_4_splitter.widget(0)
            self.f1_2_splitter.addWidget(function)

