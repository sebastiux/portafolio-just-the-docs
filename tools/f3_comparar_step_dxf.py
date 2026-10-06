#!/usr/bin/env python3
"""F3 — Compara las placas del STEP contra los contornos cortados de los DXF.

Responde a una pregunta concreta: ¿el modelo 3D de GrabCAD es lo que se cortó?

Se comparan las medidas EN PLANTA. Para que la comparación sea justa se usa el
rectángulo mínimo rotado de cada contorno (las piezas están giradas en la hoja)
y las placas del STEP se miden en su MARCO LOCAL, sin la transformación del
ensamble: ahí están alineadas a ejes y el espesor sale 3.00 exacto. La caja
orientada sobre la malla ya transformada no sirve, da espesores de 3.02 a
4.53 mm porque se calcula sobre el casco convexo teselado. El emparejamiento
es óptimo global (scipy.optimize.linear_sum_assignment), no vecino más cercano.

Salida: assets/brazos/laser/corte/comparacion-step-dxf.json
"""
import collections, json, os, sys
import numpy as np, trimesh
from scipy.optimize import linear_sum_assignment
from shapely import wkt as swkt

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORTE = os.path.join(RAIZ, "assets/brazos/laser/corte")
GLB = os.environ.get("TMPDIR", "/tmp") + "/mearm.glb"


def placas_step():
    esc = trimesh.load(GLB)
    padre = {b: a for a, b in (e[:2] for e in esc.graph.to_edgelist())}
    occ = collections.defaultdict(list)
    for nodo in esc.graph.nodes:
        try:
            _T, geo = esc.graph.get(nodo)
        except Exception:
            continue
        if geo is None:
            continue
        # sin apply_transform: se mide en el marco local de la pieza
        m = esc.geometry[geo].copy(); m.apply_scale(1000.0)
        occ[nodo if padre.get(nodo) == "Final Assembly" else padre.get(nodo, nodo)].append(m)
    salida, raros = [], []
    for nombre, cuerpos in occ.items():
        if not nombre.startswith("Part"):
            continue
        m = trimesh.util.concatenate(cuerpos)
        e = np.sort(m.extents)
        if not (2.9 < e[0] < 3.1):
            raros.append((nombre, [round(float(x), 2) for x in e]))
            continue
        salida.append({"nombre": nombre, "largo": float(e[2]), "ancho": float(e[1])})
    if raros:
        print(f"AVISO: {len(raros)} ocurrencias no miden 3 mm en su marco local: {raros}")
    return salida


def piezas_dxf():
    datos = json.load(open(os.path.join(CORTE, "piezas.json"), encoding="utf-8"))
    salida = []
    for hoja in datos:
        for p in datos[hoja]["piezas"]:
            poly = swkt.loads(p["wkt"])
            r = np.array(poly.minimum_rotated_rectangle.exterior.coords)
            lados = np.linalg.norm(np.diff(r, axis=0), axis=1)[:2]
            l, a = float(max(lados)), float(min(lados))
            salida.append({"id": p["id"], "largo": l, "ancho": a})
    return salida


def main():
    S, D = placas_step(), piezas_dxf()
    print(f"placas de 3 mm en el STEP: {len(S)} | contornos en los DXF: {len(D)}")
    C = np.array([[abs(s["largo"]-d["largo"]) + abs(s["ancho"]-d["ancho"])
                   for d in D] for s in S])
    fi, ci = linear_sum_assignment(C)
    filas = []
    for i, j in zip(fi, ci):
        dif = max(abs(S[i]["largo"]-D[j]["largo"]), abs(S[i]["ancho"]-D[j]["ancho"]))
        filas.append({"step": S[i]["nombre"], "dxf": D[j]["id"],
                      "step_mm": [round(S[i]["largo"], 2), round(S[i]["ancho"], 2)],
                      "dxf_mm": [round(D[j]["largo"], 2), round(D[j]["ancho"], 2)],
                      "dif_mm": round(float(dif), 2)})
    filas.sort(key=lambda r: r["dif_mm"])
    emparejados = {r["dxf"] for r in filas}
    sin_pareja = [d["id"] for d in D if d["id"] not in emparejados]

    tramos = {"<= 1.5 mm": 0, "1.5 - 4 mm": 0, "> 4 mm": 0}
    for r in filas:
        k = "<= 1.5 mm" if r["dif_mm"] <= 1.5 else ("1.5 - 4 mm" if r["dif_mm"] <= 4 else "> 4 mm")
        tramos[k] += 1
    print("\ndiferencia máxima por pareja:")
    for k, v in tramos.items():
        print(f"  {k:12s} {v:3d} placas")
    print(f"  sin pareja   {len(sin_pareja):3d} contornos DXF: {sin_pareja}")
    print("\npeores 8 parejas:")
    for r in sorted(filas, key=lambda x: -x["dif_mm"])[:8]:
        print(f"  {r['step'][:34]:34s} {str(r['step_mm']):18s} vs {r['dxf']} {str(r['dxf_mm']):18s}  dif {r['dif_mm']:6.2f} mm")

    with open(os.path.join(CORTE, "comparacion-step-dxf.json"), "w", encoding="utf-8") as f:
        json.dump({"resumen": tramos, "sin_pareja": sin_pareja, "parejas": filas},
                  f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    sys.exit(main())
