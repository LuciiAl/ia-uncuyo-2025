# TP 7A - Introducción al Aprendizaje Estadístico (Statistical Learning)

**Universidad Nacional de Cuyo**  
Facultad de Ingeniería 

## 1. En cada uno de los siguientes ejercicios, indique si en general se espera que un método de aprendizaje de máquinas flexible se comporte mejor o peor que uno inflexible. Justifique su respuesta.

a) El tamaño de la muestra **n** es extremadamente grande, y el número de predictores **p** es pequeño.  
**→ Mejor desempeño esperado: método flexible.**

Cuando se dispone de **muchas observaciones** y pocos predictores, el modelo flexible puede capturar patrones complejos sin sobreajustar, ya que la gran cantidad de datos reduce la **varianza**.  
En estos casos, el sesgo bajo de los métodos flexibles se aprovecha y la varianza no crece significativamente.

En ISL (cap. 2), los autores explican que “con suficiente cantidad de datos, un método más flexible puede superar al lineal porque el costo en varianza se ve compensado por la reducción en sesgo”.
b) El número de predictores **p** es extremadamente grande, y el número de observaciones **n** es pequeño.
 **→ Mejor desempeño esperado: método inflexible.**

Cuando *p ≫ n*, los métodos flexibles tienden a **sobreajustar** fácilmente, ya que pueden encontrar patrones espurios en los pocos datos disponibles.  
Un modelo inflexible (de baja complejidad) impone mayor estructura, controlando la varianza y evitando el sobreajuste.

En ISL se señala que los métodos flexibles “requieren muchos más datos para estimar una superficie de respuesta precisa en espacios de alta dimensión”.

c) La relación entre los predictores y la variable dependiente es altamente no lineal.  
**→ Mejor desempeño esperado: método flexible.**

Los métodos flexibles pueden aproximar relaciones **no lineales** o interacciones complejas entre variables, mientras que los inflexibles (como un modelo lineal) suponen una forma rígida y pueden tener alto **sesgo**.

ISL enfatiza que los métodos flexibles, al permitir relaciones no lineales, reducen el sesgo cuando la función verdadera \( f(X) \) no es lineal.

d) La varianza de los términos de error, σ² = Var(ε), es extremadamente alta.

**→ Mejor desempeño esperado: método inflexible.**

Cuando hay mucho **ruido** en los datos, un método flexible puede intentar ajustar ese ruido, aumentando su **varianza** y empeorando su capacidad predictiva.  
Un modelo inflexible suaviza más la señal y resulta más **estable** frente al ruido.

En ISL se ilustra este punto con el gráfico de “Trade-off Bias–Variance”, donde los métodos flexibles son más sensibles a la varianza del error.


## 2. Explique si cada escenario representa un problema de clasificación o de regresión, e indique si el interés principal es inferir o predecir. Especifique **n** (cantidad de observaciones) y **p** (cantidad de predictores) en cada caso.

**a)** Se recopila un conjunto de datos sobre las 500 empresas más importantes de Estados Unidos. Para cada una de las empresas se registran las ganancias, el número de empleados, la industria y el salario del director ejecutivo. Se tiene interés en comprender qué factores afectan el salario de los directores ejecutivos.

**Tipo de problema:**  
**Regresión**, ya que la variable dependiente (salario) es **continua**.

**Objetivo principal:**  
**Inferencia**, porque el interés radica en **comprender la relación** entre las variables explicativas y el salario, más que en realizar predicciones para nuevos casos.

**Dimensiones:**  
- **n = 500** (empresas observadas).  
- **p = 3** (ganancias, número de empleados, industria —aunque la variable “industria” puede codificarse en varias variables dummy si hay múltiples categorías).

Se distingue explícitamente entre “problemas de inferencia”, donde se busca entender cómo los predictores afectan la respuesta, y “problemas de predicción”, donde el interés es estimar con precisión \( Y \) para nuevos valores de \( X \). Este caso es del primer tipo.


**b)** Se está considerando lanzar un nuevo producto y se desea saber si será un éxito o un fracaso. Se recolectan datos de 20 productos similares que fueron lanzados previamente. Para cada producto se ha registrado si fue un éxito o un fracaso, el precio cobrado por el producto, el presupuesto de marketing, el precio de la competencia, y otras diez variables.

