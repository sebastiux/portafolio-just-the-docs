---
layout: default
title: Brazo cortado con láser
parent: Brazos robóticos
nav_order: 2
permalink: /brazos/corte-laser/
stl_viewer: true
---

# Brazo cortado con láser

Brazo de **3 GDL más pinza**, cortado con láser en **MDF de 3 mm**. Es un **MeArm v1.0**, diseño de Benjamin Gray; el equipo lo ensambló en CAD, lo cortó, lo armó y lo controla con la [tarjeta con ESP32-C3]({{ '/brazos/electronica-programacion/' | relative_url }}) común a los dos brazos.

> **Cómo usar el visor 3D:** arrastra para girar, rueda del ratón (o pellizco) para acercar y clic derecho (o dos dedos) para desplazar. **Reiniciar vista** regresa a la vista inicial.

---

## 1) Descripción general

| Dato | Valor |
|:-----|:------|
| Grados de libertad | **3 GDL + pinza** (base, hombro, codo y apertura de pinza) |
| Material | **MDF de 3 mm** |
| Piezas cortadas | **36** (26 en la hoja A, 10 en la hoja B) |
| Hojas de corte | 2 de **150 × 200 mm** |
| Volumen de MDF | **94.8 cm³** sumando las 36 piezas |
| Actuadores | **4 servos SG90** |
| Control | **Tarjeta propia con ESP32-C3 Super Mini**: potenciómetros y switches, o app web; un switch elige cuál manda |
| Envolvente del ensamble CAD | 264.1 × 95.2 × 156.8 mm en la pose exportada |
| Alcance | ≈160 mm de eslabones (2 × ≈80 mm) más la pinza |
| Masa estimada | 94.8 cm³ × 0.75 g/cm³ ≈ 71 g de MDF + 4 × 9 g de servos ≈ **107 g** sin tornillería ni tarjeta |

---

## 2) Arquitectura

| Articulación | Actuador | Mecanismo | Control manual |
|:-------------|:---------|:----------|:---------------|
| **Base** (giro) | Servo SG90 | Plato giratorio sobre la base | Potenciómetro |
| **Hombro** | Servo SG90 | Eslabón accionado desde la base | Potenciómetro |
| **Codo** | Servo SG90 | Eslabón accionado desde la base | Potenciómetro |
| **Pinza** | Servo SG90 | Mordazas accionadas por eslabones | Switch SW1 |

El MeArm resuelve el hombro y el codo con **eslabones en paralelogramo**: los dos servos van montados abajo, en la base, y mueven el brazo a distancia. Eso mantiene la **orientación de la pinza constante** sin importar la posición del brazo, y evita cargar los eslabones con el peso de los servos.

---

## 3) Origen del diseño y créditos

Este brazo **no es un diseño original del equipo**.

