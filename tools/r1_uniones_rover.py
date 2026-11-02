#!/usr/bin/env python3
"""R1 (B05–B08) — Uniones, rin y llanta del rover para la propuesta de
materiales con tubo de aluminio 6063 de Ø30 × 1.5 mm.

Todo es paramétrico: si el tubo real mide distinto, se cambian las constantes
de abajo y se vuelve a correr. Genera:

  assets/stl/rover/uniones/*.stl     piezas de PETG (codos, T, pivotes, terminales)
  assets/stl/rover/rueda/*.stl       rin de PETG, llanta de Ecoflex y su molde
  assets/stl/rover/ensamble/*        un lado de la suspensión + ensamble.json
  assets/stl/rover/datos.json        volúmenes, masas y envolventes por pieza

Uso:    python3 tools/r1_uniones_rover.py
Requiere: numpy, trimesh, manifold3d
"""
import json
import math
import os

import numpy as np
import trimesh
from trimesh import transformations as tf

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(RAIZ, "assets/stl/rover")

# ── Tubo (anuncio: aluminio 6063, OD 30 mm, ID 27 mm, largo 300 mm) ──────────
TUBO_OD, TUBO_ID = 30.0, 27.0
# ── Casquillo de PETG que recibe el tubo ─────────────────────────────────────
HOLGURA = 0.4            # diámetro: 30.4 mm. Se calibra con la probeta de ajuste
R_BORE = (TUBO_OD + HOLGURA) / 2
PARED = 4.0
R_EXT = R_BORE + PARED   # 19.2 mm
PROF = 35.0              # profundidad del casquillo (> 1 diámetro de tubo)
S0 = 21.0                # del centro de la unión al tope del tubo
R_CABLE = 8.0            # canal interior para pasar cables por dentro del tubo
# Tornillo pasante M4 que cruza casquillo y tubo
R_M4, R_CABEZA, PROF_CABEZA = 2.2, 4.1, 3.0
R_TUERCA, ALTO_TUERCA = 7.0 / 2 / math.cos(math.radians(30)) + 0.15, 3.4
# ── Pivote: 2 rodamientos 608 (8 × 22 × 7) y eje M8 ──────────────────────────
R_608, ANCHO_608 = 22.15 / 2, 7.2
ANCHO_PIVOTE = 44.0
SEMIANGULO = 50.0        # cada pata del balancín a 50° de la vertical
# ── Motorreductor (supuesto: cuerpo Ø37 mm, tipo JGB37) y eje M8 ─────────────
R_MOTOR = 37.4 / 2
# ── Rueda ────────────────────────────────────────────────────────────────────
ANCHO_RUEDA = 64.0
R_NUCLEO, R_PESTANA, R_BANDA, R_TACO = 62.0, 65.0, 68.0, 76.0
N_TACOS, ANCHO_TACO = 16, 7.0

SEC = 96
LARGO_TRASERO = 115.0   # pata trasera del balancín; ensamble() lo comprueba
PIEZAS = {}


def alinear(d):
    """Matriz que lleva +Z a la dirección d."""
    d = np.asarray(d, float) / np.linalg.norm(d)
    z = np.array([0, 0, 1.0])
    if np.allclose(d, z):
        return np.eye(4)
    if np.allclose(d, -z):
        return tf.rotation_matrix(math.pi, [1, 0, 0])
    eje = np.cross(z, d)
    return tf.rotation_matrix(math.acos(np.clip(np.dot(z, d), -1, 1)), eje)


def cil(r, a, b, d=(0, 0, 1), centro=(0, 0, 0), sec=SEC):
    """Cilindro de radio r a lo largo de d, entre las distancias a y b."""
    m = trimesh.creation.cylinder(radius=r, height=b - a, sections=sec)
    m.apply_translation([0, 0, (a + b) / 2])
    m.apply_transform(alinear(d))
    m.apply_translation(centro)
    return m


def union(ms):
    return trimesh.boolean.union(ms, engine="manifold")


