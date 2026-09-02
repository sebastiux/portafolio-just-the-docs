---
layout: default
title: Diagramas a bloques
nav_order: 3
---

# Diagramas a bloques

Esta página documenta la arquitectura del rover en dos vistas: **mecánica** y **eléctrica/electrónica**. Los diagramas se irán actualizando conforme avance el diseño.

| Diagrama | Estado |
|:---------|:-------|
| Eléctrico / electrónico | Versión 1 publicada (sección 1) |
| Mecánico | En elaboración (sección 2) |

---

## 1) Diagrama eléctrico / electrónico

Arquitectura de control y potencia. Las líneas **azules** son señal/datos y las líneas **rojas** son alimentación.

[![Figura 1 — Diagrama de componentes eléctricos]({{ '/assets/img/rover/diagrama-electrico.svg' | relative_url }})]({{ '/assets/img/rover/diagrama-electrico.svg' | relative_url }})
**Figura 1:** Diagrama de componentes eléctricos (arquitectura de control y potencia). Haz clic en la imagen para verla a tamaño completo.

### Lectura del diagrama

**Visión y control**

- La **cámara** (5 V · 3 A) entrega el video a la **CPU**, una **Raspberry Pi**, que lo transmite a la estación del operador y recibe los comandos del control Xbox.
- De la CPU cuelgan **tres subsistemas**, cada uno con su propio **ESP32** a 3.3 V: velocidad, dirección y brazo.

**Velocidad (12 V · 12 A, 6 motores DC)**

- Un ESP32 comanda **3 puentes H** (12 V · 4 A cada uno).
- Cada puente H mueve **2 motores DC** (2 A por motor): un par delantero, un par medio y un par trasero.

**Dirección (5 V · 4 A, 4 servos)**

- Un ESP32 controla **4 servos** de 1 A · 5 V, uno por rueda direccional: delantera izquierda, delantera derecha, trasera izquierda y trasera derecha.

**Brazo (5 V · 3 A, 3 servos)**

- Un ESP32 controla **3 servos** de 1 A · 5 V para las articulaciones del brazo.

**Alimentación**

- **Batería** de 11.7 V · 18 A conectada a un **regulador de 3 salidas**:

| Salida | Alimenta a |
|:-------|:-----------|
| **12 V · 12 A** (salida directa de batería) | 3 puentes H (4 A cada uno) → 6 motores DC |
| **5 V · 10 A** | Todos los servos (brazo + dirección), Raspberry Pi y cámara |
| **3.3 V · 0.5 A** | Los tres ESP32 (velocidad, dirección, brazo) |

### Nomenclatura

| Etiqueta | Significado |
|:---------|:------------|
| DI / DD | Delantero izquierdo / delantero derecho |
| M I / M D | Medio izquierdo / medio derecho |
| TI / TD | Trasero izquierdo / trasero derecho |
| Servo B / M / C | Servos de las articulaciones del brazo (base, medio y codo/pinza, según se defina en el diseño mecánico) |

### Consistencia con las especificaciones

Puntos del diagrama que conviene revisar contra la [tabla de métricas]({{ '/01-especificaciones/' | relative_url }}):

- **Bus de 12 V**: coincide con la métrica 59 (tensión nominal del bus de potencia).
- **Lógica separada de potencia**: los ESP32 van en la salida de 3.3 V y los motores en la de 12 V, lo que cubre la métrica 64 (alimentación lógica aislada del bus de motores).
- **Corriente de batería**: el diagrama considera 18 A; la métrica 61 pide **≥25 A** de descarga continua (ideal ≥40 A). Verificar la batería seleccionada.
- **Drivers de tracción**: cada puente H entrega 4 A (2 A por motor); la métrica 28 pide **≥5 A continuos por canal** y la 29 **≥15 A pico**. Verificar el driver contra el par de bloqueo de los motores.
- **Grados de libertad del brazo**: el diagrama contempla 3 servos; la métrica 30 pide **≥4 GDL** sin contar la pinza. Definir si se agregan servos (brazo y pinza) y ajustar el presupuesto de corriente de la salida de 5 V.

---

## 2) Diagrama mecánico

> **En elaboración.** Esta sección se completará con el diagrama a bloques mecánico (chasis, tracción, suspensión, brazo, pinza y tolva) cuando el equipo lo entregue.

---

## Sección anterior

[Características técnicas y necesidades]({{ '/01-especificaciones/' | relative_url }})
