from typing import Generic, TypeVar, Any

import numpy as np

from .quaternion import Quaternion


T = TypeVar("T")
EulerVec3 = np.ndarray[tuple[int, ...], np.dtype[np.float64]]  # Type alias for Euler vector type
CoordVec3 = np.ndarray[tuple[int, ...], np.dtype[np.float64]]  # Type alias for vertex type
CoordVec2 = np.ndarray[tuple[int, ...], np.dtype[np.float64]]  # Type alias for 2D vector type
Scalar = np.floating[Any] | float # Type alias for scalar type, can be float or double


class ObjectSpace(Generic[T]):
    def __init__(self):
        self.verts = dict[T, CoordVec3]()
        self.lines = set[tuple[T, T]]()

    def clear(self):
        self.verts.clear()
        self.lines.clear()

    def add_vert(self, key: T, value: CoordVec3):
        self.verts[key] = value

    def del_vert(self, key: T):
        del self.verts[key]
        self.lines = {(i, j) for i, j in self.lines if i != key and j != key}

    def add_line(self, p: T, q: T):
        self.lines.add((p, q))

    def del_line(self, p: T, q: T):
        self.lines.remove((p, q))
        self.lines.remove((q, p))


class Camera(Generic[T]):
    coordv: CoordVec3
    rotate: Quaternion
    objspc: ObjectSpace[T]

    def __init__(
        self,
        objspc: ObjectSpace[T],
        coordv: CoordVec3 | None = None,
        eulerv: EulerVec3 | None = None,
    ):
        self.objspc = objspc
        if coordv is None:
            coordv = np.zeros(3)
        self.coordv = coordv.copy()
        if eulerv is None:
            eulerv = np.zeros(3)
        self.rotate = Quaternion.from_rvec(eulerv)

    def set_coordv(self, coordv: CoordVec3 | None = None):
        if coordv is None:
            coordv = np.zeros(3)
        self.coordv = coordv.copy()

    def set_eulerv(self, eulerv: EulerVec3 | None = None):
        if eulerv is None:
            eulerv = np.zeros(3)
        self.rotate = Quaternion.from_rvec(eulerv)

    def get_coordv(self) -> CoordVec3:
        return self.coordv

    def get_eulerv(self) -> EulerVec3:
        return self.rotate.to_rvec()

    def rota(self, rvec: EulerVec3):
        self.rotate *= Quaternion.from_rvec(rvec)
        return self

    def move(self, mvec: CoordVec3):
        self.coordv += self.rotate.inv().transform(mvec)
        return self

    def copy(self):
        return Camera(self.objspc, self.get_coordv(), self.get_eulerv())

    def get_position(self, absolute: CoordVec3, dist: Scalar) -> tuple[CoordVec2, int]:
        relative = self.rotate.transform(absolute - self.coordv)
        return relative[:2] / (relative[2] or 1.0) * dist, np.sign(relative[2])

    def draw(self, r: Scalar, dist: Scalar):
        positions = dict[T, tuple[CoordVec2, int]]()
        for k, absolute in self.objspc.verts.items():
            positions[k] = self.get_position(absolute, dist)
        for i, j in self.objspc.lines:
            P, p = positions[i]
            Q, q = positions[j]
            if p + q == 2:
                yield P, Q
            elif p == 1:
                V = Q if q == 0 else P - Q  # PQ'
                N = V / (np.linalg.norm(V) or 1.0)
                a, c = np.dot(P, N), np.linalg.norm(P)
                Q = P + N * ((np.sqrt(r * r - c * c + a * a) if r > c else abs(a)) - a)
                yield P, Q
            elif q == 1:
                V = P if p == 0 else Q - P  # QP'
                N = V / (np.linalg.norm(V) or 1.0)
                a, c = np.dot(Q, N), np.linalg.norm(Q)
                P = Q + N * ((np.sqrt(r * r - c * c + a * a) if r > c else abs(a)) - a)
                yield Q, P
