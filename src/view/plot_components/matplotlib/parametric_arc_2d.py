from src.util.helpers_general import qcolor_to_pv_color

class ParametricArc2D:
    def __init__(self,ax,color, vecs):
        self.color = qcolor_to_pv_color(color)
        self.base_vecs = vecs
        self.base_vecs_opp = vecs*-1
        self.upper_arc, = ax.plot(self.base_vecs[0],self.base_vecs[1],color=self.color)
        self.lower_arc, = ax.plot(self.base_vecs_opp[0],self.base_vecs_opp[1],color=self.color)

        self.color = color
        self.set_visible(False)
    def update(self, pvs):
        upper_vecs = self.base_vecs.T*pvs[:,None]
        lower_vecs = upper_vecs * -1
        self.lower_arc.set_data(lower_vecs[:,0],lower_vecs[:,1])
        self.upper_arc.set_data(upper_vecs[:,0],upper_vecs[:,1])
        
    def set_color(self, color):
        self.color = qcolor_to_pv_color(color)
        self.upper_arc.set_color(self.color)
        self.lower_arc.set_color(self.color)

    def highlight(self, highlight_on):
        if highlight_on:
            self.upper_arc.set_color('black')
            self.lower_arc.set_color('black') 
        else:
            self.upper_arc.set_color(self.color)
            self.lower_arc.set_color(self.color)

    def set_visible(self, visible_on):
        self.upper_arc.set_visible(visible_on)
        self.lower_arc.set_visible(visible_on)

    def remove(self):
        self.upper_arc.remove()
        self.lower_arc.remove()