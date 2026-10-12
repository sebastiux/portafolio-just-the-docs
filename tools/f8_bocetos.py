#!/usr/bin/env python3
"""F8 (B02) — Bocetos de concepto de los dos brazos, vista lateral.

Trazo a mano alzada (modo xkcd de matplotlib) con las proporciones reales:
largo de eslabones y altura del hombro salen del CAD de cada brazo.

Uso:    python3 tools/f8_bocetos.py
Salida: assets/img/brazos/bocetos/boceto-{impreso,laser}.png
"""
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(RAIZ, "assets/img/brazos/bocetos")
ROJO, AZUL, GRIS = "#E00034", "#1D4ED8", "#4B5563"


def punto(origen, largo, ang):
    return origen[0] + largo * math.cos(math.radians(ang)), origen[1] + largo * math.sin(math.radians(ang))


def servo(ax, x, y, ang=0, nota=None, dx=14, dy=-22):
    ax.add_patch(Rectangle((x - 6, y - 11), 12, 22, angle=0, color=AZUL, alpha=0.85, zorder=4))
    if nota:
        ax.annotate(nota, (x, y), xytext=(x + dx, y + dy), fontsize=9, color=AZUL,
                    arrowprops=dict(arrowstyle="->", color=AZUL, lw=1))


def cota(ax, a, b, texto, desplaz=8):
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    ox, oy = -dy / n * desplaz, dx / n * desplaz
    ax.annotate("", (b[0] + ox, b[1] + oy), (a[0] + ox, a[1] + oy),
                arrowprops=dict(arrowstyle="<->", color=GRIS, lw=1))
    ax.text((a[0] + b[0]) / 2 + ox * 1.8, (a[1] + b[1]) / 2 + oy * 1.8, texto, fontsize=9,
            color=GRIS, ha="center", va="center")


def mesa(ax, x0, x1):
    ax.plot([x0, x1], [0, 0], color="black", lw=2)
    for x in range(int(x0), int(x1), 12):
        ax.plot([x, x - 6], [0, -6], color="black", lw=0.8)


def impreso():
    fig, ax = plt.subplots(figsize=(8, 6))
    mesa(ax, -70, 230)
    # Base y tapa giratoria
    ax.add_patch(FancyBboxPatch((-22, 0), 44, 24, boxstyle="round,pad=1", fc="#d1d5db", ec="black"))
    ax.add_patch(FancyBboxPatch((-19, 24), 38, 12, boxstyle="round,pad=1", fc="#fecdd3", ec="black"))
    servo(ax, 0, 12, nota="servo de giro\n(dentro de la base)")
    hombro = (0, 50)
    ax.plot([-8, -8, 8, 8], [36, 54, 54, 36], color="black", lw=1.5)          # horquilla
    codo = punto(hombro, 80, 62)
    muneca = punto(codo, 90, -8)
    ax.plot(*zip(hombro, codo), color="#F59E0B", lw=7, solid_capstyle="round")
    ax.plot(*zip(codo, muneca), color="#2563EB", lw=7, solid_capstyle="round")
    servo(ax, *hombro, nota="servo del hombro")
    servo(ax, *codo, nota="servo del codo")
    # Soporte y pinza con engranes
    punta = punto(muneca, 30, -8)
    ax.plot(*zip(muneca, punta), color="#10B981", lw=5)
    servo(ax, *muneca, nota="servo de pinza\n+ piñón 20 mm / 28 mm", dx=-20, dy=38)
    for s in (+1, -1):
        p1 = (punta[0], punta[1] + s * 4)
        p2 = punto(p1, 42, -8 + s * 12)
        ax.plot(*zip(p1, p2), color="#0EA5E9", lw=4)
    ax.add_patch(plt.Circle(punto(punta, 46, -8), 9, fc="none", ec=ROJO, ls="--", lw=1.5))
    ax.text(*punto(punta, 46, -30), "objeto", color=ROJO, fontsize=9, ha="center")
    cota(ax, hombro, codo, "80 mm")
    cota(ax, codo, muneca, "90 mm")
    ax.annotate("", (-45, 50), (-45, 0), arrowprops=dict(arrowstyle="<->", color=GRIS))
    ax.text(-62, 25, "≈50 mm", color=GRIS, fontsize=9, rotation=90, va="center")
    ax.set_title("Brazo impreso en 3D · boceto de concepto (vista lateral)", fontsize=12)
    fin(fig, ax, "boceto-impreso.png", (-75, 235), (-15, 160))


def laser():
    fig, ax = plt.subplots(figsize=(8, 6))
    mesa(ax, -90, 220)
    ax.add_patch(Rectangle((-72, 0), 145, 6, fc="#e7c9a0", ec="black"))      # base de MDF
    ax.add_patch(Rectangle((-28, 6), 56, 36, fc="#f3dfc1", ec="black"))      # cuerpo giratorio
    servo(ax, 0, 20, nota="servo de giro", dx=40, dy=-14)
    hombro = (0, 58)
    servo(ax, -16, 46, nota="servos de hombro y codo\n(abajo, en la base)", dx=40, dy=10)
    codo = punto(hombro, 80, 70)
    muneca = punto(codo, 80, -12)
    ax.plot(*zip(hombro, codo), color="#b07d3c", lw=6, solid_capstyle="round")
    ax.plot(*zip(codo, muneca), color="#b07d3c", lw=6, solid_capstyle="round")
    # Paralelogramo: barra paralela que mantiene la pinza horizontal
    d = punto((0, 0), 14, -20)
    p_a, p_b = (hombro[0] + d[0], hombro[1] + d[1]), (codo[0] + d[0], codo[1] + d[1])
    ax.plot(*zip(p_a, p_b), color=GRIS, lw=2, ls="--")
    ax.plot(*zip(hombro, p_a), color=GRIS, lw=1.5)
    ax.plot(*zip(codo, p_b), color=GRIS, lw=1.5)
    ax.text(*punto(p_a, 40, 70), "paralelogramo", color=GRIS, fontsize=9, rotation=70)
    punta = punto(muneca, 18, 0)
    ax.plot(*zip(muneca, punta), color="#b07d3c", lw=6)
    for s in (+1, -1):
        p1 = (punta[0], punta[1] + s * 3)
        ax.plot(*zip(p1, punto(p1, 30, s * 10)), color="#8b5a2b", lw=4)
    servo(ax, *muneca, nota="servo de pinza")
    ax.add_patch(plt.Circle(punto(punta, 34, 0), 9, fc="none", ec=ROJO, ls="--", lw=1.5))
    ax.text(*punto(punta, 34, -25), "objeto", color=ROJO, fontsize=9, ha="center")
    cota(ax, hombro, codo, "≈80 mm")
    cota(ax, codo, muneca, "≈80 mm")
    ax.annotate("", (-80, 6), (75, 6), arrowprops=dict(arrowstyle="<->", color=GRIS))
    ax.text(0, -16, "base 145 × 90.7 mm (MDF 3 mm)", color=GRIS, fontsize=9, ha="center")
    ax.set_title("Brazo de corte láser (MeArm) · boceto de concepto (vista lateral)", fontsize=12)
    fin(fig, ax, "boceto-laser.png", (-95, 225), (-25, 175))


def fin(fig, ax, nombre, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    os.makedirs(DEST, exist_ok=True)
    fig.savefig(os.path.join(DEST, nombre), dpi=130, facecolor="white")
    plt.close(fig)
    print("  " + nombre)


if __name__ == "__main__":
    with plt.xkcd(scale=0.6, length=120, randomness=2):
        impreso()
        laser()
