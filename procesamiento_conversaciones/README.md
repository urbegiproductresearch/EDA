# 💬 procesamiento_conversaciones

Este módulo contiene el pipeline automatizado de procesamiento de la tabla **conversaciones** exportada desde la plataforma TGN.

Su función es transformar el archivo `conversaciones_raw` en un archivo estructurado, consistente y listo para su uso en Looker Studio.

---

# 🎯 Objetivo del módulo

- Resolver problemas estructurales del archivo original.
- Corregir columnas duplicadas con nombres idénticos.
- Estandarizar nomenclatura.
- Detectar automáticamente la comunidad.
- Exportar un archivo procesado por comunidad.

---

# 🗂️ Estructura del módulo

```
procesamiento_conversaciones/
├── data/
│   ├── raw/
│   │   └── {comunidad}/
│   │        └── conversaciones_raw.csv
│   └── processed/
│           └── conversaciones_processed_{comunidad}.csv
│
├── src/
│   └── procesar_conversaciones.py
│
└── requirements.txt (si aplica)
```

---

# 🔄 Flujo de funcionamiento

1. Se exporta la tabla `conversaciones` desde la plataforma TGN.
2. Se guarda con el nombre exacto:  
   `conversaciones_raw.csv`
3. Se sube a la carpeta correspondiente dentro de:

```
procesamiento_conversaciones/data/raw/{comunidad}/
```

4. GitHub Actions detecta el cambio.
5. Se ejecuta automáticamente el script `procesar_conversaciones.py`.
6. Se genera el archivo:

```
conversaciones_processed_{comunidad}.csv
```

en la carpeta `data/processed/`.

---

# 🧠 Transformaciones realizadas

## 1️⃣ Resolución de columnas duplicadas

La tabla original contiene columnas con el mismo nombre:

- `Usuarios`
- `Administradores`

En ambos casos existen dos columnas con el mismo nombre:
- Una columna con valores de texto.
- Una columna con valores numéricos.

El sistema:

- Mantiene la columna textual con el nombre original.
- Renombra automáticamente la columna numérica como:

```
Usuarios_num
Administradores_num
```

De esta manera se evita ambigüedad en el análisis posterior.

---

## 2️⃣ Detección automática de comunidad

El sistema detecta la comunidad de dos formas:

- Por el nombre de la subcarpeta dentro de `raw/`
- O mediante la columna interna `Comunidades` del archivo

Esto permite que el mismo script funcione para múltiples comunidades sin duplicar lógica.

Actualmente soporta:

- KonektaLan
- Altxor Digital

---

# 🤖 Automatización

Este módulo se ejecuta automáticamente mediante GitHub Actions cuando se detectan cambios en:

```
procesamiento_conversaciones/data/raw/**
```

No es necesario ejecutar el script manualmente.

---

# ⚠️ Normas importantes

- No modificar manualmente archivos en `processed/`.
- No cambiar el nombre `conversaciones_raw.csv`.
- No alterar la estructura de carpetas.
- No editar el archivo procesado manualmente.
- No modificar nombres de columnas en el archivo original antes de subirlo.

El sistema depende estrictamente de la estructura actual.

---

# 🧩 Resultado final

El archivo generado:

```
conversaciones_processed_{comunidad}.csv
```

Está listo para:

- Subirse a Looker Studio.
- Alimentar indicadores de interacción mensual.
- Integrarse con el resto de módulos procesados del repositorio.

Este módulo forma parte del motor de transformación automatizado del repositorio EDA.
