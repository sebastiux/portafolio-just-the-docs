#!/usr/bin/env python3
"""F1 — Verificación geométrica independiente de la tarjeta v3.

No usa KiCad: lee el .kicad_pcb y el .kicad_sch directamente y recalcula lo
que el handoff afirma, para no tomar sus números por buenos.

Comprueba:
  - medidas del contorno, número de componentes, redes, segmentos y barrenos;
  - ancho mínimo de pista y longitud total;
  - separación mínima real entre redes distintas, con la geometría de pistas
    y pads (no el valor declarado en las reglas de diseño);
  - que las referencias del esquemático y de la PCB coincidan;
  - qué pads quedan sin red y de qué componente son.

El parser de s-expresiones y la geometría de los pads viven en kicad_sexp.py,
que también usa el script de figuras (F4). Ahí está explicado por qué el giro
de los footprints lleva signo negativo.

    python3 tools/f1_verificar_tarjeta_v3.py <carpeta del proyecto>
"""
import collections, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # para kicad_sexp

from shapely.geometry import LineString
from shapely.ops import unary_union

from kicad_sexp import angulo_pad, f, geometria_pad, girar, hijo, hijos, leer


def main(carpeta):
    pcb = leer(os.path.join(carpeta, "brazo_control.kicad_pcb"))
    sch = leer(os.path.join(carpeta, "brazo_control.kicad_sch"))

    # contorno
    xs, ys = [], []
    for g in hijos(pcb, "gr_line"):
        if hijo(g, "layer")[1] != "Edge.Cuts":
            continue
        for k in ("start", "end"):
            p = hijo(g, k)
            xs.append(f(p[1])); ys.append(f(p[2]))
    print(f"contorno        : {max(xs)-min(xs):.2f} x {max(ys)-min(ys):.2f} mm")

    # pistas
    porred = collections.defaultdict(list)
    anchos, capas, largo = collections.Counter(), collections.Counter(), 0.0
    for s in hijos(pcb, "segment"):
        a, b = hijo(s, "start"), hijo(s, "end")
        w = f(hijo(s, "width")[1])
        ln = LineString([(f(a[1]), f(a[2])), (f(b[1]), f(b[2]))])
        largo += ln.length
        anchos[w] += 1
        capas[hijo(s, "layer")[1]] += 1
        porred[int(hijo(s, "net")[1])].append(ln.buffer(w/2, 16))
    print(f"pistas          : {sum(anchos.values())} segmentos, {largo:.1f} mm, "
          f"anchos {dict(sorted(anchos.items()))}, capas {dict(capas)}")

    # pads y referencias
    refs_pcb, sin_red, nombres = set(), collections.defaultdict(list), {}
    n_pads = n_taladros = 0
    for fp in hijos(pcb, "footprint"):
        ref = next((t[2] for t in hijos(fp, "fp_text") if t[1] == "reference"), None)
        if ref:
            refs_pcb.add(ref)
        at = hijo(fp, "at")
        fx, fy, fr = f(at[1]), f(at[2]), (f(at[3]) if len(at) > 3 else 0.0)
        for p in hijos(fp, "pad"):
            pat, psz = hijo(p, "at"), hijo(p, "size")
            if not (pat and psz):
                continue
            n_pads += 1
            if hijo(p, "drill"):
                n_taladros += 1
            dx, dy = girar((f(pat[1]), f(pat[2])), fr)
            g = geometria_pad(p[3], f(psz[1]), f(psz[2]), fx+dx, fy+dy, angulo_pad(pat, fr))
            nt = hijo(p, "net")
            if nt and nt[2]:
                porred[int(nt[1])].append(g)
                nombres[int(nt[1])] = nt[2]
            else:
                sin_red[ref].append(p[1])
    print(f"componentes     : {len(refs_pcb)} | pads {n_pads} | con barreno {n_taladros} | "
          f"vias {len(hijos(pcb, 'via'))}")

    union = {n: unary_union(g) for n, g in porred.items() if n in nombres}
    redes = sorted(union)
    print(f"redes con cobre : {len(redes)}")
    peor = (1e9, None, None)
    for i, a in enumerate(redes):
        for b in redes[i+1:]:
            d = union[a].distance(union[b])
            if d < peor[0]:
                peor = (d, a, b)
    print(f"separación mín. : {peor[0]:.4f} mm  ({nombres[peor[1]]} ↔ {nombres[peor[2]]})")
    print(f"ancho mín. pista: {min(anchos):.3f} mm")

    refs_sch = {pr[2] for s in hijos(sch, "symbol") for pr in hijos(s, "property")
                if pr[1] == "Reference" and not pr[2].startswith("#")}
    print(f"referencias     : esquemático {len(refs_sch)}, PCB {len(refs_pcb)} | "
          f"solo sch {sorted(refs_sch - refs_pcb) or '—'} | solo pcb {sorted(refs_pcb - refs_sch) or '—'}")
    total = sum(len(v) for v in sin_red.values())
    print(f"pads sin red    : {total}")
    for r, ps in sorted(sin_red.items()):
        print(f"   {r}: {ps}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "assets/brazos/electronica/kicad-v3")
