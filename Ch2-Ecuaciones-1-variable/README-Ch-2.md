# Capítulo 2 – Soluciones de ecuaciones en una variable

Este capítulo implementa los principales métodos numéricos para encontrar raíces de ecuaciones de la forma f(x)=0. Se ha puesto énfasis en robustez, manejo de errores, pruebas automatizadas y comparación de rendimiento.

## Instalación y entorno

El proyecto usa Conda para gestionar el entorno. Los pasos son:

> conda env create -f environment.yml
> conda activate jnotebook
> pip install -e .

Si prefieres usar pip y venv (alternativa):
> python -m venv venv
> source venv/bin/activate (Linux/Mac) o venv\Scripts\activate (Windows)
> pip install -e .

## Ejecutar las pruebas unitarias

Una vez activado el entorno, ejecuta:
> pytest tests/ -v

Para cobertura:
> pytest --cov=ch2_ecuaciones tests/

## Explorar los cuadernos con Jupyter Lab

Para iniciar Jupyter Lab (ya instalado en el entorno Conda):
> jupyter lab 

Si usaste pip, instala jupyterlab con:
> pip install jupyterlab

## Métodos implementados

- Bisección (biseccion)
- Punto fijo (punto_fijo)
- Newton-Raphson (newton)
- Secante (secante)
- Posición falsa (posicion_falsa)
- Newton modificado para raíces múltiples (newton_modificado)
- Aceleración de Aitken (aitken)
- Steffensen (steffensen)
- Horner (reales y complejos) (horner_coeficientes_reales, horner_coeficientes_complejos)
- Müller (muller_polinomio)

## Uso básico

Ejemplo con Newton:
> from ch2_ecuaciones.root_finding import newton
> def f(x): return x**2 - 2
> def df(x): return 2*x
> raiz, _, _ = newton(f, df, 1.5, tol_abs=1e-8)
> print(raiz)  # 1.4142135623730951

## Ejercicios resueltos

Los cuadernos en la carpeta notebooks/ contienen la resolución de los ejercicios del capítulo 2 del libro de Burden-Faires (secciones 2.1 a 2.6). Incluyen gráficas, comparativas de métodos y análisis de convergencia.

## Contribuciones

Las contribuciones son bienvenidas. Abre un pull request siguiendo las convenciones del proyecto (importaciones absolutas, pruebas con pytest, commits semánticos).

