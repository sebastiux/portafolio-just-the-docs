#!/usr/bin/env python3
"""F2 — Ensamble 3D del MeArm a partir del STEP de Inventor.

Entrada : _entrada_brazos/laser/ensamble-mearm-mdf.stp
Salida  : assets/stl/brazo-laser/{placa-NN,servo-N}.stl + ensamble.json

Escala: el STEP sale de cascadio en metros, así que el factor a milímetros es
1000. Verificado contra dos anclas: las placas miden 3.00 mm y la base
145 x 95 mm.

Cada placa va en su propio archivo para que el control "Separar piezas" del
visor produzca una vista explosionada de verdad. La leyenda no se llena de 31
renglones porque el visor agrupa las entradas que comparten nombre y color.

El visor aplica centerOnBed() a cada pieza, que la traslada en -(cx, cy, zmin).
Por eso ensamble.json guarda position = (cx, cy, zmin): así se reconstruye la
posición original del ensamble.
"""
import collections, json, os, sys
import numpy as np, trimesh, cascadio

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEP = os.path.join(RAIZ, "_entrada_brazos/laser/ensamble-mearm-mdf.stp")
DEST = os.path.join(RAIZ, "assets/stl/brazo-laser")
TMP = os.environ.get("TMPDIR", "/tmp") + "/mearm.glb"
K = 1000.0
LLENADO_MIN = 0.20      # área / superficie de su caja; por debajo es geometría de astillas
SEPARACION = 85.0       # mm que se apartan las piezas con el control al máximo
MDF, AZUL = "#B08A5A", "#2563EB"
cat = trimesh.util.concatenate


def cargar():
    if not os.path.exists(TMP):
        cascadio.step_to_glb(STEP, TMP, 0.1, 0.5)
    esc = trimesh.load(TMP)
    padre = {b: a for a, b in (e[:2] for e in esc.graph.to_edgelist())}
    occ = collections.defaultdict(list)
    for nodo in esc.graph.nodes:
        try:
            T, geo = esc.graph.get(nodo)
        except Exception:
            continue
        # No se descarta ningún cuerpo por volumen: cascadio parte algunas piezas
        # según la orientación de sus caras. La base sale como 'Part 17 - Base'
        # (solo tapas) y 'Part 17 - Base_1' (solo cantos); el volumen de ambos es
        # basura por estar abiertos y descartar "el de volumen cero" deja la
        # placa sin caras.
        if geo is None:
            continue
        m = esc.geometry[geo].copy()
        m.apply_transform(T)
        m.apply_scale(K)
        occ[nodo if padre.get(nodo) == "Final Assembly" else padre.get(nodo, nodo)].append(m)
    return occ


def llenado(cuerpo):
    e = cuerpo.extents
    sup = 2 * (e[0]*e[1] + e[0]*e[2] + e[1]*e[2])
    return cuerpo.area / sup if sup else 0.0


def util(cuerpos):
    """Quita la geometría de astillas: cuerpos con mucha caja y casi nada de área.

    En el modelo del SG90 hay cuerpos internos de 2 700 y 3 200 triángulos con
    141 y 47 mm2 de área. No se ven —están dentro de la carcasa— y solo suman
    peso. Quitarlos no cambia el render; comprobado contra el servo completo.
    """
    buenos = [c for c in cuerpos if llenado(c) >= LLENADO_MIN]
    return buenos or cuerpos


def main():
    occ = cargar()
    placas = sorted(k for k in occ if k.startswith("Part"))
    servos = sorted(k for k in occ if "Tower Pro.1-" in k)
    horn = [k for k in occ if "Tower Pro.2" in k]
    assert len(placas) == 31, f"se esperaban 31 placas, hay {len(placas)}"
    assert len(servos) == 4, f"se esperaban 4 servos, hay {len(servos)}"

    piezas = {}
    for i, k in enumerate(placas, 1):
        piezas[f"placa-{i:02d}.stl"] = ("Placa de MDF", MDF, cat(occ[k]))
    hm = cat([m for k in horn for m in occ[k]])
    cercano = min(servos, key=lambda k: np.linalg.norm(cat(occ[k]).bounds.mean(axis=0) - hm.bounds.mean(axis=0)))
    for i, k in enumerate(servos, 1):
        cuerpos = util(occ[k]) + ([hm] if k == cercano else [])
        piezas[f"servo-{i}.stl"] = ("Servo SG90", AZUL, cat(cuerpos))

    # Verificación: la envolvente del conjunto no se mueve
    orig = cat([m for k in occ for m in occ[k]])
    nuevo = cat([m for _, _, m in piezas.values()])
    err = np.abs(orig.extents - nuevo.extents).max()
    print(f"envolvente {np.round(nuevo.extents, 2)} mm | error contra el original: {err:.3f} mm")
    assert err <= 0.1, "se movió la envolvente del ensamble"

    # Verificación: ningún archivo pierde superficie respecto a sus cuerpos de origen
    for archivo, (_, _, m) in piezas.items():
        assert m.area > 0 and len(m.faces) > 0, f"{archivo} quedó vacío"

    centro = nuevo.bounds.mean(axis=0)
    os.makedirs(DEST, exist_ok=True)
    for viejo in os.listdir(DEST):
        if viejo.startswith(("placa-", "servo-", "ensamble-")) and viejo.endswith(".stl"):
            os.remove(os.path.join(DEST, viejo))

    spec, total = [], 0
    for archivo, (nombre, color, m) in piezas.items():
        ruta = os.path.join(DEST, archivo)
        m.export(ruta)
        total += os.path.getsize(ruta)
        lo, hi = m.bounds
        pos = [round(float(x), 3) for x in ((lo[0]+hi[0])/2, (lo[1]+hi[1])/2, lo[2])]
        d = m.bounds.mean(axis=0) - centro
        n = np.linalg.norm(d)
        expl = [0.0, 0.0, 0.0] if n < 1e-6 else [round(float(x), 2) for x in d / n * SEPARACION]
        spec.append({"name": nombre, "file": archivo, "color": color,
                     "position": pos, "explode": expl})

    with open(os.path.join(DEST, "ensamble.json"), "w", encoding="utf-8") as f:
        json.dump({"note": "Generado por tools/f2_ensamble_mearm.py desde el STEP de "
                           "Inventor. Coordenadas reales del ensamble CAD, en mm.",
                   "parts": spec}, f, ensure_ascii=False, indent=1)
    tri = sum(len(m.faces) for _, _, m in piezas.values())
    print(f"{len(piezas)} archivos ({len(placas)} placas + {len(servos)} servos), "
          f"{tri} triángulos, {total/1e6:.2f} MB")


if __name__ == "__main__":
    sys.exit(main())
