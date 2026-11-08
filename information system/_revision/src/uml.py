"""Tiny UML drawing helper: produces inline SVG for use-case, class and object diagrams.

Coordinates are given by hand (centre of each element). Lines are straight and are
clipped to the border of each shape, so arrows touch the shapes exactly.
"""
import html
import math

FONT = "DejaVu Sans, Arial, sans-serif"
CW = 6.4  # approx. width of one character at 11px


def tw(text, size=11):
    return max(len(l) for l in text.split("\n")) * CW * size / 11


class Shape:
    def __init__(self, kind, cx, cy, hw, hh):
        self.kind, self.cx, self.cy, self.hw, self.hh = kind, cx, cy, hw, hh

    def edge(self, tx, ty):
        """Point on the border of this shape in the direction of (tx, ty)."""
        dx, dy = tx - self.cx, ty - self.cy
        if dx == 0 and dy == 0:
            return self.cx, self.cy
        if self.kind == "ellipse":
            t = 1 / math.sqrt((dx / self.hw) ** 2 + (dy / self.hh) ** 2)
        else:
            tx_ = self.hw / abs(dx) if dx else float("inf")
            ty_ = self.hh / abs(dy) if dy else float("inf")
            t = min(tx_, ty_)
        return self.cx + dx * t, self.cy + dy * t


