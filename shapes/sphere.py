from dataclasses import dataclass
import math

@dataclass(frozen=True,  unsafe_hash=True)
class Sphere:
    radius: float

    def __post_init__(self):
        if not isinstance(self.radius, (int, float)):
            raise TypeError(f"radius must be a float, got {type(self.radius).__name__}")
        
        if self.radius <= 0:
            raise ValueError("radius value need to be bigger than cero")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Sphere):
            return NotImplemented
        return math.isclose(self.radius, other.radius, abs_tol=1e-9)

    def volume(self):
        """Calculates and returns the volume of the sphere."""
        return (4 / 3) * math.pi * (self.radius**3)
