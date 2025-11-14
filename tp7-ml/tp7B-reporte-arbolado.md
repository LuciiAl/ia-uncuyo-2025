# **i) Preprocesamiento realizado**

En esta etapa se aplicaron varias transformaciones para preparar los datos antes del entrenamiento:


### **1. Eliminación de variables irrelevantes**

Se eliminaron las columnas:

* `id`
* `nombre_seccion`
* `ultima_modificacion`

ya que no aportaban información útil al modelo o eran identificadores sin valor predictivo.


### **2. Transformación de variables categóricas ordinales**

Se mapearon rangos textuales a valores numéricos representativos:

* `altura` → {1.5, 3, 6, 9}
* `diametro_tronco` → {10, 30, 50, 70}

Esto facilita el procesamiento sin perder su orden natural.


### **3. Codificación manual de variables categóricas nominales**

Para las variables:

* `especie`
* `seccion`

se aplicó un **encoding manual**, ya que no se utilizó sklearn.

El proceso fue:

1. Obtener las categorías presentes en train
2. Asignar un entero a cada clase
3. Codificar test con ese mismo mapeo
4. Categorías nuevas → se asignaron como `-1`


### **4. Creación de nuevas características**

Se añadieron features derivadas que mejoran la capacidad predictiva del modelo:

* `circ_altura_ratio = circ_tronco_cm / altura`
* `diam_circ_ratio = diametro_tronco / circ_tronco_cm`


### **5. Normalización**

No se aplicó normalización, ya que los árboles de XGBoost no la requieren.


# **ii) Resultados sobre el conjunto de validación**

Dado que no se utilizó sklearn, se implementó un **K-Fold manual estratificado**, asegurando la misma proporción de clases en cada fold.

Con un modelo **XGBoost nativo** (`xgb.train`) y `scale_pos_weight` correctamente ajustado para el desbalance, se obtuvieron:

* **AUC promedio (validación manual):** entre **0.70 y 0.74**
* **Validación estable y con buena sensibilidad a la clase positiva**


# **iii) Resultados obtenidos en Kaggle**

El archivo final generado por el modelo obtuvo:

# **Score Kaggle: 0.71537**

Este valor se encuentra dentro de lo esperado para modelos basados en Gradient Boosting sin tuning agresivo ni pipeline avanzado, especialmente considerando:

* dataset desbalanceado
* modelo sin sklearn
* ingeniería de features moderada
* hiperparámetros conservadores


# **iv) Descripción del algoritmo propuesto**

El algoritmo utilizado fue **XGBoost** usando:

* `xgb.DMatrix` para los datos
* `xgb.train` para el entrenamiento


### **Motivación del uso de XGBoost**

XGBoost es un algoritmo basado en árboles de decisión, pero mucho más robusto que un árbol simple, ya que utiliza:

* Gradient Boosting
* Shrinkage (learning rate)
* Subsampling
* Regularización
* Manejo nativo de desbalance


### **Hiperparámetros utilizados**

* `objective = "binary:logistic"`
* `eta = 0.03` *(learning rate)*
* `max_depth = 5`
* `subsample = 0.9`
* `colsample_bytree = 0.9`

El parámetro clave para el desbalance fue:

```
scale_pos_weight = (clase_negativa / clase_positiva)
```

Esto obliga al modelo a prestar atención a la clase minoritaria, que de otro modo sería ignorada.

Se utilizaron **800 árboles** (`num_boost_round = 800`) para mejorar la capacidad de aprendizaje sin perder generalización.


### **Por qué funciona bien este enfoque**

* Maneja desbalance en forma nativa
* Permite usar K-Fold manual
* Es más fuerte que un árbol tradicional
* Aprovecha bien las features creadas


# **Conclusión**

El modelo final basado en **XGBoost nativo** logró un desempeño sólido tanto en validación interna como en Kaggle. El preprocesamiento —incluyendo la codificación manual, la transformación de variables ordinales y la creación de nuevas características— permitió mejorar la representación del problema, mientras que el ajuste del parámetro `scale_pos_weight` fue clave para manejar el fuerte desbalance de clases. Con estos elementos, el modelo alcanzó un **score de 0.71537 en Kaggle**, un resultado consistente y adecuado para el tipo de datos y el enfoque utilizado.

