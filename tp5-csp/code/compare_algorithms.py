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
# CARGAR DATOS
# ============================================================
print("📥 Cargando resultados de TP4 y TP5...")

tp4 = pd.read_csv(TP4_PATH)
tp5 = pd.read_csv(TP5_PATH)

# Estandarizar nombres de columnas
tp4.rename(columns={
    "algorithm_name": "algorithm",
    "size": "N",
    "time": "time",
    "states": "nodes",
    "H": "H"
}, inplace=True)

tp5["H"] = 0  # No hay función H, pero agregamos columna para compatibilidad

# Unificar datasets
df = pd.concat([tp4, tp5], ignore_index=True)
df["family"] = df["algorithm"].apply(lambda a: "Local Search" if a in ["HC", "SA", "GA", "random"] else "CSP")

# ============================================================
# LIMPIEZA Y FORMATO ROBUSTO
# ============================================================
for col in ["found", "time", "nodes"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")  # convierte a numérico, NaN si falla

# Reemplazar NaN o infinitos por 0 para evitar fallos
df = df.replace([float("inf"), float("-inf")], 0)
df = df.fillna(0)

# Convertir solo después de limpiar
df["found"] = df["found"].astype(int)


# ============================================================
# MÉTRICAS AGREGADAS
# ============================================================
summary = df.groupby(["algorithm", "N"]).agg(
    success_rate=("found", lambda x: 100 * x.mean()),
    time_mean=("time", "mean"),
    time_std=("time", "std"),
    nodes_mean=("nodes", "mean"),
    nodes_std=("nodes", "std")
).reset_index()

print("\n=== RESUMEN GENERAL ===")
print(summary.round(3))

# ============================================================
# GRÁFICOS
# ============================================================

sns.set(style="whitegrid")

# --- 1️⃣ Boxplot de tiempos ---
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="algorithm", y="time", hue="N")
plt.title("Distribución de tiempos por algoritmo y tamaño N")
plt.ylabel("Tiempo (s)")
plt.xlabel("Algoritmo")
plt.legend(title="Tamaño N")
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "compare_time_boxplot.png"))
plt.close()
print("📊 Guardado: compare_time_boxplot.png")

# --- 2️⃣ Boxplot de nodos ---
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="algorithm", y="nodes", hue="N")
plt.title("Distribución de nodos explorados por algoritmo y tamaño N")
plt.ylabel("Nodos explorados")
plt.xlabel("Algoritmo")
plt.legend(title="Tamaño N")
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "compare_nodes_boxplot.png"))
plt.close()
print("📊 Guardado: compare_nodes_boxplot.png")

# --- 3️⃣ Porcentaje de éxito ---
plt.figure(figsize=(9, 6))
sns.barplot(data=summary, x="algorithm", y="success_rate", hue="N")
plt.title("Porcentaje de ejecuciones exitosas (solución encontrada)")
plt.ylabel("Éxito (%)")
plt.ylim(0, 110)
plt.legend(title="Tamaño N")
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "compare_success_rate.png"))
plt.close()
print("📊 Guardado: compare_success_rate.png")

# --- 4️⃣ Rendimiento combinado ---
plt.figure(figsize=(9, 6))
sns.scatterplot(data=summary, x="time_mean", y="success_rate", hue="algorithm", style="N", s=150)
plt.title("Tiempo promedio vs Porcentaje de éxito")
plt.xlabel("Tiempo medio (s)")
plt.ylabel("Éxito (%)")
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "compare_time_vs_success.png"))
plt.close()
print("📈 Guardado: compare_time_vs_success.png")

# --- 5️⃣ Comparación entre familias ---
plt.figure(figsize=(9, 6))
sns.boxplot(data=df, x="family", y="time", hue="N")
plt.title("Comparación de familias de algoritmos: Local Search vs CSP")
plt.ylabel("Tiempo (s)")
plt.xlabel("Familia")
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "compare_families.png"))
plt.close()
print("📈 Guardado: compare_families.png")

print("\n✅ Todos los gráficos se guardaron en la carpeta:", IMG_DIR)
