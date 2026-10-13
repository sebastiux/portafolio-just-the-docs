"""Genera brazos.kicad_sym (simbolos propios) y brazo_control.kicad_sch (formato KiCad 7, migra a 10).
Estilo: cada pin con un tramo corto y una etiqueta de net (esquematico por etiquetas)."""
import os, re, sys, uuid
import design as D
from sexp import lib_symbol, pins_of

OUT = sys.argv[1] if len(sys.argv) > 1 else 'out'
SYM = '/usr/share/kicad/symbols'
U = lambda: str(uuid.uuid4())
F = '(effects (font (size 1.27 1.27)))'
FH = '(effects (font (size 1.27 1.27)) hide)'

# ---------------- simbolos propios ----------------
def pin(t, x, y, ang, name, num):
    return (f'      (pin {t} line (at {x} {y} {ang}) (length 5.08)\n'
            f'        (name "{name}" {F})\n        (number "{num}" {F}))\n')

esp_names = {1: ('5V', 'power_in'), 2: ('GND', 'power_in'), 3: ('3V3', 'power_out'),
             4: ('IO4/ADC1_4', 'bidirectional'), 5: ('IO3/ADC1_3', 'bidirectional'),
             6: ('IO2 (strap)', 'bidirectional'), 7: ('IO1/ADC1_1', 'bidirectional'),
             8: ('IO0/ADC1_0', 'bidirectional'), 9: ('IO5', 'bidirectional'), 10: ('IO6', 'bidirectional'),
             11: ('IO7', 'bidirectional'), 12: ('IO8 (strap, LED)', 'bidirectional'),
             13: ('IO9 (BOOT)', 'bidirectional'), 14: ('IO10', 'bidirectional'),
             15: ('IO20/RX', 'bidirectional'), 16: ('IO21/TX', 'bidirectional')}
esp = ('  (symbol "ESP32C3_SuperMini" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)\n'
       f'    (property "Reference" "U" (at 0 13.97 0) {F})\n'
       f'    (property "Value" "ESP32-C3 Super Mini" (at 0 -13.97 0) {F})\n'
       f'    (property "Footprint" "brazos:ESP32C3_SuperMini_Socket" (at 0 -16.51 0) {FH})\n'
       f'    (property "Datasheet" "~" (at 0 0 0) {FH})\n'
       '    (symbol "ESP32C3_SuperMini_0_1"\n'
       '      (rectangle (start -15.24 11.43) (end 15.24 -11.43) (stroke (width 0.254) (type default)) (fill (type background))))\n'
       '    (symbol "ESP32C3_SuperMini_1_1"\n')
for i in range(1, 17):
    nm, t = esp_names[i]
    y = 8.89 - ((i - 1) % 8) * 2.54
    esp += pin(t, -20.32 if i <= 8 else 20.32, round(y, 2), 0 if i <= 8 else 180, nm, i)
esp += '    )\n  )\n'

# SW_SPDT con el comun en el pin 1 (asi numera el footprint Wuerth WS-SLTV)
spdt = lib_symbol(f'{SYM}/Switch.kicad_sym', 'SW_SPDT', 'X')
spdt = spdt.replace('"SW_SPDT_', '"SW_SPDT_C1_').replace('(symbol "X:SW_SPDT"', '(symbol "SW_SPDT_C1"')
spdt = re.sub(r'\(number "(\d)"', lambda m: '(number "%s"' % {'1': '2', '2': '1', '3': '3'}[m.group(1)], spdt)
spdt = re.sub(r'\(property "Footprint" "[^"]*"', '(property "Footprint" "Button_Switch_THT:SW_Slide-03_Wuerth-WS-SLTV_10x2.5x6.4_P2.54mm"', spdt)
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'brazos.kicad_sym'), 'w').write(
    '(kicad_symbol_lib (version 20220914) (generator brazos_gen)\n' + esp + '  ' + spdt + '\n)\n')

