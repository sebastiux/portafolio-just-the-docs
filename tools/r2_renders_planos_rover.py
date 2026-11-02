#!/usr/bin/env python3
"""R2 (B06 · B08) — Renders y planos de las uniones, rin y llanta del rover.

Renders: pyvista (VTK) fuera de pantalla.
Planos:  corte por el plano medio de la pieza (XZ, o XY para la rueda)
         con las cotas que salen de los parámetros de r1_uniones_rover.py.

Uso:    python3 tools/r1_uniones_rover.py && xvfb-run -a python3 tools/r2_renders_planos_rover.py
Salida: assets/img/rover/mecanica/{render,plano}-*.png
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from matplotlib.patches import Polygon

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r1_uniones_rover as P  # noqa: E402

RAIZ = P.RAIZ
STL = os.path.join(RAIZ, "assets/stl/rover")
DEST = os.path.join(RAIZ, "assets/img/rover/mecanica")
GRIS = "#4B5563"

PIEZAS = [
    # archivo, título, color, vista (elev, azim), plano de corte (normal), cotas
    ("uniones/codo-90.stl", "Codo 90°", "#E00034", (25, -60), "y"),
    ("uniones/codo-120.stl", "Codo 120°", "#E00034", (25, -60), "y"),
    ("uniones/union-t.stl", "Unión T", "#E00034", (25, -60), "y"),
    ("uniones/cople-recto.stl", "Cople recto", "#E00034", (25, -60), "y"),
    ("uniones/pivote.stl", "Pivote con 2 × 608", "#E00034", (20, -55), "y"),
    ("uniones/terminal-eje.stl", "Terminal de eje M8", "#E00034", (20, -55), "y"),
    ("uniones/terminal-motor.stl", "Terminal de motor Ø37", "#E00034", (20, -35), "y"),
    ("uniones/probeta-ajuste.stl", "Probeta de ajuste", "#E00034", (45, -70), None),
    ("rueda/rin.stl", "Rin", "#1D4ED8", (30, -60), "y"),
    ("rueda/llanta-ecoflex.stl", "Llanta Ecoflex 00-20", "#1F2937", (30, -60), "y"),
    ("rueda/molde-llanta-mitad.stl", "Medio molde de la llanta", "#F59E0B", (30, -120), None),
]


def render(m, color, vista, ruta, titulo):
    """Render sombreado con pyvista (VTK). Necesita pantalla: xvfb-run -a."""
    import pyvista as pv
    malla = pv.wrap(m)
    p = pv.Plotter(off_screen=True, window_size=(900, 760))
    p.set_background("white")
    p.add_mesh(malla, color=color, smooth_shading=False, specular=0.25, specular_power=12)
    p.enable_parallel_projection()
    p.view_isometric()
    p.camera.elevation = vista[0] - 30
    p.camera.azimuth = vista[1] + 45
    p.reset_camera()
    p.camera.zoom(0.95)
    p.add_text(titulo, position="upper_edge", font_size=12, color="#111827")
    p.screenshot(ruta)
    p.close()


def corte(m, normal):
    n = {"x": [1, 0, 0], "y": [0, 1, 0], "z": [0, 0, 1]}[normal]
    sec = m.section(plane_origin=[0, 0, 0], plane_normal=n)
    if normal == "x":
        T = np.array([[0, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 0, 1]], float)
    elif normal == "y":
        T = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, -1, 0, 0], [0, 0, 0, 1]], float)
    else:
        T = np.eye(4)
    plano, _ = sec.to_2D(to_2D=T)
    return plano


def plano(m, normal, ruta, titulo, notas):
    fig, (ax, at) = plt.subplots(1, 2, figsize=(9, 4.6), gridspec_kw={"width_ratios": [1.5, 1]})
    p = corte(m, normal)
    for poli in p.polygons_full:
        ax.add_patch(Polygon(np.array(poli.exterior.coords), fc="#fde2e7", ec="black", lw=1.1, hatch="///"))
        for h in poli.interiors:
            ax.add_patch(Polygon(np.array(h.coords), fc="white", ec="black", lw=1.1))
    lo, hi = p.bounds
    ax.set_xlim(lo[0] - 8, hi[0] + 8)
    ax.set_ylim(lo[1] - 8, hi[1] + 8)
    ax.set_aspect("equal")
    ax.grid(True, color="#e5e7eb", lw=0.6)
    ax.tick_params(labelsize=7)
    ax.set_xlabel("mm", fontsize=8)
    eje = {"x": "YZ", "y": "XZ", "z": "XY"}[normal]
    ax.set_title(f"Corte por el plano {eje} medio", fontsize=10)
    at.axis("off")
    at.set_title(titulo, fontsize=11, loc="left")
    filas = [[k, v] for k, v in notas]
    t = at.table(cellText=filas, colWidths=[0.55, 0.45], loc="upper left", cellLoc="left")
    t.auto_set_font_size(False)
    t.set_fontsize(8.5)
    t.scale(1, 1.35)
    fig.tight_layout()
    fig.savefig(ruta, dpi=120, facecolor="white")
    plt.close(fig)


def main():
    os.makedirs(DEST, exist_ok=True)
    datos = json.load(open(os.path.join(STL, "datos.json"), encoding="utf-8"))
    comun = [
        ["Barreno del casquillo", f"Ø{2 * P.R_BORE:.1f} mm"],
        ["Pared del casquillo", f"{P.PARED:.1f} mm"],
        ["Profundidad del casquillo", f"{P.PROF:.0f} mm"],
        ["Tope del tubo al centro", f"{P.S0:.0f} mm"],
        ["Tornillo pasante", "M4 pasante + tuerca"],
    ]
    extra = {
        "codo-90": [["Ángulo entre tubos", "90°"], ["Canal de cables", f"Ø{2 * P.R_CABLE:.0f} mm"]],
        "codo-120": [["Ángulo entre tubos", "120°"], ["Canal de cables", f"Ø{2 * P.R_CABLE:.0f} mm"]],
        "union-t": [["Vías", "3 (180° + 90°)"], ["Canal de cables", f"Ø{2 * P.R_CABLE:.0f} mm"]],
        "cople-recto": [["Tope central", "3 mm por lado"]],
        "pivote": [["Ángulo entre patas", f"{2 * P.SEMIANGULO:.0f}°"],
                   ["Rodamientos", "2 × 608 (Ø22 × 7)"], ["Asiento del rodamiento", f"Ø{2 * P.R_608:.2f} × {P.ANCHO_608} mm"],
                   ["Ancho del cubo", f"{P.ANCHO_PIVOTE:.0f} mm"], ["Salida de cables", "Ø10, una por pata"]],
        "terminal-eje": [["Barreno del eje", "Ø8.2 (eje M8)"], ["Ancho de la oreja", "20 mm"], ["Tope del tubo", "14 mm"]],
        "terminal-motor": [["Abrazadera", f"Ø{2 * P.R_MOTOR:.1f} × 30 mm"], ["Cierre", "2 × M3"],
                           ["Tope del tubo", f"{P.R_MOTOR + 8:.1f} mm"]],
        "rin": [["Diámetro del núcleo", f"Ø{2 * P.R_NUCLEO:.0f} mm"], ["Diámetro de pestañas", f"Ø{2 * P.R_PESTANA:.0f} mm"],
                ["Ancho", f"{P.ANCHO_RUEDA:.0f} mm"], ["Costillas de arrastre", f"{P.N_TACOS} × 4 × 4 mm"],
                ["Flecha", "Ø6 en D + M3"]],
        "llanta-ecoflex": [["Diámetro exterior", f"Ø{2 * P.R_TACO:.0f} mm"], ["Diámetro de banda", f"Ø{2 * P.R_BANDA:.0f} mm"],
                           ["Tacos (grousers)", f"{P.N_TACOS} × {P.ANCHO_TACO:.0f} × {P.R_TACO - P.R_BANDA:.0f} mm"],
                           ["Ancho de rodadura", f"{P.ANCHO_RUEDA:.0f} mm"]],
    }
    for archivo, titulo, color, vista, normal in PIEZAS:
        m = trimesh.load(os.path.join(STL, archivo))
        base = os.path.splitext(os.path.basename(archivo))[0]
        render(m, color, vista, os.path.join(DEST, f"render-{base}.png"), titulo)
        if normal:
            d = datos["piezas"][archivo]
            propias = extra.get(base, [])
            base_c = [] if archivo.startswith("rueda") else comun
            if any(k == "Tope del tubo" for k, _ in propias):
                base_c = [f for f in base_c if f[0] != "Tope del tubo al centro"]
            notas = base_c + propias + [
                ["Envolvente", " × ".join(f"{v:g}" for v in d["envolvente_mm"]) + " mm"],
                ["Volumen sólido", f"{d['volumen_cm3']} cm³"],
            ]
            plano(m, normal, os.path.join(DEST, f"plano-{base}.png"), titulo, notas)
        print("  " + base)


if __name__ == "__main__":
    main()
