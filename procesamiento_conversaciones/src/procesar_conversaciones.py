import pandas as pd
from pathlib import Path

# =========================
# RUTAS BASE
# =========================

CURRENT_FILE = Path(__file__).resolve()
BASE_DIR = CURRENT_FILE.parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


# =========================
# RENOMBRAR COLUMNAS DUPLICADAS
# =========================

def renombrar_columnas_duplicadas(df):

    nuevas_columnas = {}

    for col in df.columns:

        if col.startswith("Usuarios.") and pd.api.types.is_numeric_dtype(df[col]):
            nuevas_columnas[col] = "Usuarios_num"

        elif col.startswith("Administradores.") and pd.api.types.is_numeric_dtype(df[col]):
            nuevas_columnas[col] = "Administradores_num"

    df = df.rename(columns=nuevas_columnas)

    return df


# =========================
# MAIN
# =========================

def main():

    print("=== INICIO PROCESAMIENTO CONVERSACIONES ===")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    for carpeta in RAW_DIR.iterdir():

        if not carpeta.is_dir():
            continue

        comunidad = carpeta.name
        print(f"\nProcesando comunidad: {comunidad}")

        archivo = carpeta / "conversaciones_raw.csv"

        if not archivo.exists():
            print(f"No se encontró conversaciones_raw.csv en {comunidad}")
            continue

        df = pd.read_csv(archivo)
        df.columns = df.columns.str.strip()

        df = renombrar_columnas_duplicadas(df)

        output_file = PROCESSED_DIR / f"conversaciones_processed_{comunidad}.csv"

        df.to_csv(output_file, index=False)

        print(f"Generado: {output_file.name}")

    print("\n=== PROCESO CONVERSACIONES COMPLETADO ===")


if __name__ == "__main__":
    main()
