# 🏷️ Procesamiento - Resources

Este módulo procesa la tabla `resources` exportada desde la plataforma SaaS. Actualmente está adaptado a la comunidad piloto KonektaLan, con una estructura de supercategorías alineada con su modelo taxonómico.

El objetivo es transformar el CSV bruto en un dataset estructurado con supercategorías normalizadas, separación entre información estructural y contextual, clasificación coherente por tipo de perfil y columnas organizadas de forma clara.

Estructura:

procesamiento_resources/
├── data/
│   ├── raw/
│   │   └── resources_raw.csv
│   └── processed/
│       └── resources_processed.csv
├── src/
│   └── procesar_resources.py
└── requirements.txt

Funcionamiento del script:

1. Carga y limpieza inicial. Se lee el CSV raw, se eliminan espacios en los nombres de columnas y se resuelven automáticamente posibles duplicados estructurales.

2. Clasificación por supercategorías. El script analiza el campo “Tipo de perfil” y la columna “Categorías” para generar las siguientes columnas estructuradas:

- supercategoria[Género]
- supercategoria[Edad]
- supercategoria[Ámbito]
- supercategoria[Rol]
- supercategoria[Sector]
- supercategoria[tipo_de_evento]
- supercategoria[tipo_de_contenido]
- supercategoria[Canales]

Estas columnas recogen únicamente valores estructurales definidos como válidos dentro del modelo taxonómico.

3. Separación de información contextual. Se generan columnas adicionales que almacenan información no estructural:

- extra[info_noticia]
- extra[info_extra_cat_contenido]
- extra[categoria_contenido]

Estas columnas permiten mantener la taxonomía limpia sin perder información contextual relevante. El script garantiza que todas las columnas que comienzan por `extra[` se sitúan al final del dataset final.

4. Exportación del archivo procesado en `data/processed/resources_processed.csv`.

Lógica de clasificación:

- Para perfiles profesionales se identifican Rol, Sector, Género y Edad.
- Para organizaciones se clasifica Ámbito y Sector.
- Para noticias se identifica el tipo de contenido y se separa la información contextual en `extra[info_noticia]`.
- Para eventos se clasifica el tipo de evento.
- Los canales se detectan en función del tipo de perfil y categorías asociadas.

Automatización:

El procesamiento se ejecuta automáticamente mediante GitHub Actions cuando se sube un nuevo archivo raw a `procesamiento_resources/data/raw/`. El workflow instala dependencias, ejecuta el script, genera el CSV procesado y realiza commit automático si se detectan cambios.

El resultado final es un dataset estructurado, limpio y preparado para análisis segmentado, dashboards o explotación avanzada por comunidad.
