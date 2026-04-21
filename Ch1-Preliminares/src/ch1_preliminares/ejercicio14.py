#!/usr/bin/env python3
"""
Ejercicio 14 (sección 1.2): evaluación de f(x) = (e^x - e^{-x})/x
con aritmética de redondeo de 3 dígitos y usando polinomios de Maclaurin.
"""

import sys
import os
import math


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ch1_preliminares.aritmetica import redondear, operar_redondeo

def f_exacta(x: float) -> float:
    """Valor exacto de f(x) usando math.exp (doble precisión)."""
    return (math.exp(x) - math.exp(-x)) / x

def limite_en_cero() -> float:
    return 2.0

def f_redondeo_3_digitos(x: float) -> float:
    e_x = redondear(math.exp(x), 3)
    e_nx = redondear(math.exp(-x), 3)
    num = operar_redondeo(lambda a, b: a - b, e_x, e_nx, 3)
    return operar_redondeo(lambda a, b: a / b, num, x, 3)

def f_maclaurin_3digits(x: float) -> float:
    """
    Aproxima f(x) usando el tercer polinomio de Maclaurin:
    f(x) ≈ 2 + x^2/3, evaluado con redondeo de 3 dígitos.
    """
    # x^2
    x2 = redondear(x * x, 3)
    # x^2/3
    term = redondear(x2 / 3.0, 3)
    # Suma con 2
    return redondear(2.0 + term, 3)

def mostrar_resultados(x: float = 0.1):
    real = f_exacta(x)
    aprox_directa = f_redondeo_3_digitos(x)
    aprox_maclaurin = f_maclaurin_3digits(x)
    
    err_directa = abs(real - aprox_directa) / abs(real)
    err_maclaurin = abs(real - aprox_maclaurin) / abs(real)
    
    print(f"\n=== Ejercicio 14 (x={x}) ===")
    print(f"Valor real (alta precisión): {real:.10f}")
    print(f"Aprox. directa con 3 dígitos: {aprox_directa:.10f} -> Error relativo: {err_directa:.2e}")
    print(f"Aprox. con Maclaurin (3 dígitos): {aprox_maclaurin:.10f} -> Error relativo: {err_maclaurin:.2e}")

if __name__ == "__main__":
    x = 0.1
    if len(sys.argv) > 1:
        try:
            x = float(sys.argv[1])
        except ValueError:
            print("Argumento debe ser un número. Usando 0.1 por defecto.")
    mostrar_resultados(x)