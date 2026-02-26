# 👤 procesamiento_users

Este módulo contiene el pipeline automatizado de procesamiento de la tabla **users** exportada desde la plataforma TGN.

Su función es transformar el archivo `users_raw` en un archivo estructurado, normalizado y preparado para su uso en Looker Studio.

---

# 🎯 Objetivo del módulo

- Resolver problemas estructurales del archivo original.
- Estandarizar columnas duplicadas.
- Generar columnas dinámicas por canal según comunidad.
- Separar perfiles en estructura analítica.
- Exportar automáticamente el archivo procesado por comunidad.

---

# 🗂️ Estructura del módulo

```
procesamiento_users/
├── data/
│   ├── raw/
│   │   └── {comunidad}/
│   │        └── users_raw.csv
│   └── processed/
│           └── users_processed_{comunidad}.csv
│
├── src/
│   └── procesar_users.py
│
└── requirements.txt
```

---

# 🔄 Flujo de funcionamiento

1. Se exporta la tabla `users` desde la plataforma TGN.
2. Se guarda con el nombre exacto:  
   `users_raw.csv`
3. Se sube a la carpeta correspondiente dentro de:

```
procesamiento_users/data/raw/{comunidad}/
```

4. GitHub Actions detecta el cambio.
5. Se ejecuta automáticamente el script `procesar_users.py`.
6. Se genera el archivo:

```
users_processed_{comunidad}.csv
```

en la carpeta `data/processed/`.

---

# 🧠 Transformaciones realizadas

## 1️⃣ Resolución de columnas duplicadas

- Detecta columnas repetidas (ej. `.1`, `.2`).
- Mantiene la columna textual como principal.
- Renombra columnas numéricas como `{columna}_num`.

---

## 2️⃣ Generación dinámica de canales

A partir de la columna:

```
Canales a los que está suscrito
```

Se generan columnas binarias con la estructura:

```
canal[Nombre del canal]
```

Características:

- Se generan únicamente los canales válidos definidos para cada comunidad.
- La configuración es específica por comunidad.
- Arquitectura multi-comunidad.

---

## 3️⃣ Separación estructurada de perfiles

A partir de la columna:

```
Perfiles
```

Se generan columnas estructuradas:

```
extra[perfil_principal]
extra[perfil_secundario]
extra[perfil_terciario]
extra[perfil_cuaternario]
extra[perfil_quinto]
```

Esto permite:

- Análisis estructurado en Looker Studio.
- Evitar parsing manual posterior.
- Estandarización entre comunidades.

---

# 🌍 Soporte multi-comunidad

El sistema detecta automáticamente la comunidad a partir de:

- El nombre de la subcarpeta dentro de `raw/`.

Actualmente soporta:

- KonektaLan
- Altxor Digital

Se puede ampliar añadiendo nuevas configuraciones de canales y perfiles sin duplicar código.

---

# 🤖 Automatización

Este módulo se ejecuta automáticamente mediante GitHub Actions cuando se detectan cambios en:

```
procesamiento_users/data/raw/**
```

No es necesario ejecutar el script manualmente.

---

# ⚠️ Normas importantes

- No modificar manualmente archivos en `processed/`.
- No cambiar el nombre `users_raw.csv`.
- No alterar la estructura de carpetas.
- No editar el archivo procesado manualmente.

El sistema depende estrictamente de la estructura y naming actual.

---

# 🧩 Resultado final

El archivo generado:

```
users_processed_{comunidad}.csv
```

Está listo para:

- Subirse a Looker Studio.
- Alimentar dashboards de seguimiento mensual.
- Integrarse con otros módulos procesados del repositorio.

Este módulo forma parte del motor de transformación automatizado del repositorio EDA.
