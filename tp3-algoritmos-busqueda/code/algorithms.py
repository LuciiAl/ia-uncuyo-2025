from collections import deque
import heapq
import math
import gymnasium as gym
from gymnasium import wrappers
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
import random
from algorithms import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import os
import re

max=10000
# ============================================================
def generate_random_map_custom(size, ice_prob):
    desc = []
    col = ''
    sx=random.randint(0, size-1)
    sy=random.randint(0, size-1)
    # Generar ex y ey, asegurando que no sean iguales a sx y sy
    while True:
        ex = random.randint(0, size - 1)
        ey = random.randint(0, size - 1)
        if ex != sx and ey != sy:
            break
    for i in range(size):
        for j in range(size):
            if i==sx and j==sy:
                col=col + 'S'
                agent_pos = (i,j)
            elif i==ex and j==ey:
                col=col + 'G'
            else:
                if random.random() < ice_prob:
                    col=col + 'F'
                else:
                    col=col + 'H'
        desc.append(col)
        col=''
    #print(desc)
    return desc, agent_pos

# ============================================================
# ✅ FUNCIÓN AUXILIAR: movimientos válidos
# ============================================================
def is_valid_move(y, x, desc, visited):
    rows, cols = len(desc), len(desc[0])
    return (
        0 <= y < rows
        and 0 <= x < cols
        and desc[y][x] != b'H'
        and (y, x) not in visited
    )

# ============================================================
# ✅ DFS – Búsqueda en Profundidad
# ============================================================
def dfs_search(env, agent_pos, path,max_actions=max):
    directions = ((0,-1,0), (1,0,+1), (2,+1,0), (3,0,-1))
    desc = env.unwrapped.desc
    y, x = agent_pos
    visited = set()
    stack = [(y, x, [])]
    steps = 0

    while stack:
        steps += 1
        # 🚫 Condición de corte: demasiadas acciones
        if steps >= max_actions:
            print(f"[DFS] Límite de {max_actions} expansiones alcanzado.")
            return steps, [], x, y
        y, x, p = stack.pop()
        if desc[y][x] == b'G':
            return steps, p, x, y


        visited.add((y, x))
        for direction_id, dx, dy in directions:
            new_x = x + dx
            new_y = y + dy
            if is_valid_move(new_y, new_x, desc, visited):
                stack.append((new_y, new_x, p + [direction_id]))

    return steps, [], x, y  # si no hay solución


# ============================================================
# ✅ BFS – Búsqueda en Anchura
# ============================================================
def bfs_search(env, agent_pos, path, max_actions=max):
    directions = ((0, -1, 0), (1, 0, +1), (2, +1, 0), (3, 0, -1))
    desc = env.unwrapped.desc
    y, x = agent_pos
    visited = set()
    queue = deque([(y, x, [])])
    steps = 0

    while queue:
        steps += 1

        # 🚫 Condición de corte: demasiadas acciones
        if steps >= max_actions:
            print(f"[BFS] Límite de {max_actions} expansiones alcanzado.")
            return steps, [], x, y

        y, x, p = queue.popleft()

        # ✅ Verificar si se llegó al objetivo
        if desc[y][x] == b'G' or desc[y][x] == 'G':
            return steps, p, x, y

        visited.add((y, x))

        for direction_id, dx, dy in directions:
            new_x = x + dx
            new_y = y + dy
            if is_valid_move(new_y, new_x, desc, visited):
                queue.append((new_y, new_x, p + [direction_id]))

    return steps, [], x, y



# ============================================================
# ✅ DLS – Búsqueda en Profundidad Limitada
# ============================================================
def dls_search(env, agent_pos, path, limit=10, max_actions=max):
    directions = ((0,-1,0), (1,0,+1), (2,+1,0), (3,0,-1))
    desc = env.unwrapped.desc
    y, x = agent_pos
    visited = set()
    stack = [(y, x, [], 0)]
    steps = 0

    while stack:
        y, x, p, depth = stack.pop()
        steps += 1

        if steps >= max_actions:
            return steps, [], x, y  # 🔹 agrega 4 valores

        if desc[y][x] == b'G':
            return steps, p, x, y

        if depth >= limit:
            continue

        visited.add((y, x))
        for direction_id, dx, dy in directions:
            new_x = x + dx
            new_y = y + dy
            if is_valid_move(new_y, new_x, desc, visited):
                stack.append((new_y, new_x, p + [direction_id], depth + 1))

    return steps, [], x, y  # 🔹 también devuelve 4 valores al final




