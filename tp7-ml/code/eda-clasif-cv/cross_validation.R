# ============================================================
# TP7B - Validación Cruzada (punto e.i)
# ============================================================
# Funciones: create_folds() y cross_validation()
# ------------------------------------------------------------
# Este script genera un archivo tp7B-cv.md con el código
# documentado de ambas funciones, en formato Markdown.
# ============================================================

library(dplyr)

# -------- FUNCIÓN create_folds() --------
# Crea una lista de folds para validación cruzada K-Fold.
# Cada fold contiene índices de observaciones de validación.
create_folds <- function(data, k = 5, seed = 123) {
  set.seed(seed)
  n <- nrow(data)
  indices <- sample(1:n)
  folds <- split(indices, cut(seq_along(indices), k, labels = FALSE))
  return(folds)
}

# -------- FUNCIÓN cross_validation() --------
# Realiza un esquema general de validación cruzada.
# Aplica una función "train_function" sobre los datos de entrenamiento
# y evalúa en el conjunto de validación, acumulando métricas.
cross_validation <- function(data, k = 5, train_function, metric_function, seed = 123) {
  folds <- create_folds(data, k, seed)
  metricas <- list()
  
  for (i in 1:k) {
    cat(paste0("Fold ", i, "/", k, "...\n"))
    val_idx <- folds[[i]]
    train_data <- data[-val_idx, ]
    val_data <- data[val_idx, ]
    
    modelo <- train_function(train_data)
    pred <- modelo(val_data)
    
    metricas[[i]] <- metric_function(val_data$inclinacion_peligrosa, pred)
  }
  
  metricas_df <- bind_rows(metricas)
  resumen <- metricas_df %>%
    summarise(across(everything(), list(mean = mean, sd = sd)))
  
  return(list(metricas = metricas_df, resumen = resumen))
}

# ============================================================
# GENERACIÓN DEL ARCHIVO MARKDOWN
# ============================================================
OUT_MD <- "tp7B-cv.md"

md <- c(
  "# TP7B – Validación Cruzada",
  "",
  "## (e.i) Funciones `create_folds()` y `cross_validation()`",
  "",
  "```r",
  "# Crea una lista de folds para validación cruzada K-Fold",
  "create_folds <- function(data, k = 5, seed = 123) {",
  "  set.seed(seed)",
  "  n <- nrow(data)",
  "  indices <- sample(1:n)",
  "  folds <- split(indices, cut(seq_along(indices), k, labels = FALSE))",
  "  return(folds)",
  "}",
  "",
  "# Ejecuta validación cruzada con función de entrenamiento y métrica personalizada",
  "cross_validation <- function(data, k = 5, train_function, metric_function, seed = 123) {",
  "  folds <- create_folds(data, k, seed)",
  "  metricas <- list()",
  "  ",
  "  for (i in 1:k) {",
  "    cat(paste0('Fold ', i, '/', k, '...\\n'))",
  "    val_idx <- folds[[i]]",
  "    train_data <- data[-val_idx, ]",
  "    val_data <- data[val_idx, ]",
  "    ",
  "    modelo <- train_function(train_data)",
  "    pred <- modelo(val_data)",
  "    ",
  "    metricas[[i]] <- metric_function(val_data$inclinacion_peligrosa, pred)",
  "  }",
  "  ",
  "  metricas_df <- bind_rows(metricas)",
  "  resumen <- metricas_df %>%",
  "    summarise(across(everything(), list(mean = mean, sd = sd)))",
  "  ",
  "  return(list(metricas = metricas_df, resumen = resumen))",
  "}",
  "```",
  "",
  "---",
  "*Archivo generado automáticamente por `cross_validation.R`*"
)

writeLines(md, OUT_MD)
cat(paste("✅ Reporte generado:", OUT_MD, "\n"))
