# ============================================================
# TP7B – (e.i) Funciones de Validación Cruzada
# ============================================================

library(dplyr)

# ------------------------------------------------------------
# create_folds()
# Genera k subconjuntos (folds) para validación cruzada.
# ------------------------------------------------------------
create_folds <- function(data, k = 5, seed = 123) {
  set.seed(seed)
  n <- nrow(data)
  idx <- sample(seq_len(n))
  split(idx, cut(seq_along(idx), breaks = k, labels = FALSE))
}

# ------------------------------------------------------------
# cross_validation()
# Recibe:
#   - data: dataset completo
#   - train_function: función que entrena un modelo
#   - metric_function: función que calcula métricas
# Devuelve métricas por fold + resumen estadístico.
# ------------------------------------------------------------
cross_validation <- function(data, k = 5, train_function, metric_function, seed = 123) {
  
  folds <- create_folds(data, k, seed)
  metricas <- vector("list", k)

  for (i in seq_len(k)) {
    cat(sprintf("Procesando fold %d/%d...\n", i, k))

    val_idx <- folds[[i]]
    train_set <- data[-val_idx, ]
    val_set   <- data[val_idx, ]

    modelo <- train_function(train_set)
    prediccion <- modelo(val_set)

    metricas[[i]] <- metric_function(val_set$inclinacion_peligrosa, prediccion)
  }

  df_metricas <- bind_rows(metricas)

  resumen <- df_metricas %>%
    summarise(across(everything(), list(mean = mean, sd = sd)))

  list(metricas = df_metricas, resumen = resumen)
}

# ------------------------------------------------------------
# GENERACIÓN DEL ARCHIVO tp7B-cv.md (solo agrega el bloque)
# ------------------------------------------------------------

OUT_MD <- "tp7B-cv.md"

bloque_md <- c(
  "## (e.i) Funciones de Validación Cruzada",
  "",
  "Las funciones utilizadas para implementar un esquema general de *k-fold cross validation* son:",
  "",
  "```r",
  "create_folds <- function(data, k = 5, seed = 123) {",
  "  set.seed(seed)",
  "  idx <- sample(seq_len(nrow(data)))",
  "  split(idx, cut(seq_along(idx), k, labels = FALSE))",
  "}",
  "",
  "cross_validation <- function(data, k = 5, train_function, metric_function, seed = 123) {",
  "  folds <- create_folds(data, k, seed)",
  "  metricas <- vector('list', k)",
  "  ",
  "  for (i in seq_len(k)) {",
  "    val_idx <- folds[[i]]",
  "    modelo <- train_function(data[-val_idx, ])",
  "    pred <- modelo(data[val_idx, ])",
  "    metricas[[i]] <- metric_function(data$inclinacion_peligrosa[val_idx], pred)",
  "  }",
  "",
  "  df <- dplyr::bind_rows(metricas)",
  "  df %>% summarise(across(everything(), list(mean = mean, sd = sd)))",
  "}",
  "```",
  "",
  "---"
)

# Si el archivo no existe, se crea
if (!file.exists(OUT_MD)) writeLines("", OUT_MD)

# Agregar bloque al final
write( paste(bloque_md, collapse = "\n"), file = OUT_MD, append = TRUE )

cat("✅ Bloque agregado a tp7B-cv.md\n")