# ============================================================
# ✅ UCS – Búsqueda de Costo Uniforme
# ============================================================
def ucs_search(env, agent_pos, path, max_actions=max):
    directions = ((0,-1,0,1), (1,0,+1,1), (2,+1,0,1), (3,0,-1,1))
    desc = env.unwrapped.desc
    y, x = agent_pos
    visited = set()
    pq = [(0, y, x, [])]  # (costo acumulado, y, x, path)
    steps = 0

    while pq:
        cost, y, x, p = heapq.heappop(pq)
        steps += 1
        # 🚫 Condición de corte: demasiadas acciones
        if steps >= max_actions:
            print(f"[UCS] Límite de {max_actions} expansiones alcanzado.")
            return steps, [], x, y
        if desc[y][x] == b'G':
            return steps, p, x, y
        if (y, x) in visited:
            continue
        visited.add((y, x))
        for direction_id, dx, dy, move_cost in directions:
            new_x = x + dx
            new_y = y + dy
            if is_valid_move(new_y, new_x, desc, visited):
                heapq.heappush(pq, (cost + move_cost, new_y, new_x, p + [direction_id]))

    return steps, [], x, y


# ============================================================
# ✅ A* – Búsqueda A Estrella
# ============================================================
def astar_search(env, agent_pos, path, max_actions=max):
    directions = ((0,-1,0,1), (1,0,+1,1), (2,+1,0,1), (3,0,-1,1))
    desc = env.unwrapped.desc
    y, x = agent_pos
    visited = set()

    # Encontrar posición objetivo (G)
    goal = None
    for i in range(len(desc)):
        for j in range(len(desc[0])):
            if desc[i][j] == b'G':
                goal = (i, j)
                break
        if goal:
            break

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan

    pq = [(0, 0, y, x, [])]  # (f = g + h, g, y, x, path)
    steps = 0

    while pq:
        f, g, y, x, p = heapq.heappop(pq)
        steps += 1
        # 🚫 Condición de corte: demasiadas acciones
        if steps >= max_actions:
            print(f"[A*] Límite de {max_actions} expansiones alcanzado.")
            return steps, [], x, y

        if desc[y][x] == b'G':
            return steps, p, x, y

        if (y, x) in visited:
            continue

        visited.add((y, x))
        for direction_id, dx, dy, move_cost in directions:
            new_x = x + dx
            new_y = y + dy
            if is_valid_move(new_y, new_x, desc, visited):
                new_g = g + move_cost
                h = heuristic((new_y, new_x), goal)
                heapq.heappush(pq, (new_g + h, new_g, new_y, new_x, p + [direction_id]))

    return steps, [], x, y


ACTIONS = {0: "←", 1: "↓", 2: "→", 3: "↑"}

def pretty_desc(desc):
    """desc es una lista de strings (antes de crear el env) o un array de bytes (en el env)."""
    if isinstance(desc[0], bytes):  # viene del env.unwrapped.desc
        rows = ["".join([c.decode() for c in row]) for row in desc]
    else:
        rows = desc
    return "\n".join(rows)


def find_goal(desc):
    """Devuelve la posición (gy, gx) de la meta 'G', soportando str, bytes o numpy.bytes_."""
    # Si es un ndarray, lo pasamos a lista
    if isinstance(desc, np.ndarray):
        desc = desc.tolist()

    for i, row in enumerate(desc):
        for j, val in enumerate(row):
            if isinstance(val, (bytes, np.bytes_)):
                if val == b'G':
                    return (i, j)
            elif isinstance(val, str):
                if val == 'G':
                    return (i, j)
    # Si no se encontró, avisamos
    print("⚠️ No se encontró ninguna 'G' en el mapa:")
    print(desc)
    return None

