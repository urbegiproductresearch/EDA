# 🔄 Procesamiento - Evolution

Este módulo procesa los datos exportados de la tabla `evolution` de la plataforma SaaS. Su objetivo es transformar el CSV bruto en un archivo limpio, estructurado y preparado para análisis posteriores.

Estructura:

procesamiento_evolution/
├── data/
│   ├── raw/
│   │   └── evolution_raw.csv
│   └── processed/
│       └── evolution_data_processed.csv
├── scripts/
│   └── procesar_evolution.py
└── requirements.txt

Funcionamiento del script:

1. Carga del CSV raw ubicado en `data/raw/evolution_raw.csv`. Se limpian los nombres de columnas eliminando espacios innecesarios.

2. Resolución de columnas duplicadas. Si el export genera columnas como `Nombre`, `Nombre.1`, `Nombre.2`, el script las reorganiza automáticamente conservando la principal y renombrando las adicionales como `_num`, `_num2` o `_text2` según corresponda. Esto evita conflictos en análisis posteriores.

3. Limpieza y transformación básica, incluyendo conversión de tipos y eliminación de posibles inconsistencias estructurales.

4. Exportación del resultado final en `data/processed/evolution_data_processed.csv`.

Automatización:

El procesamiento se ejecuta automáticamente mediante GitHub Actions cuando se sube un nuevo archivo raw a la carpeta `procesamiento_evolution/data/raw/`. El workflow instala dependencias, ejecuta el script y realiza commit automático si se detectan cambios en el archivo procesado.

El resultado final es un dataset limpio, consistente y listo para análisis temporal, generación de dashboards o modelos analíticos.
