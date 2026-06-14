import pytest
from core.particle import Particle
from physics_math.vector3 import Vector3
from physics_math.matrix3 import Matrix3
from core.rigidbody import RigidBody

# Fixtures
@pytest.fixture
def rb():
    p = Particle(Vector3(), 1.0)
    inertia = Matrix3(Vector3(2,0,0), Vector3(0,2,0), Vector3(0,0,2))
    return RigidBody(particle=p, inertia_tensor=inertia)
@pytest.fixture
def rb_1():
    initial_position = Vector3(1,2,3)
    mass_p = 12
    initial_velocity = Vector3(5,5,0)
    p = Particle(position= initial_position,
    mass= mass_p,
    velocity=initial_velocity,
    force_accumulator= Vector3(1,1,1))

    inertia = Matrix3(Vector3(2,0,0), Vector3(0,2,0), Vector3(0,0,2))
    orientation=Matrix3(Vector3(1,2,3), Vector3(2,3,4), Vector3(5,3,2))
    w = Vector3(1,1,1)
    return RigidBody(particle=p,
     inertia_tensor= inertia,
      orientation=orientation,
      angular_velocity=w,
      torque_accumulator=Vector3(),
      )



# Construction
def test_construction_basic(rb):

    assert rb.particle.position == Vector3()
    assert rb.particle.mass == 1
    assert rb.particle.force_accumulator == Vector3()
    assert rb.particle.velocity == Vector3()

    assert rb.inertia_tensor == Matrix3(Vector3(2,0,0), Vector3(0,2,0), Vector3(0,0,2))
    assert rb.angular_velocity == Vector3()
    assert rb.torque_accumulator == Vector3()
    assert rb.orientation == Matrix3()

    assert rb.inverse_inertia_tensor == rb.inertia_tensor.inverse()

def test_construction_wrong_type():
    with pytest.raises(TypeError) as err:
        rb = RigidBody(particle=Vector3(),inertia_tensor=Matrix3(Vector3(1,1,1)))
    assert "Particle" in str(err.value)

    p = Particle(position=Vector3(), mass=1)
    with pytest.raises(TypeError) as err:
        rb = RigidBody(particle=p,inertia_tensor=Vector3(1,1,1))
    assert "inertia_tensor" in str(err.value)

    with pytest.raises(TypeError) as err:
        rb = RigidBody(particle=p,inertia_tensor=Matrix3(Vector3(1,1,1)), orientation=Vector3())
    assert "orientation" in str(err.value)

    with pytest.raises(TypeError) as err:
        rb = RigidBody(particle=p,inertia_tensor=Matrix3(Vector3(1,1,1)), angular_velocity=5)
    assert "angular_velocity" in str(err.value)

    with pytest.raises(TypeError) as err:
        rb = RigidBody(particle=p,inertia_tensor=Matrix3(Vector3(1,1,1)),torque_accumulator=7)
    assert "torque_accumulator" in str(err.value)

def test_construction_non_invertible_inertia():
    p = Particle(Vector3(), 1.0)
    # A matrix of all zeros has determinant 0
    zero_matrix = Matrix3(Vector3(0,0,0), Vector3(0,0,0), Vector3(0,0,0))

    with pytest.raises(ValueError) as err:
        RigidBody(particle=p, inertia_tensor=zero_matrix)
    assert "invertible" in str(err.value)

def test_inverse_inertia_calculation(rb):
    expected_inv = Matrix3(Vector3(0.5,0,0), Vector3(0,0.5,0), Vector3(0,0,0.5))
    assert rb.inverse_inertia_tensor == expected_inv

# Apply Torque

def test_apply_torque_basic(rb):
    assert rb.torque_accumulator == Vector3()
    rb.apply_torque(Vector3())
    assert rb.torque_accumulator == Vector3()
    torque = Vector3(1,2,3)
    rb.apply_torque(torque)
    assert rb.torque_accumulator == torque

def test_apply_torque_multiple_calls(rb):

    torque_1 = Vector3(1,2,3)
    torque_2 = Vector3(0,-1,-2)
    torque_3 = Vector3(5,6,7)

    rb.apply_torque(torque_1)
    rb.apply_torque(torque_2)
    rb.apply_torque(torque_3)
    
    assert rb.torque_accumulator == torque_1 + torque_2 + torque_3

def test_apply_torque_wrong_type(rb):

    with pytest.raises(TypeError) as err:
        rb.apply_torque(-10)
    assert "torque" in str(err.value)

# Clear torques
def test_clear_torque_basic(rb):
    torque_1 = Vector3(1,2,3)
    rb.apply_torque(torque_1)
    rb.clear_torques()
    assert rb.torque_accumulator == Vector3()

def test_clear_torque_multiple_apply(rb):
    torque_1 = Vector3(1,2,3)
    torque_2 = Vector3(0,-1,-2)
    torque_3 = Vector3(5,6,7)

    rb.apply_torque(torque_1)
    rb.apply_torque(torque_2)
    rb.apply_torque(torque_3)
    rb.clear_torques()
    assert rb.torque_accumulator == Vector3()

def test_clear_torque__persistence(rb_1):
    torque_1 = Vector3(1,2,3)
    rb_1.apply_torque(torque_1)
    rb_1.clear_torques()

    assert rb_1.angular_velocity == Vector3(1,1,1)
    assert rb_1.inertia_tensor == Matrix3(Vector3(2,0,0), Vector3(0,2,0), Vector3(0,0,2))
    assert rb_1.orientation == Matrix3(Vector3(1,2,3), Vector3(2,3,4), Vector3(5,3,2))

