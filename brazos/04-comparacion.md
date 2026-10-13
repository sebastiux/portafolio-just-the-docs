---
layout: default
title: Comparación y conclusiones
parent: Brazos robóticos
nav_order: 4
permalink: /brazos/comparacion/
---

# Comparación y conclusiones

Esta página compara las **dos versiones fabricadas** con los mismos criterios (B29), reúne las **conclusiones técnicas** (B30) y relaciona cada evidencia con el archivo que la respalda (B31).

---

## 1) Comparación de las versiones fabricadas (B29)

### Fabricación

| Criterio | Brazo impreso en 3D | Brazo cortado con láser |
|:---------|:--------------------|:------------------------|
| Proceso | Impresión 3D (FDM) | Corte láser de CO₂ |
| Máquina | Creality Ender‑3 V3 KE | Cortadora láser de CO₂ de 40–60 W |
| Material | PLA (Creality Hyper PLA) | MDF de 3 mm |
| Piezas fabricadas | **9** | **36** |
| Volumen de material en las piezas | 54.43 cm³ (sólido) | 94.8 cm³ |
| Material consumido | ≈40 g de PLA | 2 hojas de 150 × 200 mm |
| Tiempo de máquina | **≈1 h 30 min** (estimado por volumen) | **≈13.5 min** (9.30 m de corte a 15 mm/s) |
| Costo de material y máquina | ≈$17 | ≈$90 |
| Soportes o desperdicio | Sin soportes | Recorte de las hojas |
| Geometría posible | Volumétrica: horquillas, engranes, alojamientos cerrados | Solo placas planas de 3 mm |
| Archivos de fabricación | 9 STL + perfil de laminado | 2 hojas DXF + 36 DXF por pieza |
| Reposición de una pieza | Reimprimir solo esa pieza (1–40 min) | Recortarla con su DXF individual (< 1 min) |

### Diseño y ensamble

