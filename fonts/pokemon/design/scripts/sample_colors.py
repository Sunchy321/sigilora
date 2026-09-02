#!/usr/bin/env python3
"""Sample per-type colors + highlight geometry from official energy PNGs.

For each type (Grass, Fire, ...) this reads the official PNG and measures:
  - body gradient: radial buckets around the light source, excluding the
    low-saturation dark symbol and the highlight component
  - background gradient: diagonal lower-left → upper-right colors
  - symbol color: mean of the low-saturation interior region
  - sheen: brightest connected component (gloss), its center rel to orb
  - scale: IoU scale-search that best fits the font symbol onto the official
    symbol mask (saturation-based), matching the calibrated Grass=1.10 method

Writes assets/colors.json. Buckets that come up empty (dark/desaturated bodies)
are left null and must be hand-filled before building SVGs.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
PNG_DIR = ROOT / "assets" / "energy_png"
GLYPHS = json.loads((ROOT / "assets" / "glyphs.json").read_text())
OUT = ROOT / "assets" / "colors.json"

TYPES = ["Grass", "Fire", "Water", "Lightning", "Psychic", "Fighting",
         "Darkness", "Metal", "Fairy", "Dragon", "Colorless"]

# font symbol glyph per letter; the 11 types map onto these letters via the
# official order used by TCGplayer (Grass=G, Fire=R, ... Colorless=C, ...)
LETTER = {"Grass": "G", "Fire": "R", "Water": "W", "Lightning": "L",
          "Psychic": "P", "Fighting": "F", "Darkness": "D", "Metal": "M",
          "Fairy": "Y", "Dragon": "N", "Colorless": "C"}

# orb geometry in the font (c40 bbox = [0, -120, 693, 573])
ORB_CX, ORB_CY = 346.5, 226.5
ORB_R = 346.5

DEFAULT_BODY_GEOMETRY = (0.64, 0.30, 0.64)

N = 300  # orb-normalized raster canvas (orb diameter = N)
VIEW = 100.0
BASE = (N / 2) / ORB_R  # font units -> canvas units (orb fills the canvas)


def hexof(rgb) -> str:
    return "#" + "".join(f"{int(round(v)):02X}" for v in rgb)


def symbol_mask(arr: np.ndarray) -> np.ndarray:
    """Low-saturation dark interior of the orb (the symbol), on a N-canvas."""
    rgb, alpha = arr[:, :, :3].astype(float), arr[:, :, 3]
    circ = alpha > 128
    yy, xx = np.mgrid[0:N, 0:N]
    dist = np.sqrt((yy - N / 2) ** 2 + (xx - N / 2) ** 2)
    mx = np.maximum(np.maximum(rgb[:, :, 0], rgb[:, :, 1]), rgb[:, :, 2])
    mn = np.minimum(np.minimum(rgb[:, :, 0], rgb[:, :, 1]), rgb[:, :, 2])
    sat = (mx - mn) / np.maximum(mx, 1)
    return circ & (dist < 0.9 * N / 2) & (sat < 0.45) & (mx < 120)


def font_symbol_mask(pathstr: str, scale: float) -> np.ndarray:
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {N} {N}">'
           f'<g transform="translate({N / 2} {N / 2}) scale({scale * BASE}) '
           f'translate(-{ORB_CX} {ORB_CY}) scale(1 -1)">'
           f'<path d="{pathstr}" fill="black"/></g></svg>')
    Path("/tmp/_sig_scale.svg").write_bytes(svg.encode())
    subprocess.run(["rsvg-convert", "-o", "/tmp/_sig_scale.png", "/tmp/_sig_scale.svg"],
                   check=True, capture_output=True)
    return np.array(Image.open("/tmp/_sig_scale.png"))[:, :, 3] > 128


def scale_search(letter: str, official: np.ndarray) -> float:
    pathstr = GLYPHS[letter]["sym_path"]
    best, best_iou = None, 0.0
    for sc in np.arange(0.8, 1.6, 0.02):
        fm = font_symbol_mask(pathstr, float(sc))
        inter = np.logical_and(fm, official).sum()
        union = np.logical_or(fm, official).sum()
        iou = inter / max(union, 1)
        if iou > best_iou:
            best, best_iou = sc, iou
    return float(best)


def sample_type(t: str) -> dict:
    im = Image.open(PNG_DIR / f"{t}.png").convert("RGBA").resize((N, N), Image.LANCZOS)
    arr = np.array(im)
    rgb, alpha = arr[:, :, :3].astype(float), arr[:, :, 3]
    circ = alpha > 128
    yy, xx = np.mgrid[0:N, 0:N]
    dist = np.sqrt((yy - N / 2) ** 2 + (xx - N / 2) ** 2)
    rel = dist / (N / 2)
    mx = np.maximum(np.maximum(rgb[:, :, 0], rgb[:, :, 1]), rgb[:, :, 2])
    mn = np.minimum(np.minimum(rgb[:, :, 0], rgb[:, :, 1]), rgb[:, :, 2])
    sat = (mx - mn) / np.maximum(mx, 1)
    lum = rgb.mean(axis=2)

    letter = LETTER[t]
    off_mask = symbol_mask(arr)
    scale = scale_search(letter, off_mask)
    template = font_symbol_mask(GLYPHS[letter]["sym_path"], scale)
    is_sym = template & circ
    if not is_sym.any():
        is_sym = (sat < 0.48) & (mx < 120)
    # dilate the symbol mask so anti-aliased edges don't bleed into the body
    sym_d = ndimage.binary_dilation(is_sym, iterations=4)

    # Brightest connected component is the specular highlight. Exclude it from
    # all body/background statistics before sampling colors.
    inner = circ & (rel < 0.92)
    thr = np.percentile(lum[inner], 98.0)
    bright = inner & (lum >= thr)
    lbl, n = ndimage.label(bright)
    sheen_col, sheen_rel = None, None
    highlight_size, highlight_angle = [12, 15], 55
    highlight_mask = np.zeros_like(circ)
    if n:
        sizes = ndimage.sum(bright, lbl, range(1, n + 1))
        comp = lbl == 1 + int(np.argmax(sizes))
        # Include the soft halo but retain a margin around the component.
        highlight_mask = ndimage.binary_dilation(comp, iterations=12)
        sy, sx = np.where(comp)
        sheen_col = hexof(rgb[comp].mean(axis=0))
        sheen_rel = [round((sx.mean() - N / 2) / (N / 2), 3),
                     round((sy.mean() - N / 2) / (N / 2), 3)]
        if len(sx) > 2:
            covariance = np.cov(np.vstack((sx, sy)))
            values, vectors = np.linalg.eigh(covariance)
            order = np.argsort(values)[::-1]
            values, vectors = values[order], vectors[:, order]
            highlight_size = [
                round(float(np.clip(np.sqrt(values[0]) * 3.0 * VIEW / N, 6, 30)), 1),
                round(float(np.clip(np.sqrt(values[1]) * 3.0 * VIEW / N, 6, 30)), 1),
            ]
            highlight_angle = round(float(np.degrees(np.arctan2(vectors[1, 0], vectors[0, 0]))), 1)

    body = circ & (rel > 0.05) & (rel < 0.95) & ~sym_d & ~highlight_mask

    # Body gradient: sample radial buckets around the common upper-right light
    # source. Medians are stable against anti-aliasing and residual artifacts.
    bx, by, br = DEFAULT_BODY_GEOMETRY
    body_dist = np.sqrt((xx / N - bx) ** 2 + (yy / N - by) ** 2) / br
    body_cols = []
    for lo, hi in [(0.0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.1)]:
        m = body & (body_dist >= lo) & (body_dist < hi)
        body_cols.append(hexof(np.median(rgb[m], axis=0)) if m.any() else None)

    # Diagonal background gradient: lower-left is t=0, upper-right is t=1.
    diag = (xx - yy + N) / (2 * N)
    bg_cols = []
    for lo, hi in [(0.05, 0.35), (0.65, 0.95)]:
        m = body & (diag >= lo) & (diag < hi)
        bg_cols.append(hexof(np.median(rgb[m], axis=0)) if m.any() else None)

    # symbol color
    sym_px = rgb[is_sym & circ & (rel < 0.9)]
    if len(sym_px):
        sym_lum = sym_px.mean(axis=1)
        # The symbol is usually the darkest low-saturation region. Taking a
        # lower-luminance quantile avoids bevels, highlights and anti-aliasing.
        sym_px = sym_px[sym_lum <= np.percentile(sym_lum, 35)]
    sym_col = hexof(np.median(sym_px, axis=0)) if len(sym_px) else None

    # symbol scale
    return {"letter": letter, "body": body_cols, "symbol": sym_col,
            "sheen": sheen_col, "sheen_rel": sheen_rel,
            "background": bg_cols, "background_angle": -45,
            "body_center": [bx, by], "body_radius": br,
            "color_gain": 1.08,
            "body_opacity": 0.28,
            "highlight_size": highlight_size, "highlight_angle": highlight_angle,
            "highlight_opacity": [0.86, 0.34],
            "scale": scale}


def main() -> None:
    existing = json.loads(OUT.read_text()) if OUT.exists() else {}
    out = {}
    for t in TYPES:
        try:
            out[t] = sample_type(t)
            for key in ("background", "background_angle", "body_center", "body_radius", "color_gain", "body_opacity",
                        "highlight_size", "highlight_angle", "highlight_opacity"):
                if key in existing.get(t, {}):
                    out[t][key] = existing[t][key]
        except Exception as e:  # noqa: BLE001 - report and continue
            out[t] = {"error": str(e)}
        d = out[t]
        print(f"{t:11s} body={d.get('body')} symbol={d.get('symbol')} "
              f"sheen={d.get('sheen')} rel={d.get('sheen_rel')} scale={d.get('scale')}")
    OUT.write_text(json.dumps(out, indent=2))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