# ---------------- bloques de libreria embebidos ----------------
LIBS = {
    'Device:R': lib_symbol(f'{SYM}/Device.kicad_sym', 'R', 'Device'),
    'Device:LED': lib_symbol(f'{SYM}/Device.kicad_sym', 'LED', 'Device'),
    'Device:D_Schottky': lib_symbol(f'{SYM}/Device.kicad_sym', 'D_Schottky', 'Device'),
    'Device:C_Polarized': lib_symbol(f'{SYM}/Device.kicad_sym', 'C_Polarized', 'Device'),
    'Device:R_Potentiometer': lib_symbol(f'{SYM}/Device.kicad_sym', 'R_Potentiometer', 'Device'),
    'Connector:Screw_Terminal_01x02': lib_symbol(f'{SYM}/Connector.kicad_sym', 'Screw_Terminal_01x02', 'Connector'),
    'Connector_Generic:Conn_01x03': lib_symbol(f'{SYM}/Connector_Generic.kicad_sym', 'Conn_01x03', 'Connector_Generic'),
    'Switch:SW_Push': lib_symbol(f'{SYM}/Switch.kicad_sym', 'SW_Push', 'Switch'),
    'power:PWR_FLAG': lib_symbol(f'{SYM}/power.kicad_sym', 'PWR_FLAG', 'power'),
    'brazos:ESP32C3_SuperMini': esp.strip().replace('(symbol "ESP32C3_SuperMini"', '(symbol "brazos:ESP32C3_SuperMini"', 1),
    'brazos:SW_SPDT_C1': spdt.replace('(symbol "SW_SPDT_C1"', '(symbol "brazos:SW_SPDT_C1"', 1),
}
LIBID = {'U1': 'brazos:ESP32C3_SuperMini', 'J1': 'Connector:Screw_Terminal_01x02', 'J2': 'Connector:Screw_Terminal_01x02',
         'D1': 'Device:D_Schottky', 'C1': 'Device:C_Polarized', 'C2': 'Device:C_Polarized',
         'SW1': 'brazos:SW_SPDT_C1', 'SW2': 'brazos:SW_SPDT_C1', 'SW3': 'Switch:SW_Push',
         'D2': 'Device:LED', 'D3': 'Device:LED'}
for r in ('J3', 'J4', 'J5', 'J6', 'J7'):
    LIBID[r] = 'Connector_Generic:Conn_01x03'
for r in ('RV1', 'RV2', 'RV3'):
    LIBID[r] = 'Device:R_Potentiometer'
for r in ('R1', 'R2', 'R3', 'R4', 'R5', 'R6'):
    LIBID[r] = 'Device:R'

# posicion en hoja A3 (mm)
POS = {
    'J1': (40, 45, 0), 'D1': (80, 45, 0), 'C2': (110, 50, 0),
    'J2': (40, 82, 0), 'C1': (80, 87, 0),
    'U1': (220, 100, 0),
    'J3': (335, 45, 0), 'J4': (335, 65, 0), 'J5': (335, 85, 0), 'J6': (335, 105, 0), 'J7': (335, 135, 0),
    'RV1': (45, 150, 0), 'RV2': (100, 150, 0), 'RV3': (155, 150, 0),
    'R1': (45, 185, 90), 'R2': (100, 185, 90), 'R3': (155, 185, 90),
    'R4': (215, 160, 90), 'D2': (268, 160, 0),
    'R5': (215, 180, 90), 'D3': (268, 180, 0), 'R6': (215, 200, 90),
    'SW1': (335, 170, 0), 'SW2': (335, 195, 0), 'SW3': (335, 220, 0),
}
G = lambda v: round(round(v / 1.27) * 1.27, 2)

pad_net = {p: n for n, ps in D.NETS.items() for p in ps}
ROOT = U()
items = []


def wire(a, b):
    items.append(f'  (wire (pts (xy {a[0]} {a[1]}) (xy {b[0]} {b[1]})) (stroke (width 0) (type default)) (uuid {U()}))')


