from PySide6.QtCore import QObject, Signal, Slot
from src.util.helpers_3d import *
class Solution(QObject):
    solution_changed = Signal(object)
    def __init__(self, SDP_solver):
        super.__init__()
        self.SDP_solver = SDP_solver 
        
    def on_group_changed(self):
        #recalc solution
        self.solution_changed.emit()

    def set_function(self, function):
        self.function = function
        self.recalc()

    def set_algorithm(self, algorithm):
        self.set_algorithm = algorithm

    def recalc(self):
        if self.algorithm == 'manual':
            return
        elif self.algorithm == 'SDP':
            return
        elif self.algorithm == 'Tops':
            return 

    def set_euclidean(self, coord):
        self.euclidean = coord
        self.polar = euclidean_to_polar(coord)
        self.stereographic = euclidean_to_stereographic(coord)
        self.solution_changed.emit()

    def get_euclidean(self):
        return self.euclidean

    def set_polar(self, coord):
        self.polar = coord
        self.euclidean = polar_to_euclidean(coord)
        self.stereographic = euclidean_to_stereographic(self.euclidean)
        self.solution_changed.emit()

    def get_polar(self):
        return self.polar
    
    def set_stereographic(self, coord):
        self.stereographic = coord
        self.euclidean = stereographic_to_euclidean(coord)
        self.polar = euclidean_to_polar(self.euclidean)
        self.solution_changed.emit()

    def get_stereographic(self):
        return self.stereographic
    