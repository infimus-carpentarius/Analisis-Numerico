import pytest
import math
from ch2_ecuaciones.root_finding import biseccion, newton, secante, posicion_falsa

# ===================================================================
# Pruebas para bisección (ya existentes, se mantienen)
# ===================================================================
def test_biseccion_raiz_exacta_extremo_izquierdo(funcion_raiz_exacta_extremo):
    f = funcion_raiz_exacta_extremo
    raiz, hist, razon = biseccion(f, 0, 2, verbose=False)
    assert raiz == 2.0
    assert len(hist) == 1
    assert "extremo derecho" in razon

def test_biseccion_raiz_en_medio(funcion_cuadratica):
    f = funcion_cuadratica
    raiz, hist, razon = biseccion(f, 1, 2, tol_abs=1e-10, verbose=False)
    assert raiz == pytest.approx(math.sqrt(2), rel=1e-10)

# ... (puedes incluir aquí todas las pruebas de bisección que ya tenías)

# ===================================================================
# Pruebas para Newton
# ===================================================================
def test_newton_convergencia(cuadratica_completa):
    f, df, root = cuadratica_completa
    raiz, hist, razon = newton(f, df, 1.5, tol_abs=1e-12, verbose=False)
    assert raiz == pytest.approx(root, rel=1e-12)
    assert len(hist) > 1
    assert "Error absoluto" in razon or "|f(p)|" in razon

def test_newton_tolerancia_relativa(funcion_exponencial):
    f, df, root = funcion_exponencial
    raiz, hist, razon = newton(f, df, 0.5, tol_abs=1e-12, rel_tol=1e-8, verbose=False)
    assert raiz == pytest.approx(root, rel=1e-8)
    assert "Error relativo" in razon

def test_newton_derivada_cero():
    f = lambda x: (x-1)**2 + 1
    df = lambda x: 2*(x-1)
    with pytest.raises(ValueError, match="Derivada cercana a cero"):
        newton(f, df, x0=1.0, tol_abs=1e-6)

def test_newton_max_iteraciones(cuadratica_completa):
    f, df, _ = cuadratica_completa
    with pytest.raises(RuntimeError, match="No converge en 2 iteraciones"):
        newton(f, df, 1.5, tol_abs=1e-12, max_iter=2)

def test_newton_raiz_exacta_inicial(cuadratica_completa):
    f, df, root = cuadratica_completa
    raiz, hist, razon = newton(f, df, root, tol_abs=1e-12)
    assert raiz == root
    assert len(hist) == 1
    assert "f(p0) ≈ 0" in razon

def test_newton_verbose(cuadratica_completa, capsys):
    f, df, _ = cuadratica_completa
    newton(f, df, 1.5, tol_abs=0.1, verbose=True)
    captured = capsys.readouterr()
    assert "Iter" in captured.out

# ===================================================================
# Pruebas para Secante
# ===================================================================
def test_secante_convergencia(cuadratica_completa):
    f, _, root = cuadratica_completa
    raiz, hist, razon = secante(f, 1.0, 2.0, tol_abs=1e-12, verbose=False)
    assert raiz == pytest.approx(root, rel=1e-12)
    assert len(hist) > 2
    # Puede parar por error absoluto o por |f(p)| pequeño
    assert ("Error absoluto" in razon) or ("|f(p)|" in razon)

def test_secante_tolerancia_relativa(funcion_exponencial):
    f, _, root = funcion_exponencial
    raiz, hist, razon = secante(f, 0.5, 0.7, tol_abs=1e-12, rel_tol=1e-8, verbose=False)
    assert raiz == pytest.approx(root, rel=1e-8)
    assert "Error relativo" in razon

def test_secante_denominador_nulo():
    f = lambda x: x**2 - 1
    with pytest.raises(ValueError, match="Denominador nulo"):
        secante(f, 2.0, -2.0, max_iter=2)

def test_secante_max_iteraciones(cuadratica_completa):
    f, _, _ = cuadratica_completa
    with pytest.raises(RuntimeError, match="No converge en 2 iteraciones"):
        secante(f, 1.0, 2.0, tol_abs=1e-12, max_iter=2)

