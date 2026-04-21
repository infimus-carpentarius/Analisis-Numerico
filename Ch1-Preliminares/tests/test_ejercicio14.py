import pytest
import math
from ch1_preliminares.ejercicio14 import (
    f_exacta, f_redondeo_3_digitos, f_maclaurin_3digits, limite_en_cero
)

def test_limite():
    assert limite_en_cero() == 2.0

def test_valor_real():
    # Valor real dado en el enunciado
    real_enunciado = 2.003335000
    assert abs(f_exacta(0.1) - real_enunciado) < 1e-9

def test_redondeo_directo():
    # Valor esperado según cálculo manual: 2.05
    aprox = f_redondeo_3_digitos(0.1)
    # Nota: la aritmética de 3 dígitos da 2.05, pero puede haber pequeñas diferencias
    assert aprox == pytest.approx(2.05, abs=0.005)

def test_maclaurin_redondeo():
    # Valor esperado: 2.00
    aprox = f_maclaurin_3digits(0.1)
    assert aprox == pytest.approx(2.00, abs=0.005)

def test_error_relativo_maclaurin_menor():
    # El error relativo de Maclaurin debe ser menor que el de la aproximación directa
    real = f_exacta(0.1)
    err_directa = abs(real - f_redondeo_3_digitos(0.1)) / abs(real)
    err_maclaurin = abs(real - f_maclaurin_3digits(0.1)) / abs(real)
    assert err_maclaurin < err_directa

# Opcional: prueba de que el método directo tiene un error relativo alto
@pytest.mark.xfail(reason="La aproximación directa con 3 dígitos es muy burda (error ~2.3%)")
def test_error_directo_pequeno():
    # Esta prueba fallará intencionadamente porque el error no es pequeño
    real = f_exacta(0.1)
    err = abs(real - f_redondeo_3_digitos(0.1)) / abs(real)
    assert err < 0.001  # Esto falla, como esperamos