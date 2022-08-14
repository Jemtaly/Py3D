#!/usr/bin/python3
import tkinter, numpy, tk3d
def main():
    import argparse, sys
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type = argparse.FileType('r'), default = sys.stdin)
    args = parser.parse_args()
    vs = {}
    ls = set()
    for line in args.file:
        vals = line.split()
        if not vals:
            continue
        label, *vals = vals
        if label == 'v':
            vs['V' + str(len(vs) + 1)] = numpy.array([float(vals[0]), float(vals[1]), float(vals[2])])
        elif label == 'p':
            ls.add(('V' + vals[0], 'V' + vals[0]))
        elif label == 'l':
            ls.add(('V' + vals[0], 'V' + vals[1]))
        elif label == 'f':
            for i in range(len(vals)):
                ls.add(('V' + vals[i].split('/')[0], 'V' + vals[i - 1].split('/')[0]))
    root = tkinter.Tk()
    root.title('TkObjV3D')
    root.minsize(800, 600)
    tk3d.Camvas(root, verts = vs, lines = ls).pack(fill = tkinter.BOTH, expand = True)
    root.mainloop()
if __name__ == '__main__':
    main()
