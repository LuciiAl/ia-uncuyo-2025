import pandas as pd
import numpy as np

# ============================================================
# 4(a) Función para generar columna prediction_prob
# ============================================================
def add_random_probabilities(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega una nueva columna 'prediction_prob' con valores aleatorios uniformes entre 0 y 1.
    """
    df["prediction_prob"] = np.random.rand(len(df))
    return df


# ============================================================
# 4(b) Función random_classifier
# ============================================================
def random_classifier(df: pd.DataFrame) -> pd.DataFrame:
    """
    Recibe un DataFrame y genera una columna 'prediction_class':
      - 1 si prediction_prob > 0.5
      - 0 en caso contrario
    Devuelve el DataFrame con las columnas agregadas.
    """
    if "prediction_prob" not in df.columns:
        df = add_random_probabilities(df)
    df["prediction_class"] = np.where(df["prediction_prob"] > 0.5, 1, 0)
    return df


# ============================================================
# 4(c) Aplicar clasificador al dataset de validación
# ============================================================
if __name__ == "__main__":
    DATA_PATH = "data/arbolado-mendoza-dataset-validation.csv"
    OUT_PATH = "data/arbolado-mendoza-dataset-validation-random.csv"

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

    # Aplicar clasificador aleatorio
    df = random_classifier(df)

    # Guardar el nuevo CSV con columnas agregadas
    df.to_csv(OUT_PATH, index=False, encoding="utf-8")
    print(f"✅ Archivo generado: {OUT_PATH}")
    print(df.head())
