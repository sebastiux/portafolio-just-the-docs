---
layout: default
title: Características técnicas y necesidades
nav_order: 2
---

# Características técnicas y necesidades

Esta página identifica **qué debe cubrir el rover** para completar la misión del proyecto de la clase de Integración Mecatrónica Otoño 2026. Parte de una lista de **13 necesidades** y las traduce en **70 métricas objetivo** agrupadas en ocho bloques, cada una con un valor marginal (mínimo aceptable) y un valor ideal.

Fuente: tabla de especificaciones objetivo del equipo, versión preliminar para revisión con asesores.

> Operación **100 % teledirigida** (Raspberry Pi + control Xbox + enlace Wi‑Fi). Los sensores se especifican por su valor para el operador, no por desempeño autónomo.

---

## 1) Necesidades que debe cubrir el proyecto

Cada necesidad tiene una importancia de 1 (baja) a 5 (crítica). La columna **Nec.** de las tablas de métricas se refiere a estos números.


| # | Necesidad | Imp. (1-5) |
|--:|:----------|:----------:|
| 1 | El rover se controla remotamente sin pérdida de enlace ni retardo perceptible | 5 |
| 2 | El operador ve el entorno del rover en tiempo real desde la laptop | 5 |
| 3 | El rover cabe en el volumen permitido y es transportable por el equipo | 3 |
| 4 | El rover atraviesa valles, surcos y pendientes de ±30° sin volcar ni atascarse | 5 |
| 5 | El rover sujeta rocas de tamaño y color variables sin dañarlas ni soltarlas | 5 |
| 6 | El rover almacena a bordo todas las muestras y las deposita dentro del contenedor | 5 |
| 7 | El brazo acciona interruptores y botones en un rango vertical de 0 a 1 m | 4 |
| 8 | El rover completa la misión dentro de 10 min (+5 min de mantenimiento guiado) | 5 |
| 9 | El operador registra y georreferencia rocas y relieves durante la misión | 4 |
| 10 | El sistema cumple restricciones normativas (peso, envolvente, comunicación declarada) | 4 |
| 11 | El rover opera toda la jornada de competencia sin quedarse sin energía | 3 |
| 12 | El sistema es seguro y no interfiere con otros equipos | 3 |
| 13 | El rover se repara y reinicia rápido entre rondas | 2 |


---

## 2) Cómo leer las tablas de métricas

- **Imp.**: importancia de la métrica, de 1 a 5.
- **Valor marginal**: mínimo aceptable para competir.
- **Valor ideal**: meta de diseño del equipo.
- **Origen**:
  - **Reglamento**: dato tomado directamente de las reglas de la competencia.
  - **Derivada**: calculada a partir de otra métrica o del reglamento.
  - **Definida por el equipo**: decisión de diseño propia.
  - **Hipótesis (H)**: supuesto de ingeniería que requiere validación por prototipo.

---

## 3) Métricas objetivo por bloque


### A. Teleoperación y comunicaciones

El rover se opera **100 % a distancia**, así que la calidad del enlace es la primera necesidad del proyecto (necesidades 1 y 2). La estación (laptop + control Xbox) debe recibir el video de la cámara con una latencia extremo a extremo **menor a 250 ms** (ideal &lt;120 ms), a **≥15 fps** y **≥1280×720 px**, sobre un enlace Wi‑Fi con alcance operativo **≥15 m** y pérdida de paquetes **&lt;2 %**. Los comandos deben llegar del control al actuador en **&lt;150 ms** y, si el enlace se pierde, el rover debe detenerse de forma segura en **&lt;500 ms**. La estación debe mostrar **≥3 canales de sensor** al mismo tiempo y la misión debe poder operarse con **≤2 personas**.

