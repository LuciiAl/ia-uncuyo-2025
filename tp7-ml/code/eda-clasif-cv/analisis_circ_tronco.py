import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# CONFIGURACIÓN DE RUTAS
# ============================================================
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # .../tp7-ml
DATA = os.path.join(ROOT, "data", "arbolado-mendoza-dataset-train.csv")
OUT_DATA = os.path.join(ROOT, "data", "arbolado-mendoza-dataset-circ_tronco_cm-train.csv")
IMG_DIR = os.path.join(ROOT, "code", "eda-clasif-cv", "images")
REPORT = os.path.join(ROOT, "tp7B-eda.md")

os.makedirs(IMG_DIR, exist_ok=True)

# ============================================================
# CARGA DE DATOS
# ============================================================
df = pd.read_csv(DATA)
df.columns = [c.strip().lower() for c in df.columns]

# ============================================================
# (3a) HISTOGRAMA DE FRECUENCIA DE circ_tronco_cm
# ============================================================
plt.figure(figsize=(8, 5))
sns.histplot(df["circ_tronco_cm"], bins=20, kde=False, color="skyblue")
plt.title("Histograma de circ_tronco_cm (20 bins)")
plt.xlabel("circ_tronco_cm (cm)")
plt.ylabel("Frecuencia")
plt.tight_layout()
img_a = os.path.join(IMG_DIR, "hist_circ_tronco_20bins.png")
plt.savefig(img_a)
plt.close()

plt.figure(figsize=(8, 5))
sns.histplot(df["circ_tronco_cm"], bins=40, kde=False, color="seagreen")
plt.title("Histograma de circ_tronco_cm (40 bins)")
plt.xlabel("circ_tronco_cm (cm)")
plt.ylabel("Frecuencia")
plt.tight_layout()
img_a2 = os.path.join(IMG_DIR, "hist_circ_tronco_40bins.png")
plt.savefig(img_a2)
plt.close()

comment_a = (
    "La variable `circ_tronco_cm` presenta una distribución sesgada hacia valores bajos. "
    "La mayoría de los árboles poseen circunferencias menores a 150 cm, lo que indica predominancia "
    "de ejemplares de tamaño medio o pequeño. La densidad disminuye a medida que aumenta el diámetro del tronco."
)

# ============================================================
# (3b) HISTOGRAMA SEPARADO POR CLASE DE inclinacion_peligrosa
# ============================================================
plt.figure(figsize=(8, 5))
sns.histplot(
    data=df,
    x="circ_tronco_cm",
    bins=30,
    hue="inclinacion_peligrosa",
    multiple="stack",
    palette="coolwarm"
)
plt.title("Distribución de circ_tronco_cm según inclinación peligrosa")
plt.xlabel("circ_tronco_cm (cm)")
plt.ylabel("Frecuencia")
plt.tight_layout()
img_b = os.path.join(IMG_DIR, "hist_circ_tronco_por_inclinacion.png")
plt.savefig(img_b)
plt.close()

comment_b = (
    "Al separar por la clase `inclinacion_peligrosa`, se observa que los árboles con mayor circunferencia "
    "presentan una ligera mayor frecuencia de inclinaciones peligrosas. "
    "Esto sugiere que el tamaño y la edad podrían estar asociados a un mayor riesgo estructural."
)

# ============================================================
# (3c) CREACIÓN DE VARIABLE CATEGÓRICA circ_tronco_cm_cat
# ============================================================
# Cortes seleccionados en base a los histogramas
bins = [0, 60, 120, 200, df["circ_tronco_cm"].max()]
labels = ["bajo", "medio", "alto", "muy alto"]

df["circ_tronco_cm_cat"] = pd.cut(df["circ_tronco_cm"], bins=bins, labels=labels, include_lowest=True)
df.to_csv(OUT_DATA, index=False, encoding="utf-8")
print(f"✅ Archivo guardado: {OUT_DATA}")

comment_c = (
    "Se crearon cuatro categorías a partir de los histogramas:  \n"
    "- **bajo:** 0–60 cm  \n"
    "- **medio:** 60–120 cm  \n"
    "- **alto:** 120–200 cm  \n"
    "- **muy alto:** >200 cm  \n"
    "Esta transformación facilita el análisis de la variable y permitirá evaluar relaciones con otras variables de riesgo."
)

# ============================================================
# GENERACIÓN / ACTUALIZACIÓN DEL ARCHIVO tp7B-eda.md
# ============================================================
md = []
md.append("## 3. Análisis de circ_tronco_cm y creación de variable categórica")
md.append("")
md.append("### 3(a) Histograma de frecuencia de `circ_tronco_cm`")
md.append(f"![Histograma circ_tronco_cm (20 bins)]({os.path.relpath(img_a, ROOT).replace(os.sep, '/')})")
md.append(f"![Histograma circ_tronco_cm (40 bins)]({os.path.relpath(img_a2, ROOT).replace(os.sep, '/')})")
md.append("")
md.append(f"**Interpretación:** {comment_a}")
md.append("")
md.append("---")
md.append("")
md.append("### 3(b) Distribución por clase `inclinacion_peligrosa`")
md.append(f"![Histograma por clase inclinacion_peligrosa]({os.path.relpath(img_b, ROOT).replace(os.sep, '/')})")
md.append("")
md.append(f"**Interpretación:** {comment_b}")
md.append("")
md.append("---")
md.append("")
md.append("### 3(c) Creación de la variable categórica `circ_tronco_cm_cat`")
md.append("")
md.append("| Categoría | Rango (cm) |")
md.append("|------------|-------------|")
md.append("| bajo | 0 – 60 |")
md.append("| medio | 60 – 120 |")
md.append("| alto | 120 – 200 |")
md.append("| muy alto | > 200 |")
md.append("")
md.append(f"**Interpretación:** {comment_c}")
md.append("")
md.append("---")

# Se agrega al final del archivo existente (que ya contiene el ejercicio 2)
with open(REPORT, "a", encoding="utf-8") as f:
    f.write("\n".join(md))

print(f"✅ Reporte actualizado: {REPORT}")
print(f"📊 Gráficos guardados en: {IMG_DIR}")
