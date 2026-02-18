# 🔄 Procesamiento – Evolution

Este módulo procesa la tabla `evolution` exportada desde el panel del administrador de TGN (dentro de "DATOS", y tras haber filtrado por comunidad).

Su objetivo es transformar el excel bruto en un csv limpio y estructurado listo para análisis.

---

# 📂 Estructura

procesamiento_evolution/
├── data/
│   ├── raw/
│   │   └── evolution_raw.csv
│   └── processed/
│       └── evolution_data_processed.csv
├── scripts/
│   └── procesar_evolution.py
└── README.md

---

# ⚙️ Cómo funciona el procesamiento

El script `procesar_evolution.py` realiza los siguientes pasos:

1. Carga del CSV raw desde:
   data/raw/evolution_raw.csv

2. Limpieza de nombres de columnas:
   - Elimina espacios innecesarios
   - Normaliza estructura

3. Resolución de columnas duplicadas:
   Si el export genera columnas como:
   Nombre
   Nombre.1
   Nombre.2

   Se conserva la principal y se renombran las adicionales para evitar conflictos.

4. Transformaciones básicas:
   - Conversión de tipos
   - Limpieza estructural

5. Exportación final:
   data/processed/evolution_data_processed.csv

---

# 🤖 Automatización

Se ejecuta automáticamente mediante GitHub Actions cuando se sube un archivo a:

procesamiento_evolution/data/raw/

El workflow:

- Instala dependencias
- Ejecuta el script
- Hace commit automático si hay cambios

---

# 🎯 Resultado

Un dataset limpio, consistente y preparado para:

- Análisis temporal
- Dashboards
- Modelos analíticos