| # | Métrica | Nec. | Imp. | Unidades | Valor marginal | Valor ideal | Origen |
|--:|:--------|:----:|:----:|:---------|:--------------:|:-----------:|:-------|
| 1 | Latencia extremo a extremo del video (glass-to-glass) | 1, 2 | 5 | ms | <250 | <120 | Hipótesis (H) |
| 2 | Cuadros por segundo del video en la estación | 2 | 4 | fps | ≥15 | ≥30 | Hipótesis (H) |
| 3 | Resolución del video transmitido | 2 | 3 | px | ≥1280×720 | ≥1920×1080 | Definida por el equipo |
| 4 | Alcance operativo del enlace inalámbrico | 1 | 5 | m | ≥15 | ≥25 | Derivada |
| 5 | Latencia de comando (control Xbox → actuador) | 1 | 5 | ms | <150 | <60 | Hipótesis (H) |
| 6 | Tiempo de paro seguro ante pérdida de enlace | 1, 12 | 4 | ms | <500 | <200 | Derivada |
| 7 | Pérdida de paquetes en el enlace | 1 | 3 | % | <2 | <0.5 | Hipótesis (H) |
| 8 | Banda de operación declarada | 10 | 3 | Lista | 2.4 GHz | 5 GHz | Reglamento |
| 9 | Canales de sensor visibles simultáneamente en la estación | 2, 9 | 3 | canales | ≥3 | ≥5 | Derivada |
| 10 | Operadores requeridos para la misión | 1 | 2 | personas | ≤2 | 1 | Definida por el equipo |


### B. Chasis y movilidad

El chasis debe respetar las restricciones normativas (necesidades 3 y 10) y, al mismo tiempo, superar el terreno de la pista (necesidad 4): cabe en una envolvente de **≤100×100×100 cm** sin desplegar, pesa **&lt;55 kg** (objetivo del equipo: &lt;12 kg), sube pendientes de **≥30°** con carga completa, mantiene un ángulo de vuelco estático **≥40°**, libra obstáculos y surcos de **≥8 cm**, conserva un despeje al suelo **≥5 cm** y avanza a **≥0.30 m/s** en terreno emulado.

| # | Métrica | Nec. | Imp. | Unidades | Valor marginal | Valor ideal | Origen |
|--:|:--------|:----:|:----:|:---------|:--------------:|:-----------:|:-------|
| 11 | Volumen envolvente sin desplegar | 3 | 3 | cm | ≤100×100×100 | ≤60×60×60 | Reglamento |
| 12 | Masa total del rover | 3, 10 | 4 | kg | <55 | <12 | Reglamento |
| 13 | Pendiente máxima superable con carga completa | 4 | 5 | grados | ≥30 | ≥40 | Reglamento |
| 14 | Ángulo de vuelco estático | 4 | 5 | grados | ≥40 | ≥55 | Hipótesis (H) |
| 15 | Altura de obstáculo / surco superable | 4 | 4 | cm | ≥8 | ≥12 | Derivada |
| 16 | Despeje al suelo | 4 | 3 | cm | ≥5 | ≥8 | Hipótesis (H) |
| 17 | Velocidad de traslado en terreno emulado | 4, 8 | 4 | m/s | ≥0.30 | ≥0.60 | Hipótesis (H) |


### C. Actuadores de tracción

La tracción se dimensiona para un rover de 12.5 kg con rueda de 15 cm y 30 % de margen (necesidad 4). Se requieren **≥4 ruedas motrices independientes** (ideal 6) con par nominal **≥2.2 N·m** por rueda y par de bloqueo **≥6.5 N·m** por motor, motorreductores de **38 a 60 rpm** con carga, ruedas de **≥13 cm** de diámetro, banda de rodadura **≥40 mm** y grousers **≥6 mm** para lograr un coeficiente de tracción **≥0.65** en arena. El reductor debe ser reversible, cada rueda debe llevar encoder (**≥200 pulsos/rev**) y los drivers deben soportar **≥5 A continuos** y **≥15 A pico** por canal. El límite real no es el par sino la adherencia: en pendiente de 30° se necesita μ ≥ 0.577.

