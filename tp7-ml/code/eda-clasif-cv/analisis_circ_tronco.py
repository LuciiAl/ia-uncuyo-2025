import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# TP7B – Análisis de circ_tronco_cm (Ejercicio 3)
# ============================================================

sns.set_theme(style="whitegrid")

def load_data(path):
    df = pd.read_csv(path)
    df.columns = [c.lower().strip() for c in df.columns]
    return df

def histograms(df, outdir):
    imgs = {}

    plt.figure(figsize=(7, 4))
    sns.histplot(df["circ_tronco_cm"], bins=20, color="steelblue")
    plt.title("Histograma circ_tronco_cm (20 bins)")
    fname = os.path.join(outdir, "hist_20bins.png")
    plt.savefig(fname)
    plt.close()
    imgs["20"] = fname

    plt.figure(figsize=(7, 4))
    sns.histplot(df["circ_tronco_cm"], bins=40, color="darkcyan")
    plt.title("Histograma circ_tronco_cm (40 bins)")
    fname2 = os.path.join(outdir, "hist_40bins.png")
    plt.savefig(fname2)
    plt.close()
    imgs["40"] = fname2

    return imgs

def histogram_by_class(df, outdir):
    plt.figure(figsize=(7, 4))
    sns.histplot(df, x="circ_tronco_cm", hue="inclinacion_peligrosa",
                 bins=30, palette="magma", alpha=0.6)
    plt.title("Distribución por clase")
    fname = os.path.join(outdir, "hist_por_clase.png")
    plt.savefig(fname)
    plt.close()
    return fname

def categorize(df):
    qs = df["circ_tronco_cm"].quantile([0.25, 0.5, 0.75])
    bins = [0, qs[0.25], qs[0.50], qs[0.75], df["circ_tronco_cm"].max()]
    labels = ["bajo", "medio-bajo", "medio-alto", "alto"]

    df["circ_tronco_cm_cat"] = pd.cut(df["circ_tronco_cm"], bins=bins,
                                      labels=labels, include_lowest=True)
    return df, bins, labels

def update_markdown(root, imgs, img_class, bins, labels):
    md_file = os.path.join(root, "tp7B-eda.md")

    md = []
    md.append("## 3. Análisis de circ_tronco_cm")
    md.append("### 3(a) Histogramas")
    md.append(f"![20bins]({os.path.relpath(imgs['20'], root).replace(os.sep,'/')})")
    md.append(f"![40bins]({os.path.relpath(imgs['40'], root).replace(os.sep,'/')})")
    md.append("")
    md.append("---")
    md.append("")
    md.append("### 3(b) Distribución por clase")
    md.append(f"![clase]({os.path.relpath(img_class, root).replace(os.sep,'/')})")
    md.append("")
    md.append("---")
    md.append("")
    md.append("### 3(c) Categorías creadas")
    md.append("| Categoría | Rango aproximado |")
    md.append("|-----------|-------------------|")
    md.append(f"| {labels[0]} | 0 – {bins[1]:.1f} cm |")
    md.append(f"| {labels[1]} | {bins[1]:.1f} – {bins[2]:.1f} cm |")
    md.append(f"| {labels[2]} | {bins[2]:.1f} – {bins[3]:.1f} cm |")
    md.append(f"| {labels[3]} | > {bins[3]:.1f} cm |")
    md.append("")

    with open(md_file, "a", encoding="utf-8") as f:
        f.write("\n".join(md))

if __name__ == "__main__":
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    DATA = os.path.join(ROOT, "data", "arbolado-mendoza-dataset-train.csv")
    IMG_DIR = os.path.join(ROOT, "code", "eda-clasif-cv", "images")
    os.makedirs(IMG_DIR, exist_ok=True)

    df = load_data(DATA)

    imgs = histograms(df, IMG_DIR)
    img_class = histogram_by_class(df, IMG_DIR)
    df_cat, bins, labels = categorize(df)

    OUT = os.path.join(ROOT, "data", "arbolado-mendoza-dataset-circ_tronco_cm-train.csv")
    df_cat.to_csv(OUT, index=False)
    update_markdown(ROOT, imgs, img_class, bins, labels)
