#!/usr/bin/python3
def main():
    from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QPushButton, QMessageBox
    import qt3d, numpy, sys
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('Plot3D')
    window.setMinimumSize(800, 600)
    objspc = qt3d.ObjSpc()
    camera = qt3d.QCamera(objspc)
    ranges = qt3d.QSliderForm()
    xmin_slider = ranges.newSlider('X min', -10, +10, -10)
    xmax_slider = ranges.newSlider('X max', -10, +10, +10)
    xnum_slider = ranges.newSlider('X num',   1, 100,  20)
    ymin_slider = ranges.newSlider('Y min', -10, +10, -10)
    ymax_slider = ranges.newSlider('Y max', -10, +10, +10)
    ynum_slider = ranges.newSlider('Y num',   1, 100,  20)
    camera.layout().addLayout(ranges)
    def plot(mode):
        xs = numpy.linspace(xmin_slider.value(), xmax_slider.value(), xnum_slider.value() + 1, endpoint = True)
        ys = numpy.linspace(ymin_slider.value(), ymax_slider.value(), ynum_slider.value() + 1, endpoint = True)
        try:
            fn = eval('lambda x, y: ' + txtbox.text())
            vs = {(x, y): numpy.array([x, y, fn(x, y)], float) for x in xs for y in ys}
        except Exception as e:
            QMessageBox.critical(window, e.__class__.__name__, str(e))
            return False
        if mode:
            lh = set(((x1, y0), (x2, y0)) for x1, x2 in zip(xs[:-1], xs[+1:]) for y0 in ys)
            lv = set(((x0, y1), (x0, y2)) for y1, y2 in zip(ys[:-1], ys[+1:]) for x0 in xs)
        else:
            lh = set(((x1, y1), (x2, y2)) for x1, x2 in zip(xs[:-1], xs[+1:]) for y1, y2 in zip(ys[:-1], ys[+1:]))
            lv = set(((x1, y2), (x2, y1)) for x1, x2 in zip(xs[:-1], xs[+1:]) for y1, y2 in zip(ys[:-1], ys[+1:]))
        objspc.reset(verts = vs, lines = lh | lv)
        return True
    txtbox = QLineEdit()
    brplot = QPushButton('RPlot')
    bdplot = QPushButton('DPlot')
    breset = QPushButton('Reset')
    brplot.clicked.connect(lambda: plot(1)) # Rectangular plot
    bdplot.clicked.connect(lambda: plot(0)) # Diagonal plot
    breset.clicked.connect(lambda: objspc.reset())
    layout = QGridLayout()
    layout.addWidget(camera, 0, 0, 1, 4)
    layout.addWidget(txtbox, 1, 0)
    layout.addWidget(brplot, 1, 1)
    layout.addWidget(bdplot, 1, 2)
    layout.addWidget(breset, 1, 3)
    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
