"""Release-blocking validation for a built font.

Checks (per the project design):
1. OpenType, TTF, and WOFF2 file structures are valid
2. Every declared ligature shapes to its expected glyph through HarfBuzz
3. Mappings have no duplicates, no missing SVGs, no unreferenced glyphs
4. COLR/CPAL tables match the font's declared COLR version
5. TTF and WOFF2 agree on glyphs, mappings, and font internal version
"""
from __future__ import annotations

from pathlib import Path

import uharfbuzz as hb
from fontTools.ttLib import TTFont

from .build import _assign_codepoints
from .model import GameData


class ValidationError(Exception):
    pass


def check_structure(ttf: Path, woff2: Path) -> None:
    for path in (ttf, woff2):
        try:
            TTFont(str(path))
        except Exception as e:
            raise ValidationError(f"invalid font structure: {path}: {e}")


def check_shaping(game: GameData, font: TTFont, ttf: Path, lite: bool) -> None:
    cmap = font.getBestCmap()
    glyph_order = font.getGlyphOrder()
    cp_for = {(name, style): cp for name, style, cp in _assign_codepoints(game, lite=lite)}

    blob = hb.Blob.from_file_path(str(ttf))
    face = hb.Face(blob)
    hbfont = hb.Font(face)
    failed = []
    for sym in game.symbols:
        if (sym.name, "default") not in cp_for:
            failed.append((sym.name, "no default codepoint"))
            continue
        expected = cmap.get(cp_for[(sym.name, "default")])
        if expected is None:
            failed.append((sym.name, f"codepoint not in cmap: 0x{cp_for[(sym.name, 'default')]:04X}"))
            continue
        for lig in sym.ligature:
            buf = hb.Buffer()
            buf.add_str(lig)
            buf.guess_segment_properties()
            hb.shape(hbfont, buf, {"liga": True, "kern": False})
            ids = [info.codepoint for info in buf.glyph_infos]
            names = [glyph_order[i] for i in ids if i < len(glyph_order)]
            if names != [expected]:
                failed.append((sym.name, lig, names, expected))
    if failed:
        detail = "; ".join(str(f) for f in failed[:10])
        raise ValidationError(f"{len(failed)} ligatures failed to shape: {detail}")


def check_mappings(game: GameData) -> None:
    names = [s.name for s in game.symbols]
    dup_names = {n for n in names if names.count(n) > 1}
    ligs = [l for s in game.symbols for l in s.ligature]
    dup_ligs = {l for l in ligs if ligs.count(l) > 1}
    missing_svg = []
    unreferenced = []
    referenced = set()
    for s in game.symbols:
        for style, f in s.svg.items():
            svg = game.svg_dir / style / f
            if not svg.exists():
                missing_svg.append(f"{s.name}/{style}/{f}")
            referenced.add((style, f))
    if game.colr_fallback is not None:
        for o in game.colr_fallback.override_art:
            svg = game.svg_dir / o.style / o.file
            if not svg.exists():
                missing_svg.append(f"{o.name}/{o.style}/{o.file}")
            referenced.add((o.style, o.file))
    for style_dir in game.svg_dir.iterdir():
        if not style_dir.is_dir():
            continue
        for f in style_dir.iterdir():
            if (style_dir.name, f.name) not in referenced:
                unreferenced.append(f"{style_dir.name}/{f.name}")
    problems = []
    if dup_names:
        problems.append(f"duplicate symbol names: {sorted(dup_names)}")
    if dup_ligs:
        problems.append(f"duplicate ligatures: {sorted(dup_ligs)}")
    if missing_svg:
        problems.append(f"missing SVGs: {missing_svg[:10]}")
    if unreferenced:
        problems.append(f"unreferenced SVGs: {unreferenced[:10]}")
    if problems:
        raise ValidationError("; ".join(problems))


def check_colr(expected_version: str, font: TTFont) -> None:
    colr = font.get("COLR")
    if colr is None:
        raise ValidationError("font has no COLR table")
    expected = {"v0": 0, "v1": 1}[expected_version]
    if colr.version != expected:
        raise ValidationError(
            f"COLR version {colr.version} does not match expected {expected_version}"
        )


def check_consistency(font: TTFont, woff2: Path) -> None:
    other = TTFont(str(woff2))
    if list(font.getGlyphOrder()) != list(other.getGlyphOrder()):
        raise ValidationError("TTF and WOFF2 glyph orders differ")
    if font.getBestCmap() != other.getBestCmap():
        raise ValidationError("TTF and WOFF2 cmaps differ")
    if font["name"].getDebugName(5) != other["name"].getDebugName(5):
        raise ValidationError("TTF and WOFF2 version strings differ")


def validate(
    game: GameData,
    ttf: Path,
    woff2: Path,
    lite: bool = False,
    expected_colr_version: str | None = None,
) -> None:
    expected_colr_version = expected_colr_version or game.colr_version
    check_mappings(game)
    check_structure(ttf, woff2)
    font = TTFont(str(ttf))
    check_shaping(game, font, ttf, lite)
    check_colr(expected_colr_version, font)
    check_consistency(font, woff2)
