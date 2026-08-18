import pyvista as pv
from pyvistaqt import QtInteractor
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Slot

class ScatterPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.group_scatters = []
        self.plotter = QtInteractor(self)
        self.plotter.suppress_rendering = True

        layout = QVBoxLayout(self)
        layout.addWidget(self.plotter.interactor)

    @Slot()
    def on_group_requests_render(self):
        self.plotter.suppress_rendering = False
        self.plotter.render()
        self.plotter.suppress_rendering = True

    @Slot(object)
    def on_group_scatter_delete_requested(self, group_scatter):
        self.group_scatters.remove(group_scatter)
        group_scatter.remove_from_plotter(self.plotter)

    def add_group(self, group_scatter):
        group_scatter.add_to_plotter(self.plotter)
        group_scatter.delete_requested.connect(lambda : self.on_group_scatter_delete_requested(group_scatter))
        group_scatter.render_requested.connect(self.on_group_requests_render)
        self.group_scatters.append(group_scatter)

        
