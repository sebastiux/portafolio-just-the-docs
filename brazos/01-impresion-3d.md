---
layout: default
title: Brazo impreso en 3D
parent: Brazos robóticos
nav_order: 1
permalink: /brazos/impresion-3d/
stl_viewer: true
---

# Brazo impreso en 3D

Brazo de **3 GDL más pinza**, fabricado por **impresión 3D (FDM) en PLA**. Parte de un diseño publicado por RACBOTS; el equipo lo laminó, lo imprimió, lo armó y le hizo su electrónica.

> **Cómo usar los visores 3D:** arrastra para girar, rueda del ratón (o pellizco) para acercar y clic derecho (o dos dedos) para desplazar. **Reiniciar vista** regresa a la vista inicial.

| Rúbrica | Entregable | Estado |
|:--|:---|:---|
| R1 | Planos de las piezas | ✅ 9 planos A4 + resumen |
| R2 | Render de cada pieza | ✅ 9 renders |
| R3 | Ensamble en CAD | ⚠️ Captura de Inventor sí; el STEP exportado viene sin geometría |
| R4 | Render del ensamble | ✅ 3 vistas |
| R5 | Visor 3D en la página | ✅ |
| R6 | Proceso de fabricación | ✅ Parámetros de impresión; faltan fotos y video |
| R7 | Ensamble físico | ⏳ faltan fotos |
| R8 | Prueba tomando un objeto | ⏳ falta video |

---

## 1) Descripción general

| Dato | Valor |
|:-----|:------|
| Grados de libertad | **3 GDL + pinza** (base, hombro, codo y apertura de pinza) |
| Material | **PLA** (Creality Hyper PLA, 1.75 mm) |
| Piezas impresas | **9** |
| Volumen de PLA | **54.43 cm³**, masa máxima **67.5 g** sin servos ni tornillería |
| Actuadores | **4 servos SG90** |
| Control | **Arduino Uno** por USB |
| Envolvente del ensamble CAD | 174.0 × 48.1 × 117.5 mm en la pose exportada |
| Medidas del brazo armado | **[Pendiente]** <!-- PENDIENTE: medir el brazo físico. --> |
| Foto del brazo armado | **[Pendiente]** <!-- PENDIENTE: foto en assets/img/brazos/impreso3d/ --> |

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
| Servos | 4 × SG90 |
| Envolvente | 174.0 × 48.1 × 117.5 mm |

> **De dónde salen estas posiciones.** El STEP que exportó Inventor para este ensamble **viene sin geometría**: trae la estructura, las posiciones y los colores, pero cero sólidos. Aun así sirve, porque sus **transformaciones de ensamble sí están completas**, y son las que se aplican a los STL. Lo genera `tools/f2_ensamble_impreso.py`.
>
> **Corrección de escala en las mordazas.** Sus dos STL se exportaron **2.54 veces más grandes** que el resto (un dedo de 178 mm en un brazo con eslabones de 80 y 90 mm), así que se reescalan por 1/2.54. Dos comprobaciones de que la escala es la correcta: quedan en 70 × 25 × 6 mm, igual que las mordazas del archivo `pinzas.stl` original, y caen **simétricas** respecto al soporte, a 42.7 y 40.7 mm de su centro.

- **Descarga del STEP: [Pendiente]** <!-- PENDIENTE: el STEP exportado no trae sólidos, así que no se publica. Reexportarlo cuando se resuelva. -->
- **Los servos no aparecen en el ensamble: [Pendiente]** <!-- PENDIENTE: falta el STL de SERVO_SG90_mm exportado desde Inventor. Las 4 posiciones de servo sí están en el STEP; se probó sustituirlo por el modelo de SG90 del brazo de corte láser y no asienta, porque ese modelo tiene otro origen local. -->

---

## 6) Renderizado del ensamble (R4)

