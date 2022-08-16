#!/usr/bin/python3
import tkinter, numpy, tk3d
def main():
    wroot = tkinter.Tk()
    wroot.title('TkPlot3D')
    wroot.minsize(800, 600)
    camvas = tk3d.Camvas(wroot)
    camvas.pack(fill = tkinter.BOTH, expand = True)
    def plot(cross):
        xrange = numpy.linspace(xmin_var.get(), xmax_var.get(), xinr_var.get() + 1, endpoint = True)
        yrange = numpy.linspace(ymin_var.get(), ymax_var.get(), yinr_var.get() + 1, endpoint = True)
        func = eval('lambda x, y: ' + entry.get())
        vs = {(x, y): numpy.array([x, y, func(x, y)]) for x in xrange for y in yrange}
        ls = set()
        if cross:
            for x1, x2 in zip(xrange[:-1], xrange[1:]):
                for y1, y2 in zip(yrange[:-1], yrange[1:]):
                    ls.add(((x1, y1), (x2, y2)))
                    ls.add(((x1, y2), (x2, y1)))
        else:
            for x1, x2 in zip(xrange[:-1], xrange[1:]):
                for y1, y2 in zip(yrange[:-1], yrange[1:]):
                    ls.add(((x1, y1), (x1, y2)))
                    ls.add(((x2, y1), (x2, y2)))
                    ls.add(((x1, y1), (x2, y1)))
                    ls.add(((x1, y2), (x2, y2)))
        camvas.reset(verts = vs, lines = ls)
    xmin_var = tkinter.DoubleVar(value = -10.0)
    ymin_var = tkinter.DoubleVar(value = -10.0)
    xmax_var = tkinter.DoubleVar(value = +10.0)
    ymax_var = tkinter.DoubleVar(value = +10.0)
    xinr_var = tkinter.IntVar(value = 20)
    yinr_var = tkinter.IntVar(value = 20)
    xmin_scaler = tkinter.Scale(camvas, from_ = -10.0, to = +10.0, resolution = 0.1, length = 180, variable = xmin_var, orient = tkinter.HORIZONTAL, label = 'X min')
    ymin_scaler = tkinter.Scale(camvas, from_ = -10.0, to = +10.0, resolution = 0.1, length = 180, variable = ymin_var, orient = tkinter.HORIZONTAL, label = 'Y min')
    xmax_scaler = tkinter.Scale(camvas, from_ = -10.0, to = +10.0, resolution = 0.1, length = 180, variable = xmax_var, orient = tkinter.HORIZONTAL, label = 'X max')
    ymax_scaler = tkinter.Scale(camvas, from_ = -10.0, to = +10.0, resolution = 0.1, length = 180, variable = ymax_var, orient = tkinter.HORIZONTAL, label = 'Y max')
    xinr_scaler = tkinter.Scale(camvas, from_ = 1, to = 100, length = 180, variable = xinr_var, orient = tkinter.HORIZONTAL, label = 'X intervals')
    yinr_scaler = tkinter.Scale(camvas, from_ = 1, to = 100, length = 180, variable = yinr_var, orient = tkinter.HORIZONTAL, label = 'Y intervals')
    xmin_scaler.pack(anchor = tkinter.W)
    ymin_scaler.pack(anchor = tkinter.W)
    xmax_scaler.pack(anchor = tkinter.W)
    ymax_scaler.pack(anchor = tkinter.W)
    xinr_scaler.pack(anchor = tkinter.W)
    yinr_scaler.pack(anchor = tkinter.W)
    frame = tkinter.Frame(wroot)
    frame.pack(fill = tkinter.X)
    entry = tkinter.Entry(frame)
    cross = tkinter.Button(frame, text = 'Cross Plot', command = lambda: plot(1))
    block = tkinter.Button(frame, text = 'Block Plot', command = lambda: plot(0))
    entry.pack(side = tkinter.LEFT, expand = True, fill = tkinter.X)
    cross.pack(side = tkinter.LEFT)
    block.pack(side = tkinter.LEFT)
    wroot.mainloop()
if __name__ == '__main__':
    main()
