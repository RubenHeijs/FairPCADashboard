from PySide6.QtCore import *
import numpy as np
from src.util.helpers_3d import *
'''
Uses coordinate information to augment group specific visualisation data with projected variances
'''
class GroupPVSampler(QObject):
    resolution_changed = Signal(object)
    group_changed = Signal(object)

    def __init__(self, init_group_summary_data, init_surface_data):
        super().__init__()
        self.surface_data = init_surface_data
        self.group_summary_data = init_group_summary_data
        self.group_summary_data.projected_variances = projected_variance(self.surface_data.vecs, self.group_summary_data.A)


    @Slot(object)
    def on_resolution_changed(self, surface_data):
        self.surface_data = surface_data
        self.resolution_changed.emit(self.surface_data)
        self.group_summary_data.projected_variances = projected_variance(self.surface_data.vecs, self.group_summary_data.A)
        self.group_changed.emit(self.group_summary_data)

    @Slot(object)
    def on_group_changed(self, group_summary_data):
        self.group_summary_data = group_summary_data
        self.group_summary_data.projected_variances = projected_variance(self.surface_data.vecs, self.group_summary_data.A)
        self.group_changed.emit(self.group_summary_data)

    def get_summary_data(self):
        return self.group_summary_data