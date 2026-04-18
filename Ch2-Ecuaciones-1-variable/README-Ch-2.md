# Resumen del Capítulo 2 – Soluciones de ecuaciones en una variable

En este capítulo se han implementado y probado los principales métodos numéricos para encontrar raíces de ecuaciones de la forma f(x)=0. Se ha prestado especial atención a la robustez, la validación de entradas, el manejo de errores numéricos y la comparación de rendimiento.

## Métodos implementados

| Método | Descripción | Características |
|--------|-------------|------------------|
| Bisección | Búsqueda por reducción del intervalo | Convergencia lineal, robusto, garantiza encierro de la raíz. |
| Punto fijo | Iteración x_{n+1}=g(x_n) | Convergencia lineal bajo condiciones de contractividad. |
| Newton‑Raphson | x_{n+1}=x_n - f(x_n)/f'(x_n) | Convergencia cuadrática local, requiere derivada. |
| Secante | Aproximación de la derivada por diferencias | Orden de convergencia ≈1.618, sin derivada. |
| Posición falsa | Variante de la secante que mantiene el encierro | Más lento pero seguro, evita divergencia. |
| Newton modificado | x_{n+1}=x_n - m*f(x_n)/f'(x_n) | Restaura convergencia cuadrática en raíces múltiples. |
| Aitken Δ² | Aceleración de sucesiones linealmente convergentes | Convierte convergencia lineal en cuadrática. |
| Steffensen | Punto fijo acelerado con Aitken | No requiere derivadas, convergencia cuadrática. |
| Horner | Evaluación eficiente de polinomios y derivadas | Base para métodos en polinomios (Newton, Müller). |
| Müller | Interpolación cuadrática | Encuentra raíces reales y complejas, orden ≈1.84. |

## Herramientas de validación

- Funciones auxiliares robustas:
  - evaluar_seguro(): captura excepciones, convierte tipos, detecta inf/nan.
  - signos_opuestos(): evita multiplicaciones peligrosas.
  - verificar_criterios_parada(): unifica tolerancias absoluta, relativa y residuo.

- Pruebas unitarias (pytest):
  - Cobertura de casos normales, límite y errores.
  - Comparaciones con pytest.approx para tolerancias numéricas.
  - Verificación de convergencia, orden y estabilidad.
  - Tests específicos para cada método y para horner_coeficientes_complejos.


## Estructura del proyecto

Ch2-Ecuaciones-1-variable/
├── src/
│   ├── root_finding.py      # todos los métodos numéricos
│   └── utilities.py         # funciones auxiliares
├── tests/
│   ├── test_root_finding.py
│   ├── test_utilities.py
│   ├── test_steffensen.py
│   ├── test_muller_polinomio.py
│   └── test_horner_coeficientes_complejos.py
├── notebooks/               # cuadernos con ejercicios resueltos
└── README.md

## Ejercicios resueltos

Se han resuelto y documentado los siguientes problemas del libro de Burden‑Faires (capítulo 2):

- Sección 2.1 – Bisección
- Sección 2.2 – Punto fijo
- Sección 2.3 – Newton, secante, posición falsa
- Sección 2.4 – Análisis de error y Newton modificado
- Sección 2.5 – Aceleración de la convergencia
- Sección 2.6 – Polinomios y Müller

Cada solución incluye código ejecutable, gráficas ilustrativas y comparativa de métodos.


## Conclusiones y buenas prácticas

- Siempre verificar las condiciones de convergencia (teorema de Bolzano, contractividad, derivada no nula).
- Usar criterios de parada combinados (absoluto + relativo + residuo) para adaptarse a diferentes escalas.
- Aprovechar la aceleración de Aitken/Steffensen para sucesiones linealmente convergentes.
- Para polinomios, emplear Horner en evaluaciones y deflación para obtener todas las raíces.
- El método de Müller es la mejor opción cuando se requieren raíces complejas sin derivadas.
- Documentar y probar cada función con casos realistas y patológicos.

Este resumen refleja el trabajo realizado en el capítulo 2. Todo el código está disponible en el repositorio y puede ejecutarse siguiendo las instrucciones del README.md principal.
