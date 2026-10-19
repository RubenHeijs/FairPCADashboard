from src.util.helpers_general import qcolor_to_pv_color

class FunctionLine2D:
    def __init__(self,axes,color, Xs):
        self.color = qcolor_to_pv_color(color)
        self.line, = axes.plot(Xs,Xs*0,color = self.color)

    def update(self, ys):
        self.line.set_ydata(ys)
    
    def set_new_x(self, xs):
        self.line.set_data(xs, xs*0)

    def set_color(self, color):
        self.color = qcolor_to_pv_color(color)
        self.line.set_color(self.color)

    def highlight(self, highlight_on):
        if highlight_on:
            self.line.set_color('black')
        else:
            self.line.set_color(self.color)

    def set_visible(self, visible_on):
        self.line.set_visible(visible_on)
        
    def remove(self):
        self.line.remove()