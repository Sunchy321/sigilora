"""Composition algorithms, faithfully ported from the predecessor scripts.

Produces the target SVG for each (symbol, style) from the raw materials:
- shadow:       default glyph offset by the shadow, over the _shadow background
- flat-simple:  default glyph scaled around center, recolored, over the _flat background
- flat-complex: composition of _<part> components (hybrid symbols)
- loyalty:      _loyalty_{up,down,naught} plus the counter text as paths
- static:       copy a pre-built raw file verbatim (special cases)
"""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

import svgutils.transform as sg
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

from .model import GameData, Symbol

SVG_NS = "{http://www.w3.org/2000/svg}"

ET.register_namespace("", "http://www.w3.org/2000/svg")


def compose_style(game: GameData, sym: Symbol, style: str, out: Path, plantin: Path | None) -> None:
    spec = sym.compose.get(style)
    if spec is None:
        raise ValueError(f"{sym.name}: style '{style}' has no compose spec")
    kind = spec["type"]
    if kind == "shadow":
        _compose_shadow(game, sym, out)
    elif kind == "flat-simple":
        _compose_flat_simple(game, sym, out)
    elif kind == "flat-complex":
        _compose_flat_complex(game, sym, spec["parts"], out)
    elif kind == "loyalty":
        _compose_loyalty(game, sym, spec["base"], out, plantin)
    elif kind == "static":
        _copy_static(game, sym, style, out)
    else:
        raise ValueError(f"{sym.name}: unknown compose type '{kind}'")


def _compose_shadow(game: GameData, sym: Symbol, out: Path) -> None:
    params = game.compose["shadow"]
    ox, oy = params["offset"]
    fig = sg.SVGFigure(100, 100)
    fig1 = sg.fromfile(str(game.raw_dir / "default" / sym.svg["default"]))
    fig2 = sg.fromfile(str(game.raw_dir / "components" / "_shadow.svg"))
    plot1 = fig1.getroot()
    plot2 = fig2.getroot()
    plot1.moveto(ox, 0)
    plot2.moveto(0, oy)
    fig.append([plot1, plot2])
    fig.root.set("viewBox", params["viewbox"])
    fig.save(str(out))


def _compose_flat_simple(game: GameData, sym: Symbol, out: Path) -> None:
    params = game.compose["flat-simple"]
    scale = params["scale"]
    fill_map = params["fill-map"]
    fig = sg.SVGFigure(100, 100)
    fig1 = sg.fromfile(str(game.raw_dir / "default" / sym.svg["default"]))
    fig2 = sg.fromfile(str(game.raw_dir / "components" / "_flat.svg"))
    plot1 = fig1.getroot()
    plot2 = fig2.getroot()
    g = plot1[0]
    children = g.root.getchildren()
    g.root.clear()
    basic_fill = ""
    for child in children:
        if child.tag == f"{SVG_NS}circle":
            basic_fill = child.get("fill")
            continue
        if child.get("id") == "Shape":
            basic_fill = "#CAC5C0"
            continue
        child.set("transform", f"translate(50, 50) scale({scale}) translate(-50, -50)")
        if "fill" in child.keys():
            if fill_map.get(basic_fill) is None:
                raise ValueError(f"Unknown fill color: {basic_fill} in {sym.svg['default']}")
            child.set("fill", fill_map[basic_fill])
        g.root.append(child)
    circle = plot2[0]
    circle.root.set("fill", fill_map[basic_fill])
    fig.append([plot2, plot1])
    fig.root.set("viewBox", "0 0 100 100")
    fig.save(str(out))


def _compose_flat_complex(game: GameData, sym: Symbol, parts: list[str], out: Path) -> None:
    params = game.compose["flat-complex"]
    fig = sg.SVGFigure(100, 100)
    content = []
    for part in parts:
        part_fig = sg.fromfile(str(game.raw_dir / "components" / f"_{part}.svg"))
        part_root = part_fig.getroot()
        if part.endswith("_up"):
            part_root.root.set("transform", params["part-up-transform"])
        elif part.endswith("_down"):
            part_root.root.set("transform", params["part-down-transform"])
        content.append(part_root)
    fig.append(content)
    fig.root.set("viewBox", "0 0 100 100")
    fig.save(str(out))


def _text_to_path(font_path: Path, text: str, font_size: int):
    font = TTFont(str(font_path))
    head = font.get("head")
    units_per_em = getattr(head, "unitsPerEm", 1000)
    scale = font_size / units_per_em
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap()
    svg_path_pen = SVGPathPen(glyph_set)
    total_width = 0
    path_commands = []
    for char in text:
        glyph_name = cmap.get(ord(char))
        if glyph_name is None:
            continue
        glyph = glyph_set[glyph_name]
        transform = (scale, 0, 0, -scale, total_width * scale, 0)
        transform_pen = TransformPen(svg_path_pen, transform)
        glyph.draw(transform_pen)
        path_commands.append(svg_path_pen.getCommands())
        svg_path_pen = SVGPathPen(glyph_set)
        total_width += glyph.width
    all_path_data = " ".join(path_commands)
    text_width = total_width * scale
    text_height = font_size * 0.784
    return all_path_data, text_width, text_height


def _compose_loyalty(game: GameData, sym: Symbol, base: str, out: Path, plantin: Path | None) -> None:
    if plantin is None:
        plantin = game.path / "external" / game.compose["loyalty"]["font"]
    if not plantin.exists():
        raise ValueError(
            f"{sym.name}: loyalty font not found at {plantin}; see fonts/{game.code}/external/README.md"
        )

    params = game.compose["loyalty"]
    text = sym.ligature[0].strip("[]").replace("-", "−")
    component = game.raw_dir / "components" / f"_loyalty_{base}.svg"
    tree = ET.parse(component)
    root = tree.getroot()
    viewbox = root.get("viewBox", "")
    width = int(viewbox.split()[2])
    height = int(viewbox.split()[3])
    path_data, text_width, text_height = _text_to_path(plantin, text, params["font-size"])
    if not path_data:
        raise ValueError(f"{sym.name}: cannot render loyalty text '{text}' to path")
    path_elem = ET.SubElement(root, f"{SVG_NS}path")
    path_elem.set("d", path_data)
    path_elem.set("fill", "currentColor")
    x_offset = (width - text_width) / 2
    y_offset = height / 2 + text_height * 0.35
    path_elem.set("transform", f"translate({x_offset}, {y_offset})")
    tree.write(out, encoding="utf-8", xml_declaration=True)


def _copy_static(game: GameData, sym: Symbol, style: str, out: Path) -> None:
    src = game.raw_dir / "static" / style / sym.compose[style]["file"]
    out.write_bytes(src.read_bytes())