def resta(a, bs):
    return trimesh.boolean.difference([a] + list(bs), engine="manifold")


def normal_en_plano(d):
    """Eje del tornillo pasante: perpendicular al casquillo, en Y si se puede."""
    y = np.array([0, 1.0, 0])
    if abs(np.dot(y, d)) < 0.9:
        return y
    return np.array([1.0, 0, 0])


def casquillo(d, s0=S0, cable=True):
    """Devuelve (sólido, cortes) de un casquillo en la dirección d."""
    d = np.asarray(d, float) / np.linalg.norm(d)
    solido = cil(R_EXT, 0, s0 + PROF, d)
    cortes = [cil(R_BORE, s0, s0 + PROF + 1, d)]
    if cable:
        cortes.append(cil(R_CABLE, -1, s0 + 1, d))
    n = normal_en_plano(d)
    c = d * (s0 + PROF / 2)
    cortes.append(cil(R_M4, -R_EXT - 2, R_EXT + 2, n, c, sec=24))
    cortes.append(cil(R_CABEZA, R_EXT - PROF_CABEZA, R_EXT + 2, n, c, sec=32))
    cortes.append(cil(R_TUERCA, -R_EXT - 2, -R_EXT + ALTO_TUERCA, n, c, sec=6))
    return solido, cortes


def unir_casquillos(dirs, extra_solidos=(), extra_cortes=(), esfera=True, cable=True, s0=S0):
    solidos, cortes = list(extra_solidos), list(extra_cortes)
    if esfera:
        solidos.append(trimesh.creation.icosphere(subdivisions=4, radius=R_EXT))
    for d in dirs:
        s, c = casquillo(d, s0=s0, cable=cable)
        solidos.append(s)
        cortes += c
    return resta(union(solidos), cortes)


def polar(angulo_deg):
    """Dirección en el plano XZ medida desde -Z (hacia abajo), positiva hacia +X."""
    a = math.radians(angulo_deg)
    return np.array([math.sin(a), 0, -math.cos(a)])


# ── Piezas de unión ──────────────────────────────────────────────────────────
def codo(angulo):
    """Codo entre dos tubos: ángulo interior entre sus ejes."""
    return unir_casquillos([polar(90), polar(90 - angulo)])


def union_t():
    return unir_casquillos([polar(90), polar(-90), polar(180)])


def cople():
    return unir_casquillos([polar(90), polar(-90)], esfera=False, s0=3.0)


def pivote():
    """Vértice del balancín (rocker) y del bogie: 2 casquillos + 2 rodamientos 608."""
    y = np.array([0, 1.0, 0])
    w = ANCHO_PIVOTE / 2
    jefe = cil(R_EXT, -w, w, y)
    cortes = [
        cil(R_608, w - ANCHO_608, w + 1, y),
        cil(R_608, -w - 1, -w + ANCHO_608, y),
        cil(5.0, -w, w, y, sec=48),
    ]
    dirs = [polar(SEMIANGULO), polar(-SEMIANGULO)]
    # Los cables no pueden cruzar el eje que gira: salen por un ojal arriba
    # de cada casquillo, cerca del tope del tubo.
    for d in dirs:
        cortes.append(cil(5.0, 0, R_EXT + 2, [0, 0, 1], d * (S0 + 8), sec=32))
    return unir_casquillos(dirs, [jefe], cortes, cable=False)


def terminal_eje():
    """Extremo trasero del balancín: casquillo + oreja con barreno de 8.2 para el eje M8."""
    y = np.array([0, 1.0, 0])
    oreja = cil(12.0, -10, 10, y)
    s, c = casquillo([0, 0, 1], s0=14.0, cable=False)
    return resta(union([oreja, s]), c + [cil(4.1, -21, 21, y, sec=48)])


