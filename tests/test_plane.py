import pytest
from shapes.plane import Plane
from physics_math.vector3 import Vector3


def test_plane_construction_basic():
    d = 0
    n = Vector3(0,1,0)
    p = Plane(normal=n, offset=d)
    assert n == p.normal
    assert d == p.offset

    d = -23
    n = Vector3(0,1,0)
    p = Plane(normal=n, offset=d)
    assert n == p.normal
    assert d == p.offset

    d = 0.7
    n = Vector3(0,1,0)
    p = Plane(normal=n, offset=d)
    assert n == p.normal
    assert d == p.offset

def test_plane_construction_normalized_vector():
    n_v = Vector3(1,2,3).normalize()
    p = Plane(normal=n_v, offset= 5)
    assert n_v == p.normal

def test_plane_construction_bad_normal():
    d = 0
    n = Vector3(1,0,1)
    with pytest.raises(ValueError) as err:
        Plane(normal= n, offset=d)
    assert "Failed unit normal validation" in str(err.value)

def test_plane_construction_wrong_types():

    with pytest.raises(TypeError) as err:
        Plane(normal= (1,2,3), offset=5)
    assert "The normal should be a Vector3" in str(err.value)

    with pytest.raises(TypeError) as err:
        Plane(normal= Vector3(1,0,0), offset={2})
    assert "The offset should be a float" in str(err.value)

def test_plane_distance_to_point_on_the_plane():
    n = Vector3(0,1,0)
    d = 5
    p = Vector3(1,5,-20)
    plane = Plane(normal=n, offset=d)
    assert plane.distance_to_point(point=p) == 0

def test_plane_distance_to_point_in_front():
    n = Vector3(0,1,0)
    d = 5
    p = Vector3(1,10,-20)
    plane = Plane(normal=n, offset=d)
    assert plane.distance_to_point(point=p) > 0

def test_plane_distance_to_point_behind():
    n = Vector3(0,1,0)
    d = 5
    p = Vector3(1,3,-20)
    plane = Plane(normal=n, offset=d)
    assert plane.distance_to_point(point=p) < 0

def test_plane_distance_to_point_wrong_type():
    n = Vector3(0,1,0)
    d = 5
    p = (1,5,-20)
    plane = Plane(normal=n, offset=d)
    with pytest.raises(TypeError) as err:
        plane.distance_to_point(point=p) == 0
    assert "Point must be a Vector3" in str(err.value)


