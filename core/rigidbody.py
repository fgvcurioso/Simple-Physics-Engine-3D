from dataclasses import dataclass, field, replace
from core.particle import Particle
from physics_math.vector3 import Vector3
from physics_math.matrix3 import Matrix3


@dataclass
class RigidBody:
    particle: Particle                    # required — linear dynamics
    inertia_tensor: Matrix3               # required — rotational resistance
    orientation: Matrix3 = field(default_factory=Matrix3)
    angular_velocity: Vector3 = field(default_factory=Vector3)
    torque_accumulator: Vector3 = field(default_factory=Vector3)

    inverse_inertia_tensor: Matrix3 = field(init=False)

    def __post_init__(self):
        if not isinstance(self.particle, Particle):
            raise TypeError(f"particle must be a Particle, got {type(self.particle).__name__}")
        if not isinstance(self.inertia_tensor, Matrix3):
            raise TypeError(f"inertia_tensor must be a Matrix3, got {type(self.inertia_tensor).__name__}")
        if not isinstance(self.orientation, Matrix3):
            raise TypeError(f"orientation must be a Matrix3, got {type(self.orientation).__name__}")
        if not isinstance(self.angular_velocity, Vector3):
            raise TypeError(f"angular_velocity must be a Vector3, got {type(self.angular_velocity).__name__}")
        if not isinstance(self.torque_accumulator, Vector3):
            raise TypeError(f"torque_accumulator must be a Vector3, got {type(self.torque_accumulator).__name__}")

        det = self.inertia_tensor.determinant()
        if abs(det) < 1e-9:
            raise ValueError("Inertia tensor must be invertible (determinant cannot be zero).")
        self.inverse_inertia_tensor = self.inertia_tensor.inverse()

    def apply_torque(self, torque: Vector3) -> None:
        if not isinstance(torque, Vector3):
            raise TypeError(f"New torque must be a Vector3, got {type(torque).__name__}")
        self.torque_accumulator = self.torque_accumulator + torque 
        
    def clear_torques(self)->None:
        self.torque_accumulator = Vector3()

    def apply_force_at_point(self, force: Vector3, point: Vector3) -> None:
        if not isinstance(force, Vector3):
            raise TypeError(f"Force must be a Vector3, got {type(force).__name__}")
        if not isinstance(point, Vector3):
            raise TypeError(f"Point must be a Vector3, got {type(point).__name__}")
        if self.particle.is_static == True:
            return
        self.particle.apply_force(force)
        lever_arm = point - self.particle.position
        self.torque_accumulator = self.torque_accumulator + lever_arm.cross(force)

    def integrate(self, dt: int | float) -> None:
        if self.particle.is_static:
            return
        if not isinstance(dt, float | int):
            raise TypeError(f"step/time-interval must be a float, got {type(dt).__name__}")
        if dt < 0 :
            raise ValueError(f" step value: {dt} can not be negative")

        self.particle.integrate(dt)

        angular_acceleration = self.inverse_inertia_tensor.transform(self.torque_accumulator)
        self.angular_velocity = self.angular_velocity + angular_acceleration * dt
        
        skew = Matrix3.skew_symmetric(self.angular_velocity)
        self.orientation = self.orientation + (skew * self.orientation) * dt

        self.clear_torques()