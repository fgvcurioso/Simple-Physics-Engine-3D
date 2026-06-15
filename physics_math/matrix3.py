from physics_math.vector3 import Vector3
from dataclasses import dataclass, field

@dataclass
class Matrix3:
    row0: "Vector3" = field(default_factory=lambda : Vector3(1, 0, 0))
    row1: "Vector3" = field(default_factory=lambda : Vector3(0, 1, 0))
    row2: "Vector3" = field(default_factory=lambda : Vector3(0, 0, 1))


    @property
    def col0(self) -> Vector3:
        return Vector3(self.row0.x, self.row1.x, self.row2.x)

    @property
    def col1(self) -> Vector3:
        return Vector3(self.row0.y, self.row1.y, self.row2.y)

    @property
    def col2(self) -> Vector3:
        return Vector3(self.row0.z, self.row1.z, self.row2.z)

    def __post_init__(self):
        for name, value in [("row0", self.row0), ("row1", self.row1), ("row2", self.row2)]:
            if not isinstance(value, Vector3):
                raise TypeError(f"{name} must be a Vector3, got {type(value).__name__}")

    @classmethod
    def skew_symmetric(cls, w: Vector3) -> "Matrix3":
        if not isinstance(w, Vector3):
            raise TypeError(f"Parameter must be a Vector3, got: {type(w).__name__}")

        return cls(
        Vector3(0,    -w.z,  w.y),
        Vector3(w.z,   0,   -w.x),
        Vector3(-w.y,  w.x,  0)
    )

    def __add__(self, other : "Matrix3") -> "Matrix3":
        if not isinstance(other, Matrix3):
            return NotImplemented
        return Matrix3(self.row0 + other.row0, self.row1 + other.row1, self.row2 + other.row2)


    def transform(self, vector: "Vector3" ) -> "Vector3":
        if not isinstance(vector, Vector3):
            return NotImplemented
        return Vector3(self.row0.dot(vector), self.row1.dot(vector), self.row2.dot(vector))

    def compose(self, other: "Matrix3" ) -> "Matrix3":
        if not isinstance(other, Matrix3):
            return NotImplemented
        row_0 = Vector3(other.col0.dot(self.row0), other.col1.dot(self.row0), other.col2.dot(self.row0))
        row_1 = Vector3(other.col0.dot(self.row1), other.col1.dot(self.row1), other.col2.dot(self.row1))
        row_2 = Vector3(other.col0.dot(self.row2), other.col1.dot(self.row2), other.col2.dot(self.row2))
        return Matrix3(row_0, row_1, row_2)
        
    def __mul__(self, other):
        if isinstance(other, Vector3):
            return self.transform(other)
        elif isinstance(other, Matrix3):
            return self.compose(other)
        elif isinstance(other, (int, float)):
            return self._scale(other)
        else:
            return NotImplemented

    def __rmul__(self, scalar: int | float) -> "Matrix3":
        return self._scale(scalar)

    def _scale(self, scalar: int | float) -> "Matrix3":
        return Matrix3(self.row0 * scalar, self.row1 * scalar, self.row2 * scalar)


    def transpose(self) -> "Matrix3":
        return Matrix3(self.col0, self.col1, self.col2)

    def determinant(self) -> float:
        a = self.row0.x
        b = self.row0.y
        c = self.row0.z
        d = self.row1.x
        e = self.row1.y
        f = self.row1.z
        g = self.row2.x
        h = self.row2.y
        i = self.row2.z
        return a*(e*i - f*h) -b*(d*i -f*g) +c*(d*h -e*g)

    def inverse(self):
        det = self.determinant()
        if abs(det) < 1e-9:
            raise ValueError("Matrix is singular (determinant is zero): cannot compute inverse.")
        ## Cofactor matrix
        c00 = self.row1.y * self.row2.z - self.row2.y * self.row1.z
        c01 = -1* (self.row1.x * self.row2.z - self.row2.x * self.row1.z)
        c02 = self.row1.x * self.row2.y - self.row2.x * self.row1.y
        c10 = -1* (self.row0.y * self.row2.z - self.row2.y * self.row0.z)
        c11 = self.row0.x * self.row2.z - self.row2.x * self.row0.z
        c12 = -1* (self.row0.x * self.row2.y - self.row2.x * self.row0.y)
        c20 = self.row0.y * self.row1.z - self.row1.y * self.row0.z
        c21 = -1* (self.row0.x * self.row1.z - self.row1.x * self.row0.z)
        c22 = self.row0.x * self.row1.y - self.row1.x * self.row0.y

        cof_m = Matrix3(Vector3(c00,c01,c02), Vector3(c10, c11, c12), Vector3(c20, c21, c22))
        adj = cof_m.transpose()
        return adj * (1/ det)

    def orthonormalize(self) -> "Matrix3":
        x = self.col0.normalize()
        z = x.cross(self.col1).normalize()
        y = z.cross(x)
        return Matrix3(
            Vector3(x.x, y.x, z.x),
            Vector3(x.y, y.y, z.y),
            Vector3(x.z, y.z, z.z)
        )