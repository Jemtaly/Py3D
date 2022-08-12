#!/usr/bin/python3
import tkinter, numpy, tk3d
class Plot3D(tk3d.Tk3D):
    def __init__(self):
        tk3d.Tk3D.__init__(self)
    def plot(self, cross):
        xrange = numpy.linspace(self.xbeg_var.get(), self.xend_var.get(), self.xnum_var.get() + 1, endpoint = True)
        yrange = numpy.linspace(self.ybeg_var.get(), self.yend_var.get(), self.ynum_var.get() + 1, endpoint = True)
        func = eval('lambda x, y: ' + self.entry.get())
        self.verts = {(x, y): numpy.array([x, y, func(x, y)]) for x in xrange for y in yrange}
        self.lines = set()
        if cross:
            for x1, x2 in zip(xrange[:-1], xrange[1:]):
                for y1, y2 in zip(yrange[:-1], yrange[1:]):
                    self.lines.add(((x1, y1), (x2, y2)))
                    self.lines.add(((x1, y2), (x2, y1)))
        else:
            for x1, x2 in zip(xrange[:-1], xrange[1:]):
                for y1, y2 in zip(yrange[:-1], yrange[1:]):
                    self.lines.add(((x1, y1), (x1, y2)))
                    self.lines.add(((x2, y1), (x2, y2)))
                    self.lines.add(((x1, y1), (x2, y1)))
                    self.lines.add(((x1, y2), (x2, y2)))
        self.refresh()
    def run(self):
        self.tk = tkinter.Tk()
        self.tk.title('Plot3D')
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
        self.dist_scaler = tkinter.Scale(self.frame_right, from_ = 600.0, to = 6000.0, resolution = 60.0, length = 180, variable = self.dist_var, orient = tkinter.HORIZONTAL, label = 'Dist', command = self.dist_change)
        self.size_scaler = tkinter.Scale(self.frame_right, from_ = 100.0, to = 1000.0, resolution = 10.0, length = 180, variable = self.size_var, orient = tkinter.HORIZONTAL, label = 'Size', command = self.size_change)
        self.dist_scaler.pack()
        self.size_scaler.pack()
        self.dist = self.dist_var.get()
        self.size = self.size_var.get()
        self.frame_left = tkinter.Frame(self.canvas)
        self.frame_left.pack(side = tkinter.LEFT, anchor = tkinter.N)
        self.xbeg_var = tkinter.DoubleVar(value = -10.0)
        self.ybeg_var = tkinter.DoubleVar(value = -10.0)
        self.xend_var = tkinter.DoubleVar(value = +10.0)
        self.yend_var = tkinter.DoubleVar(value = +10.0)
        self.xnum_var = tkinter.IntVar(value = 20)
        self.ynum_var = tkinter.IntVar(value = 20)
        self.xbeg_scaler = tkinter.Scale(self.frame_left, from_ = -10.0, to = +10.0, resolution = 0.1, length = 180, variable = self.xbeg_var, orient = tkinter.HORIZONTAL, label = 'X beg')
        self.ybeg_scaler = tkinter.Scale(self.frame_left, from_ = -10.0, to = +10.0, resolution = 0.1, length = 180, variable = self.ybeg_var, orient = tkinter.HORIZONTAL, label = 'Y beg')
        self.xend_scaler = tkinter.Scale(self.frame_left, from_ = -10.0, to = +10.0, resolution = 0.1, length = 180, variable = self.xend_var, orient = tkinter.HORIZONTAL, label = 'X end')
        self.yend_scaler = tkinter.Scale(self.frame_left, from_ = -10.0, to = +10.0, resolution = 0.1, length = 180, variable = self.yend_var, orient = tkinter.HORIZONTAL, label = 'Y end')
        self.xnum_scaler = tkinter.Scale(self.frame_left, from_ = 1, to = 100, length = 180, variable = self.xnum_var, orient = tkinter.HORIZONTAL, label = 'X num')
        self.ynum_scaler = tkinter.Scale(self.frame_left, from_ = 1, to = 100, length = 180, variable = self.ynum_var, orient = tkinter.HORIZONTAL, label = 'Y num')
        self.xbeg_scaler.pack()
        self.ybeg_scaler.pack()
        self.xend_scaler.pack()
        self.yend_scaler.pack()
        self.xnum_scaler.pack()
        self.ynum_scaler.pack()
        self.frame_bottom = tkinter.Frame(self.tk)
        self.frame_bottom.pack(fill = tkinter.X)
        self.entry = tkinter.Entry(self.frame_bottom)
        self.entry.pack(side = tkinter.LEFT, expand = True, fill = tkinter.X)
        self.cross = tkinter.Button(self.frame_bottom, text = 'Cross Plot', command = lambda: self.plot(1))
        self.block = tkinter.Button(self.frame_bottom, text = 'Block Plot', command = lambda: self.plot(0))
        self.cross.pack(side = tkinter.LEFT)
        self.block.pack(side = tkinter.LEFT)
        self.tk.mainloop()
def main():
    Plot3D().run()
if __name__ == '__main__':
    main()
