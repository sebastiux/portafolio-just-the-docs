"""Archivos para la fresadora, vistos DESDE EL LADO DEL COBRE (espejo de la vista de componentes).
Se voltea una copia de la placa (B.Cu -> F.Cu espejado) y se exporta todo con el origen en la
esquina inferior izquierda del blank, vista desde el cobre. Cobre, taladros y contorno quedan alineados."""
import os, sys, subprocess, shutil
import pcbnew
import design as D
import placement as P

src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)
b = pcbnew.LoadBoard(src)
cx = pcbnew.FromMM(D.OX + P.W / 2)
c = pcbnew.VECTOR2I(cx, pcbnew.FromMM(D.OY + P.H / 2))
for fp in b.GetFootprints():
    fp.Flip(c, True)
for t in b.GetTracks():
    t.Flip(c, True)
for d in b.GetDrawings():
    d.Flip(c, True)
# origen: esquina inferior izquierda del BLANK (vista desde el cobre); la placa va centrada en el blank
mx, my = (P.BLANK[0] - P.W) / 2, (P.BLANK[1] - P.H) / 2
b.GetDesignSettings().SetAuxOrigin(pcbnew.VECTOR2I(pcbnew.FromMM(D.OX - mx), pcbnew.FromMM(D.OY + P.H + my)))
flipped = os.path.join(dst, '_volteada.kicad_pcb')
pcbnew.SaveBoard(flipped, b)
run = lambda *a: subprocess.run(['kicad-cli', *a], check=True, capture_output=True, text=True)
run('pcb', 'export', 'gerbers', '-o', dst + '/', '-l', 'F.Cu,Edge.Cuts', '--use-drill-file-origin',
    '--no-protel-ext', flipped)
run('pcb', 'export', 'drill', '-o', dst + '/', '--format', 'excellon', '--excellon-units', 'mm',
    '--drill-origin', 'plot', '--excellon-separate-th', flipped)
run('pcb', 'export', 'svg', '-o', os.path.join(dst, 'cobre_visto_desde_cobre.svg'), '-l', 'F.Cu,Edge.Cuts',
    '--black-and-white', '--page-size-mode', '2', '--exclude-drawing-sheet', flipped)
# nombres claros
ren = {'_volteada-F_Cu.gbr': 'cobre_espejado.gbr', '_volteada-Edge_Cuts.gbr': 'contorno_espejado.gbr',
       '_volteada-PTH.drl': 'taladros_espejado.drl', '_volteada-NPTH.drl': 'taladros_NPTH_espejado.drl'}
for f in os.listdir(dst):
    if f in ren:
        os.replace(os.path.join(dst, f), os.path.join(dst, ren[f]))
npth = os.path.join(dst, 'taladros_NPTH_espejado.drl')
if os.path.exists(npth) and '\nX' not in open(npth).read():
    os.remove(npth)   # no hay agujeros sin metalizar
for f in os.listdir(dst):
    if f.startswith('_volteada'):
        os.remove(os.path.join(dst, f))
print(sorted(os.listdir(dst)))
