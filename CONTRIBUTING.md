# 🤝 Guía para Contribuir

¡Gracias por tu interés en contribuir a **Análisis Numérico**! Esta guía te explica cómo hacerlo de forma correcta y profesional.

---

2️⃣ Crea una rama para tu característica
bash

# Actualiza tu rama principal
git fetch upstream
git checkout Principal
git merge upstream/Principal

# Crea una nueva rama
git checkout -b feature/nombre-descriptivo

# Ejemplos de buenos nombres:
# - feature/interpolacion-lagrange
# - fix/error-calculo-derivada
# - docs/mejorar-readme
# - test/cobertura-modulo-ecuaciones

3️⃣ Realiza tus cambios

    📁 Modifica los archivos necesarios
    ✍️ Crea/actualiza tests en tests/
    📚 Actualiza documentación si es necesario

4️⃣ Sincroniza y prepara el commit
bash

# Verifica que todo está actualizado
git fetch upstream

# Asegúrate de que tu rama está al día
git rebase upstream/Principal

# Prepara tus cambios
git add .

# Revisa qué vas a commitear
git diff --cached

🔐 Configurar Commits Firmados (GPG)

Los commits firmados acreditan tu autoría y aumentan la seguridad del proyecto. Es obligatorio para contribuyentes.
Windows (Git Bash o WSL)
bash

# 1. Instalar GPG
# Si usas Chocolatey:
choco install gnupg

# Si usas WSL, apt-get:
sudo apt-get install gnupg

# 2. Generar tu clave GPG
gpg --full-generate-key

# Responde:
# - Tipo de clave: RSA (opción 1)
# - Tamaño: 4096
# - Validez: 2 años o más (opción 2)
# - Nombre: Tu nombre completo
# - Email: Tu email de GitHub
# - Comentario: (dejar en blanco)

# 3. Obtén tu ID de clave
gpg --list-secret-keys --keyid-format=long

# Output similar a:
# sec   rsa4096/1234567890ABCDEF 2026-04-21 [SC]
#       Tu nombre <tu@email.com>

# ⭐ Copia: 1234567890ABCDEF

# 4. Exporta tu clave pública
gpg --armor --export 1234567890ABCDEF

# Copia TODO (desde -----BEGIN hasta -----END)

Mac/Linux
bash

# 1. Verificar que GPG está instalado
which gpg

# Si no: brew install gnupg (Mac) o sudo apt-get install gnupg (Linux)

# 2-4. Igual que Windows
gpg --full-generate-key
gpg --list-secret-keys --keyid-format=long
gpg --armor --export TU_KEY_ID

Agregar clave a GitHub

    Ve a GitHub → Configuración → SSH and GPG keys
    Click en New GPG key
    Pega toda tu clave pública (desde BEGIN hasta END)
    Click en Add GPG key

Configurar Git
bash

# Reemplaza 1234567890ABCDEF con tu Key ID
git config --global user.signingKey 1234567890ABCDEF

# Habilita firma automática de commits
git config --global commit.gpgSign true

# Verifica que esté configurado
git config --global --list | grep sign

✍️ Convenciones de Código
Commits semánticos

Usa este formato para mensajes de commit:
Code

<tipo>(<ámbito>): <descripción>

<cuerpo opcional>

<pie opcional>

Tipos válidos:

    feat: Nueva característica
    fix: Corrección de bug
    test: Agregar o mejorar tests
    docs: Cambios en documentación
    refactor: Cambio de código sin alterar función
    perf: Mejora de rendimiento
    chore: Cambios en build, CI, dependencias

Ejemplos:
bash

# ✅ Bien
git commit -m "feat(ecuaciones): agregar método de Newton-Raphson"
git commit -m "fix(preliminares): corregir cálculo de error relativo"
git commit -m "test(integracion): aumentar cobertura a 95%"
git commit -m "docs: actualizar guía de contribución"

