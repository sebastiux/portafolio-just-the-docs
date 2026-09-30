---
layout: default
title: Brazos robóticos
nav_order: 4
stl_viewer: true
---

# Brazos robóticos: impresión 3D y corte láser

**Equipo de Integración Mecatrónica Otoño 2026**  
**Integrantes:** Juan Pablo Martha, Carlos Sebastián Ortega, Santiago Alejandro Velázquez

Esta página documenta la manufactura de **dos brazos robóticos** como prototipos del subsistema **Brazo** del rover (ver [arquitectura general]({{ '/' | relative_url }}#arquitectura-general)): uno fabricado por **impresión 3D (FDM)** y otro por **corte láser**. El objetivo es comparar ambos procesos antes de fijar el brazo definitivo.

| Brazo | Proceso | Estado |
|:------|:--------|:-------|
| Brazo 1 | Impresión 3D (FDM, PLA) | 8 piezas modeladas, parámetros de impresión documentados (secciones 1 a 4) |
| Brazo 2 | Corte láser | Pendiente: faltan los archivos de corte y los parámetros (sección 5) |

> **Cómo usar los visores 3D:** arrastra para girar, rueda del ratón (o pellizco) para acercar y clic derecho (o dos dedos) para desplazar. **Reiniciar vista** regresa a la vista inicial.

---

## 1) Brazo impreso en 3D: parámetros de impresión

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

- **Sin soportes:** todas las piezas se modelaron para imprimirse **acostadas sobre su cara plana** (eslabones de 5–12 mm de espesor, engranes de 5–7 mm, pinzas de 6 mm), así que no hay voladizos que los necesiten.
- **Compensación de pata de elefante (0.15 mm):** importa en los **engranes** y en las **pinzas**, donde un primer escalón ensanchado haría que los dientes rocen.
- **Compensación XY en 0:** los barrenos de ejes y tornillos salen al tamaño del modelo; si un eje o un cuerno de servo no entra, este es el primer parámetro a ajustar (o rimar el barreno).
- **2 paredes y 15 % de relleno:** suficiente para piezas de prueba. Para el brazo definitivo, los eslabones cargan momento flector en el servo del hombro; conviene probar **3–4 paredes** y **25–40 % de relleno** en `Brazo 1`, `Brazo 2` y la `Tapa`.

> **Nota de trazabilidad:** la placa laminada dentro de `Base_2_v2.3mf` contiene dos copias de una pieza llamada `linternass.stl` (2.08 g, 8 min 20 s), no la base del brazo. Por eso aquí se documentan los **parámetros del perfil**, pero **no** el tiempo ni el peso real de impresión de las piezas del brazo. Para completarlos hay que exportar el `.3mf` o el G‑code de cada placa del brazo.

---

## 2) Ensamble del brazo impreso

<div class="stl-viewer stl-viewer--tall" data-assembly="{{ '/assets/stl/brazo-impreso/ensamble.json' | relative_url }}" data-base="{{ '/assets/stl/brazo-impreso/' | relative_url }}"></div>

**Figura 1:** Vista de conjunto de las 8 piezas. Usa **Separar piezas** para ver la vista explosionada.

> **Importante:** los STL se exportaron cada uno en su **orientación de impresión**, no en coordenadas del ensamble. Las posiciones de este visor son **aproximadas** (cadena vertical base → tapa → brazo 1 → brazo 2 → soporte → engranes → pinzas) y sirven para identificar las piezas, **no** como ensamble dimensional. Para un ensamble exacto se necesitan los STL exportados desde el ensamble CAD con la opción de conservar coordenadas.

### Cadena cinemática

| Orden | Pieza | Función en el brazo |
|:-----:|:------|:--------------------|
| 1 | Base | Aloja el **servo de giro** de la base; se fija al chasis con 3 orejas atornilladas. |
| 2 | Tapa | Plato giratorio sobre el servo de la base, con una **horquilla** de dos postes donde articula el brazo 1. |
| 3 | Brazo 1 | Primer eslabón (80 mm). Un extremo con ranura para el eje de la horquilla y otro con ventana para el servo del codo. |
| 4 | Brazo 2 | Segundo eslabón (90 mm), con alojamiento para el siguiente servo en el extremo. |
| 5 | Soporte de pinza | Marco con ventana rectangular para el **servo de la pinza**. |
| 6 | Piñón del servo | Engrane motriz montado en el eje del servo de la pinza. |
| 7 | Piñón de pinza | Engrane conducido que transmite el giro a las mordazas. |
| 8 | Pinzas | Par de mordazas con sector dentado que cierran sobre la muestra. |

---

## 3) Piezas individuales

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

## 4) Consistencia con las especificaciones

Puntos a revisar contra la [tabla de métricas]({{ '/01-especificaciones/' | relative_url }}) y el [diagrama eléctrico]({{ '/02-diagramas-a-bloques/' | relative_url }}):

- **Grados de libertad:** el diseño impreso tiene articulaciones en base (giro), hombro (horquilla de la tapa), codo (brazo 1 → brazo 2) y pinza. Eso son **3 GDL + pinza**, igual que los 3 servos del diagrama eléctrico, pero por debajo de los **≥4 GDL** que pide la métrica 30.
- **Alcance:** los dos eslabones suman **170 mm** (80 + 90) más la pinza. La necesidad 7 pide accionar el tablero en un rango vertical de **0 a 1 m**; con este alcance el brazo depende de la altura de montaje en el chasis. Es un prototipo de validación, no el brazo final.
- **Masa:** como máximo **67 g** de piezas impresas (sin servos ni tornillería), lo que deja margen para servos pequeños en el codo y la pinza.

---

## 5) Brazo cortado con láser

Pendiente de documentar. Para completar esta sección se necesita:

1. **Archivos de corte** (DXF, SVG o AI) de cada placa, para mostrarlos y publicar sus vistas 3D.
2. **Material y espesor** (por ejemplo MDF o acrílico de 3 mm).
3. **Parámetros de la cortadora:** modelo del equipo, potencia (%), velocidad (mm/s), número de pasadas y, si aplica, parámetros de grabado.
4. **Kerf medido** y la compensación aplicada en ranuras y uniones a presión.
5. **Fotografías** del brazo ensamblado.

---

## Sección anterior

[Diagramas a bloques]({{ '/02-diagramas-a-bloques/' | relative_url }})
