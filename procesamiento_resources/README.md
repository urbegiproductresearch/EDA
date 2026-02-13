# Procesamiento de Resources
Esta carpeta contiene el pipeline de transformación de datos para el archivo de resources exportado desde la web.

---

## 📂 Estructura

### data/raw/
Contiene el archivo CSV original descargado desde la web:

resources_raw.csv

Este archivo no debe modificarse manualmente.

---

### data/processed/
Contiene el archivo generado automáticamente:

resources_processed.csv

Este archivo es el dataset limpio y estructurado que se utiliza en Looker Studio.

---

### scripts/
Contiene el script principal:

procesar_resources.py

Este script:

- Procesa la columna "Categorías"
- Extrae edad (16-29, 30-44, 45-54, >55)
- Clasifica género
- Identifica tipo de organización
- Identifica contexto profesional
- Genera la variable `categoria_contenido`
- Organiza sectores según tipo de perfil

---

## 🔄 Funcionamiento

El script se ejecuta automáticamente mediante GitHub Actions cuando se actualiza el archivo:

data/raw/resources_raw.csv

No es necesario ejecutar el script manualmente.

---

## 📊 Variables generadas

El procesamiento genera las siguientes columnas estructuradas:

- genero
- edad
- tipo_organizacion
- contexto_profesional
- categoria_contenido
- sector_profesional
- sector_noticia
- sector_evento
- tipo_contenido

Todas las clasificaciones están basadas en listas de valores cerrados para garantizar coherencia y evitar categorías ambiguas.

---

## 🚀 Escalabilidad

La estructura permite:

- Añadir nuevas reglas de clasificación
- Incorporar validaciones de calidad
- Versionar datos
- Integrar futuras capas analíticas o predictivas