# ❌ Evita
git commit -m "cambios"
git commit -m "arreglé cosas"
git commit -m "update"

Estilo de código

    ✅ Sigue PEP 8 (Python)
    ✅ Usa nombres descriptivos para funciones y variables
    ✅ Comenta código complejo
    ✅ Usa type hints cuando sea posible

Python

# ✅ Bien
def calcular_error_relativo(valor_aproximado: float, valor_exacto: float) -> float:
    """Calcula el error relativo entre dos valores."""
    if valor_exacto == 0:
        raise ValueError("El valor exacto no puede ser cero")
    return abs(valor_aproximado - valor_exacto) / abs(valor_exacto)

# ❌ Evita
def error(a, b):
    return abs(a - b) / abs(b)

Tests

    📝 Escribe tests para toda nueva funcionalidad
    🎯 Usa pytest y pytest.approx para comparaciones numéricas
    📊 Mantén cobertura >= 85%

Python

import pytest
from nombre_modulo.archivo import calcular_error_relativo

def test_calcular_error_relativo():
    """Prueba cálculo de error relativo."""
    resultado = calcular_error_relativo(1.999, 2.0)
    esperado = 0.0005
    assert resultado == pytest.approx(esperado, rel=1e-4)

def test_error_relativo_valor_exacto_cero():
    """Verifica que lanza error si valor exacto es cero."""
    with pytest.raises(ValueError):
        calcular_error_relativo(1.0, 0.0)

🔀 Proceso de Pull Request
1️⃣ Antes de hacer push
bash

# Verifica que los tests pasen localmente
pytest tests/ -v

# Asegúrate de que la cobertura sea suficiente
pytest --cov=nombre_modulo tests/

2️⃣ Push a tu fork
bash

git push origin feature/nombre-descriptivo

3️⃣ Abre un Pull Request

    Ve a tu fork en GitHub
    Click en "Compare & pull request"
    Asegúrate que:
        Base: infimus-carpentarius/Analisis-Numerico → Principal
        Compare: TU_USUARIO/Analisis-Numerico → feature/tu-rama

4️⃣ Completa la descripción del PR
Markdown

## Descripción
Breve explicación de qué cambios haces y por qué.

## Tipo de cambio
- [ ] Nueva característica
- [ ] Corrección de bug
- [ ] Cambio de documentación
- [ ] Cambio que rompe backward compatibility

## ¿Cómo se ha testeado?
Describe los tests que ejecutaste.

## Checklist
- [ ] Mi código sigue las convenciones del proyecto
- [ ] He actualizado la documentación si es necesario
- [ ] He ejecutado `pytest` y todos los tests pasan
- [ ] Mi commits están firmados con GPG
- [ ] No hay cambios no relacionados en este PR

## Screenshots (si aplica)
Incluye gráficos o demostraciones si corresponde.

5️⃣ Espera revisión

    ✅ Se ejecutan automáticamente los tests (CI with Conda)
    ✅ Se revisará tu código
    ✅ Posibles cambios solicitados (no te preocupes, es normal)

6️⃣ Resuelve comentarios

Si hay cambios solicitados:
bash

# Haz los cambios
git add .
git commit -m "fix: dirección del PR basada en comentarios"
git push origin feature/nombre-descriptivo

# El PR se actualiza automáticamente

🔧 Resolver Conflictos

Si tu PR tiene conflictos con Principal:
bash

# 1. Actualiza tu rama local
git fetch upstream
git rebase upstream/Principal

# 2. Git te mostrará conflictos. Edita los archivos:
# Busca marcadores como:
# <<<<<<< HEAD
# tu código
# =======
# código de upstream
# >>>>>>> upstream/Principal

# 3. Resuelve los conflictos manualmente

# 4. Marca como resuelto
git add .

# 5. Continúa el rebase
git rebase --continue

# 6. Push forzado (solo en tu rama personal)
git push origin feature/nombre-descriptivo --force-with-lease

