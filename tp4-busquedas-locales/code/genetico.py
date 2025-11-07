import random
import time

# ============================================================
# ✅ Función objetivo: número de pares de reinas que se atacan
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
# ✅ Generar individuo aleatorio (solución candidata)
# ============================================================
def generar_individuo(N):
    return [random.randrange(N) for _ in range(N)]

# ============================================================
# ✅ Calcular fitness (mientras menor H, mejor)
# ============================================================
def fitness(individuo):
    # Convertimos H (pares que se atacan) en fitness positivo
    H = calcular_H(individuo)
    return 1 / (1 + H)  # entre 0 y 1, máximo cuando H = 0

# ============================================================
# ✅ Selección (torneo binario)
# ============================================================
def seleccion_torneo(poblacion, k=3):
    competidores = random.sample(poblacion, k)
    competidores.sort(key=lambda ind: fitness(ind), reverse=True)
    return competidores[0]

# ============================================================
# ✅ Cruce (1 punto)
# ============================================================
def cruce_un_punto(padre1, padre2):
    N = len(padre1)
    punto = random.randint(1, N - 2)
    hijo1 = padre1[:punto] + padre2[punto:]
    hijo2 = padre2[:punto] + padre1[punto:]
    return hijo1, hijo2

# ============================================================
# ✅ Mutación (cambiar aleatoriamente la posición de una reina)
# ============================================================
def mutacion(individuo, tasa_mutacion):
    N = len(individuo)
    nuevo = list(individuo)
    if random.random() < tasa_mutacion:
        col = random.randrange(N)
        nuevo[col] = random.randrange(N)
    return nuevo

# ============================================================
# ✅ Algoritmo Genético
# ============================================================
def algoritmo_genetico(N, tam_poblacion=100, tasa_mutacion=0.1, max_generaciones=1000, seed=None):
    if seed is not None:
        random.seed(seed)

    # Inicializar población aleatoria
    poblacion = [generar_individuo(N) for _ in range(tam_poblacion)]
    inicio = time.time()

    for generacion in range(max_generaciones):
        # Evaluar fitness
        poblacion.sort(key=lambda ind: fitness(ind), reverse=True)
        mejor = poblacion[0]
        H_mejor = calcular_H(mejor)

        # Criterio de terminación: solución perfecta
        if H_mejor == 0:
            fin = time.time()
            return mejor, generacion, fin - inicio, H_mejor

        # Nueva población
        nueva_poblacion = poblacion[:2]  # elitismo: los 2 mejores sobreviven

        # Reproducción hasta completar población
        while len(nueva_poblacion) < tam_poblacion:
            padre1 = seleccion_torneo(poblacion)
            padre2 = seleccion_torneo(poblacion)
            hijo1, hijo2 = cruce_un_punto(padre1, padre2)
            hijo1 = mutacion(hijo1, tasa_mutacion)
            hijo2 = mutacion(hijo2, tasa_mutacion)
            nueva_poblacion.extend([hijo1, hijo2])

        poblacion = nueva_poblacion

    fin = time.time()
    mejor = min(poblacion, key=lambda ind: calcular_H(ind))
    return mejor, max_generaciones, fin - inicio, calcular_H(mejor)

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
    mejor, generaciones, tiempo, H = algoritmo_genetico(N, max_generaciones=max_estados, seed=seed)
    return {
        "solution": mejor,
        "H": H,
        "states": generaciones
    }

if __name__ == "__main__":
    N = 8
    max_estados = 5000
    seed = 42
    result = main(N, max_estados, seed)
    print(result)

