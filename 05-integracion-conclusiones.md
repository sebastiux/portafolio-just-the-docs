---
layout: default
title: Integración y conclusiones
nav_order: 6
permalink: /05-integracion-conclusiones/
---

# Integración y conclusiones

Cómo se juntan mecánica, electrónica y software, cómo se prueba el rover completo, y qué se concluye de la propuesta de materiales.

Contenido:
- [1) Integración física (B25)](#1-integración-física-b25)
- [2) Integración entre electrónica y software (B26)](#2-integración-entre-electrónica-y-software-b26)
- [3) Pruebas de los modos de operación (B27)](#3-pruebas-de-los-modos-de-operación-b27)
- [4) Prueba funcional completa (B28)](#4-prueba-funcional-completa-b28)
- [5) Comparación de versiones (B29)](#5-comparación-de-versiones-b29)
- [6) Conclusiones técnicas (B30)](#6-conclusiones-técnicas-b30)
- [7) Evidencias y archivos (B31)](#7-evidencias-y-archivos-b31)

---

## 1) Integración física (B25)

| Interfaz | Cómo se resuelve |
|:---------|:-----------------|
| Suspensión ↔ cuerpo | Un eje M8 por lado, a través del pivote del balancín con 2 rodamientos 608 |
| Motor ↔ suspensión | Abrazadera Ø37 del terminal de motor; la rueda se monta en la flecha con prisionero M3 |
| Cables de motor ↔ cuerpo | **Por dentro de los tubos**: entran por la abrazadera, cruzan las uniones por su canal central y salen por el ojal de cada pivote con un bucle flojo |
| Servos de dirección ↔ suspensión | Pendiente del diseño de la esquina con dirección (ver conclusiones) |
| Batería ↔ cuerpo | Al centro del cuerpo, sobre el eje de los pivotes, para no cargar más un lado que otro |

---

## 2) Integración entre electrónica y software (B26)

El orden de integración va **de abajo hacia arriba**, para que cada paso tenga una sola cosa nueva que pueda fallar:

1. Un ESP32 con sus actuadores, comandado por cable desde una PC.
2. La Pi comandando un ESP32 por I2C (pruebas [E-3 y E-4]({{ '/04-electronica-software/' | relative_url }}#4-pruebas-por-bloques-b18)).
3. Los tres ESP32 en el mismo bus.
4. La estación comandando a la Pi por Wi-Fi, con video.

---

## 3) Pruebas de los modos de operación (B27)

| Modo | Prueba | Criterio de aceptación | Métrica |
|:-----|:-------|:-----------------------|:--:|
| Traslado | Recorrido de 5 m en terreno emulado | ≥0.30 m/s | 17 |
| Pendiente | Rampa de 30° con carga completa | Sube sin patinar | 13 |
| Obstáculo | Escalón de 8 cm | Lo libra sin perder contacto de las 6 ruedas | 15 |
| Recolección | Aproximar, tomar y guardar una roca | ≤45 s por roca | 66 |
| Tablero | 2 interruptores + 2 botones | ≤300 s | 68 |
| Paro | Paro de emergencia durante traslado | Se detiene; la telemetría sigue | 64 |

---

## 4) Prueba funcional completa (B28)

Una misión completa con el reglamento: navegación, recolección de las 10 rocas, almacenamiento, descarga y tablero, en **≤600 s** (métrica 67), registrando con el INA219 la corriente y el voltaje de toda la misión. Se documenta con video y con la hoja de tiempos por etapa.

---

## 5) Comparación de versiones (B29)

Para la suspensión hay dos versiones posibles del mismo diseño, y esta propuesta las deja **intercambiables**: los casquillos aceptan el tubo de aluminio o un eslabón impreso con el mismo diámetro exterior.

| Aspecto | Versión A: tubo de Al + uniones de PETG (propuesta) | Versión B: eslabones impresos completos |
|:--------|:----------------------------------------------------|:----------------------------------------|
| Rigidez del eslabón | Alta: 15.6 MPa en el caso de carga, contra ≥48 MPa de fluencia | Menor y dependiente de la orientación de capas |
| Masa | 109 g por tramo de 300 mm | Similar o mayor a igual rigidez |
| Paso de cables | Por dentro del tubo | Por fuera, con sujetadores |
| Cambiar un largo | Cortar otro tubo; las uniones no cambian | Reimprimir la pieza |
| Costo de los eslabones | $1,892.45 MXN (5 barras) | Solo filamento |

Llantas: **Ecoflex 00-20** contra **Ecoflex 00-50 o Dragon Skin 10**, con el mismo molde. Se decide con la prueba [P-5]({{ '/03-mecanica-materiales/' | relative_url }}#11-pruebas-mecánicas-b12).

---

## 6) Conclusiones técnicas (B30)

1. **El tubo de aluminio está sobrado en resistencia.** Con la carga de diseño trabaja a 15.6 MPa; aun si el tubo viniera recocido, el factor de seguridad es de 3. El tubo no es el riesgo.
2. **Los puntos débiles son las uniones y la abrazadera.** El casquillo de PETG trabaja a 4.2 MPa, con margen; la abrazadera del motor depende de la fricción para resistir el par de bloqueo, y es lo primero que hay que probar (P-4).
3. **Las ruedas son la parte más pesada de la propuesta:** 384 g cada una, 2.3 kg las seis. Es lo primero a aligerar si el presupuesto de masa no cierra.
4. **El Ecoflex 00-20 puede ser demasiado blando** para los tacos. El molde y el procedimiento sirven igual para un silicón más duro, así que el cambio es barato.
5. **Falta la esquina con dirección.** El diagrama v2 pone servos de dirección en las 4 esquinas; los terminales de motor de esta propuesta son fijos. El siguiente diseño es un terminal con un eje vertical y el servo MG996R, que se acopla al mismo casquillo de 30 mm.
6. **Comprar con cuidado:** el anuncio del tubo marcaba **últimas 2 unidades** y se necesitan 5 barras.

---

## 7) Evidencias y archivos (B31)

| Evidencia | Dónde está |
|:----------|:-----------|
| Requisitos y métricas | [Características técnicas y necesidades]({{ '/01-especificaciones/' | relative_url }}) |
| Diagramas de bloques | [Diagramas a bloques]({{ '/02-diagramas-a-bloques/' | relative_url }}) |
| Boceto de concepto | [Mecánica y materiales, figura 1]({{ '/03-mecanica-materiales/' | relative_url }}#2-arquitectura-y-dimensiones-mecánicas-b05) |
| STL de codos, uniones, rin, llanta y molde | [Mecánica y materiales, sección 3]({{ '/03-mecanica-materiales/' | relative_url }}#3-piezas-codos-uniones-rin-y-llanta-b07) |
| Ensamble 3D de la suspensión | [Visor y JSON]({{ '/assets/stl/rover/ensamble/suspension-lado.json' | relative_url }}) |
| Planos | [Mecánica y materiales, sección 5]({{ '/03-mecanica-materiales/' | relative_url }}#5-planos-de-fabricación-b08) |
| Lista de materiales | [Mecánica]({{ '/03-mecanica-materiales/' | relative_url }}#7-lista-de-materiales-mecánicos-b06) · [Electrónica]({{ '/04-electronica-software/' | relative_url }}#2-lista-de-materiales-electrónicos-b14) |
| Datos de las piezas | [`datos.json`]({{ '/assets/stl/rover/datos.json' | relative_url }}) |
| Scripts que generan todo lo anterior | [`tools/r1` a `tools/r4`](https://github.com/sebastiux/portafolio-just-the-docs/tree/main/tools) |

---

## Navegación

[← Electrónica y software]({{ '/04-electronica-software/' | relative_url }}) · [Proyecto y equipo]({{ '/' | relative_url }})