📞 ¿Preguntas o problemas?

    📝 Abre una issue si encuentras un bug
    💬 Discute cambios importantes antes de hacer un PR
    🐛 Sé específico en la descripción de problemas

🎓 Recursos útiles

    Guía oficial de Git
    Commits convencionales
    PEP 8 Style Guide
    Pytest documentation

✨ ¡Gracias por contribuir!

Tu trabajo es valorado y tu nombre aparecerá en el historial del proyecto. 🙌
Code


---

### ¿Cómo usarlo?

Tienes dos opciones:

**Opción 1:** Copia el bloque de código completo de arriba (está presentado de forma continua sin fragmentación)

**Opción 2:** Si quieres descargarlo, puedo crear un archivo `.txt` con el contenido puro para que lo descargues y renombres a `CONTRIBUTING.md`

¿Cuál prefieres? 📥

You said: no ha funcionado, sigue fragmentado.
no ha funcionado, sigue fragmentado. 
Copilot said: Perfecto — gracias por la paciencia. Te

Perfecto — gracias por la paciencia. Te doy dos opciones fiables para crear el archivo sin fragmentación: (A) un comando que puedes pegar en tu terminal y que crea el archivo literal, o (B) el contenido completo en un solo bloque para copiar/pegar en el editor de GitHub. Ambos están en un único bloque (sin usar triple-backticks internos) para evitar que el explorador lo fragmente.

Opción A — crear el archivo directamente desde la terminal (recomendado)

    Abre una terminal en la raíz del repositorio clonado.
    Ejecuta exactamente (esto crea CONTRIBUTING.md con el contenido completo):

cat > CONTRIBUTING.md <<'EOF'
🤝 Guía para Contribuir

¡Gracias por tu interés en contribuir a Análisis Numérico! Esta guía te explica cómo hacerlo de forma correcta y profesional.
📋 Índice

    Requisitos previos
    Flujo de trabajo
    Configurar commits firmados (GPG)
    Convenciones de código
    Proceso de Pull Request
    Resolver conflictos

📌 Requisitos Previos

