from typing import Callable, TextIO
from itertools import count
from enum import Enum

import numpy as np

from .engine import ObjectSpace, Vec3


class PlotMode(Enum):
    RECT = 0  # Rectangular plot
    DIAG = 1  # Diagonal plot


class Graph:
    useg: int
    vseg: int
    verts: dict[tuple[int, int], Vec3]

    def __init__(
        self,
        x: Callable[[float, float], float],
        y: Callable[[float, float], float],
        z: Callable[[float, float], float],
        umin: float,
        umax: float,
        useg: int,
        vmin: float,
        vmax: float,
        vseg: int,
    ):
        self.useg = useg
        self.vseg = vseg
        us = np.linspace(umin, umax, useg + 1, endpoint=True)
        vs = np.linspace(vmin, vmax, vseg + 1, endpoint=True)
        try:
            self.verts = {
                (i, j): np.array([x(u, v), y(u, v), z(u, v)], float)
                for i, u in enumerate(us)
                for j, v in enumerate(vs)
            }
        except Exception as e:
            raise e

    def plot(self, objspc: ObjectSpace, mode: PlotMode):
        objspc.clear()
        for key, value in self.verts.items():
            objspc.add_vert(key, value)
        match mode:
            case PlotMode.RECT:
                for i in range(self.useg):
                    for j in range(self.vseg + 1):
                        objspc.add_line((i, j), (i + 1, j))
                for j in range(self.vseg):
                    for i in range(self.useg + 1):
                        objspc.add_line((i, j), (i, j + 1))
            case PlotMode.DIAG:
                for i in range(self.useg):
                    for j in range(self.vseg):
                        objspc.add_line((i, j), (i + 1, j + 1))
                        objspc.add_line((i, j + 1), (i + 1, j))

    def save(self, file: TextIO):
        table = dict[tuple[int, int], int]()
        index = count(1)
        for i in range(self.useg + 1):
            for j in range(self.vseg + 1):
                x, y, z = self.verts[(i, j)]
                file.write(f"v {x} {y} {z}\n")
                table[(i, j)] = next(index)
        for i in range(self.useg):
            for j in range(self.vseg):
                v0 = table[(i + 0, j + 0)]
                v1 = table[(i + 1, j + 0)]
                v2 = table[(i + 1, j + 1)]
                v3 = table[(i + 0, j + 1)]
                file.write(f"f {v0} {v1} {v2} {v3}\n")
