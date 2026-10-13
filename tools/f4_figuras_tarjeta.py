#!/usr/bin/env python3
"""F4 — Figuras de la tarjeta v3, dibujadas desde el proyecto de KiCad.

Este entorno no tiene kicad-cli, así que las dos vistas de la tarjeta no salen
de `kicad-cli pcb export svg`: se dibujan leyendo el `.kicad_pcb` con el mismo
parser que usa la verificación de F1. Tiene una ventaja sobre exportar un SVG:
lo que aparece en la figura es lo que el script entendió del archivo, así que si
el dibujo saliera mal, el error se vería.

El esquemático sí viene rasterizado del PDF que trae el proyecto, porque
dibujar un esquemático de cero no aporta nada que el PDF no tenga.

Genera en assets/brazos/electronica/v3/:
  pcb-componentes.png     vista desde la cara de componentes
  pcb-cobre-espejado.png  cobre visto desde el lado del cobre (como lo fresa
                          la máquina), con la tabla de anchos
  esquematico.png         rasterizado de docs/esquematico.pdf
  esquematico.pdf         copia del PDF del proyecto

Necesita pypdfium2 solo para el esquemático:  pip install pypdfium2

    python3 tools/f4_figuras_tarjeta.py [carpeta del proyecto] [carpeta de salida]
"""
import os, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # para kicad_sexp

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle
from shapely.geometry import LineString
from shapely.ops import unary_union

from kicad_sexp import angulo_pad, f, geometria_pad, girar, hijo, hijos, leer

PLACA   = "#EFE2C0"      # fenólica
BORDE   = "#5A4632"
COBRE   = "#A85A24"
PAD     = "#C47E3F"
SILK    = "#2F4660"
REF     = "#C8102E"
PIN     = "#53606E"
DPI     = 160

def trozos(g):
    """Los polígonos de una geometría, sea uno solo o varios."""
    return list(g.geoms) if hasattr(g, "geoms") else [g]


ANCHO_A_COLOR = {0.8: "#C98A5B", 1.2: "#A85A24", 1.6: "#7A3B10"}


