"""Verificacion geometrica exacta (shapely), independiente de la rejilla del ruteador."""
import json, itertools, sys
from shapely.geometry import LineString, box
from shapely.ops import unary_union
from shapely.strtree import STRtree
from geom import pad_poly
import design as D

d = json.load(open('pads.json'))
r = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'routes.json'))
W, H = d['W'], d['H']
items = []  # (net, geom, desc)
for p in d['pads']:
    items.append((p['net'] or None, pad_poly(p), f"pad {p['ref']}.{p['num']}"))
for k, t in enumerate(r['tracks']):
    g = LineString([t['a'], t['b']]).buffer(t['w'] / 2, 16)
    items.append((t['net'], g, f"track#{k} {t['net']} w{t['w']}"))

ok = True
# 1) ancho minimo
wmin = min(t['w'] for t in r['tracks'])
print(f'ancho minimo de pista: {wmin} mm (regla {D.TRACK_MIN})')
ok &= wmin >= D.TRACK_MIN - 1e-9
# 2) clearance entre nets distintas (pads sin net cuentan como net propia)
geoms = [g for _, g, _ in items]
tree = STRtree(geoms)
worst = (9e9, None)
viol = []
for i, (n, g, desc) in enumerate(items):
    for j in tree.query(g.buffer(D.CLEAR)):
        if j <= i:
            continue
        n2, g2, d2 = items[j]
        if n is not None and n == n2:
            continue
        if desc.startswith('pad') and d2.startswith('pad') and desc.split('.')[0] == d2.split('.')[0]:
            continue  # pads del mismo footprint: geometria del fabricante
        dist = g.distance(g2)
        if dist < worst[0]:
            worst = (dist, (desc, d2))
        if dist < D.CLEAR - 1e-6:
            viol.append((round(dist, 3), desc, d2))
print(f'clearance minimo entre nets distintas: {worst[0]:.3f} mm entre {worst[1]} (regla {D.CLEAR})')
for v in viol[:20]:
    print('  VIOLACION', v)
ok &= not viol
# 3) cobre al borde
inner = box(D.EDGE_CLEAR, D.EDGE_CLEAR, W - D.EDGE_CLEAR, H - D.EDGE_CLEAR)
edge_v = [desc for n, g, desc in items if desc.startswith('track') and not inner.contains(g)]
print('pistas a menos de', D.EDGE_CLEAR, 'mm del borde:', edge_v[:5] or 'ninguna')
ok &= not edge_v
# 4) conectividad: cada net debe ser una sola isla de cobre
for net in D.NETS:
    gs = [g for n, g, _ in items if n == net]
    u = unary_union(gs)
    parts = 1 if u.geom_type == 'Polygon' else len(u.geoms)
    # los pads del boton SW3 duplicados se unen dentro del componente
    if parts != 1:
        # tolerar islas que sean solo pads gemelos del boton
        polys = [u] if u.geom_type == 'Polygon' else list(u.geoms)
        pads_sw3 = [pad_poly(p) for p in d['pads'] if p['ref'] == 'SW3' and p['net'] == net]
        lone = [pg for pg in polys if any(pg.equals(ps) or ps.contains(pg) or pg.within(ps.buffer(0.01)) for ps in pads_sw3)]
        if parts - len(lone) == 1:
            print(f'  {net}: {parts} islas, {len(lone)} son pads gemelos de SW3 (unidos dentro del boton) -> OK')
            continue
        print(f'  NET PARTIDA {net}: {parts} islas')
        ok = False
print('nets verificadas:', len(D.NETS))
print('RESULTADO:', 'OK' if ok else 'CON ERRORES')
