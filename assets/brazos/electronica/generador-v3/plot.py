import json, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from geom import pad_poly

def plot(pads_json='pads.json', routes_json=None, out='plot.png'):
    d = json.load(open(pads_json))
    fig, ax = plt.subplots(figsize=(14, 11))
    ax.add_patch(Rectangle((0, 0), d['W'], d['H'], fill=False, ec='k', lw=1.5))
    for ref, (x0, y0, x1, y1) in d['courtyard'].items():
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, ec='#bbb', lw=0.6, ls='--'))
        ax.text(x0 + 0.3, y0 + 1.2, ref, fontsize=8, color='#555')
    nets = sorted({p['net'] for p in d['pads'] if p['net']})
    cmap = plt.get_cmap('tab20')
    col = {n: cmap(i % 20) for i, n in enumerate(nets)}
    if routes_json:
        r = json.load(open(routes_json))
        for t in r['tracks']:
            (x0, y0), (x1, y1) = t['a'], t['b']
            ax.plot([x0, x1], [y0, y1], color=col.get(t['net'], 'k'), lw=t['w'] * 72 / 25.4 * 11 / d['H'] * 0.9 * 7, solid_capstyle='round', alpha=0.8)
    for p in d['pads']:
        g = pad_poly(p)
        xs, ys = g.exterior.xy
        ax.fill(xs, ys, color=col.get(p['net'], '#999'), alpha=0.9, ec='k', lw=0.3)
        if p['net']:
            ax.text(p['x'], p['y'], p['net'][:7], fontsize=4.5, ha='center', va='center')
    ax.set_xlim(-2, d['W'] + 2); ax.set_ylim(d['H'] + 2, -2); ax.set_aspect('equal')
    ax.grid(True, lw=0.2)
    fig.tight_layout(); fig.savefig(out, dpi=110)

if __name__ == '__main__':
    plot(routes_json=sys.argv[1] if len(sys.argv) > 1 else None, out=sys.argv[2] if len(sys.argv) > 2 else 'plot.png')
