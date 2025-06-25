import tkinter as tk
from tkinter import messagebox

from core.engine import ObjectSpace
from core.plot3d import PlotMode, objspc_plot
from .tk3d import Camvas


def main():
    root = tk.Tk()
    root.title("TkPlot3D")
    root.minsize(800, 600)
    objspc = ObjectSpace()
    camvas = Camvas(root, objspc)
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
    frame = tk.Frame(root)
    frame.pack(fill=tk.X)
    entry = tk.Entry(frame)

    def plot(mode: PlotMode):
        xmin = xmin_var.get()
        xmax = xmax_var.get()
        ymin = ymin_var.get()
        ymax = ymax_var.get()
        xnum = xnum_var.get()
        ynum = ynum_var.get()
        try:
            fn = eval("lambda x, y: " + entry.get())
            objspc_plot(objspc, xmin, xmax, xnum, ymin, ymax, ynum, fn, mode)
        except Exception as e:
            messagebox.showerror(e.__class__.__name__, str(e))
        camvas.refresh()

    def reset():
        objspc.clear()
        camvas.refresh()

    button_rplot = tk.Button(frame, text="RPlot", command=lambda: plot(PlotMode.RECT))  # Rectangular plot
    button_dplot = tk.Button(frame, text="DPlot", command=lambda: plot(PlotMode.DIAG))  # Diagonal plot
    button_reset = tk.Button(frame, text="Reset", command=lambda: reset())
    entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
    button_rplot.pack(side=tk.LEFT)
    button_dplot.pack(side=tk.LEFT)
    button_reset.pack(side=tk.LEFT)
    root.mainloop()


if __name__ == "__main__":
    main()
