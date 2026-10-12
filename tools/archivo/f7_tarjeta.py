#!/usr/bin/env python3
"""F7 — Tarjeta de control de los brazos (ESP32-C3 Super Mini), proyecto de KiCad 7.

Una sola lista de componentes y conexiones (NETLIST, abajo) genera el
esquemático y la PCB, así que los dos no pueden contradecirse.

Pasos:
    python3 tools/f7_tarjeta.py esquematico   # .kicad_sch + biblioteca propia
    python3 tools/f7_tarjeta.py pcb           # coloca componentes y asigna redes
    python3 tools/f7_tarjeta.py rutear        # Freerouting (requiere java y FREEROUTING_JAR)
    python3 tools/f7_tarjeta.py exportar      # ERC, DRC, PDF, Gerber, barrenos, imágenes

Salida: assets/brazos/electronica/kicad/ y assets/brazos/electronica/fabricacion/
"""
import json
import os
import re
import subprocess
import sys
import uuid

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(RAIZ, "assets/brazos/electronica/kicad")
FAB = os.path.join(RAIZ, "assets/brazos/electronica/fabricacion")
PROY = "tarjeta_brazo"
SIMBOLOS = "/usr/share/kicad/symbols"
HUELLAS = "/usr/share/kicad/footprints"

# ---------------------------------------------------------------------------
# Componentes: referencia -> (símbolo, valor, huella, {pin: red})
# Pines del ESP32-C3 Super Mini con el USB-C hacia arriba:
#   izquierda 1-8:  5V GND 3V3 GPIO4 GPIO3 GPIO2 GPIO1 GPIO0
#   derecha  9-16:  GPIO5 GPIO6 GPIO7 GPIO8 GPIO9 GPIO10 GPIO20 GPIO21
# ---------------------------------------------------------------------------
NC = None
NETLIST = {
    "U1": ("brazo:ESP32-C3_SuperMini", "ESP32-C3 Super Mini", "brazo:ESP32-C3_SuperMini",
           {"1": "+5V_MOD", "2": "GND", "3": "+3V3", "4": "SERVO_BASE", "5": "POT_CODO",
            "6": NC, "7": "POT_HOMBRO", "8": "POT_BASE",
            "9": "SERVO_HOMBRO", "10": "SERVO_CODO", "11": "SERVO_PINZA", "12": NC,
            "13": NC, "14": "INTERRUPTOR", "15": NC, "16": NC}),
    "J1": ("Connector:Screw_Terminal_01x02", "Entrada 5 V 3 A",
           "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2_1x02_P5.00mm_Horizontal",
           {"1": "VIN", "2": "GND"}),
    "F1": ("Device:Polyfuse", "MF-RG300 (3 A)", "Fuse:Fuse_Bourns_MF-RG300", {"1": "VIN", "2": "+5V"}),
    "D1": ("Device:D_Schottky", "1N5819", "Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal",
           {"1": "+5V_MOD", "2": "+5V"}),
    "C1": ("Device:C_Polarized", "1000 µF 10 V", "Capacitor_THT:CP_Radial_D10.0mm_P5.00mm",
           {"1": "+5V", "2": "GND"}),
    "C2": ("Device:C", "100 nF", "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm", {"1": "+5V", "2": "GND"}),
    "C3": ("Device:C", "100 nF", "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm", {"1": "POT_BASE", "2": "GND"}),
    "C4": ("Device:C", "100 nF", "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm", {"1": "POT_HOMBRO", "2": "GND"}),
    "C5": ("Device:C", "100 nF", "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm", {"1": "POT_CODO", "2": "GND"}),
    "R1": ("Device:R", "1 kΩ", "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal",
           {"1": "+5V", "2": "LED_PWR"}),
    "R2": ("Device:R", "1 kΩ", "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal",
           {"1": "+3V3", "2": "V_POT"}),
    "D2": ("Device:LED", "LED verde 3 mm", "LED_THT:LED_D3.0mm", {"1": "GND", "2": "LED_PWR"}),
    "J2": ("Connector_Generic:Conn_01x03", "Servo base", "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical",
           {"1": "GND", "2": "+5V", "3": "SERVO_BASE"}),
    "J3": ("Connector_Generic:Conn_01x03", "Servo hombro", "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical",
           {"1": "GND", "2": "+5V", "3": "SERVO_HOMBRO"}),
    "J4": ("Connector_Generic:Conn_01x03", "Servo codo", "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical",
           {"1": "GND", "2": "+5V", "3": "SERVO_CODO"}),
    "J5": ("Connector_Generic:Conn_01x03", "Servo pinza", "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical",
           {"1": "GND", "2": "+5V", "3": "SERVO_PINZA"}),
    "RV1": ("Device:R_Potentiometer", "10 kΩ lineal (base)", "Potentiometer_THT:Potentiometer_Alps_RK09K_Single_Vertical",
            {"1": "GND", "2": "POT_BASE", "3": "V_POT"}),
    "RV2": ("Device:R_Potentiometer", "10 kΩ lineal (hombro)", "Potentiometer_THT:Potentiometer_Alps_RK09K_Single_Vertical",
            {"1": "GND", "2": "POT_HOMBRO", "3": "V_POT"}),
    "RV3": ("Device:R_Potentiometer", "10 kΩ lineal (codo)", "Potentiometer_THT:Potentiometer_Alps_RK09K_Single_Vertical",
            {"1": "GND", "2": "POT_CODO", "3": "V_POT"}),
    "SW1": ("Switch:SW_SPDT", "Pinza abrir/cerrar", "Button_Switch_THT:SW_Slide_SPDT_Straight_CK_OS102011MS2Q",
            {"1": "GND", "2": "INTERRUPTOR", "3": NC}),
    "H1": ("Mechanical:MountingHole", "M3", "MountingHole:MountingHole_3.2mm_M3", {}),
    "H2": ("Mechanical:MountingHole", "M3", "MountingHole:MountingHole_3.2mm_M3", {}),
    "H3": ("Mechanical:MountingHole", "M3", "MountingHole:MountingHole_3.2mm_M3", {}),
    "H4": ("Mechanical:MountingHole", "M3", "MountingHole:MountingHole_3.2mm_M3", {}),
}
REDES_POTENCIA = ["VIN", "+5V", "GND", "+5V_MOD"]
SIMBOLOS_ALIMENTACION = {"GND": "power:GND", "+5V": "power:+5V", "+3V3": "power:+3V3"}

