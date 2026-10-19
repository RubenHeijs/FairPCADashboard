
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Slot
from src.view.plot_components.matplotlib.mpl_widget import MplWidget

class ScatterView2D(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.group_scatters = []
        self.solution_views = []

        self.mpl_widget = MplWidget()
        self.mpl_widget.axes.set_axis_off()
        self.mpl_widget.axes.axis('equal')
        layout = QVBoxLayout(self)
        layout.addWidget(self.mpl_widget)

    @Slot()
    def on_render_requested(self):
        #self.mpl_widget.draw()
        lim = 1
        #self.mpl_widget.axes.set_xlim(-lim*1.1,lim*1.1)
        #self.mpl_widget.axes.set_ylim(-lim*1.1,lim*1.1)
        self.mpl_widget.axes.relim()
        self.mpl_widget.axes.autoscale_view()
        self.mpl_widget.axes.autoscale_view()

        self.mpl_widget.figure.canvas.draw_idle()


    def on_group_scatter_delete_requested(self, group_scatter):
        self.group_scatters.remove(group_scatter)
        group_scatter.remove_from_axes(self.mpl_widget.axes)

    def on_solution_delete_requested(self, solution_view):
        self.solution_views.remove(solution_view)
        solution_view.remove_from_axes(self.mpl_widget.axes)

    def add_group(self, group_scatter):
        group_scatter.add_to_axes(self.mpl_widget.axes)
        group_scatter.delete_requested.connect(lambda : self.on_group_scatter_delete_requested(group_scatter))
        group_scatter.render_requested.connect(self.on_render_requested)
        self.group_scatters.append(group_scatter)

    def add_solution_view(self, solution_view):
        solution_view.add_to_axes(self.mpl_widget.axes)
        solution_view.delete_requested.connect(lambda : self.on_solution_delete_requested(solution_view))
        solution_view.render_requested.connect(self.on_render_requested)
        self.solution_views.append(solution_view)
