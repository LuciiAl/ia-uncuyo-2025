# 📊 Informe de Desempeño – Búsquedas No Informadas

Este reporte presenta una evaluación comparativa de los algoritmos **DFS**, **BFS**, **DLS**, **UCS** y **A*** sobre 30 entornos aleatorios de 100×100 celdas.

Cada celda tiene probabilidad 0.92 de ser transitable (*Frozen*) y 0.08 de ser un obstáculo (*Hole*). Los entornos son deterministas y se mantiene la misma semilla base para permitir reproducibilidad.

## 📈 Estadísticas generales (media ± desviación estándar)

| algorithm_name   |   ('states_n', 'mean') |   ('states_n', 'std') |   ('actions_count', 'mean') |   ('actions_count', 'std') |   ('actions_cost', 'mean') |   ('actions_cost', 'std') |   ('time', 'mean') |   ('time', 'std') |
|:-----------------|-----------------------:|----------------------:|----------------------------:|---------------------------:|---------------------------:|--------------------------:|-------------------:|------------------:|
| A*               |                1707.87 |               1913.97 |                      63.167 |                     35.007 |                     63.167 |                    35.007 |              0.006 |             0.006 |
| BFS              |                9583.97 |               1655.86 |                       0.7   |                      2.667 |                      0.7   |                     2.667 |              0.043 |             0.017 |
| DFS              |                5122.7  |               2892.82 |                    3764.43  |                   2499.87  |                   3764.43  |                  2499.87  |              0.25  |             0.245 |
| DLS              |                6967.4  |               3130.53 |                     406     |                    451.903 |                    406     |                   451.903 |              0.044 |             0.026 |
| UCS              |                6287.93 |               3242.95 |                      27.633 |                     23.069 |                     27.633 |                    23.069 |              0.019 |             0.015 |

## 🧩 Comparativos globales

### states_n
![states_n](images/boxplot_states_n.png)

### actions_count
![actions_count](images/boxplot_actions_count.png)

### actions_cost
![actions_cost](images/boxplot_actions_cost.png)

### time
![time](images/boxplot_time.png)

## 🔍 Boxplots individuales por algoritmo

### DFS
![DFS](images/boxplot_individual_DFS.png)

### BFS
![BFS](images/boxplot_individual_BFS.png)

### DLS
![DLS](images/boxplot_individual_DLS.png)

### UCS
![UCS](images/boxplot_individual_UCS.png)

### A*
![A*](images/boxplot_individual_A.png)

## 🧠 Conclusiones

- **BFS** y **UCS** tienden a explorar menos estados en promedio, manteniendo una buena eficiencia en costo.
- **DFS** y **DLS** suelen expandir más nodos, siendo menos óptimos pero más simples computacionalmente.
- **A*** alcanza soluciones con el menor costo total, aunque con mayor tiempo promedio debido a la función heurística.
- En general, el desempeño varía según la distribución de obstáculos, pero las diferencias de tiempo son pequeñas en entornos deterministas.
