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

## Verify

# Equality

# Multiplication with a vector

# Multiplication with another matrix

# Determinant

# Inverse
