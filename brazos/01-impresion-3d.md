---
layout: default
title: Brazo impreso en 3D
parent: Brazos robóticos
nav_order: 1
permalink: /brazos/impresion-3d/
stl_viewer: true
---

# Brazo impreso en 3D

Brazo de **3 GDL más pinza**, fabricado por **impresión 3D (FDM) en PLA**. Parte de un diseño publicado por RACBOTS; el equipo lo laminó, lo imprimió, lo armó y lo controla con la [tarjeta con ESP32-C3]({{ '/brazos/electronica-programacion/' | relative_url }}) común a los dos brazos.

> **Cómo usar los visores 3D:** arrastra para girar, rueda del ratón (o pellizco) para acercar y clic derecho (o dos dedos) para desplazar. **Reiniciar vista** regresa a la vista inicial.

---

## 1) Descripción general

| Dato | Valor |
|:-----|:------|
| Grados de libertad | **3 GDL + pinza** (base, hombro, codo y apertura de pinza) |
| Material | **PLA** (Creality Hyper PLA, 1.75 mm) |
| Piezas impresas | **9** |
| Volumen de PLA | **54.43 cm³**, masa máxima **67.5 g** sin servos ni tornillería |
| Actuadores | **4 servos SG90** |
| Control | **Tarjeta propia con ESP32-C3 Super Mini**: potenciómetros y switches, o app web; un switch elige cuál manda |
| Envolvente del ensamble CAD | 174.0 × 58.1 × 117.5 mm en la pose exportada |
| Alcance | 170 mm de eslabones (80 + 90) más 70 mm de pinza |
| Masa estimada | ≈40 g de PLA impreso + 4 × 9 g de servos ≈ **76 g** sin tarjeta |

---

## 2) Arquitectura

### Cadena cinemática

| Orden | Pieza | Función en el brazo |
|:-----:|:------|:--------------------|
| 1 | Base | Aloja el **servo de giro** de la base; se fija a la superficie de montaje con 3 orejas atornilladas. |
| 2 | Tapa | Plato giratorio sobre el servo de la base, con una **horquilla** de dos postes donde articula el brazo 1. |
| 3 | Brazo 1 | Primer eslabón (80 mm). Un extremo con ranura para el eje de la horquilla y otro con ventana para el servo del codo. |
| 4 | Brazo 2 | Segundo eslabón (90 mm), con alojamiento para el siguiente servo en el extremo. |
| 5 | Soporte de pinza | Marco con ventana rectangular para el **servo de la pinza**. |
| 6 | Piñón del servo | Engrane motriz montado en el eje del servo de la pinza. |
| 7 | Piñón de pinza | Engrane conducido que transmite el giro a las mordazas. |
| 8 | Pinza derecha | Mordaza con sector dentado que engrana con el piñón de pinza; el filo serrado sujeta la muestra. |
| 9 | Pinza izquierda | La misma pieza en espejo. Las dos cierran a la vez, movidas por el mismo piñón. |

- **Grados de libertad:** el brazo articula en la base (giro), el hombro (horquilla de la tapa) y el codo (brazo 1 → brazo 2), más la apertura de la pinza: **3 GDL + pinza**.
- **Alcance:** los dos eslabones suman **170 mm** (80 + 90) más la pinza.
- **Masa:** como máximo **67 g** de piezas impresas, sin servos ni tornillería.
- **Transmisión de la pinza:** el servo mueve la pinza a través de un par de engranes (piñón del servo de 20 mm → piñón de pinza de 28 mm), que reduce la velocidad y aumenta el par de cierre.
- **Apertura de la pinza:** en la pose del ensamble CAD las dos mordazas quedan separadas **19.3 mm** entre centros. Es el dato a contrastar con el diámetro de la pelota de la prueba.

---

## 3) Origen del diseño y créditos

El brazo impreso **no es un diseño original del equipo**. Parte de un modelo publicado por terceros, al que se le hicieron cambios cosméticos.

| Dato | Valor |
|:-----|:------|
| Diseño base | **"Brazo Robótico — Robotic Arm"**, modelo **#449747** en Printables |
| Autor del diseño base | **RACBOTS** |
| Fuente | <https://www.printables.com/model/449747> |
| Licencia del original | **[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)** (Atribución 4.0 Internacional), según declara la ficha de Printables |
| Qué permite esa licencia | Redistribuir, modificar y usar comercialmente, **siempre con atribución** |
| Modificaciones del equipo | **Sí**: cambios cosméticos sobre las piezas |
| Aporte del equipo | Cambios cosméticos sobre las piezas, laminado y parámetros de impresión, impresión, ensamble físico, electrónica y pruebas |

