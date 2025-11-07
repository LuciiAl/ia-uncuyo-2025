import random
import time

# ============================================================
# ✅ Generar estado inicial aleatorio
# ============================================================
def generar_estado_inicial(N):
    # Cada índice representa una columna, y el valor es la fila de la reina
    return [random.randrange(N) for _ in range(N)]

# ============================================================
# ✅ Calcular función objetivo H(e): número de pares de reinas que se atacan
# ============================================================
def calcular_H(tablero):
    H = 0
    N = len(tablero)
    for i in range(N):
        for j in range(i + 1, N):
            # Misma fila
            if tablero[i] == tablero[j]:
                H += 1
            # Misma diagonal
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
# ✅ Hill Climbing (versión canónica de AIMA)
# ============================================================
def hill_climbing(N, max_estados=10000, seed=None):
    if seed is not None:
        random.seed(seed)

    estado = generar_estado_inicial(N)
    valor_actual = calcular_H(estado)
    estados_evaluados = 1  # incluye el inicial

    while estados_evaluados < max_estados and valor_actual > 0:
        vecinos = generar_vecinos(estado)
        mejor_vecino = estado
        mejor_valor = valor_actual

        # Buscar el mejor vecino
        for v in vecinos:
            hv = calcular_H(v)
            estados_evaluados += 1
            if hv < mejor_valor:
                mejor_vecino = v
                mejor_valor = hv

        # Si no hay mejora, detener
        if mejor_valor >= valor_actual:
            break

        # Moverse al mejor vecino
        estado = mejor_vecino
        valor_actual = mejor_valor

    return estado, estados_evaluados, valor_actual

# ============================================================
# ✅ Imprimir tablero de forma visual
# ============================================================
def imprimir_tablero(tablero):
    N = len(tablero)
    for fila in range(N):
        linea = ""
        for col in range(N):
            if tablero[col] == fila:
                linea += "♛ "
            else:
                linea += ". "
        print(linea)
    print()




# ============================================================
# ✅ Ejecución principal
# ============================================================
def main(N, max_estados, seed):
    solucion, evaluados, H = hill_climbing(N, max_estados=max_estados, seed=seed)
    return {
        "solution": solucion,
        "H": H,
        "states": evaluados
    }

if __name__ == "__main__":
    # Ejemplo manual
    N = 8
    max_estados = 5000
    seed = 42
    result = main(N, max_estados, seed)
    print(result)



