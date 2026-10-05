---
layout: default
title: Brazo cortado con láser
parent: Brazos robóticos
nav_order: 2
permalink: /brazos/corte-laser/
---

# Brazo cortado con láser

Brazo de **3 GDL más pinza**, cortado con láser en **MDF de 3 mm**. Es un **MeArm v1.0**, diseño de Benjamin Gray, armado y electrificado por el equipo.

> **Estado: en elaboración.** Esta página ya tiene la estructura completa y los datos verificados sobre los archivos de diseño. Todo lo marcado **[Pendiente]** espera archivos o mediciones del equipo; nada de eso se rellena con suposiciones.

| Rúbrica | Entregable | Estado |
|:--|:---|:---|
| R1 | Planos de las piezas | Por generar desde los DXF |
| R2 | Render de cada pieza | Por generar desde los DXF |
| R3 | Ensamble en CAD | Hecho en Inventor 2026; falta la captura |
| R4 | Render del ensamble | Por generar desde el STEP |
| R5 | Visor 3D en la página | Por generar desde el STEP |
| R6 | Proceso de fabricación | [Pendiente]: parámetros, fotos y video |
| R7 | Ensamble físico | [Pendiente]: fotos |
| R8 | Prueba tomando un objeto | [Pendiente]: video |

<!-- PENDIENTE (bloqueante): los archivos de entrada no están en el repositorio.
     Para poder generar R1, R2, R4 y R5 hace falta subir a la rama docs/brazos-3gdl:
       _entrada_brazos/laser/Final Assembly.stp
       _entrada_brazos/laser/dxf/Mearm_1_0_150x200_A.dxf
       _entrada_brazos/laser/dxf/Mearm_1_0_150x200_B.dxf
       _entrada_brazos/laser/captura_inventor.png
       _entrada_brazos/laser/pcb/   (esquemático, firmware, foto, captura de la app)
     NO subir la carpeta inventor/ con los .SLDPRT: su licencia no está confirmada.
     Rutas de publicación acordadas:
       assets/stl/brazo-laser/        -> STL de las piezas y ensamble.json (visor)
       assets/brazos/laser/cad/       -> mearm-mdf-ensamble.step
       assets/brazos/laser/corte/     -> mearm-hoja-a.dxf, mearm-hoja-b.dxf y sus PNG
       assets/brazos/laser/planos/    -> a-01.pdf ... y planos-mearm-completo.pdf
       assets/brazos/laser/render/    -> renders del ensamble y de cada pieza
       assets/brazos/laser/fotos/     -> fotos del proceso y del brazo armado
-->

---

## 1) Descripción general

| Dato | Valor |
|:-----|:------|
| Grados de libertad | **3 GDL + pinza** (base, hombro, codo, apertura de pinza) |
| Material | **MDF de 3 mm** |
| Piezas cortadas | **31 placas** <!-- PENDIENTE: el conteo de 31 contornos salió de un análisis automático de los DXF. Verificarlo contra las piezas físicas antes de publicarlo como dato firme. --> |
| Hojas de corte | 2 hojas de **150 × 200 mm** |
| Actuadores | **4 servos SG90** |
| Control | PCB propia con **ESP32-C3 Super Mini** |
| Medidas generales del brazo armado | **[Pendiente]** <!-- PENDIENTE: medir el brazo físico. El STEP da una envolvente de ~285 × 97 × 148 mm, pero ese modelo no coincide del todo con lo que se cortó (ver sección 5), así que no sirve como medida del robot real. --> |
| Foto del brazo armado | **[Pendiente]** <!-- PENDIENTE: foto en assets/brazos/laser/fotos/ --> |

---

## 2) Arquitectura

| Articulación | Actuador | Mecanismo | Control manual |
|:-------------|:---------|:----------|:---------------|
| **Base** (giro) | Servo SG90 | Plato giratorio sobre la base | Potenciómetro |
| **Hombro** | Servo SG90 | Eslabón accionado desde la base | Potenciómetro |
| **Codo** | Servo SG90 | Eslabón accionado desde la base | Potenciómetro |
| **Pinza** | Servo SG90 | Mordazas accionadas por eslabones | Interruptor |

El MeArm resuelve el hombro y el codo con **eslabones en paralelogramo**: los dos servos van montados abajo, en la base, y mueven el brazo a distancia. Eso mantiene la **orientación de la pinza constante** sin importar la posición del brazo, y evita cargar los eslabones con el peso de los servos.

