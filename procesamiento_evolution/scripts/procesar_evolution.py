mport pandas as pd
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

    # Leer sin cabecera para poder reconstruirla
    df_raw = pd.read_excel(archivo, sheet_name="Datos", header=None)

    # Fila 0 → Categorías (Usuarios, Descargas App, etc.)
    categorias = df_raw.iloc[0]

    # Fila 1 → Mes / Dato / Acum.
    subheaders = df_raw.iloc[1]

    # Datos reales desde fila 2
    df = df_raw.iloc[2:].reset_index(drop=True)

    nuevas_columnas = []

    for i in range(len(subheaders)):

        categoria = str(categorias[i]).strip()
        subheader = str(subheaders[i]).strip()

        if subheader.lower() == "mes":
            nuevas_columnas.append("mes")
        else:
            nombre_categoria = categoria.lower().replace(" ", "_")
            nombre_sub = subheader.replace(".", "").strip()
            nuevas_columnas.append(f"{nombre_sub}_{nombre_categoria}")

    df.columns = nuevas_columnas

    # Eliminar posibles columnas mes duplicadas
    columnas_mes = [col for col in df.columns if col == "mes"]

    if len(columnas_mes) > 1:
        df = df.loc[:, ~df.columns.duplicated()]

    # Mover mes a primera posición
    columnas_finales = ["mes"] + [col for col in df.columns if col != "mes"]
    df = df[columnas_finales]

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print("Archivo procesado correctamente.")
    print(f"Generado: {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()

