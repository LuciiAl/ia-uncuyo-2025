import os
import numpy as np
import pandas as pd

# ============================================================
# TP7B – Clasificador Aleatorio (Ejercicio 4)
# ============================================================

def normalize_class_column(df):
    mapping = {"si": 1, "SI": 1, "Si": 1,
               "no": 0, "NO": 0, "No": 0}
    df = df.replace({"inclinacion_peligrosa": mapping})
    return df.astype({"inclinacion_peligrosa": int})

def add_random_probabilities(df):
    df["prediction_prob"] = np.random.rand(len(df))
    return df

def random_classifier(df):
    if "prediction_prob" not in df.columns:
        df = add_random_probabilities(df)
    df["prediction_class"] = np.where(df["prediction_prob"] > 0.5, 1, 0)
    return df

def save_output(df, out_path):
    df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"✅ Archivo generado: {out_path}")

if __name__ == "__main__":
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    DATA_PATH = os.path.join(ROOT, "data", "arbolado-mendoza-dataset-validation.csv")
    OUT_PATH = os.path.join(ROOT, "data", "arbolado-mendoza-dataset-validation-random.csv")

    try:
        df = pd.read_csv(DATA_PATH)
        df.columns = [c.lower().strip() for c in df.columns]

        df = normalize_class_column(df)
        df = random_classifier(df)
        save_output(df, OUT_PATH)

    except Exception as e:
        print(f"❌ Error procesando archivo: {e}")
