import pyvista as pv
from pyvistaqt import QtInteractor
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Slot

class ScatterPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.group_scatters = []
        self.solution_views = []
        self.plotter = QtInteractor(self)
        self.plotter.suppress_rendering = True

        layout = QVBoxLayout(self)
        layout.addWidget(self.plotter.interactor)
        self.plotter.camera.focal_point = (0, 0, 0)
        self.plotter.camera.up = (0,0,1)
        self.plotter.camera.position = (6,2,5)
        self.plotter.add_axes()
    @Slot()
    def on_render_requested(self):
        self.plotter.suppress_rendering = False
        self.plotter.render()
        self.plotter.suppress_rendering = True

    def on_group_scatter_delete_requested(self, group_scatter):
        self.group_scatters.remove(group_scatter)
        group_scatter.remove_from_plotter(self.plotter)

    def on_solution_delete_requested(self, solution_view):
        self.solution_views.remove(solution_view)
        solution_view.remove_from_plotter(self.plotter)

    def add_group(self, group_scatter):
        group_scatter.add_to_plotter(self.plotter)
        group_scatter.delete_requested.connect(lambda : self.on_group_scatter_delete_requested(group_scatter))
        group_scatter.render_requested.connect(self.on_render_requested)
        self.group_scatters.append(group_scatter)

    def add_solution_view(self, solution_view):
        solution_view.add_to_plotter(self.plotter)
        solution_view.delete_requested.connect(lambda : self.on_solution_delete_requested(solution_view))
        solution_view.render_requested.connect(self.on_render_requested)
        self.solution_views.append(solution_view)
