import pandas as pd
import numpy as np
import re
from pathlib import Path
from collections import defaultdict

# =========================
# RUTAS BASE
# =========================

BASE_DIR = Path(__file__).resolve().parent.parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


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
# PROCESAMIENTO GENERICO
# =========================
def procesar_fila(row, config):

    categorias = row.get("Categorías", "")
    tipo_perfil = str(row.get("Tipo de perfil", "")).strip()

    if pd.isna(categorias):
        categorias = ""

    items = [c.strip() for c in str(categorias).split(",") if c.strip()]

    data = {}

    # Base comunes
    data["supercategoria[Género]"] = next((i for i in items if i in config["generos"]), np.nan)

    edad_col = "supercategoria[Edad]"
    if config["nombre_comunidad"] == "altxor":
        edad_col = "supercategoria[Grupo_de_edad]"

    data[edad_col] = next((i for i in items if i in config["edades"]), np.nan)

    data["supercategoria[Rol]"] = next((i for i in items if i in config["roles"]), np.nan)

    data["supercategoria[Ámbito]"] = next((i for i in items if i in config["ambitos"]), np.nan)

    data["supercategoria[Canales]"] = "; ".join([i for i in items if i in config["canales"]]) or np.nan

    data["supercategoria[tipo_de_evento]"] = "; ".join([i for i in items if i in config["tipos_evento"]]) or np.nan

    data["supercategoria[tipo_de_contenido]"] = "; ".join([i for i in items if i in config["tipos_contenido"]]) or np.nan

    # Solo Altxor
    if config["areas"]:
        if tipo_perfil in config["perfiles_con_area"]:
            data["supercategoria[Área]"] = next((i for i in items if i in config["areas"]), np.nan)

    if config["formatos"]:
        if tipo_perfil == "Recurso web":
            data["supercategoria[Formato]"] = next((i for i in items if i in config["formatos"]), np.nan)

    if config["tipos_espacio"]:
        if tipo_perfil == "Productos o servicios":
            data["supercategoria[tipo_de_espacio]"] = next((i for i in items if i in config["tipos_espacio"]), np.nan)

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

        print(f"Procesando comunidad: {comunidad}")

        df = pd.read_csv(archivo)
        df.columns = df.columns.str.strip()

        df = resolver_columnas_duplicadas(df)

        nuevas_columnas = df.apply(lambda row: procesar_fila(row, CONFIG), axis=1)

        df = pd.concat([df, nuevas_columnas], axis=1)

        # Reordenar extras al final si existieran
        columnas_extra = [c for c in df.columns if c.startswith("extra[")]
        columnas_normales = [c for c in df.columns if not c.startswith("extra[")]

        df = df[columnas_normales + columnas_extra]

        output_file = PROCESSED_DIR / f"resources_processed_{comunidad}.csv"

        df.to_csv(output_file, index=False)

        print(f"Archivo generado: {output_file.name}")

    print("Proceso completado.")


if __name__ == "__main__":
    main()