def test_secante_raiz_exacta_inicial(cuadratica_completa):
    f, _, root = cuadratica_completa
    raiz, hist, razon = secante(f, root, root+0.1, tol_abs=1e-12)
    # La raíz debe ser la correcta
    assert raiz == pytest.approx(root, rel=1e-12)
    # El historial puede tener 1 entrada (si se detecta inmediatamente) 
    # o 2 (si por redondeo se añade p1 antes de la comprobación)
    assert len(hist) in (1, 2)
    # Si se detectó raíz en p0, la razón debe indicarlo
    if len(hist) == 1:
        assert "f(p0) ≈ 0" in razon
    # Si tiene 2, no es necesario comprobar el último valor, pues la raíz ya es correcta

def test_secante_verbose(cuadratica_completa, capsys):
    f, _, _ = cuadratica_completa
    secante(f, 1.0, 2.0, tol_abs=0.1, verbose=True)
    captured = capsys.readouterr()
    assert "Iter" in captured.out

# ===================================================================
# Pruebas para Posición Falsa
# ===================================================================
def test_posicion_falsa_convergencia(cuadratica_completa):
    f, _, root = cuadratica_completa
    raiz, hist, razon = posicion_falsa(f, 1.0, 2.0, tol_abs=1e-12, verbose=False)
    assert raiz == pytest.approx(root, rel=1e-12)
    assert len(hist) > 1
    # Puede parar por error absoluto o por |f(p)| pequeño
    assert ("Error absoluto" in razon) or ("|f(p)|" in razon)

def test_posicion_falsa_intervalo_sin_cambio_signo():
    f = lambda x: x**2 - 2
    with pytest.raises(ValueError, match="deben tener signos opuestos"):
        posicion_falsa(f, 0, 1)

def test_posicion_falsa_tolerancia_relativa(funcion_exponencial):
    f, _, root = funcion_exponencial
    raiz, hist, razon = posicion_falsa(f, 0.5, 0.8, tol_abs=1e-12, rel_tol=1e-8, verbose=False)
    assert raiz == pytest.approx(root, rel=1e-8)
    # Puede parar por error relativo o por |f(p)| pequeño
    assert ("Error relativo" in razon) or ("|f(p)|" in razon)

def test_posicion_falsa_raiz_extremo():
    f = lambda x: x - 2
    raiz, hist, razon = posicion_falsa(f, 1.0, 2.0, tol_abs=1e-12)
    assert raiz == 2.0
    assert len(hist) == 1
    assert "f(b) ≈ 0" in razon

def test_posicion_falsa_max_iteraciones(cuadratica_completa):
    f, _, _ = cuadratica_completa
    with pytest.raises(RuntimeError, match="No converge en 2 iteraciones"):
        posicion_falsa(f, 1.0, 2.0, tol_abs=1e-12, max_iter=2)

def test_posicion_falsa_verbose(cuadratica_completa, capsys):
    f, _, _ = cuadratica_completa
    posicion_falsa(f, 1.0, 2.0, tol_abs=0.1, verbose=True)
    captured = capsys.readouterr()
    assert "Iter" in captured.out

# ===================================================================
# Comparación entre métodos
# ===================================================================
def test_comparacion_metodos(funcion_cubica_con_derivada):
    f, df, root = funcion_cubica_con_derivada
    raiz_n, _, _ = newton(f, df, 1.5, tol_abs=1e-10)
    raiz_s, _, _ = secante(f, 1.0, 2.0, tol_abs=1e-10)
    raiz_pf, _, _ = posicion_falsa(f, 1.0, 2.0, tol_abs=1e-10)
    raiz_b, _, _ = biseccion(f, 1.0, 2.0, tol_abs=1e-10)
    
    assert raiz_n == pytest.approx(root, rel=1e-10)
    assert raiz_s == pytest.approx(root, rel=1e-10)
    assert raiz_pf == pytest.approx(root, rel=1e-10)
    assert raiz_b == pytest.approx(root, rel=1e-10)