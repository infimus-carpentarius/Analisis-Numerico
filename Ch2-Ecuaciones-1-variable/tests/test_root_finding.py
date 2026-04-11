import pytest
import math
from src.root_finding import biseccion

# ------------------------------------------------------------
# Pruebas para biseccion
# ------------------------------------------------------------
def test_biseccion_raiz_exacta_extremo_izquierdo(funcion_raiz_exacta_extremo):
    f = funcion_raiz_exacta_extremo  # f(x)=x-2, raíz en x=2
    # Intervalo [0,2], f(2)=0 -> debe devolver b=2
    raiz, hist, razon = biseccion(f, 0, 2, verbose=False)
    assert raiz == 2.0
    assert len(hist) == 1
    assert hist[0][0] == 0  # iteración 0
    assert "extremo derecho" in razon

def test_biseccion_raiz_exacta_extremo_derecho():
    def f(x): return x + 1   # raíz en -1
    raiz, hist, razon = biseccion(f, -2, -1, verbose=False)
    assert raiz == -1.0
    assert "extremo derecho" in razon

def test_biseccion_raiz_en_medio(funcion_cuadratica):
    f = funcion_cuadratica  # x^2 - 2, raíz sqrt(2)
    raiz, hist, razon = biseccion(f, 1, 2, tol_abs=1e-10, verbose=False)
    assert raiz == pytest.approx(math.sqrt(2), rel=1e-10)
    assert "Error absoluto" in razon or "|f(p)|" in razon

def test_biseccion_con_tolerancia_relativa(funcion_cubica):
    f = funcion_cubica
    raiz, hist, razon = biseccion(f, 1, 2, tol_abs=1e-12, rel_tol=1e-6, verbose=False)
    # La raíz real es ≈1.3652300134140969
    assert raiz == pytest.approx(1.365230013414, rel=1e-6)
    # Verificar que la razón sea relativa o absoluta
    assert "Error" in razon

def test_biseccion_funcion_sin_raiz(funcion_continua_pero_sin_raiz):
    f = funcion_continua_pero_sin_raiz  # x^2+1, siempre positiva
    with pytest.raises(ValueError, match="deben tener signos opuestos"):
        biseccion(f, -1, 1)

def test_biseccion_intervalo_desordenado(funcion_cuadratica):
    # a > b debe ordenarse internamente
    raiz, hist, razon = biseccion(funcion_cuadratica, 2, 1, tol_abs=1e-10)
    assert raiz == pytest.approx(math.sqrt(2), rel=1e-10)

def test_biseccion_max_iteraciones(funcion_cuadratica):
    # Con max_iter=1 no alcanza la tolerancia, debe lanzar RuntimeError
    with pytest.raises(RuntimeError, match="No converge en 1 iteraciones"):
        biseccion(funcion_cuadratica, 1, 2, tol_abs=1e-10, max_iter=1)

def test_biseccion_tolerancia_invalida(funcion_cuadratica):
    with pytest.raises(ValueError, match="tol_abs debe ser positivo"):
        biseccion(funcion_cuadratica, 1, 2, tol_abs=0)
    with pytest.raises(ValueError, match="rel_tol debe ser positivo"):
        biseccion(funcion_cuadratica, 1, 2, rel_tol=-0.1)

def test_biseccion_verbose(funcion_cuadratica, capsys):
    biseccion(funcion_cuadratica, 1, 2, tol_abs=1e-1, verbose=True)
    captured = capsys.readouterr()
    assert "Iter" in captured.out

def test_biseccion_con_extra_checks(funcion_cuadratica):
    # extra_checks=True no debe cambiar el resultado, solo advertir si hay discontinuidad
    raiz, hist, razon = biseccion(funcion_cuadratica, 1, 2, extra_checks=True, tol_abs=1e-8)
    assert raiz == pytest.approx(math.sqrt(2), rel=1e-8)

def test_biseccion_raiz_exacta_por_casualidad():
    # f(x)=x-1, intervalo [0,2] -> raíz en 1 (no es extremo)
    def f(x): return x - 1
    raiz, hist, razon = biseccion(f, 0, 2, tol_abs=1e-12, verbose=False)
    # El método encontrará p=1 exactamente en alguna iteración (fp=0)
    assert raiz == 1.0
    # La razón debe ser |f(p)| < eps
    assert "|f(p)|" in razon

