### **a) Jugar al CS (Counter Strike o cualquier otro 3D Shooter)**

**PEAS:**

* **P (Performance):** Precisión de disparo, número de enemigos eliminados, muertes, asistencias, tiempo de supervivencia, cumplimiento del objetivo del mapa.
* **E (Environment):** Mapa tridimensional, jugadores aliados y enemigos, obstáculos, armas, objetos del entorno, clima y terreno virtual.
* **A (Actuators):** Movimiento del jugador (teclado y mouse), disparos, saltos, uso de armas y equipamiento, comunicación.
* **S (Sensors):** Cámara (visión en primera persona), sonidos del entorno (pasos, disparos), indicadores de vida y munición.

**Tipo de agente:**
→ **Basado en modelo y objetivos.**
Debe construir un modelo del entorno dinámico (posición de enemigos, cobertura, munición, etc.) y actuar para cumplir objetivos (eliminar enemigos, plantar/desactivar bomba, sobrevivir).

### **b) Explorar los océanos**

**PEAS:**

* **P:** Superficie y profundidad explorada, precisión de las mediciones, seguridad de la tripulación, cantidad de datos recolectados.
* **E:** Océano, corrientes, fauna, flora, presión, temperatura, visibilidad, otros exploradores o embarcaciones.
* **A:** Motores, hélices, brazos mecánicos, cámaras, sensores de profundidad o temperatura, luces.
* **S:** Cámaras, sonar, radar, sensores químicos, de presión, temperatura, GPS.

**Tipo de agente:**
→ **Basado en modelo y en objetivos.**
Debe mantener un modelo interno del entorno (mapa submarino, obstáculos, corrientes) y orientarse hacia objetivos (explorar zonas nuevas, recolectar muestras, evitar colisiones).

### **c) Comprar y vender tokens crypto**

**PEAS:**

* **P:** Rentabilidad obtenida, tiempo de respuesta a las oportunidades de mercado, minimización de pérdidas.
* **E:** Mercado (blockchain), precios, volumen de operaciones, liquidez, comisiones, bots y traders humanos.
* **A:** Compra, venta, cancelación de órdenes, cambio de moneda, conexión a exchanges.
* **S:** Lectura de precios, históricos, tendencias, indicadores técnicos, señales externas.

**Tipo de agente:**
→ **Basado en utilidad o que aprende.**
Busca maximizar utilidad (ganancia esperada) y puede aprender patrones del mercado mediante machine learning para predecir movimientos.

### **d) Practicar tenis contra una pared**

**PEAS:**

* **P:** Precisión, número de golpes consecutivos, control, fuerza y dirección de la pelota.
* **E:** Pared, pelota, raqueta, superficie del piso, viento, iluminación.
* **A:** Movimiento corporal, golpes, desplazamientos, fuerza aplicada.
* **S:** Vista, tacto, sonido (rebote de la pelota).

**Tipo de agente:**
→ **Reflejo basado en modelo (si entrena conscientemente)** o **reflejo simple (si solo reacciona).**
El jugador puede ajustar su respuesta según el rebote (modelo físico del entorno), aprendiendo a anticipar trayectorias.

### **e) Realizar un salto de altura**

**PEAS:**

* **P:** Altura alcanzada, precisión del salto, aterrizaje seguro.
* **E:** Superficie, barra, condiciones ambientales, equipamiento.
* **A:** Movimiento corporal (piernas, brazos, impulso).
* **S:** Vista, equilibrio, sensores internos (propiocepción).

**Tipo de agente:**
→ **Basado en objetivos o que aprende.**
Tiene el objetivo de superar una altura y puede ajustar su técnica mediante aprendizaje y retroalimentación (ensayo y error).

### **f) Pujar por un artículo en una subasta**

**PEAS:**

* **P:** Obtener el artículo al menor precio posible, maximizar beneficio (relación valor/precio).
* **E:** Subasta, pujas de otros agentes, reglas, tiempos límite, presentador.
* **A:** Realizar ofertas, retirarse, analizar comportamiento de otros.
* **S:** Observación de las pujas, precio actual, tiempo restante, reacciones de otros.

**Tipo de agente:**
→ **Basado en utilidad.**
El agente evalúa la utilidad esperada (valor del artículo vs costo) y decide si continuar o retirarse; puede incluir aprendizaje si analiza estrategias pasadas.

