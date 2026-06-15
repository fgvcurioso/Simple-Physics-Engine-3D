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

# Addition
def test_addition_zero_matrix():
    M1 = Matrix3(Vector3(0,0,0), Vector3(0,0,0), Vector3(0,0,0))
    M2 = Matrix3(Vector3(1,-30,12), Vector3(0.9999,-23,223), Vector3(0,-5,0))

    assert M1 + M2 == M2
    assert M2 + M1 == M2

def test_addition_trivial():
    M1 = Matrix3(Vector3(4, 0, 34), Vector3(0.1,0,0), Vector3(-6, 0.9, 0))
    M2 = Matrix3(Vector3(1, -30, 12), Vector3(0.2,-23,223), Vector3(0, -5, 0))    
    assert M1 + M2 == M2 + M1
    assert  M1 + M2 == Matrix3(Vector3(5, -30, 46), Vector3(0.3, -23, 223), Vector3(-6, -4.1, 0) )

def test_addition_additive_inverse():
     M1 = Matrix3(Vector3(1, 2, 3), Vector3(4, 5, 6), Vector3(7, 8, 9))
     M2 = Matrix3(Vector3(-1, -2, -3), Vector3(-4, -5, -6), Vector3(-7, -8, -9))

     assert M1 + M2 ==  Matrix3(Vector3(0,0,0), Vector3(0,0,0), Vector3(0,0,0))

def test_addition_wrong_type():
    with pytest.raises(TypeError):
        Matrix3() + Vector3(1,2,3)

# Multiplication wrapping 
def test_multiplication_wrong_type():
    with pytest.raises(TypeError):
        Matrix3() * "8"

# Multiplication with scalar

def test_multiplication_scalar_trivial():
    m = Matrix3()
    assert m * 10 == 10 *m == Matrix3(Vector3(10,0,0), Vector3(0,10,0), Vector3(0,0,10))
    assert m * 1 == Matrix3()
    assert m * 0 == Matrix3(Vector3(0,0,0), Vector3(0,0,0), Vector3(0,0,0))



# Multiplication with a vector (Transform)
def test_transform_trivial():
    m1 = Matrix3(Vector3(0, 0, 0), Vector3(0, 0, 0), Vector3(0, 0, 0))
    v1 =Vector3(1,2,3)

    assert m1 * v1 == Vector3(0,0,0)

## The Identity Matrix Property: Ix = x
def test_transform_identity_matrix():
    assert Matrix3() * Vector3(1,2,3) == Vector3(1,2,3)

## Distributive over Vector Addition: A(x + y) = Ax + Ay
def test_transform_distributive():
    v1 = Vector3(1,2,3)
    v2 = Vector3(3,2,1)
    m1 = Matrix3()
    assert m1*(v1 + v2) == m1*v1 + m1*v2 

## Distributive over Matrix Addition (A + B)x = Ax + Bx
def test_transform_distributive_2():
    m1 = Matrix3(Vector3(1,2,3,), Vector3(0,-2,-1), Vector3(3,4, 1.23))
    m2 = Matrix3(Vector3(3,2,1), Vector3(12,-22,-451), Vector3(1,7, 1.23))
    v = Vector3(2,4,8)

    assert (m1 + m2)* v == m1*v + m2*v
# Multiplication between Matrix (compose)
def test_compose_trivial():
    m1 = Matrix3(Vector3(1,2,3), Vector3(0,1,4), Vector3(5,6,0))
    m2 = Matrix3(Vector3(2,0,-1), Vector3(1,3,2), Vector3(0,1,1))
   
    assert m1 * m2 == Matrix3(Vector3(4,9,6), Vector3(1,7,6), Vector3(16,18,7))

def test_compose_identity():
    m1 = Matrix3(Vector3(1,2,3), Vector3(0,1,4), Vector3(5,6,0))
    im = Matrix3()

    assert im * m1 == m1 
    assert m1 * im == m1
   
