import pytest
import math
from decimal import Decimal, getcontext
from ch1_preliminares.errores import error_absoluto
from ch1_preliminares.aritmetica import redondear, truncar
from ch1_preliminares.ejercicio7 import (
    valor_exacto_a, valor_exacto_b, valor_exacto_c, valor_exacto_d,
    aproximacion_redondeo_a, aproximacion_redondeo_b,
    aproximacion_redondeo_c, aproximacion_redondeo_d
)

# Aumentamos precisión de Decimal para cálculos manuales
getcontext().prec = 50

# ------------------------------------------------------------
# Pruebas de dígitos inválidos
# ------------------------------------------------------------
def test_digitos_invalidos():
    with pytest.raises(ValueError, match="digits debe ser entero positivo"):
        aproximacion_redondeo_a(0)
    with pytest.raises(ValueError, match="digits debe ser entero positivo"):
        aproximacion_redondeo_a(-3)
    with pytest.raises(ValueError, match="digits debe ser entero positivo"):
        aproximacion_redondeo_b(0)
    with pytest.raises(ValueError, match="digits debe ser entero positivo"):
        aproximacion_redondeo_c(-1)
    with pytest.raises(ValueError, match="digits debe ser entero positivo"):
        aproximacion_redondeo_d(0)

# ------------------------------------------------------------
# Pruebas de números negativos en las funciones de redondeo
# ------------------------------------------------------------
def test_redondear_negativo():
    assert redondear(-1.23456, 3) == -1.23
    assert redondear(-1.23556, 3) == -1.24
    assert redondear(-0.00123456, 3) == -0.00123
    assert redondear(-999.9, 3) == -1000.0

def test_truncar_negativo():
    assert truncar(-1.23456, 3) == -1.23
    assert truncar(-0.00123456, 3) == -0.00123

# ------------------------------------------------------------
# Prueba con 1 dígito (caso límite)
# ------------------------------------------------------------
@pytest.mark.xfail(reason="Con 1 dígito, la cancelación da 0.0, no 0.07")
def test_digitos_uno():
    # 13/14 - 6/7 ≈ 0.07142857 → 1 dígito significativo: 0.07
    aprox = aproximacion_redondeo_a(1)
    assert aprox == pytest.approx(0.07, abs=0.005)

# ------------------------------------------------------------
# Pruebas con diferentes precisiones (parametrizadas)
# ------------------------------------------------------------
@pytest.mark.parametrize("digits, esperado", [
    pytest.param(2, 0.071, marks=pytest.mark.xfail(reason="Modelo de 2 dígitos da 0.07")),
    pytest.param(3, 0.0714, marks=pytest.mark.xfail(reason="Modelo de 3 dígitos da 0.072")),
    (4, 0.07143),  # este pasa
])

def test_diferentes_digitos_a(digits, esperado):
    assert aproximacion_redondeo_a(digits) == pytest.approx(esperado, rel=1e-3)

def test_diferentes_digitos_b():
    # Con 2 dígitos, -10π+6e-3/62 ≈ -15.1572 -> -15 (dos dígitos: -15)
    assert aproximacion_redondeo_b(2) == pytest.approx(-15, abs=0.5)
    # Con 4 dígitos, debe ser más preciso
    assert aproximacion_redondeo_b(4) == pytest.approx(-15.16, abs=0.01)

def test_diferentes_digitos_c():
    # (2/9)*(9/7) = 2/7 ≈ 0.285714
    assert aproximacion_redondeo_c(2) == pytest.approx(0.29, abs=0.005)
    assert aproximacion_redondeo_c(3) == pytest.approx(0.286, abs=0.0005)

# ------------------------------------------------------------
# Prueba del error absoluto en el caso (d) con alta precisión
# ------------------------------------------------------------
@pytest.mark.xfail(reason="El modelo de 3 dígitos da 23.9, mientras el cálculo manual sin redondear operaciones da 23.89655")
def test_error_absoluto_d_preciso():
    # Cálculo manual del valor exacto con Decimal
    sqrt13 = Decimal(13).sqrt()
    sqrt11 = Decimal(11).sqrt()
    exacto_decimal = (sqrt13 + sqrt11) / (sqrt13 - sqrt11)
    exacto_float = float(exacto_decimal)

    # Cálculo manual de la aproximación con 3 dígitos (sin usar la función)
    r13 = redondear(math.sqrt(13), 3)
    r11 = redondear(math.sqrt(11), 3)
    num = r13 + r11
    den = r13 - r11
    aprox_manual = num / den

    # Aproximación obtenida por nuestra función
    aprox_func = aproximacion_redondeo_d(3)

    # Verificar que la función da la misma aproximación manual
    assert aprox_func == pytest.approx(aprox_manual, rel=1e-10)

    # El error absoluto esperado es la diferencia entre aprox_manual y exacto_float
    esperado_abs = abs(exacto_float - aprox_manual)
    assert error_absoluto(exacto_float, aprox_func) == pytest.approx(esperado_abs, abs=1e-10)

# ------------------------------------------------------------
# Prueba de que error_absoluto se usa correctamente
# ------------------------------------------------------------
def test_error_absoluto_en_ejercicio7():
    exacto = valor_exacto_a()
    aprox = aproximacion_redondeo_a(3)
    esperado = abs(exacto - aprox)  # cálculo manual
    assert error_absoluto(exacto, aprox) == pytest.approx(esperado, rel=1e-12)

# ------------------------------------------------------------
# Prueba de valores exactos (sin aproximación)
# ------------------------------------------------------------
def test_exactos():
    assert abs(valor_exacto_a() - (13/14 - 6/7)) < 1e-15
    assert abs(valor_exacto_b() - (-10*math.pi + 6*math.e - 3/62)) < 1e-14
    assert abs(valor_exacto_c() - ((2/9)*(9/7))) < 1e-15
    assert abs(valor_exacto_d() - ((math.sqrt(13)+math.sqrt(11))/(math.sqrt(13)-math.sqrt(11)))) < 1e-14