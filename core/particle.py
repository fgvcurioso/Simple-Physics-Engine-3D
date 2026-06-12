from dataclasses import dataclass, field, replace
from physics_math.vector3 import Vector3

@dataclass
class Particle:
    position: Vector3          # required
    mass: float                # required
    velocity: Vector3 = field(default_factory=Vector3)          # defaults to (0,0,0)
    force_accumulator: Vector3 = field(default_factory=Vector3) # defaults to (0,0,0)
    is_static: bool = False


    def __post_init__(self):
        if not isinstance(self.mass, (int, float)):
            raise TypeError(f"mass must be a float, got {type(self.mass).__name__}")
        if self.mass <= 0 :
            raise ValueError(f" mass value: {self.mass} must be: > 0")
        if not isinstance(self.position, Vector3):
            raise TypeError(f"position must be a Vector3, got {type(self.position).__name__}")

    def apply_force(self, new_force : Vector3) -> None:
        if not isinstance(new_force, Vector3):
            raise TypeError(f" applied force should be a vector (Vector3) we received a {type(new_force).__name__}")
        self.force_accumulator = self.force_accumulator + new_force

    def clear_forces(self) -> None:
        self.force_accumulator = Vector3()

    def integrate(self, dt: float | int) -> None:
        if self.is_static:
            return
        if not isinstance(dt, float | int):
            raise TypeError(f"step/time-interval must be a float, got {type(dt).__name__}")
        if dt < 0 :
            raise ValueError(f" step value: {dt} can not be negative")
        
        acceleration = self.force_accumulator * (1/self.mass)
        self.velocity = self.velocity + acceleration * dt 
        self.position = self.position + self.velocity * dt 
        self.clear_forces()
        
        