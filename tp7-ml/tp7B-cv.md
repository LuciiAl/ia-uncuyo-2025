
## Código de las funciones


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

  resultados
}
```

## Resultados del modelo (media y desvío estándar)

| Métrica | Media | Desvío Estándar |
|---------|-------|-----------------|
| Accuracy | 0.7728 | 0.0208 |
| Precision | 0.7834 | 0.0302 |
| Sensitivity | 0.9595 | 0.0194 |
| Specificity | 0.2405 | 0.0431 |

