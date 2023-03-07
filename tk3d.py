import tkinter, numpy, math, copy
class ObjSpc:
    def __init__(self, verts = {}, lines = set()):
        self.verts = copy.deepcopy(verts)
        self.lines = copy.deepcopy(lines)
        self.camvass = set()
    def reset(self, verts = {}, lines = set()):
        self.verts = copy.deepcopy(verts)
        self.lines = copy.deepcopy(lines)
        for camvas in self.camvass:
            camvas.refresh()
    def add_camvas(self, camvas):
        self.camvass.add(camvas)
    def remove_camvas(self, camvas):
        self.camvass.remove(camvas)
class Camvas(tkinter.Canvas):
    def __init__(self, master, objspc, coordn = numpy.zeros(3), matrix = numpy.eye(3), dist = 960.0, size = 160.0):
        assert numpy.allclose(matrix @ matrix.T, numpy.eye(3))
        assert dist in numpy.arange(600.0, 6000.0, 60.0) or dist == 6000.0
        assert size in numpy.arange(100.0, 1000.0, 10.0) or size == 1000.0
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
        self.bind('<Configure>', self.change)
        self.frame = tkinter.Frame(self)
        self.frame.place(relx = 1.0, rely = 0.0, anchor = tkinter.NE)
        self.dist_var = tkinter.DoubleVar(value = dist) # number of pixels between the viewpoint and the projection plane
        self.size_var = tkinter.DoubleVar(value = size) # number of pixels corresponding to each unit length in the space
        self.dist_scaler = tkinter.Scale(self.frame, from_ = 600.0, to = 6000.0, resolution = 60.0, length = 180, variable = self.dist_var, orient = tkinter.HORIZONTAL, label = 'Dist', command = self.dist_change)
        self.size_scaler = tkinter.Scale(self.frame, from_ = 100.0, to = 1000.0, resolution = 10.0, length = 180, variable = self.size_var, orient = tkinter.HORIZONTAL, label = 'Size', command = self.size_change)
        self.dist_scaler.pack()
        self.size_scaler.pack()
        self.dist = self.dist_var.get()
        self.size = self.size_var.get()
        self.coordn = coordn.copy()
        self.matrix = matrix.copy()
        self.objspc = objspc
        self.objspc.add_camvas(self)
    def destroy(self):
        self.objspc.remove_camvas(self)
        super().destroy()
    def refresh(self):
        positions = {}
        for k, absolute in self.objspc.verts.items():
            relative = self.matrix.dot(absolute - self.coordn)
            positions[k] = self.centre - relative[:2] / relative[2] * self.dist, numpy.sign(relative[2])
        self.delete(tkinter.ALL)
        for p, q in self.objspc.lines:
            P, p = positions[p]
            Q, q = positions[q]
            if p + q == 2:
                self.create_line(*P, *Q)
            elif p - q == 2:
                T = Q - P
                Q = P - T / numpy.linalg.norm(T) * 1e+9
                self.create_line(*P, *Q)
            elif q - p == 2:
                T = P - Q
                P = Q - T / numpy.linalg.norm(T) * 1e+9
                self.create_line(*Q, *P)
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
        rtx, rty = (self.turn_evrec.y - event.y) / self.dist, (event.x - self.turn_evrec.x) / self.dist
        self.rota(numpy.array([rtx, rty, 0.0]))
        self.turn_evrec = event
    def tilt(self, event):
        rtz = math.atan2(self.tilt_evrec.y - self.centre[1], self.tilt_evrec.x - self.centre[0]) - math.atan2(event.y - self.centre[1], event.x - self.centre[0])
        self.rota(numpy.array([0.0, 0.0, rtz]))
        self.tilt_evrec = event
    def mvxy(self, event):
        mvx, mvy = (event.x - self.mvxy_evrec.x) / self.size, (event.y - self.mvxy_evrec.y) / self.size
        self.move(numpy.array([mvx, mvy, 0.0]))
        self.mvxy_evrec = event
    def wheel(self, event):
        mvz = (event.delta or 1080 - event.num * 240) / self.size
        self.move(numpy.array([0.0, 0.0, mvz]))
    def rota(self, rt):
        half = numpy.linalg.norm(rt)
        S, C = numpy.sin(half), numpy.cos(half)
        x, y, z = rt / half if half else numpy.zeros(3)
        self.matrix = numpy.array([
            [x * x * (1 - C) + 1 * C, x * y * (1 - C) + z * S, x * z * (1 - C) - y * S],
            [y * x * (1 - C) - z * S, y * y * (1 - C) + 1 * C, y * z * (1 - C) + x * S],
            [z * x * (1 - C) + y * S, z * y * (1 - C) - x * S, z * z * (1 - C) + 1 * C],
        ]).dot(self.matrix)
        self.refresh()
    def move(self, mv):
        self.coordn += numpy.linalg.inv(self.matrix).dot(mv)
        self.refresh()
    def change(self, event): # initialize
        self.centre = numpy.array([event.width / 2, event.height / 2])
        self.refresh()
    def dist_change(self, value):
        self.dist = self.dist_var.get()
        self.refresh()
    def size_change(self, value):
        self.size = self.size_var.get()
        self.refresh()
