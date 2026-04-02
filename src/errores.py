"""
Cálculo de errores absoluto y relativo para aproximaciones numéricas.
Incluye funciones para mostrar límites de la máquina y resolver los ejercicios 1 y 2 de la sección 1.2.
"""

import sys
import math
from numbers import Number

def mostrar_limites_maquina():
    """Imprime información sobre los límites de precisión de float en esta máquina."""
    print("\n=== Límites de la máquina (float de Python) ===")
    print(f"Épsilon (máquina)      : {sys.float_info.epsilon:.5e}")
    print(f"Máximo valor           : {sys.float_info.max:.5e}")
    print(f"Mínimo positivo normal : {sys.float_info.min:.5e}")
    prec = -math.log10(sys.float_info.epsilon)
    print(f"Dígitos decimales de precisión (aprox): {int(prec)}")
    print(f"Tolerancia relativa por defecto de pytest: 1e-6")
    print(f"Tolerancia absoluta por defecto de pytest: 1e-12\n")

def error_absoluto(real: float, aprox: float) -> float:
    """
    Retorna el error absoluto |real - aprox|.
    Valida que ambos argumentos sean números (no None, no NaN).
    """
    if not isinstance(real, Number) or not isinstance(aprox, Number):
        raise TypeError("Ambos argumentos deben ser números.")
    if math.isnan(real) or math.isnan(aprox):
        raise ValueError("No se puede calcular error con NaN.")
    return abs(real - aprox)

def error_relativo(real: float, aprox: float) -> float:
    """
    Retorna el error relativo |real - aprox| / |real|, suponiendo real != 0.
    Valida tipos y que real no sea cero.
    """
    if not isinstance(real, Number) or not isinstance(aprox, Number):
        raise TypeError("Ambos argumentos deben ser números.")
    if math.isnan(real) or math.isnan(aprox):
        raise ValueError("No se puede calcular error con NaN.")
    if real == 0:
        raise ValueError("El valor real no puede ser cero para error relativo.")
    return abs(real - aprox) / abs(real)

def mostrar_ejercicio1():
    """Calcula errores para el ejercicio 1 de la sección 1.2."""
    print("\n=== Ejercicio 1 ===")
    casos = [
        (math.pi, 22/7, "π ≈ 22/7"),
        (math.pi, 3.1416, "π ≈ 3.1416"),
        (math.e, 2.718, "e ≈ 2.718"),
        (math.sqrt(2), 1.414, "√2 ≈ 1.414")
    ]
    for real, aprox, desc in casos:
        abs_err = error_absoluto(real, aprox)
        rel_err = error_relativo(real, aprox)
        print(f"{desc}:")
        print(f"  Valor real = {real:.10f}")
        print(f"  Aproximación = {aprox:.10f}")
        print(f"  Error absoluto = {abs_err:.2e}")
        print(f"  Error relativo = {rel_err:.2e}\n")

def mostrar_ejercicio2():
    """Calcula errores para el ejercicio 2 de la sección 1.2."""
    print("\n=== Ejercicio 2 ===")
    # Definimos los valores exactos con alta precisión
    e10 = math.exp(10)                # e^10
    pi10 = 10**math.pi                # 10^π
    fact8 = math.factorial(8)         # 8!
    fact9 = math.factorial(9)         # 9!
    # Aproximaciones dadas
    aprox_e10 = 22000.0
    aprox_pi10 = 1400.0
    aprox_fact8 = 39900.0
    # Stirling para 9! : √(18π) (9/e)^9
    stirling_9 = math.sqrt(18 * math.pi) * (9 / math.e)**9

    casos = [
        (e10, aprox_e10, "e^10 ≈ 22000"),
        (pi10, aprox_pi10, "10^π ≈ 1400"),
        (fact8, aprox_fact8, "8! ≈ 39900"),
        (fact9, stirling_9, "9! ≈ √(18π)(9/e)^9 (Stirling)")
    ]

    for real, aprox, desc in casos:
        abs_err = error_absoluto(real, aprox)
        rel_err = error_relativo(real, aprox)
        print(f"{desc}:")
        print(f"  Valor real = {real:.10f}")
        print(f"  Aproximación = {aprox:.10f}")
        print(f"  Error absoluto = {abs_err:.2e}")
        print(f"  Error relativo = {rel_err:.2e}\n")

if __name__ == "__main__":
    mostrar_limites_maquina()
    mostrar_ejercicio1()
    mostrar_ejercicio2()