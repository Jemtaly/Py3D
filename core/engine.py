from typing import Generic, TypeVar, Any

import numpy as np

T = TypeVar("T")
Vec3 = np.ndarray[tuple[int, ...], np.dtype[np.float64]]  # Type alias for vertex type
Vec2 = np.ndarray[tuple[int, ...], np.dtype[np.float64]]  # Type alias for 2D vector type
M3x3 = np.ndarray[tuple[int, ...], np.dtype[np.float64]]  # Type alias for 3x3 matrix type
Scalar = np.floating[Any]  # Type alias for scalar type, can be float or double


class ObjectSpace(Generic[T]):
    def __init__(self):
        self.verts = dict[T, Vec3]()
        self.lines = set[tuple[T, T]]()

    def clear(self):
        self.verts.clear()
        self.lines.clear()

    def add_vert(self, key: T, value: Vec3):
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
    coordn: Vec3
    matric: M3x3
    objspc: ObjectSpace[T]

    def __init__(self, objspc: ObjectSpace[T], coordn: Vec3 | None = None, matrix: M3x3 | None = None):
        self.objspc = objspc
        if coordn is None:
            coordn = np.zeros(3)
        self.coordn = coordn
        if matrix is None:
            matrix = np.eye(3)
        assert np.allclose(matrix @ matrix.T, np.eye(3))
        self.matrix = matrix

    def set_coordn(self, coordn: Vec3 | None = None):
        if coordn is None:
            coordn = np.zeros(3)
        self.coordn = coordn

    def set_matrix(self, matrix: M3x3 | None = None):
        if matrix is None:
            matrix = np.eye(3)
        assert np.allclose(matrix @ matrix.T, np.eye(3))
        self.matrix = matrix

    def rota(self, rvec: Vec3):
        norm = np.linalg.norm(rvec)
        s, c = np.sin(norm), np.cos(norm)
        x, y, z = rvec / norm if norm else np.zeros(3)
        self.matrix = np.array(
            [
                [x * x * (1 - c) + 1 * c, x * y * (1 - c) + z * s, x * z * (1 - c) - y * s],
                [y * x * (1 - c) - z * s, y * y * (1 - c) + 1 * c, y * z * (1 - c) + x * s],
                [z * x * (1 - c) + y * s, z * y * (1 - c) - x * s, z * z * (1 - c) + 1 * c],
            ]
        ).dot(self.matrix)

    def move(self, mvec: Vec3):
        self.coordn += np.linalg.inv(self.matrix).dot(mvec)

    def get_position(self, absolute: Vec3, dist: float) -> tuple[Vec2, int]:
        relative = self.matrix.dot(absolute - self.coordn)
        return relative[:2] / (relative[2] or 1.0) * dist, np.sign(relative[2])

    def draw(self, r: Scalar, dist: float):
        positions = dict[T, tuple[Vec2, int]]()
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
