from PySide6.QtWidgets import *
from src.view.scatter.scatter_2d import *
import numpy as np
from src.view.control.polar_control_3d import *
from src.view.control.polar_control_2d import *
from src.view.control.control_panel import *
from src.model.group import *
from src.view.scatter.group_scatter_2d import *
from src.view.scatter.group_scatter_3d import *

from src.view.function.group_function_view_3d import GroupFunctionView3D
from src.view.function.group_function_view_2d import GroupFunctionView2D

from src.model.group_pv_sampler import GroupPVSampler

class GroupInitializer:
    def __init__(self):
        self.group_count = 1

    def get_color(self):
        return QColor.fromHsv((self.group_count*99)%255,255,255)

    def make_group(self, is_2d, surface_data):
        if (is_2d):
            return self.make_group_2d()
        else: 
            return self.make_group_3d(surface_data)
        
    def make_group_3d(self, surface_data):
        col = self.get_color()
        name = 'Group ' + str(self.group_count)

        group = Group(np.array([[1,0,0],[0,1,0],[0,0,1]]), name, col, 50)
        group_control_view = PolarControl3D(name, col)

        group_pv_sampler = GroupPVSampler(group.get_summary_data(), surface_data)

        group_scatter_view = GroupScatter3D(col, group_pv_sampler.get_summary_data(), surface_data)
        group_function_view = GroupFunctionView3D(col, group_pv_sampler.get_summary_data(), surface_data)

        #group - control_view linking
        #group_control_view.set_values() TODO IK HEB NOG NIKS OM DIT TE DOEN
        group_control_view.delete_requested.connect(group.on_delete_requested)
        group_control_view.group_input_changed.connect(group.update_by_eig)
        group_control_view.color_changed.connect(group.on_color_changed)
        #control_view - scatter_view linking
        group_control_view.delete_requested.connect(group_scatter_view.on_delete_requested)
        group_control_view.color_changed.connect(group_scatter_view.on_color_changed)
        group_control_view.var_hovered.connect(group_scatter_view.on_var_hovered)
        group_control_view.alpha_hovered.connect(group_scatter_view.on_alpha_hovered)
        group_control_view.beta_hovered.connect(group_scatter_view.on_beta_hovered)
        group_control_view.theta_hovered.connect(group_scatter_view.on_theta_hovered)
        group_control_view.lambda_1_hovered.connect(group_scatter_view.on_lambda_1_hovered)
        group_control_view.lambda_2_hovered.connect(group_scatter_view.on_lambda_2_hovered)
        group_control_view.lambda_3_hovered.connect(group_scatter_view.on_lambda_3_hovered)

        #group - scatter_view linking
        group.data_changed.connect(group_scatter_view.on_data_changed)

        #contol_view - function_view linking
        group_control_view.delete_requested.connect(group_function_view.on_delete_requested)
        group_control_view.color_changed.connect(group_function_view.on_color_changed)
        group_control_view.var_hovered.connect(group_function_view.on_var_hovered)
        group_control_view.alpha_hovered.connect(group_function_view.on_vec_1_hovered)
        group_control_view.beta_hovered.connect(group_function_view.on_vec_2_hovered)
        group_control_view.theta_hovered.connect(group_function_view.on_vec_3_hovered)
        group_control_view.lambda_1_hovered.connect(group_function_view.on_vec_1_hovered)
        group_control_view.lambda_2_hovered.connect(group_function_view.on_vec_2_hovered)
        group_control_view.lambda_3_hovered.connect(group_function_view.on_vec_3_hovered)

        #group - function_view linking
        group_pv_sampler.group_changed.connect(group_function_view.on_group_changed)

        #group - sampler
        group.group_changed.connect(group_pv_sampler.on_group_changed)

        #sampler - views
        group_pv_sampler.resolution_changed.connect(group_scatter_view.on_resolution_changed)
        group_pv_sampler.resolution_changed.connect(group_function_view.on_resolution_changed)
        group_pv_sampler.group_changed.connect(group_scatter_view.on_group_changed)
        group_pv_sampler.group_changed.connect(group_function_view.on_group_changed)

        self.group_count+=1

        return group,group_control_view,group_scatter_view, group_function_view, group_pv_sampler

    def make_group_2d(self, sample_data):
        col = self.get_color()
        name = 'Group ' + str(self.group_count)
        group = Group(np.eye(2), name, col,  70)
    
        group_pv_sampler = GroupPVSampler(group.get_summary_data(), sample_data)

        group_control_view = PolarControl2D(name, col,max_var= 100)

        group_scatter_view = GroupScatter2D(col, group_pv_sampler.get_summary_data(),sample_data)
        group_function_view = GroupFunctionView2D(col, group_pv_sampler.get_summary_data(), sample_data)

        #group - control_view linking
        group_control_view.delete_requested.connect(group.on_delete_requested)
        group_control_view.group_input_changed.connect(group.update_by_eig)
        group_control_view.color_changed.connect(group.on_color_changed)

                #control_view - scatter_view linking
        group_control_view.delete_requested.connect(group_scatter_view.on_delete_requested)
        group_control_view.color_changed.connect(group_scatter_view.on_color_changed)
        group_control_view.var_hovered.connect(group_scatter_view.on_var_hovered)
        group_control_view.alpha_hovered.connect(group_scatter_view.on_alpha_hovered)
        group_control_view.beta_hovered.connect(group_scatter_view.on_lambda_2_hovered)

        group_control_view.lambda_1_hovered.connect(group_scatter_view.on_lambda_1_hovered)
        group_control_view.lambda_2_hovered.connect(group_scatter_view.on_lambda_2_hovered)

        group.group_changed.connect(group_pv_sampler.on_group_changed)

        #group - scatter_view linking
        group.data_changed.connect(group_scatter_view.on_data_changed)
        #contol_view - function_view linking
        group_control_view.delete_requested.connect(group_function_view.on_delete_requested)
        group_control_view.color_changed.connect(group_function_view.on_color_changed)
        group_control_view.var_hovered.connect(group_function_view.on_var_hovered)
        group_control_view.alpha_hovered.connect(group_function_view.on_vec_1_hovered)
        group_control_view.beta_hovered.connect(group_function_view.on_vec_2_hovered)
        
        group_control_view.lambda_1_hovered.connect(group_function_view.on_vec_1_hovered)
        group_control_view.lambda_2_hovered.connect(group_function_view.on_vec_2_hovered)

        group_pv_sampler.resolution_changed.connect(group_scatter_view.on_resolution_changed)
        group_pv_sampler.resolution_changed.connect(group_function_view.on_resolution_changed)
        group_pv_sampler.group_changed.connect(group_scatter_view.on_group_changed)
        group_pv_sampler.group_changed.connect(group_function_view.on_group_changed)

        self.group_count+=1

        return group,group_control_view,group_scatter_view, group_function_view, group_pv_sampler