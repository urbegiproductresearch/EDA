# EDA
# Análisis y Procesamiento de Tablas de TGN

Este repositorio contiene el sistema de análisis y procesamiento automatizado de los datos exportados desde la plataforma web de TGN.

El objetivo principal es transformar el archivo CSV bruto descargado desde la web en un dataset estructurado, limpio y preparado para su uso en herramientas de Business Intelligence como Looker Studio.

---

## 🔄 Flujo de trabajo

El proceso funciona de la siguiente manera:

1. Se descarga el archivo CSV desde la web.
2. Se sube el archivo como:
   
   procesamiento_resources/data/raw/resources_raw.csv o como sean los nombres de las tablas requeridas

3. GitHub Actions ejecuta automáticamente el script de procesamiento.
4. Se genera el archivo limpio en:

   procesamiento_resources/data/processed/resources_processed.csv

5. Se descarga el archivo y se sube a Looker Studio para la elaboración de informes
