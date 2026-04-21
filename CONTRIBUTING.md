# 🤝 Guía para Contribuir

¡Gracias por tu interés en contribuir a **Análisis Numérico**! Esta guía te explica cómo hacerlo de forma correcta y profesional.

---

## 📋 Índice

1. [Requisitos previos](#requisitos-previos)
2. [Flujo de trabajo](#flujo-de-trabajo)
3. [Configurar commits firmados (GPG)](#configurar-commits-firmados-gpg)
4. [Convenciones de código](#convenciones-de-código)
5. [Proceso de Pull Request](#proceso-de-pull-request)
6. [Resolver conflictos](#resolver-conflictos)

---

## 📌 Requisitos Previos

Antes de contribuir, asegúrate de tener:

- ✅ **Git** instalado (https://git-scm.com/)
- ✅ **Python 3.13+** instalado
- ✅ **Conda** o **venv** para entornos virtuales
- ✅ Una **cuenta GitHub**
- ✅ Haber hecho fork del repositorio

---

## 🔄 Flujo de Trabajo

# 1️⃣ Fork y clona el repositorio

# Fork en GitHub (botón "Fork" en la esquina superior derecha)

# Clona tu fork
git clone https://github.com/TU_USUARIO/Analisis-Numerico.git
cd Analisis-Numerico

# Agrega el repositorio original como "upstream"
git remote add upstream https://github.com/infimus-carpentarius/Analisis-Numerico.git

## 2️⃣ Crea una rama para tu característica

# Actualiza tu rama principal
git fetch upstream
git checkout Principal
git merge upstream/Principal

# Crea una nueva rama
git checkout -b feature/nombre-descriptivo

# Ejemplos de buenos nombres:
 - feature/interpolacion-lagrange
 - fix/error-calculo-derivada
 - docs/mejorar-readme
 - test/cobertura-modulo-ecuaciones

## 3️⃣ Realiza tus cambios

- Modifica los archivos necesarios.
- Crea/actualiza tests en la carpeta `tests/`.
- Actualiza documentación si es necesario.

## 4️⃣ Sincroniza y prepara el commit

# Verifica que todo está actualizado
git fetch upstream

# Asegúrate de que tu rama está al día
git rebase upstream/Principal

# Prepara tus cambios
git add .

# Revisa qué vas a commitear
git diff --cached

---

## 🔐 Configurar Commits Firmados (GPG)

Los commits firmados acreditan tu autoría y aumentan la seguridad. Recomendado para contribuyentes.

# Windows (Git Bash o WSL)

# 1. Instalar GPG
# Si usas Chocolatey:
choco install gnupg

# Si usas WSL, apt-get:
sudo apt-get install gnupg

# 2. Generar tu clave GPG
gpg --full-generate-key

# Responde:
 - Tipo de clave: RSA
 - Tamaño: 4096
 - Validez: 2 años o más
 - Nombre: Tu nombre completo
 - Email: Tu email de GitHub

# 3. Obtén tu ID de clave
gpg --list-secret-keys --keyid-format=long

# 4. Exporta tu clave pública
gpg --armor --export TU_KEY_ID

### Mac / Linux

# Instala GPG si hace falta:
 Mac: brew install gnupg
 Linux (Debian/Ubuntu): sudo apt-get install gnupg

# Genera y exporta la clave como en Windows:
gpg --full-generate-key
gpg --list-secret-keys --keyid-format=long
gpg --armor --export TU_KEY_ID

### Agregar clave a GitHub

1. En GitHub: Settings → SSH and GPG keys → New GPG key.
2. Pega tu clave pública (desde -----BEGIN hasta -----END) y guarda.

### Configurar Git

# Reemplaza TU_KEY_ID por el ID que obtuviste
git config --global user.signingKey TU_KEY_ID
git config --global commit.gpgSign true

---

## ✍️ Convenciones de Código

### Commits semánticos

Usa este formato:

<tipo>(<ámbito>): <descripción>

Tipos recomendados: feat, fix, test, docs, refactor, perf, chore.

Ejemplos:

git commit -m "feat(ecuaciones): agregar método de Newton-Raphson"
git commit -m "fix(preliminares): corregir cálculo de error relativo"
git commit -m "docs: actualizar guía de contribución"

### Estilo de código

- Sigue PEP 8 (Python).
- Usa nombres descriptivos.
- Añade type hints y comentarios útiles cuando proceda.

Ejemplo de función:

def calcular_error_relativo(valor_aproximado: float, valor_exacto: float) -> float:
    """Calcula el error relativo entre dos valores."""
    if valor_exacto == 0:
        raise ValueError("El valor exacto no puede ser cero")
    return abs(valor_aproximado - valor_exacto) / abs(valor_exacto)

### Tests

- Escribe tests para toda nueva funcionalidad.
- Usa pytest y pytest.approx para comparaciones numéricas.
- Objetivo de cobertura: >= 85% (si aplica).

---

## 🔀 Proceso de Pull Request

### Antes de push

pytest tests/ -v
pytest --cov=nombre_modulo tests/

### Push a tu fork
git push origin feature/nombre-descriptivo

### Abre un PR

1. En GitHub, crea la PR hacia `infimus-carpentarius/Analisis-Numerico` base `Principal`.
2. Completa la descripción, indica cómo se probó y añade checklist.

Elementos sugeridos en la descripción del PR:
- Descripción breve del cambio.
- Tipo de cambio (feature, fix, docs).
- Cómo se testeó.
- Checklist: tests pasan, commits firmados, documentación actualizada.

### Después

- Responde a comentarios, realiza cambios y vuelve a push.
- Cuando todo esté aprobado y el CI pase, hacer merge.

---

## 🔧 Resolver Conflictos

git fetch upstream
git rebase upstream/Principal

Resuelve manualmente los conflictos (busca <<<<<<<), luego:

git add .
git rebase --continue
git push origin feature/nombre-descriptivo --force-with-lease

---

## 📞 ¿Preguntas o problemas?

- Abre una issue describiendo el problema.
- Discute cambios importantes antes de implementarlos.
- Sé claro en las descripciones y pruebas.

---

## 🎓 Recursos útiles

- https://git-scm.com/doc
- https://www.conventionalcommits.org/
- https://pep8.org/
- https://docs.pytest.org/

---

## ✨ ¡Gracias por contribuir!

Tu trabajo es valorado y tu nombre aparecerá en el historial del proyecto. 🙌
