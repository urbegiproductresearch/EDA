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
# FUNCIÓN PARA ELIMINAR MESES DUPLICADOS
# =========================
def unificar_columna_mes(df):

    # Detectar columnas tipo mes_*
    columnas_mes = [col for col in df.columns if col.lower().startswith("mes_")]

    if not columnas_mes:
        return df

    # Tomamos la primera como referencia
    columna_principal = columnas_mes[0]

    # Crear columna mes general
    df["mes"] = df[columna_principal]

    # Eliminar todas las columnas mes_*
    df = df.drop(columns=columnas_mes)

    # Mover mes al inicio
    columnas_finales = ["mes"] + [col for col in df.columns if col != "mes"]
    df = df[columnas_finales]

    return df


# =========================
# MAIN
# =========================
def main():

    print("=== PROCESAMIENTO EVOLUTION DATA ===")

    archivos_excel = list(RAW_DIR.glob("*.xlsx"))

    if not archivos_excel:
        print("No se encontraron archivos Excel.")
        return

    archivo = archivos_excel[0]
    print(f"Leyendo archivo: {archivo.name}")

    # Leer Excel con dos filas de encabezado
    df_raw = pd.read_excel(
        archivo,
        sheet_name="Datos",
        header=[0, 1]
    )

    # Construir nombres de columnas combinando los dos niveles
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

    # Aplicar eliminación de meses duplicados
    df_final = unificar_columna_mes(df_raw)

    # Guardar
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df_final.to_csv(OUTPUT_FILE, index=False)

    print("Archivo procesado correctamente.")
    print(f"Generado: {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()

