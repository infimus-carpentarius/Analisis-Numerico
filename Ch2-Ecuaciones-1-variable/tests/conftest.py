import pytest
import math

# ============================================================
# Funciones básicas (solo la función f)
# ============================================================
@pytest.fixture
def funcion_cuadratica():
    """f(x) = x^2 - 2"""
    def f(x):
        return x**2 - 2
    return f

@pytest.fixture
def funcion_cubica():
    """f(x) = x^3 + 4x^2 - 10"""
    def f(x):
        return x**3 + 4*x**2 - 10
    return f

@pytest.fixture
def funcion_raiz_exacta_extremo():
    """f(x) = x - 2, raíz en b=2"""
    def f(x):
        return x - 2
    return f

@pytest.fixture
def funcion_continua_pero_sin_raiz():
    """f(x) = x^2 + 1, siempre positiva"""
    def f(x):
        return x**2 + 1
    return f

# ============================================================
# Funciones completas con derivada y raíz (para Newton, etc.)
# ============================================================
@pytest.fixture
def cuadratica_completa():
    def f(x): return x**2 - 2
    def df(x): return 2*x
    root = math.sqrt(2)
    return f, df, root

@pytest.fixture
def funcion_exponencial():
    def f(x): return math.exp(x) - 3*x
    def df(x): return math.exp(x) - 3
    root = 0.619061286735945  # aproximación de la raíz
    return f, df, root

@pytest.fixture
def funcion_raiz_multiple():
    def f(x): return (x-1)**3
    def df(x): return 3*(x-1)**2
    root = 1.0
    return f, df, root

@pytest.fixture
def funcion_cubica_con_derivada():
    def f(x): return x**3 + 4*x**2 - 10
    def df(x): return 3*x**2 + 8*x
    root = 1.3652300134140969
    return f, df, root

# ============================================================
# Tolerancias estándar
# ============================================================
@pytest.fixture
def tolerancias_estandar():
    return {"tol_abs": 1e-8, "rel_tol": None}