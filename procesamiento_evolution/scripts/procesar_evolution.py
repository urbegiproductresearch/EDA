import pandas as pd
import re
from pathlib import Path
from collections import defaultdict
import os


# =========================
# RUTAS BASE
# =========================

REPO_ROOT = Path(os.getcwd())

RAW_DIR = REPO_ROOT / "procesamiento_evolution" / "data" / "raw"
PROCESSED_DIR = REPO_ROOT / "procesamiento_evolution" / "data" / "processed"
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
        print("⚠️ No se encontraron columnas que empiecen por 'mes'.")
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

    print("=== INICIO PROCESAMIENTO EVOLUTION ===")
    print(f"Buscando Excel en: {RAW_DIR}")

    if not RAW_DIR.exists():
        print("❌ No existe la carpeta raw.")
        return

    archivos_excel = list(RAW_DIR.glob("*.xlsx"))

    if not archivos_excel:
        print("❌ No se encontraron archivos .xlsx en raw.")
        return

    print(f"✔ Archivos detectados: {[f.name for f in archivos_excel]}")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    dfs = []
    for archivo in archivos_excel:
        print(f"Leyendo {archivo.name}")
        df_temp = pd.read_excel(archivo, sheet_name="Datos")
        df_temp.columns = df_temp.columns.str.strip()
        dfs.append(df_temp)

    df = pd.concat(dfs, ignore_index=True)

    df = resolver_columnas_duplicadas(df)
    df = unificar_columna_mes(df)

    df.to_csv(OUTPUT_FILE, index=False)

    print("✔ Archivo procesado correctamente.")
    print(f"Generado en: {OUTPUT_FILE}")
    print("=== FIN PROCESAMIENTO EVOLUTION ===")


if __name__ == "__main__":
    main()
