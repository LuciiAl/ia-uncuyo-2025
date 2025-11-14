# ============================================================
# Script maestro: GENERA tp7B-eda.md, tp7B-clasificadores.md
# y TODAS las imágenes necesarias automáticamente
# ============================================================

library(dplyr)
library(ggplot2)

# ------------------------------------------------------------
# CARGA DEL DATASET PRINCIPAL (train completo)
# ------------------------------------------------------------

df <- read.csv("data/arbolado-mendoza-dataset-circ_tronco_cm-train.csv")

df$inclinacion_peligrosa <- as.character(df$inclinacion_peligrosa)
df$inclinacion_peligrosa <- trimws(df$inclinacion_peligrosa)
df$inclinacion_peligrosa <- ifelse(toupper(df$inclinacion_peligrosa) == "SI", 1, 0)
df$inclinacion_peligrosa <- as.integer(df$inclinacion_peligrosa)

# ------------------------------------------------------------
# CREACIÓN DE CARPETA DE IMÁGENES
# ------------------------------------------------------------

if(!dir.exists("img")) dir.create("img")

# ------------------------------------------------------------
# GENERAR IMÁGENES PARA tp7B-eda.md
# ------------------------------------------------------------

# 1) Cantidad por especie
g1 <- ggplot(df, aes(x = especie)) +
  geom_bar(fill = "steelblue") +
  coord_flip() +
  labs(title = "Cantidad de árboles por especie",
       x = "Especie", y = "Cantidad")

ggsave("img/especies.png", g1, width = 8, height = 6)


# 2) Distribución de altura
g2 <- ggplot(df, aes(x = altura)) +
  geom_bar(fill = "darkgreen") +
  labs(title = "Distribución de altura", x = "Categoría", y = "Frecuencia")

ggsave("img/altura.png", g2, width = 8, height = 6)


# 3) Histograma circ_tronco_cm
g3 <- ggplot(df, aes(x = circ_tronco_cm)) +
  geom_histogram(bins = 35, fill = "firebrick", color = "black") +
  labs(title = "Histograma de circ_tronco_cm",
       x = "circ_tronco_cm", y = "Frecuencia")

ggsave("img/circ_tronco.png", g3, width = 8, height = 6)


# 4) Scatter lat/long
g4 <- ggplot(df, aes(x = long, y = lat)) +
  geom_point(alpha = 0.3) +
  labs(title = "Distribución geográfica", x = "Longitud", y = "Latitud")

ggsave("img/mapa.png", g4, width = 7, height = 6)


# 5) Histograma diametro_tronco (si sirve para el EDA)
g5 <- ggplot(df, aes(x = diametro_tronco)) +
  geom_bar(fill = "orange") +
  labs(title = "Distribución del diámetro del tronco",
       x = "Categoría", y = "Frecuencia")

ggsave("img/diametro.png", g5, width = 7, height = 6)



# ============================================================
# GENERAR ARCHIVO tp7B-eda.md AUTOMÁTICAMENTE
# ============================================================

md_eda <- c(
"# TP7B – EDA y Clasificación Inicial",
"",
"## (2) Análisis Exploratorio de Datos",
"",
"### 2.a) Cantidad por especie",
"![Especies](img/especies.png)",
"",
"### 2.b) Distribución de alturas",
"![Altura](img/altura.png)",
"",
"### 2.c) Histograma de circ_tronco_cm",
"![Circunferencia del tronco](img/circ_tronco.png)",
"",
"### 2.d) Distribución geográfica",
"![Mapa](img/mapa.png)",
"",
"### 2.e) Distribución diámetro del tronco",
"![Diámetro](img/diametro.png)",
"",
"## (3) Criterio de corte para circ_tronco_cm",
"",
"Se seleccionaron cortes basados en los valles del histograma:",
"",
"| Rango | Categoría |",
"|--------|-----------|",
"| 0–60 | bajo |",
"| 60–120 | medio-bajo |",
"| 120–160 | medio-alto |",
"| >160 | alto |",
"",
"---",
"*Archivo generado automáticamente.*"
)

writeLines(md_eda, "tp7B-eda.md")


# ============================================================
# GENERAR ARCHIVO tp7B-clasificadores.md
# ============================================================

# Cargar CSVs generados por scripts previos
random_res <- read.csv("data/confusion_random_results.csv")
bigger_res <- read.csv("data/confusion_biggerclass_results.csv")

mat_random <- matrix(
  c(random_res$TN, random_res$FP, random_res$FN, random_res$TP),
  nrow = 2, byrow = TRUE
)

mat_bigger <- matrix(
  c(bigger_res$TN, bigger_res$FP, bigger_res$FN, bigger_res$TP),
  nrow = 2, byrow = TRUE
)

# Armado del MD
md_clasif <- c(
"# TP7B – Clasificadores Básicos",
"",
"## (4) Clasificador Aleatorio",
"",
"### Matriz de Confusión",
"",
"|                | Pred NO | Pred YES |",
"|----------------|---------|----------|",
paste0("| **Actual NO** | ", mat_random[1,1], " | ", mat_random[1,2], " |"),
paste0("| **Actual YES** | ", mat_random[2,1], " | ", mat_random[2,2], " |"),
"",
"### Métricas",
"",
paste0("- **TP** = ", random_res$TP),
paste0("- **TN** = ", random_res$TN),
paste0("- **FP** = ", random_res$FP),
paste0("- **FN** = ", random_res$FN),
"",
"---",
"",
"## (5) Clasificador por Clase Mayoritaria",
"",
"### Matriz de Confusión",
"",
"|                | Pred NO | Pred YES |",
"|----------------|---------|----------|",
paste0("| **Actual NO** | ", mat_bigger[1,1], " | ", mat_bigger[1,2], " |"),
paste0("| **Actual YES** | ", mat_bigger[2,1], " | ", mat_bigger[2,2], " |"),
"",
"### Métricas",
paste0("- **TP** = ", bigger_res$TP),
paste0("- **TN** = ", bigger_res$TN),
paste0("- **FP** = ", bigger_res$FP),
paste0("- **FN** = ", bigger_res$FN),
"",
"---",
"*Archivo generado automáticamente.*"
)

writeLines(md_clasif, "tp7B-clasificadores.md")

cat("✅ Archivos generados:\n")
cat(" - tp7B-eda.md\n")
cat(" - tp7B-clasificadores.md\n")
cat("📊 Imágenes en carpeta img/\n")
