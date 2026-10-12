---
layout: default
title: Autoevaluación
parent: Brazos robóticos
nav_order: 4
permalink: /brazos/evaluacion/
---

# Autoevaluación (rúbrica resumida)

Avance de la documentación de los brazos contra la **[evaluación resumida del curso](https://hubergiron.github.io/Integracion-mecatronica/evaluacion-resumida.html)**: 31 criterios ponderados a 100 puntos. En esa rúbrica **todos los criterios son obligatorios**: un criterio cumple solo si la evidencia existe, es verificable, está en este sitio y corresponde con el brazo físico que se presenta.

Como el proyecto pide **dos versiones**, aquí un criterio cuenta para el proyecto solo cuando **cumplen los dos brazos**.

{% assign total = 0 -%}
{%- assign logrado = 0 -%}
{%- assign en_parcial = 0 -%}
{%- assign n_cumple = 0 -%}
{%- assign n_parcial = 0 -%}
{%- assign n_falta = 0 -%}
{%- for s in site.data.evaluacion_brazos.secciones -%}
  {%- for c in s.criterios -%}
    {%- assign total = total | plus: c.peso -%}
    {%- assign estados = c.impreso | append: "," | append: c.laser -%}
    {%- if estados contains "falta" -%}
      {%- assign n_falta = n_falta | plus: 1 -%}
    {%- elsif estados contains "parcial" -%}
      {%- assign n_parcial = n_parcial | plus: 1 -%}
      {%- assign en_parcial = en_parcial | plus: c.peso -%}
    {%- else -%}
      {%- assign n_cumple = n_cumple | plus: 1 -%}
      {%- assign logrado = logrado | plus: c.peso -%}
    {%- endif -%}
  {%- endfor -%}
{%- endfor -%}
{%- assign potencial = logrado | plus: en_parcial %}

## Resumen

| | Criterios | Puntos |
|:--|:--:|:--:|
| ✅ Cumplen los dos brazos | {{ n_cumple }} | **{{ logrado }} / {{ total }}** |
| ⚠️ Con evidencia parcial | {{ n_parcial }} | {{ en_parcial }} |
| ❌ Sin evidencia en al menos un brazo | {{ n_falta }} | {{ total | minus: potencial }} |

**Calificación actual: {{ logrado }} / {{ total }}.** Si se completan los criterios parciales, sube a **{{ potencial }} / {{ total }}**. Casi todo lo que falta es **evidencia física** que solo el equipo puede producir: fotos, videos, mediciones, código y los archivos de la PCB.

> **Cómo actualizar esta página:** al subir una evidencia, cambiar el estado del criterio en `_data/evaluacion_brazos.yml` (`cumple`, `parcial`, `falta` o `na`). Los puntos se recalculan solos.

✅ cumple · ⚠️ parcial · ❌ falta · — no aplica

---

## Detalle por criterio

<div class="tabla-eval" markdown="1">
{% for s in site.data.evaluacion_brazos.secciones %}
### {{ s.titulo }}

| # | Criterio | Peso | Impreso | Láser | Qué falta |
|:--|:---------|:----:|:-------:|:-----:|:----------|
{% for c in s.criterios -%}
{%- capture ei -%}{% case c.impreso %}{% when "cumple" %}✅{% when "parcial" %}⚠️{% when "na" %}—{% else %}❌{% endcase %}{%- endcapture -%}
{%- capture el -%}{% case c.laser %}{% when "cumple" %}✅{% when "parcial" %}⚠️{% when "na" %}—{% else %}❌{% endcase %}{%- endcapture -%}
| **{{ c.id }}** | [{{ c.titulo }}]({{ c.evidencia | relative_url }}) | {{ c.peso }} | {{ ei }} | {{ el }} | {% if c.falta == "" %}Nada{% else %}{{ c.falta }}{% endif %} |
{% endfor %}
{% endfor %}
</div>

---

## Prioridades para cerrar la entrega

Ordenadas por puntos que desbloquean. Las tres primeras se resuelven en una sola sesión de laboratorio con los brazos armados.

| Prioridad | Qué hacer | Criterios | Puntos |
|:---------:|:----------|:----------|:------:|
| 1 | **Fotos de los dos brazos armados** y de la electrónica montada | B11, B17, B25 | 10 |
| 2 | **Videos**: cada articulación, cada modo de operación y la prueba con la pelota | B12, B27, B28 | 10 |
| 3 | **Medir y llenar las tablas**: rangos, apertura, voltajes, entradas contra acciones | B12, B18, B26 | 9 |
| 4 | **Publicar el código** (Arduino, `brazo_gui.py`, ESP32-C3) y documentar librerías y funciones | B22, B23, B24 | 11 |
| 5 | **Subir el proyecto de KiCad**: esquemático, PCB y Gerber | B15, B16 | 8 |
| 6 | **Parámetros de la cortadora láser** y registro de impresión por pieza | B09 | 3 |
| 7 | **Bocetos** y alternativas consideradas | B02, B03 | 6 |
| 8 | **Archivos de Inventor** del brazo impreso y tornillería | B06, B07, B10 | 11 |

Algunos criterios aparecen en dos filas: sus puntos cuentan cuando se completa todo lo que piden.

---

## Sección anterior

[Comparación y conclusiones]({{ '/brazos/comparacion/' | relative_url }})