| Dato | Valor |
|:-----|:------|
| Diseño | **MeArm v1.0** |
| Autor | **Benjamin Gray** (Mime Industries) |
| Licencia declarada | **CC BY 4.0**, según la página del autor en Hackster [[3](#referencias)] |
| Archivos usados | Descargados de **GrabCAD**, "MeArm v1.0 robot arm" [[2](#referencias)] |
| Material del diseño original | Acrílico de 3 mm (el autor indica que admite madera) |
| Material que usó el equipo | **MDF de 3 mm** |

**Lo que aportó el equipo:** el ensamble en Autodesk Inventor 2026, el corte en MDF, el armado físico, la tarjeta con ESP32-C3, el firmware, la app y las pruebas.

---

## 4) Piezas, planos y renders (R1 y R2)

Los contornos salen de **las dos hojas DXF**, que es lo que realmente se cortó, no del modelo 3D (ver la sección 5). Cada pieza se extruyó a 3 mm para su render, y su plano se dibuja a escala normalizada.

**Descargas:**

- [Plano completo, 38 páginas (PDF)]({{ '/assets/brazos/laser/planos/planos-mearm-completo.pdf' | relative_url }}) — las dos hojas numeradas más un A4 por pieza
- [Hoja A de corte (DXF)]({{ '/assets/brazos/laser/corte/mearm-hoja-a.dxf' | relative_url }}) · [Hoja B de corte (DXF)]({{ '/assets/brazos/laser/corte/mearm-hoja-b.dxf' | relative_url }}) — sin modificar, tal como se mandaron a la máquina

### Hojas numeradas

[![Hoja A de corte, 26 piezas numeradas]({{ '/assets/brazos/laser/corte/hoja-a.png' | relative_url }})]({{ '/assets/brazos/laser/corte/hoja-a.png' | relative_url }})
**Figura 1:** Hoja A, 26 piezas. Haz clic para verla a tamaño completo.

[![Hoja B de corte, 10 piezas numeradas]({{ '/assets/brazos/laser/corte/hoja-b.png' | relative_url }})]({{ '/assets/brazos/laser/corte/hoja-b.png' | relative_url }})
**Figura 2:** Hoja B, 10 piezas.

### Tabla de piezas

Las medidas son de la caja envolvente del contorno; el espesor es 3 mm en todas. La columna de nombre solo se llena cuando la pieza cortada coincide con una placa del modelo CAD dentro de 2 mm: **11 de 36**. Un guion significa que el modelo de GrabCAD no tiene equivalente cercano.

| Render | Pieza | Nombre en el modelo CAD | Medidas (mm) | Agujeros | Volumen (cm³) | Archivos |
|:------:|:------|:------------------------|:-------------|---------:|--------------:|:---------|
| <img src="{{ '/assets/brazos/laser/render/piezas/A-01.png' | relative_url }}" alt="A-01" width="86" loading="lazy"> | **A-01** | — | 2.64 × 2.66 | 0 | 0.02 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-01.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-01.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-02.png' | relative_url }}" alt="A-02" width="86" loading="lazy"> | **A-02** | — | 3.00 × 3.00 | 0 | 0.02 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-02.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-02.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-03.png' | relative_url }}" alt="A-03" width="86" loading="lazy"> | **A-03** | — | 5.40 × 3.14 | 0 | 0.05 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-03.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-03.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-04.png' | relative_url }}" alt="A-04" width="86" loading="lazy"> | **A-04** | — | 3.00 × 3.00 | 0 | 0.02 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-04.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-04.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-05.png' | relative_url }}" alt="A-05" width="86" loading="lazy"> | **A-05** | Part 14-1 | 49.80 × 29.76 | 3 | 1.92 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-05.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-05.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-06.png' | relative_url }}" alt="A-06" width="86" loading="lazy"> | **A-06** | Part 25 - Left Hand Central lever-1 | 90.00 × 12.00 | 3 | 2.28 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-06.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-06.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-07.png' | relative_url }}" alt="A-07" width="86" loading="lazy"> | **A-07** | — | 26.08 × 15.02 | 2 | 0.91 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-07.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-07.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-08.png' | relative_url }}" alt="A-08" width="86" loading="lazy"> | **A-08** | — | 47.84 × 21.58 | 1 | 1.39 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-08.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-08.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-09.png' | relative_url }}" alt="A-09" width="86" loading="lazy"> | **A-09** | — | 47.40 × 20.72 | 2 | 1.36 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-09.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-09.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-10.png' | relative_url }}" alt="A-10" width="86" loading="lazy"> | **A-10** | — | 103.38 × 15.70 | 7 | 3.25 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-10.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-10.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-11.png' | relative_url }}" alt="A-11" width="86" loading="lazy"> | **A-11** | — | 35.26 × 9.54 | 1 | 0.78 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-11.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-11.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-12.png' | relative_url }}" alt="A-12" width="86" loading="lazy"> | **A-12** | — | 8.00 × 3.00 | 0 | 0.07 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-12.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-12.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-13.png' | relative_url }}" alt="A-13" width="86" loading="lazy"> | **A-13** | — | 8.42 × 24.02 | 1 | 0.37 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-13.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-13.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-14.png' | relative_url }}" alt="A-14" width="86" loading="lazy"> | **A-14** | Part 22-2 | 25.68 × 25.44 | 2 | 0.77 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-14.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-14.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-15.png' | relative_url }}" alt="A-15" width="86" loading="lazy"> | **A-15** | — | 50.96 × 51.70 | 4 | 6.64 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-15.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-15.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-16.png' | relative_url }}" alt="A-16" width="86" loading="lazy"> | **A-16** | Part 10 - the Pig-1 | 54.20 × 34.60 | 1 | 3.06 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-16.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-16.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-17.png' | relative_url }}" alt="A-17" width="86" loading="lazy"> | **A-17** | — | 8.00 × 3.00 | 0 | 0.07 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-17.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-17.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-18.png' | relative_url }}" alt="A-18" width="86" loading="lazy"> | **A-18** | — | 31.40 × 24.80 | 3 | 1.37 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-18.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-18.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-19.png' | relative_url }}" alt="A-19" width="86" loading="lazy"> | **A-19** | — | 50.70 × 25.04 | 7 | 2.38 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-19.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-19.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-20.png' | relative_url }}" alt="A-20" width="86" loading="lazy"> | **A-20** | — | 12.00 × 56.90 | 4 | 1.20 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-20.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-20.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-21.png' | relative_url }}" alt="A-21" width="86" loading="lazy"> | **A-21** | — | 39.64 × 25.80 | 4 | 2.03 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-21.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-21.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-22.png' | relative_url }}" alt="A-22" width="86" loading="lazy"> | **A-22** | — | 35.04 × 29.74 | 4 | 1.61 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-22.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-22.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-23.png' | relative_url }}" alt="A-23" width="86" loading="lazy"> | **A-23** | Part 12 - Cradle Ends-1 | 19.00 × 51.70 | 1 | 2.21 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-23.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-23.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-24.png' | relative_url }}" alt="A-24" width="86" loading="lazy"> | **A-24** | Part 12 - Cradle Ends-2 | 19.00 × 51.70 | 3 | 2.43 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-24.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-24.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-25.png' | relative_url }}" alt="A-25" width="86" loading="lazy"> | **A-25** | — | 39.64 × 25.80 | 4 | 2.03 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-25.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-25.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/A-26.png' | relative_url }}" alt="A-26" width="86" loading="lazy"> | **A-26** | — | 36.60 × 24.98 | 5 | 1.33 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/A-26.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/A-26.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/B-01.png' | relative_url }}" alt="B-01" width="86" loading="lazy"> | **B-01** | — | 26.08 × 25.14 | 2 | 0.71 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/B-01.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/B-01.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/B-02.png' | relative_url }}" alt="B-02" width="86" loading="lazy"> | **B-02** | Part 20-2 | 32.76 × 25.14 | 4 | 1.17 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/B-02.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/B-02.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/B-03.png' | relative_url }}" alt="B-03" width="86" loading="lazy"> | **B-03** | — | 47.00 × 15.80 | 3 | 1.26 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/B-03.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/B-03.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/B-04.png' | relative_url }}" alt="B-04" width="86" loading="lazy"> | **B-04** | — | 90.70 × 145.00 | 9 | 28.99 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/B-04.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/B-04.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/B-05.png' | relative_url }}" alt="B-05" width="86" loading="lazy"> | **B-05** | Part 26 - Straight Lever-3 | 8.00 × 88.00 | 2 | 2.03 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/B-05.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/B-05.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/B-06.png' | relative_url }}" alt="B-06" width="86" loading="lazy"> | **B-06** | Part 26 - Straight Lever-2 | 8.00 × 88.00 | 2 | 2.03 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/B-06.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/B-06.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/B-07.png' | relative_url }}" alt="B-07" width="86" loading="lazy"> | **B-07** | Part 26 - Straight Lever-1 | 8.00 × 88.00 | 2 | 2.03 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/B-07.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/B-07.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/B-08.png' | relative_url }}" alt="B-08" width="86" loading="lazy"> | **B-08** | — | 15.80 × 93.90 | 5 | 3.21 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/B-08.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/B-08.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/B-09.png' | relative_url }}" alt="B-09" width="86" loading="lazy"> | **B-09** | — | 60.00 × 52.70 | 14 | 7.29 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/B-09.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/B-09.pdf' | relative_url }}) |
| <img src="{{ '/assets/brazos/laser/render/piezas/B-10.png' | relative_url }}" alt="B-10" width="86" loading="lazy"> | **B-10** | Part 05 - Rectangular Side Part-1 | 60.00 × 43.80 | 12 | 6.49 | [DXF]({{ '/assets/brazos/laser/piezas-dxf/B-10.dxf' | relative_url }}) · [Plano]({{ '/assets/brazos/laser/planos/B-10.pdf' | relative_url }}) |

