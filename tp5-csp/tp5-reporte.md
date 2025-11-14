## **1. Formulación CSP detallada para el Sudoku**

El Sudoku estándar es un tablero de **9×9** dividido en **9 subcuadrículas de 3×3**. El objetivo es asignar números del **1 al 9** de manera que se cumplan todas las restricciones.

### **Variables**

Una variable por cada celda del tablero:

```
X_{i,j}   para   i,j ∈ {1,...,9}
```

### **Dominios**

* Si la celda está vacía:

```
D(X_{i,j}) = {1,2,3,4,5,6,7,8,9}
```

* Si la celda está precompletada:

```
D(X_{i,j}) = {numero fijo}
```

### **Restricciones**

#### **Restricción de fila**

En cada fila los valores deben ser distintos:

```
X_{i,1}, X_{i,2}, ..., X_{i,9}  deben ser todos diferentes
```

Para cada par de variables en la fila:

```
X_{i,j} ≠ X_{i,k}     para todo j ≠ k
```

#### **Restricción de columna**

```
X_{1,j}, X_{2,j}, ..., X_{9,j}  deben ser todos distintos
```

#### **Restricción de subcuadrícula (3×3)**

Para cada subcuadrícula:

```
X_{r,c} ≠ X_{r',c'}   para todas las celdas del mismo bloque
```

Los bloques se definen mediante:

```
floor(i/3) = floor(i'/3)
floor(j/3) = floor(j'/3)
```

Un Sudoku puede verse como un CSP con:

* **81 variables**
* **Dominios entre 1 y 9**
* **Restricciones de desigualdad**

  * 27 grupos (9 filas, 9 columnas, 9 bloques)
  * Más de 1000 restricciones binarias individuales


## **Uso del algoritmo AC-3 para mostrar inconsistencia con la asignación parcial WA = red, V = blue**

### **Problema**

Colorear el mapa de Australia con los colores:

```
{red, green, blue}
```

Asignación parcial:

```
WA = red
V  = blue
```

Queremos ver si esto genera inconsistencia usando **AC-3**.

### **Regiones y Vecindades (AIMA)**

* WA ↔ NT, SA
* NT ↔ WA, SA, Q
* SA ↔ WA, NT, Q, NSW, V
* Q ↔ NT, SA, NSW
* NSW ↔ Q, SA, V
* V ↔ SA, NSW
* T no conecta

### **Arcos iniciales**

```
(WA,NT), (WA,SA), (NT,SA), (NT,Q), (SA,Q),
(SA,NSW), (SA,V), (Q,NSW), (NSW,V)
```

### **Paso a paso del AC-3**

#### 1) Procesar (SA, V)

```
V = blue → SA no puede usar blue
```

#### 2) Procesar (NSW, V)

```
NSW tampoco puede usar blue
```

#### 3) Propagación hacia Q y SA

```
NSW ≠ blue  →  Q ≠ blue
SA ≠ blue   →  Q ≠ blue
```

Q queda sin blue en su dominio.

#### 4) Propagación hacia NT

```
Q ≠ blue  →  NT ≠ blue
```

#### 5) Propagación hacia WA

```
WA = red
NT ≠ red y ≠ blue → NT = green
```

#### 6) Volver a SA

```
NT = green → SA ≠ green
SA ya tenía eliminado blue → Dom(SA) = {red}
```

#### 7) Conflicto con WA

```
SA = red
WA = red
```

Esto viola la restricción `WA ≠ SA`.


### **Conclusión con AC-3**

**AC-3 detecta inconsistencia**, ya que la propagación obliga:

```
SA = red
```

y ya estaba asignado:

```
WA = red
```

Como son vecinos, la asignación es inconsistente.


## **Complejidad en el peor caso de AC-3 cuando el CSP tiene estructura de árbol**

Complejidad general de AC-3:

```
O(e * d^3)
```

donde:

* `e` = número de arcos
* `d` = tamaño del dominio

Si el grafo de restricciones es un **árbol**:

* No hay ciclos
* Cada arco se revisa pocas veces
* Hay `n - 1` arcos

La complejidad se vuelve:

```
O(n * d^2)
```

### **Explicación**

* Cada arco se revisa una vez "hacia arriba" y una vez "hacia abajo"
* Revisar consistencia entre dos nodos requiere hasta `d^2` combinaciones
* En un árbol hay `n - 1` arcos

```
Complejidad final = O(n * d^2)
```

# Experimentos CSP (N-Reinas)

## Descripción general

En este experimento se evaluaron dos algoritmos de resolución del problema de las N-Reinas formulado como un **Problema de Satisfacción de Restricciones (CSP)**:

- **Backtracking clásico**: búsqueda en profundidad con verificación de consistencia.
- **Forward Checking**: versión mejorada que realiza poda de dominios luego de cada asignación parcial.

Cada algoritmo fue ejecutado **30 veces con semillas distintas** para los tamaños de tablero **N = 4, 8 y 10**.  
Se registraron el **tiempo de ejecución**, la **cantidad de nodos explorados** y si se **encontró una solución válida**.

## Resultados globales