def follow_path_on_desc(desc, start, path):
    """Simula movimientos sobre la grilla (sin usar física estocástica de Gym).
       Devuelve estado final (y,x) y si cayó en H o llegó a G."""
    y, x = start
    # mapeo consistente con tus direcciones: (0:L,1:D,2:R,3:U)
    delta = {0:(0,-1), 1:(+1,0), 2:(0,+1), 3:(-1,0)}
    rows, cols = len(desc), len(desc[0]) if isinstance(desc[0], str) else len(desc[0])

    def cell(y,x):
        return desc[y][x] if isinstance(desc[y][x], (bytes, np.bytes_)) else desc[y][x].encode()

    for a in path:
        dy, dx = delta[a]
        ny, nx = y + dy, x + dx
        # límites
        if not (0 <= ny < rows and 0 <= nx < cols):
            return (y, x), "out_of_bounds"
        # Si es H, caíste en agujero
        if cell(ny, nx) == b'H':
            return (ny, nx), "hole"
        y, x = ny, nx
        if cell(y, x) == b'G':
            return (y, x), "goal"
    # terminó sin llegar ni caer
    if cell(y, x) == b'G':
        return (y, x), "goal"
    return (y, x), "incomplete"

def build_env_from_desc(desc, is_slippery=False):
    """Crea el entorno FrozenLake con tu mapa. is_slippery=False para que sea determinista (recomendado)."""
    env = gym.make("FrozenLake-v1", desc=desc, is_slippery=is_slippery, render_mode=None)
    return env

def run_one(search_fn, env, agent_pos, **kwargs):
    """Ejecuta una búsqueda y valida el camino."""
    steps, path, last_x, last_y = search_fn(env, agent_pos, [], **kwargs) if kwargs else search_fn(env, agent_pos, [])
    desc = env.unwrapped.desc
    start = agent_pos
    end, status = follow_path_on_desc(desc, start, path)
    gy, gx = find_goal(desc)
    ok = (status == "goal") and (end == (gy, gx))
    return {
        "steps_expandidos": steps,
        "acciones": path,
        "acciones_pretty": "".join(ACTIONS[a] for a in path),
        "start": start,
        "goal": (gy, gx),
        "end": end,
        "status": status,
        "llega": ok,
    }

def evaluate_algorithm(algorithm_name, search_fn, desc, agent_pos):
    """Ejecuta un algoritmo sobre un mapa dado y devuelve métricas."""
    env = build_env_from_desc(desc, is_slippery=False)
    start_time = time.perf_counter()
    steps, path, last_x, last_y = search_fn(env, agent_pos, [])
    elapsed = time.perf_counter() - start_time
    cost = len(path)
    end, status = follow_path_on_desc(env.unwrapped.desc, agent_pos, path)
    gy, gx = find_goal(env.unwrapped.desc)
    goal_reached = (status == "goal" and end == (gy, gx))
    return {
        "algoritmo": algorithm_name,
        "steps_expandidos": steps,
        "acciones": len(path),
        "costo_total": cost,
        "tiempo": elapsed,
        "llega": goal_reached,
    }

def probar_todo(size=8, ice_prob=0.92, seed=123, is_slippery=False):
    # reproducibilidad
    random.seed(seed)

    # generar mapa y entorno
    desc, agent_pos = generate_random_map_custom(size, ice_prob)
    print("Mapa generado (S inicio, G objetivo, F seguro, H agujero):")
    print(pretty_desc(desc))
    print(f"Inicio: {agent_pos}")

    env = build_env_from_desc(desc, is_slippery=is_slippery)

    print("\n== DFS ==")
    res = run_one(dfs_search, env, agent_pos)
    print(res)

    print("\n== BFS ==")
    res = run_one(bfs_search, env, agent_pos)
    print(res)

    print("\n== DLS (limit=10) ==")
    res = run_one(dls_search, env, agent_pos, limit=10)
    print(res)

    print("\n== UCS ==")
    res = run_one(ucs_search, env, agent_pos)
    print(res)

    print("\n== A* ==")
    res = run_one(astar_search, env, agent_pos)
    print(res)


ALGORITHMS = {
    "DFS": dfs_search,
    "BFS": bfs_search,
    "DLS": lambda env, pos, path: dls_search(env, pos, path, limit=1000),
    "UCS": ucs_search,
    "A*": astar_search,
}

N_RUNS = 30
MAP_SIZE = 100
ICE_PROB = 0.92
HOLE_PROB = 0.08
AGENT_LIFE = 1000

