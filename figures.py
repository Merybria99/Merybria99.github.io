#!/usr/bin/env python3
"""Static SVG for the two new research figures.

Both are schematics, not measured data, and both are labelled as such on the
page. The protein is drawn from real scFv architecture: two immunoglobulin
variable domains (VH, VL), each a beta-sandwich of two sheets, joined by a
flexible peptide linker, with three CDR loops per domain meeting at one end to
form the combining site.
"""

import json, math

# ----------------------------------------------------------------- 3D helpers
def rot(p, ry, rx):
    x, y, z = p
    cy, sy = math.cos(ry), math.sin(ry)
    x, z = x * cy + z * sy, -x * sy + z * cy
    cx, sx = math.cos(rx), math.sin(rx)
    y, z = y * cx - z * sx, y * sx + z * cx
    return (x, y, z)


def project(p):
    """Orthographic, with SVG's y pointing down."""
    return (p[0], -p[1])


# ------------------------------------------------------- immunoglobulin domain
SHEET_A = [-0.90, -0.30, 0.30, 0.90]           # 4 strands, front sheet
SHEET_B = [-1.05, -0.52, 0.00, 0.52, 1.05]     # 5 strands, back sheet
Y_TOP, Y_BOT, Z_A, Z_B = 1.50, -1.50, -0.72, 0.72


def strand(x, z, twist):
    """A beta strand as a gently twisted line."""
    pts = []
    for i in range(7):
        t = i / 6
        y = Y_BOT + (Y_TOP - Y_BOT) * t
        pts.append((x + twist * math.sin(t * math.pi) * 0.20,
                    y,
                    z + twist * math.sin(t * math.pi) * 0.10))
    return pts


def loop(xa, xb, y_end, reach, z_bias=0.0):
    """A hairpin connecting a front strand to a back strand."""
    pts = []
    for i in range(9):
        t = i / 8
        y = y_end + reach * math.sin(t * math.pi)
        pts.append((xa + (xb - xa) * t,
                    y,
                    Z_A + (Z_B - Z_A) * t + z_bias * math.sin(t * math.pi)))
    return pts


def domain(name, dx, flip):
    """One variable domain, translated into place and optionally flipped so the
    two domains pack against each other about a pseudo-twofold axis."""
    out = []

    def place(pts):
        moved = []
        for (x, y, z) in pts:
            if flip:
                x, z = -x, -z
            moved.append((x + dx, y, z))
        return moved

    for i, x in enumerate(SHEET_A):
        out.append({"k": "sa", "d": name, "p": place(strand(x, Z_A, 1 if i % 2 else -1))})
    for i, x in enumerate(SHEET_B):
        out.append({"k": "sb", "d": name, "p": place(strand(x, Z_B, -1 if i % 2 else 1))})

    # three CDR loops at the top: the combining site
    for i, (xa, xb) in enumerate(zip(SHEET_A[:3], SHEET_B[1:4])):
        out.append({"k": "cdr", "d": name, "n": f"CDR-{name[-1]}{i + 1}",
                    "p": place(loop(xa, xb, Y_TOP, 0.55 + 0.13 * i, 0.30))})
    # framework loops at the bottom, drawn quietly
    for xa, xb in zip(SHEET_A[1:], SHEET_B[2:]):
        out.append({"k": "fw", "d": name, "p": place(loop(xa, xb, Y_BOT, -0.42))})
    return out


def scfv():
    els = domain("VH", -1.38, False) + domain("VL", 1.38, True)

    # the flexible linker: VH C-terminus round to the VL N-terminus
    link = []
    for i in range(17):
        t = i / 16
        link.append((-1.38 + 2.76 * t,
                     -2.05 - 0.42 * math.sin(t * math.pi) + 0.10 * math.sin(t * 7),
                     1.05 + 0.30 * math.cos(t * 5)))
    els.append({"k": "link", "d": "linker", "p": link})

    # antigen: an ellipsoid resting on the combining site
    ag = []
    for i in range(33):
        a = 2 * math.pi * i / 32
        ag.append((1.62 * math.cos(a), 3.30 + 0.72 * math.sin(a), 0.95 * math.sin(a)))
    els.append({"k": "ag", "d": "antigen", "p": ag, "closed": True})
    return els


# ------------------------------------------------------------------- rendering
CLS = {"sa": "pstrand", "sb": "pstrand pstrand-b", "cdr": "pcdr",
       "fw": "ploop", "link": "plink", "ag": "pag"}
LABEL = {"sa": "VH/VL beta-sheet", "sb": "VH/VL beta-sheet", "cdr": "CDR loop",
         "fw": "framework loop", "link": "flexible linker", "ag": "antigen"}


def render(els, ry, rx):
    """Depth-sorted painter's algorithm."""
    drawn = []
    for idx, e in enumerate(els):
        r = [rot(p, ry, rx) for p in e["p"]]
        depth = sum(p[2] for p in r) / len(r)
        pts = [project(p) for p in r]
        d = "".join(("M" if i == 0 else "L") + f"{x:.3f} {y:.3f}"
                    for i, (x, y) in enumerate(pts))
        if e.get("closed"):
            d += "Z"
        title = e.get("n") or LABEL[e["k"]]
        drawn.append((depth, f'<path class="{CLS[e["k"]]}" data-i="{idx}" d="{d}">'
                             f'<title>{e["d"]} \u2014 {title}</title></path>'))
    drawn.sort(key=lambda t: t[0])          # far to near
    return "\n            ".join(p for _, p in drawn)


