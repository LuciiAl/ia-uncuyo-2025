import pandas as pd
import os

# ============================================================
# CONFIG
# ============================================================
DATA_PATH = "data/arbolado-mendoza-dataset.csv"  # ruta original
OUTPUT_DIR = os.path.dirname(DATA_PATH)

TRAIN_FILE = os.path.join(OUTPUT_DIR, "arbolado-mendoza-dataset-train.csv")
VAL_FILE = os.path.join(OUTPUT_DIR, "arbolado-mendoza-dataset-validation.csv")

# ============================================================
# CARGAR Y DIVIDIR
# ============================================================
# Leer CSV original
df = pd.read_csv(DATA_PATH)

# Barajar los datos (aleatoriamente, distribución uniforme)
df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Calcular tamaño de validación (20 %)
n_total = len(df_shuffled)
n_val = int(0.2 * n_total)

# Dividir en conjuntos
df_val = df_shuffled.iloc[:n_val]
df_train = df_shuffled.iloc[n_val:]

# ============================================================
# GUARDAR RESULTADOS
# ============================================================
df_train.to_csv(TRAIN_FILE, index=False)
df_val.to_csv(VAL_FILE, index=False)

print(f"✅ División completada:")
print(f"- Train (80%): {len(df_train)} registros → {TRAIN_FILE}")
print(f"- Validation (20%): {len(df_val)} registros → {VAL_FILE}")
