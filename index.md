---
layout: default
title: Proyecto y equipo
nav_order: 1
---

# Rover Lunar

**Equipo de Integración Mecatrónica Otoño 2026**  
**Integrantes:** Juan Pablo Martha, Carlos Sebastián Ortega, Santiago Alejandro Velázquez

Contenido:
- [1. Proyecto y equipo](#descripción-del-proyecto-b01) (esta página): problema, misión, arquitectura y mapa de la documentación
- [2. Características técnicas y necesidades]({{ '/01-especificaciones/' | relative_url }}): necesidades, métricas y supuestos
- [3. Diagramas a bloques (mecánico y eléctrico/electrónico)]({{ '/02-diagramas-a-bloques/' | relative_url }})
- [4. Mecánica y materiales]({{ '/03-mecanica-materiales/' | relative_url }}): tubo de aluminio, uniones y rines de PETG, llantas de Ecoflex, STL, planos, BOM y pruebas
- [5. Electrónica y software]({{ '/04-electronica-software/' | relative_url }})
- [6. Integración y conclusiones]({{ '/05-integracion-conclusiones/' | relative_url }})

> Estado: **versión preliminar para revisión con asesores**. Los valores marcados con **(H)** son hipótesis de ingeniería, no datos del reglamento, y requieren validación por prototipo.

---

## Descripción del proyecto (B01)

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

### Arquitectura general (B04)

El rover se organiza en cinco subsistemas, según el [diagrama eléctrico v2]({{ '/02-diagramas-a-bloques/' | relative_url }}). La mecánica de la suspensión está en [Mecánica y materiales]({{ '/03-mecanica-materiales/' | relative_url }}).

| Subsistema | Función | Componentes principales |
|:-----------|:--------|:------------------------|
| **Visión y control** | Recibe los comandos del operador y transmite el video. | Raspberry Pi 4 (maestro I2C), cámara, IMU, INA219, enlace Wi-Fi |
| **Velocidad (tracción)** | Mueve el rover en el terreno. | ESP32 `0x10`, 3 drivers duales, 6 motores DC 12 V, suspensión balancín-bogie |
| **Dirección** | Orienta las ruedas de esquina. | ESP32 `0x11`, 4 servos MG996R |
| **Brazo** | Acciona el tablero y manipula las muestras. | ESP32 `0x12`, 5 servos (base, hombro, codo, pinza, tolva), sensores de color, distancia y peso |
| **Alimentación** | Energiza todo el sistema con lógica separada de potencia. | LiPo 3S 5000 mAh, fusible de 30 A, VBAT directo, 2 BEC de servos y buck de 5.1 V |

### Alcance y supuestos

- Proyecto **100 % teledirigido** (Raspberry Pi + control Xbox + enlace Wi-Fi).
- Se asume una envolvente de **100 cm por lado** y **10 rocas** por misión, según el análisis del reglamento (ver [supuestos]({{ '/01-especificaciones/' | relative_url }}#4-supuestos-y-contradicciones-detectadas-en-el-reglamento)).
- Faltan por definir con los asesores: presupuesto techo, costo objetivo por subsistema, proveedores y método de verificación de cada métrica.

### Bocetos y alternativas (B02 · B03)

[![Boceto de concepto del rover]({{ '/assets/img/rover/mecanica/boceto-rover.png' | relative_url }})]({{ '/assets/img/rover/mecanica/boceto-rover.png' | relative_url }})
**Figura 1:** Boceto de concepto con la propuesta de materiales: eslabones de tubo de aluminio, uniones y rines de PETG, llantas de Ecoflex. La suspensión está a escala.

La comparación de alternativas de materiales (eslabones, uniones y llantas), con su matriz de decisión, está en [Mecánica y materiales]({{ '/03-mecanica-materiales/' | relative_url }}#1-por-qué-estos-materiales-b03).

---

## Mapa de la documentación

Dónde se documenta cada criterio de la evaluación.

| Criterio | Dónde |
|:---------|:------|
| B01 Problema, objetivos y requisitos | [Esta página](#descripción-del-proyecto-b01) · [Necesidades y métricas]({{ '/01-especificaciones/' | relative_url }}) |
| B02 Bocetos · B03 Alternativas | [Esta página](#bocetos-y-alternativas-b02--b03) · [Matriz de materiales]({{ '/03-mecanica-materiales/' | relative_url }}#1-por-qué-estos-materiales-b03) |
| B04 Arquitectura general | [Esta página](#arquitectura-general-b04) · [Diagramas a bloques]({{ '/02-diagramas-a-bloques/' | relative_url }}) |
| B05–B12 Mecánica: dimensiones, BOM, archivos, planos, fabricación, ensamble y pruebas | [Mecánica y materiales]({{ '/03-mecanica-materiales/' | relative_url }}) |
| B13–B24 Electrónica y software | [Diagrama eléctrico]({{ '/02-diagramas-a-bloques/' | relative_url }}) · [Electrónica y software]({{ '/04-electronica-software/' | relative_url }}) |
| B25–B31 Integración, pruebas, comparación, conclusiones y evidencias | [Integración y conclusiones]({{ '/05-integracion-conclusiones/' | relative_url }}) |

---

## Siguiente sección

[Características técnicas y necesidades]({{ '/01-especificaciones/' | relative_url }})
