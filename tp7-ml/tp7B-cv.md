# TP7B – Validación Cruzada con Árbol de Decisión

## Funciones `create_folds()` y `cross_validation()`

```r
# Genera una lista de folds aleatorios para validación K-Fold
create_folds <- function(data, k = 5, seed = 123) {
  set.seed(seed)
  n <- nrow(data)
  indices <- sample(1:n)
  folds <- split(indices, cut(seq_along(indices), k, labels = FALSE))
  names(folds) <- paste0('Fold', 1:k)
  return(folds)
}

# Ejecuta validación cruzada con un árbol de decisión (rpart)
cross_validation <- function(data, k = 5, seed = 123) {
  folds <- create_folds(data, k, seed)
  resultados <- list()
  formula_tree <- formula(inclinacion_peligrosa ~ altura + circ_tronco_cm + lat + long + seccion + especie)
  for (i in 1:k) {
    test_idx <- folds[[i]]
    data_train <- data[-test_idx, ]
    data_val <- data[test_idx, ]
    modelo <- rpart(formula_tree, data = data_train, method = 'class')
    pred <- predict(modelo, data_val, type = 'class')
    pred <- as.numeric(as.character(pred))
    resultados[[i]] <- calc_metrics(data_val$inclinacion_peligrosa, pred)
  }
  metricas_df <- bind_rows(resultados)
  resumen <- metricas_df %>%
    summarise(across(everything(), list(Media = mean, SD = sd)))
  return(list(metricas = metricas_df, resumen = resumen))
}
```

## Resultados del Árbol de Decisión (rpart)

| Métrica | Media | Desviación Estándar |
|----------|-------:|-------------------:|
| Accuracy_Media | NA | NA |
| Accuracy_SD | NA | NA |
| Precision_Media | NA | NA |
| Precision_SD | NA | NA |
| Sensitivity_Media | NA | NA |
| Sensitivity_SD | NA | NA |
| Specificity_Media | NA | NA |
| Specificity_SD | NA | NA |


