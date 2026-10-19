from src.model.function.function import Function
from PySide6.QtWidgets import QLabel
import picos as pc
import cvxopt as cvx
from src.util.helpers_2d import get_sin_params, sin_find_zeros, angle_to_euclidean
from src.util.helpers_general import projected_variance
'''class ProjectedVariance(Function):
    def __init__(self):
        return
    def get_value_from_pvs(self,project_variances, lambdas):
        return project_variances
    def to_string(self):
        return "||XM||²"
        #return QLabel("max<sub>M</sub> min<sub>X</sub> ||XM||<sub>F</sub><sup>2</sup>")
    def is_minmax(self):
        return False
    def get_sdp_constraint(self, group_summary, X, z, out_dim):
        A_i = pc.new_param(group_summary.label, cvx.matrix(group_summary.A))
        return ((A_i|X) >= z)
    def find_intersects(self, group1, group2):
        A = group1.A - group2.A
        offset, amplitude, frequency, phase = get_sin_params(A)
        alphas = sin_find_zeros(offset, amplitude,frequency,phase)
        intersect_1 = [ alphas[0] , self.get_value_from_pvs(projected_variance(angle_to_euclidean(alphas[0]), group1.A),group1.vals.sum()) ]
        intersect_2 = [ alphas[1] , self.get_value_from_pvs(projected_variance(angle_to_euclidean(alphas[1]), group1.A),group1.vals.sum()) ]
        return [intersect_1, intersect_2]
'''