class Diagram:
    def __init__(self, w, h, title=None):
        self.w, self.h = w, h
        self.back, self.front, self.lines = [], [], []
        self.shapes = {}

    # ---------- elements ----------
    def boundary(self, x, y, w, h, title):
        self.back.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#fbfcff" stroke="#556" stroke-width="1.3"/>')
        self.back.append(f'<text x="{x + w / 2}" y="{y + 16}" text-anchor="middle" font-weight="bold" font-size="12">{html.escape(title)}</text>')

    def actor(self, key, x, y, label, color="#222"):
        """Stick figure; (x, y) = centre of the figure."""
        s = []
        s.append(f'<circle cx="{x}" cy="{y - 18}" r="7" fill="#fff" stroke="{color}" stroke-width="1.5"/>')
        s.append(f'<line x1="{x}" y1="{y - 11}" x2="{x}" y2="{y + 8}" stroke="{color}" stroke-width="1.5"/>')
        s.append(f'<line x1="{x - 11}" y1="{y - 4}" x2="{x + 11}" y2="{y - 4}" stroke="{color}" stroke-width="1.5"/>')
        s.append(f'<line x1="{x}" y1="{y + 8}" x2="{x - 9}" y2="{y + 22}" stroke="{color}" stroke-width="1.5"/>')
        s.append(f'<line x1="{x}" y1="{y + 8}" x2="{x + 9}" y2="{y + 22}" stroke="{color}" stroke-width="1.5"/>')
        for i, line in enumerate(label.split("\n")):
            s.append(f'<text x="{x}" y="{y + 36 + i * 13}" text-anchor="middle" font-size="11" font-weight="bold">{html.escape(line)}</text>')
        self.front += s
        top, bottom = y - 26, y + 40 + 13 * (len(label.split("\n")) - 1)
        self.shapes[key] = Shape("rect", x, (top + bottom) / 2, 18, (bottom - top) / 2)

    def uc(self, key, x, y, label, w=None, fill="#fff7d6"):
        lines = label.split("\n")
        rx = (w or tw(label) + 26) / 2
        ry = 15 + 6.5 * (len(lines) - 1)
        self.front.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="#7a5c00" stroke-width="1.2"/>')
        for i, line in enumerate(lines):
            yy = y + 4 + (i - (len(lines) - 1) / 2) * 13
            self.front.append(f'<text x="{x}" y="{yy}" text-anchor="middle" font-size="11">{html.escape(line)}</text>')
        self.shapes[key] = Shape("ellipse", x, y, rx, ry)

    def cls(self, key, x, y, name, attrs=(), ops=(), w=None, stereo=None, obj=False, fill="#eef4ff"):
        """Class box (or object box if obj=True: underlined name, attrs = values)."""
        rows_name = ([f"«{stereo}»"] if stereo else []) + [name]
        width = w or max([tw(name, 12) + 20] + [tw(a) + 16 for a in list(attrs) + list(ops)] + [80])
        h_name = 8 + 15 * len(rows_name)
        h_attr = 6 + 14 * max(len(attrs), 1 if not obj else len(attrs))
        h_ops = (6 + 14 * len(ops)) if ops or not obj else 0
        if obj and not attrs:
            h_attr = 0
        height = h_name + h_attr + h_ops
        x0, y0 = x - width / 2, y - height / 2
        s = [f'<rect x="{x0}" y="{y0}" width="{width}" height="{height}" fill="{fill}" stroke="#1f3f7a" stroke-width="1.3"/>']
        for i, r in enumerate(rows_name):
            bold = 'font-weight="bold"' if r == name else 'font-style="italic"'
            deco = ' text-decoration="underline"' if obj and r == name else ""
            s.append(f'<text x="{x}" y="{y0 + 17 + 15 * i}" text-anchor="middle" font-size="12" {bold}{deco}>{html.escape(r)}</text>')
        yy = y0 + h_name
        if h_attr:
            s.append(f'<line x1="{x0}" y1="{yy}" x2="{x0 + width}" y2="{yy}" stroke="#1f3f7a"/>')
            for i, a in enumerate(attrs):
                s.append(f'<text x="{x0 + 7}" y="{yy + 15 + 14 * i}" font-size="11" font-family="DejaVu Sans Mono, monospace">{html.escape(a)}</text>')
            yy += h_attr
        if h_ops:
            s.append(f'<line x1="{x0}" y1="{yy}" x2="{x0 + width}" y2="{yy}" stroke="#1f3f7a"/>')
            for i, o in enumerate(ops):
                s.append(f'<text x="{x0 + 7}" y="{yy + 15 + 14 * i}" font-size="11" font-family="DejaVu Sans Mono, monospace">{html.escape(o)}</text>')
        self.front += s
        self.shapes[key] = Shape("rect", x, y, width / 2, height / 2)

    def note(self, x, y, text, w=None, color="#fff4c2"):
        lines = text.split("\n")
        width = w or tw(text) + 16
        height = 10 + 14 * len(lines)
        x0, y0 = x - width / 2, y - height / 2
        self.front.append(f'<path d="M{x0},{y0} h{width - 10} l10,10 v{height - 10} h-{width} z" fill="{color}" stroke="#a08000"/>')
        for i, l in enumerate(lines):
            self.front.append(f'<text x="{x0 + 7}" y="{y0 + 17 + 14 * i}" font-size="10.5">{html.escape(l)}</text>')

    def text(self, x, y, t, size=11, color="#333", anchor="middle", bold=False, italic=False):
        extra = (' font-weight="bold"' if bold else "") + (' font-style="italic"' if italic else "")
        self.front.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{color}"{extra}>{html.escape(t)}</text>')

    # ---------- links ----------
    def _ends(self, a, b, via=None):
        A, B = self.shapes[a], self.shapes[b]
        pa = A.edge(*(via[0] if via else (B.cx, B.cy)))
        pb = B.edge(*(via[-1] if via else (A.cx, A.cy)))
        return pa, pb

    def _path(self, pa, pb, via, dash, color="#333", width=1.3):
        pts = [pa] + (via or []) + [pb]
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        da = ' stroke-dasharray="6,4"' if dash else ""
        self.lines.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{da}/>')
        return pts

    def _head(self, tip, frm, kind, color="#333"):
        (x, y), (fx, fy) = tip, frm
        ang = math.atan2(y - fy, x - fx)
        def p(l, da):
            return x - l * math.cos(ang + da), y - l * math.sin(ang + da)
        if kind == "open":
            (x1, y1), (x2, y2) = p(11, 0.42), p(11, -0.42)
            self.lines.append(f'<path d="M{x1:.1f},{y1:.1f} L{x:.1f},{y:.1f} L{x2:.1f},{y2:.1f}" fill="none" stroke="{color}" stroke-width="1.3"/>')
        elif kind == "triangle":
            (x1, y1), (x2, y2) = p(15, 0.45), p(15, -0.45)
            self.lines.append(f'<path d="M{x1:.1f},{y1:.1f} L{x:.1f},{y:.1f} L{x2:.1f},{y2:.1f} z" fill="#fff" stroke="{color}" stroke-width="1.3"/>')
        elif kind in ("diamond", "fdiamond"):
            (x1, y1), (x3, y3) = p(9, 0.5), p(9, -0.5)
            x2, y2 = x - 17 * math.cos(ang), y - 17 * math.sin(ang)
            fill = "#222" if kind == "fdiamond" else "#fff"
            self.lines.append(f'<path d="M{x:.1f},{y:.1f} L{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f} L{x3:.1f},{y3:.1f} z" fill="{fill}" stroke="{color}" stroke-width="1.3"/>')

    def _label(self, pts, text, color="#7a1fa2", italic=False, offset=-6):
        # middle of the longest segment
        best = max(range(len(pts) - 1), key=lambda i: math.dist(pts[i], pts[i + 1]))
        (x1, y1), (x2, y2) = pts[best], pts[best + 1]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        w = tw(text, 10) + 6
        self.lines.append(f'<rect x="{mx - w / 2}" y="{my + offset - 10}" width="{w}" height="13" fill="#fff" opacity="0.9"/>')
        st = ' font-style="italic"' if italic else ""
        self.lines.append(f'<text x="{mx}" y="{my + offset}" text-anchor="middle" font-size="10" fill="{color}"{st}>{html.escape(text)}</text>')

    def _mult(self, end, other, text, side=1):
        (x, y), (ox, oy) = end, other
        ang = math.atan2(oy - y, ox - x)
        px, py = x + 20 * math.cos(ang), y + 20 * math.sin(ang)
        nx, ny = -math.sin(ang) * 11 * side, math.cos(ang) * 11 * side
        self.lines.append(f'<text x="{px + nx:.1f}" y="{py + ny + 4:.1f}" text-anchor="middle" font-size="10.5" fill="#b3261e" font-weight="bold">{html.escape(text)}</text>')

    def assoc(self, a, b, label=None, ma=None, mb=None, arrow=False, via=None, side=1, kind=None, color="#333"):
        """Plain association. kind: 'agg' or 'comp' puts a diamond on a's side (a = whole)."""
        pa, pb = self._ends(a, b, via)
        pts = self._path(pa, pb, via, False, color)
        if arrow:
            self._head(pb, pts[-2], "open", color)
        if kind == "agg":
            self._head(pa, pts[1], "diamond")
        if kind == "comp":
            self._head(pa, pts[1], "fdiamond")
        if label:
            self._label(pts, label, color="#1f3f7a", italic=True)
        if ma:
            self._mult(pa, pts[1], ma, side)
        if mb:
            self._mult(pb, pts[-2], mb, side)

    def include(self, a, b, via=None):
        pa, pb = self._ends(a, b, via)
        pts = self._path(pa, pb, via, True, "#7a1fa2")
        self._head(pb, pts[-2], "open", "#7a1fa2")
        self._label(pts, "«include»")

    def extend(self, a, b, via=None, cond=None):
        pa, pb = self._ends(a, b, via)
        pts = self._path(pa, pb, via, True, "#0b7a5b")
        self._head(pb, pts[-2], "open", "#0b7a5b")
        self._label(pts, "«extend»" + (f" [{cond}]" if cond else ""), color="#0b7a5b")

    def gen(self, child, parent, via=None):
        pa, pb = self._ends(child, parent, via)
        pts = self._path(pa, pb, via, False)
        self._head(pb, pts[-2], "triangle")

    def dep(self, a, b, label=None, via=None):
        pa, pb = self._ends(a, b, via)
        pts = self._path(pa, pb, via, True)
        self._head(pb, pts[-2], "open")
        if label:
            self._label(pts, label, color="#333")

    def svg(self):
        body = "\n".join(self.back + self.lines + self.front)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="100%" '
                f'style="max-width:{self.w}px;font-family:{FONT}" class="uml">{body}</svg>')
