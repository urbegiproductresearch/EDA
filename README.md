# 📊 EDA - Exploratory Data Analysis

Este repositorio contiene los análisis exploratorios realizados sobre los datos exportados desde la plataforma TGN.

Actualmente se trabaja principalmente con datos de la tabla `resources` y la tabla `evolution`, utilizando como comunidad piloto KonektaLan.

El objetivo del EDA es comprender la estructura real de los datos exportados, detectar columnas duplicadas o inconsistencias, analizar la calidad de los datos (valores nulos, formatos y categorías), explorar la distribución de tipos de perfil y categorías, e identificar oportunidades de mejora en la taxonomía.

Estructura del repositorio:

EDA/
├── notebooks/
│   ├── eda_resources.ipynb
│   ├── eda_evolution.ipynb
├── data/
│   ├── raw/
│   ├── processed/
└── README.md

El notebook `eda_resources.ipynb` analiza la distribución de tipos de perfil, la estructura de categorías, posibles duplicados en columnas, validación de taxonomías y detección de inconsistencias en etiquetas.

El notebook `eda_evolution.ipynb` estudia la evolución temporal de registros, métricas de actividad, agrupaciones por comunidad y análisis de tendencias.

Como resultado del EDA se definió una estructura clara de supercategorías, se separó la información estructural de la contextual mediante columnas `extra[...]`, se mejoró la coherencia taxonómica y se diseñó el pipeline automatizado de procesamiento.

Este módulo sirve como base analítica para el diseño y evolución de los scripts de transformación.
