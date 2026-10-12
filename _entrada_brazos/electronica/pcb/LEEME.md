# PCB de control para brazo robótico 3 GDL — ESP32-C3 Super Mini (v3, 58 × 48 mm)

Una placa por brazo. Sirve para el MeArm y para el brazo impreso; la diferencia entre brazos va en el firmware.

- **Tamaño:** **58 × 48 mm**, centrada en el blank de fenólica de 70 × 50 mm. Quedan 6 mm libres a cada lado en X para los clamps y 1 mm en Y.
- **Contorno:** ahora sí se fresa.
- **Una sola cara:** el cobre está en **B.Cu** y los componentes son through-hole, por arriba. No hay vías ni puentes de alambre.
- **Pistas:** 0.8 mm para señales, 1.2 mm para GND y 5 V, 1.6 mm para la alimentación de los servos.
- **Aislamiento mínimo:** 0.6 mm entre cobres de nets distintas.
- **Cobre al contorno:** al menos 0.8 mm.

## Cambios contra la v2 (70 × 50 mm)

| Qué | v2 | v3 |
|---|---|---|
| Botón DIAG (SW3) | Botón de 6 mm en la placa | **Eliminado.** Hacía exactamente lo mismo que el botón **BOOT del módulo**: mismo pin (IO9) y misma función. El módulo va en zócalo, así que su botón queda accesible |
| Conector extra J7 (3V3, GND, IO8) | Sí | **Eliminado** por espacio. IO8 queda libre en el módulo |
| R1–R3 | Acostadas, entre potenciómetros | **Paradas** (5.08 mm entre patas) **debajo** de cada pot, para que los 3 pots queden juntos |
| Servos | IO5 / IO6 / IO7 / IO10 en filas consecutivas | Mismos pines. El conector PINZA quedó a la altura de IO10, con un hueco entre CODO y PINZA |
| Switches | Lado a lado, abajo a la derecha | Uno sobre otro: **PINZA arriba (SW1, IO21)** y **MODO abajo (SW2, IO20)** |

Firmware: los únicos cambios son que **ya no existe J7** y que el botón DIAG es el BOOT del módulo; ambos usan los mismos pines que antes.

## Mapa de pines (firmware)

| GPIO | Función | Notas |
|---|---|---|
| IO1 | Pot BASE (RV1) | ADC1_CH1 |
| IO0 | Pot HOMBRO (RV2) | ADC1_CH0 |
| IO3 | Pot CODO (RV3) | ADC1_CH3 |
| IO4 | LED de estado D2 | **Activo en bajo** |
| IO2 | LED DIAG D3 | **Activo en bajo**; pin de arranque con pull-up R6 de 10 kΩ |
| IO5 / IO6 / IO7 / IO10 | Servo BASE / HOMBRO / CODO / PINZA (J3–J6) | PWM a 50 Hz |
| IO21 | Switch PINZA (SW1) | `INPUT_PULLUP` |
| IO20 | Switch MODO (SW2) | `INPUT_PULLUP` |
| IO9 | Botón **BOOT del módulo** = DIAG | Léelo como entrada después del arranque. Presionado al encender entra en modo descarga |
| IO8 | Libre | LED azul del módulo (activo en bajo) |

**Conectores de servo:** el orden es **S V G** de izquierda a derecha, viendo desde los componentes. GND es el pin cuadrado.

## Fabricación en la Genmitsu Cubiko

**Archivos en `cnc/`:** ya vienen **espejados**, vistos desde el lado del cobre. **No los espejes otra vez en FlatCAM.**

| Archivo | Uso |
|---|---|
| `cobre_espejado.gbr` | Aislamiento de pistas |
| `taladros_espejado.drl` | Taladros, alineados con el cobre: 75 de 75 verificados |
| `contorno_espejado.gbr` | **Corte del contorno:** rectángulo de 58 × 48 mm en X 6–64, Y 1–49 |
| `cobre_visto_desde_cobre.svg` | Para revisar o imprimir 1:1 |

**Origen (0, 0):**
1. Pon el blank de 70 × 50 mm con el **cobre hacia arriba**.
2. El lado largo va en X y el borde del USB del módulo queda hacia el fondo (+Y).
3. El origen es la **esquina frontal izquierda del blank**, no de la placa.
4. Los clamps van en las franjas de 6 mm de cada lado en X.

**Orden de trabajo:**
1. Mapa de alturas con la sonda.
2. Aislamiento:
   - La herramienta debe cortar **≤ 0.6 mm** de ancho.
   - **HIPÓTESIS** de partida: V-bit de 20–30°, punta de 0.1 mm, 0.05–0.1 mm de profundidad, que corta ~0.13–0.16 mm.
   - Puedes dar 2–3 pasadas mientras la suma de los anchos cortados no pase de 0.6 mm.
3. Taladrado (puedes reasignar los diámetros en FlatCAM):

   | Broca | Agujeros del archivo | Para |
   |---|---|---|
   | 0.8 mm | 22 de 0.8 + 4 de 0.9 | R1–R6, C1, C2, SW1, SW2, LEDs |
   | 1.0 mm | 37 de 1.0 + 2 de 1.1 | Módulo, servos, pots, D1 |
   | 1.5 mm | 4 de 1.52 | Borneras |
   | 2.0 mm | 6 ranuras de 2.1 × 1.8 | Anclajes de los pots; taládralos redondos |

4. **Contorno, al final:**
   - Corta por fuera de la línea, con una fresa recta de 1–2 mm.
   - Da varias pasadas hasta atravesar los 1.6 mm.
   - Deja 2–4 pestañas para que la placa no se suelte.
   - En Y solo hay 1 mm de margen: la fresa va a tocar el borde del blank. Es normal.
5. **Polvo:** usa aspiradora; el polvo de fenólica irrita.

**Antes de fresar:**
- Imprime `docs/vista.png` a escala 1:1 y presenta encima tus piezas reales.
- Revisa sobre todo: pots RK09K, switches deslizables a 2.54 mm, C1 de Ø8 mm, borneras de 5.08 mm, y que las resistencias de ¼ W paradas entren a 5.08 mm.

## Hipótesis que siguen abiertas

1. **Orden de pines del Super Mini.** Compáralo con la serigrafía de tu módulo:
   - Izquierda: `5V GND 3V3 IO4 IO3 IO2 IO1 IO0`
   - Derecha: `IO5 IO6 IO7 IO8 IO9 IO10 IO20 IO21`
2. **Separación entre filas: 15.24 mm.** Mídela con calibrador.
3. **Ancho de corte de tu herramienta de aislamiento:** el requisito es ≤ 0.6 mm.
4. **Rango útil del ADC del C3 (~2.5 V):** R1–R3 de 3.3 kΩ limitan el tope de los pots.
5. **Perillas:** los pots quedan a 13.4 mm entre ejes. Usa perillas de **≤ 12 mm** de diámetro.

## Qué verifiqué

- **DRC de KiCad 7.0.11** sobre el proyecto empaquetado: 0 violaciones, 0 pads sin conectar.
- **Netlists:** la del esquemático, la de la PCB y la del diseño coinciden: 21 nets.
- **Geometría, revisada por código:**
  - pista mínima: 0.80 mm;
  - aislamiento mínimo: 0.600 mm;
  - todo el cobre a ≥ 0.8 mm del contorno;
  - cada net forma una sola isla.
- **Archivos espejados:** los 75 agujeros caen sobre la posición espejada de su pad, y el contorno queda en X 6–64, Y 1–49.

## Qué no verifiqué

- **DRC y ERC en KiCad 10.**
- **El código G**, porque depende de tus brocas y avances.
