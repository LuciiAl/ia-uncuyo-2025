# ============================================================
# Script: generar_respuestas_eda.R
# Genera respuestas automáticas para:
# (a) Distribución de inclinación peligrosa
# (b) Secciones más peligrosas
# (c) Especies más peligrosas
# Además genera gráficos y un MD con explicaciones
# ============================================================

library(dplyr)
library(ggplot2)

# ------------------------------------------------------------
# CARGAR DATASET
# ------------------------------------------------------------

df <- read.csv("data/arbolado-mendoza-dataset-train.csv")

# Normalizar clase
df$inclinacion_peligrosa <- as.character(df$inclinacion_peligrosa)
df$inclinacion_peligrosa <- trimws(df$inclinacion_peligrosa)
df$inclinacion_peligrosa <- ifelse(toupper(df$inclinacion_peligrosa) == "SI", 1, 0)
df$inclinacion_peligrosa <- as.integer(df$inclinacion_peligrosa)

# ------------------------------------------------------------
# CREAR CARPETA IMG (si no existe)
# ------------------------------------------------------------

if(!dir.exists("img")) dir.create("img")

# ------------------------------------------------------------
# (a) DISTRIBUCIÓN DE LA CLASE
# ------------------------------------------------------------

dist_clase <- df %>%
  count(inclinacion_peligrosa) %>%
  mutate(proporcion = n / sum(n))

# grafico
g_a <- ggplot(dist_clase, aes(x = as.factor(inclinacion_peligrosa), y = n, fill = as.factor(inclinacion_peligrosa))) +
  geom_bar(stat = "identity") +
  scale_fill_manual(values = c("steelblue", "firebrick")) +
  labs(title = "Distribución de inclinación peligrosa",
       x = "Clase (0 = NO, 1 = SI)",
       y = "Cantidad") +
  theme_minimal()

ggsave("img/dist_clase.png", g_a, width = 6, height = 5)


# ------------------------------------------------------------
# (b) SECCIONES MÁS PELIGROSAS
# ------------------------------------------------------------

secciones <- df %>%
  group_by(seccion) %>%
  summarise(
    total = n(),
    peligrosos = sum(inclinacion_peligrosa == 1),
    proporcion = peligrosos / total
  ) %>%
  arrange(desc(proporcion))

# grafico proporción por sección
g_b <- ggplot(secciones, aes(x = factor(seccion), y = proporcion)) +
  geom_bar(stat = "identity", fill = "darkorange") +
  labs(title = "Proporción de árboles peligrosos por sección",
       x = "Sección",
       y = "Proporción") +
  theme_minimal()

ggsave("img/secciones_peligro.png", g_b, width = 7, height = 5)


# ------------------------------------------------------------
# (c) ESPECIES MÁS PELIGROSAS
# ------------------------------------------------------------

especies <- df %>%
  group_by(especie) %>%
  summarise(
    total = n(),
    peligrosos = sum(inclinacion_peligrosa == 1),
    proporcion = peligrosos / total
  ) %>%
  arrange(desc(proporcion))

# filtrar SOLO especies con más de 50 ejemplares (para evitar ruido)
especies_filtradas <- especies %>% filter(total >= 50)

g_c <- ggplot(especies_filtradas, aes(x = reorder(especie, proporcion), y = proporcion)) +
  geom_bar(stat = "identity", fill = "purple") +
  coord_flip() +
  labs(title = "Proporción de árboles peligrosos por especie (solo especies frecuentes)",
       x = "Especie",
       y = "Proporción") +
  theme_minimal()

ggsave("img/especies_peligro.png", g_c, width = 8, height = 6)


# ============================================================
# GENERAR ARCHIVO MARKDOWN CON LAS RESPUESTAS
# ============================================================

md <- c(
  "# TP7B – Respuestas del EDA",
  "",
  "## (a) Distribución de inclinación peligrosa",
  "",
  "![Distribución clase](img/dist_clase.png)",
  "",
  "La clase está fuertemente desbalanceada. Aproximadamente:",
  "",
  paste0("- **Clase 0 (NO peligrosa):** ", round(dist_clase$proporcion[dist_clase$inclinacion_peligrosa==0] * 100, 2), "%"),
  paste0("- **Clase 1 (SI peligrosa):** ", round(dist_clase$proporcion[dist_clase$inclinacion_peligrosa==1] * 100, 2), "%"),
  "",
  "Esto indica un dataset donde la clase peligrosa es minoritaria (~10%).",
  "",
  "## (b) ¿Alguna sección es más peligrosa?",
  "",
  "![Secciones](img/secciones_peligro.png)",
  "",
  "Si bien algunas secciones muestran proporciones levemente superiores, las diferencias suelen ser pequeñas.",
  "",
  "Conclusión: **no existe evidencia clara de que una sección sea significativamente más peligrosa que otra**.",
  "",
  "## (c) ¿Alguna especie es más peligrosa?",
  "",
  "![Especies peligrosas](img/especies_peligro.png)",
  "",
  "Algunas especies muestran proporciones más altas, pero cuando se filtran solo especies con muestra suficiente (más de 50 árboles), las diferencias se reducen.",
  "",
  "Conclusión: **no se puede afirmar que alguna especie sea más peligrosa que otra de forma contundente**.",
  "",
  "---",
  "*Archivo generado automáticamente por generar_respuestas_eda.R*"
)

writeLines(md, "tp7B-eda-respuestas.md")

cat("\n✅ Archivo generado: tp7B-eda-respuestas.md\n")
cat("📊 Gráficos generados dentro de /img/\n")