TITULO = "Tarjeta de control de los brazos robóticos"
EMPRESA = "Integración Mecatrónica Otoño 2026"
AUTORES = "J. P. Martha · C. S. Ortega · S. A. Velázquez"


def uid():
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# Lectura de bibliotecas (s-expresiones)
# ---------------------------------------------------------------------------
TOKEN = re.compile(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()]+')


def leer_sexp(texto):
    pila = [[]]
    for t in TOKEN.findall(texto):
        if t == "(":
            pila.append([])
        elif t == ")":
            x = pila.pop()
            pila[-1].append(x)
        else:
            pila[-1].append(t)
    return pila[0]


def escribir_sexp(n, nivel=0):
    if not isinstance(n, list):
        return n
    if all(not isinstance(x, list) for x in n):
        return "(" + " ".join(n) + ")"
    sangria = "  " * (nivel + 1)
    partes = [escribir_sexp(x, nivel + 1) for x in n]
    return "(" + partes[0] + "".join("\n" + sangria + p for p in partes[1:]) + ")"


_cache = {}


def simbolo_lib(lib_id):
    """Devuelve el símbolo de la biblioteca de KiCad con el nombre 'Lib:Nombre'."""
    lib, nombre = lib_id.split(":")
    if lib == "brazo":
        return simbolo_modulo()
    if lib not in _cache:
        _cache[lib] = leer_sexp(open(f"{SIMBOLOS}/{lib}.kicad_sym", encoding="utf-8").read())[0]
    for s in _cache[lib]:
        if isinstance(s, list) and s[0] == "symbol" and s[1].strip('"') == nombre:
            s = [x for x in s]
            s[1] = f'"{lib_id}"'
            return s
    raise KeyError(lib_id)


def pines_de(simbolo):
    pines = {}

    def recorrer(n):
        for x in n:
            if isinstance(x, list):
                if x[0] == "pin":
                    at = next(y for y in x if isinstance(y, list) and y[0] == "at")
                    num = next(y for y in x if isinstance(y, list) and y[0] == "number")[1].strip('"')
                    pines[num] = (float(at[1]), float(at[2]), float(at[3]))
                else:
                    recorrer(x)
    recorrer(simbolo)
    return pines


# ---------------------------------------------------------------------------
# Símbolo y huella propios del ESP32-C3 Super Mini
# ---------------------------------------------------------------------------
PINES_MODULO = [
    ("1", "5V", "power_in"), ("2", "GND", "power_in"), ("3", "3V3", "power_out"),
    ("4", "GPIO4", "bidirectional"), ("5", "GPIO3", "bidirectional"), ("6", "GPIO2", "bidirectional"),
    ("7", "GPIO1", "bidirectional"), ("8", "GPIO0", "bidirectional"),
    ("9", "GPIO5", "bidirectional"), ("10", "GPIO6", "bidirectional"), ("11", "GPIO7", "bidirectional"),
    ("12", "GPIO8", "bidirectional"), ("13", "GPIO9", "bidirectional"), ("14", "GPIO10", "bidirectional"),
    ("15", "GPIO20/RX", "bidirectional"), ("16", "GPIO21/TX", "bidirectional"),
]


def simbolo_modulo(nombre_lib="brazo:ESP32-C3_SuperMini"):
    fuente = '(effects (font (size 1.27 1.27)))'
    pines = []
    for i, (num, nom, tipo) in enumerate(PINES_MODULO):
        izquierda = i < 8
        fila = i if izquierda else i - 8
        x = -12.7 if izquierda else 12.7
        y = 8.89 - fila * 2.54
        ang = 0 if izquierda else 180
        pines.append(f'(pin {tipo} line (at {x} {y:.2f} {ang}) (length 2.54) (name "{nom}" {fuente}) (number "{num}" {fuente}))')
    texto = (
        f'(symbol "{nombre_lib}" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)'
        f' (property "Reference" "U" (at 0 13.97 0) {fuente})'
        f' (property "Value" "ESP32-C3 Super Mini" (at 0 11.43 0) {fuente})'
        f' (property "Footprint" "brazo:ESP32-C3_SuperMini" (at 0 -13.97 0) (effects (font (size 1.27 1.27)) hide))'
        f' (property "Datasheet" "https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf" (at 0 -16.51 0) (effects (font (size 1.27 1.27)) hide))'
        f' (property "Description" "Módulo ESP32-C3 Super Mini (RISC-V 160 MHz, Wi-Fi, BLE, USB-C)" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))'
        f' (symbol "ESP32-C3_SuperMini_0_1" (rectangle (start -10.16 10.16) (end 10.16 -11.43)'
        f' (stroke (width 0.254) (type default)) (fill (type background))))'
        f' (symbol "ESP32-C3_SuperMini_1_1" {" ".join(pines)}))'
    )
    return leer_sexp(texto)[0]


