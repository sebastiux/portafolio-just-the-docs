#!/usr/bin/env python3
"""R4 (B02) — Boceto de concepto del rover con la propuesta de materiales.

Trazo a mano alzada (modo xkcd). La suspensión sale de las cotas reales del
ensamble generado por r1_uniones_rover.py (assets/stl/rover/datos.json); el
cuerpo, el mástil y el brazo son volúmenes de concepto, sin cotas.

Uso:    python3 tools/r4_boceto_rover.py
Salida: assets/img/rover/mecanica/boceto-rover.png
"""
import json
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(RAIZ, "assets/stl/rover/datos.json")
DEST = os.path.join(RAIZ, "assets/img/rover/mecanica/boceto-rover.png")
ROJO, AZUL, GRIS, ALU, NEGRO, AMBAR = "#E00034", "#1D4ED8", "#4B5563", "#9CA3AF", "#1F2937", "#F59E0B"


def nota(ax, texto, xy, xytext, color=GRIS):
    ax.annotate(texto, xy, xytext=xytext, fontsize=9, color=color,
                arrowprops=dict(arrowstyle="->", color=color, lw=1))


def main():
    e = json.load(open(DATOS, encoding="utf-8"))["ensamble"]
    R = 76
    xs = e["ejes_x_mm"]
    pr = (e["pivote_balancin_mm"][0], e["pivote_balancin_mm"][2])
    pb = (e["pivote_bogie_mm"][0], e["pivote_bogie_mm"][2])
    ruedas = [(xs["delantera"], R), (xs["media"], R), (xs["trasera"], R)]

    fig, ax = plt.subplots(figsize=(10, 6.2))
    ax.plot([-420, 430], [0, 0], color="black", lw=2)
    for x in range(-420, 430, 18):
        ax.plot([x, x - 8], [0, -8], color="black", lw=0.7)

    # Cuerpo (caja de electrónica) colgado del pivote del balancín
    ax.add_patch(FancyBboxPatch((-230, pr[1] + 25), 420, 120, boxstyle="round,pad=4", fc="#E5E7EB", ec="black"))
    ax.text(-20, pr[1] + 85, "cuerpo: Pi 4, 3 × ESP32,\nLiPo 3S, tolva", ha="center", va="center", fontsize=9)
    # Mástil y cámara
    ax.plot([-170, -170], [pr[1] + 150, pr[1] + 250], color="black", lw=2)
    ax.add_patch(Rectangle((-195, pr[1] + 250), 50, 30, fc="#D1D5DB", ec="black"))
    nota(ax, "cámara (FPV)", (-170, pr[1] + 280), (-330, pr[1] + 300))
    # Brazo al frente
    hombro = (170, pr[1] + 120)
    codo = (300, pr[1] + 170)
    pinza = (380, pr[1] + 40)
    ax.plot(*zip(hombro, codo), color=GRIS, lw=5)
    ax.plot(*zip(codo, pinza), color=GRIS, lw=5)
    ax.plot([pinza[0], pinza[0] + 20], [pinza[1], pinza[1] - 25], color=GRIS, lw=3)
    ax.plot([pinza[0], pinza[0] - 5], [pinza[1], pinza[1] - 30], color=GRIS, lw=3)
    nota(ax, "brazo (sin cambio de material)", codo, (220, pr[1] + 280))

    # Suspensión balancín-bogie (cotas del ensamble)
    for a, b in ((pr, ruedas[0]), (pr, pb), (pb, ruedas[1]), (pb, ruedas[2])):
        ax.plot(*zip(a, b), color=ALU, lw=7, solid_capstyle="round")
    for p, c in ((pr, ROJO), (pb, AMBAR)):
        ax.add_patch(Circle(p, 18, fc=c, ec="black", zorder=5))
        ax.add_patch(Circle(p, 6, fc="white", ec="black", zorder=6))
    for x, z in ruedas:
        ax.add_patch(Circle((x, z), R, fc=NEGRO, ec="black", zorder=3))
        ax.add_patch(Circle((x, z), 65, fc=AZUL, ec="black", zorder=4))
        ax.add_patch(Circle((x, z), 12, fc="#93C5FD", ec="black", zorder=5))
        for k in range(16):
            a = 2 * math.pi * k / 16
            ax.plot([x + 68 * math.cos(a), x + 82 * math.cos(a)], [z + 68 * math.sin(a), z + 82 * math.sin(a)],
                    color=NEGRO, lw=3, zorder=3)

    nota(ax, "tubo Al 6063 Ø30 × 1.5\n(eslabones)", (150, 166), (240, 250), "#6B7280")
    nota(ax, "pivote PETG\n+ 2 rodamientos 608", pr, (40, pr[1] - 20), ROJO)
    nota(ax, "bogie: pivote PETG", pb, (-430, pb[1] + 125), AMBAR)
    nota(ax, "rin PETG", (xs["trasera"] - 40, R + 30), (-430, 205), AZUL)
    nota(ax, "llanta Ecoflex 00-20\ncon 16 tacos", (xs["trasera"] - 70, 30), (-430, 255), NEGRO)
    ax.annotate("", (xs["delantera"], -40), (xs["trasera"], -40), arrowprops=dict(arrowstyle="<->", color=GRIS))
    ax.text(0, -58, f"{e['distancia_entre_ejes_mm']:.0f} mm entre ejes · rueda Ø152", ha="center", fontsize=9, color=GRIS)

    ax.set_title("Rover · boceto de concepto con la propuesta de materiales (vista lateral)", fontsize=12)
    ax.set_xlim(-430, 440)
    ax.set_ylim(-75, pr[1] + 320)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(DEST, dpi=120, facecolor="white")
    print("  " + os.path.relpath(DEST, RAIZ))


if __name__ == "__main__":
    with plt.xkcd(scale=0.6, length=120, randomness=2):
        main()
