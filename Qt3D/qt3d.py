import copy

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QPainter, QPen
from PyQt5.QtWidgets import QFormLayout, QHBoxLayout, QSlider, QWidget


class ObjSpc:
    def __init__(self, verts={}, lines=set()):
        self.verts = copy.deepcopy(verts)
        self.lines = copy.deepcopy(lines)
        self.camvass = set()

    def reset(self, verts={}, lines=set()):
        self.verts = copy.deepcopy(verts)
        self.lines = copy.deepcopy(lines)
        for camvas in self.camvass:
            camvas.update()

    def add_camvas(self, camvas):
        self.camvass.add(camvas)

    def remove_camvas(self, camvas):
        self.camvass.remove(camvas)


class QSliderForm(QFormLayout):
    def __init__(self):
        super().__init__()
        self.setRowWrapPolicy(QFormLayout.WrapAllRows)

    def newSlider(self, label, min, max, val, callback=None, width=160):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(min, max)
        slider.setValue(val)
        if callback:
            slider.valueChanged.connect(callback)
        slider.setMinimumWidth(width)
        self.addRow(label, slider)
        return slider


class QCamera(QWidget):
    def __init__(self, objspc, coordn=np.zeros(3), matrix=np.eye(3), dist=960, size=160):
        assert np.allclose(matrix @ matrix.T, np.eye(3))
        super().__init__()
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        left = QSliderForm()
        dist_slider = left.newSlider("Dist", 600, 6000, dist, self.dist_change)
        size_slider = left.newSlider("Size", 100, 1000, size, self.size_change)
        layout = QHBoxLayout()
        layout.addLayout(left)
        layout.addStretch(0x1)
        self.setLayout(layout)
        self.dist = dist_slider.value()  # number of pixels between the viewpoint and the projection plane
        self.size = size_slider.value()  # number of pixels corresponding to each unit length in the space
        self.coordn = coordn.copy()
        self.matrix = matrix.copy()
        self.objspc = objspc
        self.objspc.add_camvas(self)

    def __del__(self):
        self.objspc.remove_camvas(self)

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

    def wheelEvent(self, event):
        mvz = event.angleDelta().y() / self.size
        self.move(np.array([0.0, 0.0, mvz]))

    def paintEvent(self, event):
        positions = {}
        for k, absolute in self.objspc.verts.items():
            relative = self.matrix.dot(absolute - self.coordn)
            positions[k] = relative[:2] / (relative[2] or 1.0) * self.dist, np.sign(relative[2])
        C = np.array([self.width() / 2, self.height() / 2])
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        for p, q in self.objspc.lines:
            P, p = positions[p]
            Q, q = positions[q]
            if p + q == 2:
                painter.drawLine(*np.append(C - P, C - Q).astype(int))
            elif p == 1:
                V = Q if q == 0 else P - Q  # PQ'
                N = V / (np.linalg.norm(V) or 1.0)
                a, c, r = np.dot(P, N), np.linalg.norm(P), np.linalg.norm(C)
                Q = P + N * ((np.sqrt(r * r - c * c + a * a) if r > c else abs(a)) - a)
                painter.drawLine(*np.append(C - P, C - Q).astype(int))
            elif q == 1:
                V = P if p == 0 else Q - P  # QP'
                N = V / (np.linalg.norm(V) or 1.0)
                a, c, r = np.dot(Q, N), np.linalg.norm(Q), np.linalg.norm(C)
                P = Q + N * ((np.sqrt(r * r - c * c + a * a) if r > c else abs(a)) - a)
                painter.drawLine(*np.append(C - Q, C - P).astype(int))

    def rota(self, rvec):
        norm = np.linalg.norm(rvec)
        s, c = np.sin(norm), np.cos(norm)
        x, y, z = rvec / norm if norm else np.zeros(3)
        self.matrix = np.array(
            [
                [x * x * (1 - c) + 1 * c, x * y * (1 - c) + z * s, x * z * (1 - c) - y * s],
                [y * x * (1 - c) - z * s, y * y * (1 - c) + 1 * c, y * z * (1 - c) + x * s],
                [z * x * (1 - c) + y * s, z * y * (1 - c) - x * s, z * z * (1 - c) + 1 * c],
            ]
        ).dot(self.matrix)
        self.update()

    def move(self, mvec):
        self.coordn += np.linalg.inv(self.matrix).dot(mvec)
        self.update()

    def dist_change(self, value):
        self.dist = value
        self.update()

    def size_change(self, value):
        self.size = value
        self.update()
