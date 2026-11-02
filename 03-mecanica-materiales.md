---
layout: default
title: Mecánica y materiales
nav_order: 4
permalink: /03-mecanica-materiales/
stl_viewer: true
---

# Mecánica y materiales

Esta página documenta la **propuesta de materiales** para la suspensión y las ruedas del rover, y todo lo que hace falta para fabricarla: piezas, planos, lista de materiales, procedimiento y pruebas.

| Elemento | Material propuesto | Cómo se fabrica |
|:---------|:-------------------|:----------------|
| Eslabones de la suspensión (*links*) | **Tubo redondo de aluminio 6063**, Ø30 mm exterior × Ø27 mm interior (pared de 1.5 mm), tramos de 300 mm | Corte con segueta o tronzadora y barrenado de Ø4.2 mm |
| Uniones: codos, T, pivotes y terminales | **PETG** | Impresión 3D (FDM) |
| Rines | **PETG** | Impresión 3D (FDM) |
| Llantas | **Ecoflex 00-20** (silicón de curado platino, Smooth-On) | Colado sobre el rin dentro de un molde impreso |

{: .note }
> **Estado: propuesta de diseño.** Las piezas, el ensamble, los planos y los cálculos de esta página salen de un modelo paramétrico, todavía **no de piezas fabricadas**. Las fotos, mediciones y resultados de prueba se agregan conforme se construya. Los renders se marcan como renders.