| Algoritmo | N | Éxito (%) | Tiempo medio (s) | Desv. tiempo | Nodos medios | Desv. nodos |
|------------|---|------------|------------------|--------------|---------------|-------------|
| backtracking | 4 | 100.0 | 0.0 | 0.0 | 26.0 | 0.0 |
| backtracking | 8 | 100.0 | 0.00093 | 0.00071 | 876.0 | 0.0 |
| backtracking | 10 | 100.0 | 0.00092 | 0.00057 | 975.0 | 0.0 |
| forward | 4 | 100.0 | 3e-05 | 0.00019 | 8.0 | 0.0 |
| forward | 8 | 100.0 | 0.00048 | 0.00057 | 88.0 | 0.0 |
| forward | 10 | 100.0 | 0.00081 | 0.00051 | 83.0 | 0.0 |


## Gráficos

A continuación se muestran los **boxplots** de las distribuciones de tiempos de ejecución y de nodos explorados:

### boxplot_nodes_N10.png
![boxplot_nodes_N10.png](images/boxplot_nodes_N10.png)

### boxplot_nodes_N4.png
![boxplot_nodes_N4.png](images/boxplot_nodes_N4.png)

### boxplot_nodes_N8.png
![boxplot_nodes_N8.png](images/boxplot_nodes_N8.png)

### boxplot_time_N10.png
![boxplot_time_N10.png](images/boxplot_time_N10.png)

### boxplot_time_N4.png
![boxplot_time_N4.png](images/boxplot_time_N4.png)

### boxplot_time_N8.png
![boxplot_time_N8.png](images/boxplot_time_N8.png)


## Conclusión

- El algoritmo **Forward Checking** muestra una clara reducción en la cantidad promedio de nodos explorados y en el tiempo medio de ejecución.
- Ambos algoritmos alcanzan el 100% de éxito para tableros pequeños (N ≤ 10), aunque la diferencia de rendimiento se acentúa a medida que aumenta N.
- El **Backtracking clásico** presenta mayor variabilidad temporal y un crecimiento más pronunciado del número de nodos, evidenciando su naturaleza exponencial.
- Por tanto, **Forward Checking** resulta más adecuado para resolver CSPs como el de las N-Reinas, ya que mejora la eficiencia sin sacrificar exactitud.

## Comparación General – Búsquedas Locales (TP4) vs CSP (TP5)

Esta comparación integra los resultados del **TP4 (búsquedas locales: HC, HCR, SA, GA, Random)** y el **TP5 (CSP: Backtracking, Forward Checking)**.

Se busca analizar diferencias en:
- **Eficiencia temporal**
- **Nodos explorados**
- **Tasa de éxito**


### Muestra parcial de datos (TP4)
| algorithm_name | env_n | size | best_solution | H | states | time |
| --- | --- | --- | --- | --- | --- | --- |
| random | 0 | 4 | [2, 0, 3, 1] | 0 | 68 | 0.0 |
| HC | 0 | 4 | [1, 3, 0, 2] | 0 | 13 | 0.00106 |
| HCR | 0 | 4 | [1, 3, 0, 2] | 0 | 13 | 0.0 |
| SA | 0 | 4 | [1, 3, 0, 2] | 0 | 55 | 0.0 |
| GA | 0 | 4 | [2, 0, 3, 1] | 0 | 0 | 0.0 |
| random | 1 | 4 | [2, 0, 3, 1] | 0 | 21 | 0.0 |
| HC | 1 | 4 | [1, 3, 2, 0] | 1 | 25 | 0.0 |
| HCR | 1 | 4 | [2, 0, 3, 1] | 0 | 62 | 0.0 |
| SA | 1 | 4 | [2, 0, 3, 1] | 0 | 28 | 0.0 |
| GA | 1 | 4 | [2, 0, 3, 1] | 0 | 0 | 0.001068 |


### Gráficos comparativos

## Comparativa TP4 vs TP5

![compare_tp4_tp5_nodes.png](images/compare_tp4_tp5_nodes.png)

![compare_tp4_tp5_nodes_mean.png](images/compare_tp4_tp5_nodes_mean.png)

![compare_tp4_tp5_time.png](images/compare_tp4_tp5_time.png)

![compare_tp4_tp5_time_mean.png](images/compare_tp4_tp5_time_mean.png)


### Análisis comparativo

- Los métodos **CSP (Backtracking, Forward Checking)** garantizan **soluciones exactas**, pero con tiempos de ejecución más altos en N grandes.
- Los algoritmos de **búsqueda local (SA, HCR)** ofrecen soluciones rápidas y aproximadas, alcanzando buenos resultados en tiempo, aunque sin garantía de optimalidad.
- **Simulated Annealing (SA)** se posiciona como el mejor entre los métodos locales: rápido, robusto y consistente.
- **Forward Checking (CSP)** domina en exactitud y control de nodos, aunque a un costo computacional mayor en escalas grandes.


### Conclusión global

| Criterio | Local Search (TP4) | CSP (TP5) |
|-----------|-------------------|------------|
| Exactitud | Parcial (dependiente de heurística) | Completa (garantiza solución) |
| Escalabilidad | Alta para N moderado | Limitada por crecimiento exponencial |
| Robustez | Alta (en SA y GA) | Alta (en FC) |
| Tiempo | Bajo–medio | Medio–alto |
| Mejor método | **Simulated Annealing (SA)** | **Forward Checking (FC)** |


## 3. Conclusión Final

- **Forward Checking (CSP)** sobresale por su precisión y control, siendo ideal para validación o demostración de soluciones exactas.
- **Simulated Annealing (Local Search)** se destaca por su velocidad y adaptabilidad, siendo más adecuado para problemas grandes o con restricciones suaves.
- Ambos enfoques son complementarios: uno garantiza optimalidad, el otro eficiencia práctica.
