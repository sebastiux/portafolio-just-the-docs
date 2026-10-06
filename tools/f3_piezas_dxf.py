#!/usr/bin/env python3
"""F3 — Separa las piezas de las dos hojas DXF de corte del MeArm.

Los DXF son la fuente de verdad de las piezas: es lo que se cortó. De aquí
salen los contornos individuales (R1 y R2); el STEP solo se usa para el
ensamble (R3, R4, R5).

Método: aplanar cada entidad a 0.05 mm, unir, redondear a 0.02 mm y
polygonize. polygonize devuelve CARAS que teselan el plano, no anillos
anidados, así que la clasificación se hace por anillo exterior:
  - fondo  : la cara cuyo anillo exterior cubre la hoja entera
  - agujero: cara cuyo punto interior cae dentro del anillo exterior de otra
  - pieza  : el resto

Salida: assets/brazos/laser/corte/hoja-{a,b}.png  (numeradas, para verificar)
        piezas.json con la geometría y las medidas de cada pieza
"""
import json, os, sys
import ezdxf, numpy as np
from ezdxf.path import make_path
from shapely.geometry import LineString, MultiLineString, Polygon
from shapely.ops import unary_union, polygonize
from shapely import set_precision
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DXF = os.path.join(RAIZ, "_entrada_brazos/laser/dxf")
DEST = os.path.join(RAIZ, "assets/brazos/laser/corte")
HOJAS = {"A": "Mearm_1_0_150x200_A.dxf", "B": "Mearm_1_0_150x200_B.dxf"}
AREA_MIN = 60.0     # mm2; por debajo se marca "por confirmar", no se numera
APLANADO, PRECISION = 0.05, 0.02


def extraer(ruta):
    msp = ezdxf.readfile(ruta).modelspace()
    segs, descartadas = [], []
    for e in msp:
        try:
            pts = [(v.x, v.y) for v in make_path(e).flattening(distance=APLANADO)]
            if len(pts) >= 2:
                segs.append(LineString(pts))
            else:   # p. ej. el ARC de barrido cero de la hoja A (handle 114)
                descartadas.append((e.dxftype(), e.dxf.handle))
        except Exception:
            descartadas.append((e.dxftype(), e.dxf.handle))
    caras = list(polygonize(set_precision(unary_union(MultiLineString(segs)), PRECISION)))
    b = np.array([c.bounds for c in caras])
    mn, mx = b[:, :2].min(axis=0), b[:, 2:].max(axis=0)

    def es_fondo(c):
        eb = c.exterior.bounds
        return (abs(eb[0]-mn[0]) < 0.5 and abs(eb[1]-mn[1]) < 0.5 and
                abs(eb[2]-mx[0]) < 0.5 and abs(eb[3]-mx[1]) < 0.5)

    resto = [c for c in caras if not es_fondo(c)]
    ext = [Polygon(c.exterior) for c in resto]
    piezas = [c for i, c in enumerate(resto)
              if not any(j != i and ext[j].contains(c.representative_point())
                         for j in range(len(resto)))]
    return piezas, descartadas, (mn, mx)


def ordenar(polys):
    """De arriba hacia abajo y de izquierda a derecha, en bandas de 15 mm."""
    def clave(p):
        cx, cy = p.representative_point().x, p.representative_point().y
        return (-round(cy / 15.0), cx)
    return sorted(polys, key=clave)


def dibujar(destino, titulo, piezas, dudosas, mn, mx):
    fig, ax = plt.subplots(figsize=(8.5, 11), dpi=150)
    for num, p in piezas:
        ax.fill(*p.exterior.xy, color="#c9b089", ec="#333", lw=0.6, zorder=1)
        for h in p.interiors:
            ax.fill(*h.xy, color="white", ec="#333", lw=0.4, zorder=2)
        c = p.representative_point()
        ax.text(c.x, c.y, num, fontsize=7, fontweight="bold",
                ha="center", va="center", zorder=4,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.75))
    for p in dudosas:
        ax.fill(*p.exterior.xy, color="#ff5555", ec="#900", lw=0.6, zorder=3)
    ax.set_aspect("equal"); ax.set_title(titulo, fontsize=10)
    ax.set_xlim(mn[0]-6, mx[0]+6); ax.set_ylim(mn[1]-6, mx[1]+6)
    ax.set_xlabel("mm"); ax.tick_params(labelsize=7)
    plt.tight_layout(); plt.savefig(destino); plt.close()


def main():
    os.makedirs(DEST, exist_ok=True)
    salida = {}
    for tag, archivo in HOJAS.items():
        polys, descartadas, (mn, mx) = extraer(os.path.join(DXF, archivo))
        grandes = ordenar([p for p in polys if p.area >= AREA_MIN])
        dudosas = [p for p in polys if p.area < AREA_MIN]
        numeradas = [(f"{tag}-{i:02d}", p) for i, p in enumerate(grandes, 1)]
        dibujar(os.path.join(DEST, f"hoja-{tag.lower()}.png"),
                f"Hoja {tag} — {len(numeradas)} piezas numeradas"
                + (f" + {len(dudosas)} figuras sueltas por confirmar (rojo)" if dudosas else ""),
                numeradas, dudosas, mn, mx)
        salida[tag] = {
            "hoja_mm": [round(float(mx[0]-mn[0]), 2), round(float(mx[1]-mn[1]), 2)],
            "origen_mm": [round(float(mn[0]), 2), round(float(mn[1]), 2)],
            "entidades_descartadas": descartadas,
            "piezas": [{"id": n, "area_mm2": round(p.area, 2),
                        "ancho_mm": round(p.bounds[2]-p.bounds[0], 2),
                        "alto_mm": round(p.bounds[3]-p.bounds[1], 2),
                        "agujeros": len(p.interiors),
                        "wkt": p.wkt} for n, p in numeradas],
            "por_confirmar": [{"area_mm2": round(p.area, 2),
                               "ancho_mm": round(p.bounds[2]-p.bounds[0], 2),
                               "alto_mm": round(p.bounds[3]-p.bounds[1], 2),
                               "centro_mm": [round(p.centroid.x, 1), round(p.centroid.y, 1)],
                               "wkt": p.wkt} for p in dudosas],
        }
        print(f"Hoja {tag}: {len(numeradas)} piezas, {len(dudosas)} por confirmar, "
              f"{len(descartadas)} entidades descartadas {descartadas}")
    with open(os.path.join(DEST, "piezas.json"), "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=1)
    tot = sum(len(v["piezas"]) for v in salida.values())
    dud = sum(len(v["por_confirmar"]) for v in salida.values())
    print(f"\nTOTAL: {tot} piezas numeradas + {dud} figuras por confirmar")


if __name__ == "__main__":
    sys.exit(main())