def huella_modulo():
    l = ['(footprint "ESP32-C3_SuperMini" (version 20221018) (generator tools_f7) (layer "F.Cu")',
         '  (descr "ESP32-C3 Super Mini sobre dos tiras de 8 pines, paso 2.54 mm, filas a 15.24 mm")',
         '  (tags "ESP32-C3 Super Mini modulo")',
         '  (attr through_hole)',
         '  (fp_text reference "REF**" (at 7.62 -5.2) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))',
         '  (fp_text value "ESP32-C3 Super Mini" (at 7.62 21) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))',
         '  (fp_text user "USB-C" (at 7.62 -2) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))']
    x0, x1, y0, y1 = -1.38, 16.62, -3.5, 19.02
    for capa, m in (("F.SilkS", 0.12), ("F.CrtYd", 0.5), ("F.Fab", 0)):
        a, b, c, d = x0 - m, y0 - m, x1 + m, y1 + m
        ancho = 0.05 if capa == "F.CrtYd" else 0.12
        l.append(f'  (fp_rect (start {a:.2f} {b:.2f}) (end {c:.2f} {d:.2f}) (stroke (width {ancho}) (type default)) (fill none) (layer "{capa}"))')
    for i, (num, nom, _) in enumerate(PINES_MODULO):
        izquierda = i < 8
        fila = i if izquierda else i - 8
        x = 0.0 if izquierda else 15.24
        y = fila * 2.54
        forma = "rect" if num == "1" else "circle"
        l.append(f'  (pad "{num}" thru_hole {forma} (at {x:.2f} {y:.2f}) (size 1.7 1.7) (drill 1.0) (layers "*.Cu" "*.Mask"))')
        etiqueta = nom.split("/")[0].replace("GPIO", "")
        tx = x + (2.2 if izquierda else -2.2)
        just = "left" if izquierda else "right"
        l.append(f'  (fp_text user "{etiqueta}" (at {tx:.2f} {y:.2f}) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12)) (justify {just})))')
    l.append(")")
    return "\n".join(l) + "\n"


# ---------------------------------------------------------------------------
# Esquemático
# ---------------------------------------------------------------------------
# Posición de cada símbolo en la hoja A4 (mm) y ángulo.
POS_ESQ = {
    "J1": (34.29, 50.8, 0), "F1": (53.34, 45.72, 90), "D1": (86.36, 45.72, 0),
    "C1": (60.96, 68.58, 0), "C2": (78.74, 68.58, 0), "R1": (35.56, 76.2, 0), "D2": (39.37, 101.6, 0),
    "U1": (139.7, 76.2, 0),
    "J2": (226.06, 50.8, 0), "J3": (226.06, 71.12, 0), "J4": (226.06, 91.44, 0), "J5": (226.06, 111.76, 0),
    "R2": (22.86, 134.62, 0),
    "RV1": (60.96, 134.62, 0), "RV2": (99.06, 134.62, 0), "RV3": (137.16, 134.62, 0),
    "C3": (76.2, 152.4, 0), "C4": (114.3, 152.4, 0), "C5": (152.4, 152.4, 0),
    "SW1": (200.66, 147.32, 0),
    "H1": (124.46, 109.22, 0), "H2": (134.62, 109.22, 0), "H3": (144.78, 109.22, 0), "H4": (154.94, 109.22, 0),
}
# Desplazamiento (dx, dy, justificación) de la referencia y el valor de cada tipo de símbolo.
CAMPOS = {
    "*": ((0, -6.35, "center"), (0, 6.35, "center")),
    "Device:R": ((2.54, -1.27, "left"), (2.54, 1.27, "left")),
    "Device:C": ((2.54, -1.27, "left"), (2.54, 1.27, "left")),
    "Device:C_Polarized": ((2.54, -1.27, "left"), (2.54, 1.27, "left")),
    "Device:LED": ((0, -3.81, "center"), (0, 3.81, "center")),
    "Device:R_Potentiometer": ((-2.54, -1.27, "right"), (-2.54, 1.27, "right")),
    "Device:Polyfuse": ((0, -3.81, "center"), (0, 3.81, "center")),
    "Device:D_Schottky": ((0, -3.81, "center"), (0, 3.81, "center")),
    "brazo:ESP32-C3_SuperMini": ((0, -13.97, "center"), (0, 15.24, "center")),
    "Connector_Generic:Conn_01x03": ((0, -5.08, "center"), (5.08, 0, "left")),
    "Connector:Screw_Terminal_01x02": ((0, -3.81, "center"), (0, 5.08, "center")),
    "Switch:SW_SPDT": ((0, -5.08, "center"), (0, 5.08, "center")),
    "Mechanical:MountingHole": ((0, -3.81, "center"), (0, 3.81, "center")),
}

BLOQUES = [
    ("Alimentación", 20, 30), ("Microcontrolador", 115, 30), ("Servos", 205, 30),
    ("Potenciómetros (control manual)", 45, 117), ("Interruptor de la pinza", 182, 120),
    ("Barrenos de montaje", 120, 100),
]


def jus(j):
    return "" if j == "center" else f" (justify {j})"


def rot(px, py, ang):
    """Rota un punto del símbolo (coordenadas de biblioteca, y hacia arriba)."""
    import math
    a = math.radians(ang)
    return px * math.cos(a) - py * math.sin(a), px * math.sin(a) + py * math.cos(a)


