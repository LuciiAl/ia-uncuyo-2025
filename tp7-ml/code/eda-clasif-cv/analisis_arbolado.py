import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# TP7B – ANÁLISIS DE ARBOLADO (Ejercicio 2)
# ============================================================

sns.set_theme(style="whitegrid")

def load_data(path):
    df = pd.read_csv(path)
    df.columns = [c.lower().strip() for c in df.columns]
    return df

def plot_class_distribution(df, outdir):
    plt.figure(figsize=(7, 4))
    sns.countplot(x="inclinacion_peligrosa", data=df, palette="Blues")
    plt.title("Distribución de la clase 'inclinacion_peligrosa'")
    plt.xlabel("Clase")
    plt.ylabel("Cantidad")
    fname = os.path.join(outdir, "dist_clase.png")
    plt.tight_layout()
    plt.savefig(fname)
    plt.close()
    return fname, df["inclinacion_peligrosa"].value_counts(normalize=True)

def plot_seccion_risk(df, outdir):
    summary = (
        df.groupby(["seccion", "inclinacion_peligrosa"])
        .size().reset_index(name="n")
    )
    plt.figure(figsize=(9, 5))
    sns.barplot(
        data=summary,
        x="seccion",
        y="n",
        hue="inclinacion_peligrosa",
        palette="viridis"
    )
    plt.title("Peligrosidad por sección")
    plt.xlabel("Sección")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    fname = os.path.join(outdir, "peligro_seccion.png")
    plt.savefig(fname)
    plt.close()
    return fname

def plot_species_risk(df, outdir, min_count=50):
    freq = df.groupby("especie")["inclinacion_peligrosa"].mean()
    freq = freq.reset_index().rename(columns={"inclinacion_peligrosa": "riesgo"})
    freq = freq.sort_values("riesgo", ascending=False)
    top = freq.head(10)

    plt.figure(figsize=(9, 6))
    sns.barplot(y="especie", x="riesgo", data=top, palette="rocket_r")
    plt.title("Top 10 especies con mayor riesgo")
    plt.xlabel("Proporción de árboles peligrosos")
    plt.ylabel("Especie")
    plt.tight_layout()

    fname = os.path.join(outdir, "peligro_especie.png")
    plt.savefig(fname)
    plt.close()

    return fname, top

def update_markdown(root, img_clase, dist, img_seccion, img_especie, top_species):
    md_file = os.path.join(root, "tp7B-eda.md")
    md = []

    md.append("## 2. Análisis del arbolado")
    md.append("")
    md.append("### 2(a) Distribución de la clase")
    md.append(f"![dist]({os.path.relpath(img_clase, root).replace(os.sep,'/')})")
    md.append("")
    md.append("| Clase | Porcentaje (%) |")
    md.append("|--------|----------------:|")
    for k, v in dist.items():
        md.append(f"| {k} | {v*100:.2f} |")
    md.append("")
    md.append("---")
    md.append("")
    md.append("### 2(b) Secciones más peligrosas")
    md.append(f"![sec]({os.path.relpath(img_seccion, root).replace(os.sep,'/')})")
    md.append("")
    md.append("La proporción de árboles peligrosos varía entre secciones, indicando zonas con mayor riesgo relativo.")
    md.append("")
    md.append("---")
    md.append("")
    md.append("### 2(c) Especies más peligrosas")
    md.append(f"![esp]({os.path.relpath(img_especie, root).replace(os.sep,'/')})")
    md.append("")
    md.append("| Especie | Riesgo |")
    md.append("|---------|--------:|")
    for _, row in top_species.iterrows():
        md.append(f"| {row['especie']} | {row['riesgo']:.3f} |")
    md.append("")

    with open(md_file, "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print(f"📄 Reporte actualizado: {md_file}")

if __name__ == "__main__":
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    DATA = os.path.join(ROOT, "data", "arbolado-mendoza-dataset-train.csv")
    IMG_DIR = os.path.join(ROOT, "code", "eda-clasif-cv", "images")
    os.makedirs(IMG_DIR, exist_ok=True)

    df = load_data(DATA)
    img_clase, dist = plot_class_distribution(df, IMG_DIR)
    img_seccion = plot_seccion_risk(df, IMG_DIR)
    img_especie, top_species = plot_species_risk(df, IMG_DIR)

    update_markdown(ROOT, img_clase, dist, img_seccion, img_especie, top_species)
