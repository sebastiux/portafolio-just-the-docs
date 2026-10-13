#!/usr/bin/env python3
"""F4 — Capacidad de corriente de las pistas de la tarjeta v3 (IPC-2221).

No copia la tabla del handoff: lee los anchos reales del `.kicad_pcb` y los
recalcula. Además busca el cuello de botella eléctrico, que es la pregunta que
de verdad importa en esta tarjeta: la corriente de los cuatro servos no entra
por "una pista de 1.6 mm", entra por el camino completo de J2 a cada conector
de servo, y ese camino vale lo que valga su tramo más angosto.

Fórmula IPC-2221, conductor externo:

    I = k · ΔT^0.44 · A^0.725      k = 0.048,  A en mils²,  I en A

Supuestos declarados (ninguno está medido en esta tarjeta):
  - cobre de 35 µm (1 oz). Es lo típico de la placa fenólica de una cara, pero
    no viene en el proyecto de KiCad: HIPÓTESIS;
  - ΔT admisible de 10 °C sobre el ambiente, que es el valor conservador con
    el que se suele dimensionar. Se reporta también a 20 °C;
  - la fórmula es empírica y supone una pista aislada al aire. Una pista
    rodeada de cobre o pegada a otra que también calienta aguanta menos.

    python3 tools/f4_ampacidad.py [carpeta del proyecto]
"""
import collections, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # para kicad_sexp

from shapely.geometry import LineString
from shapely.strtree import STRtree

from kicad_sexp import angulo_pad, f, geometria_pad, girar, hijo, hijos, leer

K_EXTERNA = 0.048
ESPESOR_UM = 35.0          # HIPÓTESIS: 1 oz
MM_POR_MIL = 0.0254
PICO_SERVOS_A = (2.4, 2.8)  # HIPÓTESIS del handoff: 4 SG90 a 0.6-0.7 A de arranque


def ampacidad(ancho_mm, dt_c, espesor_um=ESPESOR_UM):
    """Corriente admisible de una pista externa, en amperes."""
    area_mils2 = (ancho_mm / MM_POR_MIL) * (espesor_um / 1000.0 / MM_POR_MIL)
    return K_EXTERNA * dt_c**0.44 * area_mils2**0.725


def cargar(carpeta):
    pcb = leer(os.path.join(carpeta, "brazo_control.kicad_pcb"))

    # Las pistas traen el número de red; los pads, el número y el nombre. Se
    # trabaja con nombres, así que hace falta la tabla del encabezado.
    nombre_red = {n[1]: n[2] for n in hijos(pcb, "net")}

    pistas = []
    for s in hijos(pcb, "segment"):
        a, b = hijo(s, "start"), hijo(s, "end")
        pistas.append({
            "geom": LineString([(f(a[1]), f(a[2])), (f(b[1]), f(b[2]))]),
            "w": f(hijo(s, "width")[1]),
            "net": nombre_red.get(hijo(s, "net")[1], "?"),
        })

    pads = []
    for fp in hijos(pcb, "footprint"):
        ref = next((t[2] for t in hijos(fp, "fp_text") if t[1] == "reference"), "?")
        at = hijo(fp, "at")
        fx, fy, fr = f(at[1]), f(at[2]), (f(at[3]) if len(at) > 3 else 0.0)
        for p in hijos(fp, "pad"):
            pat, psz, nt = hijo(p, "at"), hijo(p, "size"), hijo(p, "net")
            if not (pat and psz and nt and nt[2]):
                continue
            dx, dy = girar((f(pat[1]), f(pat[2])), fr)
            pads.append({
                "geom": geometria_pad(p[3], f(psz[1]), f(psz[2]), fx+dx, fy+dy,
                                      angulo_pad(pat, fr)),
                "ref": ref, "pin": p[1], "net": nt[2],
            })
    return pistas, pads


