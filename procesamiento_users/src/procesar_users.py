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


# =========================
# RESOLVER DUPLICADOS CORRECTAMENTE
# =========================

def resolver_columnas_duplicadas(df):

    grupos = defaultdict(list)

    for col in df.columns:
        base = re.sub(r"\.\d+$", "", col)
        grupos[base].append(col)

    nuevas_columnas = {}

    for base, columnas in grupos.items():

        if len(columnas) == 1:
            nuevas_columnas[columnas[0]] = base
            continue

        numericas = [c for c in columnas if pd.api.types.is_numeric_dtype(df[c])]
        no_numericas = [c for c in columnas if not pd.api.types.is_numeric_dtype(df[c])]

        if no_numericas:
            nuevas_columnas[no_numericas[0]] = base
        else:
            nuevas_columnas[columnas[0]] = base

        for col in numericas:
            nuevas_columnas[col] = f"{base}_num"

    df = df.rename(columns=nuevas_columnas)
    return df


# =========================
# LIMPIAR TEXTO
# =========================

def limpiar_texto(texto):

    texto = texto.lower().strip()
    texto = re.sub(r"[áàäâ]", "a", texto)
    texto = re.sub(r"[éèëê]", "e", texto)
    texto = re.sub(r"[íìïî]", "i", texto)
    texto = re.sub(r"[óòöô]", "o", texto)
    texto = re.sub(r"[úùüû]", "u", texto)
    texto = re.sub(r"ñ", "n", texto)
    texto = re.sub(r"[^a-z0-9]+", "_", texto)
    texto = texto.strip("_")

    return texto


# =========================
# ONE HOT CANALES (CORRECTO)
# =========================

def aplicar_one_hot_canales(df):

    columna = "Canales a los que está suscrito"

    if columna not in df.columns:
        return df

    valores = set()

    for fila in df[columna].fillna(""):
        items = [i.strip() for i in str(fila).split(",") if i.strip()]
        for item in items:
            valores.add(item)

    for valor in valores:

        nombre_col = f"supercategoria[canal_{limpiar_texto(valor)}]"

        df[nombre_col] = df[columna].apply(
            lambda x: 1 if valor in str(x) else 0
        )

    return df


# =========================
# SEPARAR PERFILES EN COLUMNAS ORDENADAS
# =========================

def separar_perfiles(df):

    columna = "Perfiles"

    if columna not in df.columns:
        return df

    # Obtener máximo número de perfiles en el dataset
    max_perfiles = 0

    perfiles_lista = []

    for fila in df[columna].fillna(""):
        items = [i.strip() for i in str(fila).split(",") if i.strip()]
        perfiles_lista.append(items)
        if len(items) > max_perfiles:
            max_perfiles = len(items)

    # Crear columnas dinámicamente
    nombres_columnas = [
        "supercategoria[perfil_principal]",
        "supercategoria[perfil_secundario]",
        "supercategoria[perfil_terciario]",
        "supercategoria[perfil_cuaternario]",
        "supercategoria[perfil_quinto]"
    ]

    for i in range(max_perfiles):
        if i < len(nombres_columnas):
            df[nombres_columnas[i]] = [
                perfiles[i] if i < len(perfiles) else None
                for perfiles in perfiles_lista
            ]

    return df


# =========================
# MAIN
# =========================

def main():

    print("=== INICIO PROCESAMIENTO USERS ===")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    for carpeta in RAW_DIR.iterdir():

        if not carpeta.is_dir():
            continue

        comunidad = carpeta.name
        print(f"\nProcesando comunidad: {comunidad}")

        archivo = carpeta / "users_raw.csv"

        if not archivo.exists():
            print(f"No se encontró users_raw.csv en {comunidad}")
            continue

        df = pd.read_csv(archivo, sep=",")

        df.columns = df.columns.str.strip()

        # 1️⃣ Resolver duplicados
        df = resolver_columnas_duplicadas(df)

        # 2️⃣ One hot canales
        df = aplicar_one_hot_canales(df)

        # 3️⃣ Separar perfiles
        df = separar_perfiles(df)

        output_file = PROCESSED_DIR / f"users_processed_{comunidad}.csv"

        df.to_csv(output_file, index=False)

        print(f"Generado: {output_file.name}")

    print("\n=== PROCESO USERS COMPLETADO ===")


if __name__ == "__main__":
    main()