def terminal_motor():
    """Extremo de pata: abrazadera para motorreductor de Ø37 con cierre M3."""
    y = np.array([0, 1.0, 0])
    anillo = cil(R_MOTOR + 4.5, -15, 15, y)
    orejas = trimesh.creation.box(extents=[22, 30, 14])
    orejas.apply_translation([0, 0, -(R_MOTOR + 9)])
    s, c = casquillo([0, 0, 1], s0=R_MOTOR + 8, cable=False)
    cortes = c + [
        cil(R_MOTOR, -40, 40, y),  # pasa de lado a lado: el casquillo es más ancho que el anillo
        trimesh.creation.box(extents=[2.0, 32, 2 * R_MOTOR]).apply_translation([0, 0, -R_MOTOR - 6]),
        cil(1.7, -12, 12, [1, 0, 0], [0, -7, -(R_MOTOR + 9)], sec=24),
        cil(1.7, -12, 12, [1, 0, 0], [0, 7, -(R_MOTOR + 9)], sec=24),
        # Salida de cables del motor hacia el interior del tubo
        cil(6.0, R_MOTOR - 2, R_MOTOR + 9, [0, 0, 1], sec=32),
    ]
    return resta(union([anillo, orejas, s]), cortes)


def probeta():
    """Tres anillos con diámetros 30.2 / 30.4 / 30.6 para calibrar la holgura."""
    anillos = []
    for i, dia in enumerate((30.2, 30.4, 30.6)):
        a = resta(cil(dia / 2 + 3, 0, 12), [cil(dia / 2, -1, 13)])
        # Marcas: 1, 2 o 3 muescas para saber cuál es cuál
        for k in range(i + 1):
            ang = math.radians(90 + (k - i / 2) * 14)
            m = cil(1.0, -1, 13, [0, 0, 1], [(dia / 2 + 3) * math.cos(ang), (dia / 2 + 3) * math.sin(ang), 0], sec=16)
            a = resta(a, [m])
        a.apply_translation([i * 42.0, 0, 0])
        anillos.append(a)
    return union(anillos)


def tubo(largo):
    return resta(cil(TUBO_OD / 2, 0, largo), [cil(TUBO_ID / 2, -1, largo + 1)])


# ── Rueda ────────────────────────────────────────────────────────────────────
def rin():
    """Rin de PETG. La llanta de Ecoflex se cuela directo sobre él."""
    a = ANCHO_RUEDA
    aro = resta(cil(R_NUCLEO, 3, a - 3), [cil(R_NUCLEO - 3, 2, a - 2)])
    pestanas = [resta(cil(R_PESTANA, 0, 3), [cil(R_NUCLEO - 3, -1, 4)]),
                resta(cil(R_PESTANA, a - 3, a), [cil(R_NUCLEO - 3, a - 4, a + 1)])]
    # Costillas transversales: el silicón no se pega al PETG, así que la
    # llanta se traba mecánicamente (par) y con las pestañas (lateral).
    costillas = []
    for k in range(N_TACOS):
        b = trimesh.creation.box(extents=[4, 4, a - 6])
        b.apply_translation([R_NUCLEO + 1.0, 0, a / 2])
        b.apply_transform(tf.rotation_matrix(2 * math.pi * (k + 0.5) / N_TACOS, [0, 0, 1]))
        costillas.append(b)
    alma = cil(R_NUCLEO - 2, 4, 9)
    maza = cil(12.0, 4, 32)
    cuerpo = union([aro, alma, maza] + pestanas + costillas)
    cortes = []
    for k in range(6):
        ang = 2 * math.pi * k / 6
        cortes.append(cil(14.0, 3, 10, [0, 0, 1], [36 * math.cos(ang), 36 * math.sin(ang), 0], sec=48))
    # Barreno en D para flecha de 6 mm (plano a 5.5 mm) y prisionero M3
    flecha = resta(cil(3.1, 3, 33, sec=48), [trimesh.creation.box(extents=[3, 8, 40]).apply_translation([2.75 + 1.5, 0, 18])])
    cortes += [flecha, cil(1.4, 0, 13, [1, 0, 0], [0, 0, 24], sec=16)]
    return resta(cuerpo, cortes)


