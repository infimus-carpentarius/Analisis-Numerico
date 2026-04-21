#!/usr/bin/env python3
"""
Funciones para simular aritmética de punto flotante con un número fijo de dígitos significativos.
Soporta corte y redondeo.
"""

import math
import struct

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
##############################################################################
#utilidades para el manejo de cadenas de bits que representan numeros reales.
##############################################################################
def ieee754_binary_to_float(binary_str: str) -> float:
    """
    Convierte una cadena binaria de 64 bits (formato IEEE 754 doble precisión)
    a su valor decimal.
    La cadena debe tener exactamente 64 caracteres (0/1).
    Formato: [1 bit signo][11 bits exponente][52 bits mantisa]
    """
    if len(binary_str) != 64:
        raise ValueError("La cadena binaria debe tener 64 bits")
    sign = int(binary_str[0], 2)
    exponent_bits = binary_str[1:12]
    fraction_bits = binary_str[12:]

    exp = int(exponent_bits, 2)
    fraction = 0.0
    for i, bit in enumerate(fraction_bits):
        if bit == '1':
            fraction += 2.0 ** (-(i+1))

    # Casos especiales
    if exp == 0:
        # Subnormal o cero
        if fraction == 0.0:
            return -0.0 if sign else 0.0
        else:
            # Subnormal: exponente = -1022, sin el 1 implícito
            value = fraction * (2.0 ** (-1022))
            return -value if sign else value
    elif exp == 2047:
        # Infinito o NaN
        if fraction == 0.0:
            return float('-inf') if sign else float('inf')
        else:
            return float('nan')
    else:
        # Normalizado: se añade el 1 implícito
        mantissa = 1.0 + fraction
        value = mantissa * (2.0 ** (exp - 1023))
        return -value if sign else value
    


def float_to_ieee754_binary(f: float) -> str:
    """
    Convierte un número float (doble precisión) a su representación binaria de 64 bits.
    """
    # Empaquetar el float como 8 bytes en orden little-endian (nativo)
    # Usar '>d' para big-endian (estándar de red) pero cuidado con el orden.
    # El estándar IEEE 754 define el bit más significativo primero, pero en memoria puede variar.
    # Usamos `struct.pack('>d', f)` para big-endian, que es el orden de bits usual en representación.
    # Luego convertimos cada byte a binario.
    try:
        packed = struct.pack('>d', f)
    except OverflowError:
        # Manejar inf o nan
        if math.isinf(f):
            if f > 0:
                return "0" + "11111111111" + "0" * 52
            else:
                return "1" + "11111111111" + "0" * 52
        elif math.isnan(f):
            # Cualquier NaN: signo 0, exponente 2047, fracción != 0
            return "0" + "11111111111" + "1" + "0" * 51
        else:
            raise
    bits = ''.join(f'{byte:08b}' for byte in packed)
    return bits

def next_float(f: float) -> float:
    """Siguiente número de máquina mayor que f."""
    return math.nextafter(f, math.inf)

def prev_float(f: float) -> float:
    """Número de máquina inmediatamente menor que f."""
    return math.nextafter(f, -math.inf)