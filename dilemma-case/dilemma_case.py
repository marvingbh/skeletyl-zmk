"""Parametric 3D-printable case for the Dilemma 3mod (one PCB half, reversible).

Bottom tray holds the PCB on standoffs. A cover closes the controller area and
a battery pod on the inner edge. All units mm. KiCad (x, y-down) coordinates are
converted to (x, -y) so the model is seen from the top like in KiCad.

Outputs left/right STL + STEP for the tray and the cover.
"""
import math, re, sys, pathlib
from build123d import *

HERE = pathlib.Path(__file__).parent
PCB = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
# gap between keyboard PCB top and controller PCB bottom (depends on the headers)
MCU_GAP = float(sys.argv[3]) if len(sys.argv) > 3 else 2.5   # standard header plastic

# ---------- parameters ----------
CLR = 0.4            # gap between PCB edge and the wall
WALL = 2.0
FLOOR = 2.0
GAP_UNDER = 3.0      # PCB bottom above floor: choc pins + solder
PCB_T = 1.6
RIM_ABOVE = 1.0      # tray wall top above PCB top
MCU_PCB, MCU_USB_H = 1.2, 3.3   # controller board, USB-C height above it
# free height under the cover: at least flush with the Choc keycaps (6.4), more for tall headers
COVER_IN = max(6.4, MCU_GAP + MCU_PCB + MCU_USB_H + 0.9)
COVER_TOP = 1.6
BAT = (20.0, 38.0, 9.0)   # battery x, y, z (lying flat on the pod floor)
BAT_CLR = 1.0
STANDOFF_D = 6.5
SCREW_D = 3.4
NUT_AF = 5.7         # M3 nut across flats + clearance
NUT_DEPTH = 2.6
HEAD_D = 6.2         # M3 head counterbore in the cover
HEAD_DEPTH = 2.0
COVER_X_MIN = 201.5  # cover starts right of the last key column (KiCad x)
COVER_Y_MAX = 85.4   # cover front edge (KiCad y)

Z_PCB_BOT = FLOOR + GAP_UNDER
Z_PCB_TOP = Z_PCB_BOT + PCB_T
Z_RIM = Z_PCB_TOP + RIM_ABOVE
Z_COVER_IN = Z_PCB_TOP + COVER_IN
Z_COVER_TOP = Z_COVER_IN + COVER_TOP

# ---------- PCB data ----------
s = PCB.read_text()

def arc_pts(st, md, en, n=10):
    (x1, y1), (x2, y2), (x3, y3) = st, md, en
    d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if abs(d) < 1e-9:
        return [st, en]
    ux = ((x1*x1+y1*y1)*(y2-y3)+(x2*x2+y2*y2)*(y3-y1)+(x3*x3+y3*y3)*(y1-y2))/d
    uy = ((x1*x1+y1*y1)*(x3-x2)+(x2*x2+y2*y2)*(x1-x3)+(x3*x3+y3*y3)*(x2-x1))/d
    r = math.hypot(x1-ux, y1-uy)
    a1, a2, a3 = (math.atan2(y-uy, x-ux) for x, y in (st, md, en))
    norm = lambda a: a % (2*math.pi)
    span = norm(a3-a1) if norm(a2-a1) < norm(a3-a1) else -norm(a1-a3)
    return [(ux+r*math.cos(a1+span*t/n), uy+r*math.sin(a1+span*t/n)) for t in range(n+1)]

segs = []
for m in re.finditer(r'\(gr_(line|arc)\b((?:(?!\(gr_).)*?)\(layer "Edge.Cuts"\)', s, re.S):
    k, b = m.groups()
    g = lambda key: tuple(map(float, re.search(r'\(%s ([-\d.]+) ([-\d.]+)\)' % key, b).groups()))
    segs.append([g('start'), g('end')] if k == 'line' else arc_pts(g('start'), g('mid'), g('end')))

# chain segments into one closed loop
def close(a, b): return abs(a[0]-b[0]) < 0.02 and abs(a[1]-b[1]) < 0.02
loop = segs.pop(0)
while segs:
    for i, sg in enumerate(segs):
        if close(loop[-1], sg[0]): loop += sg[1:]; break
        if close(loop[-1], sg[-1]): loop += sg[::-1][1:]; break
    else:
        raise SystemExit(f"outline not closed, {len(segs)} segments left")
    segs.pop(i)
