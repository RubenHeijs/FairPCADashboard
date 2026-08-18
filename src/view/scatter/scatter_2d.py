from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MatplotlibWidget(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        self.figure = Figure()
        super().__init__(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.plot([0, 1, 2, 3], [0, 1, 4, 9])