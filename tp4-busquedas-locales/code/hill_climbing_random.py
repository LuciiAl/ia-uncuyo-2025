import random
import time

# ============================================================
# ✅ Generar estado inicial aleatorio
# ============================================================
def generar_estado_inicial(N):
    return [random.randrange(N) for _ in range(N)]

# ============================================================
# ✅ Calcular función objetivo H(e): número de pares de reinas que se atacan
# ============================================================
def calcular_H(tablero):
    H = 0
    N = len(tablero)
    for i in range(N):
        for j in range(i + 1, N):
            if tablero[i] == tablero[j]:
                H += 1
            elif abs(tablero[i] - tablero[j]) == abs(i - j):
                H += 1
    return H

# ============================================================
# ✅ Generar vecinos (mover una reina a otra fila en su columna)
# ============================================================
def generar_vecinos(tablero):
    vecinos = []
    N = len(tablero)
    for col in range(N):
        for fila in range(N):
            if fila != tablero[col]:
                nuevo = list(tablero)
                nuevo[col] = fila
                vecinos.append(nuevo)
    return vecinos

# ============================================================
# ✅ Hill Climbing simple (versión canónica AIMA)
# ============================================================
def hill_climbing(N, max_estados):
    estado = generar_estado_inicial(N)
    valor_actual = calcular_H(estado)
    evaluados = 1

    while evaluados < max_estados and valor_actual > 0:
        vecinos = generar_vecinos(estado)
        mejor_vecino = estado
        mejor_valor = valor_actual

        for v in vecinos:
            hv = calcular_H(v)
            evaluados += 1
            if hv < mejor_valor:
                mejor_vecino = v
                mejor_valor = hv

        if mejor_valor >= valor_actual:
            break  # óptimo local
        estado, valor_actual = mejor_vecino, mejor_valor

    return estado, evaluados, valor_actual


# ============================================================
# ✅ Versión con reinicios aleatorios
# ============================================================
def hill_climbing_random_restart(N, max_estados=10000, max_reinicios=50, seed=None):
    if seed is not None:
        random.seed(seed)

    mejor_estado_global = None
    mejor_H_global = float("inf")
    total_evaluados = 0

    for intento in range(max_reinicios):
        estado, evaluados, H = hill_climbing(N, max_estados)
        total_evaluados += evaluados

        if H < mejor_H_global:
            mejor_estado_global = estado
            mejor_H_global = H

        if H == 0:
            print(f"✅ Solución encontrada en reinicio #{intento + 1}")
            return mejor_estado_global, total_evaluados, mejor_H_global

    print("⚠️ Se alcanzó el máximo de reinicios sin encontrar solución perfecta.")
    return mejor_estado_global, total_evaluados, mejor_H_global


# ============================================================
# ✅ Imprimir tablero
# ============================================================
def imprimir_tablero(tablero):
    N = len(tablero)
    for fila in range(N):
        linea = ""
        for col in range(N):
            linea += "♛ " if tablero[col] == fila else ". "
        print(linea)
    print()


# ============================================================
# ✅ Ejecución principal
# ============================================================
def main(N, max_estados, seed):
    max_reinicios = 50
    solucion, evaluados, H = hill_climbing_random_restart(N, max_estados, max_reinicios, seed)
    return {
        "solution": solucion,
        "H": H,
        "states": evaluados
    }

if __name__ == "__main__":
    N = 8
    max_estados = 5000
    seed = 42
    result = main(N, max_estados, seed)
    print(result)
