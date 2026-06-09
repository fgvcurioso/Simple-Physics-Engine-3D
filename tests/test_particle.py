import pytest
from core.particle import Particle
from physics_math.vector3 import Vector3
# Construction
def test_construction_trivial():
    p = Particle(position=Vector3(), mass=1)

    assert p.is_static == False
    assert p.velocity == Vector3()
    assert p.force_accumulator == Vector3()

    assert p == Particle(position=Vector3(),
     mass=1,velocity=Vector3(), 
     force_accumulator=Vector3(), 
     is_static=False)

def test_construction_negative_mass():
    with pytest.raises(ValueError):
        p = Particle(position=Vector3(), mass=-10)

def test_construction_cero_mass():
    with pytest.raises(ValueError):
        p = Particle(position=Vector3(), mass=0)

def test_construction_wrong_velocity_type():
    with pytest.raises(TypeError):
        p = Particle(position=5, mass=1)

def test_construction_wrong_mass_type():
    with pytest.raises(TypeError) as exc:
        p = Particle(position=Vector3(), mass="popo")
    assert "mass" in str(exc.value)

# Applied force

def test_apply_force_trivial():
    p = Particle(position=Vector3(), mass=1)
    assert p.force_accumulator == Vector3()

def test_apply_force_single():
    p = Particle(position=Vector3(0, 0, 0), mass=11.0)
    force=Vector3(1,1,1)
    p.apply_force(force)
    assert p.force_accumulator == force

def test_apply_force_accumulation():
    p = Particle(position=Vector3(0, 0, 0), mass=11.0)
    force_1 = Vector3(1,2,3)
    force_2 = Vector3(-1,-2,-3)
    force_3 = Vector3(-12, 3.0, 45)

    p.apply_force(force_1)
    p.apply_force(force_2)

    expected_force = force_1 + force_2
    assert p.force_accumulator == expected_force
    assert p.force_accumulator == Vector3()

    p.apply_force(force_3)
    expected_force =  expected_force + force_3
    assert p.force_accumulator == expected_force 

def test_apply_force_wrong_type():
    p = Particle(position=Vector3(0, 0, 0), mass=11.0)
    with pytest.raises(TypeError) as err:
        p.apply_force(5)
    assert "Vector3" in str(err.value)

# Clear forces
    
def test_clear_forces_trivial():
    p = Particle(position=Vector3(), mass=1)
    force = Vector3(1,2,3)
    p.apply_force(force)
    assert p.force_accumulator != Vector3()
    p.clear_forces()

    assert p.force_accumulator == Vector3()

def test_clear_forces_persistence():
    initial_position = Vector3(1,2,3)
    mass_p = 12
    initial_velocity = Vector3(5,5,0)
    p = Particle(position= initial_position,mass= mass_p,velocity=initial_velocity, force_accumulator= Vector3(1,1,1))

    force = Vector3(1,-4,10)
    p.apply_force(force)
    p.clear_forces()

    assert p.force_accumulator == Vector3()
    assert p.position == initial_position
    assert p.velocity == initial_velocity
    assert p.mass == mass_p
    assert p.is_static == False

def test_clear_forces_idempotency():
    initial_position = Vector3(1,2,3)
    mass_p = 12
    initial_velocity = Vector3(5,5,0)
    p = Particle(position= initial_position,mass= mass_p,velocity=initial_velocity, force_accumulator= Vector3(1,1,1))
    p.clear_forces()
    p.clear_forces()
    assert p.force_accumulator == Vector3()

def test_clear_forces_between_steps():
    p = Particle(position=Vector3(), mass=1)
    force_1 = Vector3(1,2,3)
    p.apply_force(force_1)
    p.clear_forces()

    force_2 = Vector3(-10,5,6)
    p.apply_force(force_2)
    assert p.force_accumulator == Vector3(-10,5,6)

# Integrate

def test_integrate_no_force():
    p = Particle(position=Vector3(), mass=1)
    force = Vector3()
    for step in range(3):
        p.apply_force(force)
        p.integrate(dt=1)
    assert p.position == Vector3()
    assert p.velocity == Vector3()
    assert p.force_accumulator == Vector3()

def test_integrate_single_impulse_coasts():
    p = Particle(position=Vector3(), mass=1)
    force = Vector3(1,0,0)
    p.apply_force(force)
    for step in range(3):
        p.integrate(dt=1)
    assert p.position == Vector3(3,0,0)
    assert p.velocity == Vector3(1 ,0,0)
    assert p.force_accumulator == Vector3()

def test_integrate_static_particle():
    p = Particle(Vector3(),
        mass=10000,
        velocity=Vector3(),
        force_accumulator=Vector3(),
        is_static= True)
    force = Vector3(100,500,500)
    p.apply_force(force)

    assert p.position == Vector3()
    assert p.mass == 10000
    assert p.velocity == Vector3()

def test_integrate_wrong_type():
    p = Particle(position=Vector3(), mass=1)
    
    with pytest.raises(TypeError) as err:
        p.integrate(Vector3())
    assert "step" in str(err.value)

def test_integrate_negative_step():
    p = Particle(position=Vector3(), mass=1)
    force = Vector3(1,0,0)
    p.apply_force(force)
    with pytest.raises(ValueError) as err:
        p.integrate(dt=-1)
    assert "negative" in str(err.value)

def test_integrate_mass_influence():
    p_low_mass = Particle(position=Vector3(), mass=1)
    p_high_mass = Particle(position=Vector3(), mass=100)

    force = Vector3(10,0,0)

    p_high_mass.apply_force(force)
    p_low_mass.apply_force(force)

    p_high_mass.integrate(dt=1)
    p_low_mass.integrate(dt=1)

    assert p_high_mass.velocity.magnitude() < p_low_mass.velocity.magnitude()

def test_integrate_gravity():
    p = Particle(position=Vector3(0, 100, 0), mass=1.0)
    gravity = Vector3(0, -9.8, 0)
    dt = 0.1

    for _ in range(10):
        p.apply_force(gravity)
        p.integrate(dt)

    assert p.position.y < 100  # fell downward
    assert p.velocity.y < 0    # moving downward

    
