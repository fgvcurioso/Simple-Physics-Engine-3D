from shapes.sphere import Sphere
import pytest
import math

# construction
def test_sphere_basic():
    sp = Sphere(radius=1.5)
    assert sp.radius == 1.5

def test_sphere_radius_less_or_equal_to_cero():
    with pytest.raises(ValueError) as err:
        Sphere(radius=0)
    assert "bigger" in str(err.value)
    
    with pytest.raises(ValueError) as err:
        Sphere(radius=-7.2)
    assert "bigger" in str(err.value)


def test_sphere_wrong_type():
    with pytest.raises(TypeError) as err:
        sp = Sphere(radius="1.5")
    assert "radius" in str(err.value)

def test_sphere_volume():
    r =  2.0
    sp = Sphere(radius=r)
    expected_v = (4/3) * math.pi * (r**3)
    assert math.isclose(expected_v, sp.volume())

def test_sphere_extreme_scaling():
    assert Sphere(radius=1e-10).radius == 1e-10
    assert Sphere(radius=1e10).radius == 1e10

def test_sphere_equality():
    sp1 = Sphere(radius=0.1 + 0.2)
    sp2 = Sphere(radius=0.3)
    assert sp1 == sp2

def test_sphere_immutable():
    sp = Sphere(radius=1.0)
    with pytest.raises(Exception):
        sp.radius = 2.0


