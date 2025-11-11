import os

# ============================================================
# CONFIGURACIÓN DE RUTAS
# ============================================================
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # .../tp7-ml
REPORT = os.path.join(ROOT, "tp7B-clasificadores.md")

# ============================================================
# CONTENIDO DEL ARCHIVO MARKDOWN
# ============================================================

md = []

md.append("# TP7B – Clasificadores")
md.append("")
md.append("---")
md.append("")
md.append("## 4. Clasificador Aleatorio")
md.append("")
md.append("### 4(a–c) Implementación en Python")
md.append("```python")
md.append("""import pandas as pd
import numpy as np

def add_random_probabilities(df: pd.DataFrame) -> pd.DataFrame:
    df["prediction_prob"] = np.random.rand(len(df))
    return df

def random_classifier(df: pd.DataFrame) -> pd.DataFrame:
    if "prediction_prob" not in df.columns:
        df = add_random_probabilities(df)
    df["prediction_class"] = np.where(df["prediction_prob"] > 0.5, 1, 0)
    return df

if __name__ == "__main__":
    DATA_PATH = "data/arbolado-mendoza-dataset-validation.csv"
    OUT_PATH = "data/arbolado-mendoza-dataset-validation-random.csv"

    df = pd.read_csv(DATA_PATH)
    df.columns = [c.strip().lower() for c in df.columns]
    if "inclinacion_peligrosa" in df.columns:
        df["inclinacion_peligrosa"] = (
            df["inclinacion_peligrosa"]
            .replace({"SI": 1, "No": 0, "NO": 0, "no": 0, "si": 1})
            .astype(int)
        )

    df = random_classifier(df)
    df.to_csv(OUT_PATH, index=False, encoding="utf-8")
    print(f"✅ Archivo generado: {OUT_PATH}")
""")
md.append("```")
md.append("")
md.append("### 4(d) Cálculo de matriz de confusión en R (`dplyr`)")
md.append("```r")
md.append("""library(dplyr)

df <- read.csv("data/arbolado-mendoza-dataset-validation-random.csv")

resultados <- df %>%
  summarise(
    TP = sum(inclinacion_peligrosa == 1 & prediction_class == 1),
    TN = sum(inclinacion_peligrosa == 0 & prediction_class == 0),
    FP = sum(inclinacion_peligrosa == 0 & prediction_class == 1),
    FN = sum(inclinacion_peligrosa == 1 & prediction_class == 0)
  )

print(resultados)

matriz_conf <- matrix(
  c(resultados$TN, resultados$FP,
    resultados$FN, resultados$TP),
  nrow = 2,
  byrow = TRUE
)

colnames(matriz_conf) <- c("Predicted: NO", "Predicted: YES")
rownames(matriz_conf) <- c("Actual: NO", "Actual: YES")

cat("\\nMatriz de confusión:\\n")
print(matriz_conf)
cat("\\nTotal de observaciones:", nrow(df), "\\n")
""")
md.append("```")
md.append("")
md.append("---")
md.append("")
md.append("## 5. Clasificador por Clase Mayoritaria")
md.append("")
md.append("### 5(a–b) Implementación en Python")
md.append("```python")
md.append("""import pandas as pd

def biggerclass_classifier(df: pd.DataFrame) -> pd.DataFrame:
    if "inclinacion_peligrosa" not in df.columns:
        raise ValueError("El DataFrame no contiene la columna 'inclinacion_peligrosa'")
    majority_class = df["inclinacion_peligrosa"].mode()[0]
    print(f"Clase mayoritaria detectada: {majority_class}")
    df["prediction_class"] = majority_class
    return df

if __name__ == "__main__":
    DATA_PATH = "data/arbolado-mendoza-dataset-validation.csv"
    OUT_PATH = "data/arbolado-mendoza-dataset-validation-biggerclass.csv"

    df = pd.read_csv(DATA_PATH)
    df.columns = [c.strip().lower() for c in df.columns]
    if "inclinacion_peligrosa" in df.columns:
        df["inclinacion_peligrosa"] = (
            df["inclinacion_peligrosa"]
            .replace({"SI": 1, "No": 0, "NO": 0, "no": 0, "si": 1})
            .astype(int)
        )

    df = biggerclass_classifier(df)
    df.to_csv(OUT_PATH, index=False, encoding="utf-8")
    print(f"✅ Archivo generado: {OUT_PATH}")
""")
md.append("```")
md.append("")
md.append("### 5(d) Cálculo de matriz de confusión en R (`dplyr`)")
md.append("```r")
md.append("""library(dplyr)

df <- read.csv("data/arbolado-mendoza-dataset-validation-biggerclass.csv")

resultados <- df %>%
  summarise(
    TP = sum(inclinacion_peligrosa == 1 & prediction_class == 1),
    TN = sum(inclinacion_peligrosa == 0 & prediction_class == 0),
    FP = sum(inclinacion_peligrosa == 0 & prediction_class == 1),
    FN = sum(inclinacion_peligrosa == 1 & prediction_class == 0)
  )

print(resultados)

matriz_conf <- matrix(
  c(resultados$TN, resultados$FP,
    resultados$FN, resultados$TP),
  nrow = 2,
  byrow = TRUE
)

colnames(matriz_conf) <- c("Predicted: NO", "Predicted: YES")
rownames(matriz_conf) <- c("Actual: NO", "Actual: YES")

cat("\\nMatriz de confusión:\\n")
print(matriz_conf)
cat("\\nTotal de observaciones:", nrow(df), "\\n")
""")
md.append("```")
md.append("")
md.append("---")
md.append("*Archivo generado automáticamente a partir de los clasificadores implementados en Python y las matrices calculadas en R.*")

# ============================================================
# GUARDAR ARCHIVO
# ============================================================
os.makedirs(os.path.dirname(REPORT), exist_ok=True)
with open(REPORT, "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print(f"✅ Reporte generado correctamente en: {REPORT}")
