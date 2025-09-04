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
        self.umin_slider = self.ranges.newSlider("u min", -10, +10, -10)
        self.umax_slider = self.ranges.newSlider("u max", -10, +10, +10)
        self.useg_slider = self.ranges.newSlider("u num", 1, 100, 20)
        self.vmin_slider = self.ranges.newSlider("v min", -10, +10, -10)
        self.vmax_slider = self.ranges.newSlider("v max", -10, +10, +10)
        self.vseg_slider = self.ranges.newSlider("v num", 1, 100, 20)
        self.camera.layout().addLayout(self.ranges)
        self.x_edit = QLineEdit()
        self.y_edit = QLineEdit()
        self.z_edit = QLineEdit()
        self.x_edit.setPlaceholderText("x(u, v)")
        self.y_edit.setPlaceholderText("y(u, v)")
        self.z_edit.setPlaceholderText("z(u, v)")
        self.brplot = QPushButton("RPlot")
        self.bdplot = QPushButton("DPlot")
        self.breset = QPushButton("Reset")
        self.b_save = QPushButton("Save")
        self.brplot.clicked.connect(lambda: self.plot(PlotMode.RECT))  # Rect
        self.bdplot.clicked.connect(lambda: self.plot(PlotMode.DIAG))  # Diag
        self.breset.clicked.connect(lambda: self.reset())
        self.b_save.clicked.connect(lambda: self.save())
        layout = QGridLayout(self)
        layout.addWidget(self.camera, 0, 0, 1, 7)
        layout.addWidget(self.x_edit, 1, 0)
        layout.addWidget(self.y_edit, 1, 1)
        layout.addWidget(self.z_edit, 1, 2)
        layout.addWidget(self.brplot, 1, 3)
        layout.addWidget(self.bdplot, 1, 4)
        layout.addWidget(self.breset, 1, 5)
        layout.addWidget(self.b_save, 1, 6)

    def reset(self):
        self.graph = None
        self.objspc.clear()
        self.camera.update()

    def plot(self, mode: PlotMode):
        umin = self.umin_slider.value()
        umax = self.umax_slider.value()
        useg = self.useg_slider.value()
        vmin = self.vmin_slider.value()
        vmax = self.vmax_slider.value()
        vseg = self.vseg_slider.value()
        x_expr = self.x_edit.text()
        y_expr = self.y_edit.text()
        z_expr = self.z_edit.text()
        try:
            glob = __import__("numpy").__dict__
            x = eval(f"lambda u, v: float({x_expr})", glob)
            y = eval(f"lambda u, v: float({y_expr})", glob)
            z = eval(f"lambda u, v: float({z_expr})", glob)
            self.graph = Graph(x, y, z, umin, umax, useg, vmin, vmax, vseg)
        except Exception as e:
            QMessageBox.critical(self, e.__class__.__name__, str(e))
        else:
            self.graph.plot(self.objspc, mode)
            self.camera.update()

    def save(self):
        if self.graph is None:
            QMessageBox.warning(self, "Warning", "No graph to save.")
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
