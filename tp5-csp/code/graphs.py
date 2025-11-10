import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import statistics

# ============================================================
# CONFIG
# ============================================================
CSV_PATH = "tp5-csp-nreinas.csv"
IMG_DIR = "images"
os.makedirs(IMG_DIR, exist_ok=True)

# ============================================================
# CARGA DE DATOS
# ============================================================
df = pd.read_csv(CSV_PATH)
print(f"✅ Archivo cargado ({len(df)} registros)\n")

df["found"] = df["found"].astype(int)
df["N"] = df["N"].astype(int)
df["time"] = pd.to_numeric(df["time"], errors="coerce").fillna(0)
df["nodes"] = pd.to_numeric(df["nodes"], errors="coerce").fillna(0)

# ============================================================
# MÉTRICAS
# ============================================================
summary = []
for (alg, N), g in df.groupby(["algorithm", "N"]):
    summary.append({
        "Algoritmo": alg,
        "N": N,
        "Éxito (%)": round(g["found"].mean() * 100, 1),
        "Tiempo medio (s)": round(statistics.mean(g["time"]), 4),
        "Desv. tiempo": round(statistics.stdev(g["time"]), 4),
        "Nodos medios": round(statistics.mean(g["nodes"]), 1),
        "Desv. nodos": round(statistics.stdev(g["nodes"]), 1),
    })

summary_df = pd.DataFrame(summary)
print("=== RESUMEN TP5 CSP ===")
print(summary_df)

# ============================================================
# GRÁFICOS
# ============================================================
sns.set(style="whitegrid")

# Boxplot de tiempos
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="algorithm", y="time", hue="N")
plt.title("Distribución de tiempos por algoritmo y tamaño N")
plt.ylabel("Tiempo (s)")
plt.xlabel("Algoritmo")
plt.legend(title="Tamaño N")
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "tp5_csp_time_boxplot.png"))
plt.close()

# Boxplot de nodos
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="algorithm", y="nodes", hue="N")
plt.title("Distribución de nodos explorados por algoritmo y tamaño N")
plt.ylabel("Nodos explorados")
plt.xlabel("Algoritmo")
plt.legend(title="Tamaño N")
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "tp5_csp_nodes_boxplot.png"))
plt.close()

# Barras de éxito
plt.figure(figsize=(8, 5))
sns.barplot(data=summary_df, x="Algoritmo", y="Éxito (%)", hue="N")
plt.title("Porcentaje de ejecuciones exitosas")
plt.ylabel("Éxito (%)")
plt.xlabel("Algoritmo")
plt.ylim(0, 110)
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "tp5_csp_success_rate.png"))
plt.close()

print("\n📊 Gráficos del TP5 generados en:", IMG_DIR)