def datos(carpeta):
    """Todo lo que hace falta dibujar, ya en coordenadas con origen en la placa."""
    pcb = leer(os.path.join(carpeta, "brazo_control.kicad_pcb"))
    nombre_red = {n[1]: n[2] for n in hijos(pcb, "net")}

    bordes = [g for g in hijos(pcb, "gr_line") if (hijo(g, "layer") or [None, None])[1] == "Edge.Cuts"]
    xs = [f(hijo(g, k)[1]) for g in bordes for k in ("start", "end")]
    ys = [f(hijo(g, k)[2]) for g in bordes for k in ("start", "end")]
    x0, y0 = min(xs), min(ys)
    W, H = max(xs) - x0, max(ys) - y0

    d = {"W": W, "H": H, "pistas": [], "pads": [], "silk": [], "textos": []}

    for s in hijos(pcb, "segment"):
        a, b = hijo(s, "start"), hijo(s, "end")
        d["pistas"].append({
            "a": (f(a[1]) - x0, f(a[2]) - y0), "b": (f(b[1]) - x0, f(b[2]) - y0),
            "w": f(hijo(s, "width")[1]),
            "net": nombre_red.get(hijo(s, "net")[1], ""),
        })

    for fp in hijos(pcb, "footprint"):
        at = hijo(fp, "at")
        fx, fy = f(at[1]) - x0, f(at[2]) - y0
        fr = f(at[3]) if len(at) > 3 else 0.0

        def absoluto(nodo, i=1):
            dx, dy = girar((f(nodo[i]), f(nodo[i+1])), fr)
            return (fx + dx, fy + dy)

        for p in hijos(fp, "pad"):
            pat, psz = hijo(p, "at"), hijo(p, "size")
            if not (pat and psz):
                continue
            cx, cy = absoluto(pat)
            ang = angulo_pad(pat, fr)
            g = geometria_pad(p[3], f(psz[1]), f(psz[2]), cx, cy, ang)
            dr = hijo(p, "drill")
            if dr and dr[1] == "oval":
                taladro = ("oval", f(dr[2]), f(dr[3]), ang)
            elif dr:
                taladro = ("circ", f(dr[1]), f(dr[1]), ang)
            else:
                taladro = None
            nt = hijo(p, "net")
            d["pads"].append({"poly": list(g.exterior.coords), "c": (cx, cy),
                              "taladro": taladro,
                              "net": nt[2] if nt and len(nt) > 2 else ""})

        for ln in hijos(fp, "fp_line"):
            if (hijo(ln, "layer") or [None, None])[1] != "F.SilkS":
                continue
            d["silk"].append(("linea", absoluto(hijo(ln, "start")), absoluto(hijo(ln, "end"))))
        for ci in hijos(fp, "fp_circle"):
            if (hijo(ci, "layer") or [None, None])[1] != "F.SilkS":
                continue
            c, e = absoluto(hijo(ci, "center")), absoluto(hijo(ci, "end"))
            r = ((c[0]-e[0])**2 + (c[1]-e[1])**2) ** 0.5
            d["silk"].append(("circulo", c, r))
        for rc in hijos(fp, "fp_rect"):
            if (hijo(rc, "layer") or [None, None])[1] != "F.SilkS":
                continue
            a, b = absoluto(hijo(rc, "start")), absoluto(hijo(rc, "end"))
            for p0, p1 in (((a[0], a[1]), (b[0], a[1])), ((b[0], a[1]), (b[0], b[1])),
                           ((b[0], b[1]), (a[0], b[1])), ((a[0], b[1]), (a[0], a[1]))):
                d["silk"].append(("linea", p0, p1))
        for ar in hijos(fp, "fp_arc"):
            if (hijo(ar, "layer") or [None, None])[1] != "F.SilkS":
                continue
            # Un arco se aproxima por su cuerda: en estas huellas son muy cortos.
            d["silk"].append(("linea", absoluto(hijo(ar, "start")), absoluto(hijo(ar, "end"))))

        for t in hijos(fp, "fp_text"):
            if (hijo(t, "layer") or [None, None])[1] != "F.SilkS":
                continue
            tam = hijo(hijo(hijo(t, "effects"), "font"), "size")
            just = hijo(hijo(t, "effects"), "justify")
            d["textos"].append({
                "txt": t[2], "p": absoluto(hijo(t, "at")), "tam": f(tam[1]),
                "clase": "ref" if t[1] == "reference" else "pin", "ang": 0.0,
                "ha": {"left": "left", "right": "right"}.get(just[1] if just else "", "center"),
            })

    for t in hijos(pcb, "gr_text"):
        if (hijo(t, "layer") or [None, None])[1] != "F.SilkS":
            continue
        at = hijo(t, "at")
        tam = hijo(hijo(hijo(t, "effects"), "font"), "size")
        d["textos"].append({
            "txt": t[1], "p": (f(at[1]) - x0, f(at[2]) - y0), "tam": f(tam[1]),
            "clase": "placa", "ang": (f(at[3]) if len(at) > 3 else 0.0), "ha": "center",
        })
    return d


