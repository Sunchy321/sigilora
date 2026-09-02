#!/usr/bin/env python3
"""Extract PTCG energy symbol outlines from the EssentiarumTCG COLR font.

Reads the EssentiarumTCG v1-COLR.otf, walks each O+<letter> ligature glyph's
COLR layer list (layer 0 = orb, layer 1 = per-type symbol), and writes the
symbol path + bounding box into assets/glyphs.json.

Font y-axis is up; SVG y-axis is down, so paths must be flipped at render time.
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

# O+<letter> ligature codepoints (from the font's liga feature analysis)
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


def main() -> None:
    f = TTFont(str(FONT))
    gs = f.getGlyphSet()
    colr = f["COLR"].table
    by_name = {r.BaseGlyph: r for r in colr.BaseGlyphList.BaseGlyphPaintRecord}

    out = {}
    for letter in "CDFGLMNPRWY":
        uni = f"uni{BASE[letter]:X}"
        rec = by_name[uni]
        orb_paint = colr.LayerList.Paint[rec.Paint.FirstLayerIndex]
        sym_paint = colr.LayerList.Paint[rec.Paint.FirstLayerIndex + 1]
        orb_glyph, sym_glyph = orb_paint.Glyph, sym_paint.Glyph
        po, bo = path_and_bounds(gs, orb_glyph)
        ps, bs = path_and_bounds(gs, sym_glyph)
        out[letter] = {
            "orb_glyph": orb_glyph,
            "sym_glyph": sym_glyph,
            "orb_path": po,
            "orb_bbox": list(bo),
            "sym_path": ps,
            "sym_bbox": list(bs),
        }
        print(f"{letter}: sym={sym_glyph} bbox={[round(x, 2) for x in bs]}")

    OUT.write_text(json.dumps(out))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
