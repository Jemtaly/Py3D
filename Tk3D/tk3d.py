import copy
import tkinter as tk

import numpy as np


class ObjSpc:
    def __init__(self, verts={}, lines=set()):
        self.verts = copy.deepcopy(verts)
        self.lines = copy.deepcopy(lines)
        self.camvass = set()

    def reset(self, verts={}, lines=set()):
        self.verts = copy.deepcopy(verts)
        self.lines = copy.deepcopy(lines)
        for camvas in self.camvass:
            camvas.refresh()

    def add_camvas(self, camvas):
        self.camvass.add(camvas)

    def remove_camvas(self, camvas):
        self.camvass.remove(camvas)


class Camvas(tk.Canvas):
    def __init__(self, master, objspc, coordn=np.zeros(3), matrix=np.eye(3), dist=960.0, size=160.0):
        assert np.allclose(matrix @ matrix.T, np.eye(3))
        super().__init__(master)
        self.bind("<ButtonPress-1>", self.turn_start)
        self.bind("<ButtonPress-2>", self.mvxy_start)
        self.bind("<ButtonPress-3>", self.tilt_start)
        self.bind("<ButtonRelease-1>", self.turn_end)
        self.bind("<ButtonRelease-2>", self.mvxy_end)
        self.bind("<ButtonRelease-3>", self.tilt_end)
        self.bind("<B1-Motion>", self.turn)
        self.bind("<B2-Motion>", self.mvxy)
        self.bind("<B3-Motion>", self.tilt)
        self.bind("<Button-4>", self.wheel)  # for unix
        self.bind("<Button-5>", self.wheel)  # for unix
        self.bind("<MouseWheel>", self.wheel)  # for windows
        self.bind("<Configure>", self.change)
        frame = tk.Frame(self)
        frame.place(relx=1.0, rely=0.0, anchor=tk.NE)
        dist_var = tk.DoubleVar(value=dist)  # number of pixels between the viewpoint and the projection plane
        size_var = tk.DoubleVar(value=size)  # number of pixels corresponding to each unit length in the space
        dist_scaler = tk.Scale(frame, from_=600.0, to=6000.0, resolution=60.0, length=180, variable=dist_var, orient=tk.HORIZONTAL, label="Dist", command=self.dist_change)
        size_scaler = tk.Scale(frame, from_=100.0, to=1000.0, resolution=10.0, length=180, variable=size_var, orient=tk.HORIZONTAL, label="Size", command=self.size_change)
        dist_scaler.pack()
        size_scaler.pack()
        self.dist = dist_var.get()
        self.size = size_var.get()
        self.coordn = coordn.copy()
        self.matrix = matrix.copy()
        self.centre = np.zeros(2)
        self.objspc = objspc
        self.objspc.add_camvas(self)

    def distroy(self):
        self.objspc.remove_camvas(self)
        super().destroy()

    def refresh(self):
        positions = {}
        for k, absolute in self.objspc.verts.items():
            relative = self.matrix.dot(absolute - self.coordn)
            positions[k] = relative[:2] / (relative[2] or 1.0) * self.dist, np.sign(relative[2])
        self.delete(tk.ALL)
        for p, q in self.objspc.lines:
            P, p = positions[p]
            Q, q = positions[q]
            if p + q == 2:
                self.create_line(*(self.centre - P), *(self.centre - Q))
            elif p == 1:
                V = Q if q == 0 else P - Q  # PQ'
                N = V / (np.linalg.norm(V) or 1.0)
                a, c, r = np.dot(P, N), np.linalg.norm(P), np.linalg.norm(self.centre)
                Q = P + N * ((np.sqrt(r * r - c * c + a * a) if r > c else abs(a)) - a)
                self.create_line(*(self.centre - P), *(self.centre - Q))
            elif q == 1:
                V = P if p == 0 else Q - P  # QP'
                N = V / (np.linalg.norm(V) or 1.0)
                a, c, r = np.dot(Q, N), np.linalg.norm(Q), np.linalg.norm(self.centre)
                P = Q + N * ((np.sqrt(r * r - c * c + a * a) if r > c else abs(a)) - a)
                self.create_line(*(self.centre - Q), *(self.centre - P))

    def turn_start(self, event):
        self.turn_evrec = event

    def mvxy_start(self, event):
        self.mvxy_evrec = event

    def tilt_start(self, event):
        self.tilt_evrec = event

    def turn_end(self, event):
        del self.turn_evrec

    def mvxy_end(self, event):
        del self.mvxy_evrec

    def tilt_end(self, event):
        del self.tilt_evrec

    def turn(self, event):
        rtx, rty = (self.turn_evrec.y - event.y) / self.dist, (event.x - self.turn_evrec.x) / self.dist
        self.rota(np.array([rtx, rty, 0.0]))
        self.turn_evrec = event

    def mvxy(self, event):
        mvx, mvy = (event.x - self.mvxy_evrec.x) / self.size, (event.y - self.mvxy_evrec.y) / self.size
        self.move(np.array([mvx, mvy, 0.0]))
        self.mvxy_evrec = event

    def tilt(self, event):
        rtz = np.arctan2(self.tilt_evrec.y - self.centre[1], self.tilt_evrec.x - self.centre[0]) - np.arctan2(event.y - self.centre[1], event.x - self.centre[0])
        self.rota(np.array([0.0, 0.0, rtz]))
        self.tilt_evrec = event

    def wheel(self, event):
        mvz = (event.delta or 1080 - event.num * 240) / self.size
        self.move(np.array([0.0, 0.0, mvz]))

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
        self.refresh()

    def move(self, mvec):
        self.coordn += np.linalg.inv(self.matrix).dot(mvec)
        self.refresh()

    def dist_change(self, value):
        self.dist = float(value)
        self.refresh()

    def size_change(self, value):
        self.size = float(value)
        self.refresh()

    def change(self, event):  # always called at startup
        self.centre = np.array([event.width, event.height]) / 2
        self.refresh()
