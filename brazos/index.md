---
layout: default
title: Brazos robóticos
nav_order: 4
has_children: true
has_toc: false
permalink: /brazos/
---

# Brazos robóticos

**Equipo de Integración Mecatrónica Otoño 2026**  
**Integrantes:** Juan Pablo Martha, Carlos Sebastián Ortega, Santiago Alejandro Velázquez

Contenido:
- [1. Proyecto y equipo](#descripción-del-proyecto) (esta página)
- [2. Brazo impreso en 3D]({{ '/brazos/impresion-3d/' | relative_url }})
- [3. Brazo cortado con láser]({{ '/brazos/corte-laser/' | relative_url }})

> Estado: **en elaboración**. El brazo de corte láser tiene documentados su diseño, sus 36 piezas y su ensamble 3D; le faltan los parámetros de corte y la evidencia física (fotos, video y pruebas). El brazo impreso en 3D tiene sus parámetros de impresión y sus piezas, y espera el STEP de su ensamble.

---

## Descripción del proyecto

Como proyecto de la clase de **Integración Mecatrónica Otoño 2026**, el equipo diseña y manufactura **dos brazos robóticos** con dos procesos de fabricación distintos:

- un brazo fabricado por **impresión 3D (FDM)** en PLA, y
- un brazo fabricado por **corte láser** a partir de placas.

El objetivo es documentar cada proceso de principio a fin (modelo, parámetros de fabricación, piezas y ensamble) y comparar los resultados.

### Brazos

| Brazo | Proceso | Diseño base | Control | Estado |
|:------|:--------|:------------|:--------|:-------|
| [Brazo impreso en 3D]({{ '/brazos/impresion-3d/' | relative_url }}) | Impresión 3D (FDM, PLA) | Printables #449747, de RACBOTS | Arduino Uno por USB | 8 piezas documentadas con visor 3D |
| [Brazo cortado con láser]({{ '/brazos/corte-laser/' | relative_url }}) | Corte láser (MDF 3 mm) | MeArm v1.0, de Benjamin Gray | PCB propia con ESP32-C3 | 36 piezas con plano, DXF y render; visor 3D |

> **Ninguno de los dos diseños es original del equipo.** Ambos parten de modelos publicados por terceros; el aporte propio es la fabricación, el ensamble, la electrónica y las pruebas. Cada página declara su autor, su fuente y su licencia.

### Estado de la rúbrica

| # | Entregable | Impreso 3D | Corte láser |
|:--|:-----------|:-----------|:------------|
| R1 | Planos de las piezas | ⏸ Falta el STEP del ensamble | ✅ 36 planos A4 + resumen de 38 páginas |
| R2 | Render de cada pieza | ⏸ | ✅ 36 renders |
| R3 | Ensamble en CAD | ⏸ El STEP exportado viene sin geometría | ✅ STEP y captura de Inventor |
| R4 | Render del ensamble | ⏸ | ✅ 3 vistas |
| R5 | Visor 3D en la página | ✅ Ensamble y 8 piezas, posiciones aproximadas | ✅ Coordenadas reales del CAD |
| R6 | Proceso de fabricación | ✅ Parámetros de impresión | ❌ Faltan parámetros de corte, fotos y video |
| R7 | Ensamble físico | ❌ Faltan fotos | ❌ Faltan fotos |
| R8 | Prueba tomando un objeto | ❌ Falta video | ❌ Falta video |

✅ hecho · ⏸ bloqueado por archivos · ❌ falta evidencia del equipo

### Visores 3D

Las páginas de cada brazo incluyen **visores 3D interactivos** de las piezas (archivos STL) y del ensamble:

- **Girar:** arrastrar con el ratón o con un dedo.
- **Acercar:** rueda del ratón o pellizco.
- **Desplazar:** clic derecho o dos dedos.
- **Reiniciar vista:** botón en la esquina de cada visor.

Cada pieza tiene además un enlace para **descargar su STL**.

---

## Siguiente sección

[Brazo impreso en 3D]({{ '/brazos/impresion-3d/' | relative_url }})
