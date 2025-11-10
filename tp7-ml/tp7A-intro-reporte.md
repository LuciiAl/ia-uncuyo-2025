# TP7A – Introducción al Aprendizaje Estadístico (Machine Learning)

**Fuente:** James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021).  
*An Introduction to Statistical Learning: with Applications in R* (2nd ed., corrected printing 2023). Springer.  
Lectura: Capítulo 2 (hasta la página 42).

---

## 1. Métodos flexibles vs inflexibles

### a) n extremadamente grande, p pequeño  
**Mejor flexible.** Con muchos datos y pocos predictores, el método flexible puede aprender relaciones complejas sin sobreajustar, ya que el gran tamaño de muestra reduce la varianza. Un método inflexible sufriría de alto sesgo.

### b) p extremadamente grande, n pequeño  
**Mejor inflexible.** Con muchos predictores y pocas observaciones, un método flexible tiene alta varianza y riesgo de sobreajuste. Un método menos flexible reduce la varianza y generaliza mejor.

### c) Relación altamente no lineal  
**Mejor flexible.** Los métodos flexibles capturan relaciones no lineales y complejas entre predictores y variable objetivo, mientras que los rígidos fallan por alto sesgo.

### d) Varianza del error muy alta (σ² grande)  
**Mejor inflexible.** Cuando el ruido es alto, los métodos flexibles tienden a seguirlo, aumentando la varianza. Los métodos más simples son más estables y menos sensibles al ruido.

---

## 2. Tipos de problema, objetivo e identificación de n y p

### a) Salario de CEO según ganancias, empleados e industria  
- **Tipo:** Regresión (variable dependiente continua).  
- **Objetivo:** Inferencia (entender qué factores afectan el salario).  
- **n:** 500 (empresas).  
- **p:** 3 (ganancias, empleados, industria).

### b) Éxito o fracaso de producto nuevo  
- **Tipo:** Clasificación (éxito/fracaso).  
- **Objetivo:** Predicción (decidir si lanzar el producto).  
- **n:** 20 (productos).  
- **p:** 13 (precio, marketing, competencia, 10 variables adicionales).

### c) Predicción del % cambio USD/EUR según mercados  
- **Tipo:** Regresión (variable continua).  
- **Objetivo:** Predicción.  
- **n:** ≈52 (semanas de 2021).  
- **p:** 3 (mercados de EE. UU., Reino Unido y Alemania).

---

## 3. Ventajas y desventajas de un enfoque muy flexible

**Ventajas:**
- Bajo sesgo.
- Puede modelar relaciones complejas y no lineales.
- Mejora el rendimiento predictivo si hay suficiente información (n grande y ruido bajo).

**Desventajas:**
- Alta varianza (sobreajuste con n pequeño o p grande).
- Menor interpretabilidad.
- Mayor costo computacional.

**Preferir flexible cuando:** la relación es compleja/no lineal, hay muchos datos, el ruido es bajo y el interés es predecir.  
**Preferir inflexible cuando:** el tamaño de muestra es pequeño, hay mucho ruido o se busca interpretar.

---

## 4. Enfoques paramétricos vs no paramétricos

| Aspecto | Paramétrico | No paramétrico |
|----------|--------------|----------------|
| **Supuesto** | Fija una forma funcional (ej. lineal). | No asume forma funcional. |
| **Ejemplo** | Regresión lineal, logística. | k-NN, árboles, kernels, splines. |
| **Ventajas** | Simplicidad, interpretabilidad, bajo costo computacional. | Alta flexibilidad, puede modelar funciones complejas. |
| **Desventajas** | Alto sesgo si la forma está mal elegida. | Alta varianza, requiere n grande, menos interpretable. |
| **Preferir cuando...** | Se desea inferencia o interpretabilidad. | Se desea predicción y relaciones no lineales. |

---

## 5. K-Nearest Neighbors (k-NN)

### Dataset
| Obs | X1 | X2 | X3 | Y |
|-----|----|----|----|---|
| 1 | 0 | 3 | 0 | Rojo |
| 2 | 2 | 0 | 0 | Rojo |
| 3 | 0 | 1 | 3 | Rojo |
| 4 | 0 | 1 | 2 | Verde |
| 5 | -1 | 0 | 1 | Verde |
| 6 | 1 | 1 | 1 | Rojo |

Punto de prueba: **X = (0, 0, 0)**

### a) Distancias euclidianas

| Obs | X | Y | Distancia |
|-----|---|---|------------|
| 1 | (0,3,0) | Rojo | 3.000 |
| 2 | (2,0,0) | Rojo | 2.000 |
| 3 | (0,1,3) | Rojo | 3.162 |
| 4 | (0,1,2) | Verde | 2.236 |
| 5 | (-1,0,1) | Verde | 1.414 |
| 6 | (1,1,1) | Rojo | 1.732 |

### b) Predicción con K = 1  
Vecino más cercano: obs. 5 → **Verde.**

### c) Predicción con K = 3  
Tres más cercanos: obs. 5 (Verde), obs. 6 (Rojo), obs. 2 (Rojo).  
Mayoría: **Rojo (2 de 3).**

### d) Valor óptimo de K ante límite de Bayes no lineal  
Si el límite de decisión es altamente no lineal, el mejor **K** es **pequeño**, ya que produce una frontera más flexible y puede seguir curvas complejas. Un **K grande** genera un modelo más rígido (alta suavización, alto sesgo).

---

**Autor:** _[Tu nombre]_  
**Materia:** Inteligencia Artificial / Machine Learning  
**Año:** 2025 – UNCUYO
