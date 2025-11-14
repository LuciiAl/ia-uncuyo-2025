# ============================================================
# TP7B – Cross Validation con Árboles de Decisión (rpart)
# ============================================================

library(dplyr)
library(rpart)

# ------------------------------------------------------------
# create_folds()
# ------------------------------------------------------------
create_folds <- function(df, k = 5, seed = 123) {
  set.seed(seed)
  idx <- sample(seq_len(nrow(df)))
  split(idx, cut(seq_along(idx), breaks = k, labels = FALSE))
}

# Fórmula con todas las variables que vamos a usar
formula_arbol <- inclinacion_peligrosa ~ 
  altura + circ_tronco_cm + circ_tronco_cm_cat +
  diametro_tronco + lat + long + seccion +
  especie + nombre_seccion + area_seccion

# ------------------------------------------------------------
# cross_validation() para rpart
# ------------------------------------------------------------
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

    # Entrenar árbol de CLASIFICACIÓN
    modelo <- rpart(
      formula_arbol,
      data   = train_set,
      method = "class"
    )

    # Predicciones de clase
    pred <- predict(modelo, test_set, type = "class")

    # Tabla de confusión
    tab <- table(Pred = pred, Real = test_set$inclinacion_peligrosa)

    TP <- tab["1", "1"]
    TN <- tab["0", "0"]
    FP <- tab["1", "0"]
    FN <- tab["0", "1"]

    acc  <- (TP + TN) / sum(tab)
    prec <- TP / (TP + FP)
    sens <- TP / (TP + FN)
    spec <- TN / (TN + FP)

    resultados[i, ] <- list(
      paste0("Fold", i),
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

# ------------------------------------------------------------
# CARGAR DATASET
# ------------------------------------------------------------

df <- read.csv("data/arbolado-mendoza-dataset-circ_tronco_cm-train.csv")

# ------------------------------------------------------------
# NORMALIZAR SOLO TIPO DE LA CLASE
# (YA VIENE COMO 0/1, SOLO LA PASAMOS A FACTOR)
# ------------------------------------------------------------

df$inclinacion_peligrosa <- factor(df$inclinacion_peligrosa, levels = c(0, 1))

# ------------------------------------------------------------
# CONVERTIR CATEGÓRICAS A FACTOR
# ------------------------------------------------------------

categoricas <- c(
  "especie",
  "altura",
  "diametro_tronco",
  "seccion",
  "nombre_seccion",
  "circ_tronco_cm_cat"
)

df[categoricas] <- lapply(df[categoricas], factor)

# Esta columna tiene miles de niveles distintos y NO la usamos en la fórmula:
# la quitamos para evitar problemas internos en rpart
df$ultima_modificacion <- NULL

# ------------------------------------------------------------
# BALANCEAR CLASES
# ------------------------------------------------------------

set.seed(123)
df_0 <- df %>% filter(inclinacion_peligrosa == 0) %>% sample_n(1000)
df_1 <- df %>% filter(inclinacion_peligrosa == 1)
df <- rbind(df_0, df_1)

# Mezclar filas
df <- df[sample(nrow(df)), ]

# ------------------------------------------------------------
# EJECUCIÓN DEL CROSS VALIDATION
# ------------------------------------------------------------

res <- cross_validation(df, k = 5)

write.csv(res$resumen_final, "data/tp7B-cv-resumen.csv", row.names = FALSE)
write.csv(res$resultados_por_fold, "data/tp7B-cv-por-fold.csv", row.names = FALSE)

cat("\n✅ Archivos exportados:\n")
cat("  • data/tp7B-cv-resumen.csv\n")
cat("  • data/tp7B-cv-por-fold.csv\n")
