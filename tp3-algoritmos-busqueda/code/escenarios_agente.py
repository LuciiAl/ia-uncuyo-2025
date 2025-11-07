"""
===============================================================
TP3 – Agente basado en objetivos
===============================================================
Implementa los escenarios de costos y algoritmos requeridos:
1️⃣ Escenario 1: costo uniforme (todas las acciones = 1)
2️⃣ Escenario 2: movimientos horizontales = 1, verticales = 10
===============================================================
"""

import heapq
import os
import random
import time
from collections import deque
import pandas as pd



# ============================================================
# ✅ GENERADOR DE ENTORNOS
# ============================================================
def generate_grid(size=8, p_frozen=0.7):
    """Genera un entorno cuadrado con S (inicio), G (meta), F (camino), H (obstáculo)."""
    grid = []
    sx, sy = random.randint(0, size - 1), random.randint(0, size - 1)
    ex, ey = random.randint(0, size - 1), random.randint(0, size - 1)
    while (sx, sy) == (ex, ey):
        ex, ey = random.randint(0, size - 1), random.randint(0, size - 1)

    for i in range(size):
        row = []
        for j in range(size):
            if (i, j) == (sx, sy):
                row.append('S')
            elif (i, j) == (ex, ey):
                row.append('G')
            else:
                row.append('F' if random.random() < p_frozen else 'H')
        grid.append(row)
    return grid, (sx, sy), (ex, ey)


def print_grid(grid):
    for row in grid:
        print(" ".join(row))
    print()


# ============================================================
# ✅ ESCENARIOS DE COSTO
# ============================================================
def cost_function_1(dx, dy):
    """Escenario 1: todas las acciones cuestan 1"""
    return 1


def cost_function_2(dx, dy):
    """Escenario 2: izquierda/derecha = 1, arriba/abajo = 10"""
    if abs(dx) == 1 and dy == 0:  # movimiento vertical
        return 10
    else:
        return 1


# ============================================================
# ✅ MOVIMIENTOS VÁLIDOS
# ============================================================
def valid_moves(grid, y, x, visited):
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # ← ↓ → ↑
    for dy, dx in directions:
        ny, nx = y + dy, x + dx
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
            if grid[ny][nx] != 'H' and (ny, nx) not in visited:
                yield ny, nx, dx, dy


# ============================================================
# ✅ ALGORITMOS DE BÚSQUEDA
# ============================================================
def bfs(grid, start, goal):
    queue = deque([(start, [])])
    visited = {start}
    steps = 0

    while queue:
        (y, x), path = queue.popleft()
        steps += 1
        if (y, x) == goal:
            return path + [(y, x)], steps
        for ny, nx, _, _ in valid_moves(grid, y, x, visited):
            visited.add((ny, nx))
            queue.append(((ny, nx), path + [(y, x)]))
    return [], steps


def dfs(grid, start, goal):
    stack = [(start, [])]
    visited = set()
    steps = 0
    while stack:
        (y, x), path = stack.pop()
        steps += 1
        if (y, x) == goal:
            return path + [(y, x)], steps
        visited.add((y, x))
        for ny, nx, _, _ in valid_moves(grid, y, x, visited):
            stack.append(((ny, nx), path + [(y, x)]))
    return [], steps


def dls(grid, start, goal, limit=50):
    stack = [(start, [], 0)]
    visited = set()
    steps = 0
    while stack:
        (y, x), path, depth = stack.pop()
        steps += 1
        if (y, x) == goal:
            return path + [(y, x)], steps
        if depth >= limit:
            continue
        visited.add((y, x))
        for ny, nx, _, _ in valid_moves(grid, y, x, visited):
            stack.append(((ny, nx), path + [(y, x)], depth + 1))
    return [], steps


def ucs(grid, start, goal, cost_fn):
    pq = [(0, start, [])]
    visited = set()
    steps = 0
    while pq:
        cost, (y, x), path = heapq.heappop(pq)
        if (y, x) in visited:
            continue
        visited.add((y, x))
        steps += 1
        if (y, x) == goal:
            return path + [(y, x)], steps, cost
        for ny, nx, dx, dy in valid_moves(grid, y, x, visited):
            move_cost = cost_fn(dx, dy)
            heapq.heappush(pq, (cost + move_cost, (ny, nx), path + [(y, x)]))
    return [], steps, cost


def astar(grid, start, goal, cost_fn):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    pq = [(0, 0, start, [])]
    visited = set()
    steps = 0
    while pq:
        f, g, (y, x), path = heapq.heappop(pq)
        steps += 1
        if (y, x) == goal:
            return path + [(y, x)], steps, g
        if (y, x) in visited:
            continue
        visited.add((y, x))
        for ny, nx, dx, dy in valid_moves(grid, y, x, visited):
            move_cost = cost_fn(dx, dy)
            ng = g + move_cost
            h = heuristic((ny, nx), goal)
            heapq.heappush(pq, (ng + h, ng, (ny, nx), path + [(y, x)]))
    return [], steps, g


def print_result(nombre_algo, path, steps, costo=None):
            exito = "Sí" if len(path) > 0 else "No"
            costo_str = f"{costo}" if costo is not None else "-"
            print(f"{nombre_algo:<12} | Nodos explorados: {steps:<5} | Éxito: {exito:<3} | Costo: {costo_str}")
            if path:
                print(f"  Secuencia de estados: {path}\n")
                log.append(f"{nombre_algo} path: {path}\n")


ACTIONS = {0: "←", 1: "↓", 2: "→", 3: "↑"}

