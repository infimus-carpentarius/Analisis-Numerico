#!/usr/bin/env python3
"""
Extensión del ejercicio 19: análisis de precisión y números vecinos.
Muestra cada número en: binario, valor decimal, notación científica y formato normal.
El formato normal usa relleno con ceros marrones para indicar límites de precisión.
"""

import sys
import os
import random
import math

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.aritmetica import float_to_ieee754_binary, next_float, prev_float

# Color marrón ANSI
BROWN = "\033[38;5;130m"
RESET = "\033[0m"

def formato_cientifico(valor: float) -> str:
    """Notación científica estándar con 15 dígitos significativos (sin relleno)."""
    return f"{valor:.15e}"

def formato_normal_fijo(valor: float, ancho: int = 30) -> str:
    """Representación decimal normal (parte entera + 15 decimales) con ancho fijo.
    Los dígitos que exceden la precisión real se rellenan con ceros marrones."""
    try:
        s = f"{valor:.15f}"
    except OverflowError:
        s = f"{valor:.15e}"
    if len(s) > ancho:
        s = s[:ancho]
    if len(s) < ancho:
        s = s + BROWN + "0" * (ancho - len(s)) + RESET
    return s

def analizar_numero(f: float, nombre: str):
    print(f"\n--- {nombre} ---")
    bin_repr = float_to_ieee754_binary(f)
    print(f"Binario IEEE 754: {bin_repr} (64 bits)")
    print(f"Valor decimal: {repr(f)}")
    print(f"Notación científica: {formato_cientifico(f)}")
    print(f"Formato normal     : {formato_normal_fijo(f)}")

    if math.isinf(f) or math.isnan(f):
        print("No se pueden calcular vecinos.")
        return

    try:
        prev = prev_float(f)
        nxt = next_float(f)
    except OverflowError:
        print("Desbordamiento al calcular vecinos.")
        return

    print("\n--- Número anterior ---")
    print(f"Binario IEEE 754: {float_to_ieee754_binary(prev)} (64 bits)")
    print(f"Valor decimal: {repr(prev)}")
    print(f"Notación científica: {formato_cientifico(prev)}")
    print(f"Formato normal     : {formato_normal_fijo(prev)}")

    print("\n--- Número posterior ---")
    print(f"Binario IEEE 754: {float_to_ieee754_binary(nxt)} (64 bits)")
    print(f"Valor decimal: {repr(nxt)}")
    print(f"Notación científica: {formato_cientifico(nxt)}")
    print(f"Formato normal     : {formato_normal_fijo(nxt)}")

    intervalo = nxt - prev
    eps_rel = intervalo / abs(f) if f != 0 else float('inf')
    print(f"\nTamaño del intervalo entre anterior y posterior: {intervalo:.5e}")
    print(f"Épsilon relativo (tamaño/|f|): {eps_rel:.5e}")

def generar_numero_aleatorio_normalizado():
    while True:
        sign = random.choice([-1, 1])
        exp = random.randint(-1022, 1023)
        mantissa = 1.0 + random.random()
        value = sign * mantissa * (2.0 ** exp)
        if math.isfinite(value) and abs(value) >= 2.0**-1022:
            return value

def main():
    random.seed(42)
    num_medio = generar_numero_aleatorio_normalizado()
    analizar_numero(num_medio, "Número aleatorio medio")

    num_pequeno = 1.0e-300
    analizar_numero(num_pequeno, "Número muy pequeño")

    num_grande = 1.0e300
    analizar_numero(num_grande, "Número muy grande")

    num_cerca_uno = 1.0 + random.random() * 1e-10
    analizar_numero(num_cerca_uno, "Número cercano a 1")

if __name__ == "__main__":
    main()