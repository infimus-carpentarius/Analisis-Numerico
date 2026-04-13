"""
Métodos numéricos para encontrar raíces de ecuaciones en una variable.
"""

from src.utilities import (
    evaluar_seguro,
    signos_opuestos,
    verificar_criterios_parada,
    verificar_continuidad_muestreo
)

def biseccion(f, a, b, tol_abs=1e-8, rel_tol=None, max_iter=100,
              verbose=False, extra_checks=False):
    """
    Método de bisección robusto con manejo de raíz exacta en extremos,
    criterios de parada absoluto y relativo opcional, y verificación extra opcional.
    
    Parámetros
    ----------
    f : callable
        Función continua, debe devolver un número real.
    a, b : float
        Extremos del intervalo (se ordenan internamente).
    tol_abs : float, opcional
        Tolerancia absoluta para la longitud del intervalo (default 1e-8).
    rel_tol : float o None, opcional
        Tolerancia relativa. Si es None (default), no se usa.
    max_iter : int, opcional
        Número máximo de iteraciones (default 100).
    verbose : bool, opcional
        Si es True, imprime información de cada iteración.
    extra_checks : bool, opcional
        Si es True, ejecuta verificaciones adicionales (continuidad) antes de iterar.
    
    Retorna
    -------
    p : float
        Aproximación a la raíz.
    historial : list of tuples
        Lista con (iteración, a, b, p, f(p)).
    razon_parada : str
        Descripción de por qué terminó el método.
    
    Lanza
    -----
    ValueError
        Si los parámetros de tolerancia son inválidos o si f(a) y f(b) no tienen signos opuestos.
    RuntimeError
        Si no converge en max_iter iteraciones.
    """
    # Ordenar extremos
    if a > b:
        a, b = b, a
    
    # Validaciones básicas
    if tol_abs <= 0:
        raise ValueError(f"tol_abs debe ser positivo: {tol_abs}")
    if rel_tol is not None and rel_tol <= 0:
        raise ValueError(f"rel_tol debe ser positivo o None: {rel_tol}")
    if max_iter <= 0:
        raise ValueError(f"max_iter debe ser positivo: {max_iter}")
    
    # Evaluación inicial
    fa = evaluar_seguro(f, a, "extremo izquierdo")
    fb = evaluar_seguro(f, b, "extremo derecho")
    
    # Raíz exacta en extremo
    if fa == 0:
        razon = f"f(a)=0, raíz exacta en extremo izquierdo a={a}"
        if verbose:
            print(razon)
        return a, [(0, a, b, a, fa)], razon
    if fb == 0:
        razon = f"f(b)=0, raíz exacta en extremo derecho b={b}"
        if verbose:
            print(razon)
        return b, [(0, a, b, b, fb)], razon
    
    # Verificación de signos opuestos
    if not signos_opuestos(fa, fb):
        raise ValueError(f"f(a) y f(b) deben tener signos opuestos. "
                         f"f({a})={fa}, f({b})={fb}")
    
    # Verificaciones adicionales (opcionales)
    if extra_checks:
        continua, msg = verificar_continuidad_muestreo(f, a, b)
        if not continua:
            print(f"Advertencia: {msg}")
            # No detenemos, solo advertimos
    
    historial = []
    for i in range(1, max_iter + 1):
        p = a + (b - a) / 2.0
        fp = evaluar_seguro(f, p, f"iteración {i}")
        historial.append((i, a, b, p, fp))
        
        if verbose:
            print(f"Iter {i:3d}: a={a:.10f}, b={b:.10f}, p={p:.10f}, f(p)={fp:.2e}")
        
        detener, razon = verificar_criterios_parada(p, a, b, fp, tol_abs, rel_tol)
        if detener:
            if verbose:
                print(f"  → {razon}")
            return p, historial, razon
        
        # Actualizar intervalo
        if (fa > 0 and fp > 0) or (fa < 0 and fp < 0):
            a = p
            fa = fp
        else:
            b = p
            fb = fp
    
    razon = f"No converge en {max_iter} iteraciones. Último intervalo [{a:.6f}, {b:.6f}], longitud {(b-a):.2e}"
    raise RuntimeError(razon)


