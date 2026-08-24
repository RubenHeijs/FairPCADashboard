import pyvista as pv
from pyvistaqt import QtInteractor
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Slot
from src.view.function.function_view import FunctionView

class FunctionPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.group_function_view_connectors = []
        self.function_views = []
        self.hbox = QVBoxLayout(self)

        self.f12_34_splitter = QSplitter(Qt.Orientation.Vertical)
        self.hbox.addWidget(self.f12_34_splitter)
        self.f1_2_splitter = QSplitter(Qt.Orientation.Horizontal, self.f12_34_splitter)
        self.f3_4_splitter = QSplitter(Qt.Orientation.Horizontal, self.f12_34_splitter)
        
        function = FunctionView(self.f1_2_splitter)
        function.function_delete_requested.connect(self.on_function_delete_requested)
        function.new_function_view_requested.connect(self.on_new_function_view_requested)
        self.function_views.append(function)

        self.max_n_views = 6
        self.update_arrangement()


    def on_group_function_view_connector_delete_requested(self, group_scatter):
        self.group_function_view_connectors.remove(group_scatter)
        #add cleanup
    def add_group(self, group_function_view_connector):
        group_function_view_connector.delete_requested.connect(lambda : self.on_group_function_view_connector_delete_requested(group_function_view_connector))
        self.group_function_view_connectors.append(group_function_view_connector)
        for function_view in self.function_views:
            function_view.add_group(group_function_view_connector.make_group_function_view())
    @Slot(object)
    def on_function_delete_requested(self, function):
        self.function_views.remove(function)
        function.setParent(None)
        function.deleteLater()
        self.update_arrangement()

    @Slot()
    def on_new_function_view_requested(self):
        function_view = FunctionView()
        function_view.function_delete_requested.connect(self.on_function_delete_requested)
        function_view.new_function_view_requested.connect(self.on_new_function_view_requested)
        for connector in self.group_function_view_connectors:
            function_view.add_group(connector.make_group_function_view())
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

