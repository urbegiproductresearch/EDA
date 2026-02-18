# 📊 EDA – Procesamiento de tablas de TGN (panel del administrador)

Este repositorio contiene el análisis exploratorio y los pipelines automatizados de transformación de datos exportados desde la plataforma de TGN.

Actualmente se procesan dos grandes tablas:

- `resources`
- `evolution`

Y múltiples comunidades, actualmente:
- KonektaLan
- Altxor Digital

El sistema está diseñado con arquitectura multi-comunidad y es escalable para incorporar nuevas comunidades sin duplicar código.

---

# 🏗️ Arquitectura del repositorio

EDA/
├── procesamiento_resources/
├── procesamiento_evolution/
├── EDA/
└── .github/workflows/

---

# 🔹 1. EDA (Exploratory Data Analysis)

Carpeta: `EDA/`

Contiene notebooks utilizados para:

- Analizar estructura de datos exportados
- Detectar duplicados y problemas estructurales
- Validar taxonomías
- Diseñar supercategorías
- Ajustar reglas de clasificación

El EDA fue la base para diseñar el sistema automatizado de procesamiento.

---

# 🔹 2. procesamiento_resources

Procesa la tabla `resources`.

Características principales:

- Arquitectura multi-comunidad
- Configuración independiente por comunidad
- Generación automática de supercategorías
- Separación entre información estructural y contextual
- Commit automático mediante GitHub Actions

Cada comunidad tiene:
- Sus propios valores válidos
- Sus propias supercategorías
- Sus propias reglas de clasificación

---

# 🔹 3. procesamiento_evolution

Procesa la tabla `evolution`.

Funciona como pipeline estructural más simple:

- Limpieza
- Resolución de columnas duplicadas
- Estandarización
- Export automático

---

# 🤖 Automatización

El repositorio utiliza GitHub Actions.

Cada vez que se sube un nuevo archivo raw a:

procesamiento_resources/data/raw/**
procesamiento_evolution/data/raw/**

Se ejecuta automáticamente:

1. Procesamiento de resources (multi-comunidad)
2. Procesamiento de evolution
3. Commit automático si hay cambios

---

# 🎯 Objetivo del sistema

Construir un motor de transformación de datos:

- Escalable
- Parametrizable
- Multi-comunidad
- Robusto ante cambios estructurales

Este repositorio ya no es solo un conjunto de scripts, sino una arquitectura de transformación modular.