def punto_fijo(g, p0, tol_abs=1e-8, rel_tol=None, max_iter=100,
               verbose=False, extra_checks=False):
    """
    Método de iteración de punto fijo: p_{n+1} = g(p_n).
    
    Parámetros
    ----------
    g : callable
        Función de iteración. Debe cumplir g(p)=p en la raíz.
    p0 : float
        Aproximación inicial.
    tol_abs : float, opcional
        Tolerancia absoluta para |p_n - p_{n-1}| (default 1e-8).
    rel_tol : float or None, opcional
        Tolerancia relativa |p_n - p_{n-1}|/|p_n| (si no es None).
    max_iter : int, opcional
        Número máximo de iteraciones (default 100).
    verbose : bool, opcional
        Si True, imprime cada iteración.
    extra_checks : bool, opcional
        Si True, realiza verificaciones adicionales (ej. continuidad de g).
    
    Retorna
    -------
    p : float
        Aproximación al punto fijo.
    historial : list of tuples
        Lista con (iteración, p_n, g(p_n)).
    razon_parada : str
        Descripción de por qué terminó.
    
    Lanza
    -----
    ValueError
        Si los parámetros son inválidos.
    RuntimeError
        Si no converge en max_iter iteraciones.
    """
    # Validaciones
    if tol_abs <= 0:
        raise ValueError(f"tol_abs debe ser positivo: {tol_abs}")
    if rel_tol is not None and rel_tol <= 0:
        raise ValueError(f"rel_tol debe ser positivo o None: {rel_tol}")
    if max_iter <= 0:
        raise ValueError(f"max_iter debe ser positivo: {max_iter}")
    
    p_prev = float(p0)
    # Evaluar g(p0) para la primera iteración (p1)
    try:
        p_next = evaluar_seguro(g, p_prev, "iteración 1")
    except Exception as e:
        raise RuntimeError(f"Error al evaluar g(p0): {e}")
    
    historial = [(0, p_prev, None)]  # iteración 0: valor inicial
    historial.append((1, p_next, None))  # iteración 1: p1
    
    if verbose:
        print(f"Iter 0: p0 = {p_prev:.10f}")
        print(f"Iter 1: p1 = {p_next:.10f}")
    
    # Verificar si ya es punto fijo (p1 == p0) -> raíz exacta
    if p_next == p_prev:
        razon = "p1 == p0 (punto fijo exacto)"
        return p_next, historial, razon
    
    for i in range(2, max_iter+1):
        p_prev, p_next = p_next, evaluar_seguro(g, p_next, f"iteración {i}")
        historial.append((i, p_next, None))
        
        if verbose:
            print(f"Iter {i:3d}: p = {p_next:.10f}, g(p) = {g(p_next):.10f}")
        
        # Criterios de parada (adaptamos verificar_criterios_parada para punto fijo)
        # Usamos diferencia absoluta y relativa entre p_next y p_prev
        error_abs = abs(p_next - p_prev)
        if error_abs < tol_abs:
            razon = f"Error absoluto {error_abs:.2e} < {tol_abs:.2e}"
            return p_next, historial, razon
        if rel_tol is not None and p_next != 0:
            error_rel = error_abs / abs(p_next)
            if error_rel < rel_tol:
                razon = f"Error relativo {error_rel:.2e} < {rel_tol:.2e}"
                return p_next, historial, razon
        # También podemos detener si |g(p)-p| es muy pequeño (equivalente a |f(p)|<eps)
        # Esto ya está implícito en el error absoluto.
    
    raise RuntimeError(f"No converge en {max_iter} iteraciones. Último p = {p_next:.6f}")

# src/root_finding.py (continuación)

