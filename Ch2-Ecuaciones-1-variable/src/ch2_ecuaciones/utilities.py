"""
Utilidades para análisis numérico: evaluación segura, validación de signos, criterios de parada.
"""

from fractions import Fraction
from decimal import Decimal

def es_numero_real_valido(valor):
    """
    Retorna True si valor es un número real convertible a float.
    Reconoce: int, float, Fraction, Decimal, y complex con parte imaginaria cero.
    """
    if isinstance(valor, (int, float, Fraction, Decimal)):
        return True
    if hasattr(valor, 'imag') and hasattr(valor, 'real'):
        return valor.imag == 0
    return False

def evaluar_seguro(f, x, contexto=""):
    """
    Evalúa f(x) de forma segura, convierte el resultado a float si es posible.
    
    Parámetros
    ----------
    f : callable
        Función a evaluar.
    x : float
        Punto de evaluación.
    contexto : str
        Texto adicional para mensajes de error (ej. "extremo izquierdo").
    
    Retorna
    -------
    float
        Valor de f(x) convertido a float.
    
    Lanza
    -----
    TypeError
        Si f no es callable.
    ValueError
        Si f(x) no es un número real convertible.
    RuntimeError
        Si ocurre un error durante la evaluación (división por cero, etc.).
    """
    if not callable(f):
        raise TypeError(f"f no es callable. Recibido: {type(f)}")
    
    try:
        valor = f(x)
    except ZeroDivisionError as e:
        raise ValueError(f"División por cero al evaluar f({x}) {contexto}: {e}")
    except OverflowError as e:
        raise ValueError(f"Desbordamiento numérico al evaluar f({x}) {contexto}: {e}")
    except TypeError as e:
        raise TypeError(f"Error de tipo al evaluar f({x}) {contexto}: {e}")
    except Exception as e:
        raise RuntimeError(f"Error inesperado al evaluar f({x}) {contexto}: {type(e).__name__}: {e}")
    
    if not es_numero_real_valido(valor):
        if hasattr(valor, 'imag') and hasattr(valor, 'real') and valor.imag != 0:
            raise ValueError(f"f({x}) {contexto} retornó un número complejo con parte imaginaria no nula: {valor}")
        else:
            raise ValueError(f"f({x}) {contexto} no es un número real convertible. "f"Tipo: {type(valor).__name__}, valor: {valor}")
        
    
    # Conversión segura a float
    if isinstance(valor, float):
        return valor
    if isinstance(valor, int):
        return float(valor)
    if isinstance(valor, Fraction):
        return float(valor.numerator) / valor.denominator
    if isinstance(valor, Decimal):
        return float(valor)
    if hasattr(valor, 'imag') and hasattr(valor, 'real'):
        return float(valor.real)
    
    # Fallback (no debería llegar aquí)
    return float(valor)

def signos_opuestos(x, y):
    """
    Retorna True si x e y tienen signos opuestos (uno positivo, otro negativo).
    Considera cero como no opuesto (a menos que se maneje aparte).
    """
    return (x > 0 and y < 0) or (x < 0 and y > 0)

def verificar_criterios_parada(p, a, b, fp, tol_abs, rel_tol=None, eps=1e-15):
    """
    Verifica si se debe detener la iteración según criterios estándar (absoluto, relativo, valor pequeño).
    
    Parámetros
    ----------
    p : float
        Aproximación actual.
    a, b : float
        Extremos del intervalo actual (para bisección).
    fp : float
        f(p).
    tol_abs : float
        Tolerancia absoluta para el error (longitud del intervalo).
    rel_tol : float o None
        Tolerancia relativa (opcional).
    eps : float
        Umbral para considerar f(p) ≈ 0.
    
    Retorna
    -------
    (detener, razon) : (bool, str)
        detener es True si se cumple algún criterio.
        razon es una descripción del criterio cumplido.
    """
    error_abs = (b - a) / 2.0
    
    if abs(fp) < eps:
        return True, f"|f(p)| = {abs(fp):.2e} < {eps:.2e}"
    if error_abs < tol_abs:
        return True, f"Error absoluto {error_abs:.2e} < {tol_abs:.2e}"
    if rel_tol is not None and p != 0:
        error_rel = error_abs / abs(p)
        if error_rel < rel_tol:
            return True, f"Error relativo {error_rel:.2e} < {rel_tol:.2e}"
    return False, ""

def verificar_continuidad_muestreo(f, a, b, num_puntos=10):
    """
    Verifica que f parezca continua en [a,b] muestreando puntos.
    No se ejecuta por defecto; el usuario debe activarla explícitamente.
    
    Retorna
    -------
    (bool, str): (es_continua_aparente, mensaje)
    """
    puntos = [a + i*(b-a)/num_puntos for i in range(num_puntos+1)]
    try:
        valores = [evaluar_seguro(f, x, "muestreo") for x in puntos]
    except Exception as e:
        return False, f"Error al evaluar durante muestreo: {e}"
    
    rango = max(valores) - min(valores)
    if rango == 0:
        return True, "Función constante, no se detectan discontinuidades."
    for i in range(len(valores)-1):
        if abs(valores[i+1] - valores[i]) > 10 * rango:
            return False, f"Posible discontinuidad entre {puntos[i]} y {puntos[i+1]}"
    return True, "No se detectaron discontinuidades evidentes."