### Cómo se generaron

Los planos y los renders se produjeron con scripts del repositorio, no a mano:

| Paso | Script |
|:-----|:-------|
| Separar los contornos de cada hoja | `tools/f3_piezas_dxf.py` |
| DXF, STL y render por pieza | `tools/f3_salidas_piezas.py` |
| Planos A4 y plano resumen | `tools/f3_planos.py` |

Dos decisiones que afectan la exactitud:

- Las curvas se aplanan con una **sagita de 0.02 mm** y los contornos se cierran redondeando a 0.02 mm. Eso está muy por debajo del ancho de corte del láser.
- En los DXF por pieza, los **agujeros redondos se escriben como círculos verdaderos**, no como polilíneas aplanadas, y con el diámetro nominal del diseño. Son archivos de corte: una circunferencia aplanada se cortaría poligonal.

---

## 5) Ensamble en CAD (R3)

El ensamble se armó en **Autodesk Inventor 2026** a partir de las piezas descargadas de GrabCAD y se exportó a STEP.

[![Ensamble abierto en Inventor 2026 con el árbol de componentes]({{ '/assets/img/brazos/laser/captura-inventor-mearm.webp' | relative_url }})]({{ '/assets/img/brazos/laser/captura-inventor-mearm.webp' | relative_url }})
**Figura 3:** `Final Assembly.iam` en Inventor 2026, con el árbol de componentes visible.