# ============================================================================
# Método de Newton (Newton-Raphson)
# ============================================================================
def newton(f, df, x0, tol_abs=1e-8, rel_tol=None, max_iter=100, verbose=False):
    """
    Método de Newton para encontrar una raíz de f.
    
    Parámetros
    ----------
    f : callable
        Función objetivo.
    df : callable
        Derivada de f (debe ser proporcionada).
    x0 : float
        Aproximación inicial.
    tol_abs : float
        Tolerancia absoluta para |p_n - p_{n-1}|.
    rel_tol : float or None
        Tolerancia relativa |p_n - p_{n-1}|/|p_n|.
    max_iter : int
        Número máximo de iteraciones.
    verbose : bool
        Si True, imprime cada iteración.
    
    Retorna
    -------
    p : float
        Aproximación a la raíz.
    historial : list of tuples (iter, p, f(p), f'(p))
    razon_parada : str
    """
    p = float(x0)
    fp = evaluar_seguro(f, p, "inicial")
    historial = [(0, p, fp, None)]
    if abs(fp) < 1e-15:
        return p, historial, "f(p0) ≈ 0"
    
    for i in range(1, max_iter+1):
        fprima = evaluar_seguro(df, p, f"derivada en iter {i}")
        if abs(fprima) < 1e-15:
            raise ValueError(f"Derivada cercana a cero en x={p}. No se puede continuar.")
        p_next = p - fp / fprima
        fp_next = evaluar_seguro(f, p_next, f"iter {i}")
        historial.append((i, p_next, fp_next, fprima))
        
        if verbose:
            print(f"Iter {i:3d}: p={p:.10f}, f(p)={fp:.2e}, f'(p)={fprima:.2e}, p_next={p_next:.10f}")
        
        error_abs = abs(p_next - p)
        if error_abs < tol_abs:
            return p_next, historial, f"Error absoluto {error_abs:.2e} < {tol_abs:.2e}"
        if rel_tol is not None and p_next != 0:
            error_rel = error_abs / abs(p_next)
            if error_rel < rel_tol:
                return p_next, historial, f"Error relativo {error_rel:.2e} < {rel_tol:.2e}"
        if abs(fp_next) < 1e-15:
            return p_next, historial, "|f(p)| ≈ 0"
        
        p, fp = p_next, fp_next
    
    raise RuntimeError(f"No converge en {max_iter} iteraciones. Último p = {p:.6f}")

# ============================================================================
# Método de la secante
# ============================================================================
def secante(f, p0, p1, tol_abs=1e-8, rel_tol=None, max_iter=100, verbose=False):
    """
    Método de la secante para encontrar una raíz de f.
    """
    p_prev = float(p0)
    p_curr = float(p1)
    fp_prev = evaluar_seguro(f, p_prev, "inicial 0")
    fp_curr = evaluar_seguro(f, p_curr, "inicial 1")
    historial = [(0, p_prev, fp_prev), (1, p_curr, fp_curr)]
    
    if abs(fp_prev) < 1e-15:
        return p_prev, historial, "f(p0) ≈ 0"
    if abs(fp_curr) < 1e-15:
        return p_curr, historial, "f(p1) ≈ 0"
    
    for i in range(2, max_iter+1):
        if abs(fp_curr - fp_prev) < 1e-15:
            raise ValueError("Denominador nulo: f(p_curr) = f(p_prev).")
        p_next = p_curr - fp_curr * (p_curr - p_prev) / (fp_curr - fp_prev)
        fp_next = evaluar_seguro(f, p_next, f"iter {i}")
        historial.append((i, p_next, fp_next))
        
        if verbose:
            print(f"Iter {i:3d}: p={p_next:.10f}, f(p)={fp_next:.2e}")
        
        error_abs = abs(p_next - p_curr)
        if error_abs < tol_abs:
            return p_next, historial, f"Error absoluto {error_abs:.2e} < {tol_abs:.2e}"
        if rel_tol is not None and p_next != 0:
            error_rel = error_abs / abs(p_next)
            if error_rel < rel_tol:
                return p_next, historial, f"Error relativo {error_rel:.2e} < {rel_tol:.2e}"
        if abs(fp_next) < 1e-15:
            return p_next, historial, "|f(p)| ≈ 0"
        
        p_prev, p_curr = p_curr, p_next
        fp_prev, fp_curr = fp_curr, fp_next
    
    raise RuntimeError(f"No converge en {max_iter} iteraciones. Último p = {p_curr:.6f}")

# ============================================================================
# Método de la secante
# ============================================================================
from src.utilities import evaluar_seguro, signos_opuestos   # asegurar import