def esquematico():
    os.makedirs(DEST, exist_ok=True)
    raiz = uid()
    lib_ids = sorted({v[0] for v in NETLIST.values()} | set(SIMBOLOS_ALIMENTACION.values()) | {"power:PWR_FLAG"})
    libs = [escribir_sexp(simbolo_lib(i), 1) for i in lib_ids]
    cuerpo = []
    n_pwr = [0]

    def texto(t, x, y, tam=1.27, negrita=False):
        b = " bold" if negrita else ""
        cuerpo.append(f'(text "{t}" (at {x} {y} 0) (effects (font (size {tam} {tam}){b}) (justify left bottom)) (uuid {uid()}))')

    def cable(x1, y1, x2, y2):
        cuerpo.append(f'(wire (pts (xy {x1:.2f} {y1:.2f}) (xy {x2:.2f} {y2:.2f})) (stroke (width 0) (type default)) (uuid {uid()}))')

    def simbolo(lib_id, ref, valor, x, y, ang, huella="", pines=(), en_bom=True):
        (rx, ry, rj), (vx, vy, vj) = CAMPOS.get(lib_id, CAMPOS["*"])
        if lib_id.startswith("power:"):
            (rx, ry, rj), (vx, vy, vj) = (0, 0, "left"), ((0, 3.81, "left") if "GND" in lib_id else (0, -3.81, "left"))
            vj = "center"
            import math
            a = math.radians(ang)
            vx, vy = vx * math.cos(a) + vy * math.sin(a), -vx * math.sin(a) + vy * math.cos(a)
        props = [
            f'(property "Reference" "{ref}" (at {x + rx:.2f} {y + ry:.2f} {ang if ang in (90, 270) else 0}) (effects (font (size 1.27 1.27)){jus(rj)}{" hide" if ref.startswith("#") else ""}))',
            f'(property "Value" "{valor}" (at {x + vx:.2f} {y + vy:.2f} {ang if ang in (90, 270) and not lib_id.startswith("power:") else 0}) (effects (font (size 1.27 1.27)){jus(vj)}{" hide" if ref.startswith("#FLG") else ""}))',
            f'(property "Footprint" "{huella}" (at {x:.2f} {y:.2f} 0) (effects (font (size 1.27 1.27)) hide))',
            f'(property "Datasheet" "~" (at {x:.2f} {y:.2f} 0) (effects (font (size 1.27 1.27)) hide))',
        ]
        pins = " ".join(f'(pin "{p}" (uuid {uid()}))' for p in pines)
        cuerpo.append(
            f'(symbol (lib_id "{lib_id}") (at {x:.2f} {y:.2f} {ang}) (unit 1) (in_bom {"yes" if en_bom else "no"}) (on_board {"yes" if en_bom else "no"}) (dnp no) (uuid {uid()}) '
            + " ".join(props) + f" {pins} (instances (project \"{PROY}\" (path \"/{raiz}\" (reference \"{ref}\") (unit 1)))))")

    def alimentacion(red, x, y, direccion):
        """Símbolo de alimentación con su gráfico hacia 'direccion' (grados, visual)."""
        n_pwr[0] += 1
        base = 270 if red == "GND" else 90
        ang = (direccion - base) % 360
        simbolo(SIMBOLOS_ALIMENTACION[red], f"#PWR{n_pwr[0]:02d}", red, x, y, ang, pines=("1",), en_bom=False)

    def bandera(x, y):
        n_pwr[0] += 1
        simbolo("power:PWR_FLAG", f"#FLG{n_pwr[0]:02d}", "PWR_FLAG", x, y, 0, pines=("1",), en_bom=False)

    for titulo, x, y in BLOQUES:
        texto(titulo, x, y, 2, True)

    for ref, (lib_id, valor, huella, conex) in NETLIST.items():
        x, y, ang = POS_ESQ[ref]
        pines = pines_de(simbolo_lib(lib_id))
        simbolo(lib_id, ref, valor, x, y, ang, huella, pines=tuple(pines))
        for num, (px, py, pang) in pines.items():
            red = conex.get(num)
            rx, ry = rot(px, py, ang)
            ex, ey = x + rx, y - ry                       # extremo del pin en la hoja (y hacia abajo)
            fuera = (pang + 180 + ang) % 360               # dirección hacia afuera del cuerpo
            dx, dy = {0: (1, 0), 90: (0, -1), 180: (-1, 0), 270: (0, 1)}[round(fuera) % 360]
            if num in conex and red is None:
                cuerpo.append(f'(no_connect (at {ex:.2f} {ey:.2f}) (uuid {uid()}))')
                continue
            if red is None:
                continue
            fx, fy = ex + dx * 2.54, ey + dy * 2.54
            cable(ex, ey, fx, fy)
            if red in SIMBOLOS_ALIMENTACION and dx == 0:
                alimentacion(red, fx, fy, round(fuera))
            elif red in SIMBOLOS_ALIMENTACION:
                just = "left" if dx > 0 else "right"
                cuerpo.append(f'(global_label "{red}" (shape passive) (at {fx:.2f} {fy:.2f} {0 if dx > 0 else 180}) (fields_autoplaced) '
                              f'(effects (font (size 1.27 1.27)) (justify {just})) (uuid {uid()}) '
                              f'(property "Intersheetrefs" "${{INTERSHEET_REFS}}" (at {fx:.2f} {fy:.2f} 0) (effects (font (size 1.27 1.27)) hide)))')
            else:
                just = {0: "left", 180: "right", 90: "left", 270: "right"}[round(fuera) % 360]
                cuerpo.append(f'(label "{red}" (at {fx:.2f} {fy:.2f} {round(fuera) % 180}) (fields_autoplaced) '
                              f'(effects (font (size 1.27 1.27)) (justify {just} bottom)) (uuid {uid()}))')

    # Banderas de alimentación: VIN, GND y +5V_MOD vienen de fuera de la hoja o pasan por el diodo.
    for red, x, y in (("VIN", 17.78, 35.56), ("GND", 45.72, 58.42), ("+5V_MOD", 101.6, 35.56)):
        bandera(x, y)
        cable(x, y, x, y + 5.08)
        if red == "GND":
            alimentacion("GND", x, y + 5.08, 270)
        else:
            cuerpo.append(f'(label "{red}" (at {x:.2f} {y + 5.08:.2f} 0) (fields_autoplaced) (effects (font (size 1.27 1.27)) (justify left bottom)) (uuid {uid()}))')

    notas = [
        "Notas:",
        "1. Los servos se alimentan directo de +5V (fuente externa de 5 V, 3 A); el USB solo alimenta al ESP32-C3.",
        "2. D1 evita que la fuente externa regrese corriente al USB de la computadora.",
        "3. R2 baja el tope de los potenciómetros a ~2.54 V: el ADC del ESP32-C3 mide bien hasta 2.5 V (atenuación de 12 dB).",
        "4. Con el interruptor cerrado a GND la pinza abre (GPIO10 con pull-up interno).",
        "5. GPIO2, GPIO8 y GPIO9 son pines de arranque; GPIO8 tiene el LED de la placa.",
    ]
    for i, n in enumerate(notas):
        texto(n, 20, 168 + i * 4, 1.5 if i == 0 else 1.27, i == 0)

    sch = (f'(kicad_sch (version 20230121) (generator eeschema)\n  (uuid {raiz})\n  (paper "A4")\n'
           f'  (title_block (title "{TITULO}") (date "2026-10-12") (rev "1.0") (company "{EMPRESA}")'
           f' (comment 1 "{AUTORES}") (comment 2 "ESP32-C3 Super Mini · 4 servos SG90 · 3 potenciómetros · interruptor"))\n'
           f'  (lib_symbols\n  ' + "\n  ".join(libs) + "\n  )\n  "
           + "\n  ".join(cuerpo) + '\n  (sheet_instances (path "/" (page "1")))\n)\n')
    open(os.path.join(DEST, PROY + ".kicad_sch"), "w", encoding="utf-8").write(sch)

    # Biblioteca propia (símbolo y huella) y tablas de bibliotecas del proyecto.
    open(os.path.join(DEST, "brazo.kicad_sym"), "w", encoding="utf-8").write(
        "(kicad_symbol_lib (version 20220914) (generator tools_f7)\n  "
        + escribir_sexp(simbolo_modulo("ESP32-C3_SuperMini"), 1) + "\n)\n")
    os.makedirs(os.path.join(DEST, "brazo.pretty"), exist_ok=True)
    open(os.path.join(DEST, "brazo.pretty", "ESP32-C3_SuperMini.kicad_mod"), "w", encoding="utf-8").write(huella_modulo())
    open(os.path.join(DEST, "sym-lib-table"), "w").write(
        '(sym_lib_table\n  (lib (name "brazo")(type "KiCad")(uri "${KIPRJMOD}/brazo.kicad_sym")(options "")(descr "Simbolos del proyecto"))\n)\n')
    libs_fp = sorted({h.split(":")[0] for _, _, h, _ in NETLIST.values()} - {"brazo"})
    open(os.path.join(DEST, "fp-lib-table"), "w").write(
        '(fp_lib_table\n  (lib (name "brazo")(type "KiCad")(uri "${KIPRJMOD}/brazo.pretty")(options "")(descr "Huellas del proyecto"))\n'
        + "".join(f'  (lib (name "{l}")(type "KiCad")(uri "${{KICAD7_FOOTPRINT_DIR}}/{l}.pretty")(options "")(descr ""))\n' for l in libs_fp)
        + ")\n")
    proyecto()
    print("  esquemático y biblioteca escritos en", os.path.relpath(DEST, RAIZ))


