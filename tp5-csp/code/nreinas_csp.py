import itertools
import random


class CSP:
    def __init__(self, variables, dominios, restricciones):
        self.variables = variables
        self.dominios = dominios  # dict: {var: [valores posibles]}
        self.restricciones = restricciones  # función que evalúa (Xi, x, Xj, y)
        self.contadores = {"asignaciones": 0}

    def consistente(self, variable, valor, asignacion):
        """Verifica si asignar 'valor' a 'variable' es consistente con las restricciones."""
        for var2, val2 in asignacion.items():
            if not self.restricciones(variable, valor, var2, val2):
                return False
        return True


# ============================================================
#  Formulación CSP del problema de N-Reinas
# ============================================================

def crear_csp_nreinas(N):
    variables = list(range(N))  # columnas 0..N-1
    dominios = {col: list(range(N)) for col in variables}  # filas 0..N-1

    def restricciones(Xi, vi, Xj, vj):
        # Dos reinas se atacan si están en la misma fila o diagonal
        if Xi == Xj:
            return True  # no comparar consigo misma
        return vi != vj and abs(vi - vj) != abs(Xi - Xj)

    return CSP(variables, dominios, restricciones)


# ============================================================
#  A) Backtracking search 
# ============================================================

def backtracking_search(csp):
    """Versión clásica de backtracking con chequeo de consistencia."""
    def backtrack(asignacion):
        if len(asignacion) == len(csp.variables):
            return asignacion
        var = seleccionar_variable(asignacion, csp)
        for valor in csp.dominios[var]:
            csp.contadores["asignaciones"] += 1
            if csp.consistente(var, valor, asignacion):
                asignacion[var] = valor
                resultado = backtrack(asignacion)
                if resultado:
                    return resultado
                del asignacion[var]
        return None

    def seleccionar_variable(asignacion, csp):
        # Selección simple: primera variable no asignada
        for v in csp.variables:
            if v not in asignacion:
                return v

    return backtrack({})


# ============================================================
#  B) Forward Checking 
# ============================================================

def forward_checking(csp):
    """Backtracking con forward checking para podar dominios."""
    dominios_actuales = {v: list(vals) for v, vals in csp.dominios.items()}

    def backtrack(asignacion):
        if len(asignacion) == len(csp.variables):
            return asignacion
        var = seleccionar_variable(asignacion, csp)
        for valor in dominios_actuales[var][:]:
            csp.contadores["asignaciones"] += 1
            if csp.consistente(var, valor, asignacion):
                asignacion[var] = valor
                dominios_guardados = {v: list(vals) for v, vals in dominios_actuales.items()}

                # Forward checking: eliminar valores inconsistentes en vecinos
                if aplicar_forward_check(var, valor, asignacion):
                    resultado = backtrack(asignacion)
                    if resultado:
                        return resultado

                # Restaurar dominios
                dominios_actuales.update(dominios_guardados)
                del asignacion[var]
        return None

    def aplicar_forward_check(var, valor, asignacion):
        """Elimina valores inconsistentes de los dominios restantes."""
        for vecino in csp.variables:
            if vecino != var and vecino not in asignacion:
                for v in dominios_actuales[vecino][:]:
                    if not csp.restricciones(vecino, v, var, valor):
                        dominios_actuales[vecino].remove(v)
                if not dominios_actuales[vecino]:
                    return False  # dominio vacío → inconsistencia
        return True

    def seleccionar_variable(asignacion, csp):
        for v in csp.variables:
            if v not in asignacion:
                return v

    return backtrack({})


# ============================================================
#  Utilidades
# ============================================================

def imprimir_tablero(solucion):
    if solucion is None:
        print("No se encontró solución.")
        return
    N = len(solucion)
    for fila in range(N):
        linea = ""
        for col in range(N):
            if solucion[col] == fila:
                linea += "♛ "
            else:
                linea += ". "
        print(linea)
    print()


# ============================================================
#  Ejecución principal
# ============================================================

if __name__ == "__main__":
    N = 8
    print(f"\n=== N-REINAS con BACKTRACKING ===")
    csp1 = crear_csp_nreinas(N)
    sol1 = backtracking_search(csp1)
    imprimir_tablero(sol1)
    print(f"Asignaciones: {csp1.contadores['asignaciones']}\n")

    print(f"\n=== N-REINAS con FORWARD CHECKING ===")
    csp2 = crear_csp_nreinas(N)
    sol2 = forward_checking(csp2)
    imprimir_tablero(sol2)
    print(f"Asignaciones: {csp2.contadores['asignaciones']}\n")