def path_to_arrows(path):
    """Convierte una lista de coordenadas [(y,x)] a flechas según movimiento."""
    if len(path) < 2:
        return ""
    arrows = []
    for (y1, x1), (y2, x2) in zip(path[:-1], path[1:]):
        dy, dx = y2 - y1, x2 - x1
        if dy == 0 and dx == -1:
            arrows.append(ACTIONS[0])  # ←
        elif dy == 1 and dx == 0:
            arrows.append(ACTIONS[1])  # ↓
        elif dy == 0 and dx == 1:
            arrows.append(ACTIONS[2])  # →
        elif dy == -1 and dx == 0:
            arrows.append(ACTIONS[3])  # ↑
        else:
            arrows.append("?")  # movimiento raro (no ortogonal)
    return "".join(arrows)


def pretty_desc(desc):
    """Convierte una grilla (lista de listas o bytes) a texto legible."""
    if isinstance(desc[0], bytes):  # entorno de gym
        rows = ["".join([c.decode() for c in row]) for row in desc]
    elif isinstance(desc[0], list):  # grilla generada como [['S','F','F'], ...]
        rows = ["".join(row) for row in desc]
    else:  # lista de strings
        rows = desc
    return "\n".join(rows)


# ============================================================
# ✅ MAIN: EJECUTAR ESCENARIOS
# ============================================================
if __name__ == "__main__":
   if __name__ == "__main__":
    random.seed(42)
    grid, start, goal = generate_grid(size=8, p_frozen=0.8)

    print("=" * 60)
    print(" ENTORNO GENERADO ".center(60, "="))
    print("=" * 60)
    print(pretty_desc(grid))
    print(f"\nInicio: {start}    |    Meta: {goal}")
    print("=" * 60)

    # --- carpeta de resultados ---
    base_dir = os.path.join(os.getcwd(), "tp3-algoritmos-busqueda", "resultados_escenarios")
    os.makedirs(base_dir, exist_ok=True)

    log_path = os.path.join(base_dir, "log_ejecucion.txt")
    log = []

    escenarios = {
        "Escenario 1 (Costo=1)": cost_function_1,
        "Escenario 2 (Izq/Der=1, Arr/Ab=10)": cost_function_2
    }

    all_results = []

    for nombre, cost_fn in escenarios.items():
        print("\n" + "-" * 60)
        print(nombre.center(60))
        print("-" * 60)

        log.append(f"\n=== {nombre} ===\n")
        scenario_results = []

        # BFS
        path, steps = bfs(grid, start, goal)
        scenario_results.append(("BFS", len(path) > 0, steps, len(path), None, path))
        print(f"BFS → nodos explorados: {steps}, camino encontrado: {len(path) > 0}")
        if path:
            print("Secuencia de estados (BFS):", path)
            print("Camino (flechas):", path_to_arrows(path))
            log.append(f"BFS path: {path}\n")

        # DFS
        path, steps = dfs(grid, start, goal)
        scenario_results.append(("DFS", len(path) > 0, steps, len(path), None, path))
        print(f"DFS → nodos explorados: {steps}, camino encontrado: {len(path) > 0}")
        if path:
            print("Secuencia de estados (DFS):", path)
            print("Camino (flechas):", path_to_arrows(path))
            log.append(f"DFS path: {path}\n")

        # DLS
        for L in [50, 75, 100]:
            path, steps = dls(grid, start, goal, limit=L)
            name = f"DLS(L={L})"
            scenario_results.append((name, len(path) > 0, steps, len(path), None, path))
            print(f"{name} → nodos: {steps}, éxito: {len(path) > 0}")
            if path:
                print(f"Secuencia de estados ({name}):", path)
                print("Camino (flechas):", path_to_arrows(path))
                log.append(f"{name} path: {path}\n")

        # UCS
        path, steps, cost = ucs(grid, start, goal, cost_fn)
        scenario_results.append(("UCS", len(path) > 0, steps, len(path), cost, path))
        print(f"UCS → nodos: {steps}, costo total: {cost}")
        if path:
            print("Secuencia de estados (UCS):", path)
            print("Camino (flechas):", path_to_arrows(path))
            print("Camino (flechas):", path_to_arrows(path))
            log.append(f"UCS path: {path}\n")

        # A*
        path, steps, cost = astar(grid, start, goal, cost_fn)
        scenario_results.append(("A*", len(path) > 0, steps, len(path), cost, path))
        print(f"A* → nodos: {steps}, costo total: {cost}")
        if path:
            print("Secuencia de estados (A*):", path)
            print("Camino (flechas):", path_to_arrows(path))
            log.append(f"A* path: {path}\n")

        # --- guardar CSV por escenario ---
        df = pd.DataFrame(
            scenario_results,
            columns=["algoritmo", "solucion_encontrada", "nodos_explorados", "long_camino", "costo_total", "path"]
        )
        filename = f"escenario{1 if 'Costo=1' in nombre else 2}_resultados.csv"
        df.to_csv(os.path.join(base_dir, filename), index=False)
        all_results.extend([(nombre, *row) for row in scenario_results])

    # --- resumen general ---
    df_all = pd.DataFrame(
        all_results,
        columns=["escenario", "algoritmo", "solucion_encontrada", "nodos_explorados", "long_camino", "costo_total", "path"]
    )
    df_all.to_csv(os.path.join(base_dir, "resumen_estadistico.csv"), index=False)

    # --- guardar entorno y caminos en texto ---
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("🔹 ENTORNO GENERADO 🔹\n")
        for row in grid:
            f.write(" ".join(row) + "\n")
        f.write(f"\nInicio: {start}\nMeta: {goal}\n\n")
        f.writelines(log)

    print(f"\n✅ Resultados guardados en: {base_dir}")
    print(f"📝 Log con caminos y entorno: {log_path}")