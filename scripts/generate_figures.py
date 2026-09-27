"""Generate the repository's SVG figures using only the Python standard library."""

from __future__ import annotations

import csv
import math
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
DATA = ROOT / "data"
FIGURES.mkdir(exist_ok=True)


def save(name: str, content: str) -> None:
    (FIGURES / name).write_text(content, encoding="utf-8")


def svg_open(width: int, height: int, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'role="img" aria-label="{escape(title)}">\n'
        f'<title>{escape(title)}</title>\n'
        '<rect width="100%" height="100%" fill="#ffffff"/>\n'
        '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#1d2a3a}'
        '.heading{font-weight:700;font-size:22px}.label{font-size:15px}'
        '.small{font-size:12px;fill:#526174}</style>\n'
    )


def pin_figure() -> None:
    cx, cy, scale = 300, 265, 300
    outer_r = 0.7 / math.cos(math.pi / 6)
    pts = []
    for k in range(6):
        angle = math.pi / 6 + k * math.pi / 3
        pts.append(f"{cx + scale * outer_r * math.cos(angle):.1f},{cy - scale * outer_r * math.sin(angle):.1f}")
    s = svg_open(900, 550, "Illustrative cross-section mesh regions: fuel, gap, sheath, coolant")
    s += '<text class="heading" x="34" y="40">Defective fuel element: teaching geometry</text>\n'
    s += '<text class="small" x="34" y="62">Schematic only; dimensions are normalized exercise values, not CANDU measurements.</text>\n'
    s += f'<polygon points="{" ".join(pts)}" fill="#dbeefa" stroke="#2870a5" stroke-width="3"/>\n'
    for radius, color, stroke in [(0.48, "#9ea6b0", "#414c5c"), (0.42, "#f2c46e", "#9e6712"), (0.40, "#ea8d6a", "#9f3d27")]:
        s += f'<circle cx="{cx}" cy="{cy}" r="{radius * scale:.1f}" fill="{color}" stroke="{stroke}" stroke-width="2"/>\n'
    s += f'<circle cx="{cx}" cy="{cy}" r="4" fill="#8e2c22"/>\n'
    # A red mark locates the conceptual defect at the top of the sheath.
    s += '<path d="M 300 121 L 300 93 M 291 107 L 309 107" stroke="#c52232" stroke-width="5" stroke-linecap="round"/>\n'
    labels = [
        ("Fuel pellet", "r < 0.40", 590, 165, 407, 203, "#9f3d27"),
        ("Fuel-to-sheath gap", "0.40 - 0.42", 590, 240, 423, 222, "#9e6712"),
        ("Sheath", "0.42 - 0.48", 590, 315, 443, 265, "#414c5c"),
        ("Coolant cell", "outside r = 0.48", 590, 390, 480, 341, "#2870a5"),
    ]
    for title, detail, tx, ty, px, py, color in labels:
        s += f'<path d="M {px} {py} L {tx-14} {ty-7}" stroke="{color}" stroke-width="2" fill="none"/>\n'
        s += f'<circle cx="{px}" cy="{py}" r="4" fill="{color}"/>\n'
        s += f'<text class="label" x="{tx}" y="{ty}">{escape(title)}</text>\n'
        s += f'<text class="small" x="{tx}" y="{ty+19}">{escape(detail)}</text>\n'
    s += '<text class="small" x="34" y="518">The red mark indicates a possible defect location. The mesh input does not model a breach.</text>\n'
    save("fuel_element_schematic.svg", s + "</svg>\n")


