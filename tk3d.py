#!/usr/bin/python3
import tkinter, numpy, math
class Camera:
    def __init__(self):
        self.coordinate = numpy.array([0.0, 0.0, 0.0])
        self.matrix = numpy.array([[1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, -1.0]])
    def transform(self, absolute):
        return self.matrix.dot(absolute - self.coordinate)
    def move(self, ds):
        self.coordinate -= numpy.linalg.inv(self.matrix).dot(ds)
    def rotate(self, th):
        alpha = numpy.linalg.norm(th)
        if alpha:
            nx, ny, nz = th / alpha
            n = numpy.array([[nx, ny, nz]])
            N = numpy.array([[0.0, -nz, ny], [nz, 0.0, -nx], [-ny, nx, 0.0]])
            self.matrix = (math.cos(alpha) * numpy.eye(3) + (1 - math.cos(alpha)) * n * n.T + math.sin(alpha) * N).dot(self.matrix)
class Tk3D:
    def __init__(self, points = {}, lines = set()):
        self.camera = Camera()
        self.points = points
        self.lines = lines
    def run(self):
        self.tk = tkinter.Tk()
        self.tk.minsize(800, 600)
        self.canvas = tkinter.Canvas(self.tk)
        self.canvas.pack(fill = tkinter.BOTH, expand = True)
        self.canvas.bind('<ButtonPress-1>', self.turn_start)
        self.canvas.bind('<ButtonPress-3>', self.tilt_start)
        self.canvas.bind('<ButtonPress-2>', self.move_start)
        self.canvas.bind('<ButtonRelease-1>', self.turn_end)
        self.canvas.bind('<ButtonRelease-3>', self.tilt_end)
        self.canvas.bind('<ButtonRelease-2>', self.move_end)
        self.canvas.bind('<B1-Motion>', self.turn)
        self.canvas.bind('<B3-Motion>', self.tilt)
        self.canvas.bind('<B2-Motion>', self.move)
        self.canvas.bind('<Button-4>', self.wheel) # for unix
        self.canvas.bind('<Button-5>', self.wheel) # for unix
        self.canvas.bind('<MouseWheel>', self.wheel) # for windows
        self.canvas.bind('<Configure>', self.config)
        self.dist_var = tkinter.DoubleVar(value = 960.0) # number of pixels between the viewpoint and the projection plane
        self.size_var = tkinter.DoubleVar(value = 160.0) # number of pixels corresponding to each unit length in the space
        self.dist_scaler = tkinter.Scale(self.canvas, from_ = 600.0, to = 6000.0, length = 180, variable = self.dist_var, orient = tkinter.HORIZONTAL, label = 'Dist', command = self.dist_change)
        self.size_scaler = tkinter.Scale(self.canvas, from_ = 100.0, to = 1000.0, length = 180, variable = self.size_var, orient = tkinter.HORIZONTAL, label = 'Size', command = self.size_change)
        self.dist_scaler.pack(anchor = tkinter.NE)
        self.size_scaler.pack(anchor = tkinter.NE)
        self.dist = self.dist_var.get()
        self.size = self.size_var.get()
        self.tk.mainloop()
    def refresh(self):
        positions = {}
        for k, absolute in self.points.items():
            relative = self.camera.transform(absolute)
            if relative[2] > 0:
                positions[k] = self.cx + relative[0] / relative[2] * self.dist, self.cy + relative[1] / relative[2] * self.dist
        self.canvas.delete(tkinter.ALL)
        # for k, coordinate in positions.items():
        #     self.canvas.create_text(*coordinate, fill = 'blue', text = k)
        for p, q in self.lines:
            if p in positions and q in positions:
                self.canvas.create_line(*positions[p], *positions[q])
    def turn_start(self, event):
        self.turn_evrec = event
    def tilt_start(self, event):
        self.tilt_evrec = event
    def move_start(self, event):
        self.move_evrec = event
    def turn_end(self, event):
        del self.turn_evrec
    def tilt_end(self, event):
        del self.tilt_evrec
    def move_end(self, event):
        del self.move_evrec
    def turn(self, event):
        dx, dy = event.x - self.turn_evrec.x, event.y - self.turn_evrec.y
        self.camera.rotate(numpy.array([-dy / self.dist, dx / self.dist, 0.0]))
        self.turn_evrec = event
        self.refresh()
    def tilt(self, event):
        bx, by, ax, ay = event.x - self.cx, event.y - self.cy, self.tilt_evrec.x - self.cx, self.tilt_evrec.y - self.cy
        self.camera.rotate(numpy.array([0.0, 0.0, math.atan2(ax * by - ay * bx, ax * bx + ay * by)]))
        self.tilt_evrec = event
        self.refresh()
    def move(self, event):
        dx, dy = event.x - self.move_evrec.x, event.y - self.move_evrec.y
        self.camera.move(numpy.array([dx / self.size, dy / self.size, 0.0]))
        self.move_evrec = event
        self.refresh()
    def wheel(self, event):
        delta = event.delta or 1080 - event.num * 240
        self.camera.move(numpy.array([0.0, 0.0, -delta / self.size]))
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
def main():
    import argparse, sys
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs = '?', type = argparse.FileType('r'), default = sys.stdin)
    args = parser.parse_args()
    ps = {}
    ls = set()
    for line in args.file:
        vals = line.split()
        if not vals:
            continue
        label, *vals = vals
        if label == 'v':
            ps['V' + str(len(ps) + 1)] = numpy.array([float(vals[0]), float(vals[1]), float(vals[2])])
        elif label == 'p':
            ls.add(('V' + vals[0], 'V' + vals[0]))
        elif label == 'l':
            ls.add(('V' + vals[0], 'V' + vals[1]))
        elif label == 'f':
            for i in range(len(vals)):
                ls.add(('V' + vals[i].split('/')[0], 'V' + vals[i - 1].split('/')[0]))
    Tk3D(points = ps, lines = {tuple(sorted(l)) for l in ls}).run()
if __name__ == '__main__':
    main()
