# LICENSES — Pokémon TCG

This file records the asset sources and license basis for `fonts/pokemon/`.

## 1. Base energy symbol SVGs

- Location: `fonts/pokemon/raw/default/` (11 energy orbs).
- Sources and basis:
  - Symbol (letter) outlines are vector-extracted from the community font
    **EssentiarumTCG v1-COLR.otf** (vendored at `design/assets/font_src/`,
    author Nick15). The font is used **only** as an extraction source and is
    **not** redistributed with the font binary.
  - Colors and specular gloss are sampled from the official Pokémon energy PNG
    references (`design/assets/energy_png/`) and redrawn by the author; the
    SVG construction lives in `design/scripts/build_svgs.py`.
- License: The Pokémon energy artwork is © Nintendo / Creatures / GAME FREAK /
  The Pokémon Company (and related IP owners). The EssentiarumTCG community
  font is an unofficial fan work. It has not been verified whether these
  sources permit converting the graphics into glyphs, distributing them with
  the font binary, installing/embedding/redistributing, or re-licensing.
  Until that per-asset audit is completed, this font is **not** declared as
  OFL and no redistribution rights for these assets are assumed.
