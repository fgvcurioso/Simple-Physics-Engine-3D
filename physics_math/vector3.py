
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Vector3:
    """A 3D vector with floating-point components, used for physics calculations."""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __eq__(self, other: "Vector3") -> bool:
        """
        Check equality using a small absolute tolerance (1e-9) to account for 
        floating-point precision errors.
        """
        if not isinstance(other, Vector3):
            return NotImplemented

        return (
            math.isclose(self.x, other.x, abs_tol=1e-9) and
            math.isclose(self.y, other.y, abs_tol=1e-9) and
            math.isclose(self.z, other.z, abs_tol=1e-9)
        )

    def __add__(self, other: "Vector3") -> "Vector3":
        if not isinstance(other, Vector3):
            return NotImplemented

        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector3") -> "Vector3":
        if not isinstance(other, Vector3):
            return NotImplemented

        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__ (self, value: int | float) -> "Vector3":
        if not isinstance(value, (int, float)):
            return NotImplemented
        return Vector3(self.x * value , self.y * value, self.z * value)

    def __rmul__(self, value: int | float) -> "Vector3":
        return self.__mul__(value)

    def __truediv__(self, value: int | float) -> "Vector3":
        if not isinstance(value, (int, float)):
            return NotImplemented
        if abs(value) < 1e-9:
            raise ZeroDivisionError("division by zero: Cannot divide a Vector3 by scalar zero.")
        return Vector3(self.x / value , self.y / value, self.z / value)

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self) -> "Vector3":
        """
        Return a unit vector pointing in the same direction. 
        Raises ZeroDivisionError if the vector is too small to normalize.
        """
        magnitude = self.magnitude()
        if abs(magnitude) < 1e-9:
            raise ZeroDivisionError("Cannot normalize a zero vector (magnitude is 0).")
        return self / magnitude

    def dot(self, other: "Vector3") -> float :
        if not isinstance(other, Vector3):
            raise TypeError(f"unsupported operand type(s) for dot(): 'Vector3' and '{type(other).__name__}'")
        return self.x * other.x + self.y * other.y +  self.z * other.z

    def cross (self, other: "Vector3") -> "Vector3":
        if not isinstance(other, Vector3):
            raise TypeError(f"unsupported operand type(s) for cross(): 'Vector3' and '{type(other).__name__}'")
        return Vector3(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x)