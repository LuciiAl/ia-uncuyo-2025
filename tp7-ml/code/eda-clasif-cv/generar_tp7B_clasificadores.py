import os

# ============================================================
# TP7B – Generador de Reporte para Clasificadores (Ej. 4 y 5)
# ============================================================

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
REPORT = os.path.join(ROOT, "tp7B-clasificadores.md")

md = []

# ------------------------------------------------------------
# ENCABEZADO
# ------------------------------------------------------------
md.append("# TP7B – Clasificadores Básicos")
md.append("")
md.append("Este informe resume la implementación y evaluación de los clasificadores solicitados:")
md.append("- Clasificador aleatorio")
md.append("- Clasificador por clase mayoritaria")
md.append("")
md.append("---")

# ------------------------------------------------------------
# SECCIÓN 4 – CLASIFICADOR ALEATORIO
# ------------------------------------------------------------
md.append("## 4. Clasificador Aleatorio")
md.append("")
md.append("El clasificador aleatorio asigna probabilidades uniformes en (0,1) y clasifica como `1` si `p > 0.5`.")
md.append("")

md.append("### Implementación (Python)")
md.append("```python")
md.append("""def random_classifier(df):
    df['prediction_prob'] = np.random.rand(len(df))
    df['prediction_class'] = (df['prediction_prob'] > 0.5).astype(int)
    return df
""")
md.append("```")

md.append("")
md.append("### Matriz de confusión (R)")
md.append("```r")
md.append("""df <- read.csv("data/arbolado-mendoza-dataset-validation-random.csv")

df %>%
  summarise(
    TP = sum(inclinacion_peligrosa==1 & prediction_class==1),
    TN = sum(inclinacion_peligrosa==0 & prediction_class==0),
    FP = sum(inclinacion_peligrosa==0 & prediction_class==1),
    FN = sum(inclinacion_peligrosa==1 & prediction_class==0)
  )
""")
md.append("```")
md.append("---")

# ------------------------------------------------------------
# SECCIÓN 5 – CLASIFICADOR POR CLASE MAYORITARIA
# ------------------------------------------------------------
md.append("## 5. Clasificador por Clase Mayoritaria")
md.append("")
md.append("Este clasificador asigna a todas las observaciones la clase más frecuente del conjunto de validación.")
md.append("")

md.append("### Implementación (Python)")
md.append("```python")
md.append("""def biggerclass_classifier(df):
    majority = df['inclinacion_peligrosa'].mode()[0]
    df['prediction_class'] = majority
    return df
""")
md.append("```")

md.append("")
md.append("### Matriz de confusión (R)")
md.append("```r")
md.append("""df <- read.csv("data/arbolado-mendoza-dataset-validation-biggerclass.csv")

df %>%
  summarise(
    TP = sum(inclinacion_peligrosa==1 & prediction_class==1),
    TN = sum(inclinacion_peligrosa==0 & prediction_class==0),
    FP = sum(inclinacion_peligrosa==0 & prediction_class==1),
    FN = sum(inclinacion_peligrosa==1 & prediction_class==0)
  )
""")
md.append("```")

md.append("")
md.append("---")
md.append("*Archivo generado automáticamente.*")

# ------------------------------------------------------------
# GUARDAR
# ------------------------------------------------------------
with open(REPORT, "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print(f"✅ Reporte generado en: {REPORT}")
