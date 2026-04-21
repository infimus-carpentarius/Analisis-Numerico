#!/usr/bin/env python3
"""
Resuelve el ejercicio 7 de la sección 1.2:
Usa aritmética de redondeo de tres dígitos para calcular expresiones
y calcula errores absoluto y relativo.
Permite cambiar la precisión (número de dígitos) mediante un parámetro.
"""

import sys
import os
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ch1_preliminares.aritmetica import redondear, operar_redondeo

def mostrar_enunciado():
    print("=" * 60)
    print("Ejercicio 7 (Sección 1.2)")
    print("Use aritmética de redondeo de tres dígitos para realizar:")
    print("a) 13/14 - 6/7")
    print("b) -10π + 6e - 3/62")
    print("c) (2/9) * (9/7)")
    print("d) (√13 + √11) / (√13 - √11)")
    print("Calcule errores absoluto y relativo con valor exacto de al menos 5 dígitos.")
    print("=" * 60)

def valor_exacto_a():
    return 13/14 - 6/7

def valor_exacto_b():
    return -10 * math.pi + 6 * math.e - 3/62

def valor_exacto_c():
    return (2/9) * (9/7)

def valor_exacto_d():
    return (math.sqrt(13) + math.sqrt(11)) / (math.sqrt(13) - math.sqrt(11))

def aproximacion_redondeo_a(digits: int = 3) -> float:
    """Aproxima (13/14 - 6/7) con redondeo a 'digits' dígitos."""
    if not isinstance(digits, int) or digits <= 0:
        raise ValueError("digits debe ser entero positivo")
    # Redondeamos cada término individualmente y luego la resta
    t1 = redondear(13/14, digits)
    t2 = redondear(6/7, digits)
    return operar_redondeo(lambda x, y: x - y, t1, t2, digits)

def aproximacion_redondeo_b(digits: int = 3) -> float:
    """Aproxima -10π + 6e - 3/62 con redondeo a 'digits' dígitos."""
    if not isinstance(digits, int) or digits <= 0:
        raise ValueError("digits debe ser entero positivo")
    term1 = redondear(-10 * math.pi, digits)
    term2 = redondear(6 * math.e, digits)
    term3 = redondear(3/62, digits)
    suma1 = operar_redondeo(lambda x, y: x + y, term1, term2, digits)
    return operar_redondeo(lambda x, y: x - y, suma1, term3, digits)

def aproximacion_redondeo_c(digits: int = 3) -> float:
    """Aproxima (2/9)*(9/7) con redondeo a 'digits' dígitos."""
    if not isinstance(digits, int) or digits <= 0:
        raise ValueError("digits debe ser entero positivo")
    t1 = redondear(2/9, digits)
    t2 = redondear(9/7, digits)
    return operar_redondeo(lambda x, y: x * y, t1, t2, digits)

def aproximacion_redondeo_d(digits: int = 3) -> float:
    """Aproxima (√13+√11)/(√13-√11) con redondeo a 'digits' dígitos."""
    if not isinstance(digits, int) or digits <= 0:
        raise ValueError("digits debe ser entero positivo")
    r13 = redondear(math.sqrt(13), digits)
    r11 = redondear(math.sqrt(11), digits)
    num = operar_redondeo(lambda x, y: x + y, r13, r11, digits)
    den = operar_redondeo(lambda x, y: x - y, r13, r11, digits)
    return operar_redondeo(lambda x, y: x / y, num, den, digits)

def resolver_ejercicio7(digits: int = 3):
    casos = [
        ("a) 13/14 - 6/7", valor_exacto_a, aproximacion_redondeo_a),
        ("b) -10π + 6e - 3/62", valor_exacto_b, aproximacion_redondeo_b),
        ("c) (2/9)*(9/7)", valor_exacto_c, aproximacion_redondeo_c),
        ("d) (√13+√11)/(√13-√11)", valor_exacto_d, aproximacion_redondeo_d)
    ]
    for nombre, exacto_func, aprox_func in casos:
        exacto = exacto_func()
        aprox = aprox_func(digits)
        abs_err = abs(exacto - aprox)
        rel_err = abs_err / abs(exacto) if exacto != 0 else float('inf')
        print(f"\n{nombre}")
        print(f"  Valor exacto (10 dígitos): {exacto:.10f}")
        print(f"  Aprox. redondeo ({digits} dígitos): {aprox:.10f}")
        print(f"  Error absoluto: {abs_err:.2e}")
        print(f"  Error relativo: {rel_err:.2e}")

if __name__ == "__main__":
    mostrar_enunciado()
    digits = 3
    if len(sys.argv) > 1:
        try:
            digits = int(sys.argv[1])
        except ValueError:
            print("El argumento debe ser un entero (número de dígitos). Usando 3 por defecto.")
    resolver_ejercicio7(digits)