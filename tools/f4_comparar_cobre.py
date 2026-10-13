#!/usr/bin/env python3
"""F4 — Comprueba el dibujo del cobre contra la imagen que trae el proyecto.

Las figuras de la tarjeta no salen de kicad-cli (este entorno no lo tiene), sino
de leer el `.kicad_pcb`. Eso deja una pregunta abierta: ¿el script entendió bien
el archivo? El proyecto trae `docs/cobre_espejo.png`, generada con KiCad por
quien diseñó la tarjeta. Comparar las dos responde la pregunta.

Se rasteriza el cobre calculado sobre la misma rejilla de esa imagen, se busca
el encuadre que mejor las superpone y se reporta:
  - cuánto difiere el área total de cobre;
  - la intersección sobre la unión (IoU), que castiga cualquier corrimiento;
  - cuánta discrepancia sobrevive a una tolerancia de 1 y 2 píxeles, que es lo
    que separa un error de geometría de uno de rasterizado.

Así se encontró un error real: el ángulo que un pad declara en `(at x y ang)`
ya viene girado con su footprint y no hay que sumarlo. Con la suma, los seis
pads de montaje de los potenciómetros salían cruzados 90°: la discrepancia que
sobrevivía a 1 px era 4.89 % del área. Corregido, baja a 0.36 %.

Necesita numpy, scipy, pillow y shapely.

    python3 tools/f4_comparar_cobre.py [carpeta del proyecto]
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # para kicad_sexp

import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation
from shapely import contains_xy
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union

from kicad_sexp import geometria_pad
from f4_figuras_tarjeta import datos


def cobre_espejado(d):
    """Todo el cobre de la cara B, reflejado en X y con los barrenos quitados."""
    W = d["W"]
    piezas = [LineString([(W - t["a"][0], t["a"][1]), (W - t["b"][0], t["b"][1])])
              .buffer(t["w"]/2, 8) for t in d["pistas"]]
    piezas += [Polygon([(W - x, y) for x, y in p["poly"]]) for p in d["pads"]]

    huecos = []
    for p in d["pads"]:
        t = p["taladro"]
        if not t:
            continue
        cx, cy = W - p["c"][0], p["c"][1]
        if t[0] == "oval":
            huecos.append(geometria_pad("oval", t[1], t[2], cx, cy, -t[3]))
        else:
            huecos.append(Point(cx, cy).buffer(t[1]/2, 16))
    return unary_union(piezas).difference(unary_union(huecos))


def main(carpeta):
    referencia = os.path.join(carpeta, "docs", "cobre_espejo.png")
    img = np.array(Image.open(referencia).convert("L"))
    suyo = img < 128
    alto, ancho = img.shape

    d = datos(carpeta)
    W, H = d["W"], d["H"]
    cobre = cobre_espejado(d)
    # El marco de la imagen es el contorno de la placa, no cobre: se recorta.
    util = Polygon([(0, 0), (W, 0), (W, H), (0, H)]).buffer(-0.8)

    yy, xx = np.mgrid[0:alto, 0:ancho]
    print(f"referencia: {referencia}  ({ancho} x {alto} px)")

    # Encuadre: escala aproximada por el ancho de la imagen, y de ahí una
    # búsqueda fina desplazando la máscara, que es barato.
    mejor = (0.0,)
    for s in np.arange(ancho / (W + 4), ancho / (W - 1), 0.04):
        mm_x, mm_y = (xx - 10) / s, (yy - 50) / s
        base_mio, base_util = contains_xy(cobre, mm_x, mm_y), contains_xy(util, mm_x, mm_y)
        for dx in range(-8, 9):
            for dy in range(-8, 9):
                mio = np.roll(np.roll(base_mio, dy, 0), dx, 1)
                dentro = np.roll(np.roll(base_util, dy, 0), dx, 1)
                a, b = mio & dentro, suyo & dentro
                u = (a | b).sum()
                if u and (a & b).sum() / u > mejor[0]:
                    mejor = ((a & b).sum() / u, 10 + dx, 50 + dy, s)
    _, x0, y0, s = mejor

    mm_x, mm_y = (xx - x0) / s, (yy - y0) / s
    dentro = contains_xy(util, mm_x, mm_y)
    a = contains_xy(cobre, mm_x, mm_y) & dentro
    b = suyo & dentro

    print(f"encuadre  : origen ({x0}, {y0}) px, {s:.2f} px/mm  -> 1 px = {1000/s:.0f} um")
    print(f"area      : {a.sum()} px calculada, {b.sum()} px de referencia  "
          f"-> difieren {abs(int(a.sum())-int(b.sum()))/b.sum()*100:.2f} %")
    print(f"IoU       : {(a & b).sum() / (a | b).sum() * 100:.2f} %")
    for r in (1, 2):
        sobra = (a & ~binary_dilation(b, iterations=r)).sum() + \
                (b & ~binary_dilation(a, iterations=r)).sum()
        print(f"  con tolerancia de {r} px ({r*1000/s:.0f} um): "
              f"{sobra / b.sum() * 100:.2f} % del área")
    print("\nUna discrepancia que sobrevive a 1-2 px es geometría distinta.")
    print("Una que desaparece es solo el borde del rasterizado.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "assets/brazos/electronica/kicad-v3")
