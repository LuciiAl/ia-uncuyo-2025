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

# Limpiamos valores nulos o sin suciedad
df = df[(df["Suciedad inicial"] > 0) & (df["Acciones totales"] > 0)].copy()

# Calculamos métricas derivadas
df["Porcentaje limpiado (%)"] = (df["Celdas limpiadas"] / df["Suciedad inicial"]).clip(upper=1) * 100
df["Eficiencia"] = df["Celdas limpiadas"] / df["Acciones totales"]

print("Datos cargados correctamente ✅")

# === 1️⃣ Gráficos por TAMAÑO de entorno ===
for size in sorted(df["Tamaño (N×N)"].unique()):
    subset = df[df["Tamaño (N×N)"] == size]
    grouped = (
        subset.groupby(["Agente", "Suciedad (%)"])["Porcentaje limpiado (%)"]
        .mean()
        .reset_index()
    )

    plt.figure(figsize=(7,5))
    for agent in grouped["Agente"].unique():
        data = grouped[grouped["Agente"] == agent]
        plt.plot(data["Suciedad (%)"], data["Porcentaje limpiado (%)"], marker="o", label=agent)

    plt.title(f"Comparación por nivel de suciedad (Tamaño {size}×{size})")
    plt.xlabel("Suciedad inicial (%)")
    plt.ylabel("Porcentaje limpiado (%)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(images_dir / f"comparacion_por_suciedad_size_{size}.png", dpi=140)
    plt.close()

print("📊 Gráficos generados por tamaño de entorno.")


# === 2️⃣ Gráficos por SUCIEDAD inicial ===
for dirt in sorted(df["Suciedad (%)"].unique()):
    subset = df[df["Suciedad (%)"] == dirt]
    grouped = (
        subset.groupby(["Agente", "Tamaño (N×N)"])["Porcentaje limpiado (%)"]
        .mean()
        .reset_index()
    )

    plt.figure(figsize=(7,5))
    for agent in grouped["Agente"].unique():
        data = grouped[grouped["Agente"] == agent]
        plt.plot(data["Tamaño (N×N)"], data["Porcentaje limpiado (%)"], marker="o", label=agent)

    plt.title(f"Comparación por tamaño del entorno (Suciedad {dirt*100:.0f}%)")
    plt.xlabel("Tamaño del entorno (N×N)")
    plt.ylabel("Porcentaje limpiado (%)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(images_dir / f"comparacion_por_tamaño_dirt_{int(dirt*100)}.png", dpi=140)
    plt.close()

print("🧩 Gráficos generados por porcentaje de suciedad.")
print(f"🖼️ Todos los gráficos guardados en: {images_dir}")
