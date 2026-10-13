"""Construye la placa con la API pcbnew (KiCad 7) a partir de design.py + placement.py.
Exporta pads.json (coordenadas relativas a la placa, mm) para el ruteador."""
import json, math, sys
import pcbnew
import design as D
import placement as P

MM = pcbnew.FromMM


def v(x, y):
    return pcbnew.VECTOR2I(MM(x + D.OX), MM(y + D.OY))


def esp_footprint(board):
    """ESP32-C3 Super Mini sobre dos tiras hembra 1x08, filas a 15.24 mm (HIPOTESIS: medir)."""
    fp = pcbnew.FOOTPRINT(board)
    fp.SetFPID(pcbnew.LIB_ID('brazos', 'ESP32C3_SuperMini_Socket'))
    for i in range(16):
        pad = pcbnew.PAD(fp)
        pad.SetNumber(str(i + 1))
        pad.SetAttribute(pcbnew.PAD_ATTRIB_PTH)
        pad.SetLayerSet(pad.PTHMask())
        pad.SetShape(pcbnew.PAD_SHAPE_RECT if i == 0 else pcbnew.PAD_SHAPE_CIRCLE)
        pad.SetSize(pcbnew.VECTOR2I(MM(1.8), MM(1.8)))
        pad.SetDrillSize(pcbnew.VECTOR2I(MM(1.0), MM(1.0)))
        x = 0 if i < 8 else 15.24
        y = (i % 8) * 2.54
        pad.SetPosition(pcbnew.VECTOR2I(MM(x), MM(y)))
        pad.SetPos0(pcbnew.VECTOR2I(MM(x), MM(y)))
        fp.Add(pad)

    def rect(layer, x0, y0, x1, y1, w):
        for (a, b, c, d) in [(x0, y0, x1, y0), (x1, y0, x1, y1), (x1, y1, x0, y1), (x0, y1, x0, y0)]:
            s = pcbnew.FP_SHAPE(fp)
            s.SetShape(pcbnew.SHAPE_T_SEGMENT)
            s.SetLayer(layer)
            s.SetWidth(MM(w))
            s.SetStart0(pcbnew.VECTOR2I(MM(a), MM(b)))
            s.SetEnd0(pcbnew.VECTOR2I(MM(c), MM(d)))
            fp.Add(s)
    cx = 7.62
    # Modulo 18 x 22.5 mm, extremo USB arriba
    rect(pcbnew.F_SilkS, cx - 9, -2.36 - 0.15, cx + 9, 17.78 + 2.36 + 0.15, 0.12)
    rect(pcbnew.F_CrtYd, cx - 9.3, -2.36 - 1.5, cx + 9.3, 17.78 + 2.36 + 0.15, 0.05)
    # marca del conector USB
    for txt, (x, y) in {'USB': (cx, 1.5)}.items():
        t = pcbnew.FP_TEXT(fp)
        t.SetText(txt); t.SetLayer(pcbnew.F_SilkS)
        t.SetPos0(pcbnew.VECTOR2I(MM(x), MM(y)))
        t.SetTextSize(pcbnew.VECTOR2I(MM(1), MM(1))); t.SetTextThickness(MM(0.15))
        fp.Add(t)
    labels = ['5V', 'G', '3V3', 'IO4', 'IO3', 'IO2', 'IO1', 'IO0',
              'IO5', 'IO6', 'IO7', 'IO8', 'IO9', 'IO10', 'IO20', 'IO21']
    for i, lab in enumerate(labels):
        t = pcbnew.FP_TEXT(fp)
        t.SetText(lab); t.SetLayer(pcbnew.F_SilkS)
        x = 2.3 if i < 8 else 15.24 - 2.3
        t.SetPos0(pcbnew.VECTOR2I(MM(x), MM((i % 8) * 2.54)))
        t.SetTextSize(pcbnew.VECTOR2I(MM(0.8), MM(0.8))); t.SetTextThickness(MM(0.12))
        t.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_LEFT if i < 8 else pcbnew.GR_TEXT_H_ALIGN_RIGHT)
        fp.Add(t)
    fp.Reference().SetPos0(pcbnew.VECTOR2I(MM(cx), MM(11.5)))
    fp.Value().SetPos0(pcbnew.VECTOR2I(MM(cx), MM(14.0)))
    fp.Value().SetLayer(pcbnew.F_Fab)
    return fp


