from physics_math.vector3 import Vector3
from physics_math.matrix3 import Matrix3
import pytest
import math

# Construction
def test_construction_default():
    m = Matrix3()
    assert m == Matrix3(Vector3(1,0,0), Vector3(0,1,0), Vector3(0,0,1))


## Verify matrix initialization  using both positional and keyword arguments.
def test_construction_custom_rows():
    v0 = Vector3(1, 2, 3)
    v1 = Vector3(3, -4.0, -10/2)
    v2 = Vector3(-6, 7, 16/1)

    m1 = Matrix3(v0,v1,v2)
    assert v0 == m1.row0
    assert v1 == m1.row1
    assert v2 == m1.row2

    m2 = Matrix3(row1=v1, row2=v2, row0=v0)
    assert m2.row0 == v0
    assert m2.row1 == v1
    assert m2.row2 == v2
## Verify that overriding only one/two row keeps the other/others as identity defaults.
def test_construction_partial_override():
    v0 = Vector3(1, 2, 3)
    v1 = Vector3(3, -4.0, -10/2)
    m1 = Matrix3(v0,v1)
    assert v0 == m1.row0
    assert v1 == m1.row1
    assert Vector3(0, 0, 1)== m1.row2


def test_construction_wrong_type():
    v0 = Vector3(1, 2, 3)
    v1 = Vector3(3, -4.0, -10/2)
    with pytest.raises(TypeError) as exc:
        Matrix3(v0, v1, 5)
    assert "row2" in str(exc.value)
    assert "Vector3" in str(exc.value)
    assert "int" in str(exc.value)

# Equality
def test_equality_trivial():
    assert Matrix3(Vector3(1,0,0), Vector3(0,1,0), Vector3(0,0,1)) ==Matrix3()


    assert Matrix3(Vector3(1,0,0), Vector3(0,1,0), Vector3(0,0.001,1)) != Matrix3()
    assert Matrix3(Vector3(1.1,0,0), Vector3(0,1,0), Vector3(0,0,1)) != Matrix3()
    assert Matrix3(Vector3(1,0,0), Vector3(0,1,0), Vector3(0,0,9999999)) != Matrix3()

    m1 = Matrix3(Vector3(1, 2, 3), Vector3(4, 5, 6), Vector3(7, 8, 9))
    m2 = Matrix3(Vector3(1, 2, 3), Vector3(4, 5, 6), Vector3(7, 8, 9))
    assert m1 == m2

def test_equality_wrong_type():
    v = Vector3(0,0,0)
    assert Matrix3(v,v,v) != 0
    assert Matrix3(v,v,v) != [0,0,0]

def test_equality_float_tolerance():
    row_a = Vector3(1.0, 0.2 + 0.1, 5)
    row_b = Vector3(1.0, 0.3, 5)
    assert Matrix3(row_a) == Matrix3(row_b)

# Multiplication with a vector

# Multiplication with another matrix

# Determinant

# Inverse
