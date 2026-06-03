from physics_math.vector3 import Vector3
from dataclasses import dataclass, field

@dataclass
class Matrix3:
    row0: "Vector3" = field(default_factory=lambda : Vector3(1, 0, 0))
    row1: "Vector3" = field(default_factory=lambda : Vector3(0, 1, 0))
    row2: "Vector3" = field(default_factory=lambda : Vector3(0, 0, 1))

