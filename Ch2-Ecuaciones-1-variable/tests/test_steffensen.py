import pytest
import math
from ch2_ecuaciones.root_finding import steffensen, aitken

# ------------------------------------------------------------
# Funciones de prueba
# ------------------------------------------------------------
def g_sqrt(x):
    """Iteración de Herón: converge a sqrt(2)"""
    return (x + 2/x) / 2

def g_cos(x):
    """Iteración de coseno: converge a 0.7390851332"""
    return math.cos(x)

def g_lineal(x):
    """Sucesión lineal p_n = 1/n (no es iteración de punto fijo, solo para probar aitken)"""
    return 1 / (x + 1)   # no se usa en steffensen

# ------------------------------------------------------------
# Pruebas para aitken (paso individual)
# ------------------------------------------------------------
def test_aitken_formula():
    # Sucesión p_n = 1/n (converge a 0)
    p0, p1, p2 = 1.0, 0.5, 1/3
    p_hat = aitken(p0, p1, p2)
    # El valor acelerado debe estar más cerca de 0 que p2
    assert abs(p_hat) < abs(p2)
    # Verificar fórmula con valores conocidos
    # Cálculo manual: numerador = (0.5-1)^2 = 0.25, denominador = 1/3 - 1 + 0.5 = -0.16666...
    # p_hat = 1 - 0.25 / (-0.16666) = 1 + 1.5 = 2.5 ?? Eso no es correcto. Revisemos:
    # Denominador = p2 - 2p1 + p0 = 0.3333 - 1 + 1 = 0.3333. Entonces p_hat = 1 - 0.25/0.3333 = 1 - 0.75 = 0.25.
    # Efectivamente, p_hat = 0.25, que está más cerca de 0 que 0.3333.
    assert p_hat == pytest.approx( 0.25, rel=1e-9, abs=1e-12)

def test_aitken_denominador_cero():
    # Caso donde denominador es cero (sucesión constante)
    p0 = p1 = p2 = 2.0
    p_hat = aitken(p0, p1, p2)
    assert p_hat == p2   # fallback

# ------------------------------------------------------------
# Pruebas para steffensen
# ------------------------------------------------------------
def test_steffensen_sqrt():
    raiz, hist, razon = steffensen(g_sqrt, p0=1.5, tol_abs=1e-12, verbose=False)
    assert raiz == pytest.approx(math.sqrt(2), rel=1e-12)
    assert len(hist) <= 5   # convergencia cuadrática → pocas iteraciones

def test_steffensen_cos():
    raiz, hist, razon = steffensen(g_cos, p0=0.5, tol_abs=1e-10)
    assert raiz == pytest.approx(0.7390851332151606, rel=1e-10)
    assert len(hist) <= 6

def test_steffensen_tolerancia_relativa():
    raiz, hist, razon = steffensen(g_sqrt, p0=1.5, tol_abs=1e-15, rel_tol=1e-8)
    assert raiz == pytest.approx(math.sqrt(2), rel=1e-8)
    assert "Error relativo" in razon or "Error absoluto" in razon

def test_steffensen_raiz_exacta_inicial():
    # Si p0 ya es punto fijo, debe retornar inmediatamente
    p0 = math.sqrt(2)
    raiz, hist, razon = steffensen(g_sqrt, p0=p0, tol_abs=1e-12)
    assert raiz == pytest.approx(p0, abs=1e-12)
    assert len(hist) == 1
    assert "f(p0)" in razon or "inicial" in razon or "p0 es punto fijo" in razon  # depende de la implementación

def test_steffensen_verbose(capsys):
    steffensen(g_sqrt, p0=1.5, tol_abs=1e-2, verbose=True)
    captured = capsys.readouterr()
    assert "Iter" in captured.out

def test_steffensen_max_iter():
    with pytest.raises(RuntimeError, match="No converge en 2 iteraciones"):
        steffensen(g_sqrt, p0=1000, max_iter=2)   # desde muy lejos, no converge rápido

def g_divergente(x):
    return x + 1   # no tiene punto fijo, diverge

def test_steffensen_no_converge():
    with pytest.raises(RuntimeError, match="No converge en 5 iteraciones"):
        steffensen(g_divergente, p0=0, max_iter=5)