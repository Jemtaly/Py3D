import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QPainter, QPen, QWheelEvent, QPaintEvent
from PyQt5.QtWidgets import QFormLayout, QHBoxLayout, QVBoxLayout, QSlider, QWidget

from py3d.core.engine import ObjectSpace, Camera, CoordVec3, EulerVec3


class QSliderForm(QFormLayout):
    def __init__(self, width=160):
        super().__init__()
        self.setRowWrapPolicy(QFormLayout.WrapAllRows)
        self.width = width

    def newSlider(self, label: str, min: int, max: int, val: int, callback=None) -> QSlider:
        slider = QSlider(Qt.Horizontal)
        slider.setRange(min, max)
        slider.setValue(val)
        if callback:
            slider.valueChanged.connect(callback)
        slider.setMinimumWidth(self.width)
        self.addRow(label, slider)
        return slider


class QCamera(QWidget):
    def __init__(self, objspc: ObjectSpace, coordv: CoordVec3 | None = None, eulerv: EulerVec3 | None = None, dist=960, size=160):
        super().__init__()
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.right = QVBoxLayout()
        layout = QHBoxLayout()
        layout.addStretch(0x1)
        layout.addLayout(self.right)
        self.setLayout(layout)
        ne_layout = QSliderForm()
        dist_slider = ne_layout.newSlider("Dist (px)", 600, 6000, dist, self.dist_change)
        size_slider = ne_layout.newSlider("Size (px)", 100, 1000, size, self.size_change)
        self.right.addLayout(ne_layout)
        self.right.addStretch(0x1)
        self.dist = dist_slider.value()  # type: int
        self.size = size_slider.value()  # type: int
        self.camera = Camera(objspc, coordv, eulerv)

    def mouseMoveEvent(self, event: QMouseEvent):
        Nx, Ny = event.x(), event.y()
        if event.buttons() == Qt.LeftButton:
            rtx, rty = (self.Ry - Ny) / self.dist, (Nx - self.Rx) / self.dist
            self.rota(np.array([rtx, rty, 0.0]))
        if event.buttons() == Qt.MiddleButton:
            mvx, mvy = (Nx - self.Rx) / self.size, (Ny - self.Ry) / self.size
            self.move(np.array([mvx, mvy, 0.0]))
        if event.buttons() == Qt.RightButton:
            Cx, Cy = self.width() / 2, self.height() / 2
            rtz = np.arctan2(self.Ry - Cy, self.Rx - Cx) - np.arctan2(Ny - Cy, Nx - Cx)
            self.rota(np.array([0.0, 0.0, rtz]))
        self.Rx, self.Ry = Nx, Ny

    def wheelEvent(self, event: QWheelEvent):
        mvz = event.angleDelta().y() / self.size
        self.move(np.array([0.0, 0.0, mvz]))

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        C = np.array([self.width() / 2, self.height() / 2])
        for P, Q in self.camera.draw(np.linalg.norm(C), self.dist):
            painter.drawLine(*np.append(C - P, C - Q).astype(int))
        coordv = self.camera.get_coordv()
        eulerv = self.camera.get_eulerv()
        painter.drawText(10, 20, "Coordinates:")
        painter.drawText(10, 40, f"  x: {coordv[0]:.2f}")
        painter.drawText(10, 60, f"  y: {coordv[1]:.2f}")
        painter.drawText(10, 80, f"  z: {coordv[2]:.2f}")
        painter.drawText(10, 110, "Rotation:")
        painter.drawText(10, 130, f"  x: {np.degrees(eulerv[0]):.2f}°")
        painter.drawText(10, 150, f"  y: {np.degrees(eulerv[1]):.2f}°")
        painter.drawText(10, 170, f"  z: {np.degrees(eulerv[2]):.2f}°")
        painter.end()

    def dist_change(self, value: int):
        self.dist = value
        self.update()

    def size_change(self, value: int):
        self.size = value
        self.update()

    def rota(self, rvec: EulerVec3):
        self.camera.rota(rvec)
        self.update()

    def move(self, mvec: CoordVec3):
        self.camera.move(mvec)
        self.update()
