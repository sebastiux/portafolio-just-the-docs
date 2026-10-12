---
layout: default
title: Comparación y conclusiones
parent: Brazos robóticos
nav_order: 3
permalink: /brazos/comparacion/
---

# Comparación y conclusiones

Esta página compara las **dos versiones fabricadas** con los mismos criterios (B29), reúne las **conclusiones técnicas** (B30) y revisa que la **evidencia y los archivos** correspondan con lo que se presenta (B31).

---

## 1) Comparación de las versiones fabricadas (B29)

### Fabricación

| Criterio | Brazo impreso en 3D | Brazo cortado con láser |
|:---------|:--------------------|:------------------------|
| Proceso | Impresión 3D (FDM) | Corte láser |
| Máquina | Creality Ender‑3 V3 KE | **[Pendiente]** |
| Material | PLA (Creality Hyper PLA) | MDF de 3 mm |
| Piezas fabricadas | **9** | **36** |
| Volumen de material en las piezas | 54.43 cm³ | 94.8 cm³ |
| Masa de las piezas | ≤ 67.5 g (si fueran 100 % sólidas; con 15 % de relleno es menos) | ≈ 71 g estimados con una densidad típica de MDF de 0.75 g/cm³ (por confirmar con báscula) |
| Material de partida | Filamento de 1.75 mm | 2 hojas de 150 × 200 mm |
| Tiempo de fabricación | **[Pendiente]** (suma de los G-code) | **[Pendiente]** (tiempo de corte de las 2 hojas) |
| Soportes o desperdicio | Sin soportes | Recorte de las hojas (**[pendiente]** medir el aprovechamiento) |
| Geometría posible | Volumétrica: horquillas, engranes, alojamientos cerrados | Solo placas planas de 3 mm |
| Archivos de fabricación | 9 STL + perfil de laminado | 2 hojas DXF |
| Reposición de una pieza | Reimprimir solo esa pieza | Recortarla con su DXF individual |

### Diseño y ensamble

