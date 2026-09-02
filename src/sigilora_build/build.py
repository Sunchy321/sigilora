"""Font build: nanoemoji base font + liga/salt/ssXX features.

Faithfully ports the predecessor build pipeline: assign Private Use Area
codepoints to every (symbol, style) glyph, stage the normalized SVGs,
run nanoemoji (COLR version from the game config), then add OpenType
features via fontTools.
"""
from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from fontTools.feaLib.builder import addOpenTypeFeatures
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph

from .model import GameData

CHAR_NAME = {
    "0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
    "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine",
    ".": "period", ",": "comma", ":": "colon", ";": "semicolon",
    "!": "exclam", "?": "question", "'": "quotesingle", '"': "quotedbl",
    "`": "grave", "(": "parenleft", ")": "parenright", "[": "bracketleft",
    "]": "bracketright", "{": "braceleft", "}": "braceright", "<": "less",
    ">": "greater", "#": "numbersign", "$": "dollar", "%": "percent",
    "&": "ampersand", "*": "asterisk", "+": "plus", "-": "hyphen",
    "/": "slash", "\\": "backslash", "=": "equal", "@": "at",
    "^": "asciicircum", "_": "underscore", "|": "bar", "~": "asciitilde",
    " ": "space", "½": "onehalf", "∞": "uni221E",
}
CHAR_NAME.update({chr(c): chr(c) for c in range(ord("a"), ord("z") + 1)})
CHAR_NAME.update({chr(c): chr(c) for c in range(ord("A"), ord("Z") + 1)})

INPUT_GLYPHS = {
    "braceleft": 0x007B, "braceright": 0x007D, "slash": 0x002F,
    "onehalf": 0x00BD, "uni221E": 0x221E,
    "zero": 0x30, "one": 0x31, "two": 0x32, "three": 0x33, "four": 0x34,
    "five": 0x35, "six": 0x36, "seven": 0x37, "eight": 0x38, "nine": 0x39,
    "bracketleft": 0x005B, "bracketright": 0x005D,
    "plus": 0x002B, "hyphen": 0x002D,
    **{chr(cp): cp for cp in range(0x41, 0x5B)},
}


def _liga_to_string(ligature: str) -> str | None:
    if not ligature:
        return None
    names = []
    for c in ligature:
        if c in CHAR_NAME:
            names.append(CHAR_NAME[c])
        else:
            code = ord(c)
            names.append(f"uni{code:04X}" if code <= 0xFFFF else f"u{code:06X}")
    return " ".join(names) or None


def _assign_codepoints(game: GameData, lite: bool):
    """Return list of (symbol_name, style, codepoint) in a deterministic order."""
    entries: list[tuple[str, str, int]] = []
    cp = 0xE000
    styles = ["default"] if lite else game.style_order
    for sym in game.symbols:
        for style in styles:
            if style in sym.svg:
                entries.append((sym.name, style, cp))
                cp += 1
    return entries


def _default_resolve(game: GameData):
    """Identity art resolver: draw each (symbol, style) glyph from svg/<style>/<file>."""
    def resolve(sym, style):
        return game.svg_dir / style / sym.svg[style]
    return resolve


def _fallback_resolve(game: GameData):
    """COLRv0-flavor art resolver: apply colr-fallback overrides — first any
    per-(symbol, style) override-art, then style-art style substitution."""
    fb = game.colr_fallback
    overrides = {(o.name, o.style): o.file for o in fb.override_art}

    def resolve(sym, style):
        file = overrides.get((sym.name, style))
        if file is not None:
            return game.svg_dir / style / file
        art_style = fb.style_art.get(style, style)
        file = sym.svg[art_style] if art_style in sym.svg else sym.svg[style]
        return game.svg_dir / art_style / file
    return resolve


def _stage_svgs(game: GameData, entries, work_dir: Path, resolve=None) -> list[str]:
    if resolve is None:
        resolve = _default_resolve(game)
    staged = []
    for name, style, cp in entries:
        sym = game.by_name(name)
        svg = resolve(sym, style)
        target = work_dir / f"emoji_u{cp:04X}.svg"
        shutil.copy2(svg, target)
        staged.append(str(target))
    return staged


def _run_nanoemoji(family: str, svgs: list[str], output_file: Path, nanoemoji: str, color_format: str) -> None:
    cmd = [
        nanoemoji,
        "--family", family,
        "--color_format", color_format,
        "--output_file", str(output_file),
        "--width", "0",
        "--ascender", "850",
        "--descender", "-150",
        "--noclip_to_viewbox",
        *svgs,
    ]
    env = dict(subprocess.os.environ)
    # nanoemoji shells out to ninja; make its sibling tools discoverable on PATH
    env["PATH"] = str(Path(nanoemoji).resolve().parent) + subprocess.os.pathsep + env.get("PATH", "")
    subprocess.run(cmd, check=True, env=env)


