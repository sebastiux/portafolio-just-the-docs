#!/usr/bin/env python3
"""F6 (B10) — Secuencia de ensamblaje del brazo impreso, un render por paso.

Cada imagen muestra en gris lo que ya está montado y en color lo que se agrega
en ese paso. El encuadre es el mismo en todos los pasos para que se lean como
una secuencia.

Requiere pantalla virtual:  xvfb-run -a python3 tools/f6_secuencia_impreso.py
Salida: assets/brazos/impreso3d/render/secuencia/paso-NN.png
"""
import json, os, sys
import numpy as np
import pyvista as pv
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.path.join(RAIZ, "assets/stl/brazo-impreso/ensamble")
DEST = os.path.join(RAIZ, "assets/brazos/impreso3d/render/secuencia")
TAM = (1600, 1200)
GRIS = "#c9cdd3"

# Orden propuesto a partir de la jerarquía del ensamble CAD: de la base hacia
# la pinza, y cada servo se monta junto con la pieza que lo aloja. Los servos
# se identifican por su posición en el STEP (ver ensamble-cad.json).
PASOS = [
    ["base.stl", "servo-1.stl"],                 # 1. servo de giro dentro de la base
    ["tapa.stl"],                                # 2. tapa sobre el eje del servo de giro
    ["servo-3.stl", "brazo-1.stl"],              # 3. servo del hombro y brazo 1
    ["servo-2.stl", "brazo-2.stl"],              # 4. servo del codo y brazo 2
    ["soporte-pinza.stl", "servo-4.stl"],        # 5. soporte y servo de la pinza
    ["pinon-servo.stl", "pinon-pinza.stl"],      # 6. tren de engranes de la pinza
    ["pinza-derecha.stl", "pinza-izquierda.stl"],  # 7. mordazas
]


def main():
    spec = json.load(open(os.path.join(ORIG, "ensamble-cad.json"), encoding="utf-8"))
    color = {p["file"]: p["color"] for p in spec["parts"]}
    usados = [f for paso in PASOS for f in paso]
    faltan = set(color) - set(usados)
    if faltan:
        sys.exit(f"Piezas sin paso asignado: {sorted(faltan)}")
    mallas = {f: pv.read(os.path.join(ORIG, f)) for f in usados}

    # Cámara fija, calculada una sola vez con el ensamble completo.
    p = pv.Plotter(off_screen=True, window_size=TAM)
    for m in mallas.values():
        p.add_mesh(m)
    p.enable_parallel_projection()
    p.view_isometric()
    camara = p.camera_position
    escala = p.camera.parallel_scale
    p.close()

    os.makedirs(DEST, exist_ok=True)
    montado = []
    imagenes = []
    for i, nuevos in enumerate(PASOS, start=1):
        p = pv.Plotter(off_screen=True, window_size=TAM)
        p.set_background("#f5f6f8")
        for f in montado:
            p.add_mesh(mallas[f], color=GRIS, smooth_shading=False, specular=0.1)
        for f in nuevos:
            p.add_mesh(mallas[f], color=color[f], smooth_shading=False,
                       specular=0.2, specular_power=10)
        p.enable_parallel_projection()
        p.camera_position = camara
        p.camera.parallel_scale = escala
        p.add_light(pv.Light(position=(1, -1.5, 2), light_type="headlight", intensity=0.45))
        imagenes.append(p.screenshot(return_img=True))
        p.close()
        montado += nuevos

    # Recorte común: el rectángulo que cubre el contenido de todos los pasos,
    # con margen. Así el brazo queda centrado y en el mismo lugar en cada imagen.
    fondo = imagenes[0][0, 0]
    ocupado = np.zeros(imagenes[0].shape[:2], dtype=bool)
    for img in imagenes:
        ocupado |= np.any(np.abs(img.astype(int) - fondo.astype(int)) > 6, axis=2)
    filas, cols = np.where(ocupado)
    m = 30
    y0, y1 = max(filas.min() - m, 0), min(filas.max() + m, ocupado.shape[0])
    x0, x1 = max(cols.min() - m, 0), min(cols.max() + m, ocupado.shape[1])
    for i, (img, nuevos) in enumerate(zip(imagenes, PASOS), start=1):
        archivo = os.path.join(DEST, f"paso-{i:02d}.png")
        Image.fromarray(img[y0:y1, x0:x1]).save(archivo, optimize=True)
        print(f"  paso-{i:02d}.png  {os.path.getsize(archivo)/1e3:.0f} KB  + {', '.join(nuevos)}")


if __name__ == "__main__":
    sys.exit(main())
