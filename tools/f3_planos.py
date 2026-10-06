#!/usr/bin/env python3
"""F3 (R1) — Un plano A4 por pieza, más el plano resumen.

Los planos salen de los contornos DXF, que es lo que se cortó, no del modelo
3D de GrabCAD. El nombre de la pieza se toma del STEP solo cuando el
emparejamiento difiere 2 mm o menos; si no, la pieza va solo con su número.

Salida: assets/brazos/laser/planos/<id>.pdf
        assets/brazos/laser/planos/planos-mearm-completo.pdf
"""
import json, os, sys
import ezdxf
import numpy as np
from shapely import wkt as swkt
from shapely.geometry import Polygon
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORTE = os.path.join(RAIZ, "assets/brazos/laser/corte")
DXF_IN = os.path.join(RAIZ, "_entrada_brazos/laser/dxf")
HOJAS = {"A": "Mearm_1_0_150x200_A.dxf", "B": "Mearm_1_0_150x200_B.dxf"}
DEST = os.path.join(RAIZ, "assets/brazos/laser/planos")

A4 = (8.2677, 11.6929)                      # pulgadas, vertical
# Factores normalizados: >1 amplía, <1 reduce. Una pieza de 3 mm a 1:1 es
# un punto perdido en la A4, así que las pequeñas se dibujan ampliadas.
FACTORES = [10, 5, 2, 1, 1/2, 1/2.5, 1/5, 1/10]
ESPESOR, MATERIAL = 3.0, "MDF 3 mm"
EQUIPO = "Juan Pablo Martha · Carlos Sebastián Ortega · Santiago Alejandro Velázquez"
MATERIA = "Integración Mecatrónica Otoño 2026"
PROFESOR = "Dr. Huber Girón"
ENTREGA = "12/10/2026"
CREDITO = "Diseño: MeArm v1.0, Benjamin Gray (Mime Industries), CC BY 4.0"
# Caja de dibujo dentro de la A4, en pulgadas
DIB = dict(x0=0.55, y0=2.30, w=7.17, h=8.85)


def circulos_dxf():
    """Diámetros nominales, leídos de las entidades CIRCLE de cada hoja.

    No se miden sobre el contorno procesado: aplanar la curva y redondear a
    0.02 mm para cerrar los contornos desvía el diámetro hasta 0.02 mm
    (Ø2.67 donde el diseño dice Ø2.65). El DXF trae el radio exacto.
    """
    salida = {}
    for tag, archivo in HOJAS.items():
        salida[tag] = [((c.dxf.center.x, c.dxf.center.y), round(c.dxf.radius * 2, 2))
                       for c in ezdxf.readfile(os.path.join(DXF_IN, archivo)).modelspace()
                       if c.dxftype() == "CIRCLE"]
    return salida


def agujeros(poly, circulos):
    """Agrupa los agujeros por diámetro nominal, o los describe como recorte."""
    circ, recortes = {}, {}
    for anillo in poly.interiors:
        h = Polygon(anillo)
        A, P = h.area, h.length
        if P and 4 * np.pi * A / (P * P) > 0.93:
            c = h.centroid
            cerca = [d for (cx, cy), d in circulos
                     if (cx - c.x) ** 2 + (cy - c.y) ** 2 < 0.25]
            d = cerca[0] if cerca else round(float(2 * np.sqrt(A / np.pi)), 2)
            circ[d] = circ.get(d, 0) + 1
        else:
            r = np.array(h.minimum_rotated_rectangle.exterior.coords)
            lad = np.linalg.norm(np.diff(r, axis=0), axis=1)[:2]
            k = (round(float(max(lad)), 1), round(float(min(lad)), 1))
            recortes[k] = recortes.get(k, 0) + 1
    return circ, recortes


def escala_para(an, al):
    """Mayor factor normalizado con el que la pieza cabe en la caja de dibujo."""
    for f in FACTORES:
        if an * f <= DIB["w"] * 25.4 * 0.86 and al * f <= DIB["h"] * 25.4 * 0.86:
            return f
    return FACTORES[-1]


def etiqueta_escala(f):
    if f == 1:
        return "1:1"
    return f"{f:g}:1" if f > 1 else f"1:{1/f:g}"


