# ============================================================
# GENERADOR DEL REPORTE tp7B-cv.md
# ============================================================

library(dplyr)

# ------------------------------------------------------------
# IMPORTAR RESULTADOS GENERADOS EN EL PASO ANTERIOR
# ------------------------------------------------------------

resumen <- read.csv("data/tp7B-cv-resumen.csv")

# ------------------------------------------------------------
# ARMAR TABLA EN MARKDOWN
# ------------------------------------------------------------

tabla_md <- paste0(
"| Métrica | Media | Desvío Estándar |\n",
"|---------|-------|-----------------|\n",
"| Accuracy | ", sprintf("%.4f", resumen$Accuracy), " | ", sprintf("%.4f", resumen$sd_Acc), " |\n",
"| Precision | ", sprintf("%.4f", resumen$Precision), " | ", sprintf("%.4f", resumen$sd_Pre), " |\n",
"| Sensitivity | ", sprintf("%.4f", resumen$Sensitivity), " | ", sprintf("%.4f", resumen$sd_Sens), " |\n",
"| Specificity | ", sprintf("%.4f", resumen$Specificity), " | ", sprintf("%.4f", resumen$sd_Spec), " |\n"
)

# ------------------------------------------------------------
# CÓDIGO DE LAS FUNCIONES (para incluir tal cual)
# ------------------------------------------------------------

codigo_folds <- "
```r
create_folds <- function(df, k = 5, seed = 123) {
  set.seed(seed)
  idx <- sample(seq_len(nrow(df)))
  split(idx, cut(seq_along(idx), breaks = k, labels = FALSE))
}

cross_validation <- function(df, k = 5) {

  folds <- create_folds(df, k)

  resultados <- data.frame(
    Fold = character(k),
    Accuracy = numeric(k),
    Precision = numeric(k),
    Sensitivity = numeric(k),
    Specificity = numeric(k),
    stringsAsFactors = FALSE
  )

  for (i in seq_len(k)) {
    test_idx <- folds[[i]]
    train_set <- df[-test_idx, ]
    test_set  <- df[test_idx, ]

    modelo <- rpart(
      formula_arbol,
      data   = train_set,
      method = 'class'
    )

    pred <- predict(modelo, test_set, type = 'class')

    tab <- table(Pred = pred, Real = test_set$inclinacion_peligrosa)

    TP <- tab['1', '1']
    TN <- tab['0', '0']
    FP <- tab['1', '0']
    FN <- tab['0', '1']

    acc  <- (TP + TN) / sum(tab)
    prec <- TP / (TP + FP)
    sens <- TP / (TP + FN)
    spec <- TN / (TN + FP)

    resultados[i, ] <- list(
      paste0('Fold', i),
      acc, prec, sens, spec
    )
  }

  resumen <- resultados %>%
    summarise(
      Accuracy     = mean(Accuracy),     sd_Acc  = sd(Accuracy),
      Precision    = mean(Precision),    sd_Pre  = sd(Precision),
      Sensitivity  = mean(Sensitivity),  sd_Sens = sd(Sensitivity),
      Specificity  = mean(Specificity),  sd_Spec = sd(Specificity)
    )

  list(
    resultados_por_fold = resultados,
    resumen_final = resumen
  )
}
```"

# ------------------------------------------------------------
# ARMAR ARCHIVO FINAL MD
# ------------------------------------------------------------

md <- c(
  "# TP7B – Validación Cruzada con Árbol de Decisión",
  "",
  "## (e.i) Código de las funciones",
  "",
  codigo_folds,
  "",
  "## (e.ii) Resultados del modelo (media y desvío estándar)",
  "",
  tabla_md,
  "",
  "---",
  "*Archivo generado automáticamente.*"
)

writeLines(md, "tp7B-cv.md")

cat("\n✅ Archivo generado: tp7B-cv.md\n")
