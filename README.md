# 📊 EDA – Procesamiento de tablas de TGN (panel del administrador)

Este repositorio contiene los pipelines automatizados de transformación de datos exportados desde la plataforma TGN (panel del administrador).

Su objetivo es procesar archivos "raw" y generar automáticamente archivos "processed" listos para su uso en Looker Studio.

# 🌍 Alcance actual

Actualmente se procesan las siguientes tablas:

users

resources

evolution_data

conversaciones

Y múltiples comunidades, actualmente:

KonektaLan

Altxor Digital

El sistema está diseñado con arquitectura multi-comunidad y es escalable para incorporar nuevas comunidades sin duplicar código.

# 🏗️ Estructura actual del repositorio

EDA/
├── .github/workflows/
├── procesamiento_users/
├── procesamiento_resources/
├── procesamiento_evolution/
├── procesamiento_conversaciones/
└── README.md

Cada módulo de procesamiento sigue la misma estructura interna:

procesamiento_xxx/
├── data/
│ ├── raw/ (Archivos originales exportados desde TGN)
│ └── processed/ (Archivos transformados automáticamente)
├── src/ o scripts/
└── requirements.txt (si aplica)

# 🔹 Lógica de funcionamiento

El flujo de trabajo es el siguiente:

Se exportan las tablas desde la plataforma TGN.

Se suben a la carpeta correspondiente dentro de data/raw/.

GitHub Actions detecta el cambio.

Se ejecuta automáticamente el script de procesamiento.

Se generan los archivos en data/processed/.

Se realiza commit automático si hay cambios.

No es necesario ejecutar scripts manualmente.

# 📌 Módulos actuales
procesamiento_users

Resolución automática de columnas duplicadas

Generación dinámica de columnas por canal según comunidad

Separación estructurada de perfiles

Detección automática de comunidad

Export por comunidad

procesamiento_resources

Arquitectura multi-comunidad

Generación automática de supercategorías

Normalización estructural

Export automático

procesamiento_evolution

Unificación de columnas de mes

Estandarización de fechas

Limpieza estructural

Preparación para análisis temporal

procesamiento_conversaciones

Resolución de columnas duplicadas

Renombrado estructural consistente

Detección automática de comunidad

Export por comunidad

# 🤖 Automatización

El repositorio utiliza GitHub Actions.

Cada vez que se sube un nuevo archivo raw a:

procesamiento_*/data/raw/**

Se ejecuta automáticamente:

Instalación de dependencias

Ejecución de los scripts correspondientes

Generación de archivos procesados

Commit automático si hay cambios

# ⚠️ Normas importantes

No modificar manualmente los archivos en processed/.

No cambiar la estructura de carpetas.

No modificar nombres de archivos raw.

No ejecutar scripts manualmente desde fuera del workflow.

El sistema depende estrictamente de la estructura actual.

# 🎯 Propósito estratégico

Este repositorio actúa como capa intermedia entre:

Plataforma TGN → Transformación automatizada → Looker Studio

Permite:

Estandarizar indicadores

Automatizar informes mensuales

Reducir intervención manual

Facilitar la escalabilidad futura