def plano(fig, pid, nombre, poly, circulos=()):
    an, al = poly.bounds[2], poly.bounds[3]
    f = escala_para(an, al)
    ax = fig.add_axes([DIB["x0"]/A4[0], DIB["y0"]/A4[1], DIB["w"]/A4[0], DIB["h"]/A4[1]])
    ancho_mm = DIB["w"] * 25.4 / f             # mm de pieza que caben a lo ancho
    alto_mm = DIB["h"] * 25.4 / f
    cx, cy = an / 2, al / 2
    ax.set_xlim(cx - ancho_mm/2, cx + ancho_mm/2)
    ax.set_ylim(cy - alto_mm/2, cy + alto_mm/2)
    ax.set_aspect("equal"); ax.axis("off")
    ax.fill(*poly.exterior.xy, fc="#eceff3", ec="#111", lw=1.1, zorder=1)
    for h in poly.interiors:
        ax.fill(*h.xy, fc="white", ec="#111", lw=0.9, zorder=2)
    # cotas generales
    o = max(an, al) * 0.07 + ancho_mm * 0.015
    ax.annotate("", (0, -o), (an, -o), arrowprops=dict(arrowstyle="<->", lw=0.8))
    ax.text(an/2, -o - ancho_mm*0.012, f"{an:.2f}", ha="center", va="top", fontsize=8)
    ax.annotate("", (-o, 0), (-o, al), arrowprops=dict(arrowstyle="<->", lw=0.8))
    ax.text(-o - ancho_mm*0.012, al/2, f"{al:.2f}", ha="right", va="center", fontsize=8, rotation=90)
    for x in (0, an):
        ax.plot([x, x], [0, -o], lw=0.4, color="#888", zorder=0)
    for y in (0, al):
        ax.plot([0, -o], [y, y], lw=0.4, color="#888", zorder=0)

    # cuadro de título
    tb = fig.add_axes([0.55/A4[0], 0.45/A4[1], 7.17/A4[0], 1.70/A4[1]])
    tb.axis("off")
    tb.add_patch(plt.Rectangle((0, 0), 1, 1, fill=False, lw=1.1, transform=tb.transAxes))
    tb.plot([0, 1], [0.62, 0.62], lw=0.7, color="black", transform=tb.transAxes)
    tb.plot([0.56, 0.56], [0.62, 1], lw=0.7, color="black", transform=tb.transAxes)
    t = lambda x, y, s, **k: tb.text(x, y, s, transform=tb.transAxes, **k)
    t(0.02, 0.86, pid, fontsize=19, fontweight="bold", va="center")
    t(0.02, 0.70, nombre, fontsize=9.5, va="center", color="#333")
    c, r = agujeros(poly, circulos)
    det = [f"Ø{d} ×{n}" for d, n in sorted(c.items())] + \
          [f"recorte {a}×{b} ×{n}" for (a, b), n in sorted(r.items())]
    t(0.58, 0.90, f"Escala  {etiqueta_escala(f)}", fontsize=9, va="center")
    t(0.58, 0.80, f"Medidas  {an:.2f} × {al:.2f} × {ESPESOR:g} mm", fontsize=9, va="center")
    t(0.58, 0.70, f"Material  {MATERIAL}", fontsize=9, va="center")
    t(0.02, 0.50, "Agujeros:  " + ("  ·  ".join(det) if det else "ninguno"),
      fontsize=8.5, va="center")
    t(0.02, 0.34, f"{MATERIA}  ·  Prof. {PROFESOR}  ·  Entrega {ENTREGA}", fontsize=8, va="center")
    t(0.02, 0.21, EQUIPO, fontsize=7.5, va="center", color="#333")
    t(0.02, 0.08, CREDITO, fontsize=7, va="center", color="#555", style="italic")
    t(0.98, 0.08, "Cotas en mm", fontsize=7, va="center", ha="right", color="#555")


def main():
    os.makedirs(DEST, exist_ok=True)
    piezas = json.load(open(os.path.join(CORTE, "piezas.json"), encoding="utf-8"))
    comp = json.load(open(os.path.join(CORTE, "comparacion-step-dxf.json"), encoding="utf-8"))
    nombres = {p["dxf"]: p["step"] for p in comp["parejas"] if p["dif_mm"] <= 2.0}
    circ_hoja = circulos_dxf()
    print(f"piezas con nombre heredado del STEP (diferencia <= 2 mm): {len(nombres)}")

    todas = []
    for hoja in piezas:
        for p in piezas[hoja]["piezas"]:
            poly = swkt.loads(p["wkt"]); b = poly.bounds
            poly = Polygon([(x - b[0], y - b[1]) for x, y in poly.exterior.coords],
                           [[(x - b[0], y - b[1]) for x, y in h.coords]
                            for h in poly.interiors])
            nombre = nombres.get(p["id"], "Sin nombre en el modelo CAD")
            # los círculos se buscan en coordenadas de hoja y se trasladan igual
            cs = [((cx - b[0], cy - b[1]), d) for (cx, cy), d in circ_hoja[hoja]]
            todas.append((p["id"], nombre, poly, cs))

    for pid, nombre, poly, cs in todas:
        fig = plt.figure(figsize=A4)
        plano(fig, pid, nombre, poly, cs)
        fig.savefig(os.path.join(DEST, f"{pid}.pdf"))
        plt.close(fig)
    print(f"{len(todas)} planos individuales")

    with PdfPages(os.path.join(DEST, "planos-mearm-completo.pdf")) as pdf:
        for tag in piezas:
            fig = plt.figure(figsize=A4)
            ax = fig.add_axes([0.07, 0.07, 0.86, 0.86]); ax.axis("off")
            img = plt.imread(os.path.join(CORTE, f"hoja-{tag.lower()}.png"))
            ax.imshow(img)
            pdf.savefig(fig); plt.close(fig)
        for pid, nombre, poly, cs in todas:
            fig = plt.figure(figsize=A4)
            plano(fig, pid, nombre, poly, cs)
            pdf.savefig(fig); plt.close(fig)
    tam = os.path.getsize(os.path.join(DEST, "planos-mearm-completo.pdf"))
    print(f"plano resumen: {2 + len(todas)} páginas, {tam/1e6:.2f} MB")


if __name__ == "__main__":
    sys.exit(main())