**Tipo de problema:**  
**Clasificación**, dado que la variable respuesta es **categórica (éxito o fracaso)**.

**Objetivo principal:**  
**Predicción**, porque el interés es **anticipar el resultado** (éxito o fracaso) de un nuevo producto.

**Dimensiones:**  
- **n = 20** (productos históricos).  
- **p = 13** (precio, presupuesto de marketing, precio de la competencia + 10 variables adicionales).

Los autores destacan que en clasificación el objetivo suele ser predictivo, evaluando el desempeño mediante la tasa de error de clasificación, más que la interpretación de los coeficientes.


**c)** Se tiene interés en predecir el % de cambio en el tipo de cambio USD/Euro en relación a los cambios semanales en los mercados de valores mundiales. Para eso se recolectan datos semanalmente durante todo el 2021. Para cada semana se registran el % de cambio de USD/Euro, el % de cambio en el mercado estadounidense, el % de cambio en el mercado británico, y el % de cambio en el mercado alemán.

**Tipo de problema:**  
**Regresión**, ya que la variable dependiente (porcentaje de cambio) es **numérica y continua**.

**Objetivo principal:**  
**Predicción**, ya que el interés es **estimar valores futuros** del tipo de cambio a partir de las variaciones en los mercados.

**Dimensiones:**  
- **n ≈ 52** (semanas del año 2021).  
- **p = 3** (mercados: estadounidense, británico, alemán).

Los problemas de predicción cuantitativa se abordan con métodos de regresión orientados a minimizar el error de predicción, no necesariamente a interpretar parámetros.


## 3. ¿Cuáles son las ventajas y desventajas de un enfoque muy flexible (versus uno menos flexible) para la regresión o clasificación? ¿Bajo qué circunstancias podría preferirse un enfoque más flexible a uno menos flexible? ¿Cuándo podría preferirse un enfoque menos flexible?

Ventajas de un enfoque muy flexible

- **Bajo sesgo:** el modelo puede aproximar relaciones muy complejas entre \( X \) y \( Y \).  
- **Capacidad para modelar no linealidades:** puede capturar interacciones o dependencias que un modelo lineal no detectaría.  
- **Mayor precisión predictiva** cuando la relación verdadera es altamente no lineal y el conjunto de datos es grande.  
- **Adecuado para tareas donde el objetivo es predecir**, no interpretar.

Ejemplo típico del libro: el método *k*-NN con \( k \) pequeño puede adaptarse bien a límites de decisión no lineales si hay suficientes observaciones.

Desventajas de un enfoque muy flexible

- **Alta varianza:** el modelo es más sensible a fluctuaciones aleatorias o ruido en los datos.  
- **Mayor riesgo de sobreajuste (overfitting):** se ajusta al ruido del conjunto de entrenamiento, empeorando el desempeño en datos nuevos.  
- **Menor interpretabilidad:** es más difícil explicar cómo los predictores afectan la variable objetivo.  
- **Mayor costo computacional:** suelen requerir más procesamiento y ajuste de hiperparámetros.

ISL resalta que, cuando σ² (ruido) es alto o n es pequeño, los métodos flexibles tienden a sobreajustar, mientras que los rígidos se comportan mejor.

Cuándo preferir cada tipo de enfoque

### Preferir un **enfoque más flexible** cuando:
- La relación entre los predictores y la respuesta es **no lineal o compleja**.  
- El tamaño de muestra \( n \) es **grande**, lo que permite controlar la varianza.  
- El **objetivo principal es la predicción** más que la inferencia.  
- El ruido en los datos es bajo (σ² pequeño).

### Preferir un **enfoque menos flexible** cuando:
- Se desea **interpretar** las relaciones entre variables (no solo predecir).  
- El conjunto de datos es **pequeño** o tiene pocos ejemplos por predictor.  
- La relación verdadera es aproximadamente **lineal o simple**.  
- Hay **alto nivel de ruido** en las observaciones.

## 4. Describa las diferencias entre un enfoque paramétrico y uno no paramétrico. ¿Cuáles son las ventajas y desventajas de un enfoque paramétrico para regresión o clasificación, a diferencia de un enfoque no paramétrico?