def label(name, p, ang):
    just = {0: 'left bottom', 180: 'right bottom', 90: 'left bottom', 270: 'right bottom'}[ang]
    items.append(f'  (label "{name}" (at {p[0]} {p[1]} {ang}) (fields_autoplaced) (effects (font (size 1.27 1.27)) (justify {just})) (uuid {U()}))')


def text(s, p, size=1.5):
    s = s.replace('"', "'")
    items.append(f'  (text "{s}" (at {p[0]} {p[1]} 0) (effects (font (size {size} {size})) (justify left top)) (uuid {U()}))')


def place(ref, lib_id, value, footprint, X, Y, rot, pins_connect, extra_props=()):
    import math
    blk = LIBS[lib_id]
    pins = pins_of(blk)
    X, Y = G(X), G(Y)
    pin_uuids = []
    c, sn = round(math.cos(math.radians(rot))), round(math.sin(math.radians(rot)))
    for num, name, px, py, ang, typ in pins:
        rx, ry = px * c - py * sn, px * sn + py * c
        ax, ay = round(X + rx, 2), round(Y - ry, 2)
        out = (ang + rot + 180) % 360
        dx, dy = {0: (1, 0), 180: (-1, 0), 90: (0, -1), 270: (0, 1)}[out]
        L = 2.54 * 2
        b = (round(ax + dx * L, 2), round(ay + dy * L, 2))
        net = pins_connect.get(num)
        if net is None:
            items.append(f'  (no_connect (at {ax} {ay}) (uuid {U()}))')
        else:
            wire((ax, ay), b)
            label(net, b, {0: 0, 180: 180, 90: 90, 270: 270}[out])
        pin_uuids.append(num)
    vertical2 = lib_id in ('Device:R', 'Device:C_Polarized', 'Device:R_Potentiometer') and rot == 0
    if vertical2:
        dx_ = 5.08 if lib_id == 'Device:R_Potentiometer' else 2.54
        rp, vp, j = (round(X + dx_, 2), round(Y - 1.27, 2)), (round(X + dx_, 2), round(Y + 1.27, 2)), ' (justify left)'
    elif lib_id == 'Device:R':
        rp, vp, j = (X, round(Y - 2.54, 2)), (X, round(Y + 2.54, 2)), ''
    elif ref == 'U1':
        rp, vp, j = (X, round(Y - 13.97, 2)), (X, round(Y + 13.97, 2)), ''
    else:
        rp, vp, j = (X, round(Y - 7.62, 2)), (X, round(Y + 7.62, 2)), ''
    FJ = F[:-1] + j + ')' if j else F
    fa = 90 if rot == 90 else 0
    props = (f'    (property "Reference" "{ref}" (at {rp[0]} {rp[1]} {fa}) {FJ})\n'
             f'    (property "Value" "{value}" (at {vp[0]} {vp[1]} {fa}) {FJ})\n'
             f'    (property "Footprint" "{footprint}" (at {X} {Y} 0) {FH})\n'
             f'    (property "Datasheet" "~" (at {X} {Y} 0) {FH})\n')
    for k, v in extra_props:
        props += f'    (property "{k}" "{v}" (at {X} {Y} 0) {FH})\n'
    pins_txt = ''.join(f'    (pin "{n}" (uuid {U()}))\n' for n in sorted(set(pin_uuids)))
    items.append(f'  (symbol (lib_id "{lib_id}") (at {X} {Y} {rot}) (unit 1)\n'
                 f'    (in_bom yes) (on_board yes) (dnp no)\n    (uuid {U()})\n{props}{pins_txt}'
                 f'    (instances\n      (project "brazo_control"\n        (path "/{ROOT}" (reference "{ref}") (unit 1))))\n  )')


for ref, (lib, fp, value, *_r, desc) in D.PARTS.items():
    con = {k.split('.')[1]: n for k, n in pad_net.items() if k.split('.')[0] == ref}
    place(ref, LIBID[ref], value, f'{lib}:{fp}', *POS[ref], con, extra_props=[('Funcion', desc)])

