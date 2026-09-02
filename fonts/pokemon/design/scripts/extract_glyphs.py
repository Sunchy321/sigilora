#!/usr/bin/env python3
"""Export the canonical PTCG energy symbol data from the EssentiarumTCG COLR font.

Every energy type has ONE canonical symbol outline: the glyph that the font's
`[X]`/`{X}` ligatures actually resolve to (a plain lowercase letter, c/d/f/g/l/m/
n/p/r/w/y). Those glyphs carry no COLR record, so in Essentiarum they are pure
monochrome outlines. Sigilora's pokemon font uses that same outline for all three
styles (default = bare currentColor, orb = glossy, flat = flat round badge) so the
three styles stay shape-identical.

Per type we also export the official round-disc base color from the font's O+letter
COLR glyph (layer 0 is the disc as a PaintSolid whose palette index differs per
energy); Sigilora's flat style fills its disc with that color.

Font y-axis is up; SVG y-axis is down, so paths are flipped at render time.
"""
from __future__ import annotations

import json
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]  # fonts/pokemon/design
FONT = ROOT / "assets" / "font_src" / "EssentiarumTCG v1-COLR.otf"
OUT = ROOT / "assets" / "glyphs.json"

# Energy color key letter -> canonical symbol glyph name (the {X} ligature target).
GLYPH = {
    "C": "c", "D": "d", "F": "f", "G": "g", "L": "l", "M": "m",
    "N": "n", "P": "p", "R": "r", "W": "w", "Y": "y",
}

# O+<letter> round-glyph codepoints: only used to read each type's disc solid color.
BASE = {
    "C": 0xE052, "D": 0xE053, "F": 0xE054, "G": 0xE055, "L": 0xE056,
    "M": 0xE057, "N": 0xE058, "P": 0xE059, "R": 0xE05A, "W": 0xE05B, "Y": 0xE05C,
}


def path_and_bounds(gs, gname):
    gl = gs[gname]
    pen = SVGPathPen(gs)
    gl.draw(pen)
    bp = BoundsPen(gs)
    gl.draw(bp)
    return pen.getCommands(), bp.bounds


def disc_color(by_name, ll, palette, cp) -> str:
    """Solid fill of the O+letter glyph's disc layer (a PaintSolid palette index)."""
    rec = by_name[f"uni{cp:X}"]
    disc_paint = ll.Paint[rec.Paint.FirstLayerIndex].Paint
    index = disc_paint.PaletteIndex
    color = palette[index]
    return f"#{color.red:02X}{color.green:02X}{color.blue:02X}"


def main() -> None:
    f = TTFont(str(FONT))
    gs = f.getGlyphSet()
    colr = f["COLR"].table
    palette = f["CPAL"].palettes[0]
    by_name = {r.BaseGlyph: r for r in colr.BaseGlyphList.BaseGlyphPaintRecord}
    ll = colr.LayerList

    out = {}
    for letter in "CDFGLMNPRWY":
        glyph = GLYPH[letter]
        path, bbox = path_and_bounds(gs, glyph)
        out[letter] = {
            # canonical symbol outline, shared by the default / orb / flat styles
            "sym_glyph": glyph,
            "sym_path": path,
            "sym_bbox": list(bbox),
            # official round-disc base color (used by the flat style's disc fill)
            "disc_color": disc_color(by_name, ll, palette, BASE[letter]),
        }
        print(f"{letter}: glyph={glyph} bbox={[round(x, 2) for x in bbox]} disc={out[letter]['disc_color']}")

    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
