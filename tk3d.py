#!/usr/bin/python3
import tkinter, numpy, math
class Space:
    def __init__(self, points={}, lines=set()):
        self.points = points
        self.lines = lines
        self.camera = numpy.array([0.0, 0.0, 0.0])
        self.matrix = numpy.array([[1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, -1.0]])
        self.scale = 720.0
        self.stick = 120.0
    def start(self):
        self.tk = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.tk)
        self.canvas.pack(fill=tkinter.BOTH, expand=True)
        self.canvas.bind('<Button-1>', self.turn_press)
        self.canvas.bind('<B1-Motion>', self.turn_motion)
        self.canvas.bind('<Button-3>', self.tilt_press)
        self.canvas.bind('<B3-Motion>', self.tilt_motion)
        self.canvas.bind('<Button-2>', self.move_press)
        self.canvas.bind('<B2-Motion>', self.move_motion)
        self.canvas.bind('<MouseWheel>', self.move_wheel)
        self.canvas.bind('<Button-4>', self.move_wheel)
        self.canvas.bind('<Button-5>', self.move_wheel)
        self.canvas.bind('<Configure>', self.configure)
        self.tk.mainloop()
    def refresh(self):
        relatives = {}
        for k, coordinate in self.points.items():
            relative = self.matrix.dot(coordinate - self.camera)
            if relative[2] > 0:
                relatives[k] = relative[0] / relative[2] * self.scale + self.center_x, relative[1] / relative[2] * self.scale + self.center_y
        self.canvas.delete(tkinter.ALL)
        self.canvas.create_text(0.0, 0.0, fill='blue', text='Scale = {}'.format(self.scale), anchor=tkinter.NW)
        # for k, coordinate in relatives.items():
        #     self.canvas.create_text(*coordinate, fill='blue', text=k)
        for p, q in self.lines:
            if p in relatives and q in relatives:
                self.canvas.create_line(*relatives[p], *relatives[q])
    def turn_press(self, event):
        self.turn_rec = event
    def turn_motion(self, event):
        dx, dy = event.x - self.turn_rec.x, event.y - self.turn_rec.y
        ds = math.sqrt(dx ** 2 + dy ** 2)
        nx, ny = -dy / ds, dx / ds
        alpha = ds / self.scale
        n = numpy.array([[nx, ny, 0.0]])
        N = numpy.array([[0.0, 0.0, ny], [0.0, 0.0, -nx], [-ny, nx, 0.0]])
        self.matrix = (math.cos(alpha) * numpy.eye(3) + (1 - math.cos(alpha)) * n * n.T + math.sin(alpha) * N).dot(self.matrix)
        self.refresh()
        self.turn_rec = event
    def tilt_press(self, event):
        self.tilt_rec = event
    def tilt_motion(self, event):
        ax, ay, bx, by = event.x - self.center_x, event.y - self.center_y, self.tilt_rec.x - self.center_x, self.tilt_rec.y - self.center_y
        asbs = math.sqrt(ax ** 2 + ay ** 2) * math.sqrt(bx ** 2 + by ** 2)
        sina, cosa = (ax * by - ay * bx) / asbs, (ax * bx + ay * by) / asbs
        self.matrix = numpy.array([[cosa, sina, 0.0], [-sina, cosa, 0.0], [0.0, 0.0, 1.0]]).dot(self.matrix)
        self.refresh()
        self.tilt_rec = event
    def move_press(self, event):
        self.move_rec = event
    def move_motion(self, event):
        self.camera -= numpy.linalg.inv(self.matrix).dot(numpy.array([(event.x - self.move_rec.x) / self.stick, (event.y - self.move_rec.y) / self.stick, 0.0]))
        self.refresh()
        self.move_rec = event
    def move_wheel(self, event):
        delta = event.delta or 1080 - event.num * 240
        # move forward/backward when middle mouse button is pressed, otherwise zoom in/out
        if event.state & 0x200:
            self.camera -= numpy.linalg.inv(self.matrix).dot(numpy.array([0.0, 0.0, -delta / self.stick]))
        else:
            self.scale *= (2400 + delta) / (2400 - delta)
        self.refresh()
    def configure(self, event):
        self.center_y, self.center_x = 0.5 * event.height, 0.5 * event.width
        self.refresh()
def main():
    import argparse, sys
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    args = parser.parse_args()
    ps = {}
    ls = set()
    for line in args.file:
        vals = line.split()
        if not vals:
            continue
        type, *vals = vals
        if type == 'v':
            ps['V' + str(len(ps) + 1)] = numpy.array([float(vals[0]), float(vals[1]), float(vals[2])])
        elif type == 'p':
            ls.add(tuple(sorted(('V' + vals[0], 'V' + vals[0]))))
        elif type == 'l':
            ls.add(tuple(sorted(('V' + vals[0], 'V' + vals[1]))))
        elif type == 'f':
            for i in range(len(vals)):
                ls.add(tuple(sorted(('V' + vals[i].split('/')[0], 'V' + vals[i - 1].split('/')[0]))))
    Space(points=ps, lines=ls).start()
if __name__ == '__main__':
    main()