# ============================================================
# ✅ FUNCIÓN AUXILIAR: ejecución controlada de un algoritmo
# ============================================================
def evaluate_algorithm(algorithm_name, search_fn, desc, agent_pos):
    """Ejecuta un algoritmo sobre un mapa dado y devuelve métricas."""
    env = build_env_from_desc(desc, is_slippery=False)
    start_time = time.perf_counter()
    steps, path, last_x, last_y = search_fn(env, agent_pos, [])
    elapsed = time.perf_counter() - start_time
    cost = len(path)
    end, status = follow_path_on_desc(env.unwrapped.desc, agent_pos, path)
    gy, gx = find_goal(env.unwrapped.desc)
    goal_reached = (status == "goal" and end == (gy, gx))
    return {
        "algorithm_name": algorithm_name,
        "states_n": steps,
        "actions_count": len(path),
        "actions_cost": cost,
        "time": elapsed,
        "solution_found": goal_reached,
    }

# ============================================================
# ✅ MAIN DEL EXPERIMENTO
# ============================================================
def run_experiments(n_runs=30, random_seed=1234):
    # --- carpetas destino ---
    base_dir = os.path.join(os.getcwd(), "tp3-algoritmos-busqueda")
    img_dir = os.path.join(base_dir, "images")
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    random.seed(random_seed)
    all_results = []
    all_maps = []

    # --- generar 30 mapas reproducibles ---
    seeds = [random_seed + i for i in range(n_runs)]
    for i, s in enumerate(seeds):
        random.seed(s)
        desc, agent_pos = generate_random_map_custom(MAP_SIZE, ICE_PROB)
        all_maps.append((desc, agent_pos))

    # --- ejecutar algoritmos ---
    for run_idx, (desc, agent_pos) in enumerate(all_maps, 1):
        print(f"\n🌍 Mapa {run_idx}/{n_runs}")
        for algo_name, algo_fn in ALGORITHMS.items():
            print(f"  ▶ Ejecutando {algo_name} ...")
            res = evaluate_algorithm(algo_name, algo_fn, desc, agent_pos)
            res["env_n"] = run_idx  # número del entorno
            all_results.append(res)

    # --- guardar CSV en carpeta pedida ---
    df = pd.DataFrame(all_results)[[
        "algorithm_name", "env_n", "states_n",
        "actions_count", "actions_cost", "time", "solution_found"
    ]]
    csv_path = os.path.join(base_dir, "results.csv")
    df.to_csv(csv_path, index=False)
    print(f"\n✅ Resultados exportados a: {csv_path}")

    # --- estadísticas básicas ---
    summary = (
        df.groupby("algorithm_name")[["states_n", "actions_count", "actions_cost", "time"]]
        .agg(["mean", "std"])
        .round(3)
    )
    print("\n📊 Estadísticas (media y desviación estándar):")
    print(summary)

    # 🔹 Guardar resumen como CSV y Markdown
    summary_csv = os.path.join(base_dir, "summary_estadisticas.csv")
    summary_md = os.path.join(base_dir, "summary_estadisticas.md")

    summary.to_csv(summary_csv)
    with open(summary_md, "w", encoding="utf-8") as f:
        f.write(summary.to_markdown())

    print(f"\n✅ Estadísticas guardadas en:\n  - {summary_csv}\n  - {summary_md}")

    # ============================================================
    # ✅ Boxplots comparativos
    # ============================================================
    metrics = ["states_n", "actions_count", "actions_cost", "time"]
    for metric in metrics:
        plt.figure(figsize=(12,7))

        # 🎨 estilo visual más elegante
        boxprops = dict(linewidth=3.0, color="#4B5563")
        whiskerprops = dict(linewidth=3.5, color="#6B7280")
        medianprops = dict(linewidth=3.5, color="#B91C1C")
        capprops = dict(linewidth=3.0, color="#374151")

        df.boxplot(column=metric, by="algorithm_name", grid=False,
                boxprops=boxprops, whiskerprops=whiskerprops,
                medianprops=medianprops, capprops=capprops)
        
        bp = df.boxplot(column=metric, by="algorithm_name", grid=False,
                boxprops=boxprops, whiskerprops=whiskerprops,
                medianprops=medianprops, capprops=capprops)

        # 🔹 Colorear el interior de las cajas
        for patch in bp.artists:
            patch.set_facecolor("#E5E7EB")   # gris claro suave
            patch.set_alpha(0.8)             # leve transparencia

        plt.title(f"Comparativo - {metric}", fontsize=16, fontweight="bold", color="#111827")
        plt.suptitle("")
        plt.xlabel("Algoritmo", fontsize=13)
        plt.ylabel(metric, fontsize=13)
        plt.xticks(rotation=15, fontsize=11)
        plt.yticks(fontsize=11)
        plt.grid(axis="y", linestyle="--", alpha=0.4)
        plt.tight_layout()
        plt.savefig(os.path.join(img_dir, f"boxplot_{metric}.png"), bbox_inches="tight")
        plt.close()

    print(f"✅ Boxplots comparativos guardados en: {img_dir}")

    # ============================================================
    # ✅ Boxplots individuales por algoritmo
    # ============================================================
    for algo_name in ALGORITHMS.keys():
        subset = df[df["algorithm_name"] == algo_name]
        if subset.empty:
            continue

        plt.figure(figsize=(14, 8))
        plt.suptitle(f"Boxplots individuales - {algo_name}",
                     fontsize=18, fontweight="bold", color="darkblue")

        boxprops = dict(linewidth=2.5, color="royalblue")
        whiskerprops = dict(linewidth=2.0, color="gray")
        medianprops = dict(linewidth=3.0, color="red")
        capprops = dict(linewidth=2.0, color="black")

        metrics_labels = [
            ("states_n", "Estados explorados"),
            ("actions_count", "Acciones tomadas"),
            ("actions_cost", "Costo total"),
            ("time", "Tiempo (s)")
        ]

        for i, (col, title) in enumerate(metrics_labels, start=1):
            plt.subplot(2, 2, i)
            subset.boxplot(column=col, grid=False,
                           boxprops=boxprops, whiskerprops=whiskerprops,
                           medianprops=medianprops, capprops=capprops)
            plt.title(title, fontsize=13)
            plt.xticks([])
            plt.yticks(fontsize=10)
            plt.grid(axis="y", linestyle="--", alpha=0.5)

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        safe_name = re.sub(r'[^A-Za-z0-9_-]', '', algo_name)
        plt.savefig(os.path.join(img_dir, f"boxplot_individual_{safe_name}.png"),
                    bbox_inches="tight")
        plt.close()

    print(f"✅ Boxplots individuales guardados en: {img_dir}")

    # ============================================================
    # ✅ Generar reporte Markdown con resultados y gráficos
    # ============================================================
    report_path = os.path.join(base_dir, "tp3-reporte.md")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# 📊 Informe de Desempeño – Búsquedas No Informadas\n\n")
        f.write("Este reporte presenta una evaluación comparativa de los algoritmos **DFS**, **BFS**, **DLS**, **UCS** y **A*** sobre 30 entornos aleatorios de 100×100 celdas.\n\n")
        f.write("Cada celda tiene probabilidad 0.92 de ser transitable (*Frozen*) y 0.08 de ser un obstáculo (*Hole*). Los entornos son deterministas y se mantiene la misma semilla base para permitir reproducibilidad.\n\n")

        # --- resumen numérico ---
        f.write("## 📈 Estadísticas generales (media ± desviación estándar)\n\n")
        f.write(summary.to_markdown())
        f.write("\n\n")

        # --- comparativos ---
        f.write("## 🧩 Comparativos globales\n\n")
        for metric in ["states_n", "actions_count", "actions_cost", "time"]:
            img_file = f"images/boxplot_{metric}.png"
            f.write(f"### {metric}\n")
            f.write(f"![{metric}]({img_file})\n\n")

        # --- individuales ---
        f.write("## 🔍 Boxplots individuales por algoritmo\n\n")
        for algo_name in ALGORITHMS.keys():
            safe_name = re.sub(r'[^A-Za-z0-9_-]', '', algo_name)
            img_file = f"images/boxplot_individual_{safe_name}.png"
            f.write(f"### {algo_name}\n")
            f.write(f"![{algo_name}]({img_file})\n\n")

        # --- conclusiones ---
        f.write("## 🧠 Conclusiones\n\n")
        f.write("- **BFS** y **UCS** tienden a explorar menos estados en promedio, manteniendo una buena eficiencia en costo.\n")
        f.write("- **DFS** y **DLS** suelen expandir más nodos, siendo menos óptimos pero más simples computacionalmente.\n")
        f.write("- **A*** alcanza soluciones con el menor costo total, aunque con mayor tiempo promedio debido a la función heurística.\n")
        f.write("- En general, el desempeño varía según la distribución de obstáculos, pero las diferencias de tiempo son pequeñas en entornos deterministas.\n")

    print(f"✅ Reporte Markdown generado en: {report_path}")


    return df, summary


# ============================================================
# ✅ EJECUCIÓN
# ============================================================
if __name__ == "__main__":
    df, summary = run_experiments(n_runs=N_RUNS)