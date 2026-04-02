import sys
import math
import pytest
from src.errores import error_absoluto, error_relativo, mostrar_limites_maquina

def test_info_maquina_vs_pytest(capsys):
    """Muestra los límites de la máquina y compara con las tolerancias por defecto de pytest."""
    mostrar_limites_maquina()
    captured = capsys.readouterr()
    print(captured.out)  # para que pytest muestre la información con -s

    default_rel = 1e-6
    default_abs = 1e-12

    print(f"\nPrecisión decimal de la máquina: {-math.log10(sys.float_info.epsilon):.1f} dígitos")
    print(f"Tolerancia relativa pytest: {default_rel:.1e}")
    print(f"Tolerancia absoluta pytest: {default_abs:.1e}")

    if default_rel < sys.float_info.epsilon:
        print("⚠️ ADVERTENCIA: La tolerancia relativa de pytest es más pequeña que el épsilon de máquina.")
    if default_abs < sys.float_info.epsilon * 1e-2:
        print("⚠️ ADVERTENCIA: La tolerancia absoluta de pytest es extremadamente pequeña.")
    # No fallamos la prueba, solo mostramos información.

def test_error_absoluto():
    tol_rel = 10 * sys.float_info.epsilon  # factor de seguridad

    real1, aprox1 = 3.141592653589793, 3.1416
    esperado_abs1 = error_absoluto(real1, aprox1)
    assert error_absoluto(real1, aprox1) == pytest.approx(esperado_abs1, rel=tol_rel)

    real2, aprox2 = 2.718281828459045, 2.718
    esperado_abs2 = error_absoluto(real2, aprox2)
    assert error_absoluto(real2, aprox2) == pytest.approx(esperado_abs2, rel=tol_rel)

def test_error_relativo():
    tol_rel = 10 * sys.float_info.epsilon

    real1, aprox1 = 3.141592653589793, 3.1416
    esperado_rel1 = error_relativo(real1, aprox1)
    assert error_relativo(real1, aprox1) == pytest.approx(esperado_rel1, rel=tol_rel)

    real2, aprox2 = 2.718281828459045, 2.718
    esperado_rel2 = error_relativo(real2, aprox2)
    assert error_relativo(real2, aprox2) == pytest.approx(esperado_rel2, rel=tol_rel)

def test_error_relativo_cero():
    with pytest.raises(ValueError):
        error_relativo(0, 0.001)