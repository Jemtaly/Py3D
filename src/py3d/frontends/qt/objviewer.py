import argparse
import sys

from PyQt5.QtWidgets import QApplication

from py3d.core.objviewer import get_objspc
from .qt3d import QCamera


def main():
    prsr = argparse.ArgumentParser(description="3D Viewer for Wavefront OBJ Files")
    prsr.add_argument("file", type=argparse.FileType("r"))
    args = prsr.parse_args()
    objspc = get_objspc(args.file)
    args.file.close()

    app = QApplication(sys.argv)
    camera = QCamera(objspc)
    camera.setWindowTitle("ObjV3D")
    camera.setMinimumSize(800, 600)
    camera.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
