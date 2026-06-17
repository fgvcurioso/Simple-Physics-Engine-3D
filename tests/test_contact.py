import pytest
from collision.contact import Contact
from core.rigidbody import RigidBody
from core.particle import Particle
from physics_math.vector3 import Vector3
from physics_math.matrix3 import Matrix3


# Fixtures
@pytest.fixture
def body1():
    return RigidBody(Particle(Vector3(0,0,0), 1), Matrix3())
@pytest.fixture
def body2():
    return RigidBody(Particle(Vector3(1,0,0), 1), Matrix3())

def test_contact_basic(body1, body2):
    point = Vector3(0.5, 0, 0)
    normal = Vector3(1, 0, 0)
    depth = 0.1

    contact = Contact(body1, body2, point, normal, depth)
    assert contact.body_a == body1
    assert contact.body_b == body2
    assert contact.point == point
    assert contact.normal == normal
    assert contact.penetration_depth == depth

def test_contact_self_collision(body1):
    point = Vector3(0.5, 0, 0)
    normal = Vector3(1, 0, 0)
    depth = 0.1
    with pytest.raises(ValueError) as err:
        Contact(body1, body1, point, normal, depth)
    assert "Reference should be differents" in str(err.value)

def test_contact_non_unit_normal(body1, body2):
    # normal magnitude more than 1
    with pytest.raises(ValueError) as err:
        Contact(body_a=body1,
        body_b=body2,
        point=Vector3(),
        normal=Vector3(2, 0, 0),
        penetration_depth=0.1)

    assert "unit normal validation" in str(err.value)
     # normal magnitude equal 0
    with pytest.raises(ValueError):
        Contact(body_a= body1,
        body_b= body2,
        point= Vector3(),
        normal= Vector3(0, 0, 0),
        penetration_depth= 0.1)

def test_contact_negative_penetration(body1, body2):
    with pytest.raises(ValueError) as err:
        Contact(body_a=body1,
        body_b= body2,
        point= Vector3(),
        normal= Vector3(1, 0, 0),
        penetration_depth= -0.5)
    assert "major than zero" in str(err.value)

    # Zero depth should be allow
    try:
        Contact(body_a=body1,
        body_b= body2,
        point= Vector3(),
        normal= Vector3(1, 0, 0),
        penetration_depth= 0.0)
    except ValueError:
        pytest.fail("Zero penetration depth should be valid")

def test_contact_wrong_types(body1, body2):
    with pytest.raises(TypeError) as err:
        Contact("not a body", body2, Vector3(), Vector3(1,0,0), 0.1)
    assert "Reference" in str(err.value)
    with pytest.raises(TypeError) as err:
        Contact(body1, body2, (0,0,0), Vector3(1,0,0), 0.1)
    assert "point should be a Vector3" in str(err.value)
    with pytest.raises(TypeError) as err:
        Contact(body1, body2, Vector3(), (1,2,3), 0.1)
    assert "normal should be a Vector3" in str(err.value)
    with pytest.raises(TypeError) as err:
        Contact(body1, body2, Vector3(), Vector3(1,0,0), Vector3())
    assert "penetration_depth should be a float" in str(err.value)

def test_contact_different_bodies_same_position(body1):
    body3 = RigidBody(Particle(Vector3(0,0,0), 1), Matrix3())  # same position as body1
    contact = Contact(body1, body3, Vector3(), Vector3(1,0,0), 0.1)
    assert contact.body_a is not contact.body_b