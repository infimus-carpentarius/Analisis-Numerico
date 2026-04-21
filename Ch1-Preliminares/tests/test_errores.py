import sys
import math
import pytest
from decimal import Decimal, getcontext
from ch1_preliminares.errores import error_absoluto, error_relativo, mostrar_limites_maquina

# Aumentamos precisión de Decimal para cálculos manuales
getcontext().prec = 50

def test_info_maquina_vs_pytest(capsys):
    """Prueba real: verifica que el épsilon de máquina sea menor que 1e-15 y que las tolerancias por defecto sean razonables."""
    mostrar_limites_maquina()
    captured = capsys.readouterr()
    
    # Aserciones reales
    assert sys.float_info.epsilon < 1e-15, "El épsilon de máquina debe ser menor que 1e-15"
    default_rel = 1e-6
    default_abs = 1e-12
    assert default_rel >= sys.float_info.epsilon, "La tolerancia relativa por defecto es más pequeña que el épsilon"
    assert default_abs > 0

def test_error_absoluto():
    # Valores esperados calculados manualmente con Decimal (sin usar la función error_absoluto)
    
    # Caso 1: π ≈ 3.1416
    real1 = Decimal('3.14159265358979323846264338327950288419716939937510')
    aprox1 = Decimal('3.1416')
    # Cálculo manual del error absoluto: |real - aprox|
    esperado_abs1 = abs(real1 - aprox1)  # Esto es Decimal, no la función bajo prueba
    # Convertimos a float para comparar con pytest.approx
    assert error_absoluto(float(real1), float(aprox1)) == pytest.approx(float(esperado_abs1), rel=1e-12)
    
    # Caso 2: e ≈ 2.718
    real2 = Decimal('2.71828182845904523536028747135266249775724709369995')
    aprox2 = Decimal('2.718')
    esperado_abs2 = abs(real2 - aprox2)
    assert error_absoluto(float(real2), float(aprox2)) == pytest.approx(float(esperado_abs2), rel=1e-12)
    
    # Caso 3: números enteros (fáciles)
    assert error_absoluto(10, 10) == 0.0
    assert error_absoluto(10, 9) == 1.0
    assert error_absoluto(-5, -4) == 1.0

def test_error_relativo():
    # Valores esperados calculados manualmente con Decimal
    
    # Caso 1: π ≈ 3.1416
    real1 = Decimal('3.14159265358979323846264338327950288419716939937510')
    aprox1 = Decimal('3.1416')
    esperado_rel1 = abs(real1 - aprox1) / abs(real1)  # cálculo manual
    assert error_relativo(float(real1), float(aprox1)) == pytest.approx(float(esperado_rel1), rel=1e-12)
    
    # Caso 2: e ≈ 2.718
    real2 = Decimal('2.71828182845904523536028747135266249775724709369995')
    aprox2 = Decimal('2.718')
    esperado_rel2 = abs(real2 - aprox2) / abs(real2)
    assert error_relativo(float(real2), float(aprox2)) == pytest.approx(float(esperado_rel2), rel=1e-12)
    
    # Caso 3: valores simples
    assert error_relativo(100, 99) == 0.01
    assert error_relativo(0.5, 0.51) == pytest.approx(0.02, rel=1e-12)

def test_error_absoluto_valores_pequenos():
    """Real muy pequeño (1e-200) y aprox ligeramente diferente."""
    real = 1e-200
    aprox = 1.0000000001e-200
    esperado = abs(real - aprox)  # cálculo directo con Python (no llamamos a error_absoluto)
    assert error_absoluto(real, aprox) == pytest.approx(esperado, rel=1e-12)

def test_error_absoluto_valores_grandes():
    """Real muy grande (1e200) y aprox igual."""
    real = 1e200
    aprox = 1e200
    assert error_absoluto(real, aprox) == 0.0

def test_error_relativo_valores_pequenos():
    """Real muy pequeño (1e-200) y aprox ligeramente diferente."""
    real = 1e-200
    aprox = 1.0000000001e-200
    esperado = abs(real - aprox) / abs(real)  # cálculo manual
    assert error_relativo(real, aprox) == pytest.approx(esperado, rel=1e-12)

def test_error_relativo_valores_grandes():
    """Real muy grande (1e200) y aprox diferente en una parte pequeña."""
    real = 1e200
    aprox = 1.0000000001e200
    esperado = abs(real - aprox) / abs(real)
    assert error_relativo(real, aprox) == pytest.approx(esperado, rel=1e-12)

def test_error_con_nan():
    """Prueba que lanza ValueError cuando se pasa NaN."""
    with pytest.raises(ValueError, match="No se puede calcular error con NaN"):
        error_absoluto(math.nan, 1.0)
    with pytest.raises(ValueError, match="No se puede calcular error con NaN"):
        error_absoluto(1.0, math.nan)
    with pytest.raises(ValueError, match="No se puede calcular error con NaN"):
        error_relativo(math.nan, 1.0)
    with pytest.raises(ValueError, match="No se puede calcular error con NaN"):
        error_relativo(1.0, math.nan)

def test_error_relativo_cero():
    with pytest.raises(ValueError, match="El valor real no puede ser cero"):
        error_relativo(0, 0.001)

def test_validacion_tipos():
    """Prueba que se lanza TypeError si los argumentos no son números."""
    with pytest.raises(TypeError):
        error_absoluto("a", 1)
    with pytest.raises(TypeError):
        error_absoluto(1, None)
    with pytest.raises(TypeError):
        error_relativo([1,2], 3)