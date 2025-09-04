from typing import Callable, TextIO
from itertools import count
from enum import Enum

import numpy as np

from .engine import ObjectSpace, Vec3


class PlotMode(Enum):
    RECT = 0  # Rectangular plot
    DIAG = 1  # Diagonal plot


class Graph:
    xseg: int
    yseg: int
    verts: dict[tuple[int, int], Vec3]

    def __init__(
        self,
        fn: Callable[[float, float], float],
        xmin: float,
        xmax: float,
        xseg: int,
        ymin: float,
        ymax: float,
        yseg: int,
    ):
        self.xseg = xseg
        self.yseg = yseg
        xs = np.linspace(xmin, xmax, xseg + 1, endpoint=True)
        ys = np.linspace(ymin, ymax, yseg + 1, endpoint=True)
        try:
            self.verts = {
                (i, j): np.array([x, y, fn(x, y)], float)
                for i, x in enumerate(xs)
                for j, y in enumerate(ys)
            }
        except Exception as e:
            raise e

    def plot(self, objspc: ObjectSpace, mode: PlotMode):
        objspc.clear()
        for key, value in self.verts.items():
            objspc.add_vert(key, value)
        match mode:
            case PlotMode.RECT:
                for i in range(self.xseg):
                    for j in range(self.yseg + 1):
                        objspc.add_line((i, j), (i + 1, j))
                for j in range(self.yseg):
                    for i in range(self.xseg + 1):
                        objspc.add_line((i, j), (i, j + 1))
            case PlotMode.DIAG:
                for i in range(self.xseg):
                    for j in range(self.yseg):
                        objspc.add_line((i, j), (i + 1, j + 1))
                        objspc.add_line((i, j + 1), (i + 1, j))

    def save(self, file: TextIO):
        table = dict[tuple[int, int], int]()
        index = count(1)
        for i in range(self.xseg + 1):
            for j in range(self.yseg + 1):
                x, y, z = self.verts[(i, j)]
                file.write(f"v {x} {y} {z}\n")
                table[(i, j)] = next(index)
        for i in range(self.xseg):
            for j in range(self.yseg):
                v0 = table[(i + 0, j + 0)]
                v1 = table[(i + 1, j + 0)]
                v2 = table[(i + 1, j + 1)]
                v3 = table[(i + 0, j + 1)]
                file.write(f"f {v0} {v1} {v2} {v3}\n")
