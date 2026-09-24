from src.model.function.function import Function
from PySide6.QtWidgets import QLabel
import picos as pc
import cvxopt as cvx

class ProjectedVariance(Function):
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
    