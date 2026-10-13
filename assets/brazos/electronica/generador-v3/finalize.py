"""Arma el .kicad_pcb final: footprints + pistas ruteadas (B.Cu) + contorno + serigrafia + reglas.
Luego corre el DRC de KiCad y guarda el reporte."""
import json, os, sys, math
import pcbnew
import design as D
import placement as P
import build

MM = pcbnew.FromMM
OUT = sys.argv[1] if len(sys.argv) > 1 else 'out'
NAME = 'brazo_control'
LAYER = pcbnew.B_Cu   # una sola cara: cobre abajo, componentes THT arriba

os.makedirs(OUT, exist_ok=True)
pcb_path = os.path.join(OUT, NAME + '.kicad_pcb')
for ext in ('.kicad_pcb', '.kicad_pro', '.kicad_prl'):
    if os.path.exists(os.path.join(OUT, NAME + ext)):
        os.remove(os.path.join(OUT, NAME + ext))
board = pcbnew.NewBoard(pcb_path)
build.build(board=board)
nets = {n.GetNetname(): n for n in board.GetNetsByName().values()}


def v(x, y):
    return pcbnew.VECTOR2I(MM(x + D.OX), MM(y + D.OY))


# ---------------- pistas ----------------
routes = json.load(open('routes.json'))
assert not routes['fails'], routes['fails']
for t in routes['tracks']:
    tr = pcbnew.PCB_TRACK(board)
    tr.SetStart(v(*t['a'])); tr.SetEnd(v(*t['b']))
    tr.SetWidth(MM(t['w'])); tr.SetLayer(LAYER)
    tr.SetNet(nets[t['net']])
    board.Add(tr)

# ---------------- contorno con esquinas redondeadas ----------------
Wb, Hb, R = P.W, P.H, 2.0


def seg(a, b, layer=pcbnew.Edge_Cuts, w=0.1):
    s = pcbnew.PCB_SHAPE(board); s.SetShape(pcbnew.SHAPE_T_SEGMENT)
    s.SetStart(v(*a)); s.SetEnd(v(*b)); s.SetLayer(layer); s.SetWidth(MM(w)); board.Add(s)


def arc(c, start_ang):
    s = pcbnew.PCB_SHAPE(board); s.SetShape(pcbnew.SHAPE_T_ARC)
    a0 = math.radians(start_ang); am = math.radians(start_ang + 45); a1 = math.radians(start_ang + 90)
    p = lambda a: v(c[0] + R * math.cos(a), c[1] + R * math.sin(a))
    s.SetArcGeometry(p(a0), p(am), p(a1)); s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(MM(0.1)); board.Add(s)


seg((0, 0), (Wb, 0)); seg((Wb, 0), (Wb, Hb)); seg((Wb, Hb), (0, Hb)); seg((0, Hb), (0, 0))  # contorno de 58x48 (se fresa dentro del blank de 70x50)

# ---------------- serigrafia ----------------
def text(s, x, y, size=1.0, rot=0, just='c', layer=pcbnew.F_SilkS):
    t = pcbnew.PCB_TEXT(board)
    t.SetText(s); t.SetLayer(layer)
    t.SetPosition(v(x, y)); t.SetTextSize(pcbnew.VECTOR2I(MM(size), MM(size)))
    t.SetTextThickness(MM(max(0.15, size * 0.15)))
    if rot:
        t.SetTextAngleDegrees(rot)
    t.SetHorizJustify({'c': pcbnew.GR_TEXT_H_ALIGN_CENTER, 'l': pcbnew.GR_TEXT_H_ALIGN_LEFT,
                       'r': pcbnew.GR_TEXT_H_ALIGN_RIGHT}[just])
    board.Add(t)


text('5V', 3.8, 9.7, 0.9); text('GND', 8.88, 9.7, 0.9)
text('S V G', 53.78, 11.5, 0.8)
for name, x in (('BASE', 12.4), ('HOMBRO', 25.8), ('CODO', 39.2)):
    text(name, x, 24.8, 0.9)
text('PINZA', 46.9, 30.0, 0.8, rot=90); text('MODO', 46.9, 41.2, 0.8, rot=90)
text('EST', 30.0, 12.4, 0.8); text('DIAG', 30.0, 17.0, 0.8)
text('BRAZO 3GDL v3', 6.5, 18.0, 1.0, rot=90)

REFPOS = {'J1': (6.3, 11.3), 'J2': (53.1, 43.4), 'C2': (24.0, 6.6), 'D2': (21.5, 12.6), 'R6': (17.3, 20.8)}
HIDE = {'RV1', 'RV2', 'RV3', 'J3', 'J4', 'J5', 'J6', 'SW1', 'SW2'}   # ya tienen etiqueta de funcion
for fp in board.GetFootprints():
    r = fp.GetReference()
    if r in HIDE:
        fp.Reference().SetVisible(False)
    if r in REFPOS:
        fp.Reference().SetPosition(v(*REFPOS[r]))
        fp.Reference().SetTextAngleDegrees(0)

# ---------------- reglas ----------------
ds = board.GetDesignSettings()
nc = ds.m_NetSettings.m_DefaultNetClass
nc.SetClearance(MM(D.CLEAR)); nc.SetTrackWidth(MM(D.W_SIG))
ds.m_TrackMinWidth = MM(D.TRACK_MIN)
ds.m_MinClearance = MM(D.CLEAR)
ds.m_CopperEdgeClearance = MM(0.5)
ds.m_HoleClearance = MM(0.25)
ds.SetCopperLayerCount(2)

pcbnew.SaveBoard(pcb_path, board)
print('guardado', pcb_path)

# ---------------- DRC ----------------
b2 = pcbnew.LoadBoard(pcb_path)
rep = os.path.join(OUT, 'drc_report.txt')
ok = pcbnew.WriteDRCReport(b2, rep, pcbnew.EDA_UNITS_MILLIMETRES, True)
print('DRC escrito:', ok)
