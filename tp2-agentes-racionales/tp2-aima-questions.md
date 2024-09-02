## 2.10 Consider a modified version of the vacuum environment in Exercise 2.8, in which the agent is penalized one point for each movement. 
#### a. Can a simple reflex agent be perfectly rational for this environment? Explain. 

No, no puede ya que no tiene la posibilidad de elegir la mejor acción, simplemente elige una sin importar si es la mejor o la peor

#### b. What about a reflex agent with state? Design such an agent. 

Tampoco podría ya que no sabe sobre todo el mundo, solo sobre el que tiene guardado en su información. Sería mejor el desempeño pero no 100% racional. 
Para el diseño se podrían agregar reglas que se fijen cual es la celda sucia mas cercana y moverse hacia ella, o si no hay mas celdas sucias no hacer nada. 

#### c. How do your answers to a and b change if the agent’s percepts give it the clean/dirty status of every square in the environment?

En los dos casos podrían moverse hacia donde está sucio directamente lo cual si los haría racionales, ya que no desperdiciarían movimientos a lugares a los que ya fueron o que no están sucios. Lo único que no sería es perfecto ya que no pueden saber si el camino que están haciendo es el mejor o que tendría menos penalizaciones. 

## 2.11 Consider a modified version of the vacuum environment in Exercise 2.8, in which the geography of the environment—its extent, boundaries, and obstacles—is unknown, as is the initial dirt configuration. (The agent can go Up and Down as well as Left and Right.) 

#### a. Can a simple reflex agent be perfectly rational for this environment? Explain. 

No puede serlo, por la misma razón que antes, no tiene memoria ni conocimiento del entorno por lo que no va a saber que hacer y simplemente irá probando acciones hasta que el entorno se lo permita.

#### b. Can a simple reflex agent with a randomized agent function outperform a simple reflex agent? Design such an agent and measure its performance on several environments.

No, quizás en entornos pequeños y sin castigos pueden ser similares, pero en entornos grandes ya no. 

#### c. Can you design an environment in which your randomized agent will perform poorly? Show your results. 

En comparación con un agente no aleatorizado tiene una performance peor en casi cualquier entorno, se puede ver en el informe la comparación.

#### d. Can a reflex agent with state outperform a simple reflex agent? Design such an agent and measure its performance on several environments. Can you design a rational agent of this type?

Si puede ser mejor la performance ya que al guardar la información del entorno es más fácil elegir una acción a continuación. 
Para el diseño se pueden agregar condiciones de no volver a cuadrículas ya visitadas, o en mismas direcciones por las cuales viajó. 
