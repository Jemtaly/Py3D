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
        self.umin_var = tk.DoubleVar(value=-10.0)
        self.vmin_var = tk.DoubleVar(value=-10.0)
        self.umax_var = tk.DoubleVar(value=+10.0)
        self.vmax_var = tk.DoubleVar(value=+10.0)
        self.useg_var = tk.IntVar(value=20)
        self.vseg_var = tk.IntVar(value=20)
        umin_scaler = tk.Scale(self.camvas, from_=-10.0, to=+10.0, resolution=0.1, length=180, variable=self.umin_var, orient=tk.HORIZONTAL, label="u min")
        umax_scaler = tk.Scale(self.camvas, from_=-10.0, to=+10.0, resolution=0.1, length=180, variable=self.umax_var, orient=tk.HORIZONTAL, label="u max")
        useg_scaler = tk.Scale(self.camvas, from_=1, to=100, length=180, variable=self.useg_var, orient=tk.HORIZONTAL, label="u num")
        vmin_scaler = tk.Scale(self.camvas, from_=-10.0, to=+10.0, resolution=0.1, length=180, variable=self.vmin_var, orient=tk.HORIZONTAL, label="v min")
        vmax_scaler = tk.Scale(self.camvas, from_=-10.0, to=+10.0, resolution=0.1, length=180, variable=self.vmax_var, orient=tk.HORIZONTAL, label="v max")
        vseg_scaler = tk.Scale(self.camvas, from_=1, to=100, length=180, variable=self.vseg_var, orient=tk.HORIZONTAL, label="v num")
        umin_scaler.pack(anchor=tk.W)
        umax_scaler.pack(anchor=tk.W)
        useg_scaler.pack(anchor=tk.W)
        vmin_scaler.pack(anchor=tk.W)
        vmax_scaler.pack(anchor=tk.W)
        vseg_scaler.pack(anchor=tk.W)
        frame = tk.Frame(self)
        frame.pack(fill=tk.X)
        self.x_entry = tk.Entry(frame)
        self.y_entry = tk.Entry(frame)
        self.z_entry = tk.Entry(frame)
        button_rplot = tk.Button(frame, text="RPlot", command=lambda: self.plot(PlotMode.RECT))
        button_dplot = tk.Button(frame, text="DPlot", command=lambda: self.plot(PlotMode.DIAG))
        button_reset = tk.Button(frame, text="Reset", command=lambda: self.reset())
        button_saves = tk.Button(frame, text="Save", command=lambda: self.save())
        tk.Label(frame, text="x(u, v) =").pack(side=tk.LEFT)
        self.x_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        tk.Label(frame, text="y(u, v) =").pack(side=tk.LEFT)
        self.y_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        tk.Label(frame, text="z(u, v) =").pack(side=tk.LEFT)
        self.z_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        button_rplot.pack(side=tk.LEFT)
        button_dplot.pack(side=tk.LEFT)
        button_reset.pack(side=tk.LEFT)
        button_saves.pack(side=tk.LEFT)

    def reset(self):
        self.graph = None
        self.objspc.clear()
        self.camvas.refresh()

    def plot(self, mode: PlotMode):
        umin = self.umin_var.get()
        umax = self.umax_var.get()
        useg = self.useg_var.get()
        vmin = self.vmin_var.get()
        vmax = self.vmax_var.get()
        vseg = self.vseg_var.get()
        x_expr = self.x_entry.get()
        y_expr = self.y_entry.get()
        z_expr = self.z_entry.get()
        try:
            glob = __import__("numpy").__dict__
            x = eval(f"lambda u, v: float({x_expr})", glob)
            y = eval(f"lambda u, v: float({y_expr})", glob)
            z = eval(f"lambda u, v: float({z_expr})", glob)
            self.graph = Graph(x, y, z, umin, umax, useg, vmin, vmax, vseg)
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