def posicion_falsa(f, a, b, tol_abs=1e-8, rel_tol=None, max_iter=100, verbose=False):
    """
    Método de posición falsa (Regula Falsi) para encontrar una raíz de f en [a,b].
    
    Parámetros
    ----------
    f : callable
        Función continua.
    a, b : float
        Extremos del intervalo (se ordenan internamente).
    tol_abs : float
        Tolerancia absoluta para la longitud del intervalo (|b-a|).
    rel_tol : float or None
        Tolerancia relativa (opcional).
    max_iter : int
        Número máximo de iteraciones.
    verbose : bool
        Si True, imprime cada iteración.
    
    Retorna
    -------
    p : float
        Aproximación a la raíz.
    historial : list of tuples (iter, a, b, p, f(p))
    razon_parada : str
    """
    if a > b:
        a, b = b, a
    fa = evaluar_seguro(f, a, "extremo izquierdo")
    fb = evaluar_seguro(f, b, "extremo derecho")
    
    # Raíz exacta en extremo
    if abs(fa) < 1e-15:
        return a, [(0, a, b, a, fa)], "f(a) ≈ 0"
    if abs(fb) < 1e-15:
        return b, [(0, a, b, b, fb)], "f(b) ≈ 0"
    
    # Verificar cambio de signo usando función auxiliar (evita multiplicación)
    if not signos_opuestos(fa, fb):
        raise ValueError("f(a) y f(b) deben tener signos opuestos")
    
    historial = []
    for i in range(1, max_iter+1):
        # Calcular punto por interpolación lineal
        p = b - fb * (b - a) / (fb - fa)
        fp = evaluar_seguro(f, p, f"iter {i}")
        historial.append((i, a, b, p, fp))
        
        if verbose:
            print(f"Iter {i:3d}: a={a:.10f}, b={b:.10f}, p={p:.10f}, f(p)={fp:.2e}")
        
        # Criterios de parada
        error_abs = abs(b - a)
        if error_abs < tol_abs:
            return p, historial, f"Error absoluto (intervalo) {error_abs:.2e} < {tol_abs:.2e}"
        if rel_tol is not None and p != 0:
            error_rel = error_abs / abs(p)
            if error_rel < rel_tol:
                return p, historial, f"Error relativo {error_rel:.2e} < {rel_tol:.2e}"
        if abs(fp) < 1e-15:
            return p, historial, "|f(p)| ≈ 0"
        
        # Actualizar intervalo usando comparación de signos (sin multiplicar)
        if signos_opuestos(fa, fp):
            # La raíz está entre a y p
            b = p
            fb = fp
        else:
            # La raíz está entre p y b
            a = p
            fa = fp
    
    raise RuntimeError(f"No converge en {max_iter} iteraciones. Último intervalo [{a:.6f}, {b:.6f}]")

from src.utilities import evaluar_seguro

# src/root_finding.py

from src.utilities import evaluar_seguro

def newton_modificado(f, df, ddf, x0, tol_abs=1e-8, rel_tol=None, max_iter=100, eps=1e-15, verbose=False):
    """
    Método de Newton modificado para raíces múltiples.
    
    Parámetros
    ----------
    f : callable
        Función objetivo.
    df : callable
        Primera derivada.
    ddf : callable
        Segunda derivada.
    x0 : float
        Aproximación inicial.
    tol_abs : float
        Tolerancia absoluta para |x_{n+1} - x_n|.
    rel_tol : float or None
        Tolerancia relativa |x_{n+1} - x_n| / |x_{n+1}|.
    max_iter : int
        Número máximo de iteraciones.
    eps : float
        Umbral para considerar |f(p)| ≈ 0.
    verbose : bool
        Si es True, imprime cada iteración.
    
    Retorna
    -------
    p : float
        Aproximación a la raíz.
    historial : list of tuples (iter, x, f(x))
    razon_parada : str
    """
    x = float(x0)
    fx = evaluar_seguro(f, x, "inicial")
    historial = [(0, x, fx)]
    
    if abs(fx) < eps:
        return x, historial, "f(x0) ≈ 0"
    
    for i in range(1, max_iter+1):
        fpx = evaluar_seguro(df, x, f"derivada {i}")
        fppx = evaluar_seguro(ddf, x, f"segunda derivada {i}")
        
        denominador = fpx*fpx - fx*fppx
        if abs(denominador) < 1e-15:
            raise ValueError(f"Denominador nulo en x={x}. Posible raíz exacta o mal condicionamiento.")
        
        x_next = x - fx*fpx / denominador
        fx_next = evaluar_seguro(f, x_next, f"iter {i}")
        historial.append((i, x_next, fx_next))
        
        if verbose:
            print(f"Iter {i:3d}: x={x:.10f}, f(x)={fx:.2e}, x_next={x_next:.10f}")
        
        error_abs = abs(x_next - x)
        if error_abs < tol_abs:
            return x_next, historial, f"Error absoluto {error_abs:.2e} < {tol_abs:.2e}"
        if rel_tol is not None and x_next != 0:
            error_rel = error_abs / abs(x_next)
            if error_rel < rel_tol:
                return x_next, historial, f"Error relativo {error_rel:.2e} < {rel_tol:.2e}"
        if abs(fx_next) < eps:
            return x_next, historial, "|f(p)| ≈ 0"
        
        x, fx = x_next, fx_next
    
    raise RuntimeError(f"No converge en {max_iter} iteraciones. Último x = {x:.6f}")

