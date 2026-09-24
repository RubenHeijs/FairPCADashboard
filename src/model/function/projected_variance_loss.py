from src.model.function.function import Function
import picos as pc
import cvxopt as cvx
from PySide6.QtWidgets import QLabel
class ProjectedVarianceLoss(Function):
    def __init__(self):
        return
    def get_value_from_pvs(self,project_variances, lambdas):
        return lambdas[0]-project_variances
    def to_string(self):
        return"||XM⁺||²-||XM||²"
        return QLabel("min<sub>M</sub> max<sub>X</sub> ||XM+||<sub>F</sub><sup>2</sup> ||XM||<sub>F</sub><sup>2</sup>")

    def is_minmax(self):
        return True
    def get_sdp_constraint(self, group_summary, X, z, out_dim):
        A_i = pc.new_param(group_summary.label, cvx.matrix(group_summary.A))
        return (group_summary.vals[0:out_dim].sum()-(A_i|X) <= z)
    