Un modelo paramétrico asume que la relación entre la variable de respuesta Y y los predictores X₁, X₂, …, Xₚ puede representarse mediante una función con un número finito de parámetros, por ejemplo:

Y ≈ f(X) = β₀ + β₁X₁ + … + βₚXₚ

El aprendizaje consiste en estimar los parámetros β₀, β₁, …, βₚ a partir de los datos.

### Ventajas de los métodos paramétricos

- Son **simples e interpretables**, permiten entender cómo cada predictor afecta la respuesta.  
- Requieren **menos datos** para estimar la relación subyacente.  
- Tienen **baja varianza**, ya que restringen el espacio de funciones posibles.  
- Son **computacionalmente eficientes**.

### Desventajas de los métodos paramétricos

- Si la forma funcional asumida no refleja bien la realidad, el modelo tiene **alto sesgo**.  
- Son poco adecuados cuando la relación entre \( X \) y \( Y \) es **altamente no lineal** o compleja.  
- No pueden adaptarse a estructuras de datos con dependencias o interacciones no especificadas de antemano.

Ejemplos típicos: regresión lineal, regresión logística, análisis discriminante lineal (LDA).


## Enfoques no paramétricos

Los **métodos no paramétricos** no imponen una forma funcional específica.  
En lugar de asumir una estructura fija para \( f(X) \), permiten que los datos determinen la forma de la función de manera más libre.

Y ≈ f(X), donde f es aprendida directamente de los datos.

### Ventajas de los métodos no paramétricos

- **Alta flexibilidad:** pueden adaptarse a relaciones no lineales o complejas entre las variables.  
- **Bajo sesgo:** al no imponer una forma funcional, pueden aproximar con mayor precisión la relación verdadera.  
- **No requieren especificar un modelo a priori.**

### Desventajas de los métodos no paramétricos

- **Alta varianza:** son más sensibles al ruido y al tamaño de la muestra.  
- Requieren **grandes cantidades de datos** para obtener estimaciones estables.  
- Pueden sufrir la **maldición de la dimensionalidad** cuando el número de predictores es alto.  
- Menor interpretabilidad y mayor costo computacional.

Ejemplos típicos: k-Nearest Neighbors (k-NN), árboles de decisión, random forests, splines, modelos kernel.


## Conclusión

Los **enfoques paramétricos** son más adecuados cuando se busca **interpretar** la relación entre las variables y cuando se tiene un **modelo teórico claro** o pocos datos.  
Por el contrario, los **métodos no paramétricos** son preferibles cuando el objetivo principal es **predecir con precisión** y cuando la relación subyacente es **no lineal o compleja**.

En términos del equilibrio **sesgo-varianza**, los modelos paramétricos suelen presentar **mayor sesgo y menor varianza**, mientras que los no paramétricos presentan **menor sesgo y mayor varianza**.


## 5. Conjunto de entrenamiento (6 observaciones, 3 predictores, Y cualitativa)

| Obs. | X1  | X2 | X3 | Y     |
|:----:|:---:|:--:|:--:|:-----:|
| 1    | 0   | 3  | 0  | Rojo  |
| 2    | 2   | 0  | 0  | Rojo  |
| 3    | 0   | 1  | 3  | Rojo  |
| 4    | 0   | 1  | 2  | Verde |
| 5    | -1  | 0  | 1  | Verde |
| 6    | 1   | 1  | 1  | Rojo  |

Se desea predecir **Y** para el punto de prueba **X1 = X2 = X3 = 0** usando **K vecinos más cercanos (K-NN)**.

**a)** Calcule la distancia Euclidiana entre cada observación y el punto de prueba X = (0, 0, 0).
La distancia euclidiana entre dos puntos Xᵢ = (xᵢ₁, xᵢ₂, xᵢ₃) y X = (0, 0, 0) se calcula como:

d(Xᵢ, X) = √((xᵢ₁)² + (xᵢ₂)² + (xᵢ₃)²)

Aplicando esta fórmula:

