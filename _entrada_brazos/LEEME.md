# Carpeta de entrada — brazos robóticos

Jekyll ignora las carpetas que empiezan con `_`, así que **nada de aquí se publica** en el
sitio. Es solo el buzón para los archivos originales mientras se procesan.

## Qué falta subir (rama `docs/brazos-3gdl`)

```
_entrada_brazos/
  laser/
    Final Assembly.stp          <- ensamble de Inventor 2026, en mm
    dxf/
      Mearm_1_0_150x200_A.dxf
      Mearm_1_0_150x200_B.dxf
    captura_inventor.png        <- Inventor abierto con el árbol de componentes visible (R3)
    pcb/                        <- KiCad o esquemático en PDF, firmware, foto de la PCB,
                                   captura de la app, pinout
  media/
    laser/                      <- fotos y videos del corte, el armado y la prueba
    impreso3d/
  datos.txt                     <- respuestas a los pendientes (ver abajo)
```

**No subas** la carpeta `inventor/` con los `.SLDPRT`: su licencia en GrabCAD no está
confirmada y hasta entonces no se pueden republicar. Tampoco subas `OldVersions/`.

## Límites

- Menos de 100 MB por archivo (límite de GitHub).
- Imágenes: lado largo de 1600 px, hasta 500 KB, **sin EXIF** (sobre todo sin GPS).
- Videos: a YouTube no listado o a Drive, y se embeben. No al repositorio.

## Preguntas abiertas para `datos.txt`

1. Cortadora láser: marca, modelo y área de trabajo.
2. Software de corte y versión.
3. Parámetros: potencia (%), velocidad (mm/s) y número de pasadas.
4. Kerf medido y compensación aplicada.
5. ¿Se mandaron los DXF a la máquina sin modificar (sin reescalar ni compensar)?
6. ¿Quién subió el MeArm a GrabCAD y qué licencia declara esa página?
7. ¿Qué licencia declara RACBOTS en Printables #449747?
8. ¿Las piezas `Part 09`, `Part 23` y `Part 27 - Sticky Foot` no se usaron?
9. ESP32-C3: pinout completo (servos, 3 potenciómetros, interruptor) y de dónde sale la
   corriente de los 4 SG90.
10. ¿Cómo se controla el cuarto eje, si solo hay 3 potenciómetros?
11. Medidas generales del brazo láser **armado** (no las del STEP).
12. Diámetro de la pelota de espuma y resultado de cada intento.
13. ¿El brazo impreso tiene 8 o 9 piezas? El repositorio tiene 8.
14. Profesor y fecha de entrega, para el cuadro de título de los planos.

## Al terminar

Cuando los archivos ya estén procesados y publicados en `assets/`, esta carpeta se borra
del repositorio en un commit aparte.
