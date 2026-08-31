# LICENSES — Magic: The Gathering

This file records the asset sources and license basis for `fonts/magic/`.

## 1. Base symbol SVGs (default style)

- Location: `fonts/magic/raw/default/` (84 symbols)
- Source: Scryfall (`https://svgs.scryfall.io/card-symbols/...`)
- License: these are graphical renderings of Wizards of the Coast (WotC) card symbols, governed by the WotC Fan Content Policy. Neither Scryfall nor WotC grants the right to convert the graphics into glyphs, distribute them with a font binary, or re-license them (e.g., under OFL).

## 2. Style variants (original work layered on the base)

- Location: generated at build time from `fonts/magic/raw/default/` and `fonts/magic/raw/components/`; special cases kept as files under `fonts/magic/raw/static/`
- Source: original work by the project author, layered on top of the base Scryfall SVGs. The raw Scryfall files contain no shadows; the shadow style, the flat recoloring, and the special-case shadows for `100`, `1000000`, `half-white`, `half-red` and the snow flat are the author's own additions.
- License: the added layers are original work; the base glyphs underneath remain WotC/Scryfall IP.

## 3. Composition parts (components)

- Location: `fonts/magic/raw/components/` (19 parts)
- Source: not part of Scryfall's card-symbol set; the project's own decomposition parts for composing hybrid, phyrexian, loyalty-counter, and other symbols.
- License: original building blocks, combined with the Scryfall base glyphs.

## 4. Plantin-Bold font (external dependency, not committed)

- Purpose: the font used by `compose.loyalty` to convert loyalty-counter text (e.g., "+1") into paths.
- Location: `fonts/magic/external/Plantin-Bold.ttf` — not committed to the repository; you must provide it yourself (see `external/README.md`).
- License: commercial font by Monotype. Its binary is not committed or distributed. The final font embeds glyph outline paths rendered from it.
