import os
import pandas as pd

# ============================================================
# TP7B – CREACIÓN DE DATASETS (TRAIN / VALIDATION)
# ============================================================

def load_dataset(path):
    """Carga el dataset original."""
    return pd.read_csv(path)

def split_dataset(df, val_ratio=0.20, seed=42):
    """Divide el dataset en train y validation."""
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    n_total = len(df)
    n_val = int(n_total * val_ratio)

    df_val = df.iloc[:n_val]
    df_train = df.iloc[n_val:]

    return df_train, df_val

def save_datasets(train, val, train_path, val_path):
    """Guarda los datasets generados."""
    train.to_csv(train_path, index=False)
    val.to_csv(val_path, index=False)

    print("✅ División completada:")
    print(f"- Train ({len(train)}) → {train_path}")
    print(f"- Validation ({len(val)}) → {val_path}")

if __name__ == "__main__":
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    DATA_PATH = os.path.join(ROOT, "data", "arbolado-mendoza-dataset.csv")

    TRAIN_PATH = os.path.join(ROOT, "data", "arbolado-mendoza-dataset-train.csv")
    VAL_PATH = os.path.join(ROOT, "data", "arbolado-mendoza-dataset-validation.csv")

    df = load_dataset(DATA_PATH)
    df_train, df_val = split_dataset(df, val_ratio=0.20, seed=42)
    save_datasets(df_train, df_val, TRAIN_PATH, VAL_PATH)
