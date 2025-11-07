import random
import math
import time

# ============================================================
# ✅ Generar estado inicial aleatorio
# ============================================================
def generar_estado_inicial(N):
    return [random.randrange(N) for _ in range(N)]

# ============================================================
# ✅ Calcular función objetivo H(e): pares de reinas que se atacan
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
# ✅ Generar un vecino aleatorio (un solo movimiento)
# ============================================================
def generar_vecino(tablero):
    N = len(tablero)
    nuevo = list(tablero)
    col = random.randrange(N)
    fila = random.randrange(N)
    while fila == tablero[col]:
        fila = random.randrange(N)
    nuevo[col] = fila
    return nuevo

# ============================================================
# ✅ Función de enfriamiento (Schedule)
# ============================================================
def schedule(t):
    # Versión clásica: T decrece exponencialmente
    T0 = 1.0       # temperatura inicial
    alpha = 0.003  # velocidad de enfriamiento
    return T0 * math.exp(-alpha * t)

# ============================================================
# ✅ Algoritmo Simulated Annealing (AIMA)
# ============================================================
def simulated_annealing(N, max_iter=100000, seed=None):
    if seed is not None:
        random.seed(seed)

    estado = generar_estado_inicial(N)
    valor_actual = calcular_H(estado)
    t = 1
    inicio = time.time()

    while t < max_iter and valor_actual > 0:
        T = schedule(t)
        if T <= 1e-6:
            break  # criterio de temperatura mínima

        vecino = generar_vecino(estado)
        valor_vecino = calcular_H(vecino)
        deltaE = valor_actual - valor_vecino

        # Si mejora, aceptar siempre; si empeora, aceptar con probabilidad e^(ΔE/T)
        if deltaE > 0 or random.random() < math.exp(deltaE / T):
            estado = vecino
            valor_actual = valor_vecino

        t += 1

    fin = time.time()
    return estado, valor_actual, t, fin - inicio

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
    solucion, H, iteraciones, tiempo = simulated_annealing(N, max_iter=max_estados, seed=seed)
    return {
        "solution": solucion,
        "H": H,
        "states": iteraciones
    }

if __name__ == "__main__":
    N = 8
    max_estados = 5000
    seed = 42
    result = main(N, max_estados, seed)
    print(result)
