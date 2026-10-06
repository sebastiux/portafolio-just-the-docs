#!/usr/bin/env python3
"""F3 (R1) — Un plano A4 por pieza del brazo impreso, más el plano resumen.

A diferencia del brazo de corte láser, estas piezas no son planas, así que el
plano lleva tres vistas (planta, alzado y lateral) a la misma escala. Las
vistas son SILUETAS proyectadas de la malla: contorno exterior, sin aristas
internas ni líneas ocultas. Son suficientes para identificar y acotar la
pieza, pero no son un plano de taller con cortes y tolerancias.

Salida: assets/brazos/impreso3d/planos/<id>.pdf
        assets/brazos/impreso3d/planos/planos-brazo-impreso-completo.pdf
"""
import json, os, sys
import numpy as np, trimesh
from trimesh.path import polygons as tp
from shapely.affinity import translate
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from piezas_impreso import PIEZAS

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STL = os.path.join(RAIZ, "assets/stl/brazo-impreso")
DEST = os.path.join(RAIZ, "assets/brazos/impreso3d/planos")

A4 = (8.2677, 11.6929)
FACTORES = [10, 5, 2, 1, 1/2, 1/2.5, 1/5, 1/10]
# La separación entre vistas y el espacio de cotas se calculan a partir del
# tamaño de la pieza, no con una constante: con un valor fijo los rótulos de
# una vista caían encima de otra.
MATERIAL = "PLA, impresión 3D (FDM)"
EQUIPO = "Juan Pablo Martha · Carlos Sebastián Ortega · Santiago Alejandro Velázquez"
MATERIA = "Integración Mecatrónica Otoño 2026"
PROFESOR = "Dr. Huber Girón"
ENTREGA = "12/10/2026"
CREDITO = "Diseño base: «Brazo Robótico», RACBOTS, Printables #449747, CC BY 4.0"
DIB = dict(x0=0.55, y0=2.30, w=7.17, h=8.85)


def siluetas(m):
    """Contorno proyectado en los tres planos principales."""
    return {"planta": tp.projected(m, normal=[0, 0, 1]),
            "alzado": tp.projected(m, normal=[0, -1, 0]),
            "lateral": tp.projected(m, normal=[1, 0, 0])}


def etiqueta(f):
    if f == 1:
        return "1:1"
    return f"{f:g}:1" if f > 1 else f"1:{1/f:g}"


