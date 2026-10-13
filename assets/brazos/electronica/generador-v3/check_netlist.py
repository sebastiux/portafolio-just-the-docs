"""Compara 3 fuentes: design.NETS, netlist exportada del esquematico por KiCad, y pads del .kicad_pcb."""
import re, sys
import pcbnew
import design as D

net_txt = open(sys.argv[1]).read()
sch = {}
for m in re.finditer(r'\(net \(code "\d+"\) \(name "([^"]*)"\)([\s\S]*?)\)\s*(?=\(net |\)\s*\)\s*$)', net_txt):
    name = m.group(1).lstrip('/')
    nodes = re.findall(r'\(node \(ref "([^"]+)"\) \(pin "([^"]+)"\)', m.group(2))
    nodes = {f'{r}.{p}' for r, p in nodes if not r.startswith('#')}
    if name.startswith('unconnected-') or name.startswith('Net-('):
        if len(nodes) <= 1:
            continue
    if nodes:
        sch[name] = nodes

b = pcbnew.LoadBoard(sys.argv[2])
pcb = {}
for f in b.GetFootprints():
    for p in f.Pads():
        n = p.GetNetname()
        if n:
            pcb.setdefault(n, set()).add(f'{f.GetReference()}.{p.GetNumber()}')

ref = {n: set(v) for n, v in D.NETS.items()}
ok = True
for name, src in (('esquematico', sch), ('pcb', pcb)):
    if src != ref:
        ok = False
        for n in sorted(set(src) | set(ref)):
            if src.get(n) != ref.get(n):
                print(f'  [{name}] {n}: tiene {sorted(src.get(n, []))} esperado {sorted(ref.get(n, []))}')
print(f'nets: diseno={len(ref)} esquematico={len(sch)} pcb={len(pcb)}')
print('COINCIDEN' if ok else 'DIFERENCIAS')