if close(loop[0], loop[-1]): loop.pop()

def rdp(pts, eps):
    if len(pts) < 3: return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    L = math.hypot(x2-x1, y2-y1) or 1e-9
    dmax, idx = 0, 0
    for i in range(1, len(pts)-1):
        d = abs((y2-y1)*pts[i][0]-(x2-x1)*pts[i][1]+x2*y1-y2*x1)/L
        if d > dmax: dmax, idx = d, i
    if dmax > eps:
        return rdp(pts[:idx+1], eps)[:-1] + rdp(pts[idx:], eps)
    return [pts[0], pts[-1]]
half = len(loop) // 2
loop = rdp(loop[:half + 1], 0.03)[:-1] + rdp(loop[half:] + [loop[0]], 0.03)[:-1]
clean = []
for pt in loop:
    if not clean or math.hypot(pt[0]-clean[-1][0], pt[1]-clean[-1][1]) > 0.05:
        clean.append(pt)
if math.hypot(clean[0][0]-clean[-1][0], clean[0][1]-clean[-1][1]) <= 0.05:
    clean.pop()
loop = clean
print(f"outline: {len(loop)} points")

holes = [tuple(map(float, re.search(r'\(at ([-\d.]+) ([-\d.]+)', s[m.start():m.start()+400]).groups()))
         for m in re.finditer(r'\(footprint "[^"]*MountingHole', s)]
COVER_HOLES = [h for h in holes if h[0] > 200 and h[1] < 75]          # H6 H7 H8 H9
TRAY_HOLES = [h for h in holes if h not in COVER_HOLES]

P = lambda x, y: (x, -y)   # KiCad -> CAD

pcb_face = Face(Wire.make_polygon([Vector(*P(x, y)) for x, y in loop], close=True))
xs = [p[0] for p in loop]
X_EDGE = max(xs)                               # inner edge of the board (controller side)

# battery pod, next to the controller on the inner edge
pod_x0 = X_EDGE + CLR
pod_x1 = pod_x0 + BAT[0] + 2*BAT_CLR
pod_y0, pod_y1 = 36.0, 36.0 + BAT[1] + 2*BAT_CLR + 2
pod_in = Rectangle(pod_x1-pod_x0+CLR+1, pod_y1-pod_y0, align=(Align.MIN, Align.MIN)).moved(
    Location((pod_x0-CLR-1, -pod_y1)))

inner = offset(pcb_face, CLR, kind=Kind.ARC) + pod_in
inner = inner.faces()[0] if hasattr(inner, 'faces') else inner
outer = offset(inner, WALL, kind=Kind.ARC)
outer = outer.faces()[0]
inner_f = inner if isinstance(inner, Face) else inner.faces()[0]

def prism(face, z0, z1):
    return extrude(face.moved(Location((0, 0, z0))), amount=z1 - z0)

# ---------- tray ----------
tray = prism(outer, 0, Z_RIM) - prism(inner_f, FLOOR, Z_RIM + 1)
for hx, hy in holes:
    x, y = P(hx, hy)
    tray += Cylinder(STANDOFF_D/2, Z_PCB_BOT, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, y, 0)))
for hx, hy in holes:
    x, y = P(hx, hy)
    tray -= Cylinder(SCREW_D/2, Z_RIM + 2, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, y, -1)))
    nut = extrude(RegularPolygon(NUT_AF/2/math.cos(math.pi/6), 6), amount=NUT_DEPTH + 1)
    tray -= nut.moved(Location((x, y, -1)))

# power switch notch in the front wall (actuator sticks out of the board edge)
psw = re.search(r'Switch_MSK-12C01-07".*?\(at ([-\d.]+) ([-\d.]+)', s, re.S)
psw_x, psw_y = map(float, psw.groups())
tray -= Box(12, 8, Z_RIM, align=(Align.CENTER, Align.MIN, Align.MIN)).moved(
    Location((psw_x, -(psw_y + 1.0) - 8, Z_PCB_BOT - 0.5)))

