from src.model.function.function import Function
import numpy as np
class ProportionalProjectedVarianceLoss(Function):
    def __init__(self):
        return
    def get_value_from_pvs(self,project_variances, lambdas):
        return (lambdas[0]-project_variances)/np.sum(lambdas)
    def to_string(self):
        return "(||XM⁺||²-||XM||²)/||X||²"
        return ("min<sub>M</sub> max<sub>X</sub> (||XM+||<sub>F</sub><sup>2</sup> ||XM||<sub>F</sub><sup>2</sup>)/||X||<sub>F</sub><sup>2</sup>")