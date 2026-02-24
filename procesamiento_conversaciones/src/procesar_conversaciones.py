import pandas as pd
from pathlib import Path
import re

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

        # Usuarios.1 → Usuarios_num
        if col.startswith("Usuarios."):

            if pd.api.types.is_numeric_dtype(df[col]):
                nuevas_columnas[col] = "Usuarios_num"

        # Administradores.1 → Administradores_num
        elif col.startswith("Administradores."):

            if pd.api.types.is_numeric_dtype(df[col]):
                nuevas_columnas[col] = "Administradores_num"

    df = df.rename(columns=nuevas_columnas)

    return df


# =========================
# LIMPIEZA GENERAL
# =========================

def limpiar_columnas(df):
    df.columns = df.columns.str.strip()
    return df


# =========================
# MAIN
# =========================

def main():

    print("=== INICIO PROCESAMIENTO CONVERSACIONES ===")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    archivo = RAW_DIR / "conversaciones_raw.csv"

    if not archivo.exists():
        print("No se encontró conversaciones_raw.csv")
        return

    df = pd.read_csv(archivo)

    df = limpiar_columnas(df)
    df = renombrar_columnas_duplicadas(df)

    if "Comunidades" not in df.columns:
        print("No existe columna 'Comunidades'")
        return

    # Separar automáticamente por comunidad
    comunidades = df["Comunidades"].dropna().unique()

    for comunidad in comunidades:

        df_comunidad = df[df["Comunidades"] == comunidad].copy()

        nombre_comunidad = comunidad.lower().replace(" ", "_")

        output_file = PROCESSED_DIR / f"conversaciones_processed_{nombre_comunidad}.csv"

        df_comunidad.to_csv(output_file, index=False)

        print(f"Generado: {output_file.name}")

    print("\n=== PROCESO CONVERSACIONES COMPLETADO ===")


if __name__ == "__main__":
    main()
