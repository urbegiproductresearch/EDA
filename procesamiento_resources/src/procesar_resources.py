import pandas as pd
import numpy as np
import re
from pathlib import Path
from collections import defaultdict
import sys

# =========================
# RUTAS BASE
# =========================

CURRENT_FILE = Path(__file__).resolve()
BASE_DIR = CURRENT_FILE.parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

sys.path.append(str(BASE_DIR))


# =========================
# RESOLVER DUPLICADOS
# =========================
def resolver_columnas_duplicadas(df):

    grupos = defaultdict(list)

    for col in df.columns:
        base = re.sub(r"\.\d+$", "", col)
        grupos[base].append(col)

    nuevas_columnas = {}

    for base, columnas in grupos.items():
        nuevas_columnas[columnas[0]] = base

    df = df.rename(columns=nuevas_columnas)
    return df


# =========================
# CLASIFICACION CONTENIDO
# =========================
def clasificar_categoria_contenido(tipo_perfil):

    if tipo_perfil == "Evento":
        return "Evento"

    if tipo_perfil == "Ayuda":
        return "Ayuda"

    if tipo_perfil in ["Noticia", "Noticias"]:
        return "Actualidad"

    return "Actualidad"


# =========================
# PROCESAMIENTO FILA
# =========================
def procesar_fila(row, config):

    categorias = row.get("Categorías", "")
    tipo_perfil = str(row.get("Tipo de perfil", "")).strip()

    if pd.isna(categorias):
        categorias = ""

    items = [c.strip() for c in str(categorias).split(",") if c.strip()]

    data = {}

    # =========================
    # GENERO
    # =========================
    data["supercategoria[Género]"] = next(
        (i for i in items if i in config["generos"]),
        np.nan
    )

    # =========================
    # EDAD
    # =========================
    edad_col = "supercategoria[Edad]"
    if config["nombre_comunidad"] == "altxor":
        edad_col = "supercategoria[Grupo_de_edad]"

    data[edad_col] = next(
        (i for i in items if i in config["edades"]),
        np.nan
    )

    # =========================
    # ROL
    # =========================
    data["supercategoria[Rol]"] = next(
        (i for i in items if i in config["roles"]),
        np.nan
    )

    # =========================
    # ÁMBITO
    # =========================
    data["supercategoria[Ámbito]"] = next(
        (i for i in items if i in config["ambitos"]),
        np.nan
    )

    # =========================
    # SECTOR (solo si definido)
    # =========================
    if config.get("sectores"):
        sectores = [i for i in items if i in config["sectores"]]
        data["supercategoria[Sector]"] = "; ".join(sectores) if sectores else np.nan

    # =========================
    # CANALES
    # =========================
    canales = [i for i in items if i in config["canales"]]
    data["supercategoria[Canales]"] = "; ".join(canales) if canales else np.nan

    # =========================
    # TIPO EVENTO
    # =========================
    tipos_evento = [i for i in items if i in config["tipos_evento"]]
    data["supercategoria[tipo_de_evento]"] = "; ".join(tipos_evento) if tipos_evento else np.nan

    # =========================
    # TIPO CONTENIDO
    # =========================
    tipos_contenido = [i for i in items if i in config["tipos_contenido"]]
    data["supercategoria[tipo_de_contenido]"] = "; ".join(tipos_contenido) if tipos_contenido else np.nan

    # =========================
    # AREA (solo Altxor)
    # =========================
    if config.get("areas") and tipo_perfil in config.get("perfiles_con_area", []):
        data["supercategoria[Área]"] = next(
            (i for i in items if i in config["areas"]),
            np.nan
        )

    # =========================
    # FORMATO (solo Altxor)
    # =========================
    if config.get("formatos") and tipo_perfil == "Recurso web":
        data["supercategoria[Formato]"] = next(
            (i for i in items if i in config["formatos"]),
            np.nan
        )

    # =========================
    # TIPO DE ESPACIO (solo Altxor)
    # =========================
    if config.get("tipos_espacio") and tipo_perfil in ["Productos o servicios", "Producto o servicio"]:
        data["supercategoria[tipo_de_espacio]"] = next(
            (i for i in items if i in config["tipos_espacio"]),
            np.nan
        )

    # =========================
    # EXTRA CATEGORIA CONTENIDO
    # =========================
    data["extra[categoria_contenido]"] = clasificar_categoria_contenido(tipo_perfil)

    return pd.Series(data)


# =========================
# MAIN MULTI-COMUNIDAD
# =========================
def main():

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    for carpeta in RAW_DIR.iterdir():

        if not carpeta.is_dir():
            continue

        comunidad = carpeta.name

        print(f"\nProcesando comunidad: {comunidad}")

        if comunidad == "konektalan":
            from config.konektalan import CONFIG
        elif comunidad == "altxor":
            from config.altxor import CONFIG
        else:
            print(f"Comunidad desconocida: {comunidad}")
            continue

        archivo = carpeta / "resources_raw.csv"

        if not archivo.exists():
            print(f"No se encontró resources_raw.csv en {comunidad}")
            continue

        df = pd.read_csv(archivo)
        df.columns = df.columns.str.strip()

        df = resolver_columnas_duplicadas(df)

        nuevas_columnas = df.apply(
            lambda row: procesar_fila(row, CONFIG),
            axis=1
        )

        df = pd.concat([df, nuevas_columnas], axis=1)

        output_file = PROCESSED_DIR / f"resources_processed_{comunidad}.csv"

        df.to_csv(output_file, index=False)

        print(f"Generado: {output_file.name}")

    print("\nProceso completado correctamente.")


if __name__ == "__main__":
    main()







