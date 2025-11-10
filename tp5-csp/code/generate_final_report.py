import pandas as pd
import os

# ============================================================
# CONFIG
# ============================================================
TP4_CSV = "C:\\Users\\cocuc\\OneDrive\\Escritorio\\Facultad\\IA\\Repo IA\\ia-uncuyo-2025\\tp4-busquedas-locales\\tp4-Nreinas.csv"
TP5_CSV = "tp5-csp-summary.csv"
IMG_DIR = "images"
OUT_MD = "tp5-final-report.md"

# ============================================================
# VERIFICAR EXISTENCIA
# ============================================================
for f in [TP4_CSV, TP5_CSV]:
    if not os.path.exists(f):
        raise FileNotFoundError(f"No se encontró el archivo {f}")

# ============================================================
# CARGA DE DATOS
# ============================================================
tp4 = pd.read_csv(TP4_CSV)
tp5 = pd.read_csv(TP5_CSV)

# ============================================================
# GENERAR TABLAS MARKDOWN
# ============================================================
def df_to_markdown(df):
    md = "| " + " | ".join(df.columns) + " |\n"
    md += "| " + " | ".join(["---"] * len(df.columns)) + " |\n"
    for _, row in df.iterrows():
        md += "| " + " | ".join(str(v) for v in row.values) + " |\n"
    return md

tp5_md = df_to_markdown(tp5.head(10))  # si es largo, solo muestra primeras filas
tp4_md = df_to_markdown(tp4.head(10))

# ============================================================
# EMBED GRÁFICOS EXISTENTES
# ============================================================
def embed_images(file_list, title):
    section = f"\n## {title}\n"
    for img in sorted(file_list):
        section += f"### {img}\n![{img}]({IMG_DIR}/{img})\n"
    return section

tp5_imgs = [
    "tp5_csp_time_boxplot.png",
    "tp5_csp_nodes_boxplot.png",
    "tp5_csp_success_rate.png",
]

compare_imgs = [
    "compare_tp4_tp5_time.png",
    "compare_tp4_tp5_nodes.png",
    "compare_tp4_tp5_time_mean.png",
    "compare_tp4_tp5_nodes_mean.png",
]

# ============================================================
# CONTENIDO DEL REPORTE MARKDOWN
# ============================================================
content = f"""# Informe Final – N-Reinas (TP4 y TP5)

## 1. Resultados del TP5 – CSP (Backtracking vs Forward Checking)

En este trabajo se evaluaron los algoritmos **Backtracking clásico** y **Forward Checking** aplicados al problema de las N-Reinas, formulado como un **Problema de Satisfacción de Restricciones (CSP)**.

Cada algoritmo fue ejecutado **30 veces** para los tamaños **N = 4, 8 y 10**, registrando el tiempo, los nodos explorados y la tasa de éxito (soluciones válidas encontradas).

---

### Tabla resumen de resultados
{tp5_md}

---

### Gráficos de desempeño
{embed_images(tp5_imgs, "Gráficos de TP5 – CSP")}

---

### Conclusiones del TP5

- **Forward Checking** logra una mejora notable respecto al **Backtracking clásico**, reduciendo significativamente el número de nodos explorados.
- Ambos alcanzan un **100% de éxito** en tableros pequeños, pero **Backtracking** crece exponencialmente en costo al aumentar N.
- En términos de tiempo, **Forward Checking** mantiene un comportamiento más estable y eficiente.
- La poda anticipada de dominios en cada asignación es clave para reducir la explosión combinatoria.

> **Conclusión:** Forward Checking es el método más eficiente y escalable para resolver el CSP de N-Reinas, sin comprometer exactitud.

---

## 2. Comparación General – Búsquedas Locales (TP4) vs CSP (TP5)

Esta comparación integra los resultados del **TP4 (búsquedas locales: HC, HCR, SA, GA, Random)** y el **TP5 (CSP: Backtracking, Forward Checking)**.

Se busca analizar diferencias en:
- **Eficiencia temporal**
- **Nodos explorados**
- **Tasa de éxito**

---

### Muestra parcial de datos (TP4)
{tp4_md}

---

### Gráficos comparativos
{embed_images(compare_imgs, "Comparativa TP4 vs TP5")}

---

### Análisis comparativo

- Los métodos **CSP (Backtracking, Forward Checking)** garantizan **soluciones exactas**, pero con tiempos de ejecución más altos en N grandes.
- Los algoritmos de **búsqueda local (SA, GA, HCR)** ofrecen soluciones rápidas y aproximadas, alcanzando buenos resultados en tiempo, aunque sin garantía de optimalidad.
- **Simulated Annealing (SA)** se posiciona como el mejor entre los métodos locales: rápido, robusto y consistente.
- **Forward Checking (CSP)** domina en exactitud y control de nodos, aunque a un costo computacional mayor en escalas grandes.

---

### Conclusión global

| Criterio | Local Search (TP4) | CSP (TP5) |
|-----------|-------------------|------------|
| Exactitud | Parcial (dependiente de heurística) | Completa (garantiza solución) |
| Escalabilidad | Alta para N moderado | Limitada por crecimiento exponencial |
| Robustez | Alta (en SA y GA) | Alta (en FC) |
| Tiempo | Bajo–medio | Medio–alto |
| Mejor método | **Simulated Annealing (SA)** | **Forward Checking (FC)** |

---

## 3. Conclusión Final Integrada

- **Forward Checking (CSP)** sobresale por su precisión y control, siendo ideal para validación o demostración de soluciones exactas.
- **Simulated Annealing (Local Search)** se destaca por su velocidad y adaptabilidad, siendo más adecuado para problemas grandes o con restricciones suaves.
- Ambos enfoques son complementarios: uno garantiza optimalidad, el otro eficiencia práctica.

> **Conclusión final:**  
> Los resultados muestran la sinergia entre los paradigmas **CSP (exactos)** y **Búsquedas Locales (aproximadas)**.  
> En conjunto, permiten abordar el problema de las N-Reinas desde dos perspectivas complementarias: **optimización exacta y heurística**.

---

*Generado automáticamente a partir de los CSV `tp4-Nreinas.csv` y `tp5-csp-summary.csv`, con gráficos ubicados en la carpeta `{IMG_DIR}/`.*
"""

# ============================================================
# GUARDAR
# ============================================================
with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write(content)

print(f"✅ Reporte generado: {OUT_MD}")