def test_clear_torque_idempotency(rb):
    torque_1 = Vector3(1,2,3)
    rb.apply_torque(Vector3(1,1,1))
    rb.clear_torques()
    rb.clear_torques()
    assert rb.torque_accumulator == Vector3()

def test_clear_torque_isolation_from_particle(rb):
    linear_force = Vector3(10, 0, 0)
    angular_torque = Vector3(0, 10, 0)

    rb.particle.apply_force(linear_force)
    rb.apply_torque(angular_torque)

    assert rb.particle.force_accumulator == linear_force
    assert rb.torque_accumulator == angular_torque

    rb.clear_torques()

    assert rb.torque_accumulator == Vector3(0, 0, 0)
    assert rb.particle.force_accumulator == linear_force

# Apply force to a point
def test_apply_force_at_point_static(rb):
    force = Vector3(0, 230, 0)
    point = Vector3(2, 0, 0)
    rb.particle.is_static = True
    rb.apply_force_at_point(force, point)
    

    assert rb.particle.force_accumulator == Vector3()
    assert rb.torque_accumulator == Vector3()


def test_apply_force_at_point_basic(rb):
    force = Vector3(0, 10, 0)
    point = Vector3(2, 0, 0)
    rb.apply_force_at_point(force, point)

    assert rb.particle.force_accumulator == Vector3(0, 10, 0)
    assert rb.torque_accumulator == Vector3(0, 0, 20)


def test_apply_force_at_center_of_mass(rb):
    force = Vector3(1,0,0)
    point = rb.particle.position

    rb.apply_force_at_point(force=force, point= point)

    assert rb.particle.force_accumulator == force
    assert rb.torque_accumulator == Vector3()

def test_apply_force_off_center_parallel_to_force(rb):
    force = Vector3(1,2,3)
    point = Vector3(2,4,6)
    rb.apply_force_at_point(force=force, point= point)
    assert rb.particle.force_accumulator == force
    assert rb.torque_accumulator == Vector3()

def test_apply_force_off_center_perpendicular_to_force(rb):
    force = Vector3(0,1,0)
    point = Vector3(1,0,0)
    rb.apply_force_at_point(force=force, point= point)
    assert rb.particle.force_accumulator != Vector3()
    assert rb.torque_accumulator != Vector3()

def test_apply_force_couple(rb):
    point_1 = Vector3(1,0,0)
    point_2 = Vector3(-1,0,0)
    force_1 = Vector3(0,10,0)
    force_2 = Vector3(0,-10,0)

    rb.apply_force_at_point(force=force_1, point=point_1)
    rb.apply_force_at_point(force=force_2, point=point_2)

    assert rb.particle.force_accumulator == Vector3()
    assert rb.torque_accumulator == Vector3(0, 0, 20)

def test_apply_force_at_point_wrong_types(rb):
    with pytest.raises(TypeError) as err:
        rb.apply_force_at_point(force=1, point=Vector3())
    assert "Force" in str(err.value)

    with pytest.raises(TypeError) as err:
        rb.apply_force_at_point(force=Vector3(3,2,1), point=(6,5))
    assert "Point" in str(err.value)


def test_apply_force_at_point_moved_body(rb_1):
    force = Vector3(0, 10, 0)
    point = Vector3(2, 2, 3)
    rb_1.apply_force_at_point(force, point)

    assert rb_1.torque_accumulator == Vector3(0, 0, 10)

# Integrate
def test_integrate_static_body(rb):
    rb.particle.is_static = True

    pos_init = rb.particle.position
    v_init = rb.particle.velocity
    acc_force_init = rb.particle.force_accumulator

    inertia_tensor_init = rb.inertia_tensor
    orientation_init = rb.orientation
    torque_accumulator_init = rb.torque_accumulator

    for i in range(6):
        rb.apply_force_at_point(force= Vector3(1,2,2), point= Vector3())
        rb.integrate(i)
        assert pos_init == rb.particle.position
        assert v_init == rb.particle.velocity
        assert acc_force_init == rb.particle.force_accumulator
        assert orientation_init == rb.orientation
        assert torque_accumulator_init == rb.torque_accumulator
        assert inertia_tensor_init == rb.inertia_tensor


def test_integrate_no_torque_no_w(rb):
    for i in range(3):
        rb.integrate(i)
        assert Matrix3() == rb.orientation

def test_integrate_no_torque_preserves_angular_velocity(rb):
    rb.angular_velocity = Vector3(1, 0, 0)  
    for _ in range(5):
        rb.integrate(dt=0.1)               
    assert rb.angular_velocity == Vector3(1, 0, 0)

def test_integrate_constant_torque(rb):
    force = Vector3(0, 10, 0)
    point = Vector3(2, 0, 0)
    w = Vector3()
    w_m = w.magnitude()
    dt = 1
    for _ in range(3):
        rb.apply_force_at_point(force, point)
        rb.integrate(dt)
        w_m_c = rb.angular_velocity.magnitude()
        assert w_m_c > w_m 
        w_m = w_m_c

def test_integrate_torque_cleared_after_integration(rb):
    force = Vector3(0, 10, 0)
    point = Vector3(2, 0, 0)
    for _ in range(3):
        rb.apply_force_at_point(force, point)

    assert rb.torque_accumulator == Vector3(0,0,60)
    rb.integrate(1)
    assert rb.torque_accumulator == Vector3()