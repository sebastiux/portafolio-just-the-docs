#!/usr/bin/env python3
"""F2 (brazo impreso) — Ensamble 3D con las coordenadas reales del CAD.

El STEP del ensamble que exportó Inventor viene SIN geometría: trae la
estructura, las posiciones y los colores, pero cero sólidos. Aun así sirve,
porque las transformaciones de ensamble sí están completas. Este script las
extrae y se las aplica a los STL que ya había en el repositorio.

Siete de las nueve piezas colocan bien. Las dos mordazas no: pinzas.stl trae
las dos en un solo archivo y, al separarlas, ninguna de las dos asignaciones
posibles las deja cerca del soporte (quedan a ~90 mm). Ese archivo está en un
marco propio, no en el de cada pieza, así que las mordazas quedan fuera del
ensamble hasta tener su exportación por separado.

Salida: assets/stl/brazo-impreso/ensamble/*.stl + ensamble-cad.json
"""
import json, os, re, sys
import numpy as np, trimesh

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEP = os.path.join(RAIZ, "_entrada_brazos/impreso3d/ensamble-brazo-impreso-VACIO.stp")
ORIG = os.path.join(RAIZ, "assets/stl/brazo-impreso")
DEST = os.path.join(ORIG, "ensamble")
SEPARACION = 55.0

PIEZAS = [
    ("Base 2 v2:1",              "base.stl",          "Base (alojamiento servo)", "#4B5563"),
    ("Tapa v2:1",                "tapa.stl",          "Tapa giratoria",           "#E00034"),
    ("Brazo 1 v1:1",             "brazo-1.stl",       "Brazo 1",                  "#F59E0B"),
    ("Brazo 2 v1_FINAL_FInal:1", "brazo-2.stl",       "Brazo 2",                  "#2563EB"),
    ("Soporte Pinza v1:1",       "soporte-pinza.stl", "Soporte de pinza",         "#10B981"),
    ("Pi\\X\\F1on Servo v1:1",   "pinon-servo.stl",   "Piñón del servo",          "#8B5CF6"),
    ("Pi\\X\\F1on pinza 1 v1:1", "pinon-pinza.stl",   "Piñón de pinza",           "#EC4899"),
]


def transformaciones():
    s = re.sub(r"\s*\n\s*", "", open(STEP, encoding="utf-8", errors="replace").read())
    E = dict(re.findall(r"#(\d+)=(.*?);", s))
    ref = lambda k: re.findall(r"#(\d+)", E.get(k, ""))
    def nums(k):
        return [float(x) for x in re.findall(r"-?\d+\.?\d*(?:E-?\d+)?", E[k].split("(", 1)[1])]
    def matriz(a2):
        p, z, x = ref(a2)
        P = np.array(nums(p)[:3]); Z = np.array(nums(z)[:3]); X = np.array(nums(x)[:3])
        Z = Z / np.linalg.norm(Z)
        X = X - np.dot(X, Z) * Z
        X = X / np.linalg.norm(X)
        T = np.eye(4)
        T[:3, 0], T[:3, 1], T[:3, 2], T[:3, 3] = X, np.cross(Z, X), Z, P
        return T
    out = {}
    for k, v in E.items():
        if not v.startswith("CONTEXT_DEPENDENT_SHAPE_REPRESENTATION"):
            continue
        rr, pds = ref(k)
        nombre = re.findall(r"'([^']*)'", E[ref(pds)[0]])[0]
        idt = re.search(r"REPRESENTATION_RELATIONSHIP_WITH_TRANSFORMATION\(#(\d+)\)", E[rr]).group(1)
        out[nombre] = matriz(ref(idt)[1])
    return out


def main():
    tr = transformaciones()
    os.makedirs(DEST, exist_ok=True)
    colocadas = []
    for clave, archivo, nombre, color in PIEZAS:
        if clave not in tr:
            print(f"AVISO: sin transformación para {clave}")
            continue
        m = trimesh.load(os.path.join(ORIG, archivo))
        m.apply_transform(tr[clave])
        m.export(os.path.join(DEST, archivo))
        colocadas.append((nombre, archivo, color, m))

    todo = trimesh.util.concatenate([m for *_, m in colocadas])
    centro = todo.bounds.mean(axis=0)
    print(f"envolvente del ensamble: {np.round(todo.extents, 1)} mm, {len(colocadas)} piezas")

    spec = []
    for nombre, archivo, color, m in colocadas:
        lo, hi = m.bounds
        pos = [round(float(x), 3) for x in ((lo[0]+hi[0])/2, (lo[1]+hi[1])/2, lo[2])]
        d = m.bounds.mean(axis=0) - centro
        n = np.linalg.norm(d)
        expl = [0.0, 0.0, 0.0] if n < 1e-6 else [round(float(x), 2) for x in d / n * SEPARACION]
        spec.append({"name": nombre, "file": archivo, "color": color,
                     "position": pos, "explode": expl})
        print(f"  {archivo:18s} centro {np.round(m.bounds.mean(axis=0), 1)}")

    with open(os.path.join(DEST, "ensamble-cad.json"), "w", encoding="utf-8") as f:
        json.dump({"note": "Posiciones reales del ensamble CAD, extraídas de las "
                           "transformaciones del STEP de Inventor. Faltan las dos "
                           "mordazas: pinzas.stl trae las dos en un solo archivo y no "
                           "está en el marco de cada pieza.",
                   "parts": spec}, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    sys.exit(main())
