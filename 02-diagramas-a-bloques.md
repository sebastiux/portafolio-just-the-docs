---
layout: default
title: Diagramas a bloques
nav_order: 3
---

# Diagramas a bloques

Esta página documenta la arquitectura del rover en dos vistas: **mecánica** y **eléctrica/electrónica**. Los diagramas se irán actualizando conforme avance el diseño.

| Diagrama | Estado |
|:---------|:-------|
| Eléctrico / electrónico | Versión 1 publicada (sección 1) |
| Mecánico | Versión preliminar publicada, sin nomenclatura (sección 2) |

---

## 1) Diagrama eléctrico / electrónico

Hay **dos versiones** del diagrama. La **v2** es la vigente; la v1 se conserva abajo para ver de dónde salió cada decisión.

### Versión 2 (vigente)

Las líneas **azules** son señal y datos, las **verdes** el bus I2C y las **rojas** alimentación. Las líneas **punteadas** son lo que todavía no está decidido.

[![Figura 1 — Diagrama de componentes eléctricos, versión 2]({{ '/assets/img/rover/diagrama-electrico-v2.svg' | relative_url }})]({{ '/assets/img/rover/diagrama-electrico-v2.svg' | relative_url }})

**Figura 1:** Diagrama de componentes eléctricos, **versión 2** (19-oct-2026). Haz clic para verlo a tamaño completo.

#### Qué cambió respecto a la v1

| | Versión 1 | Versión 2 |
|:--|:--|:--|
| Comunicación Pi ↔ ESP32 | Sin definir | **Bus I2C** a 100 kHz, con direcciones `0x10`, `0x11` y `0x12` |
| Wi-Fi de los ESP32 | Encendido | **Apagado**: solo la Raspberry Pi transmite |
| Alimentación | Un regulador con tres salidas | **Cuatro rieles separados**: VBAT directo, dos BEC de servos y un buck de lógica |
| ESP32 | 3.3 V directos | 5 V al pin de entrada, y su propio LDO baja a 3.3 V |
| Batería | 11.7 V · 18 A, sin más detalle | LiPo **3S de 5000 mAh**, con **fusible de 30 A** e interruptor |
| Paro de emergencia | No aparecía | Corta los actuadores, **no la lógica** |
| Brazo | 3 servos | 5 servos: base, hombro, codo, pinza y tolva, con su par declarado |
| Sensores | Solo cámara | IMU, INA219, sensor de color, ToF, celda de carga y LIDAR como opcional |
| Presupuesto de corriente | No había | **19.0 A continuos** en el peor caso, ≈3.8C |

### Lectura del diagrama (v2)

**Control central**

- La **Raspberry Pi 4** es el maestro: recibe los comandos de la estación por **Wi-Fi 2.4 GHz** y le devuelve video y telemetría.
- Cuelgan de ella la **cámara** (USB o CSI), la **IMU BNO055** y el **INA219**, que mide voltaje y corriente de batería. El **LIDAR 2D** está dibujado punteado porque todavía no está decidido.

**Bus I2C**

- Un solo bus a **100 kHz y 3.3 V** conecta la Pi con los tres ESP32, con direcciones `0x10` (tracción), `0x11` (dirección) y `0x12` (brazo).
- Los pull-ups de 1.8 kΩ **ya vienen en la Pi**, en GPIO2 y GPIO3, así que no hay que agregarlos.
- Como el mando va por I2C, el **Wi-Fi de los ESP32 queda apagado**: menos consumo y menos interferencia con el enlace de la Pi.

**Tracción** — ESP32 `0x10`, VBAT directo

- Tres **drivers duales** mueven los 6 motores de 12 V, dos por driver.
- Los encoders de las ruedas medias entran al ESP32 por su periférico de pulsos, y los ultrasónicos también.
- **Failsafe:** si pasan 300 ms sin tráfico I2C, el ESP32 para los motores por su cuenta.

**Dirección** — ESP32 `0x11`, riel de servos A

- Cuatro **MG996R**, uno por rueda de esquina. Las ruedas centrales no giran.

**Brazo** — ESP32 `0x12`, riel de servos B

- Cinco servos: base, hombro, codo, pinza y tolva, con el par que necesita cada articulación.
- El sensor de color y el de distancia cuelgan de un **segundo bus I2C del propio ESP32**, no del bus de la Pi, así que sus direcciones no pueden chocar con las de los esclavos.

**Alimentación**

| Riel | Tensión | Alimenta a |
|:--|:--|:--|
| VBAT directo | 11.1 V nominal · 12 A | Los 3 drivers duales → 6 motores, sin regulador de por medio |
| BEC A | 6 V · ≥10 A | Los 4 servos de dirección |
| BEC B | 6–7.4 V · ≥10 A | Los 5 servos del brazo |
| Buck | 5.1 V · 5 A | Raspberry Pi, cámara, los 3 ESP32 y los sensores |

- La tierra es **común en un punto estrella**, no encadenada.
- El **paro de emergencia** corta los cuatro rieles de actuadores pero deja la lógica viva, así que la Pi sigue reportando por qué se detuvo.

### Nomenclatura

| Etiqueta | Significado |
|:---------|:------------|
| DI / DD | Delantero izquierdo / delantero derecho |
| MI / MD | Medio izquierdo / medio derecho |
| TI / TD | Trasero izquierdo / trasero derecho |
| VBAT | Tensión de batería sin regular |
| BEC | Regulador de servos (*battery eliminator circuit*) |
| `0x10` · `0x11` · `0x12` | Direcciones I2C de tracción, dirección y brazo |