def oxygen_figure() -> None:
    with (DATA / "oxygen_center.csv").open(newline="", encoding="utf-8") as stream:
        rows = [(float(r["time"]), float(r["center_c"])) for r in csv.DictReader(stream)]
    left, top, width, height = 95, 92, 680, 330
    x = lambda t: left + width * t
    y = lambda c: top + height * (1 - c / 0.30)
    s = svg_open(900, 520, "Oxygen concentration at fuel-path midpoint from MOOSE run")
    s += '<text class="heading" x="36" y="42">Oxygen ingress at the midpoint</text>\n'
    s += '<text class="small" x="36" y="64">Observed MOOSE output; normalized model units</text>\n'
    for val in (0, 0.1, 0.2, 0.3):
        yy = y(val)
        s += f'<line x1="{left}" y1="{yy:.1f}" x2="{left+width}" y2="{yy:.1f}" stroke="#dbe3ec"/>\n'
        s += f'<text class="small" x="{left-15}" y="{yy+4:.1f}" text-anchor="end">{val:.1f}</text>\n'
    for val in (0, 0.25, 0.5, 0.75, 1):
        xx = x(val)
        s += f'<line x1="{xx:.1f}" y1="{top}" x2="{xx:.1f}" y2="{top+height}" stroke="#eef2f6"/>\n'
        s += f'<text class="small" x="{xx:.1f}" y="{top+height+22}" text-anchor="middle">{val:g}</text>\n'
    s += f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+height}" stroke="#33465d" stroke-width="2"/>\n'
    s += f'<line x1="{left}" y1="{top+height}" x2="{left+width}" y2="{top+height}" stroke="#33465d" stroke-width="2"/>\n'
    points = " ".join(f"{x(t):.1f},{y(c):.1f}" for t, c in rows)
    s += f'<polyline points="{points}" fill="none" stroke="#007e87" stroke-width="4" stroke-linejoin="round"/>\n'
    for t, c in rows:
        s += f'<circle cx="{x(t):.1f}" cy="{y(c):.1f}" r="3" fill="#007e87"/>\n'
    s += f'<text class="label" x="{left+width/2:.1f}" y="{top+height+56}" text-anchor="middle">Model time</text>\n'
    s += '<text class="label" transform="translate(31 257) rotate(-90)" text-anchor="middle">Normalized concentration</text>\n'
    s += f'<text class="label" x="{x(1)-105:.1f}" y="{y(rows[-1][1])-18:.1f}">c = {rows[-1][1]:.3f}</text>\n'
    save("oxygen_ingress_curve.svg", s + "</svg>\n")


def coupling_figure() -> None:
    s = svg_open(1000, 310, "Conceptual links in defective fuel and teaching models")
    s += '<text class="heading" x="35" y="42">From a sheath defect to coupled fuel behavior</text>\n'
    boxes = [
        (35, "Sheath defect", "path for steam"),
        (275, "Fuel oxidation", "oxygen enters fuel"),
        (515, "Lower conductivity", "less heat escapes"),
        (755, "Higher fuel T", "can affect release"),
    ]
    for x, title, note in boxes:
        s += f'<rect x="{x}" y="100" width="210" height="92" rx="10" fill="#eaf3fb" stroke="#2870a5" stroke-width="2"/>\n'
        s += f'<text class="label" x="{x+105}" y="133" text-anchor="middle">{escape(title)}</text>\n'
        s += f'<text class="small" x="{x+105}" y="159" text-anchor="middle">{escape(note)}</text>\n'
    for x in (246, 486, 726):
        s += f'<path d="M {x} 146 L {x+25} 146 M {x+15} 137 L {x+25} 146 L {x+15} 155" fill="none" stroke="#2870a5" stroke-width="3"/>\n'
    s += '<text class="small" x="35" y="235">Mesh example: geometry</text>\n'
    s += '<text class="small" x="275" y="235">Oxygen example: diffusion</text>\n'
    s += '<text class="small" x="515" y="235">Heat example: change k</text>\n'
    s += '<text class="small" x="755" y="235">Not modeled: fission products / hydriding</text>\n'
    s += '<text class="small" x="35" y="278">Conceptual map based on Lewis (2024); arrows are not solved as a coupled system in these exercises.</text>\n'
    save("conceptual_coupling.svg", s + "</svg>\n")


if __name__ == "__main__":
    pin_figure()
    oxygen_figure()
    coupling_figure()
    print("Wrote 3 figures to", FIGURES)
