from typing import TextIO

import numpy as np

from .engine import ObjectSpace


def get_objspc(file: TextIO) -> ObjectSpace:
    objs = ObjectSpace()
    c = 1
    for line in file:
        vals = line.split()
        if not vals:
            continue
        label, *vals = vals
        if label == "v":
            objs.add_vert(f"V{c}", np.array(vals, dtype=float))
        elif label == "p":
            objs.add_line(f"V{vals[0]}", f"V{vals[0]}")
        elif label == "l":
            objs.add_line(f"V{vals[0]}", f"V{vals[1]}")
        elif label == "f":
            for I, J in zip(vals, [*vals[1:], vals[0]]):
                i = I.split("/")[0]
                j = J.split("/")[0]
                objs.add_line(f"V{i}", f"V{j}")
        c += 1
    return objs
