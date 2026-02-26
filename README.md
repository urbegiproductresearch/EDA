# 📊 EDA – Procesamiento de tablas de TGN (panel del administrador)

Este repositorio contiene el sistema de análisis exploratorio y los pipelines automatizados de transformación de datos exportados desde la plataforma TGN (panel del administrador).

No es únicamente un conjunto de scripts, sino una arquitectura modular diseñada para alimentar de forma automática los informes mensuales en Looker Studio.

🌍 Alcance actual

Actualmente se procesan las siguientes tablas:

users

resources

proyectos

evolution_data

conversaciones

Y múltiples comunidades, actualmente:

KonektaLan

Altxor Digital

El sistema está diseñado con arquitectura multi-comunidad y es escalable para incorporar nuevas comunidades sin duplicar código.

🏗️ Arquitectura del repositorio
EDA/
│
├── EDA/                              # Análisis exploratorio (notebooks)
│
├── procesamiento_users/
├── procesamiento_resources/
├── procesamiento_proyectos/
├── procesamiento_evolution/
├── procesamiento_conversaciones/
│
└── .github/workflows/                 # Automatización

Cada módulo de procesamiento sigue la misma estructura:

procesamiento_xxx/
│
├── data/
│   ├── raw/           # Archivos originales exportados desde TGN
│   └── processed/     # Archivos transformados automáticamente
│
├── src/ o scripts/
└── requirements.txt   (si aplica)
🔎 1. EDA (Exploratory Data Analysis)

Carpeta: EDA/

Contiene notebooks utilizados para:

Analizar estructura de datos exportados

Detectar duplicados y problemas estructurales

Validar taxonomías

Diseñar supercategorías

Ajustar reglas de clasificación

Probar lógica multi-comunidad

El EDA fue la base conceptual para diseñar el sistema automatizado de procesamiento.

Aquí se experimenta.
En los módulos de procesamiento se implementa.

🔹 2. Procesamiento modular por tabla

Cada carpeta procesamiento_xxx es un pipeline independiente.

Esto permite:

Separación clara de responsabilidades

Escalabilidad

Mantenimiento aislado

Evolución controlada

📌 procesamiento_users

Procesa la tabla users.

Características:

Resolución automática de columnas duplicadas

Generación dinámica de columnas por canal (según comunidad)

Separación estructurada de perfiles (extra[perfil_x])

Arquitectura multi-comunidad basada en configuración

Export automático con nombre normalizado

Cada comunidad puede tener:

Canales distintos

Perfiles distintos

Configuración independiente

📌 procesamiento_resources

Procesa la tabla resources.

Características:

Arquitectura multi-comunidad

Generación automática de supercategorías

Separación entre información estructural y contextual

Reglas parametrizadas por comunidad

Commit automático vía GitHub Actions

📌 procesamiento_proyectos

Procesa la tabla proyectos.

Pipeline estructural:

Limpieza

Normalización

Preparación para reporting

Export automático

📌 procesamiento_evolution

Procesa la tabla evolution_data.

Pipeline enfocado en:

Unificación de columnas mes

Estandarización de fechas

Resolución de duplicados

Preparación para análisis temporal en Looker Studio

Es la base de los indicadores mensuales.

📌 procesamiento_conversaciones

Procesa la tabla conversaciones.

Características:

Resolución de columnas duplicadas (Usuarios / Administradores)

Renombrado estructural consistente

Detección automática de comunidad

Export por comunidad

🤖 Automatización

El repositorio utiliza GitHub Actions.

Cada vez que se sube un nuevo archivo raw a:

procesamiento_*/data/raw/**

Se ejecuta automáticamente:

Instalación de dependencias

Ejecución de los scripts correspondientes

Generación de archivos en data/processed/

Commit automático si hay cambios

El sistema está diseñado para no requerir ejecución manual.

🧠 Filosofía del sistema

Este repositorio no es simplemente procesamiento de CSV.

Es un motor de transformación de datos con las siguientes propiedades:

Escalable

Parametrizable

Multi-comunidad

Modular

Robusto ante cambios estructurales

Integrado con reporting automatizado

Permite desacoplar:

Plataforma → Transformación → Reporting

Reduciendo errores manuales y dependencia operativa.

🎯 Objetivo estratégico

Construir una infraestructura de datos ligera que permita:

Automatizar informes mensuales

Estandarizar indicadores

Garantizar coherencia entre comunidades

Reducir intervención manual

Facilitar la escalabilidad futura

Este repositorio representa la capa intermedia entre la plataforma TGN y el sistema de reporting en Looker Studio.
