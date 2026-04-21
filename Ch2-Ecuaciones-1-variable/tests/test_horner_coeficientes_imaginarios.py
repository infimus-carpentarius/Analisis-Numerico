import pytest
import cmath
import math
from decimal import Decimal
from fractions import Fraction
from ch2_ecuaciones.root_finding import horner_coeficientes_complejos

# ------------------------------------------------------------
# Funciones auxiliares de comparación
# ------------------------------------------------------------
def casi_igual(a, b, tol=1e-10):
    """Compara dos números complejos o reales con tolerancia."""
    return abs(a - b) < tol

def comparar_tuplas(t1, t2, tol=1e-10):
    return all(casi_igual(x, y, tol) for x, y in zip(t1, t2))

# ------------------------------------------------------------
# Tests con coeficientes reales (debe coincidir con versión real)
# ------------------------------------------------------------
def test_polinomio_real_simple():
    coefs = [1, -3, 2]  # x^2 - 3x + 2
    x = 1.0
    # Solo valor
    p = horner_coeficientes_complejos(coefs, x)
    assert casi_igual(p, 0.0)
    # Con derivada orden 1
    p, dp = horner_coeficientes_complejos(coefs, x, derivada_orden=1)
    assert casi_igual(p, 0.0)
    assert casi_igual(dp, -1.0)  # P'(1) = 2*1 -3 = -1

def test_polinomio_real_derivadas_superiores():
    coefs = [1, -6, 11, -6]  # (x-1)(x-2)(x-3)
    x = 2.0
    p, dp, ddp, dddp = horner_coeficientes_complejos(coefs, x, derivada_orden=3)
    assert casi_igual(p, 0.0)
    assert casi_igual(dp, -1.0)  # P'(2) = -1
    assert casi_igual(ddp, 0.0)  # P''(2) = 0
    assert casi_igual(dddp, 6.0)  # P'''(2) = 6

# ------------------------------------------------------------
# Tests con coeficientes complejos
# ------------------------------------------------------------
def test_polinomio_complejo_simple():
    coefs = [1+1j, 2-1j, 3+0j]  # (1+i)z^2 + (2-i)z + 3
    x = 1+1j
    # Valor esperado: (1+i)*(1+i)^2 = (1+i)*(2i) = 2i -2 = -2+2i
    # Más (2-i)*(1+i) = (2-i)+(2-i)i = 2-i + 2i+1 = 3 + i
    # Suma: (-2+2i) + (3+i) + 3 = 4 + 3i
    esperado = 4 + 3j
    p = horner_coeficientes_complejos(coefs, x)
    assert casi_igual(p, esperado)

def test_polinomio_complejo_derivada():
    # P(z) = (1+i)z^2 + (2-i)z + 3
    coefs = [1+1j, 2-1j, 3]
    x = 1+1j
    # P'(z) = 2(1+i)z + (2-i)
    # En z = 1+i: 2(1+i)(1+i) = 2(2i) = 4i; más (2-i) = 2 - i + 4i = 2 + 3i
    esperado_derivada = 2 + 3j
    p, dp = horner_coeficientes_complejos(coefs, x, derivada_orden=1)
    assert casi_igual(p, 4+3j)
    assert casi_igual(dp, esperado_derivada)

def test_polinomio_complejo_derivada_orden_2():
    # P''(z) = 2(1+i) = 2+2i
    coefs = [1+1j, 2-1j, 3]
    x = 1+1j
    p, dp, ddp = horner_coeficientes_complejos(coefs, x, derivada_orden=2)
    assert casi_igual(p, 4+3j)
    assert casi_igual(dp, 2+3j)
    assert casi_igual(ddp, 2+2j)

# ------------------------------------------------------------
# Tests de errores y casos límite
# ------------------------------------------------------------
def test_coefs_vacio():
    with pytest.raises(ValueError, match="La lista de coeficientes no puede estar vacía"):
        horner_coeficientes_complejos([], 1)

def test_coeficientes_cero_principal():
    # Polinomio de grado menor con ceros iniciales
    coefs = [0, 0, 1, -3, 2]  # equivale a x^2 - 3x + 2
    p = horner_coeficientes_complejos(coefs, 1)
    assert casi_igual(p, 0.0)

def test_polinomio_nulo():
    coefs = [0, 0, 0]
    with pytest.raises(ValueError, match="polinomio es idénticamente cero"):
        horner_coeficientes_complejos(coefs, 1)

def test_derivada_orden_negativo():
    with pytest.raises(ValueError, match="derivada_orden debe ser >= 0"):
        horner_coeficientes_complejos([1,2,3], 1, derivada_orden=-1)

def test_coeficiente_no_numerico():
    with pytest.raises(TypeError, match="Error al convertir coeficientes"):
        horner_coeficientes_complejos(["a", 2, 3], 1)

def test_x_no_convertible():
    with pytest.raises(TypeError, match="Error al convertir x"):
        horner_coeficientes_complejos([1,2,3], "hola")

def test_overflow():
    coefs = [1e300, 0, 1e300]
    x = 1e200
    with pytest.raises(RuntimeError, match="Desbordamiento"):
        horner_coeficientes_complejos(coefs, x)
        
def test_inf_nan_en_x():
    coefs = [1, 2, 3]
    x = float('inf')
    with pytest.raises(RuntimeError, match="contiene valor infinito o NaN"):
        horner_coeficientes_complejos(coefs, x)
    x = float('nan')
    with pytest.raises(RuntimeError, match="contiene valor infinito o NaN"):
        horner_coeficientes_complejos(coefs, x)

# ------------------------------------------------------------
# Tests de evaluación múltiple (si se implementa en el futuro)
# ------------------------------------------------------------
def test_evaluacion_multiple():
    coefs = [1, -3, 2]
    xs = [0, 1, 2, 3]
    # No hay versión múltiple por ahora; pero podemos llamar individualmente
    for x in xs:
        p = horner_coeficientes_complejos(coefs, x)
        assert casi_igual(p, x*x - 3*x + 2)

# ------------------------------------------------------------
# Tests de evaluación con valores decimal y fraction que se deben convertir a complejos
# ------------------------------------------------------------

def test_con_decimal():
    coefs = [Decimal('1'), Decimal('-3'), Decimal('2')]
    x = Decimal('1')
    p = horner_coeficientes_complejos(coefs, x)
    assert casi_igual(p, 0.0)

def test_con_fraction():
    coefs = [Fraction(1,1), Fraction(-3,1), Fraction(2,1)]
    x = Fraction(1,1)
    p = horner_coeficientes_complejos(coefs, x)
    assert casi_igual(p, 0.0)

def test_complejo_con_decimal():
    coefs = [Decimal('1.5'), Decimal('-2.5'), Decimal('1')]  # 1.5x^2 - 2.5x + 1
    x = Decimal('1')
    p = horner_coeficientes_complejos(coefs, x)
    assert casi_igual(p, 1.5 - 2.5 + 1)  # 0.0

def test_complejo_con_fraction_y_decimal():
    coefs = [Fraction(3,2), Decimal('-2.5'), 1]
    x = 1.0
    p = horner_coeficientes_complejos(coefs, x)
    assert casi_igual(p, 0.0)

def test_decimal_con_derivada():
    coefs = [Decimal('1'), Decimal('-3'), Decimal('2')]
    x = Decimal('1')
    p, dp = horner_coeficientes_complejos(coefs, x, derivada_orden=1)
    assert casi_igual(p, 0.0)
    assert casi_igual(dp, -1.0)