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
# CONFIG CANALES POR COMUNIDAD
# =========================

CANALES_CONFIG = {

    "konektalan": [
        "Trabajar en Euskadi",
        "Emprendimiento y autoempleo",
        "Oportunidades laborales",
        "Formación",
        "Guía de uso",
        "Ayudas y subvenciones",
        "Vivir en Euskadi",
        "Historias de vida",
        "Innovación en la empresa"
    ],

    "altxor": [
        "Salud y autonomía",
        "Mayores expatriados",
        "Cooperación al desarrollo",
        "Primeros pasos en Altxor Digital",
        "Experiencias vitales",
        "Iniciativas colectivas",
        "Seguridad y protección",
        "Ocio y actividad física",
        "Ecología, medioambiente y tecnología",
        "Participación, convivencia y voluntariado"
    ]
}


# =========================
# RESOLVER DUPLICADOS
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
# ONE HOT CANALES CONTROLADO
# =========================

def aplicar_one_hot_canales(df, comunidad):

    columna = "Canales a los que está suscrito"

    if columna not in df.columns:
        return df

    comunidad = comunidad.lower()

    if comunidad not in CANALES_CONFIG:
        return df

    canales_config = CANALES_CONFIG[comunidad]

    for canal in canales_config:

        nombre_col = f"canal[{canal}]"

        df[nombre_col] = df[columna].apply(
            lambda x: 1 if canal in str(x) else 0
        )

    return df


# =========================
# SEPARAR PERFILES → extra[]
# =========================

def separar_perfiles(df):

    columna = "Perfiles"

    if columna not in df.columns:
        return df

    perfiles_lista = []
    max_perfiles = 0

    for fila in df[columna].fillna(""):
        items = [i.strip() for i in str(fila).split(",") if i.strip()]
        perfiles_lista.append(items)
        if len(items) > max_perfiles:
            max_perfiles = len(items)

    nombres_columnas = [
        "extra[perfil_principal]",
        "extra[perfil_secundario]",
        "extra[perfil_terciario]",
        "extra[perfil_cuaternario]",
        "extra[perfil_quinto]"
    ]

    for i in range(min(max_perfiles, len(nombres_columnas))):
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

        # 2️⃣ One hot canales por comunidad
        df = aplicar_one_hot_canales(df, comunidad)

        # 3️⃣ Separar perfiles como extra[]
        df = separar_perfiles(df)

        output_file = PROCESSED_DIR / f"users_processed_{comunidad}.csv"

        df.to_csv(output_file, index=False)

        print(f"Generado: {output_file.name}")

    print("\n=== PROCESO USERS COMPLETADO ===")


if __name__ == "__main__":
    main()