Antes de contribuir, asegúrate de tener:

    ✅ Git instalado (https://git-scm.com/)
    ✅ Python 3.13+ instalado
    ✅ Conda o venv para entornos virtuales
    ✅ Una cuenta GitHub
    ✅ Haber hecho fork del repositorio

🔄 Flujo de Trabajo
1️⃣ Fork y clona el repositorio
Code

# Fork en GitHub (botón "Fork" en la esquina superior derecha)

# Clona tu fork
git clone https://github.com/TU_USUARIO/Analisis-Numerico.git
cd Analisis-Numerico

# Agrega el repositorio original como "upstream"
git remote add upstream https://github.com/infimus-carpentarius/Analisis-Numerico.git

2️⃣ Crea una rama para tu característica
Code

# Actualiza tu rama principal
git fetch upstream
git checkout Principal
git merge upstream/Principal

# Crea una nueva rama
git checkout -b feature/nombre-descriptivo

# Ejemplos de buenos nombres:
# - feature/interpolacion-lagrange
# - fix/error-calculo-derivada
# - docs/mejorar-readme
# - test/cobertura-modulo-ecuaciones

3️⃣ Realiza tus cambios

    Modifica los archivos necesarios.
    Crea/actualiza tests en la carpeta tests/.
    Actualiza documentación si es necesario.

4️⃣ Sincroniza y prepara el commit
Code

# Verifica que todo está actualizado
git fetch upstream

# Asegúrate de que tu rama está al día
git rebase upstream/Principal

# Prepara tus cambios
git add .

# Revisa qué vas a commitear
git diff --cached

🔐 Configurar Commits Firmados (GPG)

Los commits firmados acreditan tu autoría y aumentan la seguridad. Recomendado para contribuyentes.
Windows (Git Bash o WSL)
Code

# 1. Instalar GPG
# Si usas Chocolatey:
choco install gnupg

# Si usas WSL, apt-get:
sudo apt-get install gnupg

# 2. Generar tu clave GPG
gpg --full-generate-key

# Responde:
# - Tipo de clave: RSA
# - Tamaño: 4096
# - Validez: 2 años o más
# - Nombre: Tu nombre completo
# - Email: Tu email de GitHub

# 3. Obtén tu ID de clave
gpg --list-secret-keys --keyid-format=long

# 4. Exporta tu clave pública
gpg --armor --export TU_KEY_ID

Mac / Linux
Code

# Instala GPG si hace falta:
# Mac: brew install gnupg
# Linux (Debian/Ubuntu): sudo apt-get install gnupg

# Genera y exporta la clave como en Windows:
gpg --full-generate-key
gpg --list-secret-keys --keyid-format=long
gpg --armor --export TU_KEY_ID

Agregar clave a GitHub

    En GitHub: Settings → SSH and GPG keys → New GPG key.
    Pega tu clave pública (desde -----BEGIN hasta -----END) y guarda.

Configurar Git
Code

# Reemplaza TU_KEY_ID por el ID que obtuviste
git config --global user.signingKey TU_KEY_ID
git config --global commit.gpgSign true

✍️ Convenciones de Código
Commits semánticos

Usa este formato:
Code

<tipo>(<ámbito>): <descripción>

Tipos recomendados: feat, fix, test, docs, refactor, perf, chore.

Ejemplos:
Code

git commit -m "feat(ecuaciones): agregar método de Newton-Raphson"
git commit -m "fix(preliminares): corregir cálculo de error relativo"
git commit -m "docs: actualizar guía de contribución"

Estilo de código

    Sigue PEP 8 (Python).
    Usa nombres descriptivos.
    Añade type hints y comentarios útiles cuando proceda.

Ejemplo de función:
Code

def calcular_error_relativo(valor_aproximado: float, valor_exacto: float) -> float:
    """Calcula el error relativo entre dos valores."""
    if valor_exacto == 0:
        raise ValueError("El valor exacto no puede ser cero")
    return abs(valor_aproximado - valor_exacto) / abs(valor_exacto)

Tests

    Escribe tests para toda nueva funcionalidad.
    Usa pytest y pytest.approx para comparaciones numéricas.
    Objetivo de cobertura: >= 85% (si aplica).

🔀 Proceso de Pull Request
Antes de push
Code

pytest tests/ -v
pytest --cov=nombre_modulo tests/

Push a tu fork
Code

git push origin feature/nombre-descriptivo

Abre un PR

    En GitHub, crea la PR hacia infimus-carpentarius/Analisis-Numerico base Principal.
    Completa la descripción, indica cómo se probó y añade checklist.

Elementos sugeridos en la descripción del PR:

    Descripción breve del cambio.
    Tipo de cambio (feature, fix, docs).
    Cómo se testeó.
    Checklist: tests pasan, commits firmados, documentación actualizada.

Después

    Responde a comentarios, realiza cambios y vuelve a push.
    Cuando todo esté aprobado y el CI pase, hacer merge.

🔧 Resolver Conflictos
Code

git fetch upstream
git rebase upstream/Principal

Resuelve manualmente los conflictos (busca <<<<<<<), luego:
Code

git add .
git rebase --continue
git push origin feature/nombre-descriptivo --force-with-lease

📞 ¿Preguntas o problemas?

    Abre una issue describiendo el problema.
    Discute cambios importantes antes de implementarlos.
    Sé claro en las descripciones y pruebas.

🎓 Recursos útiles

    https://git-scm.com/doc
    https://www.conventionalcommits.org/
    https://pep8.org/
    https://docs.pytest.org/

✨ ¡Gracias por contribuir!

Tu trabajo es valorado y tu nombre aparecerá en el historial del proyecto. 🙌