| Criterio | Brazo impreso en 3D | Brazo cortado con láser |
|:---------|:--------------------|:------------------------|
| Diseño base | RACBOTS, Printables #449747 | MeArm v1.0, Benjamin Gray |
| Grados de libertad | 3 GDL + pinza | 3 GDL + pinza |
| Actuadores | 4 × SG90 | 4 × SG90 |
| Cinemática | Servo en cada articulación (serie) | Paralelogramo: servos de hombro y codo en la base |
| Carga sobre el hombro | Lleva el peso del servo del codo y del de la pinza | Menor: los servos van abajo |
| Pinza | Dos mordazas con sector dentado y piñón | Mordazas accionadas por eslabones |
| Envolvente del ensamble CAD | 174.0 × 58.1 × 117.5 mm | 264.1 × 95.2 × 156.8 mm |
| Pasos de armado | 7 ([secuencia]({{ '/brazos/impresion-3d/' | relative_url }}#9-secuencia-de-ensamblaje-b10)) | 13 según la guía oficial |
| Tiempo de armado | **[Pendiente]** | **[Pendiente]** |
| Tornillería | **[Pendiente]** | Tornillos M3 (**[pendiente]** cantidades) |

### Control y desempeño

| Criterio | Brazo impreso en 3D | Brazo cortado con láser |
|:---------|:--------------------|:------------------------|
| Controlador | Arduino Uno (comercial) | PCB propia con ESP32-C3 |
| Modos de operación | 1: computadora por USB | 2: manual (potenciómetros) y app |
| Rango de cada articulación | **[Pendiente]** | **[Pendiente]** |
| Apertura de la pinza | **[Pendiente]** (CAD: 19.3 mm entre centros) | **[Pendiente]** |
| Tomas exitosas de la pelota | **[Pendiente]** / 3 | **[Pendiente]** / 3 |
| Repetibilidad (misma posición, 3 veces) | **[Pendiente]** | **[Pendiente]** |
| Juego en las articulaciones | **[Pendiente]** | **[Pendiente]** |

> **Para que la comparación sea justa,** la prueba de desempeño debe hacerse con el **mismo objeto**, la **misma secuencia** y el **mismo número de intentos** en los dos brazos, y medir el rango de cada articulación de la misma forma.

---

## 2) Conclusiones técnicas (B30)

### Lo que ya se puede concluir

1. **Los dos procesos llevan a geometrías distintas para el mismo problema.** La impresión 3D permite piezas volumétricas (la horquilla de la tapa, los engranes de la pinza) con solo 9 piezas; el corte láser obliga a resolverlo todo con placas planas y necesita **36 piezas**, pero las fabrica en dos hojas y cada pieza se puede reponer por separado.
2. **El paralelogramo del MeArm compensa las limitaciones del MDF.** Al llevar los servos del hombro y el codo a la base, los eslabones de 3 mm no cargan el peso de los motores. El brazo impreso pone un servo en cada articulación, así que el hombro carga más; ahí conviene subir paredes y relleno (sección 8 del [brazo impreso]({{ '/brazos/impresion-3d/' | relative_url }}#8-fabricación-impresión-3d-r6)).
3. **El modelo 3D descargado no es igual a lo que se cortó.** Al comparar el STEP de GrabCAD con las hojas DXF, 13 de 31 placas difieren más de 4 mm; la base mide 95.00 mm en el modelo y 90.70 mm en lo cortado. **Las medidas de fabricación válidas son las de los DXF**, no las del modelo 3D.
4. **Las exportaciones del CAD tuvieron errores que se detectaron y corrigieron:**
   - El STEP del brazo impreso salió **sin sólidos**; solo se aprovecharon sus posiciones.
   - Tres exportaciones (las dos mordazas y el servo) salieron **2.54 veces más grandes**, que es el factor entre pulgadas y milímetros. Se corrigieron y se validaron contra medidas independientes (el SG90 mide 12.0 × 31.5 × 32.6 mm).
   - El STL de **Brazo 2 (P-04)** es una **malla abierta**, que puede dar problemas al laminar.
5. **El proyecto de laminado guardado no corresponde al brazo.** El `.3mf` contiene otra pieza (`linternass.stl`), así que los parámetros de impresión están documentados, pero el tiempo y la masa reales de cada pieza no.
6. **La pinza del brazo de láser se controla con dos ángulos fijos** (20° y 80°, provisionales) en vez de llevar el servo a tope, para que el SG90 no se caliente empujando contra la mordaza.
7. **Riesgo común a los dos brazos: la alimentación de los servos no está documentada.** Cuatro SG90 a la vez pueden pedir más corriente de la que entrega un Arduino por USB o un regulador pequeño. Es lo primero que hay que medir.

### Lo que falta para cerrar las conclusiones

{% include espacio.html criterio="B30" titulo="Conclusiones de desempeño" detalle="Con los resultados de las pruebas: ¿qué brazo tomó la pelota con más éxito?, ¿cuál fue más rápido de fabricar y de armar?, ¿qué problemas aparecieron al armar y cómo se corrigieron?, ¿se cumplieron los requisitos RQ1 a RQ9?, ¿qué cambiarían en una segunda versión?" %}

### Cumplimiento de requisitos

| # | Requisito | Impreso | Láser |
|:--|:----------|:--------|:------|
| RQ1 | 3 GDL + pinza | ✅ En el CAD; falta confirmar en físico | ✅ En el CAD; falta confirmar en físico |
| RQ2 | 4 servos SG90 | ✅ | ✅ |
| RQ3 | Un proceso de fabricación cada uno | ✅ Impresión 3D | ✅ Corte láser |
| RQ4 | Tomar la pelota | **[Pendiente]** | **[Pendiente]** |
| RQ5 | Control por USB | **[Pendiente]** | — |
| RQ6 | Control manual | — | **[Pendiente]** |
| RQ7 | Control con app | — | **[Pendiente]** |
| RQ8 | Tarjeta propia | — | **[Pendiente]** |
| RQ9 | Documentación | Ver la [autoevaluación]({{ '/brazos/evaluacion/' | relative_url }}) | Ver la [autoevaluación]({{ '/brazos/evaluacion/' | relative_url }}) |

---

## 3) Coherencia de la evidencia con la entrega (B31)

Lista de revisión antes de entregar. Cada punto se marca solo cuando es cierto para **la versión física que se presenta**.

| Revisión | Impreso | Láser |
|:---------|:--------|:------|
| Las fotos son del brazo real, no renders | **[Pendiente]** | **[Pendiente]** |
| Cada video muestra la prueba completa, sin cortes | **[Pendiente]** | **[Pendiente]** |
| Los archivos de fabricación son los que se usaron | ✅ STL de las 9 piezas | ✅ DXF tal como se mandaron a la máquina (**[pendiente]** confirmar que no se modificaron) |
| El código publicado es el que se cargó en la tarjeta | **[Pendiente]** | **[Pendiente]** |
| El esquemático corresponde a la tarjeta y al cableado reales | **[Pendiente]** | **[Pendiente]** |
| Las medidas de la página coinciden con el brazo armado | **[Pendiente]** (medir) | **[Pendiente]** (medir; el CAD difiere de lo cortado) |
| Cada prueba enlaza su resultado | **[Pendiente]** | **[Pendiente]** |

---

## Sección anterior

[Brazo cortado con láser]({{ '/brazos/corte-laser/' | relative_url }})

## Siguiente sección

[Autoevaluación]({{ '/brazos/evaluacion/' | relative_url }})
