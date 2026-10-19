from src.util.helpers_general import qcolor_to_pv_color

class FunctionPoint2D:
    def __init__(self,axes,color, with_line = False):
        self.has_line = with_line
        self.color = qcolor_to_pv_color(color)
        if self.has_line:
            self.line, = axes.plot([0,0],[0,0], color = self.color)
            self.crossing = axes.scatter(0.0, 0.0, color = self.color, marker='x',zorder = 5)
        else:
            self.crossing = axes.scatter(0.0, 0.0, color = self.color, zorder = 5)

        return
    def update(self, coord):
        self.crossing.set_offsets([coord])
        if self.has_line:
            self.line.set_data([coord[0],coord[0]], [0,coord[1]])
        return
    def set_color(self, color):
        self.color = qcolor_to_pv_color(color)

        self.crossing.set_color(self.color)
        if self.has_line:
            self.line.set_color(self.color)

    def highlight(self, highlight_on):
        if highlight_on:
            self.crossing.set_color('black')
            if self.has_line:
                self.line.set_color('black')
        else:
            self.crossing.set_color(self.color)
            if self.has_line:
                self.line.set_color(self.color)
    def set_visible(self, visible_on):
        self.crossing.set_visible(visible_on)
        if self.has_line:
            self.line.set_visible(visible_on)
    def remove(self):
        self.crossing.remove()
        if self.has_line:
            self.line.remove()
