#!/usr/bin/python3
def main():
    import tkinter, tkinter.messagebox, tk3d, numpy
    wroot = tkinter.Tk()
    wroot.title('TkPlot3D')
    wroot.minsize(800, 600)
    objspc = tk3d.ObjSpc()
    camvas = tk3d.Camvas(wroot, objspc)
    camvas.pack(fill = tkinter.BOTH, expand = True)
    xmin_var = tkinter.DoubleVar(value = -10.0)
    ymin_var = tkinter.DoubleVar(value = -10.0)
    xmax_var = tkinter.DoubleVar(value = +10.0)
    ymax_var = tkinter.DoubleVar(value = +10.0)
    xnum_var = tkinter.IntVar(value = 20)
    ynum_var = tkinter.IntVar(value = 20)
    xmin_scaler = tkinter.Scale(camvas, from_ = -10.0, to = +10.0, resolution = 0.1, length = 180, variable = xmin_var, orient = tkinter.HORIZONTAL, label = 'X min')
    ymin_scaler = tkinter.Scale(camvas, from_ = -10.0, to = +10.0, resolution = 0.1, length = 180, variable = ymin_var, orient = tkinter.HORIZONTAL, label = 'Y min')
    xmax_scaler = tkinter.Scale(camvas, from_ = -10.0, to = +10.0, resolution = 0.1, length = 180, variable = xmax_var, orient = tkinter.HORIZONTAL, label = 'X max')
    ymax_scaler = tkinter.Scale(camvas, from_ = -10.0, to = +10.0, resolution = 0.1, length = 180, variable = ymax_var, orient = tkinter.HORIZONTAL, label = 'Y max')
    xnum_scaler = tkinter.Scale(camvas, from_ = 1, to = 100, length = 180, variable = xnum_var, orient = tkinter.HORIZONTAL, label = 'X num')
    ynum_scaler = tkinter.Scale(camvas, from_ = 1, to = 100, length = 180, variable = ynum_var, orient = tkinter.HORIZONTAL, label = 'Y num')
    xmin_scaler.pack(anchor = tkinter.W)
    xmax_scaler.pack(anchor = tkinter.W)
    xnum_scaler.pack(anchor = tkinter.W)
    ymin_scaler.pack(anchor = tkinter.W)
    ymax_scaler.pack(anchor = tkinter.W)
    ynum_scaler.pack(anchor = tkinter.W)
    frame = tkinter.Frame(wroot)
    frame.pack(fill = tkinter.X)
    entry = tkinter.Entry(frame)
    def plot(mode):
        xs = numpy.linspace(xmin_var.get(), xmax_var.get(), xnum_var.get() + 1, endpoint = True)
        ys = numpy.linspace(ymin_var.get(), ymax_var.get(), ynum_var.get() + 1, endpoint = True)
        try:
            fn = eval('lambda x, y: ' + entry.get())
            vs = {(x, y): numpy.array([x, y, fn(x, y)], float) for x in xs for y in ys}
        except Exception as e:
            tkinter.messagebox.showerror(e.__class__.__name__, str(e))
            return False
        if mode:
            lh = set(((x1, y0), (x2, y0)) for x1, x2 in zip(xs[:-1], xs[+1:]) for y0 in ys)
            lv = set(((x0, y1), (x0, y2)) for y1, y2 in zip(ys[:-1], ys[+1:]) for x0 in xs)
        else:
            lh = set(((x1, y1), (x2, y2)) for x1, x2 in zip(xs[:-1], xs[+1:]) for y1, y2 in zip(ys[:-1], ys[+1:]))
            lv = set(((x1, y2), (x2, y1)) for x1, x2 in zip(xs[:-1], xs[+1:]) for y1, y2 in zip(ys[:-1], ys[+1:]))
        objspc.reset(verts = vs, lines = lh | lv)
        return True
    rplot = tkinter.Button(frame, text = 'RPlot', command = lambda: plot(1)) # Rectangular plot
    dplot = tkinter.Button(frame, text = 'DPlot', command = lambda: plot(0)) # Diagonal plot
    reset = tkinter.Button(frame, text = 'Reset', command = lambda: objspc.reset())
    entry.pack(side = tkinter.LEFT, expand = True, fill = tkinter.X)
    rplot.pack(side = tkinter.LEFT)
    dplot.pack(side = tkinter.LEFT)
    reset.pack(side = tkinter.LEFT)
    wroot.mainloop()
if __name__ == '__main__':
    main()
