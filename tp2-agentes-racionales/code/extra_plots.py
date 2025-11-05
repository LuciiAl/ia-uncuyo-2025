import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# === CONFIGURACIÓN ===
base_dir = Path("tp2-agentes-racionales")
results_path = base_dir / "results_all.csv"
images_dir = base_dir / "images"
images_dir.mkdir(parents=True, exist_ok=True)

# === CARGAR DATOS ===
df = pd.read_csv(results_path, delimiter=";")

# Limpiamos datos nulos o sin suciedad
df = df[(df["Suciedad inicial"] > 0) & (df["Acciones totales"] > 0)].copy()

# Calculamos métricas derivadas
df["Porcentaje limpiado (%)"] = (df["Celdas limpiadas"] / df["Suciedad inicial"]).clip(upper=1) * 100
df["Eficiencia"] = df["Celdas limpiadas"] / df["Acciones totales"]

print("Datos cargados y procesados correctamente ✅")

# --- GRÁFICO 1: Por tamaño del entorno ---
plt.figure(figsize=(8,5))
for agent in df["Agente"].unique():
    data = (
        df.groupby(["Agente", "Tamaño (N×N)"])["Porcentaje limpiado (%)"]
        .mean()
        .reset_index()
    )
    data_agent = data[data["Agente"] == agent]
    plt.plot(data_agent["Tamaño (N×N)"], data_agent["Porcentaje limpiado (%)"],
             marker="o", label=agent)

plt.title("Porcentaje promedio limpiado según tamaño del entorno")
plt.xlabel("Tamaño del entorno (N×N)")
plt.ylabel("Porcentaje limpiado (%)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(images_dir / "limpieza_por_tamaño.png", dpi=140)
plt.close()

# --- GRÁFICO 2: Por nivel de suciedad ---
plt.figure(figsize=(8,5))
for agent in df["Agente"].unique():
    data = (
        df.groupby(["Agente", "Suciedad (%)"])["Porcentaje limpiado (%)"]
        .mean()
        .reset_index()
    )
    data_agent = data[data["Agente"] == agent]
    plt.plot(data_agent["Suciedad (%)"], data_agent["Porcentaje limpiado (%)"],
             marker="o", label=agent)

plt.title("Porcentaje promedio limpiado según nivel de suciedad")
plt.xlabel("Suciedad inicial (%)")
plt.ylabel("Porcentaje limpiado (%)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(images_dir / "limpieza_por_suciedad.png", dpi=140)
plt.close()

# --- GRÁFICO 3: Limpieza por tamaño Y suciedad ---
plt.figure(figsize=(10,6))
for agent in df["Agente"].unique():
    pivot = (
        df[df["Agente"] == agent]
        .groupby(["Tamaño (N×N)", "Suciedad (%)"])["Porcentaje limpiado (%)"]
        .mean()
        .unstack()
    )
    plt.plot(pivot.index, pivot[0.1], "o--", label=f"{agent} (0.1)")
    plt.plot(pivot.index, pivot[0.4], "s--", label=f"{agent} (0.4)")
    plt.plot(pivot.index, pivot[0.8], "D--", label=f"{agent} (0.8)")

plt.title("Comparación combinada por tamaño y nivel de suciedad")
plt.xlabel("Tamaño del entorno (N×N)")
plt.ylabel("Porcentaje limpiado (%)")
plt.legend(title="Agente (Suciedad)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(images_dir / "limpieza_tamaño_y_suciedad.png", dpi=140)
plt.close()

# === GRÁFICO: Acciones promedio por tamaño del entorno ===
acciones_by_size = (
    df.groupby(["Agente", "Tamaño (N×N)"])["Acciones totales"]
      .median()   # la mediana es más robusta que el promedio
      .reset_index()
      .sort_values("Tamaño (N×N)")
)

plt.figure(figsize=(8, 5))
for agent in acciones_by_size["Agente"].unique():
    data = acciones_by_size[acciones_by_size["Agente"] == agent]
    plt.plot(data["Tamaño (N×N)"], data["Acciones totales"], marker="o", label=agent)

plt.title("Mediana de acciones totales según tamaño del entorno")
plt.xlabel("Tamaño del entorno (N×N)")
plt.ylabel("Acciones totales (hasta 1000)")
plt.ylim(0, 1050)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(images_dir / "acciones_por_tamaño_median.png", dpi=140)
plt.close()


print(f"🖼️ Gráficos adicionales guardados en: {images_dir}")