| Criterio | Brazo impreso en 3D | Brazo cortado con láser |
|:---------|:--------------------|:------------------------|
| Diseño base | RACBOTS, Printables #449747 | MeArm v1.0, Benjamin Gray |
| Grados de libertad | 3 GDL + pinza | 3 GDL + pinza |
| Actuadores | 4 × SG90 | 4 × SG90 |
| Cinemática | Servo en cada articulación (serie) | Paralelogramo: servos de hombro y codo en la base |
| Carga sobre el hombro | Lleva el peso del servo del codo y del de la pinza | Menor: los servos van abajo |
| Pinza | Dos mordazas con sector dentado y piñón (20 → 28 mm) | Mordazas accionadas por eslabones |
| Envolvente del ensamble CAD | 174.0 × 58.1 × 117.5 mm | 264.1 × 95.2 × 156.8 mm |
| Masa estimada (con servos) | ≈76 g | ≈107 g |
| Pasos de armado | 7 ([secuencia]({{ '/brazos/impresion-3d/' | relative_url }}#9-secuencia-de-ensamblaje-b10)) | 5 etapas, 13 pasos de la guía oficial |
| Tornillería | 9 tornillos M3 y 5 tuercas, más la de los servos | ≈36 tornillos M3 y 10 tuercas, más la de los servos |
| Costo mecánico | ≈$211 | ≈$316 |

### Control y desempeño

| Criterio | Brazo impreso en 3D | Brazo cortado con láser |
|:---------|:--------------------|:------------------------|
| Tarjeta | `brazo_control` v3 con ESP32-C3 Super Mini (58 × 48 mm, una cara) | La misma |
| Firmware | `firmware_brazo` con `BRAZO_IMPRESO` | `firmware_brazo` con `BRAZO_LASER` |
| Modos de operación | Manual (potenciómetros) y App (app web y USB), con el interruptor MODO | Igual |
| Rango de la base | 0–180° | 0–180° |
| Rango del hombro | 30–150° (120°) | 40–140° (100°) |
| Rango del codo | 20–160° (140°) | 40–140° (100°) |
| Pinza (cerrada / abierta) | 30° / 100° | 20° / 80° |
| Orientación de la pinza | Cambia con el hombro y el codo | Se mantiene horizontal (paralelogramo) |
| Velocidad máxima por articulación | 120 °/s | 120 °/s |
| Alimentación | 5 V lógica + 5–6 V, 3 A servos | Igual |

> **Para que la comparación sea justa,** la prueba de desempeño usa el **mismo objeto**, la **misma secuencia de órdenes** por USB (MODO en App) y el **mismo número de intentos** en los dos brazos (ver la prueba funcional de cada página).

---

## 2) Conclusiones técnicas (B30)

1. **Los dos procesos llevan a geometrías distintas para el mismo problema.** La impresión 3D permite piezas volumétricas (la horquilla de la tapa, los engranes de la pinza) con solo 9 piezas; el corte láser obliga a resolverlo todo con placas planas y necesita **36 piezas**, pero las fabrica en **≈13.5 min** contra **≈1.5 h** de impresión, y cada pieza se repone por separado.
2. **El paralelogramo del MeArm compensa las limitaciones del MDF.** Al llevar los servos del hombro y el codo a la base, los eslabones de 3 mm no cargan el peso de los motores y la pinza se mantiene horizontal. El precio es un rango menor (100° contra 120–140°), porque el paralelogramo se traba antes de los extremos del servo.
3. **El brazo impreso carga más el hombro.** Un servo en cada articulación suma peso al final del brazo; para el uso continuo conviene subir paredes (3–4) y relleno (25–40 %) en Brazo 1, Brazo 2 y la Tapa.
4. **Una sola tarjeta y un solo firmware sirven para los dos brazos.** La diferencia entre ellos se reduce a una tabla de límites en `config.h`, lo que permite comparar estructuras con el mismo control.
5. **El ADC del ESP32-C3 condicionó el circuito de los potenciómetros.** Con la atenuación por defecto mide bien solo hasta ≈2.5 V; con los potenciómetros directo a 3.3 V, el último cuarto de su giro no movería nada. R1–R3 (3.3 kΩ) en serie bajan el tope a ≈2.48 V y el firmware toma 2450 mV como fondo de escala.
6. **La alimentación de los servos se separa de la del microcontrolador.** Cuatro SG90 pueden pedir ≈2.8 A al arrancar juntos. La tarjeta tiene dos borneras: J2 lleva el canal de 5–6 V, 3 A directo a los servos por una pista de 1.6 mm, y J1 alimenta la lógica a través de D1, así que las caídas de los motores no reinician el ESP32-C3 y el USB nunca alimenta a la fuente. El firmware además limita la velocidad a 120 °/s para repartir los picos de corriente.
7. **El modelo 3D descargado no es igual a lo que se cortó.** Al comparar el STEP de GrabCAD con las hojas DXF, 13 de 31 placas difieren más de 4 mm; la base mide 95.00 mm en el modelo y 90.70 mm en lo cortado. **Las medidas de fabricación válidas son las de los DXF.**
8. **Las exportaciones del CAD tuvieron errores que se detectaron y corrigieron:** el STEP del brazo impreso salió sin sólidos (solo se usaron sus posiciones), tres exportaciones salieron 2.54 veces más grandes (pulgadas contra milímetros) y el STL de Brazo 2 es una malla abierta que hay que reparar antes de laminar.
9. **La pinza se controla por dos ángulos fijos** en vez de llevar el servo a tope, para que el SG90 no se caliente empujando contra la mordaza.
10. **Un interruptor de modo evita conflictos de mando.** Con SW2 el operador decide si mandan los potenciómetros o la app y la computadora; el firmware rechaza las órdenes remotas en Manual y lo avisa en la app y en la GUI.
11. **Una placa de una cara se puede fabricar en el laboratorio.** Sin vías ni puentes, con pistas de 0.8 mm o más y 0.6 mm de aislamiento, la tarjeta se fresa en la Genmitsu Cubiko sobre fenólica de 70 × 50 mm.
12. **El software se verificó antes de tener el hardware:** las 37 pruebas automáticas del firmware pasan en las dos configuraciones, y las dos interfaces (app y `brazo_gui.py`) se probaron contra el firmware compilado en la computadora.

### Requisitos cubiertos por el diseño

| # | Requisito | Impreso | Láser | Dónde se cubre |
|:--|:----------|:-------:|:-----:|:----------|
| RQ1 | 3 GDL + pinza | ✅ | ✅ | Ensamble CAD y visor 3D de cada brazo |
| RQ2 | 4 servos SG90 | ✅ | ✅ | Listas de materiales |
| RQ3 | Un proceso de fabricación cada uno | ✅ | ✅ | Registro de impresión y de corte |
| RQ4 | Tomar y trasladar la pelota | ✅ | ✅ | Apertura de la pinza mayor que la pelota; secuencia y criterio de la prueba funcional en cada página |
| RQ5 | Control manual | ✅ | ✅ | SW2, RV1–RV3 y SW1 en la tarjeta; pruebas 3, 5 y 8 del firmware |
| RQ6 | App web | ✅ | ✅ | `servidor_web` y `pagina_web.h`; captura de la app |
| RQ7 | Control por USB | ✅ | ✅ | `puerto_serie` y `brazo_gui.py`; prueba 6 del firmware |
| RQ8 | Tarjeta propia | ✅ | ✅ | Proyecto de KiCad, archivos de CNC y DRC sin errores |
| RQ9 | Alimentación de 2 canales con protección | ✅ | ✅ | Esquemático: J1, D1, C2 (lógica); J2, C1 (servos) |
| RQ10 | Ángulos limitados y velocidad máxima | ✅ | ✅ | Pruebas 4 y 6 del firmware |

### Mejoras para una segunda versión

| Mejora | Beneficio |
|:-------|:----------|
| Reemplazar los SG90 del hombro por MG90S (engranes metálicos) | Más par y menos juego donde más carga hay |
| Rodamiento axial en la base de los dos brazos | El servo de giro no carga el peso del brazo |
| Imprimir el brazo con 3–4 paredes y 30 % de relleno | Eslabones más rígidos |
| Agregar un sensor de corriente (INA219) a la tarjeta | Detectar cuando la pinza aprieta demasiado |
| Guardar posiciones desde la app y reproducirlas | Repetir la tarea sin operador |

---

## 3) Evidencias y archivos de la entrega (B31)

Cada entregable enlaza el archivo que lo respalda.

| Evidencia | Brazo impreso | Brazo de láser | Común |
|:----------|:--------------|:---------------|:------|
| Planos de fabricación | [PDF de 9 páginas]({{ '/assets/brazos/impreso3d/planos/planos-brazo-impreso-completo.pdf' | relative_url }}) | [PDF de 38 páginas]({{ '/assets/brazos/laser/planos/planos-mearm-completo.pdf' | relative_url }}) | |
| Archivos de fabricación | STL de cada pieza | [Hoja A]({{ '/assets/brazos/laser/corte/mearm-hoja-a.dxf' | relative_url }}) y [hoja B]({{ '/assets/brazos/laser/corte/mearm-hoja-b.dxf' | relative_url }}) | [Archivos de CNC de la tarjeta](https://github.com/sebastiux/portafolio-just-the-docs/tree/main/assets/brazos/electronica/brazo_control_pcb/cnc) |
| Ensamble 3D | [Visor y STL]({{ '/brazos/impresion-3d/' | relative_url }}#7-visor-3d-r5) | [STEP]({{ '/assets/brazos/laser/cad/mearm-mdf-ensamble.step' | relative_url }}) | |
| Secuencia de ensamblaje | [7 pasos con render]({{ '/brazos/impresion-3d/' | relative_url }}#9-secuencia-de-ensamblaje-b10) | [5 etapas]({{ '/brazos/corte-laser/' | relative_url }}#9-secuencia-de-ensamblaje-b10) | |
| Esquemático y PCB | | | [Proyecto completo]({{ '/assets/brazos/electronica/brazo_control_pcb_v3_58x48.zip' | relative_url }}) · [PDF]({{ '/assets/brazos/electronica/brazo_control_pcb/docs/esquematico.pdf' | relative_url }}) |
| Verificación eléctrica | | | [Esquemático contra PCB: 69 pines, 0 diferencias]({{ '/brazos/electronica-programacion/' | relative_url }}#3-esquemático-b15) · [DRC: 0 errores]({{ '/assets/brazos/electronica/brazo_control_pcb/docs/drc_report.txt' | relative_url }}) |
| Código fuente | | | [Firmware]({{ '/assets/brazos/codigo/firmware_brazo.zip' | relative_url }}) · [brazo_gui.py]({{ '/assets/brazos/codigo/brazo_gui.zip' | relative_url }}) |
| Pruebas del software | | | [37/37 por brazo]({{ '/brazos/electronica-programacion/' | relative_url }}#pruebas-automáticas-del-firmware) |
| Interfaces | | | [Capturas de la app y la GUI]({{ '/brazos/electronica-programacion/' | relative_url }}#9-interfaz-y-procedimiento-de-operación-b21) |

Los planos, renders, secuencia de ensamblaje y bocetos salen de scripts en [`tools/`](https://github.com/sebastiux/portafolio-just-the-docs/tree/main/tools), así que se pueden regenerar si cambia el diseño.

---

## Sección anterior

[Electrónica y programación]({{ '/brazos/electronica-programacion/' | relative_url }})
