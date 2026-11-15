"""Build a coloured assembly preview (both halves) of the Dilemma 3mod case.

Usage: python assembly.py <dilemma.kicad_pcb> <out_dir>
Writes assembly_closed.glb (cover on) and assembly_open.glb (cover lifted off).
"""
import math, re, sys, runpy, pathlib
from build123d import *

pcb_path, out_dir = sys.argv[1], pathlib.Path(sys.argv[2])
here = pathlib.Path(__file__).parent
sys.argv = [str(here / "dilemma_case.py"), pcb_path, str(out_dir)]
g = runpy.run_path(sys.argv[0], run_name="__main__")
s = pathlib.Path(pcb_path).read_text()
P = g["P"]; zt = g["Z_PCB_TOP"]; zb = g["Z_PCB_BOT"]

def colored(shape, rgb):
    shape.color = Color(*rgb)
    return shape

# switch positions and rotations
switches = []
for m in re.finditer(r'\(footprint "[^"]*SW_MX_choc"', s):
    at = re.search(r'\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)', s[m.start():m.start() + 600])
    switches.append((float(at.group(1)), float(at.group(2)), float(at.group(3) or 0)))

def half():
    parts = []
    parts.append(colored(g["tray"], (0.55, 0.58, 0.63)))
    pcb = extrude(g["pcb_face"].moved(Location((0, 0, zb))), amount=g["PCB_T"])
    parts.append(colored(pcb, (0.12, 0.45, 0.25)))
    for x, y, r in switches:
        cx, cy = P(x, y)
        loc = Location((cx, cy, 0), (0, 0, 1), r)
        housing = Box(15, 15, 3.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, zt)))
        cap = Box(17.5, 16.5, 3.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, zt + 5.0)))
        cap = fillet(cap.edges().filter_by(Axis.Z), 1.5)
        parts.append(colored(housing.moved(loc), (0.15, 0.15, 0.15)))
        parts.append(colored(cap.moved(loc), (0.92, 0.92, 0.88)))
    mx, my = P(g["mcu_x"], g["mcu_y"])
    parts.append(colored(Box(18, 33.3, 1.2, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((mx, my, zt + 1.0))), (0.05, 0.05, 0.4)))
    parts.append(colored(Box(9, 7.5, 3.3, align=(Align.CENTER, Align.MAX, Align.MIN)).moved(Location((mx, my + 16.65 + 0.8, zt + 2.2))), (0.7, 0.7, 0.72)))
    bx = g["pod_x0"] + g["BAT_CLR"] + g["BAT"][0] / 2
    by = -(g["pod_y0"] + g["BAT_CLR"] + 1 + g["BAT"][1] / 2)
    parts.append(colored(Box(*g["BAT"], align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((bx, by, g["FLOOR"]))), (0.85, 0.75, 0.2)))
    # MSK-12C02 slide switch: body on the PCB, actuator sticking out of the front edge
    sx, sy = P(g["psw_x"], g["psw_y"])
    parts.append(colored(Box(6.7, 2.6, 1.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((sx, sy, zt))), (0.75, 0.75, 0.78)))
    parts.append(colored(Box(1.5, 2.0, 1.2, align=(Align.CENTER, Align.MAX, Align.MIN)).moved(Location((sx, sy - 1.3, zt + 0.1))), (0.9, 0.1, 0.1)))
    return parts

def cover(lift):
    return colored(g["cover"].moved(Location((0, 0, lift))), (0.55, 0.58, 0.63))

left = half()
bb = Compound(left).bounding_box()
gap = 40
shift = bb.max.X + gap + (bb.max.X - bb.min.X) * 0 - bb.min.X  # placeholder, recomputed below

def mirrored(parts):
    out = []
    for p in parts:
        q = mirror(p, Plane.YZ)
        q.color = p.color
        out.append(q)
    return out

def place_right(parts):
    # mirror about x=0, then move so the inner edges face each other with a gap
    m = mirrored(parts)
    mb = Compound(m).bounding_box()
    dx = (bb.max.X + gap) - mb.min.X
    return [q.moved(Location((dx, 0, 0))) for q in m], dx

for name, lift in (("assembly_closed", 0.0), ("assembly_open", 25.0)):
    lp = left + [cover(lift)]
    rp, _ = place_right(lp)
    asm = Compound(children=lp + rp)
    export_gltf(asm, str(out_dir / f"{name}.glb"), binary=True, linear_deflection=0.05, angular_deflection=0.3)
    print("wrote", name)
