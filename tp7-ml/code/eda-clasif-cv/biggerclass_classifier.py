import pandas as pd
import numpy as np

# ============================================================
# 5(a) Función biggerclass_classifier
# ============================================================
def biggerclass_classifier(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clasificador por clase mayoritaria:
    - Determina la clase más frecuente en 'inclinacion_peligrosa'
    - Genera una columna 'prediction_class' asignando siempre esa clase
    Devuelve el DataFrame original con la nueva columna.
    """
    if "inclinacion_peligrosa" not in df.columns:
        raise ValueError("El DataFrame no contiene la columna 'inclinacion_peligrosa'")

    majority_class = df["inclinacion_peligrosa"].mode()[0]
    print(f"Clase mayoritaria detectada: {majority_class}")

    df["prediction_class"] = majority_class
    return df


# ============================================================
# 5(b) Aplicar clasificador al dataset de validación
# ============================================================
if __name__ == "__main__":
    DATA_PATH = "data/arbolado-mendoza-dataset-validation.csv"
    OUT_PATH = "data/arbolado-mendoza-dataset-validation-biggerclass.csv"

    # Cargar datos
    df = pd.read_csv(DATA_PATH)
    df.columns = [c.strip().lower() for c in df.columns]

    # Normalizar la clase real
    if "inclinacion_peligrosa" in df.columns:
        df["inclinacion_peligrosa"] = (
            df["inclinacion_peligrosa"]
            .replace({"SI": 1, "No": 0, "NO": 0, "no": 0, "si": 1})
            .astype(int)
        )

    # Aplicar clasificador por clase mayoritaria
    df = biggerclass_classifier(df)

    # Guardar dataset resultante
    df.to_csv(OUT_PATH, index=False, encoding="utf-8")
    print(f"✅ Archivo generado: {OUT_PATH}")
    print(df.head())