def _add_features(font_file: Path, game: GameData, entries, lite: bool) -> None:
    cp_by_name = {(name, style): cp for name, style, cp in entries}

    liga_rules = []
    for sym in game.symbols:
        if (sym.name, "default") not in cp_by_name:
            continue
        default_cp = cp_by_name[(sym.name, "default")]
        for lig in sym.ligature:
            seq = _liga_to_string(lig)
            if seq:
                liga_rules.append((seq, f"uni{default_cp:04X}"))

    fea = ["languagesystem DFLT dflt;", ""]
    if liga_rules:
        fea.append("feature liga {")
        for seq, glyph in liga_rules:
            fea.append(f"  sub {seq} by {glyph};")
        fea.append("} liga;")
        fea.append("")
    if not lite:
        for style in game.style_order:
            if style == "default":
                continue
            rules = [
                (f"uni{cp_by_name[(sym.name, 'default')]:04X}", f"uni{cp_by_name[(sym.name, style)]:04X}")
                for sym in game.symbols
                if (sym.name, "default") in cp_by_name and (sym.name, style) in cp_by_name
            ]
            if not rules:
                continue
            idx = game.style_order.index(style)
            fea.append(f"feature ss0{idx} {{  # Stylistic Set {idx} ({style})")
            for src, dst in rules:
                fea.append(f"  sub {src} by {dst};")
            fea.append(f"}} ss0{idx};")
            fea.append("")

    fea_path = font_file.with_suffix(".fea")
    fea_path.write_text("\n".join(fea), encoding="utf-8")

    font = TTFont(font_file)
    for name, cp in INPUT_GLYPHS.items():
        if name in font["glyf"].glyphs:
            continue
        g = Glyph()
        g.numberOfContours = 0
        g.xMin = g.yMin = g.xMax = g.yMax = 0
        font["glyf"].glyphs[name] = g
        font["hmtx"].metrics[name] = (0, 0)
        order = font.getGlyphOrder()
        order.append(name)
        font.setGlyphOrder(order)
    input_mapping = {cp: name for name, cp in INPUT_GLYPHS.items()}
    for table in font["cmap"].tables:
        if table.platformID == 0 or (table.platformID == 3 and table.platEncID in (1, 10)):
            for cp, name in input_mapping.items():
                if cp not in table.cmap:
                    table.cmap[cp] = name
    addOpenTypeFeatures(font, str(fea_path), tables=["GSUB"])
    font.save(font_file)
    fea_path.unlink(missing_ok=True)


def _to_woff2(ttf_path: Path) -> Path:
    woff2 = ttf_path.with_suffix(".woff2")
    font = TTFont(ttf_path)
    font.flavor = "woff2"
    font.save(woff2)
    return woff2


def _nanoemoji_path(game: GameData) -> str:
    # Prefer the project venv (local dev), else the one installed by pip on PATH (CI).
    venv = game.path.parent.parent / ".venv" / "bin" / "nanoemoji"
    if venv.exists():
        return str(venv)
    found = shutil.which("nanoemoji")
    if not found:
        raise FileNotFoundError("nanoemoji not found; install it (pip install -e .)")
    return found


_COLOR_FORMATS = {"v0": "glyf_colr_0", "v1": "glyf_colr_1"}


def flavor_specs(game: GameData, lite: bool) -> list[dict]:
    """Which binaries one family is built from: its primary flavor plus, when the
    family's COLR version is v1 and the game declares [colr-fallback], a COLRv0
    fallback flavor (`-v0`). The lite family's COLR version is lite-colr-version
    (default: the full one) — a lite family whose glyphs are all COLRv0-
    expressible can set it to v0 and needs no fallback."""
    color = game.colr_for(lite)
    specs = [{"suffix": "", "colr": color}]
    if color == "v1" and game.colr_fallback is not None:
        specs.append({"suffix": "-v0", "colr": "v0"})
    return specs


def _build_flavor(
    game: GameData,
    out_dir: Path,
    lite: bool,
    *,
    resolve,
    color_format: str,
    file_suffix: str = "",
    family_suffix: str = "",
):
    game_label = game.code.capitalize()
    family = f"Sigilora {game_label}{' Lite' if lite else ''}{family_suffix}"
    entries = _assign_codepoints(game, lite)
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        svgs = _stage_svgs(game, entries, work, resolve)
        stem = f"Sigilora-{game_label}{'-Lite' if lite else ''}-{game.font_version}{file_suffix}"
        ttf = out_dir / f"{stem}.ttf"
        _run_nanoemoji(family, svgs, ttf, _nanoemoji_path(game), color_format)
        _add_features(ttf, game, entries, lite)
        woff2 = _to_woff2(ttf)
    return {"family": family, "stem": stem, "ttf": ttf, "woff2": woff2, "entries": entries}


def build(game: GameData, out_dir: Path, lite: bool = False) -> list[dict]:
    """Build one font family from its flavor specs (see flavor_specs). A family
    whose COLR version is v1 and whose game declares [colr-fallback] is also
    built as a COLRv0 fallback flavor with the same glyphs/features — same
    codepoints and liga/ssXX, colour encoding downgraded to v0, a `-v0` file
    suffix, and a distinct internal family so desktop installs of both can
    coexist. A lite family set to COLRv0 is built as one v0 font."""
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for spec in flavor_specs(game, lite):
        fallback = spec["suffix"] == "-v0"
        results.append(
            _build_flavor(
                game, out_dir, lite,
                resolve=_fallback_resolve(game) if fallback else _default_resolve(game),
                color_format=_COLOR_FORMATS[spec["colr"]],
                file_suffix=spec["suffix"],
                family_suffix=" V0" if fallback else "",
            )
        )
    return results
