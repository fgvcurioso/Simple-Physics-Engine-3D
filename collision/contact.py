from dataclasses import dataclass
from core.rigidbody import RigidBody
from physics_math.vector3 import Vector3
import math


@dataclass
class Contact:
    body_a: RigidBody
    body_b: RigidBody
    point: Vector3
    normal: Vector3
    penetration_depth: float

    def __post_init__(self):
        
        if not isinstance(self.body_a, RigidBody):
            raise TypeError(f"Reference should be RigidBody, we got instead: {type(self.body_a).__name__}")
        if not isinstance(self.body_b, RigidBody):
            raise TypeError(f"Reference should be RigidBody, we got instead: {type(self.body_b).__name__}")
        if not isinstance(self.point, Vector3):
            raise TypeError(f"point should be a Vector3, we got instead: {type(self.point).__name__}")
        if not isinstance(self.normal, Vector3):
            raise TypeError(f"normal should be a Vector3, we got instead: {type(self.normal).__name__}")
        if not isinstance(self.penetration_depth, float | int ):
            raise TypeError(f"penetration_depth should be a float, we got instead: {type(self.penetration_depth).__name__}")
        if self.body_a is self.body_b:
            raise ValueError(f"Reference should be differents ({self.body_a}, {self.body_b})")

        n_magnitude = self.normal.magnitude()
        if  not math.isclose(n_magnitude, 1.0, abs_tol=1e-9):
            raise ValueError(f"Failed unit normal validation normal magnitude = {n_magnitude}")

        if self.penetration_depth < 0:
            raise ValueError(f"A valid collision have penetration depth equal or major than zero, we got: {self.penetration_depth}")

        