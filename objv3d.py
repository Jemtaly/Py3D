#!/usr/bin/python3
import tkinter, numpy, tk3d
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type = argparse.FileType('r'))
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
    args.file.close()
    tkroot = tkinter.Tk()
    tkroot.title('TkObjV3D')
    tkroot.minsize(800, 600)
    objspc = tk3d.ObjSpc(verts = vs, lines = ls)
    camvas = tk3d.Camvas(tkroot, objspc)
    camvas.pack(fill = tkinter.BOTH, expand = True)
    tkroot.mainloop()
if __name__ == '__main__':
    main()