Contenido:
- [1) Por qué estos materiales (B03)](#1-por-qué-estos-materiales-b03)
- [2) Arquitectura y dimensiones mecánicas (B05)](#2-arquitectura-y-dimensiones-mecánicas-b05)
- [3) Piezas: codos, uniones, rin y llanta (B07)](#3-piezas-codos-uniones-rin-y-llanta-b07)
- [4) Ensamble de la suspensión](#4-ensamble-de-la-suspensión)
- [5) Planos de fabricación (B08)](#5-planos-de-fabricación-b08)
- [6) Cálculos de verificación](#6-cálculos-de-verificación)
- [7) Lista de materiales mecánicos (B06)](#7-lista-de-materiales-mecánicos-b06)
- [8) Fabricación (B09)](#8-fabricación-b09)
- [9) Secuencia de ensamblaje (B10)](#9-secuencia-de-ensamblaje-b10)
- [10) Versión ensamblada (B11)](#10-versión-ensamblada-b11)
- [11) Pruebas mecánicas (B12)](#11-pruebas-mecánicas-b12)

---

## 1) Por qué estos materiales (B03)

### Eslabones

| Criterio (peso) | Tubo Al 6063 Ø30 × 1.5 | Eslabón impreso en PETG | Tubo de PVC hidráulico | Perfil de aluminio 20×20 |
|:----------------|:--:|:--:|:--:|:--:|
| Rigidez a flexión (30 %) | **5** | 2 | 2 | 5 |
| Masa por metro (20 %) | **4** (≈363 g/m) | 4 | 4 | 3 (≈500 g/m) |
| Facilidad de fabricación (20 %) | 4 | **5** | 4 | 4 |
| Pasar cables por dentro (15 %) | **5** (Ø27 libre) | 2 | 5 | 1 |
| Costo y disponibilidad (15 %) | 3 | **5** | 5 | 3 |
| **Total ponderado** | **4.30** | 3.45 | 3.70 | 3.50 |

Escala de 1 a 5. La calificación es **del equipo**, no una medición. El tubo gana porque la pieza más cargada de la suspensión trabaja a flexión, y un tubo es la sección más eficiente para eso: con 1.5 mm de pared y 30 mm de diámetro tiene un momento de inercia de **13 674 mm⁴** y pesa **109 g por cada tramo de 300 mm** ([cálculo](#6-cálculos-de-verificación)). Además, el interior hueco de Ø27 mm sirve como **ducto para los cables de los motores**.

### Uniones y rines: PETG en lugar de PLA

- **Temperatura:** el PETG se ablanda alrededor de 80 °C; el PLA, alrededor de 55–60 °C. Un rover en exteriores, con motores calientes junto a la abrazadera, está más cerca de lo segundo de lo que parece.
- **Tenacidad:** el PETG se deforma antes de romperse; el PLA es frágil al impacto, y las uniones reciben los golpes de la suspensión.
- **Fricción y desgaste:** el PETG tolera mejor los asientos de rodamiento a presión y las uniones atornilladas.

### Llantas: Ecoflex 00-20

| Opción | A favor | En contra |
|:-------|:--------|:----------|
| **Ecoflex 00-20 colado sobre el rin** | Máximo agarre en arena y roca; se cuela en la forma exacta del molde, con tacos incluidos; mezcla sencilla **1A:1B por volumen** | Muy blando (dureza Shore 00-20): los tacos pueden doblarse bajo carga. No se adhiere al PETG, así que la llanta se **traba mecánicamente** |
| Llanta impresa en TPU | Una sola pieza, sin molde | Menos agarre; tiempos de impresión largos |
| Rueda rígida de PETG con tacos | La más ligera y barata | Poco agarre en superficies lisas; no amortigua |
| Llanta comercial de hule | Probada | Diámetros y bujes que no coinciden con el motor; tacos fijos |

{: .warning }
> **Riesgo identificado: dureza.** Shore 00-20 es un silicón muy blando, pensado para piel y prótesis. Con ≈2 kg por rueda (12.5 kg entre 6), los tacos de 8 mm pueden doblarse en lugar de clavarse en la arena. La prueba **P-5** ([sección 11](#11-pruebas-mecánicas-b12)) decide si se queda o si se cambia por un silicón más duro de la misma familia (por ejemplo **Ecoflex 00-50** o **Dragon Skin 10**), que usa **el mismo molde** y el mismo procedimiento.

---

## 2) Arquitectura y dimensiones mecánicas (B05)

![Boceto de concepto del rover con la propuesta de materiales]({{ '/assets/img/rover/mecanica/boceto-rover.png' | relative_url }})
**Figura 1:** Boceto de concepto. La suspensión está **a escala**, con las cotas del modelo paramétrico; el cuerpo, el mástil y el brazo son volúmenes de concepto.

La suspensión es un **balancín-bogie** (*rocker-bogie*) de 6 ruedas, consistente con los **6 motores** y las **4 ruedas de esquina con dirección** del [diagrama eléctrico v2]({{ '/02-diagramas-a-bloques/' | relative_url }}):

- El **balancín** (*rocker*) gira sobre un eje M8 fijo al cuerpo. Su pata delantera lleva la rueda delantera; su pata trasera lleva el pivote del bogie.
- El **bogie** gira sobre un eje M8 al final del balancín y lleva la rueda media y la trasera.
- Cada pivote lleva **2 rodamientos 608** (8 × 22 × 7 mm).
- Todas las patas abren a **50° de la vertical**, así que las dos piezas de pivote son **la misma pieza**.

| Cota (un lado) | Valor | Métrica relacionada |
|:---------------|:------|:--------------------|
| Diámetro de rueda con tacos | **152 mm** | 22 · diámetro ≥13 cm (ideal ≥16) ✅ |
| Ancho de banda de rodadura | **64 mm** | 23 · ≥40 mm (ideal ≥60) ✅ |
| Altura de taco (*grouser*) | **8 mm**, 16 tacos | 24 · ≥6 mm (ideal ≥10) ✅ |
| Distancia entre ejes, delantera a trasera | **533 mm** | 11 · envolvente ≤100 cm ✅ |
| Largo total de la suspensión | **685 mm** | 11 · envolvente ≤100 cm ✅ |
| Altura del pivote del balancín | **300 mm** sobre el suelo | Libra el obstáculo de la métrica 15 (≥8 cm) por geometría |
| Separación entre ruedas, delantera a media / media a trasera | 230 mm / 303 mm | |

El ancho de vía depende del cuerpo, que todavía no tiene medidas, así que no se declara aquí.

---

## 3) Piezas: codos, uniones, rin y llanta (B07)

Todas las uniones comparten **el mismo casquillo**: barreno de **Ø30.4 mm** (0.4 mm de holgura sobre el tubo), pared de **4 mm**, **35 mm** de profundidad, y un **tornillo M4 pasante** que cruza casquillo y tubo, con la tuerca alojada en una caja hexagonal. El tubo entra hasta un tope a 21 mm del centro de la unión, y el centro está hueco (**Ø16 mm**) para que los cables pasen de un tubo a otro sin salir.

Arrastra para girar, rueda para acercar. Cada visor tiene su enlace de descarga.

### Codos y uniones

<div class="stl-grid">
  <figure>
    <div class="stl-viewer" data-stl="{{ '/assets/stl/rover/uniones/codo-90.stl' | relative_url }}" data-color="#E00034"></div>
    <figcaption><strong>Codo 90°</strong>: esquinas del marco del cuerpo · <a href="{{ '/assets/stl/rover/uniones/codo-90.stl' | relative_url }}" download>STL</a></figcaption>
  </figure>
  <figure>
    <div class="stl-viewer" data-stl="{{ '/assets/stl/rover/uniones/codo-120.stl' | relative_url }}" data-color="#E00034"></div>
    <figcaption><strong>Codo 120°</strong>: balancín sin pivote o mástil inclinado · <a href="{{ '/assets/stl/rover/uniones/codo-120.stl' | relative_url }}" download>STL</a></figcaption>
  </figure>
  <figure>
    <div class="stl-viewer" data-stl="{{ '/assets/stl/rover/uniones/union-t.stl' | relative_url }}" data-color="#E00034"></div>
    <figcaption><strong>Unión T</strong>: travesaños del marco · <a href="{{ '/assets/stl/rover/uniones/union-t.stl' | relative_url }}" download>STL</a></figcaption>
  </figure>
  <figure>
    <div class="stl-viewer" data-stl="{{ '/assets/stl/rover/uniones/cople-recto.stl' | relative_url }}" data-color="#E00034"></div>
    <figcaption><strong>Cople recto</strong>: para eslabones de más de 300 mm · <a href="{{ '/assets/stl/rover/uniones/cople-recto.stl' | relative_url }}" download>STL</a></figcaption>
  </figure>
  <figure>
    <div class="stl-viewer" data-stl="{{ '/assets/stl/rover/uniones/pivote.stl' | relative_url }}" data-color="#E00034"></div>
    <figcaption><strong>Pivote</strong>: vértice del balancín y del bogie, 2 × 608 · <a href="{{ '/assets/stl/rover/uniones/pivote.stl' | relative_url }}" download>STL</a></figcaption>
  </figure>
  <figure>
    <div class="stl-viewer" data-stl="{{ '/assets/stl/rover/uniones/terminal-eje.stl' | relative_url }}" data-color="#E00034"></div>
    <figcaption><strong>Terminal de eje</strong>: final del balancín, eje M8 del bogie · <a href="{{ '/assets/stl/rover/uniones/terminal-eje.stl' | relative_url }}" download>STL</a></figcaption>
  </figure>
  <figure>
    <div class="stl-viewer" data-stl="{{ '/assets/stl/rover/uniones/terminal-motor.stl' | relative_url }}" data-color="#E00034"></div>
    <figcaption><strong>Terminal de motor</strong>: abrazadera Ø37 con cierre M3 · <a href="{{ '/assets/stl/rover/uniones/terminal-motor.stl' | relative_url }}" download>STL</a></figcaption>
  </figure>
  <figure>
    <div class="stl-viewer" data-stl="{{ '/assets/stl/rover/uniones/probeta-ajuste.stl' | relative_url }}" data-color="#E00034"></div>
    <figcaption><strong>Probeta de ajuste</strong>: anillos de Ø30.2 / 30.4 / 30.6 · <a href="{{ '/assets/stl/rover/uniones/probeta-ajuste.stl' | relative_url }}" download>STL</a></figcaption>
  </figure>
</div>

**Detalles de diseño que no se ven a primera vista:**

- **Pivote.** Los cables **no pueden cruzar el eje que gira**, así que el pivote no tiene el canal central: cada casquillo tiene un **ojal de Ø10 mm** arriba, junto al tope del tubo, para sacar los cables y dejar un bucle flojo que acompañe el giro.
- **Terminal de motor.** Supone un motorreductor de **cuerpo Ø37 mm** (tipo JGB37, el más común a 12 V con ese par). La abrazadera puede tomar el motor en cualquier punto de su cuerpo; así las 3 ruedas de un lado quedan **en la misma vía**, aunque el balancín y el bogie estén en planos distintos. Si el motor elegido mide distinto, se cambia `R_MOTOR` en el script y se regenera.
- **Probeta de ajuste.** Se imprime **antes** que todo lo demás, con el mismo carrete y los mismos parámetros. Los anillos llevan 1, 2 y 3 muescas para distinguirlos. El que entre en el tubo **con presión ligera de la mano** define la holgura real; si no es el de 0.4 mm, se cambia `HOLGURA` y se regeneran las piezas.

### Rin, llanta y molde

<div class="stl-grid">
  <figure>
    <div class="stl-viewer" data-stl="{{ '/assets/stl/rover/rueda/rin.stl' | relative_url }}" data-color="#1D4ED8"></div>
    <figcaption><strong>Rin (PETG)</strong>: flecha de 6 mm en D + prisionero M3 · <a href="{{ '/assets/stl/rover/rueda/rin.stl' | relative_url }}" download>STL</a></figcaption>
  </figure>
  <figure>
    <div class="stl-viewer" data-stl="{{ '/assets/stl/rover/rueda/llanta-ecoflex.stl' | relative_url }}" data-color="#1F2937"></div>
    <figcaption><strong>Llanta (Ecoflex 00-20)</strong>: referencia, no se imprime · <a href="{{ '/assets/stl/rover/rueda/llanta-ecoflex.stl' | relative_url }}" download>STL</a></figcaption>
  </figure>
  <figure>
    <div class="stl-viewer" data-stl="{{ '/assets/stl/rover/rueda/molde-llanta-mitad.stl' | relative_url }}" data-color="#F59E0B"></div>
    <figcaption><strong>Medio molde (PETG)</strong>: se imprimen 2 iguales · <a href="{{ '/assets/stl/rover/rueda/molde-llanta-mitad.stl' | relative_url }}" download>STL</a></figcaption>
  </figure>
</div>

**Cómo se traba la llanta.** El silicón de platino **no se pega al PETG**, así que la unión es mecánica:

- **16 costillas** de 4 × 4 mm a lo largo del núcleo del rin transmiten el par: la llanta no puede girar sobre el rin.
- Las **pestañas** de Ø130 mm a cada lado quedan envueltas por el silicón y evitan que la llanta se salga de lado.
- El **molde** usa el propio rin como núcleo: el rin se apoya en el piso del molde, se cierran las dos mitades con 4 tornillos M4 y se vierte por arriba. Las dos mitades son idénticas (simetría de 180°), así que se imprime **una sola pieza dos veces**, y el mismo molde sirve para las 6 llantas.

### Archivos editables y de fabricación

| Archivo | Para qué sirve |
|:--------|:---------------|
| [`tools/r1_uniones_rover.py`](https://github.com/sebastiux/portafolio-just-the-docs/blob/main/tools/r1_uniones_rover.py) | **Modelo paramétrico** de todas las piezas. Las medidas del tubo, la holgura, la pared, el ángulo de las patas y el motor son constantes al inicio del archivo |
| [`tools/r2_renders_planos_rover.py`](https://github.com/sebastiux/portafolio-just-the-docs/blob/main/tools/r2_renders_planos_rover.py) | Renders y planos de corte |
| [`tools/r3_ensamble_rover.py`](https://github.com/sebastiux/portafolio-just-the-docs/blob/main/tools/r3_ensamble_rover.py) | Render del ensamble y secuencia de armado |
| [`datos.json`]({{ '/assets/stl/rover/datos.json' | relative_url }}) | Volumen, masa, envolvente y estanqueidad de cada pieza, y cotas del ensamble |
| STL de cada pieza | Enlaces de descarga bajo cada visor. **Todas son mallas cerradas** (estancas), listas para laminar |

---

## 4) Ensamble de la suspensión

<div class="stl-viewer stl-viewer--tall" data-assembly="{{ '/assets/stl/rover/ensamble/suspension-lado.json' | relative_url }}" data-base="{{ '/assets/stl/rover/ensamble/' | relative_url }}"></div>

**Figura 2:** Un lado de la suspensión, interactivo: balancín (rojo), bogie (ámbar), tubos de aluminio, motores de referencia, rines y llantas. Usa **Separar piezas** para la vista explosionada. El otro lado es el espejo.

[![Render isométrico del ensamble de un lado de la suspensión]({{ '/assets/img/rover/mecanica/ensamble-iso.png' | relative_url }})]({{ '/assets/img/rover/mecanica/ensamble-iso.png' | relative_url }})
**Figura 3:** Render isométrico del ensamble (modelo, no foto).

[![Render lateral del ensamble de un lado de la suspensión]({{ '/assets/img/rover/mecanica/ensamble-lateral.png' | relative_url }})]({{ '/assets/img/rover/mecanica/ensamble-lateral.png' | relative_url }})
**Figura 4:** Vista lateral. Se distinguen el balancín (pivote rojo), el bogie (pivote ámbar) y las tres ruedas en la misma vía.

---

## 5) Planos de fabricación (B08)

Cada plano muestra el **corte por el plano medio** de la pieza (donde se ven el barreno, el tope del tubo, el canal de cables y los asientos de rodamiento) y una tabla con las cotas que la definen. Las cotas salen de las mismas constantes que generan el STL, así que no pueden contradecirse. Haz clic para ampliar.

<div class="pasos">
  <figure><a href="{{ '/assets/img/rover/mecanica/plano-codo-90.png' | relative_url }}"><img src="{{ '/assets/img/rover/mecanica/plano-codo-90.png' | relative_url }}" alt="Plano del codo de 90 grados" loading="lazy"></a><figcaption><strong>Codo 90°</strong></figcaption></figure>
  <figure><a href="{{ '/assets/img/rover/mecanica/plano-codo-120.png' | relative_url }}"><img src="{{ '/assets/img/rover/mecanica/plano-codo-120.png' | relative_url }}" alt="Plano del codo de 120 grados" loading="lazy"></a><figcaption><strong>Codo 120°</strong></figcaption></figure>
  <figure><a href="{{ '/assets/img/rover/mecanica/plano-union-t.png' | relative_url }}"><img src="{{ '/assets/img/rover/mecanica/plano-union-t.png' | relative_url }}" alt="Plano de la unión T" loading="lazy"></a><figcaption><strong>Unión T</strong></figcaption></figure>
  <figure><a href="{{ '/assets/img/rover/mecanica/plano-cople-recto.png' | relative_url }}"><img src="{{ '/assets/img/rover/mecanica/plano-cople-recto.png' | relative_url }}" alt="Plano del cople recto" loading="lazy"></a><figcaption><strong>Cople recto</strong></figcaption></figure>
  <figure><a href="{{ '/assets/img/rover/mecanica/plano-pivote.png' | relative_url }}"><img src="{{ '/assets/img/rover/mecanica/plano-pivote.png' | relative_url }}" alt="Plano del pivote" loading="lazy"></a><figcaption><strong>Pivote</strong></figcaption></figure>
  <figure><a href="{{ '/assets/img/rover/mecanica/plano-terminal-eje.png' | relative_url }}"><img src="{{ '/assets/img/rover/mecanica/plano-terminal-eje.png' | relative_url }}" alt="Plano del terminal de eje" loading="lazy"></a><figcaption><strong>Terminal de eje</strong></figcaption></figure>
  <figure><a href="{{ '/assets/img/rover/mecanica/plano-terminal-motor.png' | relative_url }}"><img src="{{ '/assets/img/rover/mecanica/plano-terminal-motor.png' | relative_url }}" alt="Plano del terminal de motor" loading="lazy"></a><figcaption><strong>Terminal de motor</strong></figcaption></figure>
  <figure><a href="{{ '/assets/img/rover/mecanica/plano-rin.png' | relative_url }}"><img src="{{ '/assets/img/rover/mecanica/plano-rin.png' | relative_url }}" alt="Plano del rin" loading="lazy"></a><figcaption><strong>Rin</strong></figcaption></figure>
  <figure><a href="{{ '/assets/img/rover/mecanica/plano-llanta-ecoflex.png' | relative_url }}"><img src="{{ '/assets/img/rover/mecanica/plano-llanta-ecoflex.png' | relative_url }}" alt="Plano de la llanta" loading="lazy"></a><figcaption><strong>Llanta</strong></figcaption></figure>
</div>

**Corte de los tubos.** Los tramos se cortan a escuadra, se les quita la rebaba por dentro y por fuera (por dentro pasan cables) y se barrenan con **broca de 4.2 mm** usando la propia unión impresa como **plantilla de barrenado**, a 17.5 mm del extremo (la mitad de la profundidad del casquillo).

| Tramo | Largo | Cantidad (rover completo) |
|:------|------:|--:|
| Pata delantera del balancín | 300 mm (barra entera) | 2 |
| Pata trasera del balancín | 115 mm | 2 |
| Pata del bogie | 150 mm | 4 |

---

## 6) Cálculos de verificación

Cálculo de escritorio, para saber si la propuesta es razonable **antes** de comprar. No sustituye la prueba P-3.

**Sección del tubo** (Ø30 × Ø27):

| Propiedad | Fórmula | Valor |
|:----------|:--------|------:|
| Área | π/4 · (30² − 27²) | 134.3 mm² |
| Momento de inercia | π/64 · (30⁴ − 27⁴) | 13 674 mm⁴ |
| Módulo de sección | I / 15 | 911.6 mm³ |
| Masa por tramo de 300 mm | 134.3 mm² · 300 mm · 2.70 g/cm³ | 108.8 g |

**Caso de carga:** rover de **12.5 kg** (la masa con la que se dimensionó la tracción) repartido en 6 ruedas, con **factor dinámico de 2** por golpes: **F = 12.5 · 9.81 / 6 · 2 = 40.9 N** por rueda, aplicada de lado en la punta de la pata más larga (la delantera del balancín, **347.7 mm** de centro a centro).

| Verificación | Resultado | Contra qué |
|:-------------|----------:|:-----------|
| Esfuerzo en el tubo: M = 40.9 N · 347.7 mm = 14.2 N·m → σ = M / W | **15.6 MPa** | Fluencia del 6063: ≈145 MPa en temple T5, ≈48 MPa recocido (O). El anuncio **no dice el temple**; aun en el peor caso el factor de seguridad es **3.1** |
| Deflexión lateral: δ = F·L³ / (3·E·I), con E = 69 GPa | **0.61 mm** | Despreciable a escala de la rueda |
| Esfuerzo en el casquillo de PETG (Ø38.4 × Ø30.4, W = 3 375 mm³) | **4.2 MPa** | Resistencia entre capas del PETG impreso, del orden de 20–30 MPa |
| Flexión por el par de bloqueo del motor (6.5 N·m, métrica 19) en el tubo / en el casquillo | **7.1 / 1.9 MPa** | Mismas referencias |

**Conclusión:** el tubo está **sobrado** en resistencia; el eslabón débil son las **uniones de PETG** y, sobre todo, **la abrazadera del motor**: 6.5 N·m de par de bloqueo pueden hacer girar el motor dentro de la abrazadera si solo la sujeta la fricción. Por eso la prueba P-4 lo revisa, y si falla, la solución es atornillar la cara del motor (los JGB37 traen barrenos M3) a una brida en lugar de solo abrazarlo.

---

## 7) Lista de materiales mecánicos (B06)

Para la suspensión y las ruedas del **rover completo** (dos lados). Las masas de PETG son de la pieza **100 % sólida**, es decir, un **techo**: con 4 perímetros y 40 % de relleno, la pieza real pesa menos.

### Material

| Material | Uso | Cantidad | Precio unitario | Subtotal |
|:---------|:----|:--|--:|--:|
| Tubo redondo Al 6063, OD 30 × ID 27 mm, 300 mm | Eslabones | **5 barras** | $378.49 MXN | **$1,892.45 MXN** |
| Filamento PETG | Uniones y rines | ≤1.9 kg de pieza; ≈2.5 kg con soportes, purgas y la probeta | Por cotizar | |
| Ecoflex 00-20 (A + B) | Llantas | ≈1.26 kg de mezcla para 6 llantas; **≈1.4 kg** con 10 % de merma | Por cotizar | |
| Desmoldante (por ejemplo, Ease Release 200) | Molde | 1 | Por cotizar | |

**De dónde salen las 5 barras.** Por lado se necesitan 300 + 115 + 150 + 150 mm. Una barra entera va a la pata delantera; otra da 150 + 115 mm; y una tercera da las dos patas de 150 que sobran de los dos lados. Sobran 2 × 35 mm.

{: .warning }
> **Precio y disponibilidad del tubo.** El precio de $378.49 MXN (IVA incluido) es del anuncio de Mercado Libre que consultó el equipo, para **un tramo de 300 mm**, y el anuncio marcaba **"últimas 2 unidades"**. Para comprar las 5 barras hay que confirmar existencias o buscar el mismo tubo en tramos largos, que suelen salir más baratos por metro.

### Piezas impresas

| Pieza | STL | Cantidad | Masa sólida c/u | Total |
|:------|:----|:--:|--:|--:|
| Pivote (balancín y bogie) | `pivote.stl` | 4 | 103.5 g | 414 g |
| Terminal de eje | `terminal-eje.stl` | 2 | 43.2 g | 86 g |
| Terminal de motor | `terminal-motor.stl` | 6 | 58.1 g | 349 g |
| Rin | `rin.stl` | 6 | 174.1 g | 1 045 g |
| Medio molde de llanta | `molde-llanta-mitad.stl` | 2 | 271.0 g | 542 g |
| Probeta de ajuste | `probeta-ajuste.stl` | 1 | 14.2 g | 14 g |
| Codo 90° / unión T (marco del cuerpo) | `codo-90.stl` / `union-t.stl` | Según el diseño del cuerpo | 86.6 / 110.7 g | |

### Tornillería y componentes

| Componente | Uso | Cantidad |
|:-----------|:----|:--:|
| Tornillo M4 × 45 + tuerca M4 | Uno por casquillo (8 en pivotes, 2 en terminales de eje, 6 en terminales de motor) | 16 |
| Tornillo M3 × 16 + tuerca M3 | Cierre de las abrazaderas de motor | 12 |
| Prisionero M3 × 6 | Rin a flecha del motor | 6 |
| Rodamiento 608 (8 × 22 × 7 mm) | Pivotes | 8 |
| Tornillo M8 × 80 + tuerca de seguridad + rondanas | Eje balancín–cuerpo | 2 |
| Tornillo M8 × 90 + tuerca de seguridad + separador de 10 mm | Eje balancín–bogie | 2 |
| Tornillo M4 × 20 + tuerca | Cierre del molde | 4 |

### Presupuesto de masa

| Grupo | Masa |
|:------|-----:|
| Tubos cortados (1 430 mm en total) | 0.52 kg |
| PETG de suspensión y rines (techo, 100 % sólido) | 1.89 kg |
| Llantas de Ecoflex | 1.26 kg |
| **Suspensión + ruedas, sin motores ni tornillería** | **≤3.67 kg** |

Contra el objetivo de **<12 kg** del rover completo (métrica 12), las ruedas son lo que más pesa de esta propuesta: **384 g cada una**. Si el presupuesto de masa no cierra, lo primero es aligerar el rin (menos relleno, más ventanas) y adelgazar la banda de la llanta.

---

## 8) Fabricación (B09)

### Impresión de PETG

| Parámetro | Valor | Por qué |
|:----------|:------|:--------|
| Boquilla / cama | 235–245 °C / 75–85 °C | Rango típico del PETG; ajustar a la ficha del carrete |
| Ventilador de capa | 30–50 % | Más ventilador baja la adhesión entre capas, que es lo que carga el casquillo |
| Altura de capa | 0.2 mm | |
| Perímetros | **4** (1.6 mm con boquilla de 0.4) | El casquillo de 4 mm queda casi sólido en paredes |
| Relleno | 40 % giroide | |
| Orientación de codos, T y pivotes | **Acostados**: el plano de los casquillos paralelo a la cama | Las capas quedan a lo largo del casquillo; la flexión no las separa. Requiere soporte dentro de los barrenos horizontales |
| Orientación del rin | Con la cara del alma sobre la cama | Sin soportes |
| Orientación de terminales | Casquillo vertical | Sin soportes salvo en la abrazadera |
| Superficie de cama | PEI texturizado o con pegamento en barra | El PETG se pega demasiado al PEI liso y puede arrancarlo |

### Colado de las llantas (Ecoflex 00-20)

1. **Preparar el molde.** Aplicar desmoldante en el interior de las dos mitades. **No** aplicarlo en el rin: ahí se busca agarre.
2. **Armar.** Apoyar el rin en el piso del molde, cerrar las dos mitades alrededor y apretar los 4 tornillos M4. Sellar la línea de partición con plastilina si hay rendija.
3. **Mezclar.** Partes **A y B en proporción 1:1 por volumen**, revolviendo raspando paredes y fondo del recipiente. Si hay cámara de vacío, desgasificar.
4. **Verter** en un hilo delgado desde un solo punto, para que el aire salga por delante del silicón, hasta llenar la cara superior.
5. **Curar** a temperatura ambiente sin mover el molde. El tiempo de trabajo y de curado se toman de la **ficha técnica del lote** (en el orden de 30 minutos de trabajo y 4 horas de curado para el 00-20).
6. **Desmoldar** abriendo las dos mitades. Recortar la rebaba de la línea de partición.

{: .note }
> **Inhibición del curado.** Los silicones de platino pueden **no curar** al contacto con azufre, estaño, látex y algunos plásticos. Antes de colar la primera llanta, se hace una **prueba de 10 g** sobre un recorte impreso con el mismo PETG (prueba P-6). Tampoco se usan guantes de látex: nitrilo.

### Registro de fabricación por pieza

Cada pieza se anota aquí al fabricarse: fecha, carrete o lote, tiempo real, masa real y defectos.

| Pieza | Cantidad | Material | Estado |
|:------|:--:|:---------|:-------|
| Probeta de ajuste | 1 | PETG | Por imprimir (primera) |
| Pivote | 4 | PETG | Por imprimir |
| Terminal de eje | 2 | PETG | Por imprimir |
| Terminal de motor | 6 | PETG | Por imprimir |
| Rin | 6 | PETG | Por imprimir |
| Medio molde | 2 | PETG | Por imprimir |
| Llanta | 6 | Ecoflex 00-20 | Por colar (después de P-6) |
| Tubos | 8 tramos | Al 6063 | Por cortar |

---

## 9) Secuencia de ensamblaje (B10)

Para un lado; el otro es el espejo. En cada imagen, lo gris ya está montado y lo de color se agrega en ese paso.

<div class="pasos">
  <figure>
    <img src="{{ '/assets/img/rover/mecanica/secuencia/paso-01.png' | relative_url }}" alt="Paso 1: ruedas" loading="lazy">
    <figcaption><strong>1.</strong> <strong>Ruedas:</strong> colar la llanta sobre cada rin (sección 8) y dejar curar.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/assets/img/rover/mecanica/secuencia/paso-02.png' | relative_url }}" alt="Paso 2: motores y terminales" loading="lazy">
    <figcaption><strong>2.</strong> <strong>Motores:</strong> meter cada motor en su terminal, montar la rueda en la flecha con el prisionero M3, alinear la vía y cerrar la abrazadera con 2 × M3.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/assets/img/rover/mecanica/secuencia/paso-03.png' | relative_url }}" alt="Paso 3: bogie" loading="lazy">
    <figcaption><strong>3.</strong> <strong>Bogie:</strong> prensar 2 rodamientos 608 en el pivote, insertar las 2 patas de 150 mm y sus terminales de motor, pasar los cables por dentro de los tubos y fijar cada casquillo con M4.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/assets/img/rover/mecanica/secuencia/paso-04.png' | relative_url }}" alt="Paso 4: balancín" loading="lazy">
    <figcaption><strong>4.</strong> <strong>Balancín:</strong> pivote con sus 2 × 608, tubo de 300 mm al frente y de 115 mm atrás con el terminal de eje. Unir el bogie con el eje M8 × 90 y el separador, y el balancín al cuerpo con el M8 × 80.</figcaption>
  </figure>
</div>

**Pares de apriete.** Los M4 de los casquillos se aprietan **solo hasta que el tubo no gire**: si se aprietan de más, aplastan el PETG y el tubo de 1.5 mm de pared. Las tuercas de los ejes M8 son de seguridad (con nylon) y se dejan **sin juego axial pero con giro libre**.

---

## 10) Versión ensamblada (B11)

Por ahora existe **solo el ensamble virtual** (figuras 2 a 4). La evidencia física se agrega aquí al armar el primer lado:

- Foto de un lado completo, de frente y de perfil.
- Foto de un casquillo con su tornillo M4 y del pivote con sus rodamientos.
- Masa real de un lado, para compararla con el presupuesto de masa de la sección 7.

---

## 11) Pruebas mecánicas (B12)

Cada prueba está ligada a una métrica de las [especificaciones]({{ '/01-especificaciones/' | relative_url }}) y tiene un criterio de aceptación fijado **antes** de hacerla.

| # | Prueba | Procedimiento | Criterio de aceptación | Métrica |
|:-:|:-------|:--------------|:-----------------------|:--:|
| P-1 | Ajuste del casquillo | Probeta de ajuste en un tramo de tubo | Un anillo entra con presión de la mano, sin juego radial perceptible | — |
| P-2 | Extracción del casquillo | Colgar peso del tubo con la unión fija y el M4 puesto | ≥20 kg sin deslizamiento ni fisuras | 12 |
| P-3 | Flexión de una pata | Pata delantera empotrada, carga lateral de 4.2 kg (≈41 N) en la punta | Deflexión ≤2 mm y sin deformación permanente | 13, 14 |
| P-4 | Par en la abrazadera | Rueda bloqueada, motor a par de bloqueo durante 3 s | El motor no gira dentro de la abrazadera | 19 |
| P-5 | Tacos de Ecoflex | Rueda cargada con 2.1 kg rodando sobre arena | Los tacos no se doblan por completo; la rueda avanza sin patinar en 30° | 13, 24, 25 |
| P-6 | Curado sobre PETG | 10 g de Ecoflex sobre recorte de PETG | Cura completo, sin zona pegajosa | — |
| P-7 | Obstáculo | Un lado de la suspensión cruza un escalón de 8 cm | Las 3 ruedas siguen en contacto con el suelo | 15 |
| P-8 | Pendiente y vuelco | Rover completo en rampa de 30° y luego inclinación lateral | Sube sin patinar; no vuelca antes de 40° | 13, 14 |

---

## Navegación

[← Diagramas a bloques]({{ '/02-diagramas-a-bloques/' | relative_url }}) · [Electrónica y software →]({{ '/04-electronica-software/' | relative_url }})
