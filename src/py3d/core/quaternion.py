from typing import overload
from dataclasses import dataclass

import numpy as np


CoordVec3R = np.ndarray
EulerVec3R = np.ndarray
EulerMat3x3R = np.ndarray
PauliMat2x2C = np.ndarray


def vec2mat(rvec: EulerVec3R) -> EulerMat3x3R:
    H = np.linalg.norm(rvec)
    S, C = np.sin(H), np.cos(H)
    x, y, z = rvec / H if H else np.zeros(3)
    return np.array(
        [
            [
                x * x * (1 - C) + 1 * C,
                x * y * (1 - C) + z * S,
                x * z * (1 - C) - y * S,
            ],
            [
                y * x * (1 - C) - z * S,
                y * y * (1 - C) + 1 * C,
                y * z * (1 - C) + x * S,
            ],
            [
                z * x * (1 - C) + y * S,
                z * y * (1 - C) - x * S,
                z * z * (1 - C) + 1 * C,
            ],
        ]
    )


def mat2vec(rmat: EulerMat3x3R) -> EulerVec3R:
    assert np.allclose(rmat @ rmat.T, np.eye(3))
    H = np.arccos((np.trace(rmat) - 1) / 2)
    if np.isclose(H, 0.0):
        return np.zeros(3)
    rx = (rmat[1, 2] - rmat[2, 1]) / (2 * np.sin(H))
    ry = (rmat[2, 0] - rmat[0, 2]) / (2 * np.sin(H))
    rz = (rmat[0, 1] - rmat[1, 0]) / (2 * np.sin(H))
    return np.array([rx, ry, rz]) * H


@dataclass
class Quaternion:
    w: float
    x: float = 0
    y: float = 0
    z: float = 0

    @staticmethod
    def from_coord(v: CoordVec3R) -> "Quaternion":
        x, y, z = v
        return Quaternion(0, x, y, z)

    def to_coord(self) -> CoordVec3R:
        x, y, z = self.x, self.y, self.z
        return np.array([x, y, z])

    @overload
    def transform(self, v: EulerVec3R) -> EulerVec3R: ...

    @overload
    def transform(self, v: "Quaternion") -> "Quaternion": ...

    def transform(self, v: "EulerVec3R | Quaternion") -> "EulerVec3R | Quaternion":
        if isinstance(v, Quaternion):
            return ~self * v * self
        return (~self * Quaternion.from_coord(v) * self).to_coord()

    def __repr__(self) -> str:
        return "<%s, %s, %s, %s>" % (self.w, self.x, self.y, self.z)

    def __neg__(self) -> "Quaternion":
        return Quaternion(-self.w, -self.x, -self.y, -self.z)

    def __pos__(self) -> "Quaternion":
        return Quaternion(+self.w, +self.x, +self.y, +self.z)

    def conj(self) -> "Quaternion":
        return Quaternion(+self.w, -self.x, -self.y, -self.z)

    def __abs__(self) -> float:
        return (self.w**2 + self.x**2 + self.y**2 + self.z**2) ** 0.5

    def inv(self) -> "Quaternion":
        norm_squared = self.w**2 + self.x**2 + self.y**2 + self.z**2
        return Quaternion(
            +self.w / norm_squared,
            -self.x / norm_squared,
            -self.y / norm_squared,
            -self.z / norm_squared,
        )

    def __invert__(self) -> "Quaternion":
        return self.inv()

    def __add__(self, fles: "Quaternion") -> "Quaternion":
        return Quaternion(
            self.w + fles.w,
            self.x + fles.x,
            self.y + fles.y,
            self.z + fles.z,
        )

    def __sub__(self, fles: "Quaternion") -> "Quaternion":
        return Quaternion(
            self.w - fles.w,
            self.x - fles.x,
            self.y - fles.y,
            self.z - fles.z,
        )

    def __truediv__(self, num: float) -> "Quaternion":
        return Quaternion(
            self.w / num,
            self.x / num,
            self.y / num,
            self.z / num,
        )

    def __mul__(self, fles: "Quaternion | float") -> "Quaternion":
        if not isinstance(fles, Quaternion):
            return Quaternion(
                self.w * fles,
                self.x * fles,
                self.y * fles,
                self.z * fles,
            )
        return Quaternion(
            self.w * fles.w - self.x * fles.x - self.y * fles.y - self.z * fles.z,
            self.w * fles.x + self.x * fles.w + self.y * fles.z - self.z * fles.y,
            self.w * fles.y - self.x * fles.z + self.y * fles.w + self.z * fles.x,
            self.w * fles.z + self.x * fles.y - self.y * fles.x + self.z * fles.w,
        )

    def exp(self) -> "Quaternion":
        h = (self.x**2 + self.y**2 + self.z**2) ** 0.5
        s, c = np.sin(h), np.cos(h)
        x, y, z = (self.x / h, self.y / h, self.z / h) if h else (0, 0, 0)
        return Quaternion(c, x * s, y * s, z * s) * np.exp(self.w)

    def log(self) -> "Quaternion":
        norm = abs(self)
        unit = (self / norm) if norm else Quaternion(1)
        c = unit.w
        h = np.arccos(c)
        s = np.sin(h)
        x, y, z = (unit.x / s, unit.y / s, unit.z / s) if s else (0, 0, 0)
        return Quaternion(np.log(norm), x * h, y * h, z * h)

    def __pow__(self, num: float) -> "Quaternion":
        return (self.log() * num).exp()

    @staticmethod
    def from_rvec(rvec: EulerVec3R) -> "Quaternion":
        x, y, z = rvec
        r = Quaternion(0, x, y, z)
        return (r / 2).exp()

    def to_rvec(self) -> EulerVec3R:
        r = self.log() * 2
        x, y, z = r.x, r.y, r.z
        return np.array([x, y, z])

    @staticmethod
    def from_euler(mat: EulerMat3x3R) -> "Quaternion":
        return Quaternion.from_rvec(mat2vec(mat))

    def to_euler(self) -> EulerMat3x3R:
        return vec2mat(self.to_rvec())

    @staticmethod
    def from_pauli(mat: PauliMat2x2C) -> "Quaternion":
        w = (+mat[0, 0].real + +mat[1, 1].real) / 2
        x = (-mat[0, 1].imag + -mat[1, 0].imag) / 2
        y = (-mat[0, 1].real + +mat[1, 0].real) / 2
        z = (-mat[0, 0].imag + +mat[1, 1].imag) / 2
        return Quaternion(w, x, y, z)

    def to_pauli(self) -> PauliMat2x2C:
        return np.array(
            [
                [self.w * +1 + self.z * -1j, self.y * -1 + self.x * -1j],
                [self.y * +1 + self.x * -1j, self.w * +1 + self.z * +1j],
            ]
        )
