# Cálculo de errores absoluto y relativo
Estos archvivos resuelven algunos problemas del  capitulo uno y se crean test unitarios. 
Al ser capitulo de fundamentos, solo se ve todo de forma general. En los siguientes capitulos se trabajara con mas rigurosidad. 


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
