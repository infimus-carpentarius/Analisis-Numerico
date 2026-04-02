import pytest
from src.errores import error_absoluto, error_relativo

def test_error_absoluto():
    assert error_absoluto(3.1415926535, 3.1416) == pytest.approx(7.3465e-6)
    assert error_absoluto(2.718281828, 2.718) == pytest.approx(2.81828e-4)

def test_error_relativo():
    assert error_relativo(3.1415926535, 3.1416) == pytest.approx(2.338e-6)
    assert error_relativo(2.718281828, 2.718) == pytest.approx(1.0367e-4)

def test_error_relativo_cero():
    with pytest.raises(ValueError):
        error_relativo(0, 0.001)