# 🏷️ Procesamiento – Resources (Arquitectura Multi-Comunidad)

Este módulo procesa la tabla `resources` exportada desde el panel del administrador de TGN. (Se encuentra en "información" y se descarga tras haber filtrado por comunidad).

Está diseñado con arquitectura multi-comunidad y actualmente soporta:

- KonektaLan
- Altxor Digital

El sistema es escalable para añadir nuevas comunidades sin modificar el motor principal.

---

# 🏗️ Estructura

procesamiento_resources/
├── config/
│   ├── konektalan.py
│   ├── altxor.py
│
├── data/
│   ├── raw/
│   │   ├── konektalan/
│   │   │   └── resources_raw.csv
│   │   └── altxor/
│   │       └── resources_raw.csv
│   │
│   └── processed/
│       ├── resources_processed_konektalan.csv
│       └── resources_processed_altxor.csv
│
├── src/
│   └── procesar_resources.py
└── README.md

---

# 🧠 Cómo funciona el sistema

## 1️⃣ Separación por comunidad

Cada comunidad tiene su propia carpeta en:

data/raw/

El script detecta automáticamente cada comunidad recorriendo las carpetas.

---

## 2️⃣ Configuración independiente

Cada comunidad tiene un archivo de configuración:

config/konektalan.py
config/altxor.py

En estos archivos se definen:

- Valores válidos de Género
- Rangos de Edad
- Roles
- Ámbitos
- Sectores
- Canales
- Tipos de evento
- Tipos de contenido
- Áreas (si aplica)
- Formatos (si aplica)
- Tipos de espacio (si aplica)

El motor no contiene valores hardcodeados.
Todo se define en la configuración.

---

## 3️⃣ Procesamiento fila a fila

El script:

- Lee la columna "Categorías"
- Analiza el "Tipo de perfil"
- Detecta coincidencias con los valores definidos en config
- Genera nuevas columnas de supercategorías

Supercategorías estructurales:

- supercategoria[Género]
- supercategoria[Edad] o supercategoria[Grupo_de_edad]
- supercategoria[Rol]
- supercategoria[Ámbito]
- supercategoria[Sector]
- supercategoria[Canales]
- supercategoria[tipo_de_evento]
- supercategoria[tipo_de_contenido]
- supercategoria[Área] (solo Altxor)
- supercategoria[Formato] (solo Altxor)
- supercategoria[tipo_de_espacio] (solo Altxor)

Además genera:

- extra[categoria_contenido]

---

## 4️⃣ Exportación

Se genera automáticamente un archivo por comunidad:

resources_processed_konektalan.csv
resources_processed_altxor.csv

---

# 🤖 Automatización

GitHub Actions ejecuta automáticamente el procesamiento cuando se suben archivos a:

procesamiento_resources/data/raw/**

El workflow:

1. Ejecuta el script
2. Genera los CSV procesados
3. Hace commit automático si hay cambios

---

# 🎯 Ventajas del diseño

- No hay duplicación de código
- Añadir nueva comunidad = crear nuevo archivo config
- Arquitectura escalable
- Separación clara entre motor y reglas de negocio
- Mantenible a largo plazo

---

# 📌 Resultado final

Un motor de clasificación taxonómica multi-comunidad, parametrizable y preparado para crecer.
