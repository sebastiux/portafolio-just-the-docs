"""Fuente unica de verdad: partes, footprints, nets y colocacion.

Coordenadas en mm, origen = esquina superior izquierda de la placa.
En KiCad se desplaza todo por (OX, OY).
"""
OX, OY = 100.0, 60.0

# Reglas de fabricacion (fresadora)
TRACK_MIN = 0.8      # dado por el usuario
CLEAR = 0.6          # HIPOTESIS: aislamiento minimo de la fresadora (ver LEEME)
ROUTE_MARGIN = 0.1   # margen extra del ruteador por la rejilla
EDGE_CLEAR = 0.8     # cobre al contorno (el contorno se fresa dentro del blank de 70x50)

W_SIG = 0.8
W_PWR = 1.2
W_SRV = 1.6

FPLIB = '/usr/share/kicad/footprints'

# ref: (lib, footprint, value, x, y, rot, descripcion)
PARTS = {
    'U1':  ('brazos', 'ESP32C3_SuperMini_Socket', 'ESP32-C3 Super Mini', 0, 0, 0, 'Modulo en zocalo 2x(1x08) hembra'),
    'J1':  ('TerminalBlock', 'TerminalBlock_bornier-2_P5.08mm', 'LOGICA 5V', 0, 0, 0, 'Bornera canal 1 fuente: logica'),
    'J2':  ('TerminalBlock', 'TerminalBlock_bornier-2_P5.08mm', 'VSERVO 5-6V', 0, 0, 0, 'Bornera canal 2 fuente: servos'),
    'D1':  ('Diode_THT', 'D_DO-41_SOD81_P7.62mm_Horizontal', '1N5819', 0, 0, 0, 'Schottky: polaridad inversa y retroalimentacion USB'),
    'C1':  ('Capacitor_THT', 'CP_Radial_D8.0mm_P3.50mm', '1000uF 10V', 0, 0, 0, 'Bulk servos'),
    'C2':  ('Capacitor_THT', 'CP_Radial_D5.0mm_P2.50mm', '100uF 10V', 0, 0, 0, 'Bulk ESP32 (picos WiFi)'),
    'J3':  ('brazos', 'PinHeader_1x03_P2.54mm_Servo', 'SERVO BASE', 0, 0, 0, 'GND V+ SIG'),
    'J4':  ('brazos', 'PinHeader_1x03_P2.54mm_Servo', 'SERVO HOMBRO', 0, 0, 0, 'GND V+ SIG'),
    'J5':  ('brazos', 'PinHeader_1x03_P2.54mm_Servo', 'SERVO CODO', 0, 0, 0, 'GND V+ SIG'),
    'J6':  ('brazos', 'PinHeader_1x03_P2.54mm_Servo', 'SERVO PINZA', 0, 0, 0, 'GND V+ SIG'),
    'RV1': ('Potentiometer_THT', 'Potentiometer_Alps_RK09K_Single_Vertical', '10k', 0, 0, 0, 'Pot base'),
    'RV2': ('Potentiometer_THT', 'Potentiometer_Alps_RK09K_Single_Vertical', '10k', 0, 0, 0, 'Pot hombro'),
    'RV3': ('Potentiometer_THT', 'Potentiometer_Alps_RK09K_Single_Vertical', '10k', 0, 0, 0, 'Pot codo'),
    'R1':  ('Resistor_THT', 'R_Axial_DIN0207_L6.3mm_D2.5mm_P5.08mm_Vertical', '3.3k', 0, 0, 0, 'Limita tope de RV1 a ~2.5 V'),
    'R2':  ('Resistor_THT', 'R_Axial_DIN0207_L6.3mm_D2.5mm_P5.08mm_Vertical', '3.3k', 0, 0, 0, 'Limita tope de RV2 a ~2.5 V'),
    'R3':  ('Resistor_THT', 'R_Axial_DIN0207_L6.3mm_D2.5mm_P5.08mm_Vertical', '3.3k', 0, 0, 0, 'Limita tope de RV3 a ~2.5 V'),
    'R4':  ('Resistor_THT', 'R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal', '330', 0, 0, 0, 'LED estado'),
    'R5':  ('Resistor_THT', 'R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal', '330', 0, 0, 0, 'LED diagnostico'),
    'R6':  ('Resistor_THT', 'R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal', '10k', 0, 0, 0, 'Pull-up GPIO2 (strapping)'),
    'D2':  ('LED_THT', 'LED_D3.0mm', 'LED verde', 0, 0, 0, 'Estado (activo en bajo)'),
    'D3':  ('LED_THT', 'LED_D3.0mm', 'LED rojo', 0, 0, 0, 'Diagnostico'),
    'SW1': ('Button_Switch_THT', 'SW_Slide-03_Wuerth-WS-SLTV_10x2.5x6.4_P2.54mm', 'PINZA', 0, 0, 0, 'Abrir/cerrar pinza (manual)'),
    'SW2': ('Button_Switch_THT', 'SW_Slide-03_Wuerth-WS-SLTV_10x2.5x6.4_P2.54mm', 'MODO', 0, 0, 0, 'Manual / App WiFi'),
}

