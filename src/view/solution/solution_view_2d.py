from PySide6.QtCore import Signal, QObject, Slot
from src.view.plot_components.matplotlib.vec_2d import*
from PySide6.QtGui import QColor
from src.view.plot_components.matplotlib.function_point_2d import *
class SolutionView2D(QObject):
    render_requested = Signal()
    delete_requested = Signal()
    color_changed = Signal(QColor)
    solution_changed = Signal(object)
    
    def __init__(self, color, init_solution_data):
        super().__init__()
        self.color = color
        self.coupled = False
        self.solution_data = init_solution_data
        self.mode = 0

    def set_euclidean_mode(self):
        self.mode = 0
        if (self.coupled):
            self.function_point.update(0.0 )

        self.update_mode()

    def set_function_mode(self):
        self.mode = 1
        if (self.coupled):
            self.function_point.update(self.solution_data.angle )
        self.update_mode()

    def update_mode(self):
        if (self.coupled):
            self.euclidean_vec.set_visible(self.mode == 0)

            self.function_point.set_visible(self.mode == 1)

            self.render_requested.emit()
    def add_to_axes(self, axes):
        self.euclidean_vec = Vec2D(axes, self.color)

        self.function_point = FunctionPoint2D(axes, self.color, True)
        
        self.coupled = True
        self.update_mode()

    def remove_from_axes(self,axes):
        self.euclidean_vec.remove()

        self.function_point.remove()
        self.render_requested.emit()
        self.coupled = False 

    @Slot()
    def on_delete_requested(self):
        self.delete_requested.emit()

    @Slot(QColor)
    def on_color_changed(self,color):
        self.color = color
        if (self.coupled):

            self.euclidean_vec.set_color(self.color)

            self.function_point.set_color(self.color)

            self.render_requested.emit()

        self.color_changed.emit(color)

    @Slot(object)
    def on_solution_changed(self, solution_data):
        self.solution_data = solution_data
        self.update()
        self.solution_changed.emit(solution_data)

    def update(self):
        if (self.coupled):
            self.euclidean_vec.update(self.solution_data.euclidean)

            if (self.mode == 1):
                self.function_point.update(self.solution_data.angle )


            self.render_requested.emit()

    def make_next_solution_view(self):
        new_solution_view = SolutionView2D(self.color,self.solution_data)
        self.delete_requested.connect(new_solution_view.on_delete_requested) 
        self.color_changed.connect(new_solution_view.on_color_changed) 
        self.solution_changed.connect(new_solution_view.on_solution_changed)
        return new_solution_view 