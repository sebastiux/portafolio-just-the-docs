#!/usr/bin/env python3
"""F3 (R2) — Render isométrico de cada pieza del brazo impreso, y su tabla.

Las piezas ya existen como STL; aquí solo se miden y se renderizan, con el
mismo tratamiento que las del brazo de corte láser.

    xvfb-run -a python3 tools/f3_salidas_piezas_impreso.py
"""
import json, os, sys
import numpy as np, trimesh
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from piezas_impreso import PIEZAS

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STL = os.path.join(RAIZ, "assets/stl/brazo-impreso")
D_PNG = os.path.join(RAIZ, "assets/brazos/impreso3d/render/piezas")
DATOS = os.path.join(RAIZ, "assets/brazos/impreso3d")
DENSIDAD_PLA = 1.24      # g/cm3


def main():
    os.makedirs(D_PNG, exist_ok=True)
    import pyvista as pv
    tabla = []
    for pid, archivo, cad, nombre, color in PIEZAS:
        m = trimesh.load(os.path.join(STL, archivo))
        pl = pv.Plotter(off_screen=True, window_size=(800, 600))
        pl.set_background("#f5f6f8")
        pl.add_mesh(pv.wrap(m), color=color, smooth_shading=False,
                    specular=0.2, specular_power=10)
        pl.enable_parallel_projection()
        pl.view_isometric()
        pl.camera.zoom(1.35)
        pl.screenshot(os.path.join(D_PNG, f"{pid}.png"))
        pl.close()
        v = m.volume / 1000.0
        tabla.append({"id": pid, "archivo": archivo, "cad": cad, "nombre": nombre,
                      "color": color,
                      "dim_mm": [round(float(x), 2) for x in m.extents],
                      "volumen_cm3": round(v, 2),
                      "masa_max_g": round(v * DENSIDAD_PLA, 1),
                      "triangulos": len(m.faces),
                      "cerrada": bool(m.is_watertight)})
        print(f"  {pid} {nombre:26s} {m.extents[0]:6.2f} x {m.extents[1]:6.2f} x {m.extents[2]:5.2f} mm  "
              f"{v:5.2f} cm3  {len(m.faces):6d} tri  cerrada={m.is_watertight}")
    with open(os.path.join(DATOS, "tabla-piezas.json"), "w", encoding="utf-8") as f:
        json.dump(tabla, f, ensure_ascii=False, indent=1)
    vol = sum(t["volumen_cm3"] for t in tabla)
    print(f"\n{len(tabla)} piezas | {vol:.2f} cm3 de PLA | masa máxima {vol*DENSIDAD_PLA:.1f} g")


if __name__ == "__main__":
    sys.exit(main())
