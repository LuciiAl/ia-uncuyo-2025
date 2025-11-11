import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# CONFIGURACIÓN DE RUTAS
# ============================================================
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # .../tp7-ml
DATA = os.path.join(ROOT, "data", "arbolado-mendoza-dataset-train.csv")
IMG_DIR = os.path.join(ROOT, "code", "eda-clasif-cv", "images")
REPORT = os.path.join(ROOT, "tp7B-eda.md")

os.makedirs(IMG_DIR, exist_ok=True)

# ============================================================
# CARGA DE DATOS
# ============================================================
df = pd.read_csv(DATA)

# Normalizamos nombres de columnas (por si hay mayúsculas o tildes)
df.columns = [c.strip().lower() for c in df.columns]

# ============================================================
# (a) DISTRIBUCIÓN DE LA CLASE "inclinacion_peligrosa"
# ============================================================
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="inclinacion_peligrosa", palette="Set2")
plt.title("Distribución de la clase 'inclinacion_peligrosa'")
plt.xlabel("¿Inclinación peligrosa?")
plt.ylabel("Cantidad de árboles")
plt.tight_layout()
img_a = os.path.join(IMG_DIR, "dist_inclinacion_peligrosa.png")
plt.savefig(img_a)
plt.close()

dist = df["inclinacion_peligrosa"].value_counts(normalize=True).mul(100).round(2)
comment_a = (
    "La mayoría de los árboles **no presentan inclinación peligrosa**, "
    "lo que indica un **conjunto de datos desbalanceado**. "
    "Este desbalance debe considerarse en las etapas de modelado."
)

# ============================================================
# (b) SECCIÓN MÁS PELIGROSA
# ============================================================
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x="seccion", hue="inclinacion_peligrosa", palette="coolwarm")
plt.title("Distribución de árboles peligrosos por sección")
plt.xlabel("Sección")
plt.ylabel("Cantidad de árboles")
plt.legend(title="Inclinación peligrosa")
plt.tight_layout()
img_b = os.path.join(IMG_DIR, "peligrosidad_por_seccion.png")
plt.savefig(img_b)
plt.close()

section_risk = (
    df.groupby("seccion")["inclinacion_peligrosa"]
    .value_counts(normalize=True)
    .rename("porcentaje")
    .reset_index()
)
danger_sections = section_risk[
    section_risk["inclinacion_peligrosa"].astype(str).str.upper() == "SI"
].sort_values("porcentaje", ascending=False)
top_sections = danger_sections.head(5)
comment_b = (
    "Las secciones con mayor proporción de árboles con inclinación peligrosa son las siguientes: "
    f"{', '.join(top_sections['seccion'].astype(str))}. "
    "Estas zonas pueden considerarse **más riesgosas** y deberían priorizarse en inspecciones."
)

# ============================================================
# (c) ESPECIES MÁS PELIGROSAS
# ============================================================
species_col = "especie"

# Calcular proporción de árboles peligrosos (inclinacion_peligrosa = 1) por especie
species_risk = (
    df.groupby(species_col)["inclinacion_peligrosa"]
    .mean()
    .reset_index()
    .rename(columns={"inclinacion_peligrosa": "porcentaje"})
)

# Tomar las 10 especies con mayor proporción de riesgo
top_species = species_risk.sort_values("porcentaje", ascending=False).head(10)

# Graficar
plt.figure(figsize=(10, 6))
sns.barplot(data=top_species, y=species_col, x="porcentaje", palette="Reds_r")
plt.title("Top 10 especies con mayor proporción de inclinación peligrosa")
plt.xlabel("Proporción de árboles con inclinación peligrosa")
plt.ylabel("Especie")
plt.tight_layout()
img_c = os.path.join(IMG_DIR, "peligrosidad_por_especie.png")
plt.savefig(img_c)
plt.close()
print(f"📊 Guardado: {img_c}")
comment_c = (
    "Las especies con mayor proporción de árboles con inclinación peligrosa "
    "pueden considerarse más vulnerables estructuralmente o menos adaptadas a las "
    "condiciones del entorno urbano. Estas especies requieren mayor seguimiento "
    "y eventualmente podas o reemplazos preventivos."
)


# ============================================================
# GENERACIÓN DEL ARCHIVO tp7B-eda.md
# ============================================================
md = []

md.append("# TP7B – Análisis Exploratorio de Datos (EDA)")
md.append("")
md.append("## 2(a) Distribución de la clase `inclinacion_peligrosa`")
md.append("")
md.append(f"![Distribución de inclinación peligrosa]({os.path.relpath(img_a, ROOT).replace(os.sep, '/')})")
md.append("")
md.append("| Clase | Porcentaje (%) |")
md.append("|--------|----------------:|")
for k, v in dist.items():
    md.append(f"| {k} | {v:.2f} |")
md.append("")
md.append(f"**Interpretación:** {comment_a}")
md.append("")
md.append("---")
md.append("")
md.append("## 2(b) Secciones más peligrosas")
md.append("")
md.append(f"![Peligrosidad por sección]({os.path.relpath(img_b, ROOT).replace(os.sep, '/')})")
md.append("")
md.append("| Sección | Proporción de árboles peligrosos |")
md.append("|----------|---------------------------------:|")
for _, row in top_sections.iterrows():
    md.append(f"| {row['seccion']} | {row['porcentaje']:.3f} |")
md.append("")
md.append(f"**Interpretación:** {comment_b}")
md.append("")
md.append("---")
md.append("")
md.append("## 2(c) Especies más peligrosas")
md.append("")
md.append(f"![Peligrosidad por especie]({os.path.relpath(img_c, ROOT).replace(os.sep, '/')})")
md.append("")
md.append("| Especie | Proporción de árboles peligrosos |")
md.append("|----------|---------------------------------:|")
for _, row in top_species.iterrows():
    md.append(f"| {row['especie']} | {row['porcentaje']:.3f} |")
md.append("")
md.append(f"**Interpretación:** {comment_c}")
md.append("")
md.append("---")
md.append("*Archivo generado automáticamente a partir del dataset de entrenamiento.*")

# Guardar Markdown
with open(REPORT, "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print(f"✅ Reporte generado: {REPORT}")
print(f"📊 Gráficos guardados en: {IMG_DIR}")
