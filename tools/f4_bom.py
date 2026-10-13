#!/usr/bin/env python3
"""F4 — Lista de materiales de la tarjeta v3, sacada del esquemático.

No se escribe a mano ni se copia del paquete: se lee `brazo_control.kicad_sch`,
se agrupan los componentes iguales y se cuenta. Después se compara el resultado
con el `docs/bom.csv` que trae el proyecto; si los dos no coinciden, uno de los
dos está mal y hay que mirarlo antes de publicar nada.

También comprueba contra el `.kicad_pcb` que cada componente del esquemático
esté colocado en la placa con la misma huella. Una lista de materiales que no
corresponde a lo que se fresó no sirve para comprar.

La columna de precio queda en blanco a propósito: no hay ninguna fuente para
esos números y poner un precio inventado sería peor que dejarlo pendiente.

    python3 tools/f4_bom.py [carpeta del proyecto] [carpeta de salida]
"""
import collections, csv, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # para kicad_sexp

from kicad_sexp import hijo, hijos, leer

PENDIENTE = "[Pendiente]"


def orden_ref(ref):
    """R10 va después de R9, no entre R1 y R2."""
    letras = "".join(c for c in ref if c.isalpha())
    numero = "".join(c for c in ref if c.isdigit())
    return (letras, int(numero) if numero else 0)


def componentes_sch(carpeta):
    sch = leer(os.path.join(carpeta, "brazo_control.kicad_sch"))
    salida = {}
    for s in hijos(sch, "symbol"):
        p = {pr[1]: pr[2] for pr in hijos(s, "property")}
        ref = p.get("Reference", "")
        if not ref or ref.startswith("#"):          # alimentación, banderas: no son material
            continue
        salida[ref] = {
            "valor": p.get("Value", ""),
            "huella": p.get("Footprint", "").split(":")[-1],
            "funcion": p.get("Funcion", ""),
        }
    return salida


def huellas_pcb(carpeta):
    pcb = leer(os.path.join(carpeta, "brazo_control.kicad_pcb"))
    salida = {}
    for fp in hijos(pcb, "footprint"):
        ref = next((t[2] for t in hijos(fp, "fp_text") if t[1] == "reference"), None)
        if ref:
            salida[ref] = fp[1].split(":")[-1]
    return salida


def agrupar(comps):
    grupos = collections.OrderedDict()
    for ref in sorted(comps, key=orden_ref):
        c = comps[ref]
        clave = (c["valor"], c["huella"])
        g = grupos.setdefault(clave, {"refs": [], "funciones": []})
        g["refs"].append(ref)
        if c["funcion"]:
            g["funciones"].append(c["funcion"])
    return grupos


def main(carpeta, salida):
    comps = componentes_sch(carpeta)
    pcb = huellas_pcb(carpeta)

    print(f"esquemático: {len(comps)} componentes | PCB: {len(pcb)} huellas")
    problemas = []
    for ref, c in comps.items():
        if ref not in pcb:
            problemas.append(f"{ref} está en el esquemático y no en la placa")
        elif pcb[ref] != c["huella"]:
            problemas.append(f"{ref}: huella {c['huella']} en el esquemático, {pcb[ref]} en la placa")
    for ref in pcb:
        if ref not in comps:
            problemas.append(f"{ref} está en la placa y no en el esquemático")
    print("coherencia  : " + ("todo coincide" if not problemas else "PROBLEMAS"))
    for p in problemas:
        print(f"   {p}")

    grupos = agrupar(comps)
    os.makedirs(salida, exist_ok=True)
    destino = os.path.join(salida, "bom.csv")
    with open(destino, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Cantidad", "Referencias", "Valor", "Huella", "Funcion",
                    "Precio unitario (MXN)", "Precio total (MXN)"])
        for (valor, huella), g in grupos.items():
            w.writerow([len(g["refs"]), " ".join(g["refs"]), valor, huella,
                        "; ".join(dict.fromkeys(g["funciones"])), PENDIENTE, PENDIENTE])
        w.writerow([len(comps), "TOTAL", f"{len(grupos)} tipos distintos", "", "",
                    "", PENDIENTE])
    print(f"escrito     : {destino}  ({len(grupos)} renglones, {len(comps)} piezas)")

    # Comparación contra la lista que trae el paquete.
    original = os.path.join(carpeta, "docs", "bom.csv")
    if not os.path.exists(original):
        return
    with open(original, encoding="utf-8") as fh:
        viejo = {r["Referencias"]: r for r in csv.DictReader(fh)}
    nuevo = {" ".join(g["refs"]): (valor, huella) for (valor, huella), g in grupos.items()}
    print(f"comparación : {len(nuevo)} renglones propios contra {len(viejo)} del paquete")
    difs = []
    for refs, (valor, huella) in nuevo.items():
        if refs not in viejo:
            difs.append(f"renglón '{refs}' no está en el bom.csv del paquete")
            continue
        v = viejo[refs]
        if v["Valor"] != valor:
            difs.append(f"{refs}: valor '{valor}' contra '{v['Valor']}'")
        if v["Footprint"] != huella:
            difs.append(f"{refs}: huella '{huella}' contra '{v['Footprint']}'")
    for refs in viejo:
        if refs not in nuevo:
            difs.append(f"renglón '{refs}' del paquete no sale del esquemático")
    print("              " + ("sin diferencias" if not difs else f"{len(difs)} diferencias"))
    for d in difs:
        print(f"   {d}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "assets/brazos/electronica/kicad-v3",
         sys.argv[2] if len(sys.argv) > 2 else "assets/brazos/electronica/v3")
