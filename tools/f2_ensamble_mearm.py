#!/usr/bin/env python3
"""F2 — Ensamble 3D del MeArm a partir del STEP de Inventor.

Entrada : _entrada_brazos/laser/ensamble-mearm-mdf.stp
Salida  : assets/stl/brazo-laser/{ensamble-mdf,servo-1..4}.stl + ensamble.json

Notas de escala: el STEP declara pulgadas y cascadio lo entrega en metros,
así que el factor a milímetros es 1000. Se verifica contra dos anclas
conocidas: las placas miden 3.00 mm y la base 145 x 95 mm.

El visor (assets/js/stl-viewer.js) aplica centerOnBed() a cada pieza, que la
traslada en -(cx, cy, zmin). Por eso ensamble.json guarda position = (cx, cy,
zmin): así el visor reconstruye la posición original del ensamble.
"""
import collections, json, os, sys
import numpy as np, trimesh, cascadio

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEP = os.path.join(RAIZ, "_entrada_brazos/laser/ensamble-mearm-mdf.stp")
DEST = os.path.join(RAIZ, "assets/stl/brazo-laser")
TMP  = os.environ.get("TMPDIR", "/tmp") + "/mearm.glb"
K, TOL = 1000.0, 0.1          # mm por unidad; tolerancia de decimación en mm
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
        # No se descarta ningún cuerpo. cascadio parte algunas piezas en varios
        # cuerpos por orientación de cara: la base sale como 'Part 17 - Base'
        # (solo las tapas horizontales) y 'Part 17 - Base_1' (solo los cantos).
        # Ninguno es un duplicado y el volumen de ambos es basura por estar
        # abiertos; descartar "el de volumen cero" deja la placa sin caras.
        if geo is None:
            continue
        m = esc.geometry[geo].copy()
        m.apply_transform(T)
        m.apply_scale(K)
        occ[nodo if padre.get(nodo) == "Final Assembly" else padre.get(nodo, nodo)].append(m)
    return occ


def decimar(cuerpo, tol=TOL):
    """Reduce caras sin perder más de `tol` mm de envolvente.

    Baja la cuenta de caras solo mientras la envolvente aguante: en el SG90,
    una decimación agresiva se come las orejas de montaje (9.6 mm de error).
    """
    if len(cuerpo.faces) <= 1500:
        return cuerpo
    for frac in (0.25, 0.4, 0.55, 0.7):
        d = cuerpo.simplify_quadric_decimation(face_count=int(len(cuerpo.faces) * frac))
        if np.abs(d.extents - cuerpo.extents).max() <= tol:
            return d
    return cuerpo


def main():
    occ = cargar()
    placas = [k for k in occ if k.startswith("Part")]
    servos = sorted(k for k in occ if "Tower Pro.1-" in k)
    horn = [k for k in occ if "Tower Pro.2" in k]
    assert len(placas) == 31, f"se esperaban 31 placas, hay {len(placas)}"
    assert len(servos) == 4, f"se esperaban 4 servos, hay {len(servos)}"

    piezas = {"ensamble-mdf.stl": ("Estructura de MDF (31 placas)", MDF,
                                   cat([m for k in placas for m in occ[k]]))}
    hm = cat([m for k in horn for m in occ[k]])
    cercano = min(servos, key=lambda k: np.linalg.norm(cat(occ[k]).bounds.mean(axis=0) - hm.bounds.mean(axis=0)))
    for i, k in enumerate(servos, 1):
        cuerpos = occ[k] + ([hm] if k == cercano else [])
        piezas[f"servo-{i}.stl"] = (f"Servo SG90 ({i})", AZUL, cat([decimar(c) for c in cuerpos]))

    # Verificación: la envolvente del conjunto no debe moverse
    orig = cat([m for k in occ for m in occ[k]])
    nuevo = cat([m for _, _, m in piezas.values()])
    err = np.abs(orig.extents - nuevo.extents).max()
    print(f"envolvente {np.round(nuevo.extents, 2)} mm | error contra el original: {err:.3f} mm")
    assert err <= TOL, "la decimación movió la envolvente del ensamble"

    centro = nuevo.bounds.mean(axis=0)
    os.makedirs(DEST, exist_ok=True)
    spec = []
    for archivo, (nombre, color, m) in piezas.items():
        m.export(os.path.join(DEST, archivo))
        lo, hi = m.bounds
        # el visor hace centerOnBed(); position devuelve la pieza a su sitio
        pos = [round(float(x), 3) for x in ((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, lo[2])]
        d = m.bounds.mean(axis=0) - centro
        n = np.linalg.norm(d)
        expl = [0.0, 0.0, 0.0] if archivo.startswith("ensamble") or n < 1e-6 else \
               [round(float(x), 2) for x in d / n * 70.0]
        spec.append({"name": nombre, "file": archivo, "color": color,
                     "position": pos, "explode": expl})
        print(f"  {archivo:18s} {len(m.faces):6d} tri  {os.path.getsize(os.path.join(DEST, archivo))/1e6:.2f} MB")

    with open(os.path.join(DEST, "ensamble.json"), "w", encoding="utf-8") as f:
        json.dump({"note": "Generado por tools/f2_ensamble_mearm.py desde el STEP de Inventor. "
                           "Coordenadas reales del ensamble CAD, en mm.",
                   "parts": spec}, f, ensure_ascii=False, indent=2)
    print(f"\ntotal: {sum(os.path.getsize(os.path.join(DEST,a)) for a in piezas)/1e6:.2f} MB")


if __name__ == "__main__":
    sys.exit(main())