def proyecto():
    """Archivo .kicad_pro con las clases de red (pistas de potencia más anchas)."""
    pro = {
        "board": {"design_settings": {"rules": {"min_clearance": 0.2, "min_track_width": 0.25,
                                                 "min_via_diameter": 0.6, "min_through_hole_diameter": 0.3}}},
        "meta": {"filename": PROY + ".kicad_pro", "version": 1},
        "net_settings": {
            "classes": [
                {"name": "Default", "clearance": 0.25, "track_width": 0.4, "via_diameter": 0.8, "via_drill": 0.4,
                 "microvia_diameter": 0.3, "microvia_drill": 0.1, "diff_pair_width": 0.2, "diff_pair_gap": 0.25,
                 "diff_pair_via_gap": 0.25, "wire_width": 6, "bus_width": 12, "line_style": 0,
                 "schematic_color": "rgba(0, 0, 0, 0.000)", "pcb_color": "rgba(0, 0, 0, 0.000)"},
                {"name": "Potencia", "clearance": 0.25, "track_width": 1.2, "via_diameter": 1.2, "via_drill": 0.6,
                 "microvia_diameter": 0.3, "microvia_drill": 0.1, "diff_pair_width": 0.2, "diff_pair_gap": 0.25,
                 "diff_pair_via_gap": 0.25, "wire_width": 6, "bus_width": 12, "line_style": 0,
                 "schematic_color": "rgba(0, 0, 0, 0.000)", "pcb_color": "rgba(0, 0, 0, 0.000)"},
            ],
            "meta": {"version": 3},
            "net_colors": None,
            "netclass_assignments": None,
            "netclass_patterns": [{"netclass": "Potencia", "pattern": r} for r in REDES_POTENCIA],
        },
        "pcbnew": {"last_paths": {}, "page_layout_descr_file": ""},
        "schematic": {"legacy_lib_dir": "", "legacy_lib_list": []},
        "sheets": [], "text_variables": {},
    }
    json.dump(pro, open(os.path.join(DEST, PROY + ".kicad_pro"), "w"), indent=2)


