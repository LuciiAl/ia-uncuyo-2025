# ============================================================
# 4(d) Matriz de confusión para el clasificador aleatorio
# ============================================================

library(dplyr)

# -------- CONFIGURACIÓN --------
DATA_PATH <- "data/arbolado-mendoza-dataset-validation-random.csv"
OUT_CSV   <- "data/confusion_random_results.csv"
OUT_MD    <- "tp7B-clasificadores-random.md"

# -------- CARGA DE DATOS --------
df <- read.csv(DATA_PATH)

# -------- CÁLCULO DE MÉTRICAS --------
resultados <- df %>%
  summarise(
    TP = sum(inclinacion_peligrosa == 1 & prediction_class == 1),
    TN = sum(inclinacion_peligrosa == 0 & prediction_class == 0),
    FP = sum(inclinacion_peligrosa == 0 & prediction_class == 1),
    FN = sum(inclinacion_peligrosa == 1 & prediction_class == 0)
  )

# -------- MATRIZ DE CONFUSIÓN --------
matriz_conf <- matrix(
  c(resultados$TN, resultados$FP,
    resultados$FN, resultados$TP),
  nrow = 2,
  byrow = TRUE
)
colnames(matriz_conf) <- c("Predicted: NO", "Predicted: YES")
rownames(matriz_conf) <- c("Actual: NO", "Actual: YES")

# -------- GUARDAR RESULTADOS --------
write.csv(resultados, OUT_CSV, row.names = FALSE)

# Generar archivo Markdown
md <- c(
  "# TP7B – Clasificador Aleatorio",
  "",
  "## 4(d) Matriz de confusión",
  "",
  "|                | Predicted: NO | Predicted: YES |",
  "|----------------|---------------|----------------|",
  paste0("| **Actual: NO** | ", resultados$TN, " | ", resultados$FP, " |"),
  paste0("| **Actual: YES** | ", resultados$FN, " | ", resultados$TP, " |"),
  "",
  paste0("**Total de observaciones:** ", nrow(df)),
  "",
  "---",
  "*Archivo generado automáticamente por `confusion_random.R`*"
)

writeLines(md, OUT_MD)

# -------- IMPRESIÓN EN CONSOLA --------
cat("\n📊 Matriz de confusión (Clasificador Aleatorio):\n")
print(matriz_conf)
cat("\nTotales:\n")
print(resultados)
cat(paste0("\n✅ Guardado: ", OUT_CSV, " y ", OUT_MD, "\n"))
