import argparse
import tkinter as tk

from core.obj_viewer import get_objspc
from .tk3d import Camvas


def main():
    prsr = argparse.ArgumentParser(description="3D Viewer for Wavefront OBJ Files")
    prsr.add_argument("file", type=argparse.FileType("r"))
    args = prsr.parse_args()
    objs = get_objspc(args.file)
    args.file.close()
    root = tk.Tk()
    root.title("TkObjV3D")
    root.minsize(800, 600)
    camv = Camvas(root, objs)
    camv.pack(fill=tk.BOTH, expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
