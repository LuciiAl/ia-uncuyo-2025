import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# CONFIG
# ============================================================
TP4_PATH = "../tp4-busquedas-locales/tp4-Nreinas.csv"
TP5_PATH = "tp5-csp-nreinas.csv"
IMG_DIR = "images"
os.makedirs(IMG_DIR, exist_ok=True)

# ============================================================
# CARGA DE DATOS
# ============================================================
print("Cargando resultados de TP4 y TP5...")

tp4 = pd.read_csv(TP4_PATH)
tp5 = pd.read_csv(TP5_PATH)

# Normalizar columnas
tp4.rename(columns={
    "algorithm_name": "algorithm",
    "size": "N",
    "time": "time",
    "states": "nodes",
    "H": "H"
}, inplace=True)

tp5["H"] = 0
tp5["family"] = "CSP"
tp4["family"] = "Local Search"

df = pd.concat([tp4, tp5], ignore_index=True)

# Convertir tipos y limpiar
for col in ["time", "nodes"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# ============================================================
# MÉTRICAS AGREGADAS
# ============================================================
summary = df.groupby(["family", "algorithm", "N"]).agg(
    time_mean=("time", "mean"),
    time_std=("time", "std"),
    nodes_mean=("nodes", "mean"),
    nodes_std=("nodes", "std")
).reset_index()

print("\n=== RESUMEN COMPARATIVO ===")
print(summary.round(3))

# ============================================================
# GRÁFICOS COMPARATIVOS
# ============================================================
sns.set(style="whitegrid")

# 1️⃣ Boxplot de tiempo
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="algorithm", y="time", hue="family")
plt.title("Comparativo de tiempo por algoritmo (TP4 vs TP5)")
plt.xlabel("Algoritmo")
plt.ylabel("Tiempo (s)")
plt.legend(title="Familia")
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "compare_tp4_tp5_time.png"))
plt.close()

# 2️⃣ Boxplot de nodos
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="algorithm", y="nodes", hue="family")
plt.title("Comparativo de nodos explorados por algoritmo (TP4 vs TP5)")
plt.xlabel("Algoritmo")
plt.ylabel("Nodos explorados")
plt.legend(title="Familia")
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "compare_tp4_tp5_nodes.png"))
plt.close()

# 3️⃣ Promedios agrupados
plt.figure(figsize=(9, 6))
sns.barplot(data=summary, x="algorithm", y="time_mean", hue="family")
plt.title("Tiempo medio de ejecución (TP4 vs TP5)")
plt.ylabel("Tiempo promedio (s)")
plt.xlabel("Algoritmo")
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "compare_tp4_tp5_time_mean.png"))
plt.close()

plt.figure(figsize=(9, 6))
sns.barplot(data=summary, x="algorithm", y="nodes_mean", hue="family")
plt.title("Nodos promedio explorados (TP4 vs TP5)")
plt.ylabel("Nodos promedio")
plt.xlabel("Algoritmo")
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "compare_tp4_tp5_nodes_mean.png"))
plt.close()

print("\n✅ Gráficos comparativos guardados en:", IMG_DIR)
