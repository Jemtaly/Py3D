import sys

from PyQt5.QtWidgets import QApplication, QFileDialog, QGridLayout, QLineEdit, QMessageBox, QPushButton, QWidget

from core.engine import ObjectSpace
from core.plot3d import Graph, PlotMode
from .qt3d import QCamera, QSliderForm


class Plot3DWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plot3D")
        self.setMinimumSize(800, 600)
        self.graph = None
        self.objspc = ObjectSpace()
        self.camera = QCamera(self.objspc)
        self.ranges = QSliderForm()
        self.xmin_slider = self.ranges.newSlider("X min", -10, +10, -10)
        self.xmax_slider = self.ranges.newSlider("X max", -10, +10, +10)
        self.xseg_slider = self.ranges.newSlider("X num", 1, 100, 20)
        self.ymin_slider = self.ranges.newSlider("Y min", -10, +10, -10)
        self.ymax_slider = self.ranges.newSlider("Y max", -10, +10, +10)
        self.yseg_slider = self.ranges.newSlider("Y num", 1, 100, 20)
        self.camera.layout().addLayout(self.ranges)
        self.txtbox = QLineEdit()
        self.brplot = QPushButton("RPlot")
        self.bdplot = QPushButton("DPlot")
        self.breset = QPushButton("Reset")
        self.b_save = QPushButton("Save")
        self.brplot.clicked.connect(lambda: self.plot(PlotMode.RECT))  # Rect
        self.bdplot.clicked.connect(lambda: self.plot(PlotMode.DIAG))  # Diag
        self.breset.clicked.connect(lambda: self.reset())
        self.b_save.clicked.connect(lambda: self.save())
        layout = QGridLayout(self)
        layout.addWidget(self.camera, 0, 0, 1, 5)
        layout.addWidget(self.txtbox, 1, 0)
        layout.addWidget(self.brplot, 1, 1)
        layout.addWidget(self.bdplot, 1, 2)
        layout.addWidget(self.breset, 1, 3)
        layout.addWidget(self.b_save, 1, 4)

    def reset(self):
        self.graph = None
        self.objspc.clear()
        self.camera.update()

    def plot(self, mode: PlotMode):
        xmin = self.xmin_slider.value()
        xmax = self.xmax_slider.value()
        xseg = self.xseg_slider.value()
        ymin = self.ymin_slider.value()
        ymax = self.ymax_slider.value()
        yseg = self.yseg_slider.value()
        try:
            fn = eval("lambda x, y: " + self.txtbox.text())
            self.graph = Graph(fn, xmin, xmax, xseg, ymin, ymax, yseg)
        except Exception as e:
            QMessageBox.critical(self, e.__class__.__name__, str(e))
        else:
            self.graph.plot(self.objspc, mode)
            self.camera.update()

    def save(self):
        if self.graph is None:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Wavefront OBJ Files (*.obj);;All Files (*)")
        if not path:
            return
        try:
            with open(path, "w") as file:
                self.graph.save(file)
        except Exception as e:
            QMessageBox.critical(self, e.__class__.__name__, str(e))


def main():
    app = QApplication(sys.argv)
    window = Plot3DWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
