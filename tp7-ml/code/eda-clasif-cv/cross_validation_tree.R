# ============================================================
# TP7B – Validación Cruzada con Árbol de Decisión (rpart)
# ============================================================

library(dplyr)
library(rpart)

# ------------------------------------------------------------
# (a) create_folds(): genera lista de índices para validación K-fold
# ------------------------------------------------------------
create_folds <- function(data, k = 5, seed = 123) {
  set.seed(seed)
  n <- nrow(data)
  indices <- sample(1:n)
  folds <- split(indices, cut(seq_along(indices), k, labels = FALSE))
  names(folds) <- paste0("Fold", 1:k)
  return(folds)
}

# ------------------------------------------------------------
# Funciones de métricas
# ------------------------------------------------------------
calc_metrics <- function(real, pred) {
  TP <- sum(real == 1 & pred == 1)
  TN <- sum(real == 0 & pred == 0)
  FP <- sum(real == 0 & pred == 1)
  FN <- sum(real == 1 & pred == 0)
  
  accuracy <- (TP + TN) / (TP + TN + FP + FN)
  precision <- ifelse((TP + FP) == 0, 0, TP / (TP + FP))
  sensitivity <- ifelse((TP + FN) == 0, 0, TP / (TP + FN))
  specificity <- ifelse((TN + FP) == 0, 0, TN / (TN + FP))
  
  return(data.frame(
    Accuracy = accuracy,
    Precision = precision,
    Sensitivity = sensitivity,
    Specificity = specificity
  ))
}

# ------------------------------------------------------------
# (b) cross_validation(): aplica árbol de decisión y evalúa métricas
# ------------------------------------------------------------
cross_validation <- function(data, k = 5, seed = 123) {
  folds <- create_folds(data, k, seed)
  resultados <- list()
  
  # Definimos fórmula de entrenamiento (como en el enunciado)
  formula_tree <- formula(inclinacion_peligrosa ~ altura + circ_tronco_cm + lat + long + seccion + especie)
  
  for (i in 1:k) {
  cat(paste0("🌀 Ejecutando Fold ", i, "/", k, "...\n"))
  
  test_idx <- folds[[i]]
  data_train <- data[-test_idx, ]
  data_val <- data[test_idx, ]
  
  # Entrenar modelo
  modelo <- rpart(formula_tree, data = data_train, method = "class")
  
  # 🔧 Alinear factores (eliminar niveles nuevos no presentes en el entrenamiento)
  for (col in c("seccion", "especie")) {
    if (is.factor(data_val[[col]])) {
      # Dejar solo los niveles que existen en el entrenamiento
      data_val[[col]] <- factor(
        data_val[[col]],
        levels = intersect(levels(data_val[[col]]), levels(data_train[[col]]))
      )
    }
  }
  
  # ⚙️ Eliminar filas con NA en factores desconocidos
  data_val <- data_val[complete.cases(data_val[, c("seccion", "especie")]), ]
  if (nrow(data_val) == 0) next  # salta el fold si se vacía
  
  # Predicción segura
  suppressWarnings({
    pred <- tryCatch(
      predict(modelo, data_val, type = "class"),
      error = function(e) {
        warning(paste("⚠️ Fold", i, "omitido por niveles no coincidentes"))
        return(factor(rep(NA, nrow(data_val))))
      }
    )
  })
  
  # Convertir predicción a binaria (1 = SI, 0 = NO)
  pred_bin <- as.numeric(pred == "SI")
  real_bin <- as.numeric(data_val$inclinacion_peligrosa == "SI")
  
  # Calcular métricas solo si hay datos válidos
  if (length(pred_bin) > 0 && length(real_bin) > 0) {
    resultados[[i]] <- calc_metrics(real_bin, pred_bin)
  }
}


  
  metricas_df <- bind_rows(resultados)
  resumen <- metricas_df %>%
    summarise(across(everything(), list(Media = mean, SD = sd)))
  
  return(list(metricas = metricas_df, resumen = resumen))
}