# ---------------------------------------------------------------------------
# PCB
# ---------------------------------------------------------------------------
ANCHO, ALTO = 90.0, 66.0
ORIGEN = (100.0, 100.0)
# Posición (x, y desde la esquina superior izquierda de la tarjeta), ángulo, cara.
POS_PCB = {
    "U1": (37.38, 4.6, 0),
    "J1": (11.0, 10.0, 0),
    "F1": (8.0, 20.0, 0),
    "D1": (16.0, 29.0, 0),
    "C1": (10.5, 39.0, 0),
    "C2": (21.0, 37.0, 0),
    "R1": (4.5, 46.5, 0),
    "D2": (5.5, 55.0, 0),
    "J2": (82.0, 9.0, 0), "J3": (82.0, 21.0, 0), "J4": (82.0, 33.0, 0), "J5": (82.0, 45.0, 0),
    "R2": (11.0, 60.0, 0),
    "RV1": (28.0, 50.0, 0), "RV2": (44.0, 50.0, 0), "RV3": (60.0, 50.0, 0),
    "C3": (26.0, 42.0, 0), "C4": (42.0, 42.0, 0), "C5": (58.0, 42.0, 0),
    "SW1": (77.0, 55.5, 0),
    "H1": (4.0, 4.0, 0), "H2": (ANCHO - 4.0, 4.0, 0), "H3": (4.0, ALTO - 4.0, 0), "H4": (ANCHO - 4.0, ALTO - 4.0, 0),
}
ETIQUETAS_SERIGRAFIA = [
    ("BASE", 86.5, 11.5), ("HOMBRO", 86.5, 23.5), ("CODO", 86.5, 35.5), ("PINZA", 86.5, 47.5),
    ("G", 79.6, 9.0), ("+", 79.6, 11.54), ("S", 79.6, 14.08),
    ("5V 3A", 24.0, 10.0),
    ("BASE", 31.5, 60.6), ("HOMBRO", 47.5, 60.6), ("CODO", 63.5, 60.6),
    ("PINZA", 79.8, 58.6),
]


def mm(v):
    import pcbnew
    return pcbnew.FromMM(v)


def pcb():
    import pcbnew
    ruta = os.path.join(DEST, PROY + ".kicad_pcb")
    tablero = pcbnew.NewBoard(ruta)
    ox, oy = ORIGEN

    redes = {}
    for _, (_, _, _, conex) in NETLIST.items():
        for red in conex.values():
            if red and red not in redes:
                ni = pcbnew.NETINFO_ITEM(tablero, red)
                tablero.Add(ni)
                redes[red] = ni

    for ref, (lib_id, valor, huella, conex) in NETLIST.items():
        lib, nombre = huella.split(":")
        carpeta = os.path.join(DEST, "brazo.pretty") if lib == "brazo" else os.path.join(HUELLAS, lib + ".pretty")
        fp = pcbnew.FootprintLoad(carpeta, nombre)
        fp.SetReference(ref)
        fp.SetValue(valor)
        fp.SetFPID(pcbnew.LIB_ID(lib, nombre))
        x, y, ang = POS_PCB[ref]
        fp.SetPosition(pcbnew.VECTOR2I(mm(ox + x), mm(oy + y)))
        fp.SetOrientationDegrees(ang)
        if ref.startswith("H"):
            fp.Reference().SetVisible(False)
        tablero.Add(fp)
        for pad in fp.Pads():
            red = conex.get(pad.GetNumber())
            if red:
                pad.SetNet(redes[red])

    # Contorno con esquinas redondeadas
    r = 3.0
    puntos = [((r, 0), (ANCHO - r, 0)), ((ANCHO, r), (ANCHO, ALTO - r)),
              ((ANCHO - r, ALTO), (r, ALTO)), ((0, ALTO - r), (0, r))]
    for (a, b) in puntos:
        s = pcbnew.PCB_SHAPE(tablero)
        s.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s.SetStart(pcbnew.VECTOR2I(mm(ox + a[0]), mm(oy + a[1])))
        s.SetEnd(pcbnew.VECTOR2I(mm(ox + b[0]), mm(oy + b[1])))
        s.SetLayer(pcbnew.Edge_Cuts)
        s.SetWidth(mm(0.1))
        tablero.Add(s)
    for cx, cy, a0 in ((r, r, 180), (ANCHO - r, r, 270), (ANCHO - r, ALTO - r, 0), (r, ALTO - r, 90)):
        s = pcbnew.PCB_SHAPE(tablero)
        s.SetShape(pcbnew.SHAPE_T_ARC)
        s.SetCenter(pcbnew.VECTOR2I(mm(ox + cx), mm(oy + cy)))
        import math
        sx = cx + r * math.cos(math.radians(a0))
        sy = cy + r * math.sin(math.radians(a0))
        s.SetStart(pcbnew.VECTOR2I(mm(ox + sx), mm(oy + sy)))
        s.SetArcAngleAndEnd(pcbnew.EDA_ANGLE(90, pcbnew.DEGREES_T))
        s.SetLayer(pcbnew.Edge_Cuts)
        s.SetWidth(mm(0.1))
        tablero.Add(s)

    def texto(t, x, y, capa=pcbnew.F_SilkS, tam=1.0):
        tx = pcbnew.PCB_TEXT(tablero)
        tx.SetText(t)
        tx.SetPosition(pcbnew.VECTOR2I(mm(ox + x), mm(oy + y)))
        tx.SetLayer(capa)
        tx.SetTextSize(pcbnew.VECTOR2I(mm(tam), mm(tam)))
        tx.SetTextThickness(mm(tam * 0.15))
        tx.SetMirrored(capa == pcbnew.B_SilkS)   # que se lea bien viendo la cara inferior
        tablero.Add(tx)

    for t, x, y in ETIQUETAS_SERIGRAFIA:
        texto(t, x, y)
    texto("BRAZOS ROBOTICOS · ESP32-C3 · v1.0", ANCHO / 2, ALTO - 1.8, tam=1.0)
    texto("Integracion Mecatronica 2026", ANCHO / 2, ALTO - 3.4, pcbnew.B_SilkS, 1.2)

    pcbnew.SaveBoard(ruta, tablero)
    print("  PCB colocada en", os.path.relpath(ruta, RAIZ))


