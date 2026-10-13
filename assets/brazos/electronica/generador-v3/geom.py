import math
from shapely.geometry import Point, Polygon, LineString
from shapely import affinity


def pad_poly(p, grow=0.0):
    """Poligono del pad en coordenadas de placa (mm). grow agrega margen."""
    w, h = p['w'], p['h']
    if p.get('npth'):
        return Point(p['x'], p['y']).buffer(p['drill'] / 2 + grow, 32)
    if p['shape'] == 'circle':
        return Point(p['x'], p['y']).buffer(w / 2 + grow, 32)
    if p['shape'] == 'oval':
        if abs(w - h) < 1e-6:
            g = Point(0, 0).buffer(w / 2 + grow, 32)
        elif w > h:
            g = LineString([(-(w - h) / 2, 0), ((w - h) / 2, 0)]).buffer(h / 2 + grow, 32)
        else:
            g = LineString([(0, -(h - w) / 2), (0, (h - w) / 2)]).buffer(w / 2 + grow, 32)
    else:
        g = Polygon([(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)])
        if grow:
            g = g.buffer(grow, 32)
    # KiCad: angulo positivo = antihorario en pantalla (y hacia abajo) -> en coords y-abajo es -rot
    g = affinity.rotate(g, -p['rot'], origin=(0, 0))
    return affinity.translate(g, p['x'], p['y'])
