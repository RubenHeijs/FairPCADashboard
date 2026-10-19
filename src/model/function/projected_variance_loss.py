from src.model.function.function import Function
import picos as pc
import cvxopt as cvx
from PySide6.QtWidgets import QLabel
from src.util.helpers_2d import get_sin_params, sin_find_zeros, angle_to_euclidean
from src.util.helpers_general import projected_variance


class ProjectedVarianceLoss(Function):
    def __init__(self):
        return
    def get_value_from_pvs(self,project_variances, lambdas):
        return lambdas[0]-project_variances

    def to_string(self):
        return"||XM⁺||²-||XM||²"
        return QLabel("min<sub>M</sub> max<sub>X</sub> ||XM+||<sub>F</sub><sup>2</sup> ||XM||<sub>F</sub><sup>2</sup>")
    def evaluate(self, vec, group):
        return self.get_value_from_pvs(projected_variance(vec, group.A),group.vals)
    def is_minmax(self):
        return True
    def get_sdp_constraint(self, group_summary, X, z, out_dim):
        A_i = pc.new_param(group_summary.label, cvx.matrix(group_summary.A))
        return (group_summary.vals[0:out_dim].sum()-(A_i|X) <= z)
    def find_intersects(self, group1, group2):
        A = group2.A - group1.A
        offset, amplitude, frequency, phase = get_sin_params(A)
        offset = offset + (group1.vals[0] - group2.vals[0])
        alphas = sin_find_zeros(offset, amplitude,frequency,phase)
        intersect_1 = [ alphas[0] , self.evaluate(angle_to_euclidean(alphas[0]), group1) ]
        intersect_2 = [ alphas[1] , self.evaluate(angle_to_euclidean(alphas[1]), group1) ]
        return [intersect_1, intersect_2]