| # | Métrica | Nec. | Imp. | Unidades | Valor marginal | Valor ideal | Origen |
|--:|:--------|:----:|:----:|:---------|:--------------:|:-----------:|:-------|
| 18 | Par nominal por rueda motriz (config. 4WD) | 4 | 5 | N·m | ≥2.2 | ≥3.5 | Derivada |
| 19 | Par de bloqueo (stall) por motor | 4 | 5 | N·m | ≥6.5 | ≥10 | Derivada |
| 20 | Velocidad de salida del motorreductor con carga | 4, 17 | 4 | rpm | 38-60 | 60-80 | Derivada |
| 21 | Ruedas motrices independientes | 4 | 4 | unidades | ≥4 | 6 | Definida por el equipo |
| 22 | Diámetro de rueda | 4 | 4 | cm | ≥13 | ≥16 | Derivada |
| 23 | Ancho de banda de rodadura | 4 | 5 | mm | ≥40 | ≥60 | Hipótesis (H) |
| 24 | Altura de grouser / taco | 4 | 5 | mm | ≥6 | ≥10 | Hipótesis (H) |
| 25 | Coeficiente de tracción efectivo en arena | 4 | 5 | - | ≥0.65 | ≥0.85 | Hipótesis (H) |
| 26 | Reductor no autobloqueante (reversible) | 4 | 3 | Sí/No | Sí | Sí | Definida por el equipo |
| 27 | Resolución de encoder por rueda | 9 | 3 | pulsos/rev salida | ≥200 | ≥1000 | Hipótesis (H) |
| 28 | Corriente continua por canal del driver | 12 | 4 | A | ≥5 | ≥10 | Derivada |
| 29 | Corriente pico soportada por el driver | 12 | 4 | A | ≥15 | ≥30 | Derivada |


### D. Brazo robótico

El brazo acciona interruptores y botones en un rango vertical de **0 a 100 cm** (necesidad 7). Debe tener **≥4 grados de libertad** sin contar la pinza, alcance horizontal **≥25 cm** y pares de bloqueo de **≥6.0 N·m** en hombro, **≥3.0 N·m** en codo, **≥1.2 N·m** en muñeca y **≥2.0 N·m** en la base, con rangos angulares **≥180°**. En la punta debe ejercer **≥20 N** a 0.20 m, con repetibilidad **≤10 mm**, resolución de comando **≤1°**, juego mecánico **≤2°** y velocidad **≥60 °/s**. La corriente pico total del brazo no debe exceder **12 A**. Los pares se calcularon con eslabones de 0.25 y 0.20 kg y 0.40 kg de carga; en aluminio suben cerca de 40 %.

| # | Métrica | Nec. | Imp. | Unidades | Valor marginal | Valor ideal | Origen |
|--:|:--------|:----:|:----:|:---------|:--------------:|:-----------:|:-------|
| 30 | Grados de libertad del brazo (sin contar pinza) | 7 | 3 | GDL | ≥4 | ≥5 | Definida por el equipo |
| 31 | Alcance vertical del efector desde el suelo | 7 | 4 | cm | 0-100 | 0-115 | Reglamento |
| 32 | Alcance horizontal útil del brazo | 7 | 4 | cm | ≥25 | ≥40 | Hipótesis (H) |
| 33 | Par de bloqueo, articulación de hombro | 7 | 5 | N·m | ≥6.0 | ≥12.0 | Derivada |
| 34 | Par de bloqueo, articulación de codo | 7 | 5 | N·m | ≥3.0 | ≥6.0 | Derivada |
| 35 | Par de bloqueo, muñeca (pitch) | 7 | 4 | N·m | ≥1.2 | ≥2.5 | Derivada |
| 36 | Par de bloqueo, base (yaw) | 7 | 4 | N·m | ≥2.0 | ≥4.0 | Derivada |
| 37 | Rango angular de hombro y codo | 7 | 4 | grados | ≥180 | ≥270 | Definida por el equipo |
| 38 | Rango angular de la base | 7 | 4 | grados | ≥180 | 360 | Definida por el equipo |
| 39 | Fuerza de empuje en el efector a L = 0.20 m | 7 | 4 | N | ≥20 | ≥40 | Derivada |
| 40 | Repetibilidad de posicionamiento del efector | 7 | 4 | mm | ≤10 | ≤3 | Hipótesis (H) |
| 41 | Resolución de comando por articulación | 7 | 4 | grados | ≤1.0 | ≤0.3 | Hipótesis (H) |
| 42 | Juego mecánico (backlash) por articulación | 7 | 4 | grados | ≤2.0 | ≤0.5 | Hipótesis (H) |
| 43 | Retención de posición sin energía | 7 | 3 | Sí/No | No | Sí | Definida por el equipo |
| 44 | Velocidad angular de articulación sin carga | 7, 8 | 3 | °/s | ≥60 | ≥120 | Hipótesis (H) |
| 45 | Corriente pico total de actuadores del brazo | 12 | 4 | A | ≤12 | ≤8 | Hipótesis (H) |


