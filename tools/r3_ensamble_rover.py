#!/usr/bin/env python3
"""R3 (B06 · B10) — Render del ensamble de un lado de la suspensión y su
secuencia de armado, leyendo el mismo JSON que usa el visor 3D del sitio.

Las rotaciones del JSON siguen la convención de three.js (Euler XYZ en
grados), así que lo que se ve aquí es lo mismo que en el visor.

Uso:    xvfb-run -a python3 tools/r3_ensamble_rover.py
Salida: assets/img/rover/mecanica/ensamble-*.png y secuencia/paso-NN.png
"""
import json
import math
import os

import numpy as np
import pyvista as pv
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(RAIZ, "assets/stl/rover/ensamble")
DEST = os.path.join(RAIZ, "assets/img/rover/mecanica")
GRIS = "#c9cdd3"
TAM = (1600, 1000)

# Pasos de armado: por nombre (prefijo) de las partes del JSON
PASOS = [
    ("Rueda: rin + llanta colada", ["Rin", "Llanta"]),
    ("Motores en sus terminales", ["Motorreductor", "Terminal de motor"]),
    ("Bogie: pivote + 2 patas de 150 mm", ["Pivote del bogie", "Pata del bogie"]),
    ("Balancín: pivote + tubos + terminal de eje", ["Pivote del balancín", "Tubo delantero", "Tubo trasero", "Terminal de eje"]),
]


def matriz(p):
    rx, ry, rz = (math.radians(v) for v in p.get("rotation", [0, 0, 0]))
    cx, sx, cy, sy, cz, sz = math.cos(rx), math.sin(rx), math.cos(ry), math.sin(ry), math.cos(rz), math.sin(rz)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    T = np.eye(4)
    T[:3, :3] = Rx @ Ry @ Rz           # three.js, orden 'XYZ'
    T[:3, 3] = p.get("position", [0, 0, 0])
    return T


def cargar():
    spec = json.load(open(os.path.join(BASE, "suspension-lado.json"), encoding="utf-8"))
    piezas = []
    for p in spec["parts"]:
        m = pv.read(os.path.normpath(os.path.join(BASE, p["file"])))
        # Igual que el visor: centro en XY y base en Z = 0 antes de colocar
        lo = np.array(m.bounds[0::2]); hi = np.array(m.bounds[1::2])
        m = m.translate([-(lo[0] + hi[0]) / 2, -(lo[1] + hi[1]) / 2, -lo[2]], inplace=False)
        m = m.transform(matriz(p), inplace=False)
        piezas.append((p, m))
    return piezas


def foto(piezas, ruta, vista, resaltar=None, escala=None, camara=None):
    pl = pv.Plotter(off_screen=True, window_size=TAM)
    pl.set_background("white")
    for p, m in piezas:
        color = p["color"]
        if resaltar is not None and not any(p["name"].startswith(k) for k in resaltar[1]):
            color = GRIS if any(p["name"].startswith(k) for k in resaltar[0]) else None
        if color:
            pl.add_mesh(m, color=color, smooth_shading=True, specular=0.2)
    pl.enable_parallel_projection()
    if camara is None:
        vista(pl)
        pl.reset_camera()
        pl.camera.zoom(1.25)
    else:
        pl.camera_position, pl.camera.parallel_scale = camara
    img = pl.screenshot(return_img=True)
    cam = (pl.camera_position, pl.camera.parallel_scale)
    pl.close()
    if ruta:
        Image.fromarray(recortar([img])[0]).save(ruta, optimize=True)
    return img, cam


def recortar(imagenes, margen=24):
    """Recorte común a todas las imágenes: el contenido queda en el mismo lugar."""
    fondo = imagenes[0][0, 0].astype(int)
    ocupado = np.zeros(imagenes[0].shape[:2], dtype=bool)
    for img in imagenes:
        ocupado |= np.any(np.abs(img.astype(int) - fondo) > 6, axis=2)
    f, c = np.where(ocupado)
    y0, y1 = max(f.min() - margen, 0), min(f.max() + margen, ocupado.shape[0])
    x0, x1 = max(c.min() - margen, 0), min(c.max() + margen, ocupado.shape[1])
    return [img[y0:y1, x0:x1] for img in imagenes]


def iso(pl):
    pl.view_vector((1, 1.6, 0.9), viewup=(0, 0, 1))


def lado(pl):
    pl.view_vector((0, 1, 0), viewup=(0, 0, 1))


def main():
    piezas = cargar()
    foto(piezas, os.path.join(DEST, "ensamble-iso.png"), iso)
    foto(piezas, os.path.join(DEST, "ensamble-lateral.png"), lado)
    # Secuencia con la cámara del ensamble completo
    _, cam = foto(piezas, None, iso)
    d = os.path.join(DEST, "secuencia")
    os.makedirs(d, exist_ok=True)
    montado, imagenes = [], []
    for titulo, nuevos in PASOS:
        img, _ = foto(piezas, None, iso, resaltar=(montado, nuevos), camara=cam)
        imagenes.append(img)
        montado += nuevos
    for i, ((titulo, _), img) in enumerate(zip(PASOS, recortar(imagenes)), start=1):
        Image.fromarray(img).save(os.path.join(d, f"paso-{i:02d}.png"), optimize=True)
        print(f"  paso-{i:02d}  {titulo}")


if __name__ == "__main__":
    main()