def envolvente_llanta():
    banda = cil(R_BANDA, 0, ANCHO_RUEDA)
    tacos = []
    for k in range(N_TACOS):
        b = trimesh.creation.box(extents=[R_TACO - R_BANDA + 1, ANCHO_TACO, ANCHO_RUEDA])
        b.apply_translation([(R_TACO + R_BANDA - 1) / 2, 0, ANCHO_RUEDA / 2])
        b.apply_transform(tf.rotation_matrix(2 * math.pi * k / N_TACOS, [0, 0, 1]))
        tacos.append(b)
    return union([banda] + tacos)


def llanta(r):
    """Ecoflex 00-20: todo lo que hay entre el rin y el molde."""
    hueco = cil(R_NUCLEO - 3, -1, ANCHO_RUEDA + 1)
    return resta(envolvente_llanta(), [r, hueco])


def molde_mitad():
    """Medio molde (se imprimen 2 iguales). El rin hace de núcleo; se vierte por arriba."""
    r_ext = R_TACO + 6
    cuerpo = union([cil(r_ext, 0, ANCHO_RUEDA), cil(r_ext, -3, 0)])
    orejas = []
    for s in (+1, -1):
        b = trimesh.creation.box(extents=[12, 14, ANCHO_RUEDA + 3])
        b.apply_translation([6, s * (r_ext + 4), (ANCHO_RUEDA - 3) / 2])
        orejas.append(b)
    cuerpo = union([cuerpo] + orejas)
    cortes = [envolvente_llanta(), cil(R_NUCLEO - 1, -4, 1)]
    for s in (+1, -1):
        for z in (12, ANCHO_RUEDA - 12):
            cortes.append(cil(2.2, -1, 14, [1, 0, 0], [0, s * (r_ext + 4), z], sec=24))
    mitad = trimesh.creation.box(extents=[400, 400, 400]).apply_translation([-200 + 0.15, 0, 0])
    return resta(cuerpo, cortes + [mitad])


# ── Ensamble de un lado de la suspensión ─────────────────────────────────────
def rot_y(d):
    """Ángulo (grados) que, girando en Y, lleva +Z a la dirección d (plano XZ)."""
    return math.degrees(math.atan2(d[0], d[2]))


def matriz_threejs(rot):
    """Rotación de three.js para Euler [rx, ry, rz] en grados, orden 'XYZ'."""
    rx, ry, rz = (math.radians(v) for v in rot)
    return (tf.rotation_matrix(rx, [1, 0, 0]) @ tf.rotation_matrix(ry, [0, 1, 0])
            @ tf.rotation_matrix(rz, [0, 0, 1]))[:3, :3]


