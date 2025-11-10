import importlib
import random
import time
import csv
import statistics
import os
from collections import defaultdict

# ============================================================
# CONFIGURACIÓN
# ============================================================
SIZES = [4, 8, 10]          # opcional: [4, 8, 10, 12, 15]
SEEDS = list(range(30))     # 30 ejecuciones por configuración
OUT_CSV = "tp5-csp-nreinas.csv"
SUMMARY_CSV = "tp5-csp-summary.csv"
IMG_DIR = "images"
os.makedirs(IMG_DIR, exist_ok=True)

# Cargar tu módulo con los algoritmos CSP
nreinas = importlib.import_module("nreinas_csp")

# Intentar cargar matplotlib (si no está, omite los gráficos)
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MPL = True
except Exception:
    HAS_MPL = False


# ============================================================
# FUNCIÓN PARA EJECUTAR UN ALGORITMO
# ============================================================
def run_algorithm(algorithm, N, seed):
    """Ejecuta un algoritmo (backtracking o forward checking) con semilla fija."""
    random.seed(seed)
    csp = nreinas.crear_csp_nreinas(N)

    start = time.time()
    if algorithm == "backtracking":
        sol = nreinas.backtracking_search(csp)
    elif algorithm == "forward":
        sol = nreinas.forward_checking(csp)
    else:
        raise ValueError("Algoritmo no reconocido.")
    end = time.time()

    # Determinar si se encontró una solución válida
    found = sol is not None
    nodos = csp.contadores["asignaciones"]
    tiempo = end - start

    return {
        "algorithm": algorithm,
        "N": N,
        "seed": seed,
        "found": found,
        "time": tiempo,
        "nodes": nodos
    }


# ============================================================
# EJECUTAR TODOS LOS EXPERIMENTOS
# ============================================================
def run_all():
    resultados = []
    for N in SIZES:
        for seed in SEEDS:
            for algo in ["backtracking", "forward"]:
                print(f"Ejecutando {algo} (N={N}, seed={seed})...")
                res = run_algorithm(algo, N, seed)
                resultados.append(res)
    return resultados


# ============================================================
# GUARDAR CSV COMPLETO
# ============================================================
def save_csv(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["algorithm", "N", "seed", "found", "time", "nodes"])
        for r in rows:
            writer.writerow([r["algorithm"], r["N"], r["seed"], int(r["found"]),
                             f"{r['time']:.6f}", r["nodes"]])
    print(f"\n✅ Resultados detallados guardados en {path}")


# ============================================================
# CÁLCULO DE MÉTRICAS
# ============================================================
def resumen_estadistico(rows):
    resumen = []
    grupo = defaultdict(list)
    for r in rows:
        grupo[(r["algorithm"], r["N"])].append(r)

    for (algo, N), lista in sorted(grupo.items()):
        exito = sum(r["found"] for r in lista) / len(lista) * 100
        tiempos = [r["time"] for r in lista]
        nodos = [r["nodes"] for r in lista]

        resumen.append({
            "algorithm": algo,
            "N": N,
            "success_%": round(exito, 1),
            "time_mean": statistics.mean(tiempos),
            "time_std": statistics.stdev(tiempos),
            "nodes_mean": statistics.mean(nodos),
            "nodes_std": statistics.stdev(nodos)
        })
    return resumen


# ============================================================
# GUARDAR RESUMEN CSV
# ============================================================
def save_summary_csv(resumen, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["algorithm", "N", "success_%", "time_mean", "time_std", "nodes_mean", "nodes_std"])
        for r in resumen:
            writer.writerow([r["algorithm"], r["N"], r["success_%"],
                             f"{r['time_mean']:.6f}", f"{r['time_std']:.6f}",
                             f"{r['nodes_mean']:.1f}", f"{r['nodes_std']:.1f}"])
    print(f"📊 Resumen estadístico guardado en {path}")


# ============================================================
# GRÁFICOS
# ============================================================
def boxplots(rows, resumen):
    if not HAS_MPL:
        print("Matplotlib no disponible, se omiten gráficos.")
        return

    # --- Boxplots de tiempos y nodos ---
    agrupado = defaultdict(list)
    for r in rows:
        agrupado[r["N"]].append(r)

    for N, lista in agrupado.items():
        algoritmos = sorted(set(r["algorithm"] for r in lista))

        for metrica in ["time", "nodes"]:
            data = [[r[metrica] for r in lista if r["algorithm"] == a] for a in algoritmos]
            plt.figure()
            plt.boxplot(data, tick_labels=algoritmos)
            plt.title(f"Distribución de {metrica} (N={N})")
            plt.ylabel(metrica)
            plt.tight_layout()
            path_img = os.path.join(IMG_DIR, f"boxplot_{metrica}_N{N}.png")
            plt.savefig(path_img)
            plt.close()
            print(f"📈 Gráfico guardado: {path_img}")

    # --- Gráfico de barras del porcentaje de éxito ---
    plt.figure()
    for N in sorted(set(r["N"] for r in resumen)):
        subset = [r for r in resumen if r["N"] == N]
        algoritmos = [r["algorithm"] for r in subset]
        valores = [r["success_%"] for r in subset]
        plt.bar([f"{a}-N{N}" for a in algoritmos], valores, label=f"N={N}")

    plt.title("Porcentaje de ejecuciones con solución válida")
    plt.ylabel("Éxito (%)")
    plt.ylim(0, 110)
    plt.legend()
    plt.tight_layout()
    path_img = os.path.join(IMG_DIR, "success_rate.png")
    plt.savefig(path_img)
    plt.close()
    print(f"✅ Gráfico de porcentaje de éxito guardado en {path_img}")


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    resultados = run_all()
    save_csv(resultados, OUT_CSV)

    resumen = resumen_estadistico(resultados)
    save_summary_csv(resumen, SUMMARY_CSV)

    print("\n=== RESUMEN ESTADÍSTICO ===")
    for r in resumen:
        print(f"{r['algorithm']} | N={r['N']} | "
              f"Éxito={r['success_%']}% | "
              f"Tiempo={r['time_mean']:.4f}±{r['time_std']:.4f}s | "
              f"Nodos={r['nodes_mean']:.1f}±{r['nodes_std']:.1f}")

    boxplots(resultados, resumen)
