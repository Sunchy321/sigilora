#!/usr/bin/env python3
"""Compare rasterized SVGs with the official energy PNG references."""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PNG_DIR = ROOT / "assets" / "energy_png"
SVG_DIR = ROOT / "svg"
TYPES = ["Grass", "Fire", "Water", "Lightning", "Psychic", "Fighting",
         "Darkness", "Metal", "Fairy", "Dragon", "Colorless"]


def load(path: Path, size: int = 300) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGBA").resize((size, size), Image.Resampling.LANCZOS))


def masks(arr: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    rgb = arr[:, :, :3].astype(float)
    alpha = arr[:, :, 3] > 128
    mx, mn = rgb.max(axis=2), rgb.min(axis=2)
    sat = (mx - mn) / np.maximum(mx, 1)
    symbol = alpha & (sat < 0.48) & (mx < 120)
    lum = rgb.mean(axis=2)
    inner = alpha & ~symbol
    threshold = np.percentile(lum[inner], 98) if inner.any() else 255
    highlight = inner & (lum >= threshold)
    return symbol, highlight


def centroid(mask: np.ndarray) -> tuple[float, float]:
    ys, xs = np.where(mask)
    if not len(xs):
        return (0.0, 0.0)
    n = mask.shape[0]
    return ((xs.mean() - n / 2) / (n / 2), (ys.mean() - n / 2) / (n / 2))


def iou(left: np.ndarray, right: np.ndarray) -> float:
    union = np.logical_or(left, right).sum()
    return float(np.logical_and(left, right).sum() / max(union, 1))


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="sigilora-energy-") as tmp:
        for typ in TYPES:
            out = Path(tmp) / f"{typ}.png"
            subprocess.run(["rsvg-convert", "-w", "300", "-h", "300", str(SVG_DIR / f"{typ}.svg"), "-o", str(out)], check=True)
            official = load(PNG_DIR / f"{typ}.png")
            generated = load(out)
            official_symbol, official_highlight = masks(official)
            generated_symbol, generated_highlight = masks(generated)
            ox, oy = centroid(official_highlight)
            gx, gy = centroid(generated_highlight)
            print(f"{typ:11s} symbol_iou={iou(official_symbol, generated_symbol):.3f} "
                  f"highlight=({ox:+.3f},{oy:+.3f})→({gx:+.3f},{gy:+.3f}) "
                  f"area={official_highlight.mean():.3f}→{generated_highlight.mean():.3f}")


if __name__ == "__main__":
    main()
