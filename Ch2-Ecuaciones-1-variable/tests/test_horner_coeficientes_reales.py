import pytest
import math
from src.root_finding import horner_coeficientes_reales

# ------------------------------------------------------------
# Funciones auxiliares para polinomios de prueba
# ------------------------------------------------------------
def polinomio_cuadratico():
    return [1, -3, 2]          # x^2 - 3x + 2

def polinomio_cubico():
    return [1, -6, 11, -6]     # x^3 - 6x^2 + 11x - 6

def polinomio_constante():
    return [5]

def polinomio_lineal():
    return [2, 1]              # 2x + 1

# ------------------------------------------------------------
# Tests de evaluación correcta (ajustados a tupla cuando derivada_orden=0)
# ------------------------------------------------------------
def test_evaluacion_simple():
    coefs = polinomio_cuadratico()
    # Con derivada_orden=0, la función devuelve una tupla de un elemento
    resultado = horner_coeficientes_reales(coefs, 1)
    assert resultado[0] == pytest.approx(0.0)
    assert horner_coeficientes_reales(coefs, 2)[0] == pytest.approx(0.0)
    assert horner_coeficientes_reales(coefs, 3)[0] == pytest.approx(2.0)

def test_evaluacion_con_derivada_orden_1():
    coefs = polinomio_cuadratico()
    resultado = horner_coeficientes_reales(coefs, 1, derivada_orden=1)
    esperado = (0.0, -1.0)
    assert resultado[0] == pytest.approx(esperado[0])
    assert resultado[1] == pytest.approx(esperado[1])

def test_evaluacion_con_derivada_orden_2():
    coefs = polinomio_cuadratico()
    resultado = horner_coeficientes_reales(coefs, 1, derivada_orden=2)
    esperado = (0.0, -1.0, 2.0)
    for r, e in zip(resultado, esperado):
        assert r == pytest.approx(e)

def test_evaluacion_con_derivada_orden_3():
    coefs = polinomio_cubico()
    resultado = horner_coeficientes_reales(coefs, 2, derivada_orden=3)
    esperado = (0.0, -1.0, 0.0, 6.0)
    for r, e in zip(resultado, esperado):
        assert r == pytest.approx(e)

def test_evaluacion_orden_mayor_que_grado():
    coefs = polinomio_cuadratico()
    resultado = horner_coeficientes_reales(coefs, 1, derivada_orden=3)
    esperado = (0.0, -1.0, 2.0, 0.0)
    for r, e in zip(resultado, esperado):
        assert r == pytest.approx(e)

def test_evaluacion_polinomio_constante():
    coefs = polinomio_constante()
    assert horner_coeficientes_reales(coefs, 100)[0] == pytest.approx(5.0)
    resultado = horner_coeficientes_reales(coefs, 100, derivada_orden=1)
    assert resultado[0] == pytest.approx(5.0)
    assert resultado[1] == pytest.approx(0.0)

def test_evaluacion_polinomio_lineal():
    coefs = polinomio_lineal()
    resultado = horner_coeficientes_reales(coefs, 3, derivada_orden=1)
    assert resultado[0] == pytest.approx(7.0)
    assert resultado[1] == pytest.approx(2.0)

def test_evaluacion_multiple():
    coefs = polinomio_cuadratico()
    xs = [0, 1, 2, 3]
    resultados = horner_coeficientes_reales(coefs, xs, derivada_orden=1)
    esperado = [(2.0, -3.0), (0.0, -1.0), (0.0, 1.0), (2.0, 3.0)]
    for res, esp in zip(resultados, esperado):
        assert res[0] == pytest.approx(esp[0])
        assert res[1] == pytest.approx(esp[1])

# ------------------------------------------------------------
# Tests de manejo de errores (entradas inválidas)
# ------------------------------------------------------------
def test_coefs_vacio():
    with pytest.raises(ValueError, match="La lista de coeficientes no puede estar vacía"):
        horner_coeficientes_reales([], 1)

def test_derivada_orden_no_entero():
    coefs = polinomio_cuadratico()
    with pytest.raises(TypeError, match="derivada_orden debe ser un número entero"):
        horner_coeficientes_reales(coefs, 1, derivada_orden=1.5)
    with pytest.raises(TypeError, match="derivada_orden debe ser un número entero"):
        horner_coeficientes_reales(coefs, 1, derivada_orden=True)

def test_derivada_orden_negativo():
    coefs = polinomio_cuadratico()
    with pytest.raises(ValueError, match="derivada_orden debe ser >= 0"):
        horner_coeficientes_reales(coefs, 1, derivada_orden=-1)

def test_coeficiente_no_real():
    coefs = [1, "a", 2]
    with pytest.raises(ValueError, match="Coeficiente no real"):
        horner_coeficientes_reales(coefs, 1)

def test_x_no_convertible_a_float():
    coefs = polinomio_cuadratico()
    with pytest.raises(ValueError, match="Error al convertir x"):
        horner_coeficientes_reales(coefs, "abc")

# ------------------------------------------------------------
# Tests de desbordamiento (ahora verifican que el resultado sea inf)
# ------------------------------------------------------------
def test_overflow_polinomio_alto_grado():
    coefs = [1] + [0]*999 + [1]   # x^1000 + 1
    x_grande = 1e200
    resultado = horner_coeficientes_reales(coefs, x_grande, derivada_orden=0)
    assert math.isinf(resultado[0]), f"Se esperaba infinito, se obtuvo {resultado[0]}"

def test_overflow_con_derivada():
    # Coeficientes que provocan overflow con x adecuado
    coefs = [1e200, 0, 0, 1]          # 1e200 * x^3 + 1
    x = 1e50                           # (1e50)^3 = 1e150 → producto = 1e350 → inf
    resultado = horner_coeficientes_reales(coefs, x, derivada_orden=1)
    # Al menos uno de los valores (polinomio o derivada) debe ser infinito
    assert math.isinf(resultado[0]) or math.isinf(resultado[1]), \
        f"Se esperaba inf, se obtuvo ({resultado[0]}, {resultado[1]})"

# ------------------------------------------------------------
# Test adicional: polinomio con Decimal (ya debería funcionar)
# ------------------------------------------------------------
def test_polinomio_con_decimal():
    from decimal import Decimal
    coefs = [Decimal('1.5'), Decimal('-2.5'), Decimal('1.0')]
    resultado = horner_coeficientes_reales(coefs, 1, derivada_orden=1)
    assert resultado[0] == pytest.approx(0.0)
    assert resultado[1] == pytest.approx(0.5)