### Consistencia con las especificaciones

Revisado contra la [tabla de métricas]({{ '/01-especificaciones/' | relative_url }}). **La v2 arregla unas cosas y deja otras igual**, y las que siguen abiertas se dicen como tales:

| Métrica | Qué pide | Qué trae la v2 | |
|:--|:--|:--|:--|
| 64 · Lógica aislada del bus de motores | Sí | Cuatro rieles separados y tierra en estrella. La v1 lo cumplía a medias con un regulador de tres salidas | ✅ |
| 59 · Tensión del bus de potencia | 12 V | 11.1 V nominal, que es lo que da un LiPo 3S. Baja a 9.9 V al final de la descarga | ⚠️ |
| 61 · Descarga continua de la batería | ≥25 A | El consumo estimado es de 19.0 A, pero **el diagrama no dice de cuántos C es el pack**. Para 25 A hacen falta ≥5C | ⚠️ |
| 28 · Corriente continua por canal del driver | ≥5 A | ≥4 A por canal. **Sigue sin cumplirse**, igual que en la v1 | ❌ |
| 29 · Corriente pico del driver | ≥15 A | No aparece en el diagrama | ❓ |
| 30 · Grados de libertad del brazo | ≥4 sin contar la pinza | 3 GDL: base, hombro y codo. **Sigue sin cumplirse** | ❌ |

**Lo que hay que resolver antes de comprar:**

1. **Driver de tracción.** Elegir uno de ≥5 A continuos y ≥15 A pico por canal, contra el par de bloqueo real de los motores.
2. **C de la batería.** Un pack de 5000 mAh a 19 A trabaja a 3.8C; para cubrir la métrica 61 hay que comprar ≥5C y dejarlo escrito.
3. **Cuarto grado de libertad del brazo.** O se agrega, o se cambia la métrica 30 con una justificación.

{: .note }
> Las corrientes de motor y de servo del diagrama están marcadas como **hipótesis**: salen de valores típicos, no de las hojas de datos de las piezas que se van a comprar ni de una medición. El INA219 está justamente para medir lo que de verdad consume el rover.

### Versión 1 (anterior)

Se conserva para comparar. **No describe lo que se va a construir**: su alimentación, el brazo de 3 servos y la ausencia de bus I2C quedaron sustituidos por la v2.

[![Figura 2 — Diagrama de componentes eléctricos, versión 1]({{ '/assets/img/rover/diagrama-electrico.svg' | relative_url }})]({{ '/assets/img/rover/diagrama-electrico.svg' | relative_url }})

**Figura 2:** Diagrama de componentes eléctricos, **versión 1**. Primera arquitectura, con un regulador de tres salidas y sin bus de comunicación definido.

---

## 2) Diagrama mecánico

Versión preliminar entregada por el equipo (fecha anotada en la hoja: **26/08/26**). Es un diagrama de bloques por **iconos**, sin texto ni leyenda.

[![Figura 3 — Diagrama mecánico a bloques (versión preliminar)]({{ '/assets/img/rover/diagrama-mecanico.jpg' | relative_url }})]({{ '/assets/img/rover/diagrama-mecanico.jpg' | relative_url }})
**Figura 3:** Diagrama mecánico a bloques, versión preliminar. Haz clic en la imagen para verla a tamaño completo.

### Lectura del diagrama

Lo que se puede afirmar mirando la hoja, sin interpretar los iconos:

- Hay un **elemento único en la parte superior** del que salen dos ramas hacia dos agrupaciones de bloques prácticamente **idénticas entre sí**, una a la izquierda y otra a la derecha de la hoja.
- Dentro de cada agrupación se repiten varias **cadenas de bloques** con la misma estructura.
- Los bloques se conectan con **líneas de un solo tipo**: no hay distinción gráfica entre unión, transmisión o soporte.
- Los bloques con el icono de **brazo articulado** aparecen resaltados con un fondo más oscuro; la hoja no explica qué significa ese resaltado.

### Pendientes antes de dar la sección por cerrada

Este diagrama todavía **no es interpretable sin la persona que lo dibujó**. Falta:

1. **Nomenclatura.** Ningún bloque tiene etiqueta. Sin nombres no se puede verificar contra la [tabla de métricas]({{ '/01-especificaciones/' | relative_url }}) ni contrastarlo con el diagrama eléctrico de la sección 1.
2. **Leyenda de iconos.** Los iconos son genéricos (motor, rodamiento, eslabón, brazo, cuña). La correspondencia icono → pieza real es una suposición, no un dato.
3. **Semántica de las líneas.** Definir qué representa una conexión: unión mecánica fija, articulación, transmisión de par o soporte estructural.
4. **Correspondencia con la sección 1.** El diagrama eléctrico declara **6 motores DC**, **4 servos de dirección** y **3 servos de brazo**. Este diagrama muestra cadenas de bloques repetidas en dos agrupaciones simétricas; hay que confirmar si el conteo de actuadores coincide con esa arquitectura o si hay una discrepancia.
5. **Versión vectorial.** La sección 1 usa SVG (texto seleccionable, escala sin pérdida). Esta es una imagen rasterizada; conviene redibujarla en el mismo formato una vez que existan las etiquetas.

---

## Sección anterior

[Características técnicas y necesidades]({{ '/01-especificaciones/' | relative_url }})
