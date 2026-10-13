# Archivo

Material que **no se fabricó ni se usa**, conservado solo como registro del
proceso. **Ninguna página del sitio enlaza a esta carpeta.**

## `tarjeta-2-capas/`

Diseño previo de la tarjeta de control: 2 capas, 90 × 66 mm, FR-4, pensado
para mandar a fabricar a un proveedor. **Nunca se fabricó.** Lo sustituyó la
**tarjeta v3 de una cara, 58 × 48 mm**, fresada en la Genmitsu Cubiko, que es
la que está armada y montada en los dos brazos.

Sus pines **no coinciden** con los de la v3, así que ni el esquemático ni la
PCB ni el Gerber de aquí sirven para la tarjeta real.

| Carpeta | Contenido |
|:--|:--|
| `kicad/` | Proyecto de KiCad de la tarjeta de 2 capas |
| `fabricacion/` | Gerber, barrenos, netlist, DRC y PDF de ese diseño |
| `render/` | Imágenes del esquemático y de las dos caras |
| `proyecto-kicad-tarjeta-brazo.zip` | El proyecto empaquetado |

El diseño vigente está en `assets/brazos/electronica/kicad-v3/`.

## `modo-usb/`

El control por USB desde la computadora **se retiró**. La tarjeta v3 elige el
modo con el **switch SW2**: manual o app web. El puerto USB queda solo para
programar el módulo y para leer el diagnóstico.

| Archivo | Qué era |
|:--|:--|
| `gui/` y `brazo_gui.zip` | Interfaz de escritorio en Python que mandaba órdenes por el puerto serie |
| `simulador.cpp` | Simulaba el firmware en la computadora para probar esa interfaz sin hardware |
| `gui-usb.png` | Captura de la ventana de esa interfaz |
| `app-web.png` | Captura de la app web anterior, de cuando el encabezado decía la fuente de mando |

El `Makefile` de las pruebas ya no tiene el target `simulador`.

## `tools/archivo/f7_tarjeta.py`

El script que generaba la tarjeta de 2 capas (esquemático, PCB, ruteo con
Freerouting y exportación). La v3 se generó con otro juego de scripts, que
están publicados en `assets/brazos/electronica/generador-v3/`.
