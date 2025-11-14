import os
import pandas as pd

# ============================================================
# TP7B – Clasificador por Clase Mayoritaria (Ejercicio 5)
# ============================================================

def normalize_class_column(df):
    """Normaliza la columna inclinacion_peligrosa a valores 0/1."""
    mapping = {"si": 1, "SI": 1, "Si": 1,
               "no": 0, "NO": 0, "No": 0}
    return df.replace({"inclinacion_peligrosa": mapping}).astype({"inclinacion_peligrosa": int})

def detect_majority_class(df):
    """Devuelve la clase mayoritaria del dataframe."""
    return df["inclinacion_peligrosa"].mode()[0]

def biggerclass_classifier(df):
    """
    Asigna a todas las observaciones la clase mayoritaria.
    """
    majority = detect_majority_class(df)
    df["prediction_class"] = majority
    print(f"Clase mayoritaria detectada: {majority}")
    return df

def save_output(df, out_path):
    df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"✅ Archivo generado: {out_path}")

if __name__ == "__main__":
    ROOT = os.path.dirname(os.path.dirname(__file__))  # /tp7-ml
    DATA_PATH = os.path.join(ROOT, "data", "arbolado-mendoza-dataset-validation.csv")
    OUT_PATH = os.path.join(ROOT, "data", "arbolado-mendoza-dataset-validation-biggerclass.csv")

    try:
        df = pd.read_csv(DATA_PATH)
        df.columns = [c.lower().strip() for c in df.columns]

        df = normalize_class_column(df)
        df = biggerclass_classifier(df)
        save_output(df, OUT_PATH)

    except Exception as e:
        print(f"❌ Error procesando archivo: {e}")
