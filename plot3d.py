#!/usr/bin/python3
import tk3d, tkinter, numpy
class Plot3D(tk3d.Tk3D):
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
        self.frame_right = tkinter.Frame(self.canvas)
        self.frame_right.pack(side = tkinter.RIGHT, anchor = tkinter.N)
        self.dist_var = tkinter.DoubleVar(value = 960.0) # number of pixels between the viewpoint and the projection plane
        self.size_var = tkinter.DoubleVar(value = 160.0) # number of pixels corresponding to each unit length in the space
        self.dist_scaler = tkinter.Scale(self.frame_right, from_ = 600.0, to = 6000.0, length = 180, variable = self.dist_var, orient = tkinter.HORIZONTAL, label = 'Dist', command = self.dist_change)
        self.size_scaler = tkinter.Scale(self.frame_right, from_ = 100.0, to = 1000.0, length = 180, variable = self.size_var, orient = tkinter.HORIZONTAL, label = 'Size', command = self.size_change)
        self.dist_scaler.pack()
        self.size_scaler.pack()
        self.dist = self.dist_var.get()
        self.size = self.size_var.get()
        self.frame_left = tkinter.Frame(self.canvas)
        self.frame_left.pack(side = tkinter.LEFT, anchor = tkinter.N)
        self.xstart_var = tkinter.DoubleVar(value = -10.0)
        self.ystart_var = tkinter.DoubleVar(value = -10.0)
        self.xend_var = tkinter.DoubleVar(value = 10.0)
        self.yend_var = tkinter.DoubleVar(value = 10.0)
        self.xstep_var = tkinter.DoubleVar(value = 0.1)
        self.ystep_var = tkinter.DoubleVar(value = 0.1)
        self.xstart_scaler = tkinter.Scale(self.frame_left, from_ = -10.0, to = 10.0, resolution = 0.1, length = 180, variable = self.xstart_var, orient = tkinter.HORIZONTAL, label = 'X start')
        self.ystart_scaler = tkinter.Scale(self.frame_left, from_ = -10.0, to = 10.0, resolution = 0.1, length = 180, variable = self.ystart_var, orient = tkinter.HORIZONTAL, label = 'Y start')
        self.xend_scaler = tkinter.Scale(self.frame_left, from_ = -10.0, to = 10.0, resolution = 0.1, length = 180, variable = self.xend_var, orient = tkinter.HORIZONTAL, label = 'X end')
        self.yend_scaler = tkinter.Scale(self.frame_left, from_ = -10.0, to = 10.0, resolution = 0.1, length = 180, variable = self.yend_var, orient = tkinter.HORIZONTAL, label = 'Y end')
        self.xstep_scaler = tkinter.Scale(self.frame_left, from_ = 0.1, to = 1.0, resolution = 0.01, length = 180, variable = self.xstep_var, orient = tkinter.HORIZONTAL, label = 'X step')
        self.ystep_scaler = tkinter.Scale(self.frame_left, from_ = 0.1, to = 1.0, resolution = 0.01, length = 180, variable = self.ystep_var, orient = tkinter.HORIZONTAL, label = 'Y step')
        self.xstart_scaler.pack()
        self.ystart_scaler.pack()
        self.xend_scaler.pack()
        self.yend_scaler.pack()
        self.xstep_scaler.pack()
        self.ystep_scaler.pack()
        self.frame_bottom = tkinter.Frame(self.tk)
        self.frame_bottom.pack(fill = tkinter.X)
        self.entry = tkinter.Entry(self.frame_bottom)
        self.entry.pack(side = tkinter.LEFT, expand = True, fill = tkinter.X)
        self.button = tkinter.Button(self.frame_bottom, text = 'Plot', command = self.plot)
        self.button.pack(side = tkinter.RIGHT)
        self.tk.mainloop()
    def plot(self):
        xrange = numpy.arange(self.xstart_var.get(), self.xend_var.get(), self.xstep_var.get())
        yrange = numpy.arange(self.ystart_var.get(), self.yend_var.get(), self.ystep_var.get())
        self.points = {hash((x, y)): numpy.array([x, y, eval(self.entry.get())]) for x in xrange for y in yrange}
        self.lines = set()
        for x1, x2 in zip(xrange[:-1], xrange[1:]):
            for y1, y2 in zip(yrange[:-1], yrange[1:]):
                self.lines.add((hash((x1, y1)), hash((x2, y1))))
                self.lines.add((hash((x1, y1)), hash((x1, y2))))
        y = yrange[-1]
        for x1, x2 in zip(xrange[:-1], xrange[1:]):
            self.lines.add((hash((x1, y)), hash((x2, y))))
        x = xrange[-1]
        for y1, y2 in zip(yrange[:-1], yrange[1:]):
            self.lines.add((hash((x, y1)), hash((x, y2))))
        self.refresh()
def main():
    Plot3D().run()
if __name__ == '__main__':
    main()
