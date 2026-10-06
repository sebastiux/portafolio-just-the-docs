#!/usr/bin/env python3
"""F2 (R4) — Renders del ensamble del MeArm desde los STL generados.

Requiere pantalla virtual:  xvfb-run -a python3 tools/f2_renders_mearm.py
Salida: assets/brazos/laser/render/ensamble-{iso,lateral,superior}.png
"""
import json, os, sys
import pyvista as pv

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.path.join(RAIZ, "assets/stl/brazo-laser")
DEST = os.path.join(RAIZ, "assets/brazos/laser/render")
TAM = (1600, 1200)


def main():
    spec = json.load(open(os.path.join(ORIG, "ensamble.json"), encoding="utf-8"))
    os.makedirs(DEST, exist_ok=True)
    vistas = {
        "ensamble-iso.png": lambda p: p.view_isometric(),
        "ensamble-lateral.png": lambda p: p.view_xz(),
        "ensamble-superior.png": lambda p: p.view_xy(),
    }
    for archivo, encuadrar in vistas.items():
        p = pv.Plotter(off_screen=True, window_size=TAM)
        p.set_background("#f5f6f8")
        for parte in spec["parts"]:
            malla = pv.read(os.path.join(ORIG, parte["file"]))
            # Sombreado plano: las 31 piezas son placas planas y el suave
            # promedia normales entre triángulos largos, que las abomba.
            p.add_mesh(malla, color=parte["color"], smooth_shading=False,
                       specular=0.2, specular_power=10)
        p.enable_parallel_projection()
        encuadrar(p)
        p.camera.zoom(1.45)   # camera.tight() reencuadra pero pierde la orientación
        p.add_light(pv.Light(position=(1, -1.5, 2), light_type="headlight", intensity=0.45))
        p.screenshot(os.path.join(DEST, archivo))
        p.close()
        print(f"  {archivo}  {os.path.getsize(os.path.join(DEST, archivo))/1e3:.0f} KB")


if __name__ == "__main__":
    sys.exit(main())