# ---------- cover ----------
cut_rect = Rectangle(400, 400, align=(Align.MIN, Align.MIN)).moved(Location((COVER_X_MIN, -COVER_Y_MAX)))
cover_out = (outer & cut_rect).faces()[0]
cover_in = offset(cover_out, -WALL, kind=Kind.ARC).faces()[0]
cover = prism(cover_out, Z_RIM, Z_COVER_TOP) - prism(cover_in, Z_RIM - 1, Z_COVER_IN)
for hx, hy in COVER_HOLES:
    x, y = P(hx, hy)
    cover += Cylinder(STANDOFF_D/2, Z_COVER_IN - Z_PCB_TOP, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((x, y, Z_PCB_TOP)))
    cover -= Cylinder(SCREW_D/2, 40, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, y, 0)))
    cover -= Cylinder(HEAD_D/2, HEAD_DEPTH + 1, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((x, y, Z_COVER_TOP - HEAD_DEPTH)))
# USB opening in the back wall, centred on the controller. The controller's
# USB-C end overhangs the back edge of the board (KiCad y ~ 32).
mcu = re.search(r'pro-micro".*?\(at ([-\d.]+) ([-\d.]+)', s, re.S)
mcu_x, mcu_y = map(float, mcu.groups())
def edge_ys(x0):
    ys = []
    for (ax, ay), (bx, by) in zip(loop, loop[1:] + loop[:1]):
        if (ax - x0) * (bx - x0) <= 0 and ax != bx:
            ys.append(ay + (by - ay) * (x0 - ax) / (bx - ax))
    return ys
top_edge_y = min(edge_ys(mcu_x))            # back edge of the board at the controller
USB_W = 12.5                                # cable plug width
# U-shaped notch from just above the PCB through the top of the cover, so the
# plug fits whatever header height the controller is soldered on.
USB_Z0 = Z_PCB_TOP + 0.2
usb_slot = Box(USB_W, 3 * WALL + 2 * CLR, 40, align=(Align.CENTER, Align.MIN, Align.MIN))
usb_slot = fillet(usb_slot.edges().filter_by(Axis.Y).group_by(Axis.Z)[0], 2.0)
usb_slot = usb_slot.moved(Location((mcu_x, -top_edge_y - 0.5, USB_Z0)))
USB_Z = Z_PCB_TOP + MCU_GAP + MCU_PCB + MCU_USB_H / 2   # plug centre for this build
cover -= usb_slot      # open notch through the cover's back wall, so any plug fits
tray -= usb_slot
# finger room over the power switch
cover -= Box(12, 8, 3.0, align=(Align.CENTER, Align.MIN, Align.MIN)).moved(
    Location((psw_x, -(psw_y + 1.0) - 8, Z_RIM - 1)))

# ---------- export ----------
def save(part, name):
    export_stl(part, str(OUT / f"{name}.stl"), tolerance=0.02, angular_tolerance=0.2)
    export_step(part, str(OUT / f"{name}.step"))

mirror_plane = Plane.YZ
save(tray, "dilemma_tray_left")
save(cover, "dilemma_cover_left")
save(mirror(tray, mirror_plane), "dilemma_tray_right")
save(mirror(cover, mirror_plane), "dilemma_cover_right")

bb = (tray + cover).bounding_box()
print(f"size {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm")
print(f"controller gap {MCU_GAP} mm -> cover inside {COVER_IN:.1f} mm")
print(f"PCB top z={Z_PCB_TOP:.1f}, rim z={Z_RIM:.1f}, cover top z={Z_COVER_TOP:.1f}")
print(f"tray holes {len(TRAY_HOLES)}, cover holes {len(COVER_HOLES)}, pod x {pod_x0:.1f}..{pod_x1:.1f} y {pod_y0:.1f}..{pod_y1:.1f}")
cover_len = Z_COVER_TOP - HEAD_DEPTH - 0.6          # head seat down to inside the nut
cover_screw = max(l for l in (6, 8, 10, 12, 14, 16, 18, 20) if l <= cover_len)
print(f"USB U-notch at x={mcu_x:.1f}, back edge y={top_edge_y:.1f}, z {USB_Z0:.1f}..top (plug centre {USB_Z:.1f})")
print(f"screws: tray M3x6 ({len(TRAY_HOLES)}), cover M3x{cover_screw} ({len(COVER_HOLES)}), nuts {len(holes)}")