# ============================================================================
# Método Δ² de Aitken y método de Steffensen
# ============================================================================

def aitken(p0, p1, p2):
    """
    Aplica un paso del método Δ² de Aitken a tres términos consecutivos.

    Parámetros
    ----------
    p0, p1, p2 : float
        Tres términos consecutivos de una sucesión (p_n, p_{n+1}, p_{n+2}).

    Retorna
    -------
    p_hat : float
        Estimación acelerada del límite.
    """
    numerador = (p1 - p0) ** 2
    denominador = p2 - 2*p1 + p0
    if abs(denominador) < 1e-15:
        return p2   # fallback seguro
    return p0 - numerador / denominador


def steffensen(g, p0, tol_abs=1e-8, rel_tol=None, max_iter=100, verbose=False):
    """
    Método de Steffensen para encontrar un punto fijo de g.

    Parámetros
    ----------
    g : callable
        Función de iteración (debe cumplir g(p)=p en la raíz).
    p0 : float
        Aproximación inicial.
    tol_abs : float
        Tolerancia absoluta para |p_{n+1} - p_n|.
    rel_tol : float or None
        Tolerancia relativa |p_{n+1} - p_n| / |p_{n+1}|.
    max_iter : int
        Número máximo de iteraciones.
    verbose : bool
        Si es True, imprime cada iteración.

    Retorna
    -------
    p : float
        Aproximación al punto fijo.
    historial : list of tuples
        (iteración, p_actual, g(p_actual))
    razon_parada : str
        Descripción de la causa de terminación.
    """
    from src.utilities import evaluar_seguro

    #Prueba si el punto p0 es ya un punto fijo y no es necesaria ninguna operacion
    gp0 = evaluar_seguro(g, p0, "inicial")
    if abs(gp0 - p0) < 1e-15:
        return p0, [(0, p0, gp0)], "p0 es punto fijo"


    p = p0
    historial = [(0, p, evaluar_seguro(g, p, "inicial"))]

    for i in range(1, max_iter + 1):
        p1 = evaluar_seguro(g, p, f"iter {i}.1")
        p2 = evaluar_seguro(g, p1, f"iter {i}.2")
        p_new = aitken(p, p1, p2)

        historial.append((i, p_new, evaluar_seguro(g, p_new, f"iter {i}.final")))
        if verbose:
            print(f"Iter {i:3d}: p0={p:.10f}, p1={p1:.10f}, p2={p2:.10f}, p_new={p_new:.10f}")

        error_abs = abs(p_new - p)
        if error_abs < tol_abs:
            return p_new, historial, f"Error absoluto {error_abs:.2e} < {tol_abs:.2e}"
        if rel_tol is not None and p_new != 0:
            error_rel = error_abs / abs(p_new)
            if error_rel < rel_tol:
                return p_new, historial, f"Error relativo {error_rel:.2e} < {rel_tol:.2e}"

        p = p_new

    raise RuntimeError(f"No converge en {max_iter} iteraciones. Último p = {p:.6f}")