import pandas as pd
import re
from pathlib import Path
from collections import defaultdict


# =========================
# RUTAS BASE
# =========================

CURRENT_FILE = Path(__file__).resolve()
BASE_DIR = CURRENT_FILE.parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_FILE = PROCESSED_DIR / "evolution_data_processed.csv"


# =========================
# RESOLVER COLUMNAS DUPLICADAS
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
# UNIFICAR COLUMNA MES
# =========================
def unificar_columna_mes(df):

    columnas_mes = [col for col in df.columns if col.lower().startswith("mes")]

    if not columnas_mes:
        print("No se encontraron columnas de mes.")
        return df

    columna_principal = columnas_mes[0]

    df["mes"] = df[columna_principal]

    df = df.drop(columns=columnas_mes)

    columnas_finales = ["mes"] + [col for col in df.columns if col != "mes"]
    df = df[columnas_finales]

    return df


# =========================
# MAIN
# =========================
def main():

    print("Procesando evolution data...")

    if not RAW_DIR.exists():
        print("No existe la carpeta raw.")
        return

    archivos_csv = list(RAW_DIR.glob("*.csv"))

    if not archivos_csv:
        print("No se encontraron archivos CSV en raw.")
        return

    print(f"Archivos detectados: {[f.name for f in archivos_csv]}")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Leer y concatenar todos los CSV encontrados
    dfs = []
    for archivo in archivos_csv:
        print(f"Leyendo {archivo.name}")
        df_temp = pd.read_csv(archivo)
        df_temp.columns = df_temp.columns.str.strip()
        dfs.append(df_temp)

    df = pd.concat(dfs, ignore_index=True)

    # Resolver duplicados
    df = resolver_columnas_duplicadas(df)

    # Unificar columna mes
    df = unificar_columna_mes(df)

    # Guardar archivo procesado
    df.to_csv(OUTPUT_FILE, index=False)

    print("Archivo procesado correctamente.")
    print(f"Generado: {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()

