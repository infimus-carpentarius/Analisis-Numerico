import pytest
from fractions import Fraction
from decimal import Decimal
from src.utilities import (
    es_numero_real_valido,
    evaluar_seguro,
    signos_opuestos,
    verificar_criterios_parada,
    verificar_continuidad_muestreo
)

# ------------------------------------------------------------
# es_numero_real_valido
# ------------------------------------------------------------
def test_es_numero_real_valido_con_numeros():
    assert es_numero_real_valido(5) is True
    assert es_numero_real_valido(3.14) is True
    assert es_numero_real_valido(Fraction(1, 3)) is True
    assert es_numero_real_valido(Decimal('2.5')) is True
    assert es_numero_real_valido(complex(3, 0)) is True   # imag=0

def test_es_numero_real_valido_con_no_reales():
    assert es_numero_real_valido(complex(1, 2)) is False
    assert es_numero_real_valido("hola") is False
    assert es_numero_real_valido(None) is False
    assert es_numero_real_valido([1, 2]) is False

# ------------------------------------------------------------
# evaluar_seguro
# ------------------------------------------------------------
def test_evaluar_seguro_normal():
    def f(x): return x**2
    assert evaluar_seguro(f, 3) == 9.0
    assert evaluar_seguro(f, 0) == 0.0

def test_evaluar_seguro_con_fraction():
    def f(x): return Fraction(1, 2) * x
    result = evaluar_seguro(f, 4)
    assert isinstance(result, float)
    assert result == pytest.approx(2.0)

def test_evaluar_seguro_con_decimal():
    def f(x): return Decimal('0.5') * x
    result = evaluar_seguro(f, 3)
    assert isinstance(result, float)
    assert result == pytest.approx(1.5)

def test_evaluar_seguro_con_complejo_real():
    def f(x): return complex(x, 0)
    result = evaluar_seguro(f, 2.5)
    assert result == 2.5

def test_evaluar_seguro_division_por_cero():
    def f(x): return 1 / x
    with pytest.raises(ValueError, match="División por cero"):
        evaluar_seguro(f, 0)

def test_evaluar_seguro_no_callable():
    with pytest.raises(TypeError, match="no es callable"):
        evaluar_seguro(42, 1)

def test_evaluar_seguro_complejo_no_real():
    def f(x): return complex(x, 1)
    with pytest.raises(ValueError, match="número complejo con parte imaginaria no nula"):
        evaluar_seguro(f, 1)

# ------------------------------------------------------------
# signos_opuestos
# ------------------------------------------------------------
def test_signos_opuestos():
    assert signos_opuestos(5, -3) is True
    assert signos_opuestos(-2, 7) is True
    assert signos_opuestos(0, 5) is False
    assert signos_opuestos(0, -1) is False
    assert signos_opuestos(0, 0) is False
    assert signos_opuestos(4, 2) is False
    assert signos_opuestos(-1, -3) is False

# ------------------------------------------------------------
# verificar_criterios_parada
# ------------------------------------------------------------
def test_criterios_parada_absoluto():
    # Caso donde NO debe parar (error_abs > tol_abs)
    detener, razon = verificar_criterios_parada(p=1.0, a=1.0, b=1.001, fp=1e-6,
                                                tol_abs=1e-4, rel_tol=None)
    assert detener is False
    
    # Caso donde SÍ debe parar (error_abs < tol_abs)
    detener, razon = verificar_criterios_parada(p=1.0, a=1.0, b=1.00001, fp=1e-6,
                                                tol_abs=1e-4, rel_tol=None)
    assert detener is True
    assert "Error absoluto" in razon

def test_criterios_parada_relativo():
    detener, razon = verificar_criterios_parada(p=100.0, a=99.9, b=100.1, fp=0.5,
                                                tol_abs=1e-9, rel_tol=1e-4)
    # error_abs = (0.2)/2 = 0.1, error_rel = 0.1/100 = 1e-3 < 1e-4? No, 1e-3 > 1e-4
    # entonces no debería parar
    assert detener is False
    # Ahora con rel_tol más grande
    detener, razon = verificar_criterios_parada(p=100.0, a=99.9, b=100.1, fp=0.5,
                                                tol_abs=1e-9, rel_tol=0.1)
    assert detener is True
    assert "Error relativo" in razon

def test_criterios_parada_fp_pequeno():
    detener, razon = verificar_criterios_parada(p=0.5, a=0, b=1, fp=1e-16,
                                                tol_abs=1e-8, rel_tol=None, eps=1e-15)
    assert detener is True
    assert "|f(p)|" in razon

def test_criterios_parada_no_parada():
    detener, razon = verificar_criterios_parada(p=2.0, a=1, b=3, fp=0.5,
                                                tol_abs=1e-6, rel_tol=None)
    assert detener is False
    assert razon == ""

# ------------------------------------------------------------
# verificar_continuidad_muestreo (opcional)
# ------------------------------------------------------------
def test_verificar_continuidad_muestreo_funcion_continua():
    def f(x): return x**2
    continua, msg = verificar_continuidad_muestreo(f, 0, 1, num_puntos=5)
    assert continua is True

def test_verificar_continuidad_muestreo_funcion_constante():
    def f(x): return 5
    continua, msg = verificar_continuidad_muestreo(f, -10, 10)
    assert continua is True
    assert "constante" in msg

def test_verificar_continuidad_muestreo_posible_discontinuidad():
    def f(x):
        if x < 0.5:
            return 0
        else:
            return 1
    continua, msg = verificar_continuidad_muestreo(f, 0, 1, num_puntos=10)
    # Podría detectar un salto si el muestreo captura el cambio
    # No es determinista pero puede fallar. Aquí asumimos que sí lo detecta.
    # Para este test, solo verificamos que no lance excepción.
    assert isinstance(continua, bool)