def rutear():
    import pcbnew
    jar = os.environ.get("FREEROUTING_JAR")
    if not jar:
        sys.exit("Define FREEROUTING_JAR con la ruta de freerouting-2.x.jar")
    ruta = os.path.join(DEST, PROY + ".kicad_pcb")
    tablero = pcbnew.LoadBoard(ruta)
    dsn = os.path.join(DEST, PROY + ".dsn")
    ses = os.path.join(DEST, PROY + ".ses")
    pcbnew.ExportSpecctraDSN(tablero, dsn)
    subprocess.run(["java", "-jar", jar, "-de", dsn, "-do", ses, "-mp", "30", "--gui.enabled=false"],
                   check=True, timeout=1200)
    importar_ses(tablero, ses)

    # Planos de tierra en las dos caras
    ox, oy = ORIGEN
    gnd = tablero.FindNet("GND")
    for capa in (pcbnew.F_Cu, pcbnew.B_Cu):
        z = pcbnew.ZONE(tablero)
        z.SetLayer(capa)
        z.SetNet(gnd)
        z.SetLocalClearance(mm(0.4))
        z.SetMinThickness(mm(0.3))
        z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
        z.SetThermalReliefGap(mm(0.5))
        z.SetThermalReliefSpokeWidth(mm(0.6))
        contorno = z.Outline()
        contorno.NewOutline()
        for px, py in ((0.5, 0.5), (ANCHO - 0.5, 0.5), (ANCHO - 0.5, ALTO - 0.5), (0.5, ALTO - 0.5)):
            contorno.Append(mm(ox + px), mm(oy + py))
        tablero.Add(z)
    pcbnew.ZONE_FILLER(tablero).Fill(tablero.Zones())
    pcbnew.SaveBoard(ruta, tablero)
    for f in (dsn, ses):
        os.remove(f)
    print("  PCB ruteada")


def verificar(netlist):
    """Compara la netlist que calcula KiCad con NETLIST, pin por pin.

    Sustituye al ERC por línea de comandos, que KiCad 7 no tiene: confirma que
    cada cable, etiqueta y símbolo de alimentación del esquemático conecta lo
    que el diseño dice, y que ninguna red quedó con un solo pin.
    """
    from collections import Counter
    arbol = leer_sexp(open(netlist, encoding="utf-8").read())[0]
    real = {}
    for n in [x for x in arbol if isinstance(x, list) and x[0] == "nets"][0][1:]:
        nombre = [y for y in n if isinstance(y, list) and y[0] == "name"][0][1].strip('"').lstrip("/")
        for nodo in [y for y in n if isinstance(y, list) and y[0] == "node"]:
            ref = [z for z in nodo if isinstance(z, list) and z[0] == "ref"][0][1].strip('"')
            pin = [z for z in nodo if isinstance(z, list) and z[0] == "pin"][0][1].strip('"')
            if not ref.startswith("#"):
                real[(ref, pin)] = nombre
    errores = []
    for ref, (_, _, _, conex) in NETLIST.items():
        for pin, red in conex.items():
            obtenido = real.get((ref, pin), "")
            if red is None and obtenido and not obtenido.startswith("unconnected"):
                errores.append(f"{ref}.{pin} debería estar libre y está en {obtenido}")
            elif red is not None and obtenido != red:
                errores.append(f"{ref}.{pin}: esperado {red}, KiCad dice {obtenido}")
    cuenta = Counter(v for v in real.values() if not v.startswith("unconnected"))
    errores += [f"la red {r} tiene un solo pin" for r, k in cuenta.items() if k < 2]
    total = sum(len(v[3]) for v in NETLIST.values())
    with open(os.path.join(FAB, "verificacion-netlist.txt"), "w", encoding="utf-8") as f:
        f.write(f"Pines revisados: {total}\nRedes: {len(cuenta)}\nDiferencias: {len(errores)}\n")
        f.writelines(e + "\n" for e in errores)
    if errores:
        raise SystemExit("La netlist no coincide:\n" + "\n".join(errores))
    print(f"  netlist verificada: {total} pines, {len(cuenta)} redes, 0 diferencias")


