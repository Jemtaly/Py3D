#!/usr/bin/env python3


import argparse
import tkinter as tk

import numpy as np
import tk3d


def main():
    prsr = argparse.ArgumentParser(description="3D Viewer for Wavefront OBJ Files")
    prsr.add_argument("file", type=argparse.FileType("r"))
    args = prsr.parse_args()
    vs = {}
    ls = set()
    for line in args.file:
        vals = line.split()
        if not vals:
            continue
        label, *vals = vals
        if label == "v":
            vs["V" + str(len(vs) + 1)] = np.array(vals, dtype=float)
        elif label == "p":
            ls.add(("V" + vals[0], "V" + vals[0]))
        elif label == "l":
            ls.add(("V" + vals[0], "V" + vals[1]))
        elif label == "f":
            ls.update(("V" + vals[i - 1].split("/")[0], "V" + vals[i].split("/")[0]) for i in range(len(vals)))
    args.file.close()
    root = tk.Tk()
    root.title("TkObjV3D")
    root.minsize(800, 600)
    objs = tk3d.ObjSpc(verts=vs, lines=ls)
    camv = tk3d.Camvas(root, objs)
    camv.pack(fill=tk.BOTH, expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
