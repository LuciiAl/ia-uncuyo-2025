import random
import time

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
# ✅ Generar tablero aleatorio
# ============================================================
def generar_tablero_aleatorio(N):
    # Cada índice = columna, valor = fila
    return [random.randrange(N) for _ in range(N)]

# ============================================================
# ✅ Algoritmo Aleatorio (Random Search)
# ============================================================
def algoritmo_aleatorio(N, max_intentos=100000, seed=None):
    """
    Intenta generar tableros aleatorios hasta encontrar una solución válida (H = 0)
    o hasta alcanzar el máximo número de intentos permitido.
    """
    if seed is not None:
        random.seed(seed)

    inicio = time.time()
    intentos = 0
    mejor_tablero = None
    mejor_H = float("inf")

    while intentos < max_intentos:
        tablero = generar_tablero_aleatorio(N)
        H = calcular_H(tablero)
        intentos += 1

        if H < mejor_H:
            mejor_tablero = tablero
            mejor_H = H

        if H == 0:
            # Solución perfecta encontrada
            fin = time.time()
            return tablero, intentos, fin - inicio, H

    fin = time.time()
    # Si no encuentra solución perfecta, devuelve la mejor encontrada
    return mejor_tablero, intentos, fin - inicio, mejor_H

# ============================================================
# ✅ Imprimir tablero
# ============================================================
def imprimir_tablero(tablero):
    N = len(tablero)
    for fila in range(N):
        print(" ".join("♛" if tablero[col] == fila else "." for col in range(N)))
    print()

# ============================================================
# ✅ Ejecución principal
# ============================================================
def main(N, max_estados, seed):
    solucion, intentos, tiempo, H = algoritmo_aleatorio(N, max_intentos=max_estados, seed=seed)
    return {
        "solution": solucion,
        "H": H,
        "states": intentos
    }

if __name__ == "__main__":
    N = 8
    max_estados = 5000
    seed = 42
    result = main(N, max_estados, seed)
    print(result)