def ensamble(datos):
    eje_z = R_TACO                      # radio de la rueda con tacos
    c_pierna = S0 + 150 + (R_MOTOR + 8)  # pata del bogie: tubo de 150
    c_frente = S0 + 300 + (R_MOTOR + 8)  # pata delantera del balancín: tubo de 300
    cs = math.cos(math.radians(SEMIANGULO))
    sn = math.sin(math.radians(SEMIANGULO))
    p_bogie_z = eje_z + c_pierna * cs
    p_rocker_z = eje_z + c_frente * cs
    c_trasera = (p_rocker_z - p_bogie_z) / cs
    largo_trasero = round(c_trasera - S0 - 14.0, 1)
    y_rocker, y_bogie = 42.0, 0.0
    P_r = np.array([0, y_rocker, p_rocker_z])
    P_b = np.array([-c_trasera * sn, y_bogie, p_bogie_z])
    d_fr, d_tr = polar(SEMIANGULO), polar(-SEMIANGULO)
    frente = P_r + d_fr * c_frente
    medio = P_b + d_fr * c_pierna
    atras = P_b + d_tr * c_pierna

    partes = []
    gris, petg, alu, motor = "#94A3B8", "#E00034", "#CBD5E1", "#4B5563"

    def poner(nombre, archivo, color, pos, rot=(0, 0, 0), exp=(0, 0, 0)):
        # El visor (assets/js/stl-viewer.js) recentra cada STL: centro en XY y
        # base en Z = 0. Se compensa aquí para que la pieza quede donde va.
        lo, hi = trimesh.load(os.path.join(DEST, "ensamble", archivo)).bounds
        o = np.array([-(lo[0] + hi[0]) / 2, -(lo[1] + hi[1]) / 2, -lo[2]])
        pos = np.asarray(pos, float) - matriz_threejs(rot) @ o
        partes.append({"name": nombre, "file": archivo, "color": color,
                       "position": [round(float(v), 2) for v in pos],
                       "rotation": [round(float(v), 2) for v in rot],
                       "explode": [round(float(v), 2) for v in exp]})

    def poner_tubo(nombre, archivo, a, d, s_a):
        poner(nombre, archivo, alu, a + d * s_a, (0, rot_y(d), 0))

    # Balancín (rocker)
    poner("Pivote del balancín (PETG)", "../uniones/pivote.stl", petg, P_r, exp=(0, 0, 60))
    poner_tubo("Tubo delantero 300 mm (Al 6063)", "tubo-300.stl", P_r, d_fr, S0)
    poner_tubo(f"Tubo trasero {largo_trasero:g} mm (Al 6063)", "tubo-trasero.stl", P_r, d_tr, S0)
    poner("Terminal de eje (PETG)", "../uniones/terminal-eje.stl", petg, P_r + d_tr * c_trasera,
          (0, rot_y(-d_tr), 0), exp=(-40, 0, 20))
    poner("Terminal de motor delantero (PETG)", "../uniones/terminal-motor.stl", petg, frente,
          (0, rot_y(-d_fr), 0), exp=(40, 0, -20))
    # Bogie
    poner("Pivote del bogie (PETG)", "../uniones/pivote.stl", "#F59E0B", P_b, exp=(0, -60, 0))
    poner_tubo("Pata del bogie 150 mm (Al 6063)", "tubo-150.stl", P_b, d_fr, S0)
    poner_tubo("Pata del bogie 150 mm (Al 6063)", "tubo-150.stl", P_b, d_tr, S0)
    poner("Terminal de motor medio (PETG)", "../uniones/terminal-motor.stl", "#F59E0B", medio,
          (0, rot_y(-d_fr), 0), exp=(20, -60, -20))
    poner("Terminal de motor trasero (PETG)", "../uniones/terminal-motor.stl", "#F59E0B", atras,
          (0, rot_y(-d_tr), 0), exp=(-20, -60, -20))
    # Motores y ruedas: todas las ruedas quedan en la misma vía porque la
    # abrazadera puede tomar el motor en cualquier punto de su cuerpo.
    y_rueda = 60.0
    for nombre, p in (("delantera", frente), ("media", medio), ("trasera", atras)):
        base = np.array([p[0], 0, p[2]])
        poner(f"Motorreductor Ø37 {nombre} (referencia)", "motor-37.stl", motor,
              base + [0, y_rueda + 2 - 75, 0], (-90, 0, 0), exp=(0, 60, 0))
        poner(f"Rin {nombre} (PETG)", "../rueda/rin.stl", "#1D4ED8",
              base + [0, y_rueda, 0], (-90, 0, 0), exp=(0, 140, 0))
        poner(f"Llanta {nombre} (Ecoflex 00-20)", "../rueda/llanta-ecoflex.stl", "#1F2937",
              base + [0, y_rueda, 0], (-90, 0, 0), exp=(0, 200, 0))

    datos["ensamble"] = {
        "semiangulo_deg": SEMIANGULO,
        "pivote_balancin_mm": [round(v, 1) for v in P_r],
        "pivote_bogie_mm": [round(v, 1) for v in P_b],
        "ejes_x_mm": {"delantera": round(frente[0], 1), "media": round(medio[0], 1), "trasera": round(atras[0], 1)},
        "distancia_entre_ejes_mm": round(frente[0] - atras[0], 1),
        "largo_total_mm": round(frente[0] - atras[0] + 2 * R_TACO, 1),
        "largo_tubo_trasero_mm": largo_trasero,
        "altura_pivote_balancin_mm": round(p_rocker_z, 1),
    }
    return partes, largo_trasero


