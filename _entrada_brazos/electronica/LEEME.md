# Buzón de la electrónica

Esta carpeta ya no guarda los archivos del proyecto: `pcb/` y `generador/` se
borraron en cuanto quedaron publicados, para no tener dos copias de lo mismo en
el repositorio.

| Qué era | Dónde está ahora |
|---|---|
| `pcb/` (proyecto de KiCad, `cnc/`, `fabricacion/`, `docs/`) | `assets/brazos/electronica/kicad-v3/` |
| `generador/` (los 13 scripts de Python) | `assets/brazos/electronica/generador-v3/` |

Lo que queda es el buzón de lo que todavía falta. **Jekyll ignora las carpetas
que empiezan con `_`, así que nada de aquí se publica.**

## Pendientes

`mediciones.txt` espera las respuestas de la sección 9 del handoff:

1. Pinout físico del Super Mini y separación entre sus filas.
2. Qué posición de SW2 es MANUAL y cuál APP; qué posición de SW1 es pinza abierta.
3. Mediciones con multímetro: J1, el pin 5V del módulo, 3V3, el tope de cada
   potenciómetro y J2 con los cuatro servos moviéndose.
4. Fresado: software, brocas, profundidad, avance, RPM, pasadas, tiempo y
   problemas que hubo.
5. Voltajes reales de cada canal de la fuente.
6. Cómo se fijó la tarjeta a cada brazo.
7. Si ya está fresada la segunda tarjeta.
8. Media (va en `media/`): fotos del fresado, del soldado y de la tarjeta
   armada por las dos caras; video del fresado; captura de la app en el
   celular; foto de cada brazo con su tarjeta.
9. Si el LED verde D2 enciende bien.
10. Ángulos reales de la pinza abierta y cerrada de cada brazo.
11. Precios, si la rúbrica los pide, y de dónde salen.

También faltan los tamaños de flash y RAM de las dos compilaciones: hay que
compilar con arduino-cli, porque en la nube no se pudo instalar.

## Límites para la media

- Menos de 100 MB por archivo (límite de GitHub).
- Imágenes: lado largo de 1600 px, hasta 500 KB, **sin EXIF** (sobre todo sin GPS).
- Videos: a YouTube no listado o a Drive, y se embeben. No al repositorio.

## Al terminar

Cuando lo de arriba esté en las páginas, esta carpeta se borra completa en un
commit aparte.