def cuello(pistas, pads, red, desde, hasta, anchos):
    """Ancho del tramo más angosto del mejor camino entre dos pads.

    Para cada ancho candidato, de mayor a menor, se prueba si los dos pads
    siguen conectados usando solo pistas de ese ancho o más. El primero que
    conecta es la capacidad del camino: no hace falta recorrer caminos uno por
    uno, basta con quitar las pistas angostas y ver si el circuito se corta.
    """
    for w in sorted(anchos, reverse=True):
        pads_red = [p for p in pads if p["net"] == red]
        piezas = [p["geom"] for p in pads_red]
        piezas += [t["geom"].buffer(t["w"]/2, 8) for t in pistas
                   if t["net"] == red and t["w"] >= w - 1e-9]
        if not piezas:
            continue

        # Union-find sobre las piezas de cobre que se tocan.
        padre = list(range(len(piezas)))
        def raiz(i):
            while padre[i] != i:
                padre[i] = padre[padre[i]]
                i = padre[i]
            return i
        arbol = STRtree(piezas)
        for i, g in enumerate(piezas):
            for j in arbol.query(g):
                if i < j and g.intersects(piezas[j]):
                    ri, rj = raiz(i), raiz(j)
                    if ri != rj:
                        padre[ri] = rj

        a = {raiz(k) for k, p in enumerate(pads_red) if p["ref"] == desde}
        b = {raiz(k) for k, p in enumerate(pads_red) if p["ref"] == hasta}
        if a & b:
            return w
    return None


def main(carpeta):
    pistas, pads = cargar(carpeta)
    anchos = sorted({t["w"] for t in pistas})

    print(f"espesor supuesto: {ESPESOR_UM:.0f} um (1 oz)   formula: IPC-2221 externa, k={K_EXTERNA}\n")

    print("Anchos usados en la tarjeta")
    print(f"{'ancho':>7} {'tramos':>7} {'largo':>9} {'seccion':>9} "
          f"{'I (dT 10C)':>11} {'I (dT 20C)':>11}")
    for w in anchos:
        tramos = [t for t in pistas if t["w"] == w]
        largo = sum(t["geom"].length for t in tramos)
        print(f"{w:>5.1f}mm {len(tramos):>7} {largo:>7.1f}mm "
              f"{w*ESPESOR_UM/1000:>7.3f}mm2 {ampacidad(w, 10):>10.2f}A {ampacidad(w, 20):>10.2f}A")

    print("\nAncho mínimo por red (el total incluye todos sus tramos)")
    por_red = collections.defaultdict(list)
    for t in pistas:
        por_red[t["net"]].append(t)
    for red in sorted(por_red, key=lambda r: (min(t["w"] for t in por_red[r]), r)):
        tramos = por_red[red]
        w = min(t["w"] for t in tramos)
        print(f"  {red:<12} min {w:.1f} mm  ({len(tramos):>3} tramos, "
              f"{sum(t['geom'].length for t in tramos):>5.1f} mm)  "
              f"-> {ampacidad(w, 10):.2f} A")

    print("\nCuello de botella de J2 (entrada de servos) a cada conector")
    print("  El camino vale lo que su tramo más angosto, no lo que el más ancho.")
    peor = 99.0
    for destino in ("J3", "J4", "J5", "J6"):
        for red, etiqueta in (("VSERVO", "VSERVO"), ("GND", "GND   ")):
            w = cuello(pistas, pads, red, "J2", destino, anchos)
            if w is None:
                print(f"  J2 -> {destino}  {etiqueta}: SIN CAMINO de cobre")
                continue
            peor = min(peor, w)
            print(f"  J2 -> {destino}  {etiqueta}: cuello {w:.1f} mm -> "
                  f"{ampacidad(w, 10):.2f} A a dT 10 C, {ampacidad(w, 20):.2f} A a dT 20 C")

    print(f"\nPico estimado de los cuatro servos: {PICO_SERVOS_A[0]}-{PICO_SERVOS_A[1]} A (HIPÓTESIS)")
    if peor < 99.0:
        margen_10 = ampacidad(peor, 10) / PICO_SERVOS_A[1]
        margen_20 = ampacidad(peor, 20) / PICO_SERVOS_A[1]
        print(f"Cuello peor del camino de servos: {peor:.1f} mm")
        print(f"  contra el pico alto ({PICO_SERVOS_A[1]} A): "
              f"{margen_10:.2f}x a dT 10 C, {margen_20:.2f}x a dT 20 C")
        print("  " + ("ALCANZA con margen." if margen_10 >= 1.0 else
                      "NO alcanza a dT 10 C: la pista se calienta más de 10 C en el pico."))
        print("  El pico de los servos dura decenas de ms, y la fórmula es para")
        print("  régimen permanente: el calentamiento real es menor. Pero el margen")
        print("  que se puede defender por cálculo es el de arriba.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "assets/brazos/electronica/kicad-v3")