# ------------------------------------------------------------
# (c) APLICACIÓN DE LA VALIDACIÓN CRUZADA
# ------------------------------------------------------------
DATA <- "data/arbolado-mendoza-dataset-train.csv"
df <- read.csv(DATA)

# Normalizamos nombres
df <- df %>% rename_with(tolower)

# Convertimos la clase objetivo a factor (requisito de rpart)
df$inclinacion_peligrosa <- ifelse(df$inclinacion_peligrosa %in% c("SI", "Si", "si", 1), "SI", "NO")
df$inclinacion_peligrosa <- as.factor(df$inclinacion_peligrosa)

# Verificamos que todas las columnas existan
required_cols <- c("inclinacion_peligrosa", "altura", "circ_tronco_cm", "lat", "long", "seccion", "especie")
missing_cols <- setdiff(required_cols, colnames(df))
if (length(missing_cols) > 0) {
  stop(paste("❌ Faltan columnas necesarias en el dataset:", paste(missing_cols, collapse = ", ")))
}

# Ejecutar validación cruzada
resultado_cv <- cross_validation(df, k = 5, seed = 123)

print("📊 Métricas por fold:")
print(resultado_cv$metricas)
print("📈 Promedios y desviaciones estándar:")
print(resultado_cv$resumen)


# ------------------------------------------------------------
# (d) GENERACIÓN DEL ARCHIVO MARKDOWN
# ------------------------------------------------------------
OUT_MD <- "tp7B-cv.md"

md <- c(
  "# TP7B – Validación Cruzada con Árbol de Decisión",
  "",
  "## (e.i) Funciones `create_folds()` y `cross_validation()`",
  "",
  "```r",
  "# Genera una lista de folds aleatorios para validación K-Fold",
  "create_folds <- function(data, k = 5, seed = 123) {",
  "  set.seed(seed)",
  "  n <- nrow(data)",
  "  indices <- sample(1:n)",
  "  folds <- split(indices, cut(seq_along(indices), k, labels = FALSE))",
  "  names(folds) <- paste0('Fold', 1:k)",
  "  return(folds)",
  "}",
  "",
  "# Ejecuta validación cruzada con un árbol de decisión (rpart)",
  "cross_validation <- function(data, k = 5, seed = 123) {",
  "  folds <- create_folds(data, k, seed)",
  "  resultados <- list()",
  "  formula_tree <- formula(inclinacion_peligrosa ~ altura + circ_tronco_cm + lat + long + seccion + especie)",
  "  for (i in 1:k) {",
  "    test_idx <- folds[[i]]",
  "    data_train <- data[-test_idx, ]",
  "    data_val <- data[test_idx, ]",
  "    modelo <- rpart(formula_tree, data = data_train, method = 'class')",
  "    pred <- predict(modelo, data_val, type = 'class')",
  "    pred <- as.numeric(as.character(pred))",
  "    resultados[[i]] <- calc_metrics(data_val$inclinacion_peligrosa, pred)",
  "  }",
  "  metricas_df <- bind_rows(resultados)",
  "  resumen <- metricas_df %>%",
  "    summarise(across(everything(), list(Media = mean, SD = sd)))",
  "  return(list(metricas = metricas_df, resumen = resumen))",
  "}",
  "```",
  "",
  "## (e.ii) Resultados del Árbol de Decisión (rpart)",
  "",
  "| Métrica | Media | Desviación Estándar |",
  "|----------|-------:|-------------------:|"
)

# Agregar resultados a tabla Markdown
for (metrica in names(resultado_cv$resumen)) {
  valores <- resultado_cv$resumen[[metrica]]
  md <- append(md, sprintf("| %s | %.3f | %.3f |", metrica, valores[1], valores[2]))
}

md <- append(md, c("", "---", "*Archivo generado automáticamente por `cross_validation_tree.R`*"))

writeLines(md, OUT_MD)
cat(paste("✅ Reporte generado:", OUT_MD, "\n"))
