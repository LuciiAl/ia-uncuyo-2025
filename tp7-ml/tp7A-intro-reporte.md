# TP 7A - Introducción al Aprendizaje Estadístico (Statistical Learning)

**Universidad Nacional de Cuyo**  
**Facultad de Ingeniería 

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

d) La varianza de los términos de error, \( \sigma^2 = \mathrm{Var}(\epsilon) \), es extremadamente alta.

**→ Mejor desempeño esperado: método inflexible.**

Cuando hay mucho **ruido** en los datos, un método flexible puede intentar ajustar ese ruido, aumentando su **varianza** y empeorando su capacidad predictiva.  
Un modelo inflexible suaviza más la señal y resulta más **estable** frente al ruido.

En ISL se ilustra este punto con el gráfico de “Trade-off Bias–Variance”, donde los métodos flexibles son más sensibles a la varianza del error.


## 2. Explique si cada escenario representa un problema de clasificación o de regresión, e indique si el interés principal es inferir o predecir. Especifique **n** (cantidad de observaciones) y **p** (cantidad de predictores) en cada caso.

**a)** Se recopila un conjunto de datos sobre las 500 empresas más importantes de Estados Unidos. Para cada una de las empresas se registran las ganancias, el número de empleados, la industria y el salario del director ejecutivo. Se tiene interés en comprender qué factores afectan el salario de los directores ejecutivos.

**b)** Se está considerando lanzar un nuevo producto y se desea saber si será un éxito o un fracaso. Se recolectan datos de 20 productos similares que fueron lanzados previamente. Para cada producto se ha registrado si fue un éxito o un fracaso, el precio cobrado por el producto, el presupuesto de marketing, el precio de la competencia, y otras diez variables.

**c)** Se tiene interés en predecir el % de cambio en el tipo de cambio USD/Euro en relación a los cambios semanales en los mercados de valores mundiales. Para eso se recolectan datos semanalmente durante todo el 2021. Para cada semana se registran el % de cambio de USD/Euro, el % de cambio en el mercado estadounidense, el % de cambio en el mercado británico, y el % de cambio en el mercado alemán.

---

## 3. ¿Cuáles son las ventajas y desventajas de un enfoque muy flexible (versus uno menos flexible) para la regresión o clasificación? ¿Bajo qué circunstancias podría preferirse un enfoque más flexible a uno menos flexible? ¿Cuándo podría preferirse un enfoque menos flexible?

---

## 4. Describa las diferencias entre un enfoque paramétrico y uno no paramétrico. ¿Cuáles son las ventajas y desventajas de un enfoque paramétrico para regresión o clasificación, a diferencia de un enfoque no paramétrico?

---

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

**a)** Calcule la distancia Euclidiana entre cada observación y el punto de prueba \( X = (0, 0, 0) \).  
**b)** ¿Cuál es la predicción con \( K = 1 \)? Justifique.  
**c)** ¿Cuál es la predicción con \( K = 3 \)? Justifique.  
**d)** Si el límite de decisión de Bayes en este problema es altamente no lineal, ¿se espera que el mejor valor para \( K \) sea grande o pequeño? ¿Por qué?