def motor_ref():
    """Marcador de motorreductor Ø37 × 75 mm con flecha de 6 × 26 mm (no se imprime)."""
    return union([cil(R_MOTOR - 0.2, 0, 75), cil(3.0, 75, 101, sec=32)])


def guardar(m, ruta, datos, material=None, densidad=None):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    m.export(ruta)
    rel = os.path.relpath(ruta, DEST)
    info = {"volumen_cm3": round(m.volume / 1000, 1),
            "envolvente_mm": [round(float(v), 1) for v in m.extents],
            "estanca": bool(m.is_watertight),
            "kb": round(os.path.getsize(ruta) / 1000)}
    if densidad:
        info["material"] = material
        info["masa_solida_g"] = round(m.volume / 1000 * densidad, 1)
    datos["piezas"][rel] = info
    print(f"  {rel:32s} {info['volumen_cm3']:7.1f} cm³  {info['envolvente_mm']}  "
          f"{'estanca' if info['estanca'] else 'ABIERTA'}  {info['kb']} KB")


def main():
    datos = {"parametros": {"tubo_od": TUBO_OD, "tubo_id": TUBO_ID, "barreno_casquillo": 2 * R_BORE,
                            "pared": PARED, "profundidad": PROF, "tope": S0}, "piezas": {}}
    PETG, ECO, AL = 1.27, 1.07, 2.70
    u = os.path.join(DEST, "uniones")
    guardar(codo(90), f"{u}/codo-90.stl", datos, "PETG", PETG)
    guardar(codo(120), f"{u}/codo-120.stl", datos, "PETG", PETG)
    guardar(union_t(), f"{u}/union-t.stl", datos, "PETG", PETG)
    guardar(cople(), f"{u}/cople-recto.stl", datos, "PETG", PETG)
    guardar(pivote(), f"{u}/pivote.stl", datos, "PETG", PETG)
    guardar(terminal_eje(), f"{u}/terminal-eje.stl", datos, "PETG", PETG)
    guardar(terminal_motor(), f"{u}/terminal-motor.stl", datos, "PETG", PETG)
    guardar(probeta(), f"{u}/probeta-ajuste.stl", datos, "PETG", PETG)

    w = os.path.join(DEST, "rueda")
    r = rin()
    guardar(r, f"{w}/rin.stl", datos, "PETG", PETG)
    guardar(llanta(r), f"{w}/llanta-ecoflex.stl", datos, "Ecoflex 00-20", ECO)
    guardar(molde_mitad(), f"{w}/molde-llanta-mitad.stl", datos, "PETG", PETG)

    e = os.path.join(DEST, "ensamble")
    guardar(tubo(300), f"{e}/tubo-300.stl", datos, "Al 6063", AL)
    guardar(tubo(150), f"{e}/tubo-150.stl", datos, "Al 6063", AL)
    guardar(tubo(LARGO_TRASERO), f"{e}/tubo-trasero.stl", datos, "Al 6063", AL)
    guardar(motor_ref(), f"{e}/motor-37.stl", datos)
    partes, largo_trasero = ensamble(datos)
    assert abs(largo_trasero - LARGO_TRASERO) < 0.5, largo_trasero
    with open(f"{e}/suspension-lado.json", "w", encoding="utf-8") as f:
        json.dump({"note": "Un lado de la suspensión balancín-bogie con tubo de Al 6063 Ø30 × 1.5 y uniones de PETG. "
                           "Lo genera tools/r1_uniones_rover.py.", "parts": partes}, f, ensure_ascii=False, indent=1)
    with open(os.path.join(DEST, "datos.json"), "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=1)
    print(json.dumps(datos["ensamble"], ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