### E. Pinza y muestras

La pinza sujeta rocas de tamaño y color variables sin dañarlas ni soltarlas (necesidad 5). Necesita una apertura **≥130 mm** entre mordazas, capacidad sostenida **≥100 g**, fuerza de sujeción entre **5 N y 25 N** (suficiente para retener, insuficiente para aplastar), coeficiente de fricción mordaza‑roca **≥0.6**, superficie de contacto **≥4 cm²** por mordaza, cierre completo en **≤2 s** y una tasa de rocas retenidas durante el traslado **≥90 %**.

| # | Métrica | Nec. | Imp. | Unidades | Valor marginal | Valor ideal | Origen |
|--:|:--------|:----:|:----:|:---------|:--------------:|:-----------:|:-------|
| 46 | Apertura máxima entre mordazas | 5 | 5 | mm | ≥130 | ≥160 | Reglamento |
| 47 | Capacidad de carga sostenida de la pinza | 5 | 5 | g | ≥100 | ≥250 | Derivada |
| 48 | Fuerza de sujeción de la pinza (cota inferior) | 5 | 5 | N | ≥5 | ≥10 | Derivada |
| 49 | Fuerza de sujeción de la pinza (cota superior, no aplastar) | 5 | 5 | N | ≤25 | ≤15 | Hipótesis (H) |
| 50 | Coeficiente de fricción mordaza-roca | 5 | 5 | - | ≥0.6 | ≥0.9 | Hipótesis (H) |
| 51 | Superficie de contacto por mordaza | 5 | 4 | cm² | ≥4 | ≥8 | Hipótesis (H) |
| 52 | Tiempo de cierre completo de la pinza | 5, 8 | 3 | s | ≤2.0 | ≤1.0 | Hipótesis (H) |
| 53 | Tasa de rocas retenidas sin caída durante traslado | 5 | 5 | % | ≥90 | 100 | Hipótesis (H) |


### F. Almacenamiento y descarga

Todas las muestras viajan a bordo y se depositan dentro del contenedor (necesidad 6). La tolva debe tener **≥12 L** de capacidad, transportar **≥500 g** de carga útil simultánea y alojar **≥10 muestras** sin retorno intermedio. La descarga debe hacerse desde **≥25 cm** sobre el borde del contenedor y colocar **≥90 %** de las rocas dentro de él.

| # | Métrica | Nec. | Imp. | Unidades | Valor marginal | Valor ideal | Origen |
|--:|:--------|:----:|:----:|:---------|:--------------:|:-----------:|:-------|
| 54 | Capacidad volumétrica de tolva a bordo | 6 | 5 | L | ≥12 | ≥20 | Hipótesis (H) |
| 55 | Carga útil transportable simultánea | 6 | 5 | g | ≥500 | ≥750 | Derivada |
| 56 | Muestras alojadas a bordo sin retorno intermedio | 6 | 5 | unidades | ≥10 | ≥10 | Derivada |
| 57 | Altura de descarga sobre el borde del contenedor | 6 | 4 | cm | ≥25 | ≥35 | Derivada |
| 58 | Rocas depositadas dentro del contenedor por descarga | 6 | 5 | % | ≥90 | 100 | Reglamento |


### G. Energía y seguridad

El rover debe operar toda la jornada sin quedarse sin energía y sin interferir con otros equipos (necesidades 11, 12 y 13). El bus de potencia es de **12 V**, con batería **≥3 Ah** capaz de entregar **≥25 A continuos**, consumo medio **≤60 W** en misión completa y autonomía **≥30 min** en operación continua. La alimentación lógica debe estar **aislada del bus de motores**, y el reinicio o cambio de batería entre rondas debe tomar **≤5 min**.

