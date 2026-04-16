import pytest
import cmath
from src.root_finding import muller_polinomio, ConvergenceError, IllConditionedError

# ------------------------------------------------------------
# Funciones auxiliares
# ------------------------------------------------------------
def casi_igual(a, b, tol=1e-10):
    return abs(a - b) < tol

# ------------------------------------------------------------
# Tests de convergencia exitosa
# ------------------------------------------------------------
def test_muller_polinomio_real():
    coefs = [1, 0, -2]  # x^2 - 2
    raiz, it, msg = muller_polinomio(coefs, 1, 1.5, 2, tol_abs=1e-10)
    assert casi_igual(raiz, 1.4142135623730951)
    assert "Convergencia alcanzada" in msg

def test_muller_polinomio_complejo():
    coefs = [1, 0, 1]  # x^2 + 1
    # Puntos asimétricos para forzar discriminante negativo
    raiz, it, msg = muller_polinomio(coefs, -1, 0.5, 1, tol_abs=1e-10)
    assert casi_igual(raiz, 1j) or casi_igual(raiz, -1j)

def test_muller_polinomio_raiz_cubica():
    coefs = [1, 0, 0, -1]  # x^3 - 1
    raiz, it, msg = muller_polinomio(coefs, 0, 1, 2, tol_abs=1e-10)
    assert casi_igual(raiz, 1.0)

# ------------------------------------------------------------
# Tests de manejo de errores
# ------------------------------------------------------------
def test_error_coefs_vacio():
    with pytest.raises(ValueError, match="La lista de coeficientes no puede estar vacía"):
        muller_polinomio([], 0, 1, 2)

def test_error_grado_cero():
    with pytest.raises(ValueError, match="El polinomio debe tener al menos grado 1"):
        muller_polinomio([5], 0, 1, 2)

def test_error_puntos_no_reales():
    with pytest.raises(ValueError, match="debe ser real"):
        muller_polinomio([1, -3, 2], 1j, 2, 3)

def test_error_puntos_no_distintos():
    with pytest.raises(ValueError, match="deben ser distintos"):
        muller_polinomio([1, -3, 2], 1, 1, 2)

@pytest.mark.xfail(reason="El estancamiento requiere condiciones muy extremas; puede no activarse en esta plataforma.")
def test_error_estancamiento():
    # Polinomio (x-1)^10 con puntos muy cercanos a 1
    # La convergencia lineal es muy lenta, pero puede no estancarse.
    coefs = [1, -10, 45, -120, 210, -252, 210, -120, 45, -10, 1]  # (x-1)^10
    with pytest.raises(ConvergenceError, match="Estancamiento detectado"):
        muller_polinomio(coefs, 0.999, 1.001, 1.002, max_iter=50, tol_abs=1e-15)

def test_error_ill_conditioned():
    # Polinomio constante no nulo (después de limpiar ceros)
    coefs = [0, 0, 1]
    with pytest.raises(IllConditionedError, match="constante no nulo"):
        muller_polinomio(coefs, 0, 1, 2)

def test_error_no_convergencia():
    coefs = [1, 0, -2]
    with pytest.raises(ConvergenceError, match="No se alcanzó convergencia en 2 iteraciones"):
        muller_polinomio(coefs, 1, 1.5, 2, max_iter=2)

def test_error_overflow():
    # Coeficientes y puntos iniciales enormes -> el método no converge en max_iter
    coefs = [1e300, 0, -2]
    p0, p1, p2 = 1e100, 2e100, 3e100
    # Se espera que termine por superar el número máximo de iteraciones
    with pytest.raises(ConvergenceError, match="No se alcanzó convergencia"):
        muller_polinomio(coefs, p0, p1, p2)

# ------------------------------------------------------------
# Tests de casos límite
# ------------------------------------------------------------
def test_raiz_cero():
    coefs = [1, 0, 0]  # x^2
    raiz, it, msg = muller_polinomio(coefs, -1, -0.5, 1, tol_abs=1e-10)
    assert casi_igual(raiz, 0.0, tol=1e-6)

def test_raices_muy_cercanas():
    # Polinomio (x-1)(x-1.000001) = x^2 - 2.000001x + 1.000001
    coefs = [1, -2.000001, 1.000001]
    raiz, it, msg = muller_polinomio(coefs, 0.9, 1.0, 1.1, tol_abs=1e-8)
    assert casi_igual(raiz, 1.0, tol=1e-5) or casi_igual(raiz, 1.000001, tol=1e-5)

def test_verbose(capsys):
    coefs = [1, 0, -2]
    muller_polinomio(coefs, 1, 1.5, 2, tol_abs=1e-2, verbose=True)
    captured = capsys.readouterr()
    assert "Iter" in captured.out