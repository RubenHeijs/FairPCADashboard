from src.model.function.function import Function
from PySide6.QtWidgets import QLabel

class ProjectedVariance(Function):
    def __init__(self):
        return
    def get_value_from_pvs(self,project_variances, lambdas):
        return project_variances
    def to_string(self):
        return "||XM||²"
        #return QLabel("max<sub>M</sub> min<sub>X</sub> ||XM||<sub>F</sub><sup>2</sup>")