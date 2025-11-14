# ============================================================
# TP7B – 5(d) Matriz de confusión para el Clasificador por Clase Mayoritaria
# ============================================================

library(dplyr)

# --------------------- CONFIGURACIÓN -------------------------
ROOT <- "data"
DATA_PATH <- file.path(ROOT, "arbolado-mendoza-dataset-validation-biggerclass.csv")
OUT_CSV   <- file.path(ROOT, "confusion_biggerclass_results.csv")
OUT_MD    <- "tp7B-clasificadores-biggerclass.md"

# ----------------------- CARGA DE DATOS ----------------------
if (!file.exists(DATA_PATH)) {
  stop(paste("❌ No se encontró el archivo:", DATA_PATH))
}

df <- read.csv(DATA_PATH)

# ------------------- CÁLCULO DE MÉTRICAS ----------------------
conf <- df %>%
  summarise(
    TP = sum(inclinacion_peligrosa == 1 & prediction_class == 1),
    TN = sum(inclinacion_peligrosa == 0 & prediction_class == 0),
    FP = sum(inclinacion_peligrosa == 0 & prediction_class == 1),
    FN = sum(inclinacion_peligrosa == 1 & prediction_class == 0)
  )

# ------------------- MATRIZ DE CONFUSIÓN ----------------------
matriz_conf <- matrix(
  c(conf$TN, conf$FP,
    conf$FN, conf$TP),
  nrow = 2,
  byrow = TRUE
)

colnames(matriz_conf) <- c("Predicted: NO", "Predicted: YES")
rownames(matriz_conf) <- c("Actual: NO", "Actual: YES")

# ------------------------- GUARDADO ----------------------------
write.csv(conf, OUT_CSV, row.names = FALSE)

md <- c(
  "# TP7B – Clasificador por Clase Mayoritaria",
  "",
  "## 5(d) Matriz de Confusión",
  "",
  "|                | Predicted: NO | Predicted: YES |",
  "|----------------|---------------|----------------|",
  sprintf("| **Actual: NO**  | %d | %d |", conf$TN, conf$FP),
  sprintf("| **Actual: YES** | %d | %d |", conf$FN, conf$TP),
  "",
  sprintf("**Total de observaciones:** %d", nrow(df)),
  "",
  "---",
  "*Matriz generada a partir del clasificador por clase mayoritaria.*"
)

writeLines(md, OUT_MD)

# ----------------------- SALIDA EN CONSOLA --------------------
cat("\n📊 Matriz de confusión (Clasificador por Clase Mayoritaria):\n")
print(matriz_conf)

cat("\nTotales por categoría:\n")
print(conf)

cat(paste0("\n✅ Resultados guardados en:\n",
           "- ", OUT_CSV, "\n",
           "- ", OUT_MD, "\n"))
