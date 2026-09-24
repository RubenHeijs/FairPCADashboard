class Function:
    def __init__(self):
        return
    def get_value_from_pvs(self,project_variances, lambdas):
        return
    def to_string(self):
        return ""
    def to_oo_string(self):
        if self.is_minmax():
            return 'min max '+ self.to_string()
        else: 
            return 'max min '+ self.to_string()

    def is_minmax(self):
        return