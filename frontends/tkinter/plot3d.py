import tkinter as tk
from tkinter import messagebox, filedialog

from core.engine import ObjectSpace
from core.plot3d import Graph, PlotMode
from .tk3d import Camvas


class Plot3DApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TkPlot3D")
        self.minsize(800, 600)
        self.graph = None
        self.objspc = ObjectSpace()
        self.camvas = Camvas(self, self.objspc)
        self.camvas.pack(fill=tk.BOTH, expand=True)
        self.xmin_var = tk.DoubleVar(value=-10.0)
        self.ymin_var = tk.DoubleVar(value=-10.0)
        self.xmax_var = tk.DoubleVar(value=+10.0)
        self.ymax_var = tk.DoubleVar(value=+10.0)
        self.xseg_var = tk.IntVar(value=20)
        self.yseg_var = tk.IntVar(value=20)
        xmin_scaler = tk.Scale(self.camvas, from_=-10.0, to=+10.0, resolution=0.1, length=180, variable=self.xmin_var, orient=tk.HORIZONTAL, label="X min")
        ymin_scaler = tk.Scale(self.camvas, from_=-10.0, to=+10.0, resolution=0.1, length=180, variable=self.ymin_var, orient=tk.HORIZONTAL, label="Y min")
        xmax_scaler = tk.Scale(self.camvas, from_=-10.0, to=+10.0, resolution=0.1, length=180, variable=self.xmax_var, orient=tk.HORIZONTAL, label="X max")
        ymax_scaler = tk.Scale(self.camvas, from_=-10.0, to=+10.0, resolution=0.1, length=180, variable=self.ymax_var, orient=tk.HORIZONTAL, label="Y max")
        xseg_scaler = tk.Scale(self.camvas, from_=1, to=100, length=180, variable=self.xseg_var, orient=tk.HORIZONTAL, label="X num")
        yseg_scaler = tk.Scale(self.camvas, from_=1, to=100, length=180, variable=self.yseg_var, orient=tk.HORIZONTAL, label="Y num")
        xmin_scaler.pack(anchor=tk.W)
        xmax_scaler.pack(anchor=tk.W)
        xseg_scaler.pack(anchor=tk.W)
        ymin_scaler.pack(anchor=tk.W)
        ymax_scaler.pack(anchor=tk.W)
        yseg_scaler.pack(anchor=tk.W)
        frame = tk.Frame(self)
        frame.pack(fill=tk.X)
        self.entry = tk.Entry(frame)
        button_rplot = tk.Button(frame, text="RPlot", command=lambda: self.plot(PlotMode.RECT))
        button_dplot = tk.Button(frame, text="DPlot", command=lambda: self.plot(PlotMode.DIAG))
        button_reset = tk.Button(frame, text="Reset", command=lambda: self.reset())
        button_saves = tk.Button(frame, text="Save", command=lambda: self.save())
        self.entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        button_rplot.pack(side=tk.LEFT)
        button_dplot.pack(side=tk.LEFT)
        button_reset.pack(side=tk.LEFT)
        button_saves.pack(side=tk.LEFT)

    def reset(self):
        self.graph = None
        self.objspc.clear()
        self.camvas.refresh()

    def plot(self, mode: PlotMode):
        xmin = self.xmin_var.get()
        xmax = self.xmax_var.get()
        ymin = self.ymin_var.get()
        ymax = self.ymax_var.get()
        xseg = self.xseg_var.get()
        yseg = self.yseg_var.get()
        try:
            fn = eval("lambda x, y: " + self.entry.get())
            self.graph = Graph(fn, xmin, xmax, xseg, ymin, ymax, yseg)
        except Exception as e:
            messagebox.showerror(e.__class__.__name__, str(e))
        else:
            self.graph.plot(self.objspc, mode)
            self.camvas.refresh()

    def save(self):
        if self.graph is None:
            messagebox.showwarning("Warning", "No graph to save.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".obj", filetypes=[("Wavefront OBJ Files", "*.obj"), ("All files", "*.*")])
        if not path:
            return
        try:
            with open(path, "w") as file:
                self.graph.save(file)
        except Exception as e:
            messagebox.showerror(e.__class__.__name__, str(e))


def main():
    app = Plot3DApp()
    app.mainloop()


if __name__ == "__main__":
    main()
