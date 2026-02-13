# =========================
# IMPORTS
# =========================
import pandas as pd
import numpy as np
from pathlib import Path


# =========================
# RUTAS
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_PATH = BASE_DIR / "procesamiento_resources" / "data" / "raw" / "resources_raw.csv"
OUTPUT_PATH = BASE_DIR / "procesamiento_resources" / "data" / "processed" / "resources_processed.csv"


# =========================
# VALORES EXACTOS PERMITIDOS
# =========================

EDADES_VALIDAS = ["16-29", "30-44", "45-54", ">55"]

GENEROS = ["Masculino", "Femenino", "No binario"]

TIPOS_ORGANIZACION_VALIDOS = [
    "Empresas",
    "Entidades de formación",
    "Instituciones públicas"
]

CONTEXTO_PROFESIONAL_VALIDO = [
    "En búsqueda de empleo",
    "Profesional sector privado",
    "Profesional sector público",
    "Estudiante",
    "Trabajador por cuenta propia"
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

TIPO_CONTENIDO = [
    "Noticias",
    "Eventos",
    "Congreso",
    "Oportunidades laborales"
]


# =========================
# FUNCIÓN DE CLASIFICACIÓN SUPERIOR
# =========================
def clasificar_categoria_contenido(tipo_perfil, items):

    if tipo_perfil not in TIPOS_CONTENIDO_GENERAL:
        return np.nan

    # Reglas directas por tipo de perfil
    if tipo_perfil == "Evento":
        return "Evento"

    if tipo_perfil == "Ayuda":
        return "Ayuda"

    if tipo_perfil == "Oferta de empleo":
        return "Búsqueda de empleo"

    # Reglas por categorías relacionadas con empleo
    empleo_keywords = [
        "En búsqueda de empleo",
        "Búsqueda de empleo",
        "Oportunidades laborales"
    ]

    if any(item in empleo_keywords for item in items):
        return "Búsqueda de empleo"

    # Noticias y resto
    if tipo_perfil == "Noticia":
        return "Actualidad"

    return "Actualidad"


# =========================
# FUNCIÓN PRINCIPAL DE PROCESAMIENTO
# =========================
def procesar_categorias(row):

    categorias = row.get("Categorías", "")
    tipo_perfil = str(row.get("Tipo de perfil", "")).strip()

    if pd.isna(categorias):
        categorias = ""

    items = [c.strip() for c in str(categorias).split(",") if c.strip()]

    # Inicialización
    genero = np.nan
    edad = np.nan
    tipo_organizacion = np.nan
    contexto_profesional = np.nan

    sector_profesional = []
    sector_noticia = []
    sector_evento = []
    tipo_contenido = []

    # Clasificación superior combinada
    categoria_contenido = clasificar_categoria_contenido(tipo_perfil, items)

    for item in items:

        # -------------------------
        # GENERO
        # -------------------------
        if item in GENEROS:
            genero = item

        # -------------------------
        # EDAD (solo valores exactos)
        # -------------------------
        elif item in EDADES_VALIDAS:
            edad = item

        # -------------------------
        # ORGANIZACION
        # -------------------------
        elif tipo_perfil == "Organización" and item in TIPOS_ORGANIZACION_VALIDOS:
            tipo_organizacion = item

        # -------------------------
        # CONTEXTO PERFIL PROFESIONAL
        # -------------------------
        elif tipo_perfil == "Perfil profesional" and item in CONTEXTO_PROFESIONAL_VALIDO:
            contexto_profesional = item

        # -------------------------
        # TIPO CONTENIDO SECUNDARIO
        # -------------------------
        elif item in TIPO_CONTENIDO:
            tipo_contenido.append(item)

        # -------------------------
        # SECTORES SEGÚN PERFIL
        # -------------------------
        else:
            if tipo_perfil == "Perfil profesional":
                sector_profesional.append(item)

            elif tipo_perfil == "Noticia":
                sector_noticia.append(item)

            elif tipo_perfil == "Evento":
                sector_evento.append(item)

    return pd.Series({
        "genero": genero,
        "edad": edad,
        "contexto_profesional": contexto_profesional,
        "tipo_organizacion": tipo_organizacion,
        "categoria_contenido": categoria_contenido,
        "sector_profesional": "; ".join(sector_profesional) if sector_profesional else np.nan,
        "sector_noticia": "; ".join(sector_noticia) if sector_noticia else np.nan,
        "sector_evento": "; ".join(sector_evento) if sector_evento else np.nan,
        "tipo_contenido": "; ".join(tipo_contenido) if tipo_contenido else np.nan
    })


# =========================
# PIPELINE
# =========================
def main():

    print("Cargando datos...")
    df = pd.read_csv(INPUT_PATH)
    df.columns = df.columns.str.strip()

    print("Procesando categorías...")
    nuevas_columnas = df.apply(procesar_categorias, axis=1)
    df = pd.concat([df, nuevas_columnas], axis=1)

    print("Guardando archivo procesado...")
    df.to_csv(OUTPUT_PATH, index=False)

    print("Proceso finalizado correctamente")


if __name__ == "__main__":
    main()




