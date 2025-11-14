# ============================================================
# TP7B – 4(d) Matriz de confusión para el Clasificador Aleatorio
# ============================================================

library(dplyr)

# --------------------- CONFIGURACIÓN -------------------------
ROOT <- "data"
DATA_PATH <- file.path(ROOT, "arbolado-mendoza-dataset-validation-random.csv")
OUT_CSV   <- file.path(ROOT, "confusion_random_results.csv")
OUT_MD    <- "tp7B-clasificadores-random.md"

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
  "# TP7B – Clasificador Aleatorio",
  "",
  "## 4(d) Matriz de Confusión",
  "",
  "|                | Predicted: NO | Predicted: YES |",
  "|----------------|---------------|----------------|",
  sprintf("| **Actual: NO**  | %d | %d |", conf$TN, conf$FP),
  sprintf("| **Actual: YES** | %d | %d |", conf$FN, conf$TP),
  "",
  sprintf("**Total de observaciones:** %d", nrow(df)),
  "",
  "---",
  "*Resultados generados automáticamente a partir del clasificador aleatorio.*"
)

writeLines(md, OUT_MD)

# ----------------------- SALIDA EN CONSOLA --------------------
cat("\n📊 Matriz de confusión (Clasificador Aleatorio):\n")
print(matriz_conf)

cat("\nTotales por categoría:\n")
print(conf)

cat(paste0("\n✅ Resultados guardados en:\n",
           "- ", OUT_CSV, "\n",
           "- ", OUT_MD, "\n"))
