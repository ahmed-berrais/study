"""Tiny finite-automaton SVG drawer: states, straight/curved edges, self-loops."""
import math, itertools

_ids = itertools.count()

INK = "#1f2a6b"
EDGE = "#2b6cb0"
LBL = "#c2185b"


def _unit(dx, dy):
    d = math.hypot(dx, dy) or 1
    return dx / d, dy / d


class FA:
    def __init__(self, w, h, r=18):
        self.w, self.h, self.r = w, h, r
        self.st = {}
        self.parts = []
        self.mid = f"ah{next(_ids)}"

    def state(self, name, x, y, init=None, final=False, rx=None, label=None, dead=False):
        rx = rx or self.r
        self.st[name] = (x, y, rx, self.r)
        fill = "#fde8ef" if dead else "#e8f1fb"
        out = []
        out.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{self.r}" fill="{fill}" stroke="{INK}" stroke-width="1.6"/>')
        if final:
            out.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx-4}" ry="{self.r-4}" fill="none" stroke="{INK}" stroke-width="1.3"/>')
        out.append(f'<text x="{x}" y="{y+4.5}" text-anchor="middle" class="sl">{label or name}</text>')
        if init:
            ang = {"left": 180, "up": -90, "down": 90, "right": 0}[init]
            a = math.radians(ang)
            ex, ey = x + math.cos(a) * (rx + 1), y + math.sin(a) * (self.r + 1)
            sx, sy = x + math.cos(a) * (rx + 26), y + math.sin(a) * (self.r + 26)
            out.append(f'<line x1="{sx}" y1="{sy}" x2="{ex}" y2="{ey}" stroke="{INK}" stroke-width="1.6" marker-end="url(#{self.mid})"/>')
        self.parts.append("".join(out))

    def _rad(self, name, ux, uy):
        x, y, rx, ry = self.st[name]
        return rx * ry / math.sqrt((ry * ux) ** 2 + (rx * uy) ** 2)

    def edge(self, a, b, label, bend=0, lo=11, t=0.5):
        ax, ay, _, _ = self.st[a]
        bx, by, _, _ = self.st[b]
        nx, ny = _unit(-(by - ay), bx - ax)
        mx, my = (ax + bx) / 2, (ay + by) / 2
        cx, cy = mx + nx * bend, my + ny * bend
        u1 = _unit(cx - ax, cy - ay)
        u2 = _unit(cx - bx, cy - by)
        sx, sy = ax + u1[0] * self._rad(a, *u1), ay + u1[1] * self._rad(a, *u1)
        ex, ey = bx + u2[0] * (self._rad(b, *u2) + 1), by + u2[1] * (self._rad(b, *u2) + 1)
        d = f"M{sx:.1f},{sy:.1f} Q{cx:.1f},{cy:.1f} {ex:.1f},{ey:.1f}"
        # point on curve at t
        px = (1 - t) ** 2 * sx + 2 * (1 - t) * t * cx + t * t * ex
        py = (1 - t) ** 2 * sy + 2 * (1 - t) * t * cy + t * t * ey
        sgn = 1 if bend >= 0 else -1
        lx, ly = px + nx * lo * sgn, py + ny * lo * sgn
        self.parts.append(
            f'<path d="{d}" fill="none" stroke="{EDGE}" stroke-width="1.5" marker-end="url(#{self.mid})"/>'
            f'<text x="{lx:.1f}" y="{ly+4:.1f}" text-anchor="middle" class="el">{label}</text>')

    def loop(self, a, label, d="up"):
        x, y, rx, ry = self.st[a]
        ang = {"up": -90, "down": 90, "left": 180, "right": 0}[d]
        pts = []
        for da in (-28, 28):
            t = math.radians(ang + da)
            pts.append((x + math.cos(t) * rx, y + math.sin(t) * ry))
        t1, t2 = math.radians(ang - 30), math.radians(ang + 30)
        L = 34
        c1 = (x + math.cos(t1) * (rx + L), y + math.sin(t1) * (ry + L))
        c2 = (x + math.cos(t2) * (rx + L), y + math.sin(t2) * (ry + L))
        (sx, sy), (ex, ey) = pts
        a0 = math.radians(ang)
        lx, ly = x + math.cos(a0) * (rx + 33), y + math.sin(a0) * (ry + 33)
        self.parts.append(
            f'<path d="M{sx:.1f},{sy:.1f} C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {ex:.1f},{ey:.1f}" '
            f'fill="none" stroke="{EDGE}" stroke-width="1.5" marker-end="url(#{self.mid})"/>'
            f'<text x="{lx:.1f}" y="{ly+4:.1f}" text-anchor="middle" class="el">{label}</text>')

    def note(self, x, y, text, cls="nt"):
        self.parts.append(f'<text x="{x}" y="{y}" class="{cls}">{text}</text>')

    def svg(self, title=""):
        return (f'<svg viewBox="-14 -16 {self.w+28} {self.h+32}" width="100%" style="max-width:{self.w+28}px" role="img" aria-label="{title}">'
                f'<defs><marker id="{self.mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M0,0 L10,5 L0,10 z" fill="{EDGE}"/></marker></defs>'
                + "".join(self.parts) + "</svg>")