# PWR_FLAG en las nets alimentadas por pines pasivos
for i, net in enumerate(['GND', '+5V', 'VSERVO', 'VLOG_IN']):
    X, Y = G(140 + 18 * i), G(40)
    blk = LIBS['power:PWR_FLAG']
    items.append(f'  (symbol (lib_id "power:PWR_FLAG") (at {X} {Y} 0) (unit 1)\n    (in_bom yes) (on_board yes) (dnp no)\n    (uuid {U()})\n'
                 f'    (property "Reference" "#FLG0{i + 1}" (at {X} {round(Y - 1.9, 2)} 0) {FH})\n'
                 f'    (property "Value" "PWR_FLAG" (at {X} {round(Y - 3.81, 2)} 0) {F})\n'
                 f'    (property "Footprint" "" (at {X} {Y} 0) {FH})\n    (property "Datasheet" "~" (at {X} {Y} 0) {FH})\n'
                 f'    (pin "1" (uuid {U()}))\n    (instances\n      (project "brazo_control"\n        (path "/{ROOT}" (reference "#FLG0{i + 1}") (unit 1))))\n  )')
    wire((X, Y), (X, round(Y + 5.08, 2)))
    label(net, (X, round(Y + 5.08, 2)), 270)

notes = [
    ((30, 25), 'ALIMENTACION: canal 1 de la fuente -> J1 (5 V logica, pasa por D1). Canal 2 -> J2 (5-6 V servos). GND comun en la placa.', 1.6),
    ((30, 30), 'No conectar USB y J1 al mismo tiempo sin D1 (D1 evita retroalimentar la fuente).', 1.3),
    ((175, 122), 'Orden fisico de pines del Super Mini = HIPOTESIS (ver LEEME). Verificar serigrafia del modulo.', 1.3),
    ((30, 200), 'Pots 10k: R1-R3 (3.3k) limitan el tope a ~2.5 V, rango util del ADC del C3 con atenuacion de 12 dB.', 1.3),
    ((190, 212), 'LEDs activos en bajo (anodo a 3V3): IO4 = 0 enciende D2, IO2 = 0 enciende D3. IO2 es pin de arranque -> R6 pull-up 10k.', 1.3),
    ((300, 235), 'Boton DIAG = boton BOOT del propio modulo (IO9). IO8 queda libre (sin conector en v3).', 1.3),
    ((300, 152), 'SW2 = MODO (IO20), SW1 = PINZA (IO21). Comun a GPIO con pull-up interno, otra posicion a GND.', 1.3),
    ((300, 28), 'Servos SG90: pin 1 GND (cafe), 2 V+ (rojo), 3 senal (naranja).', 1.3),
]
for p, s, sz in notes:
    text(s, p, sz)

lib_symbols = '  (lib_symbols\n' + '\n'.join('    ' + b.replace('\n', '\n  ') for b in LIBS.values()) + '\n  )'
sch = (f'(kicad_sch (version 20230121) (generator eeschema)\n\n  (uuid {ROOT})\n\n  (paper "A3")\n\n'
       '  (title_block\n    (title "Control de brazo robotico 3GDL - ESP32-C3")\n    (date "2026-10-07")\n    (rev "v3")\n'
       '    (comment 1 "Una placa por brazo. 58x48 mm, 1 cara (B.Cu), pista >= 0.8, aislamiento >= 0.6 mm")\n'
       '    (comment 2 "Modo manual (3 pots + switch) / modo app WiFi; LED de estado y DIAG")\n  )\n\n'
       f'{lib_symbols}\n\n' + '\n'.join(items) +
       '\n\n  (sheet_instances\n    (path "/" (page "1"))\n  )\n)\n')
open(os.path.join(OUT, 'brazo_control.kicad_sch'), 'w').write(sch)
print('ok', len(items), 'items')
