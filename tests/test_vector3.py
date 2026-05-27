
from physics_math.vector3 import Vector3
import pytest
import math
# Testing construction 
def test_construction_trivial():
    v = Vector3(19,0.001,-112334)
    assert v.x ==19 
    assert v.y ==0.001 
    assert v.z ==-112334 

def test_construction_trivial_default_params():
    v = Vector3()
    assert v.x ==0.0 
    assert v.y ==0.0 
    assert v.z ==0.0 

# Testing overloaded == operation 

def test_equality_trivial():
    v1 = Vector3(1.0,2.0,3.0)
    v2 = Vector3(-1+2, 4/2, 3+0)
    assert v1 == v2 
    assert v1 == Vector3(1,2,3) 

def test_exact_float_equality():
    assert Vector3(0.1+0.3,-1,0) == Vector3(0.4, -1, 0)
    assert Vector3(0.1 + 0.2, -1, 0) == Vector3(0.3, -1, 0)

def test_equality_false():
    assert Vector3(1,2,3) != Vector3(1,2,4)
    assert Vector3(1,2,3) != Vector3(2,2,3)
    assert Vector3(1,2,3) != Vector3(1,3,3)

def test_equality_different_type():
    assert Vector3(1, 0, 0).__eq__("not a vector") == NotImplemented
    assert Vector3(1, 0, 0).__eq__(42) == NotImplemented

#Testing overload (+) operator: __add__

def test_add_trivial():
    assert (Vector3(1,1,1) + Vector3(0,0,0)) == Vector3(1,1,1)
    v1 = Vector3(0.0, -5.0, 2.0)
    v2 = Vector3(-1, 7, 2)
    assert v2 + v1 ==  Vector3(-1.0, 2.0, 4)

def test_add_different_type():
    with pytest.raises(TypeError):
        Vector3(1, 2, 3) + 5
    with pytest.raises(TypeError):
        Vector3(1, 2, 3) + "(5, 6, 7)"

def test_add_commutative():
    v1 = Vector3(1, 2, 3)
    v2 = Vector3(4, 5, 6)
    assert v1 + v2 == v2 + v1

#Testing overload (-) operator: __sub__

def test_substraction_trivial():
    assert (Vector3(1,1,1) - Vector3(0,0,0)) == Vector3(1,1,1)
    v1 = Vector3(0.0, -5.0, 2.0)
    v2 = Vector3(-1, 7, 2)
    assert v2 - v1 ==  Vector3(-1.0, 12.0, 0)

def test_substraction_different_type():
    with pytest.raises(TypeError):
        Vector3(1, 2, 3) - 5
    with pytest.raises(TypeError):
        Vector3(1, 2, 3) - "(5, 6, 7)"

def test_substraction_non_commutative():
    v1 = Vector3(1, 2, 3)
    v2 = Vector3(-10.7, 5.9999999999999999, 6)
    assert v1 - v2 != v2 - v1


#Testing overload (*) operator: __mul__ : scalar-vector multiplication
def test_multiplication_trivial():
    v1 = Vector3(1, 2, -3)
    assert v1 * 0 == Vector3(0,0,0)
    assert v1 * 1 == v1
    assert v1 * (-10.5) == Vector3(-10.5, -21, 31.5)

    v2 = Vector3(0, 0, 0)
    assert v2 * 100.99 == Vector3(0, 0, 0)

def test_multiplication_wrong_type():
    with pytest.raises(TypeError):
        Vector3(1, 2, 3) * Vector3(5, 6, 7)


#Testing overload (*) operator: __rmul__ : scalar-vector multiplication
def test_r_multiplication_trivial():
    v1 = Vector3(1, 2, -3)
    assert 0 * v1 == Vector3(0,0,0)
    assert 1 * v1 == v1
    assert -10.5 * v1 == Vector3(-10.5, -21, 31.5)

    v2 = Vector3(0, 0, 0)
    assert 100.99 * v2 == Vector3(0, 0, 0)


# __mul__ and __rmul__ commutativity:
def test_multiplication_commutative():
    v1 = Vector3(1, 2, -3)
    assert 0.5 * v1== v1 * 0.5

