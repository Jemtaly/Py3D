from typing import TextIO
from itertools import count

import numpy as np

from .engine import ObjectSpace


def get_objspc(file: TextIO) -> ObjectSpace[int]:
    objs = ObjectSpace[int]()
    v = count(1)
    for line in file:
        match line.split():
            case ["v", x, y, z]:
                objs.add_vert(next(v), np.array([float(x), float(y), float(z)]))
            case ["p", i]:
                objs.add_line(int(i), int(i))
            case ["l", i, j]:
                objs.add_line(int(i), int(j))
            case ["f", *vals]:
                for I, J in zip(vals, [*vals[1:], vals[0]]):
                    i, *_ = I.split("/")
                    j, *_ = J.split("/")
                    objs.add_line(int(i), int(j))
            case _:
                continue
    return objs