def plano(fig, pid, nombre, cad, m):
    dx, dy, dz = m.extents
    sep = max(3.5, 0.07 * max(dx, dy, dz))   # espacio de cotas y rótulos
    hueco = 3.2 * sep                        # separación entre vistas
    W = dx + hueco + dy       # ancho total del conjunto de vistas, en mm de pieza
    H = dy + hueco + dz
    cajaW, cajaH = DIB["w"] * 25.4 * 0.84, DIB["h"] * 25.4 * 0.84
    f = next((k for k in FACTORES if W * k <= cajaW and H * k <= cajaH), FACTORES[-1])

    ax = fig.add_axes([DIB["x0"]/A4[0], DIB["y0"]/A4[1], DIB["w"]/A4[0], DIB["h"]/A4[1]])
    ax.set_aspect("equal"); ax.axis("off")
    anchoMM, altoMM = DIB["w"] * 25.4 / f, DIB["h"] * 25.4 / f
    ax.set_xlim(W/2 - anchoMM/2, W/2 + anchoMM/2)
    ax.set_ylim(H/2 - altoMM/2, H/2 + altoMM/2)

    sil = siluetas(m)
    def dibujar(poly, ox, oy, titulo, w, h):
        b = poly.bounds
        poly = translate(poly, ox - b[0], oy - b[1])
        for geom in (poly.geoms if poly.geom_type == "MultiPolygon" else [poly]):
            ax.fill(*geom.exterior.xy, fc="#eceff3", ec="#111", lw=1.0, zorder=2)
            for hueco in geom.interiors:
                ax.fill(*hueco.xy, fc="white", ec="#111", lw=0.8, zorder=3)
        ax.annotate("", (ox, oy - sep*0.55), (ox + w, oy - sep*0.55),
                    arrowprops=dict(arrowstyle="<->", lw=0.7))
        ax.text(ox + w/2, oy - sep*0.75, f"{w:.2f}", ha="center", va="top", fontsize=7)
        ax.text(ox + w/2, oy - sep*1.55, titulo, ha="center", va="top",
                fontsize=8, color="#444", zorder=4)
        ax.annotate("", (ox - sep*0.55, oy), (ox - sep*0.55, oy + h),
                    arrowprops=dict(arrowstyle="<->", lw=0.7))
        ax.text(ox - sep*0.75, oy + h/2, f"{h:.2f}", ha="right", va="center",
                fontsize=7, rotation=90)

    dibujar(sil["planta"], 0, 0, "Planta", dx, dy)
    dibujar(sil["alzado"], 0, dy + hueco, "Alzado", dx, dz)
    dibujar(sil["lateral"], dx + hueco, dy + hueco, "Lateral", dy, dz)

    tb = fig.add_axes([0.55/A4[0], 0.45/A4[1], 7.17/A4[0], 1.70/A4[1]])
    tb.axis("off")
    tb.add_patch(plt.Rectangle((0, 0), 1, 1, fill=False, lw=1.1, transform=tb.transAxes))
    tb.plot([0, 1], [0.62, 0.62], lw=0.7, color="black", transform=tb.transAxes)
    tb.plot([0.56, 0.56], [0.62, 1], lw=0.7, color="black", transform=tb.transAxes)
    t = lambda x, y, s, **k: tb.text(x, y, s, transform=tb.transAxes, **k)
    t(0.02, 0.86, pid, fontsize=19, fontweight="bold", va="center")
    t(0.02, 0.70, f"{nombre}   ·   {cad}", fontsize=9, va="center", color="#333")
    t(0.58, 0.90, f"Escala  {etiqueta(f)}", fontsize=9, va="center")
    t(0.58, 0.80, f"Medidas  {dx:.2f} × {dy:.2f} × {dz:.2f} mm", fontsize=9, va="center")
    t(0.58, 0.70, f"Material  {MATERIAL}", fontsize=9, va="center")
    t(0.02, 0.50, f"Volumen {m.volume/1000:.2f} cm³  ·  masa máxima en PLA "
                  f"{m.volume/1000*1.24:.1f} g  ·  vistas de silueta, sin líneas ocultas",
      fontsize=8.5, va="center")
    t(0.02, 0.34, f"{MATERIA}  ·  Prof. {PROFESOR}  ·  Entrega {ENTREGA}", fontsize=8, va="center")
    t(0.02, 0.21, EQUIPO, fontsize=7.5, va="center", color="#333")
    t(0.02, 0.08, CREDITO, fontsize=7, va="center", color="#555", style="italic")
    t(0.98, 0.08, "Cotas en mm", fontsize=7, va="center", ha="right", color="#555")


def main():
    os.makedirs(DEST, exist_ok=True)
    todas = []
    for pid, archivo, cad, nombre, _ in PIEZAS:
        m = trimesh.load(os.path.join(STL, archivo))
        m.apply_translation(-m.bounds[0])
        todas.append((pid, nombre, cad, m))
        fig = plt.figure(figsize=A4)
        plano(fig, pid, nombre, cad, m)
        fig.savefig(os.path.join(DEST, f"{pid}.pdf"))
        plt.close(fig)
        print(f"  {pid}.pdf  {nombre}")
    with PdfPages(os.path.join(DEST, "planos-brazo-impreso-completo.pdf")) as pdf:
        for pid, nombre, cad, m in todas:
            fig = plt.figure(figsize=A4)
            plano(fig, pid, nombre, cad, m)
            pdf.savefig(fig); plt.close(fig)
    tam = os.path.getsize(os.path.join(DEST, "planos-brazo-impreso-completo.pdf"))
    print(f"\nplano resumen: {len(todas)} páginas, {tam/1e6:.2f} MB")


if __name__ == "__main__":
    sys.exit(main())
