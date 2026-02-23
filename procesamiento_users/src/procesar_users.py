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
# RESOLVER COLUMNAS DUPLICADAS
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
            for col in no_numericas[1:]:
                nuevas_columnas[col] = f"{base}_text"
        else:
            nuevas_columnas[columnas[0]] = base

        for col in numericas:
            nuevas_columnas[col] = f"{base}_num"

    df = df.rename(columns=nuevas_columnas)

    return df


# =========================
# LIMPIAR NOMBRE COLUMNA
# =========================

def limpiar_nombre(texto):

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
# ONE HOT GENERICO
# =========================

def aplicar_one_hot(df, columna_original, prefijo):

    if columna_original not in df.columns:
        print(f"No existe la columna {columna_original}")
        return df

    valores = set()

    for fila in df[columna_original].fillna(""):
        items = [i.strip() for i in str(fila).split(",") if i.strip()]
        for item in items:
            valores.add(item)

    for valor in valores:
        nombre_col = f"{prefijo}_{limpiar_nombre(valor)}"
        df[nombre_col] = df[columna_original].apply(
            lambda x: 1 if valor in str(x) else 0
        )

    return df


# =========================
# MAIN MULTI-COMUNIDAD
# =========================

def main():

    print("=== INICIO PROCESAMIENTO USERS ===")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    if not RAW_DIR.exists():
        print("No existe carpeta raw")
        return

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

        # 2️⃣ One hot Canales
        df = aplicar_one_hot(
            df,
            "Canales a los que está suscrito",
            "canal"
        )

        # 3️⃣ One hot Perfiles
        df = aplicar_one_hot(
            df,
            "Perfiles",
            "perfil"
        )

        output_file = PROCESSED_DIR / f"users_processed_{comunidad}.csv"

        df.to_csv(output_file, index=False)

        print(f"Generado: {output_file.name}")

    print("\n=== PROCESO USERS COMPLETADO ===")


if __name__ == "__main__":
    main()