[![Render isométrico del ensamble]({{ '/assets/brazos/impreso3d/render/ensamble-iso.png' | relative_url }})]({{ '/assets/brazos/impreso3d/render/ensamble-iso.png' | relative_url }})
**Figura 2:** Vista isométrica de las 9 piezas en sus posiciones reales del CAD.

[![Render lateral del ensamble]({{ '/assets/brazos/impreso3d/render/ensamble-lateral.png' | relative_url }})]({{ '/assets/brazos/impreso3d/render/ensamble-lateral.png' | relative_url }})
**Figura 3:** Vista lateral.

[![Render superior del ensamble]({{ '/assets/brazos/impreso3d/render/ensamble-superior.png' | relative_url }})]({{ '/assets/brazos/impreso3d/render/ensamble-superior.png' | relative_url }})
**Figura 4:** Vista superior.

---

## 7) Visor 3D (R5)

<div class="stl-viewer stl-viewer--tall" data-assembly="{{ '/assets/stl/brazo-impreso/ensamble/ensamble-cad.json' | relative_url }}" data-base="{{ '/assets/stl/brazo-impreso/ensamble/' | relative_url }}"></div>

**Figura 5:** Ensamble interactivo, en coordenadas reales del CAD. Usa **Separar piezas** para la vista explosionada.

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

> **Nota de trazabilidad:** la placa laminada dentro de `Base_2_v2.3mf` contiene dos copias de una pieza llamada `linternass.stl` (2.08 g, 8 min 20 s), no la base del brazo. Por eso aquí se documentan los **parámetros del perfil**, pero **no** el tiempo ni el peso real de impresión de las piezas del brazo. Para completarlos hay que exportar el `.3mf` o el G‑code de cada placa del brazo.

- **Fotos y video de la impresión: [Pendiente]** <!-- PENDIENTE: JPG/WebP, lado largo 1600 px, máx. 500 KB, sin EXIF, con alt. -->

---

## 9) Ensamble físico (R7)

**[Pendiente]**

<!-- PENDIENTE: fotos del armado en assets/img/brazos/impreso3d/, sin EXIF. -->

---

## 10) Electrónica y control

| Elemento | Valor |
|:---------|:------|
| Controlador | **Arduino Uno** |
| Actuadores | **4 servos SG90** |
| Pin base (giro) | **D9** |
| Pin hombro | **D10** |
| Pin codo | **D11** |
| Pin pinza | **D6** |
| Interfaz de control | **Por USB**, con el script `brazo_gui.py` desde la computadora |
| Alimentación de los servos | **[Pendiente]** <!-- PENDIENTE: ¿los 4 SG90 se alimentan del regulador de 5 V del Arduino o de una fuente externa? 4 SG90 pueden pedir más corriente de la que entrega el Uno. --> |
| Firmware del Arduino | **[Pendiente]** <!-- PENDIENTE: publicar el .ino que recibe los comandos por serial. --> |
| `brazo_gui.py` | **[Pendiente]** <!-- PENDIENTE: publicar el script y una captura de la interfaz. --> |

> **Diferencia con el brazo de corte láser.** Este brazo se controla con **Arduino Uno por cable USB**; el de corte láser usa una **PCB propia con ESP32-C3** y una app servida por el propio microcontrolador. Son dos arquitecturas de control distintas a propósito.

---

## 11) Pruebas (R8)

**[Pendiente]**

<!-- PENDIENTE: video del brazo tomando la pelota roja de espuma, tabla de intentos y diámetro de la pelota. Contrastar contra la apertura de 19.3 mm entre mordazas. -->

---

## 12) Componentes comerciales

| Componente | Cantidad | Nota |
|:-----------|:--------:|:-----|
| Servo SG90 | 4 | Uno por GDL más la pinza |
| Arduino Uno | 1 | Control por USB |
| Filamento PLA 1.75 mm | — | 67 g como máximo para las 9 piezas |
| Tornillería y ejes | — | **[Pendiente]** <!-- PENDIENTE: medidas y cantidades. --> |

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
