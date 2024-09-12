#!/usr/bin/env python3


import tkinter as tk
import tkinter.messagebox as messagebox

import numpy as np
import tk3d


def main():
    wroot = tk.Tk()
    wroot.title("TkPlot3D")
    wroot.minsize(800, 600)
    objspc = tk3d.ObjSpc()
    camvas = tk3d.Camvas(wroot, objspc)
    camvas.pack(fill=tk.BOTH, expand=True)
    xmin_var = tk.DoubleVar(value=-10.0)
    ymin_var = tk.DoubleVar(value=-10.0)
    xmax_var = tk.DoubleVar(value=+10.0)
    ymax_var = tk.DoubleVar(value=+10.0)
    xnum_var = tk.IntVar(value=20)
    ynum_var = tk.IntVar(value=20)
    xmin_scaler = tk.Scale(camvas, from_=-10.0, to=+10.0, resolution=0.1, length=180, variable=xmin_var, orient=tk.HORIZONTAL, label="X min")
    ymin_scaler = tk.Scale(camvas, from_=-10.0, to=+10.0, resolution=0.1, length=180, variable=ymin_var, orient=tk.HORIZONTAL, label="Y min")
    xmax_scaler = tk.Scale(camvas, from_=-10.0, to=+10.0, resolution=0.1, length=180, variable=xmax_var, orient=tk.HORIZONTAL, label="X max")
    ymax_scaler = tk.Scale(camvas, from_=-10.0, to=+10.0, resolution=0.1, length=180, variable=ymax_var, orient=tk.HORIZONTAL, label="Y max")
    xnum_scaler = tk.Scale(camvas, from_=1, to=100, length=180, variable=xnum_var, orient=tk.HORIZONTAL, label="X num")
    ynum_scaler = tk.Scale(camvas, from_=1, to=100, length=180, variable=ynum_var, orient=tk.HORIZONTAL, label="Y num")
    xmin_scaler.pack(anchor=tk.W)
    xmax_scaler.pack(anchor=tk.W)
    xnum_scaler.pack(anchor=tk.W)
    ymin_scaler.pack(anchor=tk.W)
    ymax_scaler.pack(anchor=tk.W)
    ynum_scaler.pack(anchor=tk.W)
    frame = tk.Frame(wroot)
    frame.pack(fill=tk.X)
    entry = tk.Entry(frame)

    def plot(mode):
        xs = np.linspace(xmin_var.get(), xmax_var.get(), xnum_var.get() + 1, endpoint=True)
        ys = np.linspace(ymin_var.get(), ymax_var.get(), ynum_var.get() + 1, endpoint=True)
        try:
            fn = eval("lambda x, y: " + entry.get())
            vs = {(x, y): np.array([x, y, fn(x, y)], float) for x in xs for y in ys}
        except Exception as e:
            messagebox.showerror(e.__class__.__name__, str(e))
            return False
        if mode:
            lh = set(((x1, y0), (x2, y0)) for x1, x2 in zip(xs[:-1], xs[+1:]) for y0 in ys)
            lv = set(((x0, y1), (x0, y2)) for y1, y2 in zip(ys[:-1], ys[+1:]) for x0 in xs)
        else:
            lh = set(((x1, y1), (x2, y2)) for x1, x2 in zip(xs[:-1], xs[+1:]) for y1, y2 in zip(ys[:-1], ys[+1:]))
            lv = set(((x1, y2), (x2, y1)) for x1, x2 in zip(xs[:-1], xs[+1:]) for y1, y2 in zip(ys[:-1], ys[+1:]))
        objspc.reset(verts=vs, lines=lh | lv)
        return True

    rplot = tk.Button(frame, text="RPlot", command=lambda: plot(1))  # Rectangular plot
    dplot = tk.Button(frame, text="DPlot", command=lambda: plot(0))  # Diagonal plot
    reset = tk.Button(frame, text="Reset", command=lambda: objspc.reset())
    entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
    rplot.pack(side=tk.LEFT)
    dplot.pack(side=tk.LEFT)
    reset.pack(side=tk.LEFT)
    wroot.mainloop()


if __name__ == "__main__":
    main()