> **Atribución (CC BY 4.0).** Las piezas de esta página derivan de **"Brazo Robótico — Robotic Arm"** de **RACBOTS**, publicado en [Printables (#449747)](https://www.printables.com/model/449747) bajo [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). **El equipo modificó el diseño original** (cambios cosméticos). Los STL que se descargan desde esta página son obra derivada y se redistribuyen bajo la misma atribución.

<!-- Resuelto: son 9 piezas. El repositorio tenía 8 archivos porque las dos mordazas venían fundidas en pinzas.stl; el CAD las tiene como Pinza derecha v1 y Pinza izquierda v1_MIR_MIR3. -->

---

## 4) Piezas, planos y renders (R1 y R2)

Las 9 piezas se miden directamente sobre sus STL. La masa supone la pieza **100 % sólida** en PLA (1.24 g/cm³); con 2 paredes y 15 % de relleno la masa real será **menor**.

**Descargas:**

- [Plano completo, 9 páginas (PDF)]({{ '/assets/brazos/impreso3d/planos/planos-brazo-impreso-completo.pdf' | relative_url }})

| Render | Pieza | Nombre | Nombre en el CAD | Medidas (mm) | Volumen (cm³) | Masa máx. (g) | Archivos |
|:------:|:------|:-------|:-----------------|:-------------|--------------:|--------------:|:---------|
| <img src="{{ '/assets/brazos/impreso3d/render/piezas/P-01.png' | relative_url }}" alt="P-01" width="86" loading="lazy"> | **P-01** | Base (alojamiento servo) | `Base 2 v2` | 44.98 × 44.98 × 24.00 | 23.45 | 29.1 | [STL]({{ '/assets/stl/brazo-impreso/base.stl' | relative_url }}) · [Plano]({{ '/assets/brazos/impreso3d/planos/P-01.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/impreso3d/render/piezas/P-02.png' | relative_url }}" alt="P-02" width="86" loading="lazy"> | **P-02** | Tapa giratoria | `Tapa v2` | 37.99 × 38.00 × 29.50 | 12.85 | 15.9 | [STL]({{ '/assets/stl/brazo-impreso/tapa.stl' | relative_url }}) · [Plano]({{ '/assets/brazos/impreso3d/planos/P-02.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/impreso3d/render/piezas/P-03.png' | relative_url }}" alt="P-03" width="86" loading="lazy"> | **P-03** | Brazo 1 | `Brazo 1 v1` | 16.50 × 80.00 × 5.00 | 3.63 | 4.5 | [STL]({{ '/assets/stl/brazo-impreso/brazo-1.stl' | relative_url }}) · [Plano]({{ '/assets/brazos/impreso3d/planos/P-03.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/impreso3d/render/piezas/P-04.png' | relative_url }}" alt="P-04" width="86" loading="lazy"> | **P-04** | Brazo 2 | `Brazo 2 v1_FINAL_FInal` | 17.00 × 90.00 × 12.02 | 5.93 | 7.4 | [STL]({{ '/assets/stl/brazo-impreso/brazo-2.stl' | relative_url }}) · [Plano]({{ '/assets/brazos/impreso3d/planos/P-04.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/impreso3d/render/piezas/P-05.png' | relative_url }}" alt="P-05" width="86" loading="lazy"> | **P-05** | Soporte de pinza | `Soporte Pinza v1` | 29.00 × 44.00 × 4.00 | 2.43 | 3.0 | [STL]({{ '/assets/stl/brazo-impreso/soporte-pinza.stl' | relative_url }}) · [Plano]({{ '/assets/brazos/impreso3d/planos/P-05.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/impreso3d/render/piezas/P-06.png' | relative_url }}" alt="P-06" width="86" loading="lazy"> | **P-06** | Piñón del servo | `Piñon Servo v1` | 20.00 × 20.00 × 5.00 | 0.64 | 0.8 | [STL]({{ '/assets/stl/brazo-impreso/pinon-servo.stl' | relative_url }}) · [Plano]({{ '/assets/brazos/impreso3d/planos/P-06.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/impreso3d/render/piezas/P-07.png' | relative_url }}" alt="P-07" width="86" loading="lazy"> | **P-07** | Piñón de pinza | `Piñon pinza 1 v1` | 27.97 × 27.95 × 7.00 | 1.73 | 2.1 | [STL]({{ '/assets/stl/brazo-impreso/pinon-pinza.stl' | relative_url }}) · [Plano]({{ '/assets/brazos/impreso3d/planos/P-07.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/impreso3d/render/piezas/P-08.png' | relative_url }}" alt="P-08" width="86" loading="lazy"> | **P-08** | Pinza derecha | `Pinza derecha v1` | 70.23 × 24.30 × 6.15 | 1.92 | 2.4 | [STL]({{ '/assets/stl/brazo-impreso/pinza-derecha.stl' | relative_url }}) · [Plano]({{ '/assets/brazos/impreso3d/planos/P-08.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/impreso3d/render/piezas/P-09.png' | relative_url }}" alt="P-09" width="86" loading="lazy"> | **P-09** | Pinza izquierda | `Pinza izquierda v1_MIR_MIR3` | 70.23 × 24.77 × 6.15 | 1.85 | 2.3 | [STL]({{ '/assets/stl/brazo-impreso/pinza-izquierda.stl' | relative_url }}) · [Plano]({{ '/assets/brazos/impreso3d/planos/P-09.pdf' | relative_url }}) |

### Cómo se generaron

| Paso | Script |
|:-----|:-------|
| Medidas y render de cada pieza | `tools/f3_salidas_piezas_impreso.py` |
| Planos A4 y plano resumen | `tools/f3_planos_impreso.py` |

A diferencia del brazo de corte láser, estas piezas **no son planas**, así que cada plano lleva **tres vistas** (planta, alzado y lateral) a la misma escala. Son **siluetas proyectadas** de la malla: contorno exterior, sin aristas internas ni líneas ocultas. Sirven para identificar y acotar la pieza; no son planos de taller con cortes y tolerancias.

> **Una malla abierta.** P-04 (Brazo 2) no es una malla cerrada. Un STL no estanco puede dar problemas al laminar (relleno impredecible o paredes perdidas). Conviene repararlo antes de volver a imprimir esa pieza.

### Visores por pieza

<div class="stl-grid">
  <figure>
    <div class="stl-viewer" data-stl="{{ '/assets/stl/brazo-impreso/base.stl' | relative_url }}" data-color="#4B5563"></div>
    <figcaption><strong>Base</strong> · <a href="{{ '/assets/stl/brazo-impreso/base.stl' | relative_url }}" download>Descargar STL</a></figcaption>
  </figure>
  <figure>
    <div class="stl-viewer" data-stl="{{ '/assets/stl/brazo-impreso/tapa.stl' | relative_url }}" data-color="#E00034"></div>
    <figcaption><strong>Tapa</strong> · <a href="{{ '/assets/stl/brazo-impreso/tapa.stl' | relative_url }}" download>Descargar STL</a></figcaption>
  </figure>
  <figure>
    <div class="stl-viewer" data-stl="{{ '/assets/stl/brazo-impreso/brazo-1.stl' | relative_url }}" data-color="#F59E0B"></div>
    <figcaption><strong>Brazo 1</strong> · <a href="{{ '/assets/stl/brazo-impreso/brazo-1.stl' | relative_url }}" download>Descargar STL</a></figcaption>
  </figure>
  <figure>
    <div class="stl-viewer" data-stl="{{ '/assets/stl/brazo-impreso/brazo-2.stl' | relative_url }}" data-color="#2563EB"></div>
    <figcaption><strong>Brazo 2</strong> · <a href="{{ '/assets/stl/brazo-impreso/brazo-2.stl' | relative_url }}" download>Descargar STL</a></figcaption>
  </figure>
  <figure>
    <div class="stl-viewer" data-stl="{{ '/assets/stl/brazo-impreso/soporte-pinza.stl' | relative_url }}" data-color="#10B981"></div>
    <figcaption><strong>Soporte de pinza</strong> · <a href="{{ '/assets/stl/brazo-impreso/soporte-pinza.stl' | relative_url }}" download>Descargar STL</a></figcaption>
  </figure>
  <figure>
    <div class="stl-viewer" data-stl="{{ '/assets/stl/brazo-impreso/pinon-servo.stl' | relative_url }}" data-color="#8B5CF6"></div>
    <figcaption><strong>Piñón del servo</strong> · <a href="{{ '/assets/stl/brazo-impreso/pinon-servo.stl' | relative_url }}" download>Descargar STL</a></figcaption>
  </figure>
  <figure>
    <div class="stl-viewer" data-stl="{{ '/assets/stl/brazo-impreso/pinon-pinza.stl' | relative_url }}" data-color="#EC4899"></div>
    <figcaption><strong>Piñón de pinza</strong> · <a href="{{ '/assets/stl/brazo-impreso/pinon-pinza.stl' | relative_url }}" download>Descargar STL</a></figcaption>
  </figure>
  <figure>
    <div class="stl-viewer" data-stl="{{ '/assets/stl/brazo-impreso/pinza-derecha.stl' | relative_url }}" data-color="#0EA5E9"></div>
    <figcaption><strong>Pinza derecha</strong> · <a href="{{ '/assets/stl/brazo-impreso/pinza-derecha.stl' | relative_url }}" download>Descargar STL</a></figcaption>
  </figure>
  <figure>
    <div class="stl-viewer" data-stl="{{ '/assets/stl/brazo-impreso/pinza-izquierda.stl' | relative_url }}" data-color="#0284C7"></div>
    <figcaption><strong>Pinza izquierda</strong> · <a href="{{ '/assets/stl/brazo-impreso/pinza-izquierda.stl' | relative_url }}" download>Descargar STL</a></figcaption>
  </figure>
</div>

---

## 5) Ensamble en CAD (R3)

El ensamble se armó en **Autodesk Inventor 2026** (`Assembly_PLA.iam`).

[![Ensamble del brazo impreso abierto en Inventor 2026]({{ '/assets/img/brazos/impreso3d/captura-inventor-impreso.webp' | relative_url }})]({{ '/assets/img/brazos/impreso3d/captura-inventor-impreso.webp' | relative_url }})
**Figura 1:** `Assembly_PLA.iam` en Inventor 2026, con el árbol de componentes visible.

| Dato del ensamble | Valor |
|:------------------|:------|
| Piezas impresas | 9 |
| Servos | 4 × SG90, colocados |
| Elementos en el visor | 13 |
| Envolvente | 174.0 × 58.1 × 117.5 mm |

> **De dónde salen estas posiciones.** El STEP que exportó Inventor para este ensamble **viene sin geometría**: trae la estructura, las posiciones y los colores, pero cero sólidos. Aun así sirve, porque sus **transformaciones de ensamble sí están completas**, y son las que se aplican a los STL. Lo genera `tools/f2_ensamble_impreso.py`.
>
> **Corrección de escala.** Las dos mordazas y el servo se exportaron aparte, y los tres salieron **2.54 veces más grandes** que el resto, así que se reescalan por 1/2.54. Cada corrección se comprobó contra un dato independiente:
>
> - **Mordazas:** a escala 1 un dedo medía 178 mm en un brazo con eslabones de 80 y 90 mm. Corregidas quedan en 70 × 25 × 6 mm, igual que las mordazas que traía fundidas el archivo `pinzas.stl`, y caen **simétricas** respecto al soporte, a 42.7 y 40.7 mm de su centro.
> - **Servo:** corregido queda en **12.0 × 31.5 × 32.6 mm**, que son las medidas de un SG90, y coincide con el modelo de SG90 del brazo de corte láser. El mismo archivo se instancia cuatro veces, una por cada posición del STEP.

### Archivos editables y de fabricación (B07)

| Archivo | Para qué sirve | Descarga |
|:--------|:---------------|:---------|
| STL de las 9 piezas | Fabricación (laminado) | [Tabla de piezas](#4-piezas-planos-y-renders-r1-y-r2) |
| STL del ensamble en coordenadas del CAD, con los 4 servos | Importar el ensamble completo en cualquier programa de CAD | [Carpeta `ensamble/`](https://github.com/sebastiux/portafolio-just-the-docs/tree/main/assets/stl/brazo-impreso/ensamble) |
| Posiciones del ensamble (JSON) | Ubicación y color de cada pieza, usada por el visor 3D | [ensamble-cad.json]({{ '/assets/stl/brazo-impreso/ensamble/ensamble-cad.json' | relative_url }}) |
| Planos en PDF | Fabricación y verificación | [Plano completo]({{ '/assets/brazos/impreso3d/planos/planos-brazo-impreso-completo.pdf' | relative_url }}) |
| Modelo original editable | Punto de partida del diseño | [Printables #449747](https://www.printables.com/model/449747) |
| Scripts de medidas, planos, renders y secuencia | Regenerar todo lo anterior | [Carpeta `tools/`](https://github.com/sebastiux/portafolio-just-the-docs/tree/main/tools) |

---

## 6) Renderizado del ensamble (R4)

[![Render isométrico del ensamble]({{ '/assets/brazos/impreso3d/render/ensamble-iso.png' | relative_url }}?v=2)]({{ '/assets/brazos/impreso3d/render/ensamble-iso.png' | relative_url }}?v=2)
**Figura 2:** Vista isométrica. Las 9 piezas impresas más los 4 servos SG90, en sus posiciones reales del CAD.

[![Render lateral del ensamble]({{ '/assets/brazos/impreso3d/render/ensamble-lateral.png' | relative_url }}?v=2)]({{ '/assets/brazos/impreso3d/render/ensamble-lateral.png' | relative_url }}?v=2)
**Figura 3:** Vista lateral.

[![Render superior del ensamble]({{ '/assets/brazos/impreso3d/render/ensamble-superior.png' | relative_url }}?v=2)]({{ '/assets/brazos/impreso3d/render/ensamble-superior.png' | relative_url }}?v=2)
**Figura 4:** Vista superior.

---

## 7) Visor 3D (R5)

<div class="stl-viewer stl-viewer--tall" data-assembly="{{ '/assets/stl/brazo-impreso/ensamble/ensamble-cad.json' | relative_url }}?v=2" data-base="{{ '/assets/stl/brazo-impreso/ensamble/' | relative_url }}"></div>

**Figura 5:** Ensamble interactivo: las **9 piezas impresas** y los **4 servos SG90**, en coordenadas reales del CAD. Usa **Separar piezas** para la vista explosionada.

---

## 8) Fabricación: impresión 3D (R6)

Los parámetros salen del proyecto de **Creality Print 6.3** que usó el equipo (archivo `Base_2_v2.3mf`, fecha 29/09/26). Es el perfil de fábrica **0.20mm Standard** para la Ender‑3 V3 KE, sin modificaciones de soporte ni relleno.

### Equipo y material

| Parámetro | Valor |
|:----------|:------|
| Impresora | **Creality Ender‑3 V3 KE** |
| Boquilla | **0.4 mm** |
| Cama | **PEI texturizada** |
| Material | **Creality Hyper PLA**, 1.75 mm |
| Densidad del filamento | 1.24 g/cm³ |
| Relación de flujo | 0.95 |
| Laminador | Creality Print 6.3.0 |

### Temperaturas y enfriamiento

| Parámetro | Valor |
|:----------|:------|
| **Temperatura de boquilla** | **220 °C** (primera capa y resto) |
| **Temperatura de cama** | **50 °C** (primera capa y resto) |
| Ventilador de capa | **100 %** a partir de la 2.ª capa (apagado en la 1.ª) |
| Reducción de velocidad por enfriamiento | Activada |

### Capas, paredes y relleno

| Parámetro | Valor |
|:----------|:------|
| **Altura de capa** | **0.20 mm** (primera capa 0.20 mm) |
| Ancho de línea | 0.45 mm (pared exterior 0.42 mm) |
| **Paredes (perímetros)** | **2** (generador Arachne) |
| **Capas superiores / inferiores** | **4 / 4** |
| **Relleno** | **15 %**, patrón **zig‑zag** a 45° |
| Patrón de superficie superior / inferior | Monotónico |
| Traslape relleno‑pared | 30 % |
| Planchado (ironing) | No |
| Costura | Alineada |

### Velocidades y movimiento

| Parámetro | Valor |
|:----------|:------|
| Primera capa | 50 mm/s |
| Pared exterior | 200 mm/s |
| Pared interior | 300 mm/s |
| Relleno | 270 mm/s |
| Relleno sólido interno | 250 mm/s |
| Superficie superior | 200 mm/s |
| Puentes | 50 mm/s |
| Desplazamiento | 300 mm/s |
| Aceleración por defecto | 5000 mm/s² |
| Flujo volumétrico máximo | 23 mm³/s |
| Retracción | 0.8 mm a 30 mm/s, con Z‑hop de 0.2 mm |

### Adhesión, soportes y compensaciones

| Parámetro | Valor |
|:----------|:------|
| **Soportes** | **Desactivados** |
| Brim | Automático |
| Falda (skirt) | No |
| Compensación de pata de elefante | 0.15 mm |
| Compensación XY de agujeros / contorno | 0 mm / 0 mm |
| Secuencia | Por capa |

### Por qué estos parámetros funcionan para estas piezas

- **Sin soportes:** todas las piezas están modeladas para imprimirse **acostadas sobre su cara plana** (eslabones de 5–12 mm de espesor, engranes de 5–7 mm, pinzas de 6 mm), así que no hay voladizos que los necesiten.
- **Compensación de pata de elefante (0.15 mm):** importa en los **engranes** y en las **pinzas**, donde un primer escalón ensanchado haría que los dientes rocen.
- **Compensación XY en 0:** los barrenos de ejes y tornillos salen al tamaño del modelo; si un eje o un cuerno de servo no entra, este es el primer parámetro a ajustar (o rimar el barreno).
- **2 paredes y 15 % de relleno:** suficiente para piezas de prueba. Para el brazo definitivo, los eslabones cargan momento flector en el servo del hombro; conviene probar **3–4 paredes** y **25–40 % de relleno** en `Brazo 1`, `Brazo 2` y la `Tapa`.

> **Origen de los parámetros:** el perfil sale del proyecto `Base_2_v2.3mf`. Su placa laminada contiene otra pieza (`linternass.stl`), así que el tiempo y la masa por pieza de la tabla siguiente se calculan a partir del volumen de cada STL.

### Registro de impresión por pieza (B09)

Las 9 piezas caben en **una sola placa** de 220 × 220 mm. Las capas salen de la altura de cada pieza entre 0.20 mm; el material y el tiempo se estiman con el **60 %** del volumen sólido (2 paredes, 4 capas arriba y abajo y 15 % de relleno en piezas delgadas) y un flujo efectivo de **6 mm³/s**.

| Pieza | Orientación en la cama | Altura (mm) | Capas | Volumen sólido (cm³) | PLA estimado (g) | Tiempo estimado |
|:------|:-----------------------|------------:|------:|---------------------:|-----------------:|----------------:|
| P-01 Base | Sobre la cara de las orejas | 24.00 | 120 | 23.45 | 17.4 | 39 min |
| P-02 Tapa | Sobre el disco | 29.50 | 148 | 12.85 | 9.6 | 21 min |
| P-03 Brazo 1 | Acostada | 5.00 | 25 | 3.63 | 2.7 | 6 min |
| P-04 Brazo 2 | Acostada | 12.02 | 60 | 5.93 | 4.4 | 10 min |
| P-05 Soporte de pinza | Acostada | 4.00 | 20 | 2.43 | 1.8 | 4 min |
| P-06 Piñón del servo | Acostada | 5.00 | 25 | 0.64 | 0.5 | 1 min |
| P-07 Piñón de pinza | Acostada | 7.00 | 35 | 1.73 | 1.3 | 3 min |
| P-08 Pinza derecha | Acostada | 6.15 | 31 | 1.92 | 1.4 | 3 min |
| P-09 Pinza izquierda | Acostada | 6.15 | 31 | 1.85 | 1.4 | 3 min |
| **Total** | | | | **54.43** | **≈40.5** | **≈1 h 30 min** |

**Ajustes de fabricación:**

| Pieza | Ajuste | Motivo |
|:------|:-------|:-------|
| P-04 Brazo 2 | Reparar la malla antes de laminar (por ejemplo, *Reparar modelo* en Creality Print) | El STL no es una malla cerrada |
| P-06 y P-07 | Revisar la primera capa con la compensación de pata de elefante de 0.15 mm | Que los dientes no rocen |
| Barrenos de 3 mm | Pasar una broca de 3 mm si el tornillo no entra | La compensación XY de agujeros está en 0 |

---

## 9) Secuencia de ensamblaje (B10)

Orden de montaje **de la base hacia la pinza**, sacado de la jerarquía del ensamble CAD: cada servo se monta junto con la pieza que lo aloja. En cada imagen, lo gris ya está montado y lo de color se agrega en ese paso.

<div class="pasos">
  <figure>
    <img src="{{ '/assets/brazos/impreso3d/render/secuencia/paso-01.png' | relative_url }}" alt="Paso 1: base con el servo de giro" loading="lazy">
    <figcaption><strong>1.</strong> Meter el <strong>servo de giro</strong> en la <strong>base (P-01)</strong> y fijar la base a la mesa por sus 3 orejas.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/assets/brazos/impreso3d/render/secuencia/paso-02.png' | relative_url }}" alt="Paso 2: tapa giratoria" loading="lazy">
    <figcaption><strong>2.</strong> Montar la <strong>tapa giratoria (P-02)</strong> sobre el eje del servo de giro.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/assets/brazos/impreso3d/render/secuencia/paso-03.png' | relative_url }}" alt="Paso 3: servo del hombro y brazo 1" loading="lazy">
    <figcaption><strong>3.</strong> Colocar el <strong>servo del hombro</strong> en la horquilla de la tapa y unirle el <strong>brazo 1 (P-03)</strong>.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/assets/brazos/impreso3d/render/secuencia/paso-04.png' | relative_url }}" alt="Paso 4: servo del codo y brazo 2" loading="lazy">
    <figcaption><strong>4.</strong> Colocar el <strong>servo del codo</strong> en la ventana del brazo 1 y unirle el <strong>brazo 2 (P-04)</strong>.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/assets/brazos/impreso3d/render/secuencia/paso-05.png' | relative_url }}" alt="Paso 5: soporte de pinza y su servo" loading="lazy">
    <figcaption><strong>5.</strong> Atornillar el <strong>soporte de pinza (P-05)</strong> al brazo 2 y meter el <strong>servo de la pinza</strong>.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/assets/brazos/impreso3d/render/secuencia/paso-06.png' | relative_url }}" alt="Paso 6: piñones" loading="lazy">
    <figcaption><strong>6.</strong> Montar el <strong>piñón del servo (P-06)</strong> en el eje del servo y el <strong>piñón de pinza (P-07)</strong> engranado con él.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/assets/brazos/impreso3d/render/secuencia/paso-07.png' | relative_url }}" alt="Paso 7: mordazas" loading="lazy">
    <figcaption><strong>7.</strong> Colocar las <strong>pinzas derecha e izquierda (P-08, P-09)</strong> con sus sectores dentados engranados, simétricas respecto al soporte.</figcaption>
  </figure>
</div>

**Figura 6:** Secuencia de ensamblaje en 7 pasos. Generada con `tools/f6_secuencia_impreso.py` a partir de las posiciones reales del CAD.

> **Antes de montar cada cuerno de servo:** llevar el servo a **90°** desde el programa. Así cada articulación queda centrada en su recorrido y no hay que desarmar para corregir el ángulo.

### Tornillería y conexiones por paso

| Paso | Unión | Tornillería | Nota |
|:----:|:------|:------------|:-----|
| 1 | Servo de giro → base | 2 tornillos del SG90 (M2 × 8, incluidos) | El cable sale por la ranura lateral de la base |
| 1 | Base → mesa o placa | 3 tornillos M3 × 10 por las orejas | O cinta doble cara para pruebas |
| 2 | Tapa → eje del servo de giro | Cuerno de un brazo + tornillo del cuerno (M2 × 4, incluido) | Servo a 90° antes de apretar |
| 3 | Servo del hombro → horquilla de la tapa | 2 tornillos del SG90 | |
| 3 | Brazo 1 → servo del hombro | Cuerno + tornillo del cuerno; lado opuesto con un tornillo M3 × 12 y tuerca de seguridad como pasador | El pasador no se aprieta a fondo: el brazo debe girar libre |
| 4 | Servo del codo → ventana del brazo 1 | 2 tornillos del SG90 | |
| 4 | Brazo 2 → servo del codo | Cuerno + tornillo del cuerno | |
| 5 | Soporte de pinza → brazo 2 | 2 tornillos M3 × 8 | |
| 5 | Servo de la pinza → soporte | 2 tornillos del SG90 | |
| 6 | Piñón del servo → eje del servo | Tornillo del cuerno (el piñón entra a presión en el estriado) | |
| 6 | Piñón de pinza → soporte | Tornillo M3 × 10 como eje, con tuerca | Debe girar sin juego axial |
| 7 | Pinzas → soporte | 2 tornillos M3 × 10 como ejes, con tuerca de seguridad | Engranar con la pinza cerrada (servo a 30°) |

---

## 10) Brazo ensamblado (B11)

[![Brazo impreso ensamblado]({{ '/assets/brazos/impreso3d/render/ensamble-iso.png' | relative_url }}?v=2)]({{ '/assets/brazos/impreso3d/render/ensamble-iso.png' | relative_url }}?v=2)
**Figura 7:** Brazo impreso ensamblado: las 9 piezas y los 4 servos en sus posiciones del CAD (render).

| Elemento | Pieza o componente | Función |
|:---------|:-------------------|:--------|
| Base | P-01 | Aloja el servo de giro y se fija a la mesa |
| Plato giratorio | P-02 | Gira sobre la base y sostiene la horquilla del hombro |
| Eslabón del hombro | P-03 (80 mm) | Une hombro y codo |
| Eslabón del codo | P-04 (90 mm) | Une codo y soporte de pinza |
| Soporte de pinza | P-05 | Sostiene el servo de la pinza y los ejes de las mordazas |
| Transmisión de la pinza | P-06 y P-07 | Par de engranes 20 mm → 28 mm |
| Mordazas | P-08 y P-09 | Cierran sobre el objeto con su sector dentado |
| Actuadores | 4 × SG90 | Giro, hombro, codo y pinza |

---

## 11) Pruebas mecánicas (B12)

Cada articulación se mueve de tope a tope desde la app, con SW2 en APP, o con su potenciómetro, con el brazo armado y la pinza vacía. Los ángulos de la tabla son los que se piden en los deslizables.

| Prueba | Procedimiento | Criterio de aceptación |
|:-------|:--------------|:-----------------------|
| Giro de la base | Base de 0° a 180° | Recorre 0–180° sin que el cable del servo se tense ni roce la base |
| Hombro | Hombro de 30° a 150°, con el codo a 90° | Sube y baja sin vibrar; sostiene el brazo extendido sin caer |
| Codo | Codo de 20° a 160° | No choca con el brazo 1 en ningún extremo |
| Apertura de la pinza | Botones **Abrir** y **Cerrar** de la app, o SW1 | Abierta (100°): separación mayor que el diámetro de la pelota; cerrada (30°): las mordazas se tocan sin forzar el servo |
| Engranes de la pinza | Abrir y cerrar 20 veces | Los dientes no saltan ni rozan; las dos mordazas cierran al mismo tiempo |
| Holgura de los ejes | Mover a mano cada eslabón con el servo detenido | Juego menor a 1 mm en la punta de la pinza |
| Repetibilidad | Ir a 90°, 60°, 100°, 30° y volver con el botón **Inicio**, 5 veces | La punta vuelve al mismo punto con diferencia menor a 3 mm |

Los rangos de la tabla son los límites programados para este brazo en `config.h`: el firmware nunca pide un ángulo fuera de ellos.

---

## 12) Lista de materiales (B06)

### Mecánica

| Componente | Material o modelo | Medidas | Cantidad | Precio ref. (MXN) |
|:-----------|:------------------|:--------|:--------:|------------------:|
| Piezas impresas P-01 a P-09 | PLA (Creality Hyper PLA, 1.75 mm) | Ver la [tabla de piezas](#4-piezas-planos-y-renders-r1-y-r2) | 9 | 17 (≈40 g de un rollo de 1 kg de $420) |
| Servo SG90 | Micro servo 9 g, 1.8 kg·cm | 12.0 × 31.5 × 32.6 mm (envolvente del CAD) | 4 | 180 |
| Tornillo M3 × 8 | Acero, cabeza allen | — | 2 | 2 |
| Tornillo M3 × 10 | Acero, cabeza allen | — | 6 | 6 |
| Tornillo M3 × 12 | Acero, cabeza allen | — | 1 | 1 |
| Tuerca de seguridad M3 | Con inserto de nylon | — | 4 | 4 |
| Tuerca M3 | Hexagonal | — | 1 | 1 |
| Tornillería del SG90 | Incluida con cada servo | M2 × 8 y M2 × 4 | 4 juegos | — |
| | | | **Total mecánico** | **≈211** |

### Electrónica

Tarjeta de control con ESP32-C3 Super Mini, la misma del brazo de láser: [lista completa]({{ '/brazos/electronica-programacion/' | relative_url }}#2-lista-de-materiales-b14), 23 componentes sin contar los servos, que ya están en la lista mecánica. **Precio: [Pendiente]**, igual que en la lista electrónica.
<!-- PENDIENTE: precio de la tarjeta, con su fuente (pregunta 11) -->

---

## 13) Electrónica y programación (B13–B24)

Este brazo usa la [tarjeta de control con ESP32-C3]({{ '/brazos/electronica-programacion/' | relative_url }}) y el firmware común, compilado con `#define BRAZO BRAZO_IMPRESO`. Diagrama de bloques, esquemático, PCB, código, diagramas de flujo e interfaces están en esa página.

### Conexión de los servos

| Conector | GPIO | Servo |
|:--------:|:----:|:------|
| J3 | 5 | Base (giro) |
| J4 | 6 | Hombro |
| J5 | 7 | Codo |
| J6 | 10 | Pinza |

Los cuatro conectores llevan el mismo orden. Vistos desde la cara de componentes, de izquierda a derecha: **señal** (cable naranja), **V+** (rojo) y **GND** (café). El pad **cuadrado**, el de la derecha, es el pin 1 y es GND: si el conector entra al revés, el café queda del lado equivocado.

### Controles

| Control | GPIO | Qué mueve |
|:--------|:----:|:----------|
| RV1 | 1 | Base |
| RV2 | 0 | Hombro |
| RV3 | 3 | Codo |
| SW1 | 21 | Abre y cierra la pinza |
| SW2 | 20 | Elige el modo: MANUAL o APP |

### Parámetros de este brazo en `config.h`

| Articulación | Mínimo | Máximo | Inicio | Potenciómetro |
|:-------------|:------:|:------:|:------:|:-------------:|
| Base | 0° | 180° | 90° | RV1 |
| Hombro | 30° | 150° | 90° | RV2 |
| Codo | 20° | 160° | 90° | RV3 |
| Pinza | 30° (cerrada) | 100° (abierta) | 100° | SW1 |

{: .warning }
> Estos límites son **provisionales**: son valores de diseño, no medidos con el brazo armado. Los de la pinza sobre todo, porque dependen de hasta dónde cierran las mordazas sin forzar el servo.
<!-- PENDIENTE: angulos reales de pinza abierta y cerrada de este brazo (pregunta 10) -->

| Dato | Valor |
|:-----|:------|
| Red Wi-Fi | `Brazo-Impreso`, contraseña `brazo2026` |
| App | `http://192.168.4.1` |
| Velocidad máxima de cada articulación | 120 °/s |

---

## 14) Integración y pruebas (B25–B28)

### Integración física (B25)

| Elemento | Montaje |
|:---------|:--------|
| Tarjeta de control | Junto a la base, con los potenciómetros al frente del operador. **Cómo se fijó: [Pendiente]** — la tarjeta v3 no tiene barrenos de montaje |
| Cables de servo | Los del hombro, codo y pinza bajan por el costado de los eslabones con cinchos, dejando un bucle en cada articulación para que no se tensen al girar |
| Cable del servo de giro | Sale por la ranura de la base, directo a J3 |
| Alimentación | **Dos canales separados de la fuente**: el canal de lógica (5 a 5.5 V) a J1 y el de servos (5 a 6 V) a J2. Las tierras se unen en la tarjeta |
| USB | Solo para programar y para leer el diagnóstico; el brazo funciona sin él |

<!-- PENDIENTE: como se fijo la tarjeta al brazo (pregunta 6) -->

[![Brazo impreso en vista lateral]({{ '/assets/brazos/impreso3d/render/ensamble-lateral.png' | relative_url }}?v=2)]({{ '/assets/brazos/impreso3d/render/ensamble-lateral.png' | relative_url }}?v=2)
**Figura 8:** Vista lateral del brazo, con el recorrido de las articulaciones que deben librar los cables.

### Electrónica y programa sobre el brazo (B26)

| Entrada | Acción esperada | Criterio de aceptación |
|:--------|:----------------|:-----------------------|
| RV1 de tope a tope | La base gira de 0° a 180° | Proporcional, sin saltos |
| RV2 de tope a tope | El hombro va de 30° a 150° | Proporcional, sin saltos |
| RV3 de tope a tope | El codo va de 20° a 160° | Proporcional, sin saltos |
| SW1 | La pinza abre y cierra | Un solo movimiento por cambio |
| SW2 a APP | Los potenciómetros dejan de mover el brazo | D2 pasa a parpadear |
| Deslizadores de la app, con SW2 en APP | Mueven la misma articulación | El encabezado de la app dice `app` |
| Deslizadores de la app, con SW2 en MANUAL | No mueven nada | La app muestra el aviso de cambiar el switch |
| SW2 de vuelta a MANUAL | El brazo va hacia donde estén las perillas | Sin saltos: tarda, no brinca |

### Modos de operación (B27)

| Modo | Cómo se accede | Qué se comprueba |
|:-----|:---------------|:-----------------|
| MANUAL | SW2 en MANUAL | Las 3 articulaciones y la pinza responden a RV1–RV3 y SW1; D2 queda encendido fijo |
| APP | SW2 en APP, conectarse a `Brazo-Impreso` y abrir `http://192.168.4.1` | Deslizadores, botones de pinza e inicio; D2 parpadea |

El USB **no es un modo de mando**: solo programa la tarjeta y, con la orden `D`, imprime el reporte de diagnóstico.

### Prueba funcional completa (B28)

**Tarea:** tomar la pelota roja de espuma, levantarla, girar la base y soltarla en otro punto.

| Paso | Acción | Ángulos de referencia (base, hombro, codo, pinza) |
|:----:|:-------|:-------------------------------------------------|
| 1 | Posición de inicio | 90°, 90°, 90°, 100° (abierta) |
| 2 | Bajar sobre la pelota | 90°, 60°, 130°, 100° |
| 3 | Cerrar la pinza | 90°, 60°, 130°, 30° |
| 4 | Levantar | 90°, 100°, 90°, 30° |
| 5 | Girar la base | 150°, 100°, 90°, 30° |
| 6 | Bajar y soltar | 150°, 60°, 130°, 100° |
| 7 | Regresar al inicio | Botón **Inicio** de la app |

La secuencia se ejecuta desde la app con SW2 en APP, usando los ángulos de la tabla para que cada intento sea igual.

**Criterio de aceptación:** la pelota no se cae durante el traslado ni se deforma al cerrar la pinza, en **3 de 3 intentos** seguidos.

---

## Referencias

1. Página de referencia del curso: <https://hubergiron.github.io/cnc/diseno-mecanico-cnc/>
2. RACBOTS, *Brazo Robótico — Robotic Arm*, Printables #449747 (CC BY 4.0): <https://www.printables.com/model/449747>
3. Licencia Creative Commons Atribución 4.0 Internacional: <https://creativecommons.org/licenses/by/4.0/>

---

## Sección anterior

[Brazos robóticos: proyecto y equipo]({{ '/brazos/' | relative_url }})

## Siguiente sección

[Brazo cortado con láser]({{ '/brazos/corte-laser/' | relative_url }})
