import importlib
import random
import time
import csv
import statistics
import matplotlib.pyplot as plt
from collections import defaultdict
import os

# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================
ALGORITHMS = {
    "random": "reinas_random",
    "HC": "hill_climbing",
    "HCR": "hill_climbing_random",
    "SA": "simulated_annealing",
    "GA": "genetico",
}

SIZES = [4, 8, 10]       
SEEDS = list(range(30))   
MAX_ESTADOS = 20000       
OUT_CSV = "../tp4-Nreinas.csv"
IMG_DIR = "../images"
os.makedirs(IMG_DIR, exist_ok=True)


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================
def load_algorithm(name):
    """Importa el archivo Python correspondiente al algoritmo."""
    return importlib.import_module(ALGORITHMS[name])

def run_algorithm(algorithm, N, seed):
    """Ejecuta el algoritmo usando su main() y devuelve resultados uniformes."""
    mod = load_algorithm(algorithm)
    start = time.time()
    # Cada módulo debe exponer una función main(N, max_estados, seed)
    result = mod.main(N, MAX_ESTADOS, seed)
    end = time.time()

    return {
        "algorithm_name": algorithm,
        "env_n": seed,
        "size": N,
        "best_solution": result["solution"],
        "H": result["H"],
        "states": result["states"],
        "time": end - start,
    }

# ============================================================
# EXPERIMENTOS
# ============================================================
def run_experiments():
    rows = []
    for N in SIZES:
        print(f"\n=== Ejecutando experimentos para N={N} ===")
        for seed in SEEDS:
            for algo in ALGORITHMS.keys():
                print(f"  -> {algo} (seed={seed})")
                res = run_algorithm(algo, N, seed)
                rows.append(res)
    return rows


# ============================================================
# GUARDAR CSV
# ============================================================
def save_csv(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["algorithm_name", "env_n", "size", "best_solution", "H", "states", "time"])
        for r in rows:
            writer.writerow([r["algorithm_name"], r["env_n"], r["size"], r["best_solution"],
                             r["H"], r["states"], f"{r['time']:.6f}"])
    print(f"\n✅ Resultados guardados en {path}")


# ============================================================
# CÁLCULO DE ESTADÍSTICAS Y GRÁFICOS
# ============================================================
def group_by(rows, key_fn):
    d = defaultdict(list)
    for r in rows:
        d[key_fn(r)].append(r)
    return d

def resumen_estadistico(rows):
    resumen = []
    g = group_by(rows, lambda r: (r["algorithm_name"], r["size"]))
    for (algo, N), lst in sorted(g.items()):
        Hs = [r["H"] for r in lst]
        times = [r["time"] for r in lst]
        states = [r["states"] for r in lst]
        success = sum(1 for r in lst if r["H"] == 0) / len(lst) * 100
        resumen.append({
            "algorithm": algo,
            "size": N,
            "success_%": round(success, 1),
            "H_mean": round(statistics.mean(Hs), 2),
            "H_std": round(statistics.stdev(Hs), 2) if len(Hs) > 1 else 0,
            "time_mean": round(statistics.mean(times), 4),
            "time_std": round(statistics.stdev(times), 4) if len(times) > 1 else 0,
            "states_mean": round(statistics.mean(states), 1),
            "states_std": round(statistics.stdev(states), 1) if len(states) > 1 else 0,
        })
    return resumen

def plot_boxplots(rows):
    grouped = group_by(rows, lambda r: r["size"])
    for N, data in grouped.items():
        by_algo = group_by(data, lambda r: r["algorithm_name"])
        labels = list(by_algo.keys())
        H_data = [[r["H"] for r in by_algo[a]] for a in labels]
        plt.boxplot(H_data, labels=labels)
        plt.title(f"H por algoritmo (N={N})")
        plt.ylabel("H final")
        plt.tight_layout()
        plt.savefig(os.path.join(IMG_DIR, f"boxplot_H_N{N}.png"))
        plt.close()
    print(f"📊 Boxplots guardados en {IMG_DIR}/")

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    rows = run_experiments()
    save_csv(rows, OUT_CSV)
    resumen = resumen_estadistico(rows)
    for r in resumen:
        print(r)
    plot_boxplots(rows)
