#!/usr/bin/python3
def main():
    from PyQt5.QtWidgets import QApplication
    import qt3d, numpy, argparse, sys
    prsr = argparse.ArgumentParser(description = '3D Viewer for Wavefront OBJ Files')
    prsr.add_argument('file', type = argparse.FileType('r'))
    args = prsr.parse_args()
    vs = {}
    ls = set()
    for line in args.file:
        vals = line.split()
        if not vals:
            continue
        label, *vals = vals
        if label == 'v':
            vs['V' + str(len(vs) + 1)] = numpy.array(vals, dtype = float)
        elif label == 'p':
            ls.add(('V' + vals[0], 'V' + vals[0]))
        elif label == 'l':
            ls.add(('V' + vals[0], 'V' + vals[1]))
        elif label == 'f':
            ls.update(('V' + vals[i - 1].split('/')[0], 'V' + vals[i].split('/')[0]) for i in range(len(vals)))
    args.file.close()
    app = QApplication(sys.argv)
    objspc = qt3d.ObjSpc(verts = vs, lines = ls)
    camera = qt3d.QCamera(objspc)
    camera.setWindowTitle('ObjV3D')
    camera.setMinimumSize(800, 600)
    camera.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
