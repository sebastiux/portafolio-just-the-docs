---
layout: default
title: Proyecto y equipo
nav_order: 1
---

# Rover Lunar

**Equipo de Integración Mecatrónica Otoño 2026**  
**Integrantes:** Juan Pablo Martha, Carlos Sebastián Ortega, Santiago Alejandro Velázquez

Contenido:
- [1. Proyecto y equipo](#1-descripción-del-proyecto) (esta página)
- [2. Características técnicas y necesidades]({{ '/01-especificaciones/' | relative_url }})
- [3. Diagramas a bloques (mecánico y eléctrico/electrónico)]({{ '/02-diagramas-a-bloques/' | relative_url }})

> Estado: **versión preliminar para revisión con asesores**. Los valores marcados con **(H)** son hipótesis de ingeniería, no datos del reglamento, y requieren validación por prototipo o por el comité organizador.

---

## 1) Descripción del proyecto

Como proyecto de la clase de **Integración Mecatrónica Otoño 2026**, el equipo manufacturará un rover lunar teledirigido capaz de completar la misión propuesta: recorrer un terreno lunar emulado, recolectar muestras (rocas), almacenarlas a bordo, depositarlas en un contenedor y accionar un tablero de interruptores y botones, todo dentro del tiempo de misión.

La operación es **completamente remota**: no hay navegación autónoma. Un operador controla el rover desde una laptop con un **control de Xbox**, viendo en tiempo real el video de la cámara a bordo a través de un enlace **Wi-Fi**. Por eso los sensores del rover se especifican por su valor para el operador (latencia, cuadros por segundo, canales visibles) y no por desempeño autónomo.

### Misión que debe cumplir

| Etapa | Qué debe hacer el rover | Referencia |
|:------|:------------------------|:-----------|
| Navegación | Atravesar valles, surcos y pendientes de ±30° sin volcar ni atascarse. | Necesidad 4 |
| Recolección | Sujetar rocas de tamaño y color variables sin dañarlas ni soltarlas. | Necesidad 5 |
| Almacenamiento | Alojar a bordo todas las muestras (se asumen 10) y depositarlas dentro del contenedor. | Necesidad 6 |
| Tablero | Accionar 2 interruptores y 2 botones en un rango vertical de 0 a 1 m con el brazo. | Necesidad 7 |
| Registro | Registrar y georreferenciar rocas y relieves durante la misión. | Necesidad 9 |
| Tiempo | Completar la misión en 10 min (+5 min de mantenimiento guiado). | Necesidad 8 |

### Arquitectura general

El rover se organiza en cinco subsistemas. El detalle eléctrico está en [Diagramas a bloques]({{ '/02-diagramas-a-bloques/' | relative_url }}).

| Subsistema | Función | Componentes principales |
|:-----------|:--------|:------------------------|
| **Visión y control** | Recibe los comandos del operador y transmite el video. | Raspberry Pi (CPU), cámara, enlace Wi-Fi |
| **Velocidad (tracción)** | Mueve el rover en el terreno. | ESP32, 3 puentes H, 6 motores DC |
| **Dirección** | Orienta las ruedas. | ESP32, 4 servos |
| **Brazo** | Acciona el tablero y manipula las muestras. | ESP32, 3 servos, pinza |
| **Alimentación** | Energiza todo el sistema con lógica separada de potencia. | Batería 11.7 V · 18 A, regulador de 3 salidas (12 V, 5 V, 3.3 V) |

### Alcance y supuestos

- Proyecto **100 % teledirigido** (Raspberry Pi + control Xbox + enlace Wi-Fi).
- Se asume una envolvente de **100 cm por lado** y **10 rocas** por misión, según el análisis del reglamento (ver [supuestos]({{ '/01-especificaciones/' | relative_url }}#4-supuestos-y-contradicciones-detectadas-en-el-reglamento)).
- Faltan por definir con los asesores: presupuesto techo, costo objetivo por subsistema, proveedores y método de verificación de cada métrica.

---

## 2) Equipo de trabajo

**Clase:** Integración Mecatrónica, Otoño 2026  
**Institución:** IBERO

| Integrante |
|:-----------|
| Juan Pablo Martha |
| Carlos Sebastián Ortega |
| Santiago Alejandro Velázquez |

---

## Siguiente sección

[Características técnicas y necesidades]({{ '/01-especificaciones/' | relative_url }})