def importar_ses(tablero, ses):
    """Agrega a la PCB las pistas y vías de una sesión de Freerouting (.ses).

    pcbnew.ImportSpecctraSES de KiCad 7 solo funciona con el editor abierto,
    así que se lee el archivo directamente. Unidades: 0.1 µm; el eje Y va al revés.
    """
    import pcbnew
    arbol = leer_sexp(open(ses, encoding="utf-8").read())[0]

    def hijos(n, nombre):
        return [x for x in n if isinstance(x, list) and x and x[0] == nombre]

    rutas = hijos(arbol, "routes")[0]
    res = hijos(rutas, "resolution")[0]
    escala = {"um": 1e-3, "mm": 1.0, "mil": 0.0254}[res[1]] / float(res[2])   # unidades -> mm
    capas = {"F.Cu": pcbnew.F_Cu, "B.Cu": pcbnew.B_Cu}
    pistas = vias = 0
    for net in hijos(hijos(rutas, "network_out")[0], "net"):
        red = tablero.FindNet(net[1].strip('"'))
        for w in hijos(net, "wire"):
            ruta = hijos(w, "path")[0]
            capa, ancho = capas[ruta[1].strip('"')], float(ruta[2]) * escala
            pts = [(float(ruta[i]) * escala, -float(ruta[i + 1]) * escala) for i in range(3, len(ruta), 2)]
            for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
                t = pcbnew.PCB_TRACK(tablero)
                t.SetStart(pcbnew.VECTOR2I(mm(x1), mm(y1)))
                t.SetEnd(pcbnew.VECTOR2I(mm(x2), mm(y2)))
                t.SetWidth(mm(ancho))
                t.SetLayer(capa)
                t.SetNet(red)
                tablero.Add(t)
                pistas += 1
        for v in hijos(net, "via"):
            m = re.search(r"_(\d+):(\d+)_um", v[1])
            diam, broca = (int(m.group(1)) / 1000, int(m.group(2)) / 1000) if m else (0.8, 0.4)
            via = pcbnew.PCB_VIA(tablero)
            via.SetPosition(pcbnew.VECTOR2I(mm(float(v[2]) * escala), mm(-float(v[3]) * escala)))
            via.SetWidth(mm(diam))
            via.SetDrill(mm(broca))
            via.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
            via.SetNet(red)
            tablero.Add(via)
            vias += 1
    print(f"  {pistas} segmentos de pista y {vias} vías importados")


def exportar():
    import pcbnew
    sch = os.path.join(DEST, PROY + ".kicad_sch")
    pcbf = os.path.join(DEST, PROY + ".kicad_pcb")
    os.makedirs(FAB, exist_ok=True)
    gerber = os.path.join(FAB, "gerber")
    os.makedirs(gerber, exist_ok=True)

    def kc(*a):
        r = subprocess.run(["kicad-cli", *a], capture_output=True, text=True)
        if r.returncode:
            print(r.stdout, r.stderr)
            raise SystemExit("kicad-cli falló: " + " ".join(a))
        return r.stdout

    kc("sch", "export", "pdf", "-o", os.path.join(FAB, "esquematico.pdf"), sch)
    kc("sch", "export", "svg", "-o", FAB, sch)
    kc("sch", "export", "netlist", "-o", os.path.join(FAB, "netlist.net"), sch)
    verificar(os.path.join(FAB, "netlist.net"))
    kc("sch", "export", "python-bom", "-o", os.path.join(FAB, "bom.xml"), sch)
    capas = "F.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts"
    kc("pcb", "export", "gerbers", "--layers", capas, "--subtract-soldermask", "-o", gerber + "/", pcbf)
    kc("pcb", "export", "drill", "--format", "excellon", "--excellon-separate-th", "--generate-map",
       "--map-format", "pdf", "-o", gerber + "/", pcbf)
    for nombre, cap in (("pcb-cara-superior", "F.Cu,F.SilkS,F.Mask,Edge.Cuts"),
                        ("pcb-cara-inferior", "B.Cu,B.SilkS,B.Mask,Edge.Cuts")):
        args = ["pcb", "export", "svg", "--layers", cap, "--exclude-drawing-sheet", "--page-size-mode", "2",
                "-o", os.path.join(FAB, nombre + ".svg"), pcbf]
        if "inferior" in nombre:
            args.insert(-1, "--mirror")
        kc(*args)
    kc("pcb", "export", "pdf", "--layers", "F.Cu,B.Cu,F.SilkS,Edge.Cuts", "-o", os.path.join(FAB, "pcb-capas.pdf"), pcbf)
    kc("pcb", "export", "pos", "--format", "csv", "--units", "mm", "-o", os.path.join(FAB, "posiciones.csv"), pcbf)

    tablero = pcbnew.LoadBoard(pcbf)
    drc = os.path.join(FAB, "drc.rpt")
    pcbnew.WriteDRCReport(tablero, drc, pcbnew.EDA_UNITS_MILLIMETRES, True)
    texto = open(drc, encoding="utf-8").read().replace(DEST + os.sep, "")
    open(drc, "w", encoding="utf-8").write(texto)

    # Paquete para el fabricante
    import zipfile
    with zipfile.ZipFile(os.path.join(FAB, "gerber-tarjeta-brazo.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(gerber)):
            z.write(os.path.join(gerber, f), f)
    print("  exportado en", os.path.relpath(FAB, RAIZ))


if __name__ == "__main__":
    pasos = {"esquematico": esquematico, "pcb": pcb, "rutear": rutear, "exportar": exportar}
    if len(sys.argv) < 2 or sys.argv[1] not in pasos:
        sys.exit("uso: f7_tarjeta.py " + "|".join(pasos))
    pasos[sys.argv[1]]()
