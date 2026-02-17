# =========================
# IMPORTS
# =========================
import pandas as pd
import numpy as np
import re
from pathlib import Path
from collections import defaultdict


# =========================
# RUTAS
# =========================
BASE_DIR = Path(__file__).resolve().parent.parents[1]

INPUT_PATH = BASE_DIR / "procesamiento_resources" / "data" / "raw" / "resources_raw.csv"
OUTPUT_PATH = BASE_DIR / "procesamiento_resources" / "data" / "processed" / "resources_processed.csv"


# =========================
# VALORES PERMITIDOS
# =========================

EDADES_VALIDAS = ["16-29", "30-44", "45-54", ">55"]

GENEROS = ["Masculino", "Femenino", "No binario"]

TIPOS_ORGANIZACION_VALIDOS = [
    "Empresas",
    "Entidades de formación",
    "Instituciones públicas"
]

# Nuevo ámbito extendido
ROLES_VALIDOS = [
    "En búsqueda de empleo",
    "Profesional sector privado",
    "Profesional sector público",
    "Estudiante",
    "Trabajador por cuenta propia",
    "Agente de empleo",
    "Recursos Humanos",
    "Captación Talento"
]

TIPOS_CONTENIDO_GENERAL = [
    "Noticia",
    "Producto o servicio",
    "Evento",
    "Ayuda",
    "Recurso web",
    "Otros",
    "Oferta de empleo"
]

TIPOS_NOTICIA_VALIDOS = [
    "Noticias",
    "Informes",
    "Artículos",
    "Casos de éxito",
    "Premios y reconocimientos",
    "Mesas Redondas"
]

CANALES_VALIDOS = [
    "Trabajar en Euskadi",
    "Emprendimiento y autoempleo",
    "Oportunidades laborales",
    "Formación",
    "Guía de uso",
    "Ayudas y subvenciones",
    "Vivir en Euskadi",
    "Historias de vida",
    "Innovación en la empresa"
]


# =========================
# DUPLICADOS
# =========================
def resolver_columnas_duplicadas(df):

    grupos = defaultdict(list)

    for col in df.columns:
        base = re.sub(r"\.\d+$", "", col)
        grupos[base].append(col)

    nuevas_columnas = {}

    for base, columnas in grupos.items():

        if len(columnas) == 1:
            nuevas_columnas[columnas[0]] = base
            continue

        numericas = [c for c in columnas if pd.api.types.is_numeric_dtype(df[c])]
        no_numericas = [c for c in columnas if not pd.api.types.is_numeric_dtype(df[c])]

        if no_numericas:
            nuevas_columnas[no_numericas[0]] = base
        else:
            nuevas_columnas[columnas[0]] = base

        for idx, col in enumerate(numericas, start=1):
            if idx == 1:
                nuevas_columnas[col] = f"{base}_num"
            else:
                nuevas_columnas[col] = f"{base}_num{idx}"

    df = df.rename(columns=nuevas_columnas)
    return df


# =========================
# CLASIFICACION CATEGORIA CONTENIDO
# =========================
def clasificar_categoria_contenido(tipo_perfil, items):

    if tipo_perfil == "Evento":
        return "Evento"

    if tipo_perfil == "Ayuda":
        return "Ayuda"

    if tipo_perfil == "Oferta de empleo":
        return "Búsqueda de empleo"

    if tipo_perfil == "Noticia":
        return "Actualidad"

    return np.nan


# =========================
# PROCESAMIENTO
# =========================
def procesar_categorias(row):

    categorias = row.get("Categorías", "")
    tipo_perfil = str(row.get("Tipo de perfil", "")).strip()

    if pd.isna(categorias):
        categorias = ""

    items = [c.strip() for c in str(categorias).split(",") if c.strip()]

    genero = np.nan
    edad = np.nan
    ambito = np.nan
    rol = np.nan
    sector = []
    tipo_evento = []
    tipo_contenido = []
    info_noticia = []
    canales = []

    categoria_contenido = clasificar_categoria_contenido(tipo_perfil, items)

    for item in items:

        # Género
        if item in GENEROS:
            genero = item

        # Edad
        elif item in EDADES_VALIDAS:
            edad = item

        # Ámbito (Organizaciones)
        elif tipo_perfil == "Organización" and item in TIPOS_ORGANIZACION_VALIDOS:
            ambito = item

        # Rol (Perfil profesional)
        elif tipo_perfil == "Perfil profesional" and item in ROLES_VALIDOS:
            rol = item

        # Tipo noticia estructurada
        elif item in TIPOS_NOTICIA_VALIDOS:
            tipo_contenido.append(item)

        # Canales
        elif item in CANALES_VALIDOS:
            canales.append(item)

        else:
            # Sectores ahora incluyen profesionales y organizaciones
            if tipo_perfil in ["Perfil profesional", "Organización", "Empresas"]:
                sector.append(item)

            elif tipo_perfil == "Evento":
                tipo_evento.append(item)

            elif tipo_perfil == "Noticia":
                info_noticia.append(item)

    return pd.Series({
        "supercategoria[Género]": genero,
        "supercategoria[Edad]": edad,
        "supercategoria[Ámbito]": ambito,
        "supercategoria[Rol]": rol,
        "supercategoria[Sector]": "; ".join(sector) if sector else np.nan,
        "supercategoria[tipo_de_evento]": "; ".join(tipo_evento) if tipo_evento else np.nan,
        "supercategoria[tipo_de_contenido]": "; ".join(tipo_contenido) if tipo_contenido else np.nan,
        "extra[info_noticia]": "; ".join(info_noticia) if info_noticia else np.nan,
        "extra[info_extra_cat_contenido]": np.nan,
        "extra[categoria_contenido]": categoria_contenido,
        "supercategoria[Canales]": "; ".join(canales) if canales else np.nan
    })


# =========================
# PIPELINE
# =========================
def main():

    print("Cargando datos...")
    df = pd.read_csv(INPUT_PATH)
    df.columns = df.columns.str.strip()

    df = resolver_columnas_duplicadas(df)

    print("Procesando categorías...")
    nuevas_columnas = df.apply(procesar_categorias, axis=1)
    df = pd.concat([df, nuevas_columnas], axis=1)

    print("Guardando archivo procesado...")
    df.to_csv(OUTPUT_PATH, index=False)

    print("Proceso finalizado correctamente")


if __name__ == "__main__":
    main()

