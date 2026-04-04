import pytest
from src.aritmetica import ieee754_binary_to_float
import math

def test_cero_positivo():
    bits = "0" * 64
    assert ieee754_binary_to_float(bits) == 0.0

def test_cero_negativo():
    bits = "1" + "0" * 63
    assert ieee754_binary_to_float(bits) == -0.0

def test_uno():
    bits = "0" + "01111111111" + "0" * 52
    assert ieee754_binary_to_float(bits) == 1.0

def test_infinito_positivo():
    bits = "0" + "11111111111" + "0" * 52
    assert math.isinf(ieee754_binary_to_float(bits)) and ieee754_binary_to_float(bits) > 0

def test_nan():
    bits = "0" + "11111111111" + "1" + "0" * 51
    assert math.isnan(ieee754_binary_to_float(bits))

def test_ejemplo_a():
    bits = "0100000010101001001100000000000000000000000000000000000000000000"
    valor = ieee754_binary_to_float(bits)
    # Valor correcto según la interpretación IEEE 754: 3224.0
    assert valor == pytest.approx(3224.0, abs=1e-8)

def test_ejemplo_b():
    bits = "1100000010101001001100000000000000000000000000000000000000000000"
    valor = ieee754_binary_to_float(bits)
    assert valor == pytest.approx(-3224.0, abs=1e-8)

def test_ejemplo_c():
    bits = "0011111111110101001100000000000000000000000000000000000000000000"
    valor = ieee754_binary_to_float(bits)
    assert valor == pytest.approx(1.32421875, abs=1e-8)

def test_ejemplo_d():
    # Mismo que c
    bits = "0011111111110101001100000000000000000000000000000000000000000000"
    valor = ieee754_binary_to_float(bits)
    assert valor == pytest.approx(1.32421875, abs=1e-8)

def test_longitud_incorrecta():
    with pytest.raises(ValueError):
        ieee754_binary_to_float("101")