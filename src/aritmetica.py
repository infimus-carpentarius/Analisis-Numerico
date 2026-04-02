#!/usr/bin/env python3
"""
Funciones para simular aritmética de punto flotante con un número fijo de dígitos significativos.
Soporta corte y redondeo.
"""

import math

def normalizar(valor: float, digits: int):
    """
    Normaliza un número a la forma 0.d1 d2 ... * 10^n, con 1 <= d1 <= 9.
    Retorna (mantisa normalizada, exponente).
    """
    if valor == 0.0:
        return 0.0, 0
    signo = 1 if valor > 0 else -1
    valor = abs(valor)
    exponente = math.floor(math.log10(valor))
    mantisa = valor / (10 ** exponente)
    # Ajustar para que mantisa quede en [1, 10)
    if mantisa >= 10.0:
        mantisa /= 10.0
        exponente += 1
    elif mantisa < 1.0:
        mantisa *= 10.0
        exponente -= 1
    return signo * mantisa, exponente

def truncar(valor: float, digits: int) -> float:
    """
    Representa un número usando corte (truncamiento) a 'digits' dígitos significativos.
    """
    if not isinstance(digits, int):
        raise TypeError("digits debe ser entero")
    if digits <= 0:
        raise ValueError("digits debe ser positivo")
    if math.isnan(valor) or math.isinf(valor):
        return valor
    if valor == 0.0:
        return 0.0
    mantisa, exp = normalizar(valor, digits)
    # Extraer la parte entera de la mantisa (está en [1,10))
    factor = 10 ** (digits - 1)
    entero = int(mantisa * factor)  # truncamiento
    mantisa_trunc = entero / factor
    return mantisa_trunc * (10 ** exp)

def redondear(valor: float, digits: int) -> float:
    """
    Representa un número usando redondeo a 'digits' dígitos significativos.
    """
    if not isinstance(digits, int):
        raise TypeError("digits debe ser entero")
    if digits <= 0:
        raise ValueError("digits debe ser positivo")
    if math.isnan(valor) or math.isinf(valor):
        return valor
    if valor == 0.0:
        return 0.0
    mantisa, exp = normalizar(valor, digits)
    factor = 10 ** (digits - 1)
    # Redondear usando round (que es banker's rounding, pero es suficiente)
    mantisa_redondeada = round(mantisa * factor) / factor
    # Si el redondeo lleva la mantisa a 10, ajustar
    if mantisa_redondeada >= 10.0:
        mantisa_redondeada /= 10.0
        exp += 1
    return mantisa_redondeada * (10 ** exp)

def operar_corte(op, a: float, b: float, digits: int) -> float:
    """Operación con corte a 'digits' dígitos."""
    resultado_exacto = op(a, b)
    return truncar(resultado_exacto, digits)

def operar_redondeo(op, a: float, b: float, digits: int) -> float:
    """Operación con redondeo a 'digits' dígitos."""
    resultado_exacto = op(a, b)
    return redondear(resultado_exacto, digits)