| # | Métrica | Nec. | Imp. | Unidades | Valor marginal | Valor ideal | Origen |
|--:|:--------|:----:|:----:|:---------|:--------------:|:-----------:|:-------|
| 59 | Tensión nominal del bus de potencia | 11 | 3 | V | 12 | 14.8-24 | Definida por el equipo |
| 60 | Capacidad de batería | 11 | 3 | Ah | ≥3 | ≥6 | Derivada |
| 61 | Corriente de descarga continua de la batería | 11, 12 | 4 | A | ≥25 | ≥40 | Derivada |
| 62 | Consumo medio en misión completa | 11 | 3 | W | ≤60 | ≤35 | Hipótesis (H) |
| 63 | Autonomía energética en operación continua | 11 | 3 | min | ≥30 | ≥60 | Derivada |
| 64 | Alimentación lógica aislada del bus de motores | 12 | 4 | Sí/No | Sí | Sí | Derivada |
| 65 | Tiempo de reinicio / cambio de batería entre rondas | 13 | 2 | min | ≤5 | ≤2 | Definida por el equipo |


### H. Misión y registro

La misión completa se ejecuta dentro de los tiempos del reglamento (necesidad 8) mientras el operador registra lo que ve (necesidad 9): **≤45 s** por roca (aproximar, tomar, guardar), **≤600 s** para navegación y recolección, **≤300 s** para la secuencia del tablero (2 interruptores + 2 botones), **≤20 s** para registrar y georreferenciar cada roca y un error de posición estimada **≤50 cm** en el mapa.

| # | Métrica | Nec. | Imp. | Unidades | Valor marginal | Valor ideal | Origen |
|--:|:--------|:----:|:----:|:---------|:--------------:|:-----------:|:-------|
| 66 | Tiempo de ciclo por roca (aproximar, tomar, guardar) | 8 | 5 | s | ≤45 | ≤30 | Hipótesis (H) |
| 67 | Tiempo total de misión de navegación y recolección | 8 | 5 | s | ≤600 | ≤450 | Reglamento |
| 68 | Tiempo de la secuencia del tablero (2 interruptores + 2 botones) | 8 | 4 | s | ≤300 | ≤180 | Reglamento |
| 69 | Tiempo de registro y georreferencia por roca | 9 | 3 | s | ≤20 | ≤8 | Hipótesis (H) |
| 70 | Error de posición estimada de cada roca en el mapa | 9 | 3 | cm | ≤50 | ≤15 | Hipótesis (H) |


---

## 4) Supuestos y contradicciones detectadas en el reglamento

Puntos a resolver con los asesores:


- Envolvente: el reglamento indica 100 cm³ (cubo de 4.64 cm). Con el límite de 55 kg implicaría 550 g/cm³, 24× la densidad del osmio. Se asume cubo de 100 cm por lado.
- Rocas: 5/7/10/12 cm³ con peso de 20-50 g exige densidades de 1.67 a 10 g/cm³; el PLA es 1.24 g/cm³. Se asume que las cifras son aristas en cm, no volúmenes.
- Cantidad de muestras: el cuerpo del reglamento nunca la declara. Se asume 10 rocas, única cifra compatible con la tabla de puntaje (10 pts × 10).
- Puntaje: la fila 'Marca pendiente' calcula 10 × 2 = 30 (debería ser 20). El total oficial de 655 pts incorpora ese error; corregido serían 645 pts.
- Alcance: proyecto 100% teledirigido. Bajo el reglamento oficial esto compromete 'Regreso INICIO' (25 pts) y deja en zona gris el 'Mapa' (30 pts).
- Sensores: se especifican por su aporte al operador (latencia, fps, canales visibles). Un sensor sin métrica asociada no debe entrar al BOM.
- Tracción: dimensionada para 12.5 kg, rueda de 15 cm, μ de rodadura 0.25 y 30% de margen. El límite real no es el par sino la adherencia (se requiere μ ≥ 0.577 en pendiente de 30°).
- Brazo: pares calculados con eslabones de 0.25 y 0.20 kg y carga de 0.40 kg en la punta. Si se fabrica en aluminio, los pares suben aproximadamente 40%.
- Faltan por definir con los asesores: presupuesto techo, costo objetivo por subsistema, proveedor y método de verificación de cada métrica.


---

## Siguiente sección

[Diagramas a bloques]({{ '/02-diagramas-a-bloques/' | relative_url }})
