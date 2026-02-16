# =========================
# IMPORTS
# =========================
import pandas as pd
import numpy as np
from pathlib import Path


# =========================
# RUTAS
# =========================
BASE_DIR = Path(__file__).resolve().parent.parents[1]

INPUT_PATH = BASE_DIR / "procesamiento_evolution" / "data" / "raw" / "evolution_data_raw.xlsx"
OUTPUT_PATH = BASE_DIR / "procesamiento_evolution" / "data" / "processed" / "evolution_data_processed.csv"


# =========================
# FUNCIÓN PARA LIMPIAR NOMBRE CATEGORIA
# =========================
def limpiar_texto(texto):
    texto = str(texto).strip().lower()
    texto = texto.replace(" ", "_")
    texto = texto.replace(".", "")
    return texto


# =========================
# PIPELINE
# =========================
def main():

    print("Cargando hoja 'Datos'...")

    df = pd.read_excel(INPUT_PATH, sheet_name="Datos", header=None)

    # Fila 0 → categorías principales
    categorias = df.iloc[0]

    # Fila 1 → subcolumnas (Mes, Dato, Acum.)
    subcolumnas = df.iloc[1]

    # Propagar categorías hacia la derecha
    categorias = categorias.ffill()

    nuevas_columnas = []

    for cat, sub in zip(categorias, subcolumnas):

        # Ignorar columnas completamente vacías
        if pd.isna(cat) and pd.isna(sub):
            nuevas_columnas.append(None)
            continue

        if pd.isna(sub):
            nuevas_columnas.append(None)
            continue

        categoria_limpia = limpiar_texto(cat)
        sub_limpia = limpiar_texto(sub)

        nuevo_nombre = f"{sub_limpia}_{categoria_limpia}"
        nuevas_columnas.append(nuevo_nombre)

    # Eliminar primeras dos filas
    df = df.iloc[2:].copy()

    # Asignar nuevas columnas
    df.columns = nuevas_columnas

    # Eliminar columnas None (separadores vacíos)
    df = df.loc[:, df.columns.notna()]

    print("Guardando archivo procesado...")
    df.to_csv(OUTPUT_PATH, index=False)

    print("Proceso finalizado correctamente")


if __name__ == "__main__":
    main()
