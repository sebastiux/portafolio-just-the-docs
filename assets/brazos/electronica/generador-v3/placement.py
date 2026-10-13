# Colocacion v3 (mm, origen esquina superior izquierda): ref -> (x, y, rot)
# Placa de 58 x 48 mm (se fresa el contorno dentro del blank de 70 x 50).
# Una cara (cobre B.Cu), THT. La topologia de una capa depende de este acomodo (ver LEEME.md).
W, H = 58.0, 48.0
BLANK = (70.0, 50.0)            # la placa queda centrada en el blank

P = 38.78                       # fila de pines de los potenciometros
PX = (5.7, 19.1, 32.5)          # pin 1 (GND) de RV1..RV3; pots juntos
RT = P + 2.54                   # pad superior de R1..R3 (VPOT), justo bajo el pin 3
RB = P + 7.62                   # pad inferior de R1..R3 / bus 3V3
GB = P + 5.08                   # bus GND de potenciometros (pasa entre las patas de R1..R3)
LX, UY = 33.0, 2.6              # columna izquierda del modulo; la derecha esta en LX + 15.24
RX = LX + 15.24
SX = RX + 3.0                   # columna S de los conectores de servo

PLACE = {
    'U1':  (LX, UY, 0),
    'J1':  (3.8, 4.6, 0),
    'D1':  (21.5, 2.6, 180),
    'C2':  (28.0, 2.6, 270),
    'R4':  (13.5, 10.4, 0),
    'D2':  (27.0, 10.4, 180),
    'R5':  (13.5, 15.0, 0),
    'D3':  (27.0, 15.0, 180),
    'R6':  (13.5, 18.6, 0),
    'J3':  (SX + 5.08, UY, 270),
    'J4':  (SX + 5.08, UY + 2.54, 270),
    'J5':  (SX + 5.08, UY + 5.08, 270),
    'J6':  (SX + 5.08, UY + 12.7, 270),     # fila de IO10
    'C1':  (52.0, 27.3, 0),
    'J2':  (53.1, 34.43, 270),
    'SW1': (44.6, 30.0, 270),
    'SW2': (44.6, 41.2, 270),
    'RV1': (PX[0], P, 90),
    'RV2': (PX[1], P, 90),
    'RV3': (PX[2], P, 90),
    'R1':  (PX[0] + 5, RB, 90),
    'R2':  (PX[1] + 5, RB, 90),
    'R3':  (PX[2] + 5, RB, 90),
}

FIXED = [
    # 3V3: baja por el borde izquierdo y corre por el borde inferior hasta R1..R3
    ('+3V3', 0.8, [(13.5, 18.6), (11.5, 18.6), (11.5, 21.0), (1.25, 24.0), (1.25, RB), (PX[2] + 5, RB)]),
    # GND de potenciometros: bus entre las patas de R1..R3
    ('GND', 1.2, [(PX[0], P), (PX[0], GB), (42.3, GB)]),
    ('GND', 1.2, [(PX[1], P), (PX[1], GB)]),
    ('GND', 1.2, [(PX[2], P), (PX[2], GB)]),
    # GND: canal bajo el modulo -> columna de switches -> J2
    ('GND', 1.2, [(LX, UY + 2.54), (36.6, UY + 2.54), (36.6, 24.2), (42.3, 24.2), (42.3, 45.8), (53.1, 45.8), (53.1, 39.51)]),
    # VLOG pasa por arriba de J1.2
    ('VLOG_IN', 1.2, [(3.8, 4.6), (3.8, 1.75), (12.7, 1.75), (13.88, 2.6)]),
    # IO3 baja recto por el canal hasta el cursor de RV3
    ('POT_CODO', 0.8, [(LX, UY + 10.16), (PX[2] + 2.5, UY + 10.16), (PX[2] + 2.5, P)]),
    # Switches
    ('SW_PINZA', 0.8, [(RX, UY + 17.78), (RX, 30.0), (44.6, 30.0)]),
    ('SW_MODO', 0.8, [(RX, UY + 15.24), (50.2, UY + 15.24), (50.2, 41.2), (44.6, 41.2)]),
]
