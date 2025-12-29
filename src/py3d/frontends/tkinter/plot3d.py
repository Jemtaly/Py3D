import tkinter as tk
from tkinter import messagebox, filedialog

from py3d.core.engine import ObjectSpace
from py3d.core.plot3d import Graph, PlotMode
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
        se_frame = tk.Frame(self.camvas)
        se_frame.place(relx=1.0, rely=1.0, anchor=tk.SE)
        umin_scaler = tk.Scale(se_frame, length=180, orient=tk.HORIZONTAL, label="u min", variable=self.umin_var, from_=-10.0, to=+10.0, resolution=0.1)
        umax_scaler = tk.Scale(se_frame, length=180, orient=tk.HORIZONTAL, label="u max", variable=self.umax_var, from_=-10.0, to=+10.0, resolution=0.1)
        useg_scaler = tk.Scale(se_frame, length=180, orient=tk.HORIZONTAL, label="u num", variable=self.useg_var, from_=1, to=100)
        vmin_scaler = tk.Scale(se_frame, length=180, orient=tk.HORIZONTAL, label="v min", variable=self.vmin_var, from_=-10.0, to=+10.0, resolution=0.1)
        vmax_scaler = tk.Scale(se_frame, length=180, orient=tk.HORIZONTAL, label="v max", variable=self.vmax_var, from_=-10.0, to=+10.0, resolution=0.1)
        vseg_scaler = tk.Scale(se_frame, length=180, orient=tk.HORIZONTAL, label="v num", variable=self.vseg_var, from_=1, to=100)
        umin_scaler.pack()
        umax_scaler.pack()
        useg_scaler.pack()
        vmin_scaler.pack()
        vmax_scaler.pack()
        vseg_scaler.pack()
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
        except BaseException as e:
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
        except BaseException as e:
            messagebox.showerror(e.__class__.__name__, str(e))


def main():
    app = Plot3DApp()
    app.mainloop()


if __name__ == "__main__":
    main()
