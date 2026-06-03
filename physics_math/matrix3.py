from physics_math.vector3 import Vector3
from dataclasses import dataclass, field

@dataclass
class Matrix3:
    row0: "Vector3" = field(default_factory=lambda : Vector3(1, 0, 0))
    row1: "Vector3" = field(default_factory=lambda : Vector3(0, 1, 0))
    row2: "Vector3" = field(default_factory=lambda : Vector3(0, 0, 1))

    def __post_init__(self):
        for name, value in [("row0", self.row0), ("row1", self.row1), ("row2", self.row2)]:
            if not isinstance(value, Vector3):
                raise TypeError(f"{name} must be a Vector3, got {type(value).__name__}")