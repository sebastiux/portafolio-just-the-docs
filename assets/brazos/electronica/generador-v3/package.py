"""Empaqueta el proyecto final: librerias locales, tablas, Gerber/drill, vistas, BOM."""
import os, shutil, subprocess, csv
import pcbnew
import design as D

SRC = 'out'
DST = 'brazo_control_pcb'
if os.path.exists(DST):
    shutil.rmtree(DST)
os.makedirs(DST)
for f in ('brazo_control.kicad_pcb', 'brazo_control.kicad_pro', 'brazo_control.kicad_sch', 'brazos.kicad_sym'):
    shutil.copy(os.path.join(SRC, f), DST)

# footprint propio -> brazos.pretty
b = pcbnew.LoadBoard(os.path.join(DST, 'brazo_control.kicad_pcb'))
lib = os.path.join(DST, 'brazos.pretty')
os.makedirs(lib)
for fp in b.GetFootprints():
    if fp.GetFPID().GetLibNickname() == 'brazos':
        fp2 = pcbnew.FOOTPRINT(fp)
        fp2.SetPosition(pcbnew.VECTOR2I(0, 0)); fp2.SetOrientationDegrees(0)
        fp2.SetReference('U**')
        for p in fp2.Pads():
            p.SetNetCode(0)
        pcbnew.FootprintSave(lib, fp2)
open(os.path.join(DST, 'fp-lib-table'), 'w').write(
    '(fp_lib_table\n  (version 7)\n  (lib (name "brazos")(type "KiCad")(uri "${KIPRJMOD}/brazos.pretty")(options "")(descr "Footprints propios del proyecto"))\n)\n')
open(os.path.join(DST, 'sym-lib-table'), 'w').write(
    '(sym_lib_table\n  (version 7)\n  (lib (name "brazos")(type "KiCad")(uri "${KIPRJMOD}/brazos.kicad_sym")(options "")(descr "Simbolos propios del proyecto"))\n)\n')

fab = os.path.join(DST, 'fabricacion')
os.makedirs(fab)
pcb = os.path.join(DST, 'brazo_control.kicad_pcb')
run = lambda *a: subprocess.run(['kicad-cli', *a], check=True, capture_output=True, text=True)
run('pcb', 'export', 'gerbers', '-o', fab + '/', '-l', 'B.Cu,F.SilkS,B.Mask,Edge.Cuts', pcb)
run('pcb', 'export', 'drill', '-o', fab + '/', '--format', 'excellon', '--excellon-units', 'mm',
    '--generate-map', '--map-format', 'pdf', pcb)
subprocess.run(['python3', 'cnc_export.py', pcb, os.path.join(DST, 'cnc')], check=True, capture_output=True)
docs = os.path.join(DST, 'docs')
os.makedirs(docs)
for f in ('vista.png', 'cobre_espejo.png', 'esquematico.pdf', 'drc_report.txt'):
    shutil.copy(os.path.join(SRC, f), docs)

# BOM
rows = {}
for ref, (lib_, fp, value, *_r, desc) in D.PARTS.items():
    key = (value, fp)
    rows.setdefault(key, []).append(ref)
with open(os.path.join(DST, 'docs', 'bom.csv'), 'w', newline='') as fh:
    w = csv.writer(fh)
    w.writerow(['Cantidad', 'Referencias', 'Valor', 'Footprint', 'Funcion'])
    for (value, fp), refs in rows.items():
        w.writerow([len(refs), ' '.join(refs), value, fp, '; '.join(dict.fromkeys(D.PARTS[r][-1] for r in refs))])
print('ok')