def dibujar(d, espejo, destino, titulo, subtitulo, con_silk, con_tabla):
    """Una vista de la tarjeta. Con espejo=True se refleja en X, que es como se
    ve el cobre mirándolo de frente y como lo recibe la fresadora.

    Las pistas se dibujan como polígonos y no como líneas: así su ancho sale en
    milímetros de la placa y no en puntos de la figura, que es lo que importa
    cuando la figura habla justamente de anchos de pista.
    """
    W, H = d["W"], d["H"]
    mx = (lambda x: W - x) if espejo else (lambda x: x)
    ma = (lambda a: -a) if espejo else (lambda a: a)   # al reflejar, el texto gira al revés

    # Ejes de tamaño fijo: así la escala mm -> puntos se conoce sin dibujar.
    MARGEN = 5.0
    dw, dh = W + 2*MARGEN, H + 2*MARGEN
    caja = (0.07, 0.09, 0.86, 0.80)
    fig_w = 11.0
    fig_h = fig_w * caja[2] / caja[3] * dh / dw
    fig = plt.figure(figsize=(fig_w, fig_h))
    ax = fig.add_axes(caja)
    pt_por_mm = fig_w * caja[2] * 72 / dw

    ax.add_patch(Rectangle((0, 0), W, H, facecolor=PLACA, edgecolor=BORDE, lw=1.6, zorder=0))

    alfa = 1.0 if espejo else 0.5      # desde componentes, el cobre queda del otro lado

    # Las pistas de un mismo ancho se unen antes de dibujarse: si se dibujaran
    # una por una, cada traslape se vería más oscuro que el resto.
    for w in sorted({t["w"] for t in d["pistas"]}):
        cuerpos = [LineString([(mx(t["a"][0]), t["a"][1]), (mx(t["b"][0]), t["b"][1])])
                   .buffer(t["w"]/2, 8) for t in d["pistas"] if t["w"] == w]
        for trozo in trozos(unary_union(cuerpos)):
            ax.add_patch(Polygon(list(trozo.exterior.coords), closed=True,
                                 facecolor=ANCHO_A_COLOR.get(w, COBRE), edgecolor="none",
                                 alpha=alfa, zorder=1))

    for p in d["pads"]:
        ax.add_patch(Polygon([(mx(x), y) for x, y in p["poly"]], closed=True,
                             facecolor=PAD, edgecolor=COBRE, lw=0.4, alpha=alfa, zorder=2))
    for p in d["pads"]:
        tal = p["taladro"]
        if not tal:
            continue
        cx, cy = mx(p["c"][0]), p["c"][1]
        if tal[0] == "oval":
            g = geometria_pad("oval", tal[1], tal[2], cx, cy, ma(tal[3]))
            ax.add_patch(Polygon(list(g.exterior.coords), closed=True, facecolor="white",
                                 edgecolor=BORDE, lw=0.3, zorder=3))
        else:
            ax.add_patch(Circle((cx, cy), tal[1]/2, facecolor="white",
                                edgecolor=BORDE, lw=0.3, zorder=3))

    if con_silk:
        for forma in d["silk"]:
            if forma[0] == "linea":
                (xa, ya), (xb, yb) = forma[1], forma[2]
                ax.plot([mx(xa), mx(xb)], [ya, yb], color=SILK, lw=0.4, alpha=0.5, zorder=4)
            else:
                ax.add_patch(Circle((mx(forma[1][0]), forma[1][1]), forma[2], fill=False,
                                    edgecolor=SILK, lw=0.4, alpha=0.5, zorder=4))
        estilo = {"ref":   dict(color=REF, weight="bold", alpha=1.0),
                  "pin":   dict(color=PIN, weight="normal", alpha=0.9),
                  "placa": dict(color=SILK, weight="bold", alpha=1.0)}
        for t in d["textos"]:
            e = estilo[t["clase"]]
            ax.text(mx(t["p"][0]), t["p"][1], t["txt"],
                    fontsize=t["tam"] * pt_por_mm * 0.75,   # 0.75: alto de caja -> alto de letra
                    color=e["color"], weight=e["weight"], alpha=e["alpha"],
                    rotation=ma(t["ang"]), rotation_mode="anchor",
                    ha=t["ha"] if not espejo else
                       {"left": "right", "right": "left"}.get(t["ha"], "center"),
                    va="center", zorder=5,
                    # Las referencias caen donde las puso KiCad, a veces encima
                    # de un pad: un fondo claro las deja legibles igual.
                    bbox=dict(boxstyle="square,pad=0.08", facecolor=PLACA,
                              edgecolor="none", alpha=0.75) if t["clase"] == "ref" else None)

    ax.set_xlim(-MARGEN, W + MARGEN)
    ax.set_ylim(H + MARGEN, -MARGEN)             # Y crece hacia abajo, como en KiCad
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"{titulo}\n{subtitulo}", fontsize=12, color="#222", pad=12)

    # Cotas de la placa.
    ax.annotate("", xy=(0, H + 2.6), xytext=(W, H + 2.6),
                arrowprops=dict(arrowstyle="<->", color=BORDE, lw=0.9))
    ax.text(W/2, H + 3.6, f"{W:.0f} mm", ha="center", va="top", fontsize=10, color=BORDE)
    ax.annotate("", xy=(-2.6, 0), xytext=(-2.6, H),
                arrowprops=dict(arrowstyle="<->", color=BORDE, lw=0.9))
    ax.text(-3.4, H/2, f"{H:.0f} mm", ha="right", va="center", fontsize=10,
            color=BORDE, rotation=90)

    if con_tabla:
        anchos = sorted({t["w"] for t in d["pistas"]})
        manijas = [plt.Line2D([], [], color=ANCHO_A_COLOR.get(w, COBRE), lw=4,
                              label=f"{w:.1f} mm  ·  {sum(1 for t in d['pistas'] if t['w'] == w)} tramos")
                   for w in anchos]
        ax.legend(handles=manijas, loc="upper center", bbox_to_anchor=(0.5, -0.02),
                  ncol=len(anchos), frameon=False, fontsize=10,
                  title="Ancho de pista (capacidad calculada en tools/f4_ampacidad.py)",
                  title_fontsize=10)

    fig.savefig(destino, dpi=DPI, facecolor="white")
    plt.close(fig)
    print(f"  {destino}")


