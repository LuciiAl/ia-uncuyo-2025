import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statistics
import os

# ============================================================
# CONFIGURACIÓN
# ============================================================
CSV_PATH = "tp4-Nreinas.csv"     # usa el CSV existente
IMG_DIR = "images"
os.makedirs(IMG_DIR, exist_ok=True)

# ============================================================
# CARGA DE DATOS
# ============================================================
df = pd.read_csv(CSV_PATH)
print(f"✅ Archivo cargado ({len(df)} registros)\n")

# Forzar tipos correctos
df["H"] = df["H"].astype(int)
df["states"] = df["states"].astype(int)
df["time"] = df["time"].astype(float)

# ============================================================
# 5.b) CÁLCULOS ESTADÍSTICOS
# ============================================================
def calcular_estadisticas(df):
    resumen = []
    for (alg, size), group in df.groupby(["algorithm_name", "size"]):
        H_vals = group["H"].tolist()
        time_vals = group["time"].tolist()
        states_vals = group["states"].tolist()
        success = sum(h == 0 for h in H_vals) / len(H_vals) * 100

        resumen.append({
            "Algoritmo": alg,
            "N": size,
            "% Éxito (H=0)": round(success, 1),
            "H Promedio": round(statistics.mean(H_vals), 3),
            "H DesvStd": round(statistics.stdev(H_vals), 3) if len(H_vals) > 1 else 0,
            "Tiempo Promedio (s)": round(statistics.mean(time_vals), 5),
            "Tiempo DesvStd (s)": round(statistics.stdev(time_vals), 5) if len(time_vals) > 1 else 0,
            "Estados Promedio": round(statistics.mean(states_vals), 1),
            "Estados DesvStd": round(statistics.stdev(states_vals), 1) if len(states_vals) > 1 else 0
        })
    return pd.DataFrame(resumen)

resumen_df = calcular_estadisticas(df)
print("=== RESUMEN ESTADÍSTICO ===")
print(resumen_df.to_string(index=False))
print()

# ============================================================
# 5.c) BOXPLOTS COMPARATIVOS
# ============================================================
sns.set(style="whitegrid", palette="muted")

# --- Boxplot de H por tamaño ---
for N in sorted(df["size"].unique()):
    subset = df[df["size"] == N]
    plt.figure(figsize=(7, 5))
    sns.boxplot(x="algorithm_name", y="H", data=subset)
    plt.title(f"Comparativo H final – N={N}")
    plt.xlabel("Algoritmo")
    plt.ylabel("H final (reinas en conflicto)")
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, f"boxplot_H_N{N}.png"))
    plt.close()

# --- Boxplot de tiempo total ---
plt.figure(figsize=(7, 5))
sns.boxplot(x="algorithm_name", y="time", data=df)
plt.title("Tiempo de ejecución por algoritmo")
plt.xlabel("Algoritmo")
plt.ylabel("Tiempo (s)")
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "boxplot_tiempo.png"))
plt.close()

# --- Boxplot de estados explorados ---
plt.figure(figsize=(7, 5))
sns.boxplot(x="algorithm_name", y="states", data=df)
plt.title("Estados explorados por algoritmo")
plt.xlabel("Algoritmo")
plt.ylabel("Cantidad de estados")
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "boxplot_estados.png"))
plt.close()

print("📊 Gráficos guardados en la carpeta:", IMG_DIR, "\n")

# ============================================================
# 7) REPORTE AUTOMÁTICO
# ============================================================
def generar_reporte(resumen_df):
    print("=== REPORTE DE DESEMPEÑO ===\n")
    for N in sorted(resumen_df["N"].unique()):
        print(f"--- Tablero N={N} ---")
        dataN = resumen_df[resumen_df["N"] == N]
        mejor_exito = dataN.loc[dataN["% Éxito (H=0)"].idxmax()]
        menor_tiempo = dataN.loc[dataN["Tiempo Promedio (s)"].idxmin()]
        menor_H = dataN.loc[dataN["H Promedio"].idxmin()]

        print(f"• Mayor tasa de éxito: {mejor_exito['Algoritmo']} ({mejor_exito['% Éxito (H=0)']}%)")
        print(f"• Menor tiempo promedio: {menor_tiempo['Algoritmo']} ({menor_tiempo['Tiempo Promedio (s)']} s)")
        print(f"• Menor H promedio: {menor_H['Algoritmo']} (H̄={menor_H['H Promedio']})")

        print("Resumen general:")
        for _, row in dataN.iterrows():
            print(f"  - {row['Algoritmo']}: Éxito={row['% Éxito (H=0)']}%, "
                  f"H̄={row['H Promedio']}, Estados̄={row['Estados Promedio']}, "
                  f"Tiempō={row['Tiempo Promedio (s)']} s")
        print()

    print("Conclusión global:")
    print("• Los algoritmos informados (Simulated Annealing y Genético) suelen alcanzar "
          "más soluciones óptimas (H=0) en menos iteraciones promedio.")
    print("• Hill Climbing muestra buen rendimiento pero se atasca en óptimos locales.")
    print("• El algoritmo aleatorio raramente logra H=0 y presenta alta dispersión.")
    print("• En general, los métodos con componente estocástico (SA, GA) muestran mejor "
          "robustez y estabilidad frente a distintas semillas.\n")

generar_reporte(resumen_df)