| Dato del STEP | Valor |
|:--------------|:------|
| Cuerpos | 65 |
| Placas de 3.00 mm | 31 |
| Piezas distintas | 24 (`Part 04` ×5, `Part 26` ×3, `Part 12` ×2) |
| Servos | 4 × SG90 |
| Envolvente | 264.1 × 95.2 × 156.8 mm |

- [Descargar el ensamble (STEP, 4.8 MB)]({{ '/assets/brazos/laser/cad/mearm-mdf-ensamble.step' | relative_url }})
- Los archivos `.SLDPRT` de las piezas **no se republican aquí** mientras no se confirme su licencia en GrabCAD. Están en la fuente original [[2](#referencias)].

### Archivos editables y de fabricación (B07)

| Archivo | Para qué sirve | Descarga |
|:--------|:---------------|:-------|
| Hojas DXF de corte (A y B) | Fabricación, tal como se mandaron a la máquina | [Sección 4](#4-piezas-planos-y-renders-r1-y-r2) |
| DXF por pieza (36) | Recortar o reponer una pieza suelta | [Tabla de piezas](#tabla-de-piezas) |
| STEP del ensamble | Edición e intercambio entre programas CAD | [Descarga]({{ '/assets/brazos/laser/cad/mearm-mdf-ensamble.step' | relative_url }}) |
| Planos en PDF | Verificación | [Plano completo]({{ '/assets/brazos/laser/planos/planos-mearm-completo.pdf' | relative_url }}) |
| Modelo original | Punto de partida del diseño | [GrabCAD](https://grabcad.com/library/675982) |

### ⚠️ El modelo 3D no es exactamente lo que se cortó

Se compararon las **31 placas de 3 mm del STEP** contra los **36 contornos de las hojas**, midiendo en planta con el rectángulo mínimo rotado y emparejando de forma óptima global:

| Diferencia máxima | Placas |
|:---|---:|
| ≤ 1.5 mm | 6 |
| 1.5 – 4 mm | 12 |
| > 4 mm | 13 |
| Contornos sin pareja | 5 (A-01, A-11, A-18, A-22, B-01) |

**Cómo leer la tabla:** el emparejamiento está obligado a asignar las 31 placas, así que una "pareja" de más de 4 mm quiere decir *no existe equivalente*, no que la pieza difiera en esa cantidad.

El caso más claro y verificable con un calibrador es **la base**: mide **145.00 × 95.00 mm en el STEP** y **145.00 × 90.70 mm en el contorno que se cortó** (pieza B-04). Son 4.3 mm.

> **Nota.** El ensamble 3D y los renders corresponden al **modelo de GrabCAD**. Los planos y los renders por pieza corresponden a **las piezas que se cortaron**. No son el mismo conjunto de geometría.

**Hipótesis** (sin confirmar): los `.SLDPRT` de GrabCAD son una variante del MeArm distinta de las hojas DXF v1.0.

---

## 6) Renderizado del ensamble (R4)

[![Render isométrico del ensamble]({{ '/assets/brazos/laser/render/ensamble-iso.png' | relative_url }}?v=2)]({{ '/assets/brazos/laser/render/ensamble-iso.png' | relative_url }}?v=2)
**Figura 4:** Vista isométrica. MDF en color madera, servos SG90 en azul.

[![Render lateral del ensamble]({{ '/assets/brazos/laser/render/ensamble-lateral.png' | relative_url }}?v=2)]({{ '/assets/brazos/laser/render/ensamble-lateral.png' | relative_url }}?v=2)
**Figura 5:** Vista lateral. Se aprecian los eslabones en paralelogramo del hombro y el codo.

[![Render superior del ensamble]({{ '/assets/brazos/laser/render/ensamble-superior.png' | relative_url }}?v=2)]({{ '/assets/brazos/laser/render/ensamble-superior.png' | relative_url }}?v=2)
**Figura 6:** Vista superior, con la pinza y su sector dentado.

---

## 7) Visor 3D (R5)

<div class="stl-viewer stl-viewer--tall" data-assembly="{{ '/assets/stl/brazo-laser/ensamble.json' | relative_url }}?v=2" data-base="{{ '/assets/stl/brazo-laser/' | relative_url }}"></div>

**Figura 7:** Ensamble interactivo. Usa **Separar piezas** para apartar los servos de la estructura.

Las 31 placas van en una sola malla y cada servo por separado, para que la leyenda sea legible y la separación muestre dónde se montan los actuadores. Las coordenadas son las del ensamble CAD, no aproximadas: la reconstrucción devuelve la envolvente exacta de 264.08 × 95.20 × 156.81 mm.

---

## 8) Fabricación: corte láser (R6)

### Configuración de corte

| Dato | Valor |
|:-----|:------|
| Material | MDF de **3 mm** |
| Hojas | 2 de 150 × 200 mm |
| Máquina | Cortadora láser de CO₂ de 40–60 W |
| Software | LightBurn |
| Importación de los DXF | Escala 1:1 en milímetros, sin compensación de kerf |
| Potencia de corte | **65 %** |
| Velocidad de corte | **15 mm/s** |
| Pasadas | **1** |
| Aire asistido | Encendido |
| Enfoque | Sobre la superficie del MDF |
| Orden de corte | Agujeros y contornos interiores primero, contorno exterior al final |
| Kerf | ≈0.15 mm |
| Diámetros de agujero | **Ø3.0 mm** (paso libre del M3) y **Ø2.65 mm** (el tornillo M3 rosca en el MDF) |

Son valores de referencia para MDF de 3 mm en láser de CO₂. Antes de cortar las hojas se corta un cuadro de prueba de 10 × 10 mm con un agujero de Ø3.0: la pieza debe caerse sola y el tornillo M3 debe pasar sin forzar.

> **Cambio de material respecto al diseño original.** El MeArm v1.0 está pensado para **acrílico de 3 mm** y aquí se cortó **MDF de 3 mm**. El MDF es más blando y más tolerante al apriete, pero se desgasta en los agujeros que giran; conviene revisar el juego en los pivotes después de las pruebas.

### Registro de corte por hoja (B09)

La longitud de corte se mide sobre los DXF; el tiempo se estima a 15 mm/s más un 30 % de desplazamientos en vacío.

| Hoja | Piezas | Longitud de corte | Agujeros Ø3.0 / Ø2.65 | Tiempo estimado |
|:-----|:------:|------------------:|:---------------------:|----------------:|
| A | 26 | 5.52 m | 27 / 14 | ≈8 min |
| B | 10 | 3.78 m | 16 / 22 | ≈5.5 min |
| **Total** | **36** | **9.30 m** | **43 / 36** | **≈13.5 min** |

| Ajuste | Motivo |
|:-------|:-------|
| Cortar interiores antes que el contorno | Si la pieza se suelta primero, se mueve y el agujero sale corrido |
| Retirar las piezas pequeñas (A-01 a A-04, A-12, A-17) con cuidado | Miden 3–8 mm y se pierden entre la rejilla de la cama |
| Limpiar el hollín con un trapo húmedo apenas exprimido | El MDF se mancha en los bordes; no mojarlo para que no se hinche |

---

## 9) Secuencia de ensamblaje (B10)

El armado sigue la **guía oficial de 13 pasos** del autor del MeArm [[3](#referencias)]; aquí se resume por etapas, con la tornillería y los cuidados de este brazo.

| Etapa | Qué se arma | Tornillería | Cuidado |
|:-----:|:------------|:------------|:--------|
| 1 | **Base**: placa base y laterales | M3 en los barrenos de Ø2.65 | Apretar sin pasarse: el MDF se barre |
| 2 | **Cuerpo giratorio**: servo de giro, plato y cuna de servos | 2 tornillos del SG90; cuerno en cruz con su tornillo | Servo de giro a 90° antes de montar el cuerno |
| 3 | **Hombro y codo**: los dos servos en la cuna y las palancas del paralelogramo | 4 tornillos del SG90; M3 como ejes de las palancas | Hombro y codo a 90°; los ejes no se aprietan a fondo |
| 4 | **Antebrazo**: eslabones que unen el codo con la muñeca | M3 como ejes | Comprobar que el paralelogramo se mueve sin trabarse |
| 5 | **Pinza**: servo de la pinza y mordazas | 2 tornillos del SG90; M3 como ejes de las mordazas | Servo a 80° (pinza abierta) al montar el cuerno |

### Piezas identificadas

| Pieza cortada | Nombre en el modelo CAD | Función |
|:--------------|:------------------------|:--------|
| B-04 | — | Placa base (145 × 90.7 mm) |
| B-10 | Part 05 - Rectangular Side Part | Lateral de la base |
| A-23, A-24 | Part 12 - Cradle Ends | Extremos de la cuna que sostiene los servos del hombro y el codo |
| A-06 | Part 25 - Left Hand Central lever | Palanca central del paralelogramo |
| B-05, B-06, B-07 | Part 26 - Straight Lever | Palancas rectas del brazo |

> **Antes de montar cada cuerno de servo:** llevar el servo a su ángulo de inicio con el botón **Inicio** de la app, igual que en el brazo impreso, para que cada articulación quede centrada en su recorrido. Basta con energizar la tarjeta: al arrancar, el firmware deja las cuatro articulaciones en su ángulo de inicio.

---

## 10) Brazo ensamblado (B11)

[![Brazo de corte láser ensamblado]({{ '/assets/brazos/laser/render/ensamble-iso.png' | relative_url }}?v=2)]({{ '/assets/brazos/laser/render/ensamble-iso.png' | relative_url }}?v=2)
**Figura 8:** Brazo de corte láser ensamblado (render del ensamble CAD): MDF en color madera y servos SG90 en azul.

| Elemento | Componentes | Función |
|:---------|:------------|:--------|
| Base | B-04, B-10 | Soporta el brazo y aloja el servo de giro |
| Cuerpo giratorio | A-23, A-24 y servo de giro | Gira sobre la base y sostiene los servos del hombro y el codo |
| Paralelogramo | A-06, B-05, B-06, B-07 | Mueven el brazo desde los servos de abajo y mantienen la pinza horizontal |
| Pinza | Servo de pinza y mordazas | Cierra sobre el objeto |
| Actuadores | 4 × SG90 | Giro, hombro, codo y pinza |

---

## 11) Pruebas mecánicas (B12)

Cada articulación se mueve de tope a tope desde la app, con SW2 en APP, o con su potenciómetro, con el brazo armado y la pinza vacía.

| Prueba | Procedimiento | Criterio de aceptación |
|:-------|:--------------|:-----------------------|
| Giro de la base | Base de 0° a 180° | Recorre 0–180° sin rozar la base |
| Hombro | Hombro de 40° a 140°, con el codo a 90° | El paralelogramo no se traba en ningún extremo |
| Codo | Codo de 40° a 140° | El paralelogramo no se traba en ningún extremo |
| Orientación de la pinza | Mover hombro y codo por todo su rango | La pinza se mantiene horizontal (±10°) |
| Apertura de la pinza | Botones **Abrir** (80°) y **Cerrar** (20°) de la app, o SW1 | Abierta: más ancha que la pelota; cerrada: las mordazas se tocan sin forzar el servo |
| Juego en los pivotes | Mover a mano cada eslabón con los servos detenidos | Juego menor a 1.5 mm en la punta de la pinza |
| Repetibilidad | Ir a 90°, 70°, 110°, 20° y volver con el botón **Inicio**, 5 veces | La punta vuelve al mismo punto con diferencia menor a 3 mm |

Los rangos son los límites programados para este brazo en `config.h`; son más cerrados que los del brazo impreso porque el paralelogramo se traba antes de llegar a los extremos del servo.

---

## 12) Lista de materiales (B06)

### Mecánica

| Componente | Material o modelo | Medidas | Cantidad | Precio ref. (MXN) |
|:-----------|:------------------|:--------|:--------:|------------------:|
| Piezas cortadas A-01 a B-10 | MDF de 3 mm | Ver la [tabla de piezas](#tabla-de-piezas) | 36 | — |
| Hoja de MDF | MDF de 3 mm | 150 × 200 mm | 2 | 20 |
| Tiempo de corte láser | — | ≈14 min | 1 | 70 |
| Servo SG90 | Micro servo 9 g, 1.8 kg·cm | 12.0 × 31.5 × 32.6 mm (envolvente del CAD) | 4 | 180 |
| Tornillo M3 | Acero, cabeza allen, de 6 a 20 mm | Uno por barreno de Ø2.65 mm | 36 | 36 |
| Tuerca de seguridad M3 | Con inserto de nylon | Para los ejes que giran | 10 | 10 |
| Tornillería del SG90 | Incluida con cada servo | M2 | 4 juegos | — |
| | | | **Total mecánico** | **≈316** |

### Electrónica

La misma tarjeta de control del brazo impreso: [lista completa]({{ '/brazos/electronica-programacion/' | relative_url }}#2-lista-de-materiales-b14), 23 componentes sin contar los servos. **Precio: [Pendiente]**, igual que en la lista electrónica.
<!-- PENDIENTE: precio de la tarjeta, con su fuente (pregunta 11) -->

---

## 13) Electrónica y programación (B13–B24)

Este brazo usa la [tarjeta de control con ESP32-C3]({{ '/brazos/electronica-programacion/' | relative_url }}) y el firmware común, compilado con `#define BRAZO BRAZO_LASER`. Diagrama de bloques, esquemático, PCB, código, diagramas de flujo e interfaces están en esa página.

### Conexión de los servos

| Conector | GPIO | Servo |
|:--------:|:----:|:------|
| J3 | 5 | Base (giro) |
| J4 | 6 | Hombro |
| J5 | 7 | Codo |
| J6 | 10 | Pinza |

Los cuatro conectores llevan el mismo orden. Vistos desde la cara de componentes, de izquierda a derecha: **señal** (cable naranja), **V+** (rojo) y **GND** (café). El pad **cuadrado**, el de la derecha, es el pin 1 y es GND.

### Mapeo de los controles

| Control | Señal | GPIO | Actúa sobre |
|:--------|:------|:----:|:------------|
| RV1 | Analógica, proporcional | 1 | Servo de la **base**, J3 |
| RV2 | Analógica, proporcional | 0 | Servo del **hombro**, J4 |
| RV3 | Analógica, proporcional | 3 | Servo del **codo**, J5 |
| SW1 | Digital, dos posiciones | 21 | Servo de la **pinza**, J6 |
| SW2 | Digital, dos posiciones | 20 | Elige el modo: MANUAL o APP |

**SW1 no lleva el servo de la pinza de extremo a extremo de su recorrido**: alterna entre **dos ángulos fijos**, **20°** (cerrada) y **80°** (abierta). Eso evita que el SG90 quede empujando contra el tope mecánico de la mordaza, que es lo que lo calienta y le hace consumir corriente sin estar moviéndose.

### Parámetros de este brazo en `config.h`

| Articulación | Mínimo | Máximo | Inicio |
|:-------------|:------:|:------:|:------:|
| Base | 0° | 180° | 90° |
| Hombro | 40° | 140° | 90° |
| Codo | 40° | 140° | 90° |
| Pinza | 20° (cerrada) | 80° (abierta) | 80° |

{: .warning }
> Estos límites son **provisionales**: son valores de diseño, no medidos con el brazo armado. Los de la pinza sobre todo, porque dependen de hasta dónde cierran las mordazas sin forzar el servo.
<!-- PENDIENTE: angulos reales de pinza abierta y cerrada de este brazo (pregunta 10) -->

| Dato | Valor |
|:-----|:------|
| Red Wi-Fi | `Brazo-Laser`, contraseña `brazo2026` |
| App | `http://192.168.4.1` |
| Velocidad máxima de cada articulación | 120 °/s |

---

## 14) Integración y pruebas (B25–B28)

### Integración física (B25)

| Elemento | Montaje |
|:---------|:--------|
| Tarjeta de control | Sobre una base de MDF junto al brazo, con los potenciómetros al frente. **Cómo se fijó: [Pendiente]** — la tarjeta v3 no tiene barrenos de montaje |
| Cables de servo | Los del hombro y el codo salen directo de la cuna; el de la pinza sube por el antebrazo con cinchos, con un bucle en cada articulación |
| Cable del servo de giro | Por debajo de la base hasta J3 |
| Alimentación | **Dos canales separados de la fuente**: el canal de lógica (5 a 5.5 V) a J1 y el de servos (5 a 6 V) a J2. Las tierras se unen en la tarjeta |
| USB | Solo para programar y para leer el diagnóstico |
<!-- PENDIENTE: como se fijo la tarjeta al brazo (pregunta 6) -->

[![Brazo de corte láser en vista lateral]({{ '/assets/brazos/laser/render/ensamble-lateral.png' | relative_url }}?v=2)]({{ '/assets/brazos/laser/render/ensamble-lateral.png' | relative_url }}?v=2)
**Figura 9:** Vista lateral con el paralelogramo del hombro y el codo.

### Electrónica y programa sobre el brazo (B26)

| Entrada | Acción esperada | Criterio de aceptación |
|:--------|:----------------|:-----------------------|
| RV1 de tope a tope | La base gira de 0° a 180° | Proporcional, sin saltos |
| RV2 de tope a tope | El hombro va de 40° a 140° | Sin trabar el paralelogramo |
| RV3 de tope a tope | El codo va de 40° a 140° | Sin trabar el paralelogramo |
| SW1 | La pinza alterna entre 20° y 80° | Un solo movimiento por cambio |
| SW2 a APP | Los potenciómetros dejan de mover el brazo | D2 pasa a parpadear |
| Deslizadores de la app, con SW2 en APP | Mueven la misma articulación | El encabezado de la app dice `app` |
| Deslizadores de la app, con SW2 en MANUAL | No mueven nada | La app muestra el aviso de cambiar el switch |
| SW2 de vuelta a MANUAL | El brazo va hacia donde estén las perillas | Sin saltos: tarda, no brinca |

### Modos de operación (B27)

| Modo | Cómo se accede | Qué se comprueba |
|:-----|:---------------|:-----------------|
| MANUAL | SW2 en MANUAL | RV1–RV3 y SW1 mueven el brazo; D2 encendido fijo |
| APP | SW2 en APP, conectarse a `Brazo-Laser` y abrir `http://192.168.4.1` | D2 parpadea: lento sin celular conectado, rápido con uno |

El USB **no es un modo de mando**: solo programa la tarjeta y, con la orden `D`, imprime el reporte de diagnóstico.

### Prueba funcional completa (B28)

**Tarea:** tomar la pelota roja de espuma, levantarla, girar la base y soltarla en otro punto, una vez en cada uno de los dos modos.

| Paso | Acción | Ángulos de referencia (base, hombro, codo, pinza) |
|:----:|:-------|:-------------------------------------------------|
| 1 | Posición de inicio | 90°, 90°, 90°, 80° (abierta) |
| 2 | Bajar sobre la pelota | 90°, 60°, 120°, 80° |
| 3 | Cerrar la pinza | 90°, 60°, 120°, 20° |
| 4 | Levantar | 90°, 100°, 90°, 20° |
| 5 | Girar la base | 150°, 100°, 90°, 20° |
| 6 | Bajar y soltar | 150°, 60°, 120°, 80° |
| 7 | Regresar al inicio | Botón **Inicio** de la app |

La secuencia se ejecuta desde la app con SW2 en APP, usando los ángulos de la tabla para que cada intento sea igual.

**Criterio de aceptación:** la pelota no se cae durante el traslado ni se deforma al cerrar la pinza, en **3 de 3 intentos** con cada modo de mando (MANUAL y APP).

---

## Referencias

1. Página de referencia del curso: <https://hubergiron.github.io/cnc/diseno-mecanico-cnc/>
2. *MeArm v1.0 robot arm*, GrabCAD: <https://grabcad.com/library/675982>
3. Benjamin Gray, *MeArm Robot Arm — Your Robot V1.0* (guía de armado, CC BY 4.0), Hackster: <https://www.hackster.io/benbobgray/mearm-robot-arm-your-robot-v1-0-326702>

---

## Sección anterior

[Brazo impreso en 3D]({{ '/brazos/impresion-3d/' | relative_url }})

## Siguiente sección

[Electrónica y programación]({{ '/brazos/electronica-programacion/' | relative_url }})