| Obs. | \( X_1 \) | \( X_2 \) | \( X_3 \) | \( Y \) | \( d(X_i, X) \) |
|:----:|:----------:|:----------:|:----------:|:------:|:----------------:|
| 1 | 0 | 3 | 0 | Rojo  | 3.000 |
| 2 | 2 | 0 | 0 | Rojo  | 2.000 |
| 3 | 0 | 1 | 3 | Rojo  | 3.162 |
| 4 | 0 | 1 | 2 | Verde | 2.236 |
| 5 | -1 | 0 | 1 | Verde | 1.414 |
| 6 | 1 | 1 | 1 | Rojo  | 1.732 |

**b)** ¿Cuál es la predicción con \( K = 1 \)? Justifique.  
El algoritmo **K-NN con \( K = 1 \)** clasifica el punto de prueba según la clase del **único vecino más cercano**.

- Vecino más cercano: observación **#5** (distancia 1.414).  
- Clase del vecino: **Verde**.

**Predicción:**  
Ŷ(K=1) = Verde

Con \(K=3\), K-NN estima la clase mayoritaria en el vecindario inmediato del punto de prueba. Este vecindario es lo bastante pequeño como para incluir a los tres puntos citados; la mayoría corresponde a Rojo, por lo que esa es la asignación coherente con la regla de decisión de K-NN.

**c)** ¿Cuál es la predicción con \( K = 3 \)? Justifique.  

Para \( K = 3 \), se consideran los tres vecinos más cercanos:

| Vecino | Obs. | Distancia | Clase |
|:-------:|:----:|:----------:|:------|
| 1 | 5 | 1.414 | Verde |
| 2 | 6 | 1.732 | Rojo |
| 3 | 2 | 2.000 | Rojo |

Votación por mayoría:

- **Rojo:** 2 votos  
- **Verde:** 1 voto  

**Predicción:**  
Ŷ(K=3) = Rojo

Con \(K=3\), K-NN estima la clase mayoritaria en el vecindario inmediato del punto de prueba. Este vecindario es lo bastante pequeño como para incluir a los tres puntos citados; la mayoría corresponde a Rojo, por lo que esa es la asignación coherente con la regla de decisión de K-NN.

**d)** Si el límite de decisión de Bayes en este problema es altamente no lineal, ¿se espera que el mejor valor para \( K \) sea grande o pequeño? ¿Por qué?

El parámetro \( K \) controla la **flexibilidad** del clasificador:

- Un \( K \) **pequeño** produce un modelo **muy flexible**, con fronteras de decisión **irregulares y no lineales**.  
- Un \( K \) **grande** genera un modelo **más rígido**, con fronteras **más suaves** y alto **sesgo**.

Por lo tanto, **si el límite de decisión de Bayes es altamente no lineal**, se espera que el mejor valor de \( K \) sea **pequeño**, ya que permitirá capturar la complejidad de la frontera entre clases.

**Por qué:**
- **Suavizado vs. detalle local.** K-NN aproxima la probabilidad condicional \(P(Y=c\mid X=x)\) con la **frecuencia de clase** dentro del vecindario de \(x\). A mayor \(K\), el vecindario se expande e incorpora puntos más lejanos, mezclando regiones de distintas clases y **suavizando** la frontera. Si la frontera real es altamente sinuosa/no lineal, un vecindario grande “promedia” a través de curvas y pliegues, introduciendo **alto sesgo** y borrando detalle fino.
- **Captura de curvaturas finas.** Un \(K\) pequeño mantiene el vecindario **local** y permite que la clasificación siga **cambios rápidos** de la frontera, adaptándose a ondulaciones y recodos. Esto reduce el sesgo y mejora el ajuste en zonas donde la separación entre clases cambia bruscamente.
- **Intuición geométrica.** Con frontera complicada, puntos muy cercanos al límite pueden quedar del lado opuesto si se amplía demasiado el vecindario. Un \(K\) grande integrará muchos vecinos de ambas clases, empujando la predicción hacia la mayoría global de la zona amplia en lugar de la **estructura local** alrededor de \(x\).
- **Compromiso sesgo–varianza.** Bajar \(K\) incrementa la varianza (más sensibilidad al ruido) pero **reduce el sesgo**. Cuando la frontera es compleja, el costo de sesgo de usar \(K\) grande es mayor que el beneficio de menor varianza, por lo que \(K\) pequeño resulta preferible.