def bounds(els, samples=24):
    xs, ys = [], []
    for i in range(samples):
        ry = 2 * math.pi * i / samples
        for e in els:
            for p in e["p"]:
                x, y = project(rot(p, ry, -0.34))
                xs.append(x); ys.append(y)
    return min(xs), max(xs), min(ys), max(ys)


def protein_figure():
    els = scfv()
    x0, x1, y0, y1 = bounds(els)
    pad = 0.30
    vb = f"{x0 - pad:.2f} {y0 - pad:.2f} {x1 - x0 + 2 * pad:.2f} {y1 - y0 + 2 * pad:.2f}"
    geom = json.dumps([{k: v for k, v in e.items()} for e in els],
                      separators=(",", ":"))
    svg = f'''<figure class="fig fig-protein">
          <div class="fig-box">
            <svg class="protein" id="protein" viewBox="{vb}" role="img"
                 aria-label="Schematic of a single-chain variable fragment bound to an antigen: two immunoglobulin variable domains, each a beta-sandwich, with three CDR loops apiece meeting at the combining site.">
            {render(els, 0.55, -0.34)}
            </svg>
          </div>
          <figcaption class="fig-cap">Schematic scFv: two variable domains, six CDR loops meeting at the combining site, an antigen above.<span class="hint"> Drag to rotate.</span></figcaption>
        </figure>'''
    return svg, geom


# ------------------------------------------------------------ energy landscape
NAT_X, ADV_X, TGT_X = 0.34, 0.66, 0.08


def energy(x):
    """Monotonically decreasing: moving away from the natural sample toward the
    untargeted attack always lowers energy, and toward the targeted attack
    always raises it. A barrier between the two would misstate the result."""
    return 1.02 - 0.30 * x - 0.52 / (1.0 + math.exp(-(x - 0.44) / 0.075))



W, H = 100.0, 46.0


def ex(x):
    return 6 + x * (W - 12)


def ey(e):
    return 6 + (e / 1.05) * (H - 14)


def energy_figure():
    curve = "".join(("M" if i == 0 else "L") +
                    f"{ex(i / 160):.2f} {ey(energy(i / 160)):.2f}"
                    for i in range(161))
    nx, ny = ex(NAT_X), ey(energy(NAT_X))
    ax_, ay = ex(0.50), ey(energy(0.50))          # eps = 0.5, untargeted
    d0 = energy(0.50) - energy(NAT_X)
    seed = ("&#916;E &#8722;%.2f &middot; lower energy than the natural sample" % abs(d0)
            if d0 < 0 else
            "&#916;E +%.2f &middot; higher energy than the natural sample" % d0)
    svg = f'''<figure class="fig fig-energy">
          <div class="fig-box">
            <svg class="energy" id="energy" viewBox="0 0 {W:.0f} {H:.0f}" role="img"
                 aria-label="Schematic energy landscape. A natural sample sits in a shallow well; an untargeted adversarial example sits at lower energy, further into the model's own distribution.">
              <path class="ecurve" d="{curve}"/>
              <line class="edelta" id="edelta" x1="{ax_:.2f}" y1="{ny:.2f}" x2="{ax_:.2f}" y2="{ay:.2f}"/>
              <circle class="enat" cx="{nx:.2f}" cy="{ny:.2f}" r="1.9"><title>natural sample</title></circle>
              <circle class="eadv" id="eadv" cx="{ax_:.2f}" cy="{ay:.2f}" r="1.9"><title>adversarial example</title></circle>
            </svg>
          </div>
          <div class="econtrols">
            <label class="erow"><span>attack strength</span>
              <input type="range" id="eeps" min="0" max="100" value="50" aria-label="Attack strength epsilon"></label>
            <div class="erow ebtns" role="group" aria-label="Attack type">
              <button type="button" id="euntgt" class="ebtn is-on">untargeted</button>
              <button type="button" id="etgt" class="ebtn">targeted</button>
            </div>
            <p class="ereadout" id="ereadout" aria-live="polite">{seed}</p>
          </div>
          <figcaption class="fig-cap">Schematic, not measured data. Untargeted attacks land at lower energy than real data; targeted attacks do the opposite.</figcaption>
        </figure>'''
    return svg


if __name__ == "__main__":
    els = scfv()
    print("protein elements:", len(els), "| points:", sum(len(e["p"]) for e in els))
    print("viewBox bounds  :", [round(b, 2) for b in bounds(els)])
    for label, x in (("natural", NAT_X), ("adv untargeted", ADV_X), ("adv targeted", TGT_X)):
        print(f"  E({label:15}) = {energy(x):.3f}")
    print("  dE untargeted =", round(energy(ADV_X) - energy(NAT_X), 3), "(want negative)")
    print("  dE targeted   =", round(energy(TGT_X) - energy(NAT_X), 3), "(want positive)")