def esquematico(carpeta, salida):
    origen = os.path.join(carpeta, "docs", "esquematico.pdf")
    shutil.copyfile(origen, os.path.join(salida, "esquematico.pdf"))
    print(f"  {os.path.join(salida, 'esquematico.pdf')}")
    try:
        import pypdfium2
    except ImportError:
        print("  AVISO: sin pypdfium2 no se puede rasterizar el esquemático.")
        print("         pip install pypdfium2  y volver a correr.")
        return
    pdf = pypdfium2.PdfDocument(origen)
    print(f"  (el PDF tiene {len(pdf)} página(s))")
    for i in range(len(pdf)):
        img = pdf[i].render(scale=300/72).to_pil()
        nombre = "esquematico.png" if len(pdf) == 1 else f"esquematico-{i+1}.png"
        destino = os.path.join(salida, nombre)
        img.save(destino)
        print(f"  {destino}  ({img.width} x {img.height} px)")


def main(carpeta, salida):
    os.makedirs(salida, exist_ok=True)
    d = datos(carpeta)
    print(f"leído: {d['W']:.0f} x {d['H']:.0f} mm, {len(d['pistas'])} pistas, "
          f"{len(d['pads'])} pads, {len(d['silk'])} trazos de serigrafía, "
          f"{len(d['textos'])} textos")

    dibujar(d, False, os.path.join(salida, "pcb-componentes.png"),
            "Tarjeta v3 — cara de componentes",
            "Las pistas van en la cara de abajo y se ven atenuadas, a través de la placa.\n"
            "La serigrafía no está impresa en la tarjeta real: es guía de armado.",
            con_silk=True, con_tabla=False)

    dibujar(d, True, os.path.join(salida, "pcb-cobre-espejado.png"),
            "Tarjeta v3 — cobre visto desde el lado del cobre",
            "Reflejada en X: es la vista que recibe la fresadora. Una sola cara, sin vías.",
            con_silk=False, con_tabla=True)

    esquematico(carpeta, salida)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "assets/brazos/electronica/kicad-v3",
         sys.argv[2] if len(sys.argv) > 2 else "assets/brazos/electronica/v3")
