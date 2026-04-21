# Análisis Numérico – Proyecto modular

Este repositorio contiene implementaciones de métodos numéricos clásicos, organizados en módulos independientes. Cada módulo es un paquete Python autocontenido con su propia configuración (`pyproject.toml`), estructura `src`, pruebas unitarias y documentación. El objetivo es aprender análisis numérico mientras se practica control de versiones con Git, pruebas automatizadas con `pytest` y empaquetado moderno.

## Alcance del proyecto

El proyecto abarca desde los fundamentos del análisis numérico (errores, series de Taylor) hasta métodos avanzados para resolver ecuaciones, interpolar funciones, integrar numéricamente y aproximar derivadas. Cada módulo se desarrolla de forma independiente, permitiendo su uso por separado. Se hace hincapié en la robustez de los algoritmos, la validación de entradas, el manejo de errores numéricos y la comparación de rendimiento.

## Estructura general

La raíz del proyecto contiene únicamente archivos de configuración global (`.gitignore`, `README.md`, `LICENSE`) y una carpeta para integración continua (`.github/workflows`). Cada módulo reside en su propio subdirectorio y sigue este patrón:

- `pyproject.toml` con metadatos y dependencias.
- `src/nombre_modulo/` con el código fuente.
- `tests/` con las pruebas unitarias.
- `notebooks/` (opcional) con ejemplos y ejercicios resueltos.
- `README.md` específico del módulo.

Esta organización permite que cualquier persona pueda tomar un módulo, instalarlo de forma aislada y ejecutar sus pruebas sin necesidad del resto del proyecto.

## Cómo empezar

Clona el repositorio y accede al módulo que te interese. Por ejemplo, para el módulo de ecuaciones en una variable:

```bash
git clone https://github.com/infimus-carpentarius/analisis-numerico.git
cd analisis-numerico/Ch2-Ecuaciones-1-variable

Crea y activa un entorno virtual (opcional pero recomendado), instala el paquete en modo editable y ejecuta las pruebas:

    python -m venv venv
    source venv/bin/activate      # Linux/Mac
    # o venv\Scripts\activate en Windows
    pip install -e .
    pytest tests/ -v

Cada módulo declara sus propias dependencias en pyproject.toml, por lo que no necesitas instalar nada adicional.
Integración continua

El flujo de trabajo de GitHub Actions (.github/workflows/ci.yml) detecta automáticamente todos los subdirectorios que contienen pyproject.toml, instala cada paquete y ejecuta sus pruebas. Así se garantiza que los cambios no rompan ningún módulo.
Convenciones de código

    Las importaciones dentro de cada módulo son absolutas: from nombre_modulo.archivo import funcion.

    Las pruebas usan pytest y comparaciones numéricas con pytest.approx.

    Los commits siguen la convención semántica (feat:, fix:, test:, docs:, refactor:).

    Las ramas se nombran según la funcionalidad o el módulo, y se fusionan en main.

Documentación por módulo

Cada módulo incluye un README.md que describe sus objetivos, los métodos implementados, ejemplos de uso y, en su caso, los ejercicios resueltos. Para el módulo de ecuaciones en una variable, por ejemplo, se listan todos los métodos numéricos (bisección, Newton, secante, Müller, etc.) y se explica cómo ejecutar las pruebas.
Contribuciones
 
Las contribuciones son bienvenidas. Abre un issue o un pull request siguiendo las convenciones del proyecto. Asegúrate de que todas las pruebas pasen localmente antes de enviar los cambios.