def test_compose_non_commutative():
    m1 = Matrix3(Vector3(1,2,3), Vector3(0,1,4), Vector3(5,6,0))
    m2 = Matrix3(Vector3(2,0,-1), Vector3(1,3,2), Vector3(0,1,1))

    assert m1 * m2 != m2 * m1

def test_compose_distributive():
    m1 = Matrix3(Vector3(1,2,3), Vector3(0,1,4), Vector3(5,6,0))
    m2 = Matrix3(Vector3(2,0,-1), Vector3(1,3,2), Vector3(0,1,1))
    m3 = Matrix3(Vector3(76,4,9), Vector3(3,32,2), Vector3(1,1,1))

    assert m1*(m2+m3) == m1*m2 + m1*m3 

# Transpose
## Double Transpose: (A^T)^T = A
def test_transpose_of_transpose():
    Original = Matrix3(Vector3(1,2,3), Vector3(-1,2,5), Vector3(-1, 0, 2))
    transpose_m = Original.transpose()
    transpose_double = transpose_m.transpose()

    assert Original == transpose_double

## Addition: (A + B)^T = A^T + B^T
def test_transpose_addition():
    m1 = Matrix3(Vector3(1,2,3), Vector3(-1,2,5), Vector3(-1, 0, 2))
    m2 = Matrix3(Vector3(1,-32,30), Vector3(-234,2,4), Vector3(-1, 23, 0))
    assert (m1+m2).transpose()  == m1.transpose() + m2.transpose()
## Multiplication: (AB)^T = B^T A^T
def test_transpose_multiplication():
    m1 = Matrix3(Vector3(1,2,3), Vector3(-1,2,5), Vector3(-1, 0, 2))
    m2 = Matrix3(Vector3(1,-32,30), Vector3(-234,2,4), Vector3(-1, 23, 0))

    assert (m1 * m2).transpose() == m2.transpose() * m1.transpose()

## Symmetric Matrices: A = A^T
def test_transpose_symmetric_matrix():
    m = Matrix3()
    assert  m == m.transpose()


# Determinant

def test_determinant_trivial():
    m = Matrix3(Vector3(1,2,3), Vector3(0,4,5), Vector3(1,0,6))

    assert m.determinant() == 22

def test_determinant_transpose():
    m = Matrix3(Vector3(1,2,3), Vector3(0,4,5), Vector3(1,0,6))
    m_t = m.transpose()
    assert m.determinant() == m_t.determinant() 

def test_determinant_row_swap():
    m1 = Matrix3(Vector3(1,2,3), Vector3(0,4,5), Vector3(1,0,6))
    m2 = Matrix3(Vector3(1,0,6), Vector3(0,4,5), Vector3(1,2,3))

    assert m1.determinant() == -1 * m2.determinant()

def test_determinant_zero_conditions():
    ## row/column of ceros
    m1 = Matrix3(Vector3(0,0,0), Vector3(0,4,5), Vector3(1,0,6))
    assert m1.determinant() == 0

    ## Identical rows
    m1 = Matrix3(Vector3(0,4,5), Vector3(0,4,5), Vector3(1,0,6))
    assert m1.determinant() == 0

    ## Linearly dependent
    m1 = Matrix3(Vector3(0,4,5), Vector3(0,8,10), Vector3(1,0,6))
    assert m1.determinant() == 0

def test_determinant_multplicative_property():
    m1 = Matrix3(Vector3(1,2,3), Vector3(-1,2,5), Vector3(-1, 0, 2))
    m2 = Matrix3(Vector3(1,-32,30), Vector3(-234,2,4), Vector3(-1, 23, 0))
    assert math.isclose(
    m1.determinant() * m2.determinant(),
    (m1 * m2).determinant(),
    rel_tol=1e-9
)

def test_determinant_scalar():
    m1 = Matrix3(Vector3(1,2,3), Vector3(-1,2,5), Vector3(-1, 0, 2))
    k = 5
    km1 = Matrix3(m1.row0 * k, m1.row1 * k, m1.row2 * k)
    assert math.isclose(km1.determinant(), k**3 * m1.determinant(), rel_tol=1e-9)

# Inverse

