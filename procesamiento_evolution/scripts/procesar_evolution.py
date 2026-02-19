import pandas as pd
from pathlib import Path
import os


# =========================
# RUTAS
# =========================

REPO_ROOT = Path(os.getcwd())

RAW_DIR = REPO_ROOT / "procesamiento_evolution" / "data" / "raw"
PROCESSED_DIR = REPO_ROOT / "procesamiento_evolution" / "data" / "processed"
OUTPUT_FILE = PROCESSED_DIR / "evolution_data_processed.csv"


# =========================
# UNIFICAR COLUMNA MES
# =========================
def unificar_columna_mes(df):

    columnas_mes = [col for col in df.columns if col.lower().startswith("mes_")]

    if not columnas_mes:
        print("No se encontraron columnas mes_*")
        return df

    columna_principal = columnas_mes[0]

    # Crear columna mes general
    df["mes"] = df[columna_principal]

    # Intentar conversión segura a datetime
    try:
        df["mes"] = pd.to_datetime(df["mes"], errors="raise")
        print("Columna mes convertida a datetime correctamente.")
    except Exception:
        print("No se pudo convertir mes a datetime. Se mantiene como texto.")

    # Eliminar columnas mes_*
    df = df.drop(columns=columnas_mes)

    # Colocar mes como primera columna
    columnas_finales = ["mes"] + [col for col in df.columns if col != "mes"]
    df = df[columnas_finales]

    return df


# =========================
# ELIMINAR COLUMNAS ACUM1
# =========================
def eliminar_acum1(df):

    columnas_acum1 = [col for col in df.columns if col.startswith("Acum1_")]

    if columnas_acum1:
        print(f"Eliminando columnas duplicadas: {columnas_acum1}")
        df = df.drop(columns=columnas_acum1)

    return df


# =========================
# MAIN
# =========================
def main():

    print("=== PROCESAMIENTO EVOLUTION DATA ===")

    archivos_excel = list(RAW_DIR.glob("*.xlsx"))

    if not archivos_excel:
        print("No se encontraron archivos Excel en raw.")
        return

    archivo = archivos_excel[0]
    print(f"Leyendo archivo: {archivo.name}")

    # Leer hoja Datos con encabezado multinivel
    df_raw = pd.read_excel(
        archivo,
        sheet_name="Datos",
        header=[0, 1]
    )

    # Construcción de nombres de columnas
    nuevas_columnas = []

    for categoria, subheader in df_raw.columns:

        categoria = str(categoria).strip()
        subheader = str(subheader).strip()

        if subheader.lower() == "mes":
            nuevas_columnas.append(f"mes_{categoria.lower().replace(' ', '_')}")
        else:
            categoria_limpia = categoria.lower().replace(" ", "_")
            sub_limpio = subheader.replace(".", "").strip()
            nuevas_columnas.append(f"{sub_limpio}_{categoria_limpia}")

    df_raw.columns = nuevas_columnas

    # Aplicar limpieza
    df_final = unificar_columna_mes(df_raw)
    df_final = eliminar_acum1(df_final)

    # Crear carpeta si no existe
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Guardar resultado
    df_final.to_csv(OUTPUT_FILE, index=False)

    print("Archivo procesado correctamente.")
    print(f"Generado: {OUTPUT_FILE.name}")
    print(f"Tipo columna mes final: {df_final['mes'].dtype}")


if __name__ == "__main__":
    main()
