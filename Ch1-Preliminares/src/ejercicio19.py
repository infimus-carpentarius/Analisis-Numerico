#!/usr/bin/env python3
"""
Ejercicio 19 (sección 1.2): Convertir números de máquina IEEE 754 (64 bits)
a su equivalente decimal.
"""

import sys
import os
import math

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.aritmetica import ieee754_binary_to_float

def mostrar_conversion(binario: str, desc: str):
    try:
        valor = ieee754_binary_to_float(binario)
        print(f"{desc}: {binario} -> {valor}")
    except Exception as e:
        print(f"{desc}: Error - {e}")

def main():
    # Los strings del ejercicio (se ajustan a 64 bits; algunos tenían espacios o longitudes mayores)
    # Según el PDF, las cadenas tienen 64 bits. Las copio exactamente.
    casos = {
        "a": "0100000010101001001100000000000000000000000000000000000000000000",
        "b": "1100000010101001001100000000000000000000000000000000000000000000",
        "c": "0011111111110101001100000000000000000000000000000000000000000000",
        "d": "0011111111110101001100000000000000000000000000000000000000000000"
    }
    print("=== Ejercicio 19: Conversión de números de máquina IEEE 754 ===")
    for key, bits in casos.items():
        mostrar_conversion(bits, f"Caso {key}")

if __name__ == "__main__":
    main()