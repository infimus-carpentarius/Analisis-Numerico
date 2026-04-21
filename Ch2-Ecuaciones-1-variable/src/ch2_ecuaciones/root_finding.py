"""
Métodos numéricos para encontrar raíces de ecuaciones en una variable.
"""

from ch2_ecuaciones.utilities import (
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
from ch2_ecuaciones.utilities import evaluar_seguro, signos_opuestos   # asegurar import

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



from ch2_ecuaciones.utilities import evaluar_seguro

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
    from ch2_ecuaciones.utilities import evaluar_seguro

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

from ch2_ecuaciones.utilities import es_numero_real_valido

def horner_coeficientes_reales(coefs, x, derivada_orden=0):
    """
    Evalúa un polinomio con coeficientes reales en uno o varios puntos usando el método de Horner,
    y opcionalmente calcula las derivadas hasta un orden dado.
    
    Parámetros
    ----------
    coefs : list of numeric
        Coeficientes desde el de mayor grado hasta el independiente.
    x : numeric or list of numeric
        Punto o lista de puntos donde evaluar.
    derivada_orden : int, optional
        Orden máximo de derivada a calcular. Debe ser un entero no negativo.
        0: solo valor, 1: valor y primera derivada, etc. Por defecto 0.
    
    Retorna
    -------
    Si x es un número:
        tuple (p, dp, ddp, ...) de longitud derivada_orden+1.
    Si x es una lista:
        list of tuples, cada tuple con los valores para ese punto.
    
    Lanza
    -----
    TypeError
        Si derivada_orden no es un entero.
    ValueError
        Si coefs está vacío, derivada_orden < 0, o algún coeficiente no es convertible a float.
    OverflowError
        Si ocurre desbordamiento durante las operaciones.
    """
    if not coefs:
        raise ValueError("La lista de coeficientes no puede estar vacía")
    
    # Validación estricta: derivada_orden debe ser entero (no bool, no float)
    if type(derivada_orden) is not int:
        raise TypeError(f"derivada_orden debe ser un número entero, no {type(derivada_orden).__name__}")
    
    if derivada_orden < 0:
        raise ValueError("derivada_orden debe ser >= 0")
    
    # Convertir coeficientes a float validando que sean reales
    try:
        coefs_f = []
        for c in coefs:
            if not es_numero_real_valido(c):
                raise ValueError(f"Coeficiente no real: {c}")
            coefs_f.append(float(c))
    except Exception as e:
        raise ValueError(f"Error al convertir coeficientes: {e}")
    
    n = len(coefs_f) - 1  # grado
    
    def evaluar_en_punto(x0):
        try:
            xf = float(x0)
            if not es_numero_real_valido(xf):
                raise ValueError(f"x no es un número real: {x0}")
        except Exception as e:
            raise ValueError(f"Error al convertir x: {e}")
        
        # Función auxiliar: Horner con cociente
        def horner_con_cociente(coefs, x):
            b = coefs[0]
            cociente = [b]
            for i in range(1, len(coefs)):
                b = b * x + coefs[i]
                if i < len(coefs)-1:
                    cociente.append(b)
            return b, cociente
        
        resultados = []
        coefs_actual = coefs_f[:]
        for orden in range(derivada_orden + 1):
            if orden > n:
                resultados.append(0.0)
                continue
            try:
                val, cociente = horner_con_cociente(coefs_actual, xf)
                resultados.append(val)
                coefs_actual = cociente
            except OverflowError:
                raise OverflowError(f"Desbordamiento al evaluar derivada orden {orden} en x={xf}")
        
        # Ajustar factoriales para órdenes >=2
        factorial = 1
        for k in range(2, derivada_orden + 1):
            factorial *= k
            resultados[k] *= factorial
        
        return tuple(resultados)
    
    # Si x es un solo número, devolver tupla
    if isinstance(x, (int, float)):
        return evaluar_en_punto(x)
    # Si es iterable (lista, tupla, etc.), devolver lista de tuplas
    try:
        iter(x)
    except TypeError:
        return evaluar_en_punto(x)
    else:
        return [evaluar_en_punto(xi) for xi in x]
    
import cmath
import math
from typing import List, Union, Tuple

def horner_coeficientes_complejos(
    coefs: List[Union[complex, float, int]],
    x: Union[complex, float, int],
    derivada_orden: int = 0
) -> Union[complex, Tuple[complex, ...]]:
    """
    Evalúa un polinomio con coeficientes complejos (o reales) en un punto complejo x
    usando el método de Horner. Opcionalmente calcula las derivadas hasta un orden dado.

    Parámetros
    ----------
    coefs : list
        Coeficientes del polinomio desde el de mayor grado hasta el independiente.
        Pueden ser números complejos, reales o enteros.
    x : complex, float, int
        Punto de evaluación.
    derivada_orden : int, optional
        Orden máximo de derivada a calcular (0 = solo valor, 1 = valor y primera derivada, etc.).
        Por defecto 0.

    Retorna
    -------
    Si derivada_orden == 0:
        complex : valor del polinomio en x.
    Si derivada_orden > 0:
        tuple : (P(x), P'(x), P''(x), ..., P^{(derivada_orden)}(x))

    Lanza
    -----
    ValueError
        Si la lista de coeficientes está vacía, o derivada_orden es negativo.
    TypeError
        Si algún coeficiente no es convertible a complex, o x no es convertible.
    RuntimeError
        Si ocurre overflow o se detectan valores inf/nan durante la evaluación.
    """
    if not coefs:
        raise ValueError("La lista de coeficientes no puede estar vacía")
    if derivada_orden < 0:
        raise ValueError("derivada_orden debe ser >= 0")

    # Convertir todos los coeficientes a complex
    try:
        coefs_c = [complex(c) for c in coefs]
    except Exception as e:
        raise TypeError(f"Error al convertir coeficientes a complex: {e}")

    # Eliminar ceros a la izquierda (coeficiente principal no nulo)
    while len(coefs_c) > 1 and abs(coefs_c[0]) == 0.0:
        coefs_c.pop(0)
    if len(coefs_c) == 1 and coefs_c[0] == 0:
        raise ValueError("El polinomio es idénticamente cero (todos los coeficientes nulos)")

    # Convertir x a complex
    try:
        xc = complex(x)
    except Exception as e:
        raise TypeError(f"Error al convertir x a complex: {e}")

    # Detectar posibles overflow/inf/nan en x
    if math.isinf(xc.real) or math.isinf(xc.imag) or math.isnan(xc.real) or math.isnan(xc.imag):
        raise RuntimeError(f"x contiene valor infinito o NaN: {xc}")

    n = len(coefs_c) - 1  # grado

    # Función auxiliar para evaluar polinomio y cociente (sin factorial)
    def horner_con_cociente(c: List[complex], x: complex) -> Tuple[complex, List[complex]]:
        b = c[0]
        cociente = [b]
        for i in range(1, len(c)):
            b = b * x + c[i]
            if i < len(c) - 1:
                cociente.append(b)
        return b, cociente

    resultados = []
    coefs_actual = coefs_c[:]

    for orden in range(derivada_orden + 1):
        if orden > n:
            resultados.append(0.0 + 0.0j)
            continue
        try:
            val, cociente = horner_con_cociente(coefs_actual, xc)
        except (OverflowError, ZeroDivisionError) as e:
            raise RuntimeError(f"Overflow o división por cero en derivada orden {orden}: {e}")
        # Verificar si val contiene inf o nan
        if math.isinf(val.real) or math.isinf(val.imag) or math.isnan(val.real) or math.isnan(val.imag):
            raise RuntimeError(f"Desbordamiento: valor {val} en derivada orden {orden}")
        resultados.append(val)
        coefs_actual = cociente  # preparar para siguiente derivada

    # Ajustar factoriales para órdenes >= 2
    factorial = 1
    for k in range(2, derivada_orden + 1):
        factorial *= k
        resultados[k] *= factorial

    if derivada_orden == 0:
        return resultados[0]
    else:
        return tuple(resultados)
    
import cmath
import math
from typing import List, Union, Tuple

# Excepciones específicas
class ConvergenceError(RuntimeError):
    """Excepción para fallos de convergencia."""
    pass

class IllConditionedError(RuntimeError):
    """Excepción para problemas de mal condicionamiento numérico."""
    pass

def muller_polinomio(
    coefs: List[Union[complex, float, int]],
    p0: float,
    p1: float,
    p2: float,
    tol_abs: float = 1e-8,
    tol_rel: float = 1e-8,
    tol_f: float = 1e-12,
    max_iter: int = 100,
    verbose: bool = False
) -> Tuple[Union[float, complex], int, str]:
    """
    Método de Müller para encontrar una raíz de un polinomio.

    Parámetros
    ----------
    coefs : list
        Coeficientes del polinomio (de mayor a menor grado). Pueden ser reales o complejos.
    p0, p1, p2 : float
        Tres aproximaciones iniciales reales y distintas.
    tol_abs : float
        Tolerancia absoluta para |dx| (defecto 1e-8).
    tol_rel : float
        Tolerancia relativa para |dx|/|p_new| (defecto 1e-8).
    tol_f : float
        Tolerancia para el residuo |f(p_new)| (defecto 1e-12).
    max_iter : int
        Número máximo de iteraciones (defecto 100).
    verbose : bool
        Si es True, imprime cada iteración.

    Retorna
    -------
    raiz : float or complex
        Aproximación a la raíz (se convierte a float si la parte imaginaria < 1e-12).
    iteraciones : int
        Número de iteraciones realizadas.
    razon : str
        Causa de parada.

    Lanza
    -----
    ValueError
        Si los coeficientes son inválidos, los puntos iniciales no son reales o no son distintos.
    ConvergenceError
        Si el método no converge en max_iter iteraciones o se estanca.
    IllConditionedError
        Si el polinomio está mal condicionado (puntos demasiado cercanos, función casi constante).
    RuntimeError
        Para otros errores aritméticos (overflow, etc.).
    """
    # Validaciones básicas
    if not coefs:
        raise ValueError("La lista de coeficientes no puede estar vacía.")
    if len(coefs) < 2:
        raise ValueError("El polinomio debe tener al menos grado 1.")

    # Limpiar coeficientes (eliminar ceros a la izquierda)
    coefs_c = [complex(c) for c in coefs]
    while len(coefs_c) > 1 and abs(coefs_c[0]) == 0.0:
        coefs_c.pop(0)
    if len(coefs_c) == 1:
        if coefs_c[0] == 0.0:
            raise ValueError("El polinomio es idénticamente cero.")
        else:
            raise IllConditionedError("El polinomio es constante no nulo. No tiene raíces.")

    # Normalización de coeficientes
    if abs(coefs_c[0]) > 1e10:
        factor = coefs_c[0]
        coefs_c = [c / factor for c in coefs_c]
        if verbose:
            print("Coeficientes normalizados (divididos por el principal).")

    # Validación de puntos iniciales reales y distintos
    for p in (p0, p1, p2):
        if isinstance(p, complex) and p.imag != 0:
            raise ValueError(f"El punto inicial {p} debe ser real.")
    p0, p1, p2 = float(p0), float(p1), float(p2)
    if len({p0, p1, p2}) < 3:
        raise ValueError("Los tres puntos iniciales deben ser distintos.")

    # Ordenar puntos (mejora estabilidad)
    p0, p1, p2 = sorted([p0, p1, p2])
    x0, x1, x2 = complex(p0, 0), complex(p1, 0), complex(p2, 0)
    x_new = x2  # inicialización para evitar UnboundLocalError

    # Evaluación inicial
    try:
        f0 = horner_coeficientes_complejos(coefs_c, x0)
        f1 = horner_coeficientes_complejos(coefs_c, x1)
        f2 = horner_coeficientes_complejos(coefs_c, x2)
    except Exception as e:
        raise RuntimeError(f"Error en evaluación inicial: {e}")

    # Verificar degeneración
    if abs(f0 - f1) < 1e-12 and abs(f1 - f2) < 1e-12:
        raise IllConditionedError(
            "La función es prácticamente constante en los puntos iniciales."
        )

    prev_error = None
    estancamiento = 0

    for i in range(3, max_iter + 1):
        h0 = x0 - x2
        h1 = x1 - x2
        if abs(h0) < 1e-15 or abs(h1) < 1e-15:
            raise IllConditionedError(
                f"Puntos demasiado cercanos (h0={h0}, h1={h1})."
            )
        # Evitar división por cero en denominador de a
        if abs(h1 + h0) < 1e-15:
            # Perturbar ligeramente x0
            x0 += 1e-12 * (1 + 1j)
            h0 = x0 - x2
            h1 = x1 - x2

        d0 = (f0 - f2) / h0
        d1 = (f1 - f2) / h1
        a = (d1 - d0) / (h1 + h0)
        b = a * h1 + d1
        c = f2

        if abs(a) < 1e-12:
            # Parábola casi lineal: usar secante
            if abs(b) < 1e-15:
                dx = 0.0
            else:
                dx = -c / b
        else:
            disc = b * b - 4.0 * a * c
            sqrt_disc = cmath.sqrt(disc)
            den1 = b + sqrt_disc
            den2 = b - sqrt_disc
            den = den1 if abs(den1) >= abs(den2) else den2
            if abs(den) < 1e-15:
                dx = 0.0
            else:
                dx = -2.0 * c / den

        x_new = x2 + dx
        try:
            f_new = horner_coeficientes_complejos(coefs_c, x_new)
        except Exception as e:
            raise RuntimeError(f"Error aritmético en iteración {i}: {e}")

        error_abs = abs(dx)
        error_rel = error_abs / abs(x_new) if abs(x_new) > 1e-15 else 0.0
        residuo = abs(f_new)

        if verbose:
            print(f"Iter {i:3d}: x = {x_new}, f(x) = {f_new}, "
                  f"err_abs={error_abs:.2e}, err_rel={error_rel:.2e}")

        # Criterios de parada
        if error_abs < tol_abs or error_rel < tol_rel or residuo < tol_f:
            if abs(x_new.imag) < 1e-12:
                x_new = x_new.real
            razon = f"Convergencia alcanzada: error_abs={error_abs:.2e}, error_rel={error_rel:.2e}, residuo={residuo:.2e}"
            return x_new, i, razon

        # Detección de estancamiento
        if prev_error is not None:
            if error_abs >= prev_error * 0.99:
                estancamiento += 1
            else:
                estancamiento = 0
            if estancamiento >= 5:
                raise ConvergenceError(
                    "Estancamiento detectado: el error absoluto no disminuye."
                )
        prev_error = error_abs

        # Desplazar puntos
        x0, x1, x2 = x1, x2, x_new
        f0, f1, f2 = f1, f2, f_new

    raise ConvergenceError(
        f"No se alcanzó convergencia en {max_iter} iteraciones. "
        f"Último valor: x = {x_new}"
    )