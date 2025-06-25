import tkinter as tk

import numpy as np

from core.engine import ObjectSpace, Camera, Vec3, M3x3


class Camvas(tk.Canvas):
    def __init__(self, master, objspc: ObjectSpace, coordn: Vec3 | None = None, matrix: M3x3 | None = None, dist=960.0, size=160.0):
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
        self.centre = np.zeros(2)
        self.camara = Camera(objspc, coordn, matrix)
        self.dist = dist_var.get()  # type: float
        self.size = size_var.get()  # type: float

    def refresh(self):
        self.delete(tk.ALL)
        for p, q in self.camara.draw(np.linalg.norm(self.centre), self.dist):
            self.create_line(*(self.centre - p), *(self.centre - q))

    def turn_start(self, event: tk.Event):
        self.turn_evrec = event

    def mvxy_start(self, event: tk.Event):
        self.mvxy_evrec = event

    def tilt_start(self, event: tk.Event):
        self.tilt_evrec = event

    def turn_end(self, event: tk.Event):
        del self.turn_evrec

    def mvxy_end(self, event: tk.Event):
        del self.mvxy_evrec

    def tilt_end(self, event: tk.Event):
        del self.tilt_evrec

    def turn(self, event: tk.Event):
        rtx, rty = (self.turn_evrec.y - event.y) / self.dist, (event.x - self.turn_evrec.x) / self.dist
        self.rota(np.array([rtx, rty, 0.0]))
        self.turn_evrec = event

    def mvxy(self, event: tk.Event):
        mvx, mvy = (event.x - self.mvxy_evrec.x) / self.size, (event.y - self.mvxy_evrec.y) / self.size
        self.move(np.array([mvx, mvy, 0.0]))
        self.mvxy_evrec = event

    def tilt(self, event: tk.Event):
        rtz = np.arctan2(self.tilt_evrec.y - self.centre[1], self.tilt_evrec.x - self.centre[0]) - np.arctan2(event.y - self.centre[1], event.x - self.centre[0])
        self.rota(np.array([0.0, 0.0, rtz]))
        self.tilt_evrec = event

    def wheel(self, event: tk.Event):
        mvz = (event.delta or 1080 - event.num * 240) / self.size
        self.move(np.array([0.0, 0.0, mvz]))

    def change(self, event: tk.Event):  # always called at startup
        self.centre = np.array([event.width, event.height]) / 2
        self.refresh()

    def dist_change(self, value: str):
        self.dist = float(value)
        self.refresh()

    def size_change(self, value: str):
        self.size = float(value)
        self.refresh()

    def rota(self, rvec: Vec3):
        self.camara.rota(rvec)
        self.refresh()

    def move(self, mvec: Vec3):
        self.camara.move(mvec)
        self.refresh()
