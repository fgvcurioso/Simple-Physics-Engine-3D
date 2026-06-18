from dataclasses import dataclass
from physics_math.vector3 import Vector3
import math

@dataclass(frozen=True)
class Plane:
    normal: Vector3
    offset: float

    def __post_init__(self):
        if not isinstance(self.normal,Vector3):
            raise TypeError(f"The normal should be a Vector3 instead we got{type(self.normal).__name__}")
        if not isinstance(self.offset,float | int):
            raise TypeError(f"The offset should be a float instead we got{type(self.offset).__name__}")

        n_magnitude = self.normal.magnitude()
        if  not math.isclose(n_magnitude, 1.0, abs_tol=1e-9):
            raise ValueError(f"Failed unit normal validation, normal magnitude = {n_magnitude}")

    def distance_to_point(self, point: Vector3) -> float:
        """
        Returns the signed distance from the plane to a point.
        Positive: The point is in front of the plane (direction of the normal).
        Zero: The point is exactly on the plane.
        Negative: The point is behind the plane.
        """
        if not isinstance(point, Vector3):
            raise TypeError(f"Point must be a Vector3 instead we got{type(point).__name__}")
        return self.normal.dot(point) - self.offset