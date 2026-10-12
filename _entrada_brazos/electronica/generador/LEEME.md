# Generador de la tarjeta v3

Scripts de Python que generan y verifican la tarjeta v3 de 58 × 48 mm, de una cara. Se probaron con KiCad 7.0.11 (módulo `pcbnew`) en Linux.

## Qué hace cada script

- `design.py`: partes, huellas y redes. Es la fuente única de verdad.
- `placement.py`: coloca los componentes y fija las troncales que permiten rutear en una cara.
- `build.py` → `router.py` → `finalize.py`: arman la PCB, la rutean y le aplican reglas, contorno y serigrafía.
- `gen_sch.py`: genera el esquemático a partir del mismo `design.py`.
- `verify_geom.py` y `check_netlist.py`: verifican la geometría y la netlist.
- `cnc_export.py`: exporta los archivos espejados para la fresadora.
- `package.py`: empaqueta el proyecto.

## Orden de ejecución

`build.py` → `router.py` → `verify_geom.py` → `finalize.py out` → `gen_sch.py out` → `check_netlist.py` → `package.py`
