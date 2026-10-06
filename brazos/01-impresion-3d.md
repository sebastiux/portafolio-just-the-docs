---
layout: default
title: Brazo impreso en 3D
parent: Brazos robóticos
nav_order: 1
permalink: /brazos/impresion-3d/
stl_viewer: true
---

# Brazo impreso en 3D

Esta página documenta la fabricación del brazo robótico por **impresión 3D (FDM)** en PLA: los **parámetros de impresión** que se usaron, el **ensamble** y cada una de las **8 piezas** con su visor 3D.

> **Cómo usar los visores 3D:** arrastra para girar, rueda del ratón (o pellizco) para acercar y clic derecho (o dos dedos) para desplazar. **Reiniciar vista** regresa a la vista inicial.

---

## 1) Origen del diseño y créditos

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

<!-- PENDIENTE: el documento de entrega menciona 9 piezas STL; en este repositorio hay 8 (base, tapa, brazo-1, brazo-2, soporte-pinza, pinon-servo, pinon-pinza, pinzas). Confirmar cuál es el conteo correcto y, si falta una, subirla. -->

---

## 2) Parámetros de impresión

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

---

## 3) Ensamble

<div class="stl-viewer stl-viewer--tall" data-assembly="{{ '/assets/stl/brazo-impreso/ensamble/ensamble-cad.json' | relative_url }}" data-base="{{ '/assets/stl/brazo-impreso/ensamble/' | relative_url }}"></div>

**Figura 1:** Ensamble en coordenadas reales del CAD. Usa **Separar piezas** para la vista explosionada.

> **Faltan las dos mordazas.** El ensamble muestra **7 de las 9 piezas**, colocadas con las posiciones reales del CAD. Las mordazas no aparecen porque `pinzas.stl` trae **las dos en un solo archivo** y no está en el marco de coordenadas de cada pieza: al separarlas y aplicarles su transformación, ninguna de las dos asignaciones posibles las deja cerca del soporte (quedan a unos 90 mm). Se resuelve exportando `Pinza derecha v1` y `Pinza izquierda v1_MIR_MIR3` como STL independientes. Las dos mordazas sí se ven bien en su visor individual, más abajo.
>
> **De dónde salen estas posiciones.** El STEP que exportó Inventor para este ensamble **viene sin geometría** (estructura y posiciones, cero sólidos), así que no sirve para el visor. Pero sus transformaciones de ensamble sí están completas, y son las que se aplicaron a los STL. Las genera `tools/f2_ensamble_impreso.py`.

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
| 8 | Pinzas | Par de mordazas con sector dentado que cierran sobre la muestra. |

---

## 4) Piezas individuales

Dimensiones medidas sobre cada STL (caja envolvente en la orientación de impresión, X × Y × Z). La **masa máxima** supone la pieza 100 % sólida en PLA (1.24 g/cm³); con 2 paredes y 15 % de relleno la masa real será **menor**.

| Pieza | Archivo | Dimensiones (mm) | Volumen (cm³) | Masa máx. (g) | Triángulos |
|:------|:--------|:-----------------|--------------:|--------------:|-----------:|
| Base | `Base_2_v2.stl` | 45.0 × 45.0 × 24.0 | 23.45 | 29.1 | 17 744 |
| Tapa | `Tapa_v2.stl` | 38.0 × 38.0 × 29.5 | 12.85 | 15.9 | 5 618 |
| Brazo 1 | `Brazo_1_v1.stl` | 16.5 × 80.0 × 5.0 | 3.63 | 4.5 | 870 |
| Brazo 2 | `Brazo_2_v1_FINAL_FInal.stl` | 17.0 × 90.0 × 12.0 | 5.93 | 7.4 | 4 142 |
| Soporte de pinza | `Soporte_Pinza_v1.stl` | 29.0 × 44.0 × 4.0 | 2.43 | 3.0 | 1 170 |
| Piñón del servo | `Piñon_Servo_v1.stl` | 20.0 × 20.0 × 5.0 | 0.64 | 0.8 | 1 548 |
| Piñón de pinza | `Piñon_pinza_1_v1.stl` | 28.0 × 28.0 × 7.0 | 1.73 | 2.1 | 2 342 |
| Pinzas | `Pinzas_Final.stl` | 95.3 × 43.3 × 6.2 | 3.70 | 4.6 | 3 276 |
| **Total** | | | **54.36** | **67.4** | |

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
    <div class="stl-viewer" data-stl="{{ '/assets/stl/brazo-impreso/pinzas.stl' | relative_url }}" data-color="#0EA5E9"></div>
    <figcaption><strong>Pinzas</strong> · <a href="{{ '/assets/stl/brazo-impreso/pinzas.stl' | relative_url }}" download>Descargar STL</a></figcaption>
  </figure>
</div>

---

## 5) Electrónica y control

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

## 6) Observaciones del diseño

- **Grados de libertad:** el brazo articula en la base (giro), el hombro (horquilla de la tapa) y el codo (brazo 1 → brazo 2), más la apertura de la pinza: **3 GDL + pinza**.
- **Alcance:** los dos eslabones suman **170 mm** (80 + 90) más la pinza.
- **Masa:** como máximo **67 g** de piezas impresas, sin servos ni tornillería.
- **Transmisión de la pinza:** el servo mueve la pinza a través de un par de engranes (piñón del servo de 20 mm → piñón de pinza de 28 mm), que reduce la velocidad y aumenta el par de cierre.

---

## Sección anterior

[Brazos robóticos: proyecto y equipo]({{ '/brazos/' | relative_url }})

## Siguiente sección

[Brazo cortado con láser]({{ '/brazos/corte-laser/' | relative_url }})