<!-- PENDIENTE: confirmar contra el brazo físico qué servo mueve qué articulación y
     con qué rango angular útil. El dato del paralelogramo viene del diseño del MeArm,
     no de una medición propia. -->

---

## 3) Origen del diseño y créditos

Este brazo **no es un diseño original del equipo**.

| Dato | Valor |
|:-----|:------|
| Diseño | **MeArm v1.0** |
| Autor | **Benjamin Gray** (Mime Industries) |
| Licencia declarada | **CC BY 4.0**, según la página del autor en Hackster [[3](#referencias)] |
| Archivos usados | Descargados de **GrabCAD**, "MeArm v1.0 robot arm" [[2](#referencias)] |
| Quién los subió a GrabCAD y bajo qué licencia | **[Pendiente]** <!-- PENDIENTE (L3): esa página de GrabCAD bloquea la lectura automática. Juan Pablo tiene que abrirla y anotar el uploader y la licencia declarada. Hasta entonces los .SLDPRT NO se republican aquí: solo se enlaza a GrabCAD. --> |
| Material del diseño original | Acrílico de 3 mm (el autor indica que admite madera) |
| Material que usó el equipo | **MDF de 3 mm** |

**Lo que aportó el equipo** (es lo que se documenta como trabajo propio):

- ensamble en **Autodesk Inventor 2026** (`Final Assembly.iam`), exportado a STEP el 5 de octubre de 2026;
- corte en MDF de 3 mm;
- armado físico;
- electrónica: PCB propia con ESP32-C3 y su app de control;
- pruebas.

---

## 4) Piezas, planos y renders (R1 y R2)

Los planos y los renders por pieza se generan **desde los archivos DXF**, no desde el modelo 3D, porque los DXF son lo que realmente se cortó (ver la sección 5). Cada pieza se extruye a 3 mm.

**Lo que se sabe de los DXF:**

| Dato | Hoja A | Hoja B |
|:-----|:-------|:-------|
| Tamaño | 150 × 200 mm | 150 × 200 mm |
| Unidades | mm | mm |
| Origen | (0, 0) | desplazado a x ≈ 147.5 |
| Diámetros de agujero | Ø2.65 mm y Ø3.0 mm | Ø2.65 mm y Ø3.0 mm |
| Capas | `0` y `Defpoints`, sin textos ni nombres de pieza | igual |

Entre las dos hojas hay **31 contornos exteriores** (conteo automático, pendiente de verificar a ojo).

**Tabla de piezas:** **[Pendiente]**

<!-- PENDIENTE: generar con los DXF. Por cada pieza: miniatura del render, número (A-01...,
     B-01...), nombre tomado del STEP cuando la diferencia de medidas sea <= 2 mm,
     medidas, número de agujeros, enlace al DXF individual y al plano PDF.
     También falta el plano resumen planos-mearm-completo.pdf. -->

---

## 5) Ensamble en CAD (R3)

El ensamble se armó en **Autodesk Inventor 2026** a partir de las piezas descargadas de GrabCAD y se exportó a STEP.

| Dato del STEP | Valor |
|:--------------|:------|
| Cuerpos | 65 |
| Placas | 31, todas de **3.00 mm** |
| Servos en el ensamble | 4 × SG90, en posición |
| Envolvente aproximada | 285 × 97 × 148 mm |
| Piezas repetidas | `Part 04` ×5, `Part 26` (Straight Lever) ×3, `Part 12` (Cradle Ends) ×2 |

- **Captura de Inventor con el árbol de componentes: [Pendiente]** <!-- PENDIENTE (L2): captura de pantalla con Final Assembly.iam abierto y el árbol visible. Es la evidencia que pide R3. -->
- **Descarga del STEP: [Pendiente]** <!-- PENDIENTE: publicar en assets/brazos/laser/cad/mearm-mdf-ensamble.step una vez subido el archivo de entrada. -->
- Los archivos `.SLDPRT` de las piezas **no se republican aquí** mientras no se confirme su licencia en GrabCAD. Están en la fuente original [[2](#referencias)].

### ⚠️ El modelo 3D no coincide del todo con lo que se cortó

Se compararon las medidas en planta de las 31 placas del STEP contra los 31 contornos de los DXF, emparejando cada placa con su mejor candidata:

| Diferencia entre STEP y DXF | Placas |
|:---|---:|
| ≤ 1.5 mm | 7 |
| 1.5 – 4 mm | 8 |
| > 4 mm, o sin pareja | **16** |

Ejemplos: la base mide 95 × 145 mm en el STEP y 90.7 × 145 mm en el DXF; `Part 06` (12 × 122.9 mm) no tiene equivalente en los DXF; y en los DXF hay piezas de 15.6 × 103.4 mm y 15.8 × 93.9 mm que no existen en el STEP.

> **Nota.** El ensamble 3D se armó en Inventor con las piezas del modelo de GrabCAD; algunas piezas de ese modelo difieren en dimensiones de las hojas de corte que se usaron. **Los planos corresponden a las piezas cortadas; el ensamble 3D y los renders corresponden al modelo de GrabCAD.**

**Hipótesis** (sin confirmar): los `.SLDPRT` de GrabCAD son una variante del MeArm distinta de las hojas DXF v1.0. El método tiene un límite conocido: los contornos de los DXF se separan automáticamente y puede haber piezas mal divididas.

<!-- PENDIENTE: repetir la comparación con mejor separación de contornos cuando lleguen
     los archivos, y publicar aquí la tabla de emparejamiento final pieza por pieza.
     Además: las piezas Part 09, Part 23 y Part 27 (Sticky Foot) existen como .SLDPRT
     pero no están en el ensamble. Confirmar si simplemente no se usaron. -->

---

## 6) Renderizado del ensamble (R4)

**[Pendiente]**

<!-- PENDIENTE: generar desde el STEP tres renders (isométrico, lateral y superior) a
     1600 x 1200 con fondo claro, MDF en #B08A5A y servos en azul. Descartar los cuerpos
     de volumen cero: Part 17 - Base aparece duplicada, con un cuerpo de 33.4 cm3 y otro
     de volumen 0. Guardar en assets/brazos/laser/render/. -->

---

## 7) Visor 3D (R5)

**[Pendiente]**

<!-- PENDIENTE: usar el visor que ya existe en el repositorio (assets/js/stl-viewer.js),
     el mismo del brazo impreso. Pasos:
       1. convertir el STEP a STL por pieza y publicarlos en assets/stl/brazo-laser/;
       2. escribir assets/stl/brazo-laser/ensamble.json con el mismo formato que
          assets/stl/brazo-impreso/ensamble.json (name, file, color, position, explode);
       3. agregar "stl_viewer: true" al front matter de ESTA página;
       4. insertar el visor de ensamble y la rejilla de visores por pieza.
     No hace falta model-viewer ni GLB: se reutiliza el visor de three.js que ya funciona. -->

---

## 8) Fabricación: corte láser (R6)

| Dato | Valor |
|:-----|:------|
| Cortadora | **[Pendiente]** <!-- PENDIENTE: marca, modelo y área de trabajo. --> |
| Software | **[Pendiente]** <!-- PENDIENTE: LightBurn, RDWorks u otro, con versión. --> |
| Material | MDF de **3 mm** |
| Potencia | **[Pendiente]** <!-- PENDIENTE: % de potencia. --> |
| Velocidad | **[Pendiente]** <!-- PENDIENTE: mm/s. --> |
| Pasadas | **[Pendiente]** <!-- PENDIENTE: número de pasadas. --> |
| Kerf medido y compensación | **[Pendiente]** <!-- PENDIENTE: importante porque el MeArm usa uniones a presión y ejes de 3 mm. --> |
| ¿Se cortaron los DXF sin modificar? | **[Pendiente]** <!-- PENDIENTE: confirmar que se mandaron Mearm_1_0_150x200_A/B.dxf tal cual, sin reescalar ni compensar en el software de la máquina. --> |

> **Cambio de material respecto al diseño original.** El MeArm v1.0 está pensado para **acrílico de 3 mm**. Aquí se cortó **MDF de 3 mm**. El MDF es más blando y más tolerante al apriete, pero se desgasta en los agujeros que giran; conviene revisar el juego en los pivotes después de las pruebas.

- **Vista de las hojas de corte: [Pendiente]** <!-- PENDIENTE: PNG de cada hoja con fondo blanco y trazo negro (el color 7 de DXF se ve blanco sobre blanco, hay que forzar el negro). -->
- **Fotos y video del corte: [Pendiente]** <!-- PENDIENTE: JPG/WebP, lado largo 1600 px, máx. 500 KB, sin EXIF, con alt. Video a YouTube no listado y embebido. -->

---

## 9) Ensamble físico (R7)

El armado sigue la **guía oficial de 13 pasos** del autor del MeArm [[3](#referencias)]. No se reproduce aquí: se enlaza para no republicar contenido ajeno.

- **Fotos propias del armado: [Pendiente]** <!-- PENDIENTE: fotos en assets/brazos/laser/fotos/, sin EXIF. -->

---

## 10) Electrónica y control

| Elemento | Valor |
|:---------|:------|
| Controlador | **PCB propia** con **ESP32-C3 Super Mini** |
| Actuadores | **4 servos SG90** |
| Control manual | **3 potenciómetros** (uno por servo de movimiento) y **1 interruptor** para la pinza |
| Control remoto | **App servida por el propio ESP32-C3** |
| Alimentación | Batería o fuente de laboratorio |
| Esquemático / KiCad | **[Pendiente]** <!-- PENDIENTE: subir el proyecto de KiCad o, como mínimo, el esquemático en PDF. --> |
| Foto o render de la PCB | **[Pendiente]** |
| Firmware | **[Pendiente]** |
| Pinout | **[Pendiente]** <!-- PENDIENTE: qué GPIO del ESP32-C3 va a cada servo, a cada potenciómetro y al interruptor. --> |
| Captura de la app | **[Pendiente]** |
| Alimentación de los servos | **[Pendiente]** <!-- PENDIENTE: 4 SG90 en movimiento simultáneo pueden pedir picos de varios amperes. Documentar de dónde sale esa corriente y si hay capacitor de desacople. --> |

### Mapeo de los controles

Cada uno de los 4 servos tiene su propio control: los **3 servos de movimiento** se manejan con un potenciómetro cada uno, de forma proporcional, y el **servo de la pinza** con un interruptor de dos posiciones (abrir y cerrar).

| Control | Tipo de señal | Actúa sobre |
|:--------|:--------------|:------------|
| Potenciómetro 1 | Analógica, proporcional | Servo de la **base** (giro) |
| Potenciómetro 2 | Analógica, proporcional | Servo del **hombro** |
| Potenciómetro 3 | Analógica, proporcional | Servo del **codo** |
| Interruptor | Digital, dos posiciones | Servo de la **pinza** (abrir / cerrar) |

<!-- PENDIENTE: confirmar qué potenciómetro corresponde a qué articulación en la PCB
     física, y si el interruptor manda la pinza a dos ángulos fijos o a dos extremos
     de recorrido. -->

---

## 11) Pruebas (R8)

**[Pendiente]**

<!-- PENDIENTE: video del brazo tomando la pelota roja de espuma del primer proyecto,
     más una tabla de intentos (intento, resultado, observación) y el diámetro de la pelota. -->

---

## 12) Componentes comerciales

| Componente | Cantidad | Nota |
|:-----------|:--------:|:-----|
| Servo SG90 | 4 | Uno por GDL más la pinza |
| PCB propia con ESP32-C3 Super Mini | 1 | Diseño del equipo |
| Potenciómetro | 3 | Control manual |
| Interruptor | 1 | Apertura y cierre de la pinza |
| Tornillería M3 | — | **[Pendiente]** <!-- PENDIENTE: longitudes y cantidades por longitud. --> |
| Hoja de MDF de 3 mm, 150 × 200 mm | 2 | Hojas A y B de corte |

<!-- PENDIENTE: agregar enlaces de compra y precios, como en la página de referencia del curso. -->

---

## Referencias

1. Página de referencia del curso: <https://hubergiron.github.io/cnc/diseno-mecanico-cnc/>
2. *MeArm v1.0 robot arm*, GrabCAD: <https://grabcad.com/library/675982>
3. Benjamin Gray, *MeArm Robot Arm — Your Robot V1.0* (guía de armado, CC BY 4.0), Hackster: <https://www.hackster.io/benbobgray/mearm-robot-arm-your-robot-v1-0-326702>

---

## Sección anterior

[Brazo impreso en 3D]({{ '/brazos/impresion-3d/' | relative_url }})