# ESP32-C3 Super Mini (HIPOTESIS de orden fisico, ver LEEME):
# pin 1-8 columna izquierda desde el USB: 5V GND 3V3 IO4 IO3 IO2 IO1 IO0
# pin 9-16 columna derecha desde el USB: IO5 IO6 IO7 IO8 IO9 IO10 IO20 IO21
ESP_PINS = {1: '5V', 2: 'GND', 3: '3V3', 4: 'GPIO4', 5: 'GPIO3', 6: 'GPIO2', 7: 'GPIO1', 8: 'GPIO0',
            9: 'GPIO5', 10: 'GPIO6', 11: 'GPIO7', 12: 'GPIO8', 13: 'GPIO9', 14: 'GPIO10', 15: 'GPIO20', 16: 'GPIO21'}

NETS = {
    'GND':        ['U1.2', 'J1.2', 'J2.2', 'C1.2', 'C2.2', 'J3.1', 'J4.1', 'J5.1', 'J6.1',
                   'RV1.1', 'RV2.1', 'RV3.1', 'SW1.2', 'SW2.2'],
    'VLOG_IN':    ['J1.1', 'D1.2'],
    '+5V':        ['D1.1', 'U1.1', 'C2.1'],
    '+3V3':       ['U1.3', 'R1.1', 'R2.1', 'R3.1', 'R4.1', 'R5.1', 'R6.1'],
    'VSERVO':     ['J2.1', 'C1.1', 'J3.2', 'J4.2', 'J5.2', 'J6.2'],
    'VPOT_BASE':  ['R1.2', 'RV1.3'],
    'VPOT_HOMBRO':['R2.2', 'RV2.3'],
    'VPOT_CODO':  ['R3.2', 'RV3.3'],
    'POT_BASE':   ['U1.7', 'RV1.2'],
    'POT_HOMBRO': ['U1.8', 'RV2.2'],
    'POT_CODO':   ['U1.5', 'RV3.2'],
    'LED_STAT':   ['U1.4', 'D2.1'],
    'LED_STAT_A': ['R4.2', 'D2.2'],
    'LED_DIAG_K': ['U1.6', 'D3.1', 'R6.2'],
    'LED_DIAG_A': ['R5.2', 'D3.2'],
    'SRV_BASE':   ['U1.9', 'J3.3'],
    'SRV_HOMBRO': ['U1.10', 'J4.3'],
    'SRV_CODO':   ['U1.11', 'J5.3'],
    'SRV_PINZA':  ['U1.14', 'J6.3'],
    'SW_PINZA':   ['U1.16', 'SW1.1'],
    'SW_MODO':    ['U1.15', 'SW2.1'],
}

NET_WIDTH = {'GND': W_PWR, '+5V': W_PWR, 'VLOG_IN': W_PWR, 'VSERVO': W_SRV}
