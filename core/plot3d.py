from typing import Callable
from enum import Enum

import numpy as np

from .engine import ObjectSpace


class PlotMode(Enum):
    RECT = 0  # Rectangular plot
    DIAG = 1  # Diagonal plot


def objspc_plot(
    objspc: ObjectSpace,
    xmin: float,
    xmax: float,
    xnum: int,
    ymin: float,
    ymax: float,
    ynum: int,
    fn: Callable[[float, float], float],
    mode: PlotMode,
):
    objspc.clear()
    xs = np.linspace(xmin, xmax, xnum + 1, endpoint=True)
    ys = np.linspace(ymin, ymax, ynum + 1, endpoint=True)
    try:
        for x in xs:
            for y in ys:
                objspc.add_vert((x, y), np.array([x, y, fn(x, y)], float))
    except Exception as e:
        raise e
    match mode:
        case PlotMode.RECT:
            for x1, x2 in zip(xs[:-1], xs[+1:]):
                for y0 in ys:
                    objspc.add_line((x1, y0), (x2, y0))
            for y1, y2 in zip(ys[:-1], ys[+1:]):
                for x0 in xs:
                    objspc.add_line((x0, y1), (x0, y2))
        case PlotMode.DIAG:
            for x1, x2 in zip(xs[:-1], xs[+1:]):
                for y1, y2 in zip(ys[:-1], ys[+1:]):
                    objspc.add_line((x1, y1), (x2, y2))
            for x1, x2 in zip(xs[:-1], xs[+1:]):
                for y1, y2 in zip(ys[:-1], ys[+1:]):
                    objspc.add_line((x1, y2), (x2, y1))
