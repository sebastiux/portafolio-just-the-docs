#!/usr/bin/env python3
"""Lectura de archivos de KiCad sin KiCad.

Este entorno no tiene kicad-cli, así que los scripts de verificación (F1) y de
figuras (F4) leen el `.kicad_pcb` y el `.kicad_sch` directamente. Aquí vive lo
que los dos comparten: el parser de s-expresiones y la geometría de los pads.

El giro de un footprint entra en el archivo con el signo contrario al de la
convención matemática. SIGNO_GIRO lo corrige, y ese valor no es una suposición:
está comprobado contra el archivo de taladros. Con rotación ×(−1) y Y invertida
los 75 pads caen sobre sus barrenos con un residuo de 0.138 mm, que es la media
longitud de las ranuras de 2.1 × 1.8 mm; con cualquier otra combinación de
signos el error pasa de 6 mm.
"""
import math

from shapely.affinity import rotate, translate
from shapely.geometry import LineString, Point, box

SIGNO_GIRO = -1          # verificado contra el .drl

f = float


def parse(txt):
    """Parser mínimo de s-expresiones de KiCad."""
    i, n = 0, len(txt)

    def nodo():
        nonlocal i
        while i < n and txt[i] in " \t\r\n":
            i += 1
        if txt[i] == "(":
            i += 1
            out = []
            while True:
                while i < n and txt[i] in " \t\r\n":
                    i += 1
                if txt[i] == ")":
                    i += 1
                    return out
                out.append(nodo())
        if txt[i] == '"':
            i += 1
            buf = []
            while txt[i] != '"':
                if txt[i] == "\\":
                    i += 1
                buf.append(txt[i])
                i += 1
            i += 1
            return "".join(buf)
        j = i
        while i < n and txt[i] not in " \t\r\n()":
            i += 1
        return txt[j:i]

    return nodo()


def leer(ruta):
    return parse(open(ruta, encoding="utf-8", errors="replace").read())


def hijos(nodo, nom):
    return [c for c in nodo if isinstance(c, list) and c and c[0] == nom]


def hijo(nodo, nom):
    h = hijos(nodo, nom)
    return h[0] if h else None


def capa(nodo):
    c = hijo(nodo, "layer")
    return c[1] if c else None


def girar(p, deg):
    a = math.radians(deg * SIGNO_GIRO)
    return (p[0]*math.cos(a) - p[1]*math.sin(a), p[0]*math.sin(a) + p[1]*math.cos(a))


def angulo_pad(pad_at, giro_footprint):
    """Orientación absoluta de un pad, en grados.

    El ángulo que un pad declara en `(at x y ang)` NO es relativo a su
    footprint: ya viene girado con él. Se ve en este proyecto, donde los
    footprints girados 90° tienen todos sus pads con ángulo 90, incluidos los
    circulares, en los que un ángulo no significa nada. Sumarlo al giro del
    footprint lo contaría dos veces y los pads rectangulares de los
    componentes girados saldrían cruzados 90°.

    Cuando el pad no declara ángulo, hereda el del footprint.
    """
    return f(pad_at[3]) if len(pad_at) > 3 else giro_footprint


def geometria_pad(forma, w, h, cx, cy, ang):
    if forma == "circle":
        return Point(cx, cy).buffer(w/2, 32)
    if forma == "oval":
        largo = abs(w - h) / 2
        g = LineString([(-largo, 0), (largo, 0)]).buffer(min(w, h)/2, 32)
    else:                                   # rect, roundrect
        g = box(-w/2, -h/2, w/2, h/2)
    return translate(rotate(g, ang * SIGNO_GIRO, origin=(0, 0)), cx, cy)
