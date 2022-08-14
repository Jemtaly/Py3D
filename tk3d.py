#!/usr/bin/python3
import tkinter, numpy, math, copy
class Camvas(tkinter.Canvas):
    def __init__(self, master, verts = {}, lines = set()):
        super().__init__(master)
        self.bind('<ButtonPress-1>', self.turn_start)
        self.bind('<ButtonPress-3>', self.tilt_start)
        self.bind('<ButtonPress-2>', self.mvxy_start)
        self.bind('<ButtonRelease-1>', self.turn_end)
        self.bind('<ButtonRelease-3>', self.tilt_end)
        self.bind('<ButtonRelease-2>', self.mvxy_end)
        self.bind('<B1-Motion>', self.turn)
        self.bind('<B3-Motion>', self.tilt)
        self.bind('<B2-Motion>', self.mvxy)
        self.bind('<Button-4>', self.wheel) # for unix
        self.bind('<Button-5>', self.wheel) # for unix
        self.bind('<MouseWheel>', self.wheel) # for windows
        self.bind('<Configure>', self.config)
        self.frame = tkinter.Frame(self)
        self.frame.place(relx = 1.0, rely = 0.0, anchor = tkinter.NE)
        self.dist_var = tkinter.DoubleVar(value = 960.0) # number of pixels between the viewpoint and the projection plane
        self.size_var = tkinter.DoubleVar(value = 160.0) # number of pixels corresponding to each unit length in the space
        self.dist_scaler = tkinter.Scale(self.frame, from_ = 600.0, to = 6000.0, resolution = 60.0, length = 180, variable = self.dist_var, orient = tkinter.HORIZONTAL, label = 'Dist', command = self.dist_change)
        self.size_scaler = tkinter.Scale(self.frame, from_ = 100.0, to = 1000.0, resolution = 10.0, length = 180, variable = self.size_var, orient = tkinter.HORIZONTAL, label = 'Size', command = self.size_change)
        self.dist_scaler.pack()
        self.size_scaler.pack()
        self.dist = self.dist_var.get()
        self.size = self.size_var.get()
        self.centre = numpy.zeros(3)
        self.matrix = numpy.eye(3)
        self.verts = copy.deepcopy(verts)
        self.lines = copy.deepcopy(lines)
    def refresh(self):
        positions = {}
        for k, absolute in self.verts.items():
            relative = self.matrix.dot(absolute - self.centre)
            if relative[2] < 0:
                positions[k] = self.cx - relative[0] / relative[2] * self.dist, self.cy + relative[1] / relative[2] * self.dist
        self.delete(tkinter.ALL)
        # for k, centre in positions.items():
        #     self.create_text(*centre, fill = 'blue', text = k)
        for p, q in self.lines:
            if p in positions and q in positions:
                self.create_line(*positions[p], *positions[q])
    def turn_start(self, event):
        self.turn_evrec = event
    def tilt_start(self, event):
        self.tilt_evrec = event
    def mvxy_start(self, event):
        self.mvxy_evrec = event
    def turn_end(self, event):
        del self.turn_evrec
    def tilt_end(self, event):
        del self.tilt_evrec
    def mvxy_end(self, event):
        del self.mvxy_evrec
    def turn(self, event):
        rtx, rty = (self.turn_evrec.y - event.y) / self.dist, (self.turn_evrec.x - event.x) / self.dist
        self.rota(numpy.array([rtx, rty, 0.0]))
        self.turn_evrec = event
    def tilt(self, event):
        rtz = math.atan2(self.tilt_evrec.y - self.cy, self.tilt_evrec.x - self.cx) - math.atan2(event.y - self.cy, event.x - self.cx)
        self.rota(numpy.array([0.0, 0.0, rtz]))
        self.tilt_evrec = event
    def mvxy(self, event):
        mvx, mvy = (self.mvxy_evrec.x - event.x) / self.size, (event.y - self.mvxy_evrec.y) / self.size
        self.move(numpy.array([mvx, mvy, 0.0]))
        self.mvxy_evrec = event
    def wheel(self, event):
        mvz = (0 - event.delta or event.num * 240 - 1080) / self.size
        self.move(numpy.array([0.0, 0.0, mvz]))
    def move(self, mv):
        self.centre += numpy.linalg.inv(self.matrix).dot(mv)
        self.refresh()
    def rota(self, rt):
        alpha = numpy.linalg.norm(rt)
        if alpha:
            nx, ny, nz = rt / alpha
            n = numpy.array([[+nx, +ny, +nz]])
            N = numpy.array([[0.0, -nz, +ny], [+nz, 0.0, -nx], [-ny, +nx, 0.0]])
            self.matrix = (math.cos(alpha) * numpy.eye(3) + (1 - math.cos(alpha)) * n * n.T + math.sin(alpha) * N).dot(self.matrix)
        self.refresh()
    def config(self, event):
        self.cx, self.cy = event.width / 2, event.height / 2
        self.refresh()
    def dist_change(self, value):
        self.dist = self.dist_var.get()
        self.refresh()
    def size_change(self, value):
        self.size = self.size_var.get()
        self.refresh()
    def reset(self, verts = {}, lines = set()):
        self.verts = copy.deepcopy(verts)
        self.lines = copy.deepcopy(lines)
        self.refresh()