def test_inverse_trivial():
    m = Matrix3(Vector3(1,0,2), Vector3(2, -1, 3), Vector3(4, 1, 8))
    assert m.inverse() == Matrix3(Vector3(-11, 2, 2), Vector3(-4,0,1), Vector3(6,-1,-1))

def test_inverse_identity():
    m = Matrix3(Vector3(1,0,2), Vector3(2, -1, 3), Vector3(4, 1, 8))
    assert m * m.inverse() == Matrix3()
    assert m.inverse() * m == Matrix3()

def test_inverse_of_inverse():
    m = Matrix3(Vector3(1,0,2), Vector3(2, -1, 3), Vector3(4, 1, 8))
    assert m == (m.inverse()).inverse()

def test_inverse_reverse_order():
    m1 = Matrix3(Vector3(1,2,3), Vector3(-1,2,5), Vector3(-1, 0, 2))
    m2 = Matrix3(Vector3(1,-32,30), Vector3(-234,2,4), Vector3(-1, 23, 0))

    assert (m1*m2).inverse() == m2.inverse() * m1.inverse()

def test_inverse_transpose():
    m = Matrix3(Vector3(1,0,2), Vector3(2, -1, 3), Vector3(4, 1, 8))
    assert (m.inverse()).transpose() == (m.transpose()).inverse()

def test_inverse_determinant():
    m1 = Matrix3(Vector3(1,2,3), Vector3(-1,2,5), Vector3(-1, 0, 2))
    inv = m1.inverse()
    assert math.isclose(inv.determinant(), 1/m1.determinant(), rel_tol=1e-9)

def test_inverse_singular():
    m = Matrix3(Vector3(1,2,3), Vector3(2,4,6), Vector3(0,0,1))  # row1 = 2 * row0
    with pytest.raises(ValueError) as exc:
        m.inverse()
    assert "singular" in str(exc.value)

# Skew symmetric matrix generation

def test_skew_symmetric_basic():
    w = Vector3(1.0, 2.0, 3.0)
    v = Vector3(4.0, 5.0, 6.0)

    skew_mat = Matrix3.skew_symmetric(w)
    matrix_result = skew_mat.transform(v)
    cross_result = w.cross(v)

    assert matrix_result == cross_result

def test_skew_symmetric_wrong_type():
    with pytest.raises(TypeError) as err:
        Matrix3.skew_symmetric((5,6))
    assert "Vector3" in str(err.value)

def test_skew_symmetric_transpose_is_negation():
    m = Matrix3.skew_symmetric(Vector3(1, -2, 3))
    assert m.transpose() == m * -1

# ortho normalize
def test_orthonormalize_basic():
    m = Matrix3()
    assert m.orthonormalize() == m


def test_orthonormalize_sheared_matrix():
    m = Matrix3(Vector3(1.0, 0.1, 0.0), Vector3(0.0, 1.0, 0.0), Vector3(0.0, 0.0, 1.0))
    assert m.col0.dot(m.col1) != 0.0 
    result = m.orthonormalize()

    # All columns must be exactly 90 degrees apart (orthogonal).
    assert math.isclose(result.col0.dot(result.col1), 0.0, abs_tol=1e-9)
    assert math.isclose(result.col0.dot(result.col2), 0.0, abs_tol=1e-9)
    assert math.isclose(result.col1.dot(result.col2), 0.0, abs_tol=1e-9)

    # All columns must be normalized (length = 1.0)
    assert math.isclose(result.col0.magnitude(), 1.0, abs_tol=1e-9)
    assert math.isclose(result.col1.magnitude(), 1.0, abs_tol=1e-9)
    assert math.isclose(result.col2.magnitude(), 1.0, abs_tol=1e-9)
def test_orthonormalize_drift_correction():
   
    v0 = Vector3(5,0,0)
    v1 = Vector3(0,1,0)
    v2 = Vector3(0,0,20)
    m = Matrix3(v0,v1,v2)

    result = m.orthonormalize()
    expected = Matrix3(v0.normalize(), v1.normalize(), v2.normalize())
    assert result == expected