def servo_footprint(board):
    """Header 1x03 2.54 mm con courtyard de 2.54 mm de ancho: permite apilar 4 conectores de servo a paso 2.54."""
    fp = pcbnew.FootprintLoad(f'{D.FPLIB}/Connector_PinHeader_2.54mm.pretty', 'PinHeader_1x03_P2.54mm_Vertical')
    for g in list(fp.GraphicalItems()):
        if g.GetLayer() in (pcbnew.F_CrtYd, pcbnew.F_SilkS):
            fp.Remove(g)
    def seg(layer, a, b, w):
        s = pcbnew.FP_SHAPE(fp); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetLayer(layer); s.SetWidth(MM(w))
        s.SetStart0(pcbnew.VECTOR2I(MM(a[0]), MM(a[1]))); s.SetEnd0(pcbnew.VECTOR2I(MM(b[0]), MM(b[1]))); fp.Add(s)
    x0, x1, y0, y1 = -1.22, 1.22, -1.27, 6.35
    for a, b in [((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))]:
        seg(pcbnew.F_CrtYd, a, b, 0.05)
    seg(pcbnew.F_SilkS, (-1.6, -1.0), (-1.6, 1.0), 0.15)   # marca de pin 1 (GND)
    fp.SetFPID(pcbnew.LIB_ID('brazos', 'PinHeader_1x03_P2.54mm_Servo'))
    return fp


def button_footprint(board):
    """SW_PUSH_6mm con las dos patas derechas sin numero (mecanicas): el boton las une por dentro
    con las izquierdas, asi que solo se rutean las patas izquierdas."""
    fp = pcbnew.FootprintLoad(f'{D.FPLIB}/Button_Switch_THT.pretty', 'SW_PUSH_6mm')
    for p in fp.Pads():
        if p.GetPos0().x > MM(3):
            p.SetNumber('')
    fp.SetFPID(pcbnew.LIB_ID('brazos', 'SW_PUSH_6mm_2pin'))
    return fp


def build(save_path=None, board=None):
    board = board or pcbnew.BOARD()
    nets = {}
    for name in D.NETS:
        ni = pcbnew.NETINFO_ITEM(board, name)
        board.Add(ni)
        nets[name] = ni
    pad_net = {}
    for n, pins in D.NETS.items():
        for p in pins:
            assert p not in pad_net, p
            pad_net[p] = n

    for ref, (lib, fpname, value, *_rest) in D.PARTS.items():
        if lib == 'brazos' and fpname == 'SW_PUSH_6mm_2pin':
            fp = button_footprint(board)
        elif lib == 'brazos' and fpname == 'PinHeader_1x03_P2.54mm_Servo':
            fp = servo_footprint(board)
        elif lib == 'brazos':
            fp = esp_footprint(board)
        else:
            fp = pcbnew.FootprintLoad(f'{D.FPLIB}/{lib}.pretty', fpname)
            fp.SetFPID(pcbnew.LIB_ID(lib, fpname))
        fp.SetReference(ref)
        fp.SetValue(value)
        board.Add(fp)
        x, y, rot = P.PLACE[ref]
        fp.SetPosition(v(x, y))
        fp.SetOrientationDegrees(rot)
        for pad in fp.Pads():
            key = f'{ref}.{pad.GetNumber()}'
            if key in pad_net:
                pad.SetNet(nets[pad_net[key]])
    # verificar que todos los pines de la netlist existen
    have = {f'{f.GetReference()}.{p.GetNumber()}' for f in board.GetFootprints() for p in f.Pads()}
    missing = set(pad_net) - have
    assert not missing, missing
    if save_path:
        board.Save(save_path)
    return board


def export_pads(board, path):
    out = []
    for f in board.GetFootprints():
        for p in f.Pads():
            pos = p.GetPosition()
            sz = p.GetSize()
            d = p.GetDrillSize()
            out.append(dict(ref=f.GetReference(), num=p.GetNumber(), net=p.GetNetname(),
                            x=pos.x / 1e6 - D.OX, y=pos.y / 1e6 - D.OY,
                            w=sz.x / 1e6, h=sz.y / 1e6, rot=p.GetOrientationDegrees(),
                            shape={pcbnew.PAD_SHAPE_CIRCLE: 'circle', pcbnew.PAD_SHAPE_RECT: 'rect',
                                   pcbnew.PAD_SHAPE_OVAL: 'oval', pcbnew.PAD_SHAPE_ROUNDRECT: 'rect'}.get(p.GetShape(), 'rect'),
                            drill=max(d.x, d.y) / 1e6,
                            npth=p.GetAttribute() == pcbnew.PAD_ATTRIB_NPTH))
    # courtyards (bbox) para chequear traslapes
    cy = {}
    for f in board.GetFootprints():
        xs, ys = [], []
        for g in f.GraphicalItems():
            if g.GetLayer() == pcbnew.F_CrtYd:
                b = g.GetBoundingBox()
                xs += [b.GetX(), b.GetRight()]; ys += [b.GetY(), b.GetBottom()]
        cy[f.GetReference()] = [min(xs) / 1e6 - D.OX, min(ys) / 1e6 - D.OY, max(xs) / 1e6 - D.OX, max(ys) / 1e6 - D.OY]
    json.dump(dict(pads=out, courtyard=cy, W=P.W, H=P.H), open(path, 'w'), indent=1)


if __name__ == '__main__':
    b = build()
    export_pads(b, 'pads.json')
    print('ok')
