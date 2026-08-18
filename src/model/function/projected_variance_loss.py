from src.model.function.function import Function
from PySide6.QtWidgets import QLabel
class ProjectedVarianceLoss(Function):
    def __init__(self):
        return
    def get_value_from_pvs(self,project_variances, lambdas):
        return lambdas[0]-project_variances
    def to_string(self):
        return"||XM⁺||²-||XM||²"
        return QLabel("min<sub>M</sub> max<sub>X</sub> ||XM+||<sub>F</sub><sup>2</sup> ||XM||<sub>F</sub><sup>2</sup>")