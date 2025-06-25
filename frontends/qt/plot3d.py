import sys

from PyQt5.QtWidgets import QApplication, QGridLayout, QLineEdit, QMessageBox, QPushButton, QWidget

from core.engine import ObjectSpace
from core.plot3d import PlotMode, objspc_plot
from .qt3d import QCamera, QSliderForm


def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Plot3D")
    window.setMinimumSize(800, 600)
    objspc = ObjectSpace()
    camera = QCamera(objspc)
    ranges = QSliderForm()
    xmin_slider = ranges.newSlider("X min", -10, +10, -10)
    xmax_slider = ranges.newSlider("X max", -10, +10, +10)
    xnum_slider = ranges.newSlider("X num", 1, 100, 20)
    ymin_slider = ranges.newSlider("Y min", -10, +10, -10)
    ymax_slider = ranges.newSlider("Y max", -10, +10, +10)
    ynum_slider = ranges.newSlider("Y num", 1, 100, 20)
    camera.layout().addLayout(ranges)

    def plot(mode: PlotMode):
        xmin = xmin_slider.value()
        xmax = xmax_slider.value()
        xnum = xnum_slider.value()
        ymin = ymin_slider.value()
        ymax = ymax_slider.value()
        ynum = ynum_slider.value()
        try:
            fn = eval("lambda x, y: " + txtbox.text())
            objspc_plot(objspc, xmin, xmax, xnum, ymin, ymax, ynum, fn, mode)
        except Exception as e:
            QMessageBox.critical(window, e.__class__.__name__, str(e))
        camera.update()

    def reset():
        objspc.clear()
        camera.update()

    txtbox = QLineEdit()
    brplot = QPushButton("RPlot")
    bdplot = QPushButton("DPlot")
    breset = QPushButton("Reset")
    brplot.clicked.connect(lambda: plot(PlotMode.RECT))  # Rectangular plot
    bdplot.clicked.connect(lambda: plot(PlotMode.DIAG))  # Diagonal plot
    breset.clicked.connect(lambda: reset())
    layout = QGridLayout()
    layout.addWidget(camera, 0, 0, 1, 4)
    layout.addWidget(txtbox, 1, 0)
    layout.addWidget(brplot, 1, 1)
    layout.addWidget(bdplot, 1, 2)
    layout.addWidget(breset, 1, 3)
    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
