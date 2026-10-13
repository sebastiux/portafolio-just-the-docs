"""Ruteador de laberinto de una capa (F.Cu) sobre rejilla fina.

- Cada trabajo = (net, ancho, lista de pads o None = todos los pads de la net).
- Crecimiento de arbol: conecta el pad mas cercano al arbol ya ruteado de la net.
- Obstaculos: cobre de otras nets inflado (clearance + ancho/2), borde de placa.
- Simplificacion de trayectoria por linea de vista dentro del espacio libre.
"""
import json, math, sys, itertools, random
import numpy as np
from scipy import ndimage
from skimage.graph import MCP_Geometric
from shapely.geometry import LineString, Point
from geom import pad_poly
import design as D

RES = 0.1


class Router:
    def __init__(self, pads_json, clear=D.CLEAR, edge=D.EDGE_CLEAR, holes=()):
        d = json.load(open(pads_json))
        self.W, self.H = d['W'], d['H']
        self.pads = d['pads']
        self.clear, self.edge = clear, edge
        self.nx = int(round(self.W / RES)) + 1
        self.ny = int(round(self.H / RES)) + 1
        xs = np.arange(self.nx) * RES
        ys = np.arange(self.ny) * RES
        self.X, self.Y = np.meshgrid(xs, ys)
        self.nets = sorted({p['net'] for p in self.pads if p['net']})
        self.nid = {n: i for i, n in enumerate(self.nets)}
        # owner: -1 libre, -2 cobre sin net (MP, agujeros), >=0 id de net
        self.owner = np.full((self.ny, self.nx), -1, np.int32)
        self.pad_cells = []
        for p in self.pads:
            g = pad_poly(p)
            m = self._raster_poly(g)
            self.owner[m] = self.nid[p['net']] if p['net'] else -2
            self.pad_cells.append(m)
        # distancia al borde (mm)
        dx = np.minimum(self.X, self.W - self.X)
        dy = np.minimum(self.Y, self.H - self.Y)
        self.edge_dist = np.minimum(dx, dy)
        self.tracks = []          # dict(net, w, a, b)
        self.center = {n: np.zeros((self.ny, self.nx), bool) for n in self.nets}  # celdas del arbol

    # ---------- rasterizacion ----------
    def _bbox_slice(self, x0, y0, x1, y1):
        i0 = max(0, int(math.floor(y0 / RES)) - 1); i1 = min(self.ny, int(math.ceil(y1 / RES)) + 2)
        j0 = max(0, int(math.floor(x0 / RES)) - 1); j1 = min(self.nx, int(math.ceil(x1 / RES)) + 2)
        return slice(i0, i1), slice(j0, j1)

    def _raster_poly(self, g):
        from matplotlib.path import Path
        m = np.zeros((self.ny, self.nx), bool)
        x0, y0, x1, y1 = g.bounds
        si, sj = self._bbox_slice(x0, y0, x1, y1)
        pts = np.c_[self.X[si, sj].ravel(), self.Y[si, sj].ravel()]
        inside = Path(np.asarray(g.exterior.coords)).contains_points(pts, radius=1e-9)
        m[si, sj] = inside.reshape(self.X[si, sj].shape)
        return m

    def _seg_dist(self, a, b, si, sj):
        X, Y = self.X[si, sj], self.Y[si, sj]
        ax, ay = a; bx, by = b
        vx, vy = bx - ax, by - ay
        L2 = vx * vx + vy * vy
        if L2 == 0:
            return np.hypot(X - ax, Y - ay)
        t = np.clip(((X - ax) * vx + (Y - ay) * vy) / L2, 0, 1)
        return np.hypot(X - (ax + t * vx), Y - (ay + t * vy))

    def _raster_seg(self, a, b, r):
        si, sj = self._bbox_slice(min(a[0], b[0]) - r, min(a[1], b[1]) - r, max(a[0], b[0]) + r, max(a[1], b[1]) + r)
        return si, sj, self._seg_dist(a, b, si, sj) <= r

    # ---------- ruteo ----------
    def free_mask(self, net, w):
        other = (self.owner != -1) & (self.owner != self.nid[net])
        dist = ndimage.distance_transform_edt(~other) * RES
        thr = self.clear + D.ROUTE_MARGIN + w / 2
        free = (dist > thr + 1e-6) & (self.edge_dist >= self.edge + w / 2)
        return free, dist, thr

    def route_job(self, net, w, groups):
        """groups: lista de listas de indices de pad (un grupo = pads unidos internamente).
        Termina cuando todos los grupos quedan en una sola isla de cobre de la net."""
        free, dist, thr = self.free_mask(net, w)
        cost = np.where(free, 1.0, np.inf)
        near = free & (dist < thr + 0.5)
        cost[near] += 1.5
        gcells = [np.logical_or.reduce([self.pad_cells[i] for i in g]) for g in groups]
        tree = self.center[net].copy()
        S8 = np.ones((3, 3), bool)
        for _ in range(4 * len(groups) + 10):
            lab, n = ndimage.label(tree, structure=S8)
            glab = []
            for k in range(len(groups)):
                ls = set(np.unique(lab[gcells[k]])) - {0}
                glab.append(ls)
            in_tree = [k for k in range(len(groups)) if glab[k]]
            todo = [k for k in range(len(groups)) if not glab[k]]
            comps = set().union(*glab) if glab else set()
            if not todo and len(comps) <= 1:
                break
            if not in_tree:
                tree |= gcells[todo[0]]
                continue
            main = min(glab[in_tree[0]])
            # si un grupo toca varias islas, se fusionan via el pad
            starts = np.argwhere((lab == main) & free)
            ends_map = {}
            for k in todo:
                for i in groups[k]:
                    for c in np.argwhere(self.pad_cells[i] & free):
                        ends_map[tuple(c)] = ('pad', k, i)
            for L in comps - {main}:
                for c in np.argwhere((lab == L) & free):
                    ends_map[tuple(c)] = ('isla', L, None)
            if len(starts) == 0 or not ends_map:
                return False, todo or [in_tree[-1]]
            mcp = MCP_Geometric(cost, fully_connected=True)
            cum, _ = mcp.find_costs(starts, list(ends_map.keys()), find_all_ends=False)
            ends = np.array(list(ends_map.keys()))
            cvals = cum[ends[:, 0], ends[:, 1]]
            j = int(np.argmin(cvals))
            if not np.isfinite(cvals[j]):
                return False, todo or [in_tree[-1]]
            end = tuple(ends[j])
            path = np.array(mcp.traceback(end))
            kind, kk, pi = ends_map[end]
            pts = self._simplify(path, free)
            if kind == 'pad':
                tp = self.pads[pi]
                pts.append((tp['x'], tp['y']))
            s_cell = tuple(path[0])
            for i, p in enumerate(self.pads):
                if p['net'] == net and self.pad_cells[i][s_cell]:
                    pts.insert(0, (p['x'], p['y']))
                    break
            pts = self._dedupe(pts)
            for a, b in zip(pts[:-1], pts[1:]):
                self.tracks.append(dict(net=net, w=w, a=a, b=b))
                si, sj, m = self._raster_seg(a, b, w / 2)
                sub = self.owner[si, sj]
                sub[m & (sub == -1)] = self.nid[net]
                si, sj, mc = self._raster_seg(a, b, RES * 0.75)
                tree[si, sj] |= mc
                self.center[net][si, sj] |= mc
            if kind == 'pad':
                tree |= gcells[kk]
        else:
            return False, [0]
        for k in range(len(groups)):
            self.center[net] |= gcells[k]
        return True, []

    def add_fixed(self, net, w, pts):
        for a, b in zip(pts[:-1], pts[1:]):
            self.tracks.append(dict(net=net, w=w, a=a, b=b, fixed=True))
            si, sj, m = self._raster_seg(a, b, w / 2)
            sub = self.owner[si, sj]
            sub[m & (sub == -1)] = self.nid[net]
            si, sj, mc = self._raster_seg(a, b, RES * 0.75)
            self.center[net][si, sj] |= mc
        # pads de la net tocados por la pista fija pasan al arbol
        for i, p in enumerate(self.pads):
            if p['net'] == net and (self.pad_cells[i] & self.center[net]).any():
                self.center[net] |= self.pad_cells[i]

    def _dedupe(self, pts):
        out = [pts[0]]
        for p in pts[1:]:
            if math.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) > 1e-6:
                out.append(p)
        return out

    def _los(self, a, b, free):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        n = max(2, int(L / (RES * 0.4)) + 1)
        xs = np.linspace(a[0], b[0], n); ys = np.linspace(a[1], b[1], n)
        # muestreo en las 4 celdas vecinas para ser conservador
        for fx in (np.floor, np.ceil):
            for fy in (np.floor, np.ceil):
                j = fx(xs / RES).astype(int); i = fy(ys / RES).astype(int)
                j = np.clip(j, 0, self.nx - 1); i = np.clip(i, 0, self.ny - 1)
                if not free[i, j].all():
                    return False
        return True

    def _simplify(self, path, free):
        P = [(c[1] * RES, c[0] * RES) for c in path]
        out = [P[0]]
        i = 0
        while i < len(P) - 1:
            j = len(P) - 1
            # busqueda del punto mas lejano con linea de vista (de lejos a cerca, con saltos)
            while j > i + 1 and not self._los(P[i], P[j], free):
                j -= max(1, (j - i) // 8) if j - i > 16 else 1
            out.append(P[j])
            i = j
        return out


def jobs_default():
    S, P, V = D.W_SIG, D.W_PWR, D.W_SRV
    return [
        ('VSERVO', V, None),
        ('GND', V, ['J3.1', 'J4.1', 'J5.1', 'J6.1', 'C1.2', 'J2.2']),
        ('VLOG_IN', P, None),
        ('+5V', P, None),
        ('GND', P, ['J1.2', 'C2.2', 'U1.2']),
        ('SRV_BASE', S, None),
        ('SRV_HOMBRO', S, None),
        ('SRV_CODO', S, None),
        ('SRV_PINZA', S, None),
        ('SW_PINZA', S, None),
        ('SW_MODO', S, None),
        ('VPOT_BASE', S, None),
        ('VPOT_HOMBRO', S, None),
        ('VPOT_CODO', S, None),
        ('POT_CODO', S, None),
        ('GND', S, ['SW1.2', 'SW2.2', 'J2.2']),
        ('+3V3', S, ['U1.3', 'R4.1', 'R5.1', 'R6.1']),
        ('LED_STAT', S, None),
        ('LED_STAT_A', S, None),
        ('LED_DIAG_K', S, None),
        ('LED_DIAG_A', S, None),
        ('POT_BASE', S, None),
        ('POT_HOMBRO', S, None),
        ('+3V3', S, None),
        ('GND', P, None),
    ]


def run(order, pads_json='pads.json', verbose=False):
    R = Router(pads_json)
    key = {f"{p['ref']}.{p['num']}": i for i, p in enumerate(R.pads)}
    # pads repetidos (boton): todos los indices con ese ref.num
    idx_of = {}
    for i, p in enumerate(R.pads):
        idx_of.setdefault(f"{p['ref']}.{p['num']}", []).append(i)
    import placement as PL
    for net, w, pts in PL.FIXED:
        R.add_fixed(net, w, pts)
    fails = []
    for net, w, plist in order:
        if plist is None:
            keys = sorted({f"{p['ref']}.{p['num']}" for p in R.pads if p['net'] == net})
        else:
            keys = plist
        groups = []
        for k in keys:
            # GND: cada pad del boton se conecta por cobre propio (no depender del puente interno)
            if False:
                groups += [[i] for i in idx_of[k]]
            else:
                groups.append(idx_of[k])
        ok, left = R.route_job(net, w, groups)
        if verbose:
            print(f'{net:12s} w={w} {"OK" if ok else "FALLA " + str([R.pads[groups[k][0]]["ref"] + "." + R.pads[groups[k][0]]["num"] for k in left])}', flush=True)
        if not ok:
            fails.append((net, [R.pads[groups[k][0]]["ref"] + "." + R.pads[groups[k][0]]["num"] for k in left]))
    return R, fails


if __name__ == '__main__':
    R, fails = run(jobs_default(), verbose=True)
    json.dump(dict(tracks=R.tracks, fails=fails), open('routes.json', 'w'), indent=0)
    print('fallas:', fails)