# Testing overloaded (/) __truediv__ : scalar division
def test_division_trivial():
    v1 = Vector3(10, 5, -4)
    assert v1 / 1 == v1
    assert v1 / (-10) == Vector3(-1, -0.5, 0.4)

    v2 = Vector3(0, 0, 0)
    assert v2 / 100.99 == Vector3(0, 0, 0)

def test_division_by_cero():
    v1 = Vector3(10, 5, -4)
    with pytest.raises(ZeroDivisionError) as exc_info:
        _ = v1 / 0
    assert str(exc_info.value) == "division by zero: Cannot divide a Vector3 by scalar zero."

def test_division_by_near_zero():
    with pytest.raises(ZeroDivisionError):
        Vector3(1, 2, 3) / 1e-10

# Vectors magnitude calculation
def test_magnitude_trivial():
    v1= Vector3(1,-2.0,2)
    assert v1.magnitude() == 3

    v2 = Vector3(0,0,0) 
    assert v2.magnitude() == 0

def test_magnitude_negative_components():
    v = Vector3(-1, -2, -3)

    assert v.magnitude() > 0 

# Vector normalization
def test_normalization_basic():
    v1= Vector3(3,0,4)
    assert v1.normalize() == Vector3(0.6, 0, 0.8)

def test_normalization_cero_magnitude():
    v1 = Vector3(0,0,0)
    with pytest.raises(ZeroDivisionError):
         v1.normalize()

def test_normalization_negative_components():
    v = Vector3(-10,0,0)
    assert v.normalize() == Vector3(-1,0,0)

def test_normalization_magnitude_is_one():
    v1 = Vector3(3, 1, -7)
    assert v1.normalize().magnitude() == 1.0

# Dot product
def test_dot_product_basic():
    v1 = Vector3(1,1,1)
    v2 = Vector3(0,0,0)
    assert v1.dot(v2) == 0
 
def test_dot_product_commutative():
    v1 = Vector3(1,2,3)
    v2 = Vector3(-3,10.5,-8)
    assert v1.dot(v2) == v2.dot(v1)

def test_dot_product_wrong_type():
    with pytest.raises(TypeError):
        Vector3(1, 2, 3).dot(5)

def test_dot_product_orthogonal():
    v_x = Vector3(1,0,0)
    v_y = Vector3(0,1,0)
    v_z = Vector3(0,0,1)

    assert v_x.dot(v_y) == 0
    assert v_x.dot(v_z) == 0
    assert v_y.dot(v_z) == 0

def test_dot_product_with_self():
    v = Vector3(1,2,3)
    exp_sq_magnitude = 1**2 + 2**2 + 3**2
    assert exp_sq_magnitude == v.dot(v)
    assert math.isclose(v.dot(v), v.magnitude()**2, abs_tol=1e-9)

# Cross product

def test_cross_product_basic():
    v1 = Vector3(1, 3, -5)
    v2 = Vector3(4, -2, -1)
    assert v1.cross(v2)  == Vector3(-13, -19, -14)

    i = Vector3(1, 0, 0)
    j = Vector3(0, 1, 0)
    k = Vector3(0, 0, 1)

    assert i.cross(j) == k
    assert j.cross(k) == i
    assert k.cross(i) == j
    


def test_cross_product_colinear_parallel():
    v1 = Vector3(-1.3, 0.5, 100)
    assert v1.cross(v1) == Vector3(0, 0, 0)

    v2 = v1 * 2.45
    assert v1.cross(v2) == Vector3(0,0,0)

def test_cross_product_anti_commutative():
    v1 = Vector3(1, 3, -5)
    v2 = Vector3(4, -2, -1)
    assert v1.cross(v2) == -1 * v2.cross(v1)

def test_cross_product_wrong_type():
    v = Vector3(1, 3, -5)
    with pytest.raises(TypeError) :
        v.cross(12)

def test_cross_product_ortohogonality ():
    v1 = Vector3(1, 3, -5)
    v2 = Vector3(4, -2, -1)
    v3 = v1.cross(v2)

    assert v3.dot(v1) == 0 
    assert v3.dot(v2) == 0 
