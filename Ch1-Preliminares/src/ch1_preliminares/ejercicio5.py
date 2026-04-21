#!/usr/bin/env python3
"""
Resuelve el ejercicio 5 de la sección 1.2:
Realiza operaciones con aritmética de corte y redondeo de dígitos finitos.
Permite cambiar la precisión (número de dígitos) mediante un parámetro.
"""

import sys
import os
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ch1_preliminares.aritmetica import truncar, redondear, operar_corte, operar_redondeo
from ch1_preliminares.errores import error_relativo

def mostrar_enunciado():
    print("=" * 60)
    print("Ejercicio 5 (Sección 1.2)")
    print("Realice los siguientes cálculos:")
    print("a) 4/5 + 1/3")
    print("b) 4/5 * 1/3")
    print("c) (1/3 - 1/11) + 3/20")
    print("d) (1/3 + 3/11) - 3/20")
    print("Para cada uno: i) exacto, ii) corte de 3 dígitos, iii) redondeo de 3 dígitos,")
    print("   iv) errores relativos en ii) y iii).")
    print("=" * 60)

def valor_exacto_a():
    return 4/5 + 1/3

def valor_exacto_b():
    return 4/5 * 1/3

def valor_exacto_c():
    return (1/3 - 1/11) + 3/20

def valor_exacto_d():
    return (1/3 + 3/11) - 3/20

# ------------------------------------------------------------
# Aproximaciones con corte
# ------------------------------------------------------------
def aproximacion_corte_a(digits: int = 3) -> float:
    if not isinstance(digits, int) or digits <= 0:
        raise ValueError("digits debe ser entero positivo")
    t1 = truncar(4/5, digits)
    t2 = truncar(1/3, digits)
    return operar_corte(lambda x, y: x + y, t1, t2, digits)

def aproximacion_corte_b(digits: int = 3) -> float:
    if not isinstance(digits, int) or digits <= 0:
        raise ValueError("digits debe ser entero positivo")
    t1 = truncar(4/5, digits)
    t2 = truncar(1/3, digits)
    return operar_corte(lambda x, y: x * y, t1, t2, digits)

def aproximacion_corte_c(digits: int = 3) -> float:
    if not isinstance(digits, int) or digits <= 0:
        raise ValueError("digits debe ser entero positivo")
    t1 = truncar(1/3, digits)
    t2 = truncar(1/11, digits)
    resta = operar_corte(lambda x, y: x - y, t1, t2, digits)
    t3 = truncar(3/20, digits)
    return operar_corte(lambda x, y: x + y, resta, t3, digits)

def aproximacion_corte_d(digits: int = 3) -> float:
    if not isinstance(digits, int) or digits <= 0:
        raise ValueError("digits debe ser entero positivo")
    t1 = truncar(1/3, digits)
    t2 = truncar(3/11, digits)
    suma = operar_corte(lambda x, y: x + y, t1, t2, digits)
    t3 = truncar(3/20, digits)
    return operar_corte(lambda x, y: x - y, suma, t3, digits)

# ------------------------------------------------------------
# Aproximaciones con redondeo
# ------------------------------------------------------------
def aproximacion_redondeo_a(digits: int = 3) -> float:
    if not isinstance(digits, int) or digits <= 0:
        raise ValueError("digits debe ser entero positivo")
    t1 = redondear(4/5, digits)
    t2 = redondear(1/3, digits)
    return operar_redondeo(lambda x, y: x + y, t1, t2, digits)

def aproximacion_redondeo_b(digits: int = 3) -> float:
    if not isinstance(digits, int) or digits <= 0:
        raise ValueError("digits debe ser entero positivo")
    t1 = redondear(4/5, digits)
    t2 = redondear(1/3, digits)
    return operar_redondeo(lambda x, y: x * y, t1, t2, digits)

def aproximacion_redondeo_c(digits: int = 3) -> float:
    if not isinstance(digits, int) or digits <= 0:
        raise ValueError("digits debe ser entero positivo")
    t1 = redondear(1/3, digits)
    t2 = redondear(1/11, digits)
    resta = operar_redondeo(lambda x, y: x - y, t1, t2, digits)
    t3 = redondear(3/20, digits)
    return operar_redondeo(lambda x, y: x + y, resta, t3, digits)

def aproximacion_redondeo_d(digits: int = 3) -> float:
    if not isinstance(digits, int) or digits <= 0:
        raise ValueError("digits debe ser entero positivo")
    t1 = redondear(1/3, digits)
    t2 = redondear(3/11, digits)
    suma = operar_redondeo(lambda x, y: x + y, t1, t2, digits)
    t3 = redondear(3/20, digits)
    return operar_redondeo(lambda x, y: x - y, suma, t3, digits)

# ------------------------------------------------------------
# Función principal que muestra resultados
# ------------------------------------------------------------
def resolver_ejercicio5(digits: int = 3):
    casos = [
        ("a) 4/5 + 1/3", valor_exacto_a, aproximacion_corte_a, aproximacion_redondeo_a),
        ("b) 4/5 * 1/3", valor_exacto_b, aproximacion_corte_b, aproximacion_redondeo_b),
        ("c) (1/3-1/11)+3/20", valor_exacto_c, aproximacion_corte_c, aproximacion_redondeo_c),
        ("d) (1/3+3/11)-3/20", valor_exacto_d, aproximacion_corte_d, aproximacion_redondeo_d),
    ]
    for nombre, exacto_func, corte_func, redondeo_func in casos:
        exacto = exacto_func()
        corte = corte_func(digits)
        redon = redondeo_func(digits)
        err_corte = error_relativo(exacto, corte)
        err_redon = error_relativo(exacto, redon)
        print(f"\n{nombre}")
        print(f"  Exacto: {exacto:.10f}")
        print(f"  Corte ({digits} dígitos): {corte:.10f}  -> Error relativo: {err_corte:.2e}")
        print(f"  Redondeo ({digits} dígitos): {redon:.10f} -> Error relativo: {err_redon:.2e}")

if __name__ == "__main__":
    mostrar_enunciado()
    digits = 3
    if len(sys.argv) > 1:
        try:
            digits = int(sys.argv[1])
        except ValueError:
            print("El argumento debe ser un entero (número de dígitos). Usando 3 por defecto.")
    resolver_ejercicio5(digits)