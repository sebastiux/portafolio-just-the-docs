#!/usr/bin/env python3
"""F3 (R1, R2) — DXF, STL y render de cada pieza, desde los contornos de corte.

Entrada: assets/brazos/laser/corte/piezas.json (lo genera f3_piezas_dxf.py)
Salida : assets/brazos/laser/piezas-dxf/<id>.dxf   contorno suelto, en mm
         assets/stl/brazo-laser/piezas/<id>.stl    extruido a 3 mm
         assets/brazos/laser/render/piezas/<id>.png

Cada pieza se traslada a su propio origen (esquina inferior izquierda en 0,0)
para que el DXF y el STL sueltos no arrastren la posición que tenían en la hoja.

Requiere pantalla virtual para los renders:
    xvfb-run -a python3 tools/f3_salidas_piezas.py
"""
import json, os, sys
import ezdxf, numpy as np, trimesh
from shapely import wkt as swkt
from shapely.affinity import translate
from shapely.geometry import Polygon

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORTE = os.path.join(RAIZ, "assets/brazos/laser/corte")
D_DXF = os.path.join(RAIZ, "assets/brazos/laser/piezas-dxf")
D_STL = os.path.join(RAIZ, "assets/stl/brazo-laser/piezas")
D_PNG = os.path.join(RAIZ, "assets/brazos/laser/render/piezas")
ESPESOR, MDF = 3.0, "#B08A5A"
DXF_IN = os.path.join(RAIZ, "_entrada_brazos/laser/dxf")
HOJAS = {"A": "Mearm_1_0_150x200_A.dxf", "B": "Mearm_1_0_150x200_B.dxf"}


def circulos_nominales():
    """Centro y radio exactos de cada CIRCLE, por hoja."""
    return {tag: [((c.dxf.center.x, c.dxf.center.y), c.dxf.radius)
                  for c in ezdxf.readfile(os.path.join(DXF_IN, a)).modelspace()
                  if c.dxftype() == "CIRCLE"]
            for tag, a in HOJAS.items()}


def escribir_dxf(poly, destino, circulos=()):
    # R2000 sin setup: los DXF sueltos son de descarga, no hace falta la
    # plantilla de estilos/dimensiones que infla cada archivo a ~60 KB.
    doc = ezdxf.new("R2000")
    doc.header["$INSUNITS"] = 4          # milímetros
    msp = doc.modelspace()
    doc.layers.add("CORTE", color=7)
    msp.add_lwpolyline(list(poly.exterior.coords)[:-1], close=True, dxfattribs={"layer": "CORTE"})
    for anillo in poly.interiors:
        # Los agujeros redondos se escriben como CIRCLE, no como polilínea: este
        # archivo es de corte y una circunferencia aplanada se cortaría poligonal.
        h = Polygon(anillo)
        c = h.centroid
        cerca = [r for (cx, cy), r in circulos if (cx-c.x)**2 + (cy-c.y)**2 < 0.25]
        if cerca and h.length and 4*np.pi*h.area/(h.length**2) > 0.93:
            msp.add_circle((c.x, c.y), cerca[0], dxfattribs={"layer": "CORTE"})
        else:
            msp.add_lwpolyline(list(anillo.coords)[:-1], close=True, dxfattribs={"layer": "CORTE"})
    doc.saveas(destino)


def main():
    for d in (D_DXF, D_STL, D_PNG):
        os.makedirs(d, exist_ok=True)
    datos = json.load(open(os.path.join(CORTE, "piezas.json"), encoding="utf-8"))
    circ_hoja = circulos_nominales()
    import pyvista as pv

    tabla = []
    for hoja in datos:
        for p in datos[hoja]["piezas"]:
            poly = swkt.loads(p["wkt"])
            minx, miny = poly.bounds[0], poly.bounds[1]
            poly = translate(poly, -minx, -miny)      # a su propio origen
            pid = p["id"]

            cs = [((cx-minx, cy-miny), r) for (cx, cy), r in circ_hoja[hoja]]
            escribir_dxf(poly, os.path.join(D_DXF, f"{pid}.dxf"), cs)
            malla = trimesh.creation.extrude_polygon(poly, ESPESOR)
            malla.export(os.path.join(D_STL, f"{pid}.stl"))

            pl = pv.Plotter(off_screen=True, window_size=(800, 600))
            pl.set_background("#f5f6f8")
            pl.add_mesh(pv.wrap(malla), color=MDF, smooth_shading=False,
                        specular=0.2, specular_power=10)
            pl.enable_parallel_projection()
            pl.view_isometric()
            pl.camera.zoom(1.35)
            pl.screenshot(os.path.join(D_PNG, f"{pid}.png"))
            pl.close()

            an, al = poly.bounds[2], poly.bounds[3]
            tabla.append({"id": pid, "hoja": hoja,
                          "ancho_mm": round(an, 2), "alto_mm": round(al, 2),
                          "area_mm2": round(poly.area, 2),
                          "agujeros": len(poly.interiors),
                          "volumen_cm3": round(malla.volume / 1000.0, 3),
                          "triangulos": len(malla.faces)})
            print(f"  {pid}: {an:7.2f} x {al:7.2f} x {ESPESOR} mm, "
                  f"{len(poly.interiors):2d} agujeros, {malla.volume/1000:6.2f} cm3")

    with open(os.path.join(CORTE, "tabla-piezas.json"), "w", encoding="utf-8") as f:
        json.dump(tabla, f, ensure_ascii=False, indent=1)
    vol = sum(t["volumen_cm3"] for t in tabla)
    print(f"\n{len(tabla)} piezas | volumen total de MDF: {vol:.1f} cm3")


if __name__ == "__main__":
    sys.exit(main())
