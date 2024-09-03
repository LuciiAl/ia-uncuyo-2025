# Comparación de Performance entre un Agente Reflexivo Simple y un Agente Random
## Introducción
Se realizará una simulación de dos tipos de agentes inteligentes en un entorno particular con distintos tamaños y suciedad. 
Se verá el desempeño de los mismos y se hará una comparación de los resultados de los mismos.

## Marco Teórico
### Funcionamiento del entorno
El entorno es una cuadrícula donde cada celda puede tener suciedad o estar limpia. 
La suciedad se genera de forma aleatoria según un porcentaje indicado y únicamente al inicio de la simulación.
El tamaño de la cuadrícula va incrementando en cada simulación.
El Agente (ya sea el reflexivo simple o el random) comienzan en una posición aleatoria de la cuadrícula. 

### Agentes
Existen dos tipos de agentes:
**Agente reflexivo simple** : Toma decisiones según su estado actual. Tiene conocimiento de su ubicación y si la misma está sucia o no. 
**Agente aleatorio** : Toma decisiones aleatorias sin ningún análisis de su entorno.

Ambos Agentes pueden realizar las mismas acciones: 
Moverse arriba, abajo, izquierda, derecha, limpiar y no hacer nada.
Son premiados con un punto por cada celda sucia aspirada.
Tienen una cantidad finita de movimientos (1000).

## Diseño Experimental 
Se crea un entorno y se posiciona el Agente en una celda aleatoria al igual que la suciedad comenzando con un porcentaje indicado.
Se deja al agente seleccionar hasta 1000 veces que es lo que hará. 
Por cada celda sucia aspirada genera un punto de performance. No hay penalizaciones. 
Se repite este procedimiento 10 veces. 

El porcentaje de suciedad inicialmente es de 0.1 y luego se va aumentando a 0.2, 0.4 y 0.8 repitiendo 10 veces en cada vez. 
Esta simulación se realiza igual para los siguientes tamaños: 2x2, 4x4, 8x8, 16x16, 32x32 , 64x64 y 128x128. 

## Análisis y Discusión de resultados

Se realizaron dos simulaciones, una para cada agente, y sus resultados fueron guardados en un archivo csv. 
Luego, se separaron los resultados por categoria "dirt-rate" y se hizo un promedio de las 10 iteraciones por cada agente. 
Por último se presentó en un gráfico para comparar los resultados de performance. 

![image](https://github.com/user-attachments/assets/75f0ef33-9894-4e1f-83bc-ae65dac77031)
![image](https://github.com/user-attachments/assets/78a0813f-be5b-42db-8b8c-6c5b2a8bd2af)
![image](https://github.com/user-attachments/assets/61265b1f-c658-4b5e-a7cb-fbea859f9464)
![image](https://github.com/user-attachments/assets/4955fb1e-9628-4936-9e07-8cb5dda97510)

Como se observa en los gráficos, la diferencia en performance entre los dos agentes es bastante notoria mientras mas grande se hace el entorno. A medida que hay mayor porcentaje de basura la diferencia se hace mucho mas notoria.
Estos resultados tienen sentido ya que el agente random no toma en cuenta nada para actuar sin embargo el reflexivo simple comprende un poco más su entorno y puede actuar en consecuencia. 

## Conclusiones 

Luego de ver la comparación de performance de los Agentes Aleatorio y Reflexivo Simple podemos ver que el Agente Reflexivo Simple tiene un mejor rendimiento respecto al Aleatorio.
Mientras mas grande y más sucio el entorno, la diferencia incrementa aún más mostrando que en tamaños pequeños pueden ser similares pero luego ya no.




