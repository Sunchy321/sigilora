#!/usr/bin/env python3
"""Build the three pokemon energy style sources under fonts/pokemon/raw/<style>/.

All three styles share ONE canonical symbol outline per type - the lowercase
glyph that the EssentiarumTCG `[X]`/`{X}` ligatures render (assets/glyphs.json
"sym_path"). They differ only in presentation:

  default  - bare symbol, no disc, fill=currentColor (adapts to the text color)
  orb      - glossy energy ball (approved gradient + radial shading + gloss)
  flat     - flat round badge: disc filled with the font's official base color
             (glyphs.json "disc_color"), same symbol, same placement as orb

orb and flat use an identical transform/scale so their discs and symbols are the
same size; orb adds the shading/gloss layers that flat omits.

viewBox is "0 0 100 100" (disc radius 50), matching the project's SVG convention.
raw/ is the long-term source; `sigilora normalize pokemon` produces svg/ from it.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # fonts/pokemon/design
RAW_DIR = ROOT.parent / "raw"  # fonts/pokemon/raw (style sources for `sigilora normalize`)
GLYPHS = json.loads((ROOT / "assets" / "glyphs.json").read_text())
COLORS = json.loads((ROOT / "assets" / "colors.json").read_text())

ORB_CX, ORB_CY = 346.5, 226.5  # orb center in font units
ORB_R = 346.5
VIEW = 100.0  # viewBox size; orb radius = VIEW / 2

# user-approved Grass values override the sampler (which reads slightly darker)
COLORS["Grass"]["body"] = ["#B4D43A", "#7EAF29", "#1E6E1D", "#005A29"]
COLORS["Grass"]["symbol"] = "#0B1900"

# The source images use a diagonal light field in addition to the orb shading.
# These values are intentionally kept as data so each type can be tuned without
# changing the SVG construction code.
BACKGROUND = {
    "Grass": ["#005D37", "#1CAC44"],
    "Fire": ["#A12922", "#EF6E53"],
    "Water": ["#03486A", "#00B3ED"],
    "Lightning": ["#A9791F", "#F4C52E"],
    "Psychic": ["#372740", "#E5BBD7"],
    "Fighting": ["#A52E0F", "#E15B1A"],
    "Darkness": ["#29343F", "#D0D7DF"],
    "Metal": ["#353B33", "#F3F2EA"],
    "Fairy": ["#790E2C", "#FCEFF3"],
    "Dragon": ["#4B4013", "#ADA158"],
    "Colorless": ["#8A8B8B", "#FFFFFF", "#8A8B8B"],
}

HIGHLIGHT = {
    name: {"size": [14, 18], "angle": 30, "opacity": [0.86, 0.34]}
    for name in COLORS
}

BODY_GEOMETRY = {
    "Grass": (64, 30, 62), "Fire": (66, 30, 62), "Water": (68, 30, 64),
    "Lightning": (64, 28, 62), "Psychic": (65, 27, 64),
    "Fighting": (66, 30, 62), "Darkness": (62, 32, 64),
    "Metal": (60, 32, 66), "Fairy": (65, 29, 62),
    "Dragon": (64, 30, 64), "Colorless": (60, 32, 66),
}

SYMBOL_SHADOWS = {"Metal": (0, 1.5, 2.2, "#F6F2E8", 0.82)}
METAL_TRIANGLE_PATH = "M345 90C346 88 348 88 349 90L472 307C473 308 472 311 470 311H225C222 311 221 308 222 307Z"

# gradient stops (radial centered near the top of the orb)
STOPS = [(0.0, "top"), (0.35, "upper"), (0.70, "lower"), (1.0, "bottom")]
HIGHLIGHT_PATH = "M 4.6 31.5 A 49 49 0 0 1 31.5 4.6 A 7.5 7.5 0 0 1 37.3 18.5 A 34 34 0 0 0 18.5 36.3 A 7.5 7.5 0 0 1 4.6 31.5 Z"
HIGHLIGHT_CORE_PATH = "M 8.1 28.6 A 47 47 0 0 1 28.6 8.1 A 4.2 4.2 0 0 1 32.7 16.2 A 38 38 0 0 0 16.2 32.7 A 4.2 4.2 0 0 1 8.1 28.6 Z"
DARKNESS_INNER_GUIDE_PATH = (
    "M 61.1 18.4 "
    "C 64.0 21.3 65.8 25.3 65.8 29.7 "
    "C 65.8 39.7 56.8 47.3 46.6 45.2 "
    "C 40.4 44.0 35.6 38.9 34.5 32.8 "
    "C 33.4 27.3 35.2 22.1 38.9 18.4 "
    "L 42.5 18.4 L 42.5 28.5 "
    "A 7.5 7.5 0 0 0 57.5 28.5 "
    "L 57.5 18.4 Z"
)


def mix(c1: str, c2: str, t: float) -> str:
    """Blend c1 toward c2 by t (0..1)."""
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(a, b))


def brighten(color: str, gain: float) -> str:
    channels = [int(color[index:index + 2], 16) for index in (1, 3, 5)]
    return "#" + "".join(f"{min(255, round(channel * gain)):02X}" for channel in channels)


def sheen_gradient(hexcol: str, uid: str, mid_opacity: float) -> str:
    mid = mix(hexcol, "#FFFFFF", 0.65)
    return (f'    <linearGradient id="sheen{uid}" x1="0" y1="1" x2="1" y2="0">\n'
            f'      <stop offset="0" stop-color="{hexcol}" stop-opacity="0"/>\n'
            f'      <stop offset="0.06" stop-color="{mid}" stop-opacity="0.04"/>\n'
            f'      <stop offset="0.14" stop-color="#FFFFFF" stop-opacity="0.38"/>\n'
            f'      <stop offset="0.86" stop-color="#FFFFFF" stop-opacity="0.38"/>\n'
            f'      <stop offset="0.94" stop-color="{mid}" stop-opacity="{mid_opacity:.2f}"/>\n'
            f'      <stop offset="1" stop-color="{hexcol}" stop-opacity="0"/>\n'
            f'    </linearGradient>')


def sheen_mask(uid: str) -> str:
    return (f'    <radialGradient id="sheenMaskGradient{uid}" gradientUnits="userSpaceOnUse" cx="50" cy="50" r="50">\n'
            f'      <stop offset="0.72" stop-color="#000000" stop-opacity="0"/>\n'
            f'      <stop offset="0.78" stop-color="#FFFFFF" stop-opacity="0.64"/>\n'
            f'      <stop offset="0.85" stop-color="#FFFFFF" stop-opacity="1"/>\n'
            f'      <stop offset="0.94" stop-color="#FFFFFF" stop-opacity="0.72"/>\n'
            f'      <stop offset="0.98" stop-color="#FFFFFF" stop-opacity="0.16"/>\n'
            f'      <stop offset="1" stop-color="#000000" stop-opacity="0"/>\n'
            f'    </radialGradient>\n'
            f'    <mask id="sheenMask{uid}" maskUnits="userSpaceOnUse" x="0" y="0" width="100" height="100">\n'
            f'      <path d="{HIGHLIGHT_PATH}" fill="url(#sheenMaskGradient{uid})"/>\n'
            f'    </mask>')


def background_gradient(colors: list[str], angle: float, uid: str) -> str:
    import math
    radians = math.radians(angle)
    dx, dy = math.cos(radians) * 0.5, math.sin(radians) * 0.5
    x1, y1, x2, y2 = 0.5 - dx, 0.5 - dy, 0.5 + dx, 0.5 + dy
    stops = "\n".join(
        f'      <stop offset="{index / (len(colors) - 1):.3f}" stop-color="{color}"/>'
        for index, color in enumerate(colors)
    )
    return (f'    <linearGradient id="background{uid}" x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}">\n'
            f'{stops}\n'
            f'    </linearGradient>')


def darkness_background_gradient(uid: str) -> str:
    return (f'    <linearGradient id="background{uid}" gradientUnits="userSpaceOnUse" '
            f'x1="16.4971" y1="17.7739" x2="84.1454" y2="82.8424">\n'
            f'      <stop offset="0" stop-color="#9DB6DF"/>\n'
            f'      <stop offset="0.1675" stop-color="#285666"/>\n'
            f'      <stop offset="0.4434" stop-color="#1A2734"/>\n'
            f'      <stop offset="0.5911" stop-color="#1D2C3A"/>\n'
            f'      <stop offset="0.867" stop-color="#275666"/>\n'
            f'      <stop offset="1" stop-color="#9DB7DF"/>\n'
            f'    </linearGradient>')


def darkness_inner_highlight(uid: str) -> str:
    return (f'    <radialGradient id="darknessInnerHighlight{uid}" gradientUnits="userSpaceOnUse" cx="50" cy="26" r="21">\n'
            f'      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>\n'
            f'      <stop offset="0.48" stop-color="#FFFFFF" stop-opacity="0"/>\n'
            f'      <stop offset="0.66" stop-color="#FFFFFF" stop-opacity="0.92"/>\n'
            f'      <stop offset="0.78" stop-color="#FFFFFF" stop-opacity="1"/>\n'
            f'      <stop offset="1" stop-color="#FFFFFF" stop-opacity="1"/>\n'
            f'    </radialGradient>')

def darkness_highlight(uid: str) -> str:
    return (f'    <radialGradient id="darknessHighlight{uid}" cx="0.5" cy="0.5" r="0.5">\n'
            f'      <stop offset="0" stop-color="#FFFFFF" stop-opacity="1"/>\n'
            f'      <stop offset="0.38" stop-color="#E9F5FA" stop-opacity="0.90"/>\n'
            f'      <stop offset="0.70" stop-color="#8BC7DB" stop-opacity="0.42"/>\n'
            f'      <stop offset="0.90" stop-color="#3D8EA9" stop-opacity="0.12"/>\n'
            f'      <stop offset="1" stop-color="#3D8EA9" stop-opacity="0"/>\n'
            f'    </radialGradient>')


def metal_triangle_gradient(uid: str) -> str:
    return (f'    <radialGradient id="metalTriangle{uid}" cx="50%" cy="66.667%" r="68%">\n'
            f'      <stop offset="0" stop-color="#FFFFFF" stop-opacity="1"/>\n'
            f'      <stop offset="0.40" stop-color="#FFFFFF" stop-opacity="0.92"/>\n'
            f'      <stop offset="0.65" stop-color="#FFFFFF" stop-opacity="0.46"/>\n'
            f'      <stop offset="0.85" stop-color="#FFFFFF" stop-opacity="0"/>\n'
            f'      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>\n'
            f'    </radialGradient>')


def symbol_stroke_gradient(uid: str) -> str:
    return (f'    <linearGradient id="stroke{uid}" x1="0" y1="0" x2="1" y2="1">\n'
            f'      <stop offset="0" stop-color="#0C3447" stop-opacity="0.35"/>\n'
            f'      <stop offset="0.28" stop-color="#66D0E8" stop-opacity="0.95"/>\n'
            f'      <stop offset="0.58" stop-color="#2B89A5" stop-opacity="0.75"/>\n'
            f'      <stop offset="1" stop-color="#0A2838" stop-opacity="0.3"/>\n'
            f'    </linearGradient>')


def symbol_filter(shadow: tuple[float, float, float, str, float], uid: str) -> str:
    dx, dy, blur, color, opacity = shadow
    return (f'    <filter id="symbolShadow{uid}" x="-20%" y="-20%" width="140%" height="140%">\n'
            f'      <feDropShadow dx="{dx}" dy="{dy}" stdDeviation="{blur}" flood-color="{color}" flood-opacity="{opacity}"/>\n'
            f'    </filter>')


def symbol_placement(t: str) -> tuple[dict, str]:
    """Shared canonical symbol (path, per-type scale, disc-relative transform).

    The same glyph and transform are used by default/orb/flat so the three styles
    stay shape-identical; orb and flat additionally end up the same size because
    both place the symbol relative to the disc centre this way.
    """
    c = COLORS[t]
    glyph = GLYPHS[c["letter"]]
    sym_scale = c["scale"] * (VIEW / 2) / ORB_R
    sym_tf = (f'translate({VIEW / 2} {VIEW / 2}) scale({sym_scale:.6f}) '
              f'translate(-{ORB_CX} {ORB_CY}) scale(1 -1)')
    return glyph, sym_tf


def default_svg(t: str) -> str:
    """Bare no-circle symbol that inherits the surrounding text colour."""
    glyph, sym_tf = symbol_placement(t)
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VIEW:.0f} {VIEW:.0f}">
  <path d="{glyph['sym_path']}" transform="{sym_tf}" fill="currentColor"/>
</svg>
'''


def flat_svg(t: str) -> str:
    """Flat round badge: official disc colour (from the font) + plain symbol."""
    c = COLORS[t]
    glyph, sym_tf = symbol_placement(t)
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VIEW:.0f} {VIEW:.0f}">
  <circle cx="50" cy="50" r="50" fill="{glyph['disc_color']}"/>
  <path d="{glyph['sym_path']}" transform="{sym_tf}" fill="{c['symbol']}"/>
</svg>
'''


def build_svg(t: str) -> str:
    c = COLORS[t]
    gain = c.get("color_gain", 1.08)
    highlight = {
        "size": c.get("highlight_size", HIGHLIGHT[t]["size"]),
        "angle": c.get("highlight_angle", HIGHLIGHT[t]["angle"]),
        "opacity": c.get("highlight_opacity", HIGHLIGHT[t]["opacity"]),
    }
    body_center = c.get("body_center", [BODY_GEOMETRY[t][0] / 100, BODY_GEOMETRY[t][1] / 100])
    body_cx, body_cy = body_center[0] * VIEW, body_center[1] * VIEW
    body_r = c.get("body_radius", BODY_GEOMETRY[t][2] / VIEW) * VIEW
    glyph, sym_tf = symbol_placement(t)
    uid = t  # unique gradient id prefix so multiple SVGs can be inlined together
    body_stops = "\n".join(
        f'      <stop offset="{o}" stop-color="{brighten(b, gain)}"/>'
        for (o, _), b in zip(STOPS, c["body"])
    )
    core_opacity, mid_opacity = highlight["opacity"]
    symbol_id = c["symbol"]
    background_def = (darkness_background_gradient(uid) if t == "Darkness"
                      else background_gradient([brighten(color, gain) for color in c.get("background", BACKGROUND[t])], c.get("background_angle", -45), uid))
    darkness_inner_guide = (f'  <path d="{DARKNESS_INNER_GUIDE_PATH}" fill="url(#darknessInnerHighlightDarkness)"/>'
                            if t == "Darkness" else '')
    metal_triangle_underlay = (
        f'  <path d="{METAL_TRIANGLE_PATH}" '
        f'transform="{sym_tf} translate(347 230) scale(1.5) translate(-347 -230)" '
        f'fill="url(#metalTriangleMetal)"/>'
        if t == "Metal" else ''
    )
    shadow_attr = f' filter="url(#symbolShadow{uid})"' if t in SYMBOL_SHADOWS else ""

    return f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VIEW:.0f} {VIEW:.0f}">
  <defs>
    <clipPath id="orbClip{uid}" clipPathUnits="userSpaceOnUse"><circle cx="50" cy="50" r="50"/></clipPath>
{background_def}
{darkness_inner_highlight(uid) if t == "Darkness" else ''}
{darkness_highlight(uid) if t == "Darkness" else ''}
{metal_triangle_gradient(uid) if t == "Metal" else ''}
{symbol_filter(SYMBOL_SHADOWS[t], uid) if t in SYMBOL_SHADOWS else ''}
    <radialGradient id="body{uid}" cx="{body_cx}" cy="{body_cy}" r="{body_r}" gradientUnits="userSpaceOnUse">
{body_stops}
    </radialGradient>
{sheen_gradient(c["sheen"], uid, mid_opacity)}
{sheen_mask(uid)}
  </defs>
  <circle cx="50" cy="50" r="50" fill="url(#background{uid})"/>
{'' if t == "Darkness" else f'  <circle cx="50" cy="50" r="50" fill="url(#body{uid})" opacity="{c.get("body_opacity", 0.28)}"/>'}
{darkness_inner_guide}
{metal_triangle_underlay}
  <path d="{glyph['sym_path']}" transform="{sym_tf}" fill="{symbol_id}"{shadow_attr}/>
  <g clip-path="url(#orbClip{uid})">
{f'    <ellipse cx="80" cy="80" rx="37" ry="21" transform="rotate(-45 80 80)" fill="url(#darknessHighlight{uid})" opacity="0.9"/>' if t == "Darkness" else f'    <path d="{HIGHLIGHT_PATH}" fill="url(#sheen{uid})" mask="url(#sheenMask{uid})" opacity="{core_opacity}"/>\n    <path d="{HIGHLIGHT_CORE_PATH}" fill="#FFFFFF" opacity="{core_opacity}"/>'}
  </g>
</svg>
'''


STYLES = {"default": default_svg, "orb": build_svg, "flat": flat_svg}


def main() -> None:
    names = sys.argv[1:] if len(sys.argv) > 1 else list(COLORS)
    for t in names:
        for style, builder in STYLES.items():
            target = RAW_DIR / style / f"{t.lower()}.svg"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(builder(t))
        print(f"wrote raw/{{default,orb,flat}}/{t.lower()}.svg  scale={COLORS[t]['scale']}")


if __name__ == "__main